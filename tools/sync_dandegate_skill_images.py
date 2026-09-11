"""Audit and synchronize character skill/range images with Dandegate.

The default mode is read-only. Pass ``--apply`` to update JSON mappings and save
authoritative images that are not already present in a character asset folder.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import unicodedata
import urllib.request
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "characters"
ASSET_DIR = ROOT / "assets" / "images" / "characters"
USER_AGENT = "gfl2-wiki-image-audit/1.0 (+https://dandegate.net/)"
STATE_MARKER = "window.__REACT_QUERY_STATE__"

# Local data occasionally uses an older/alternate English localization while
# Dandegate exposes the current global name. Keep these explicit and scoped to
# one doll so similarly named skills elsewhere cannot be matched accidentally.
SKILL_NAME_ALIASES = {
    "faelynn": {
        normalize: reference
        for normalize, reference in {
            "Hunting Instinct I": "Hunter's Instinct I",
            "Hunting Instinct II": "Hunter's Instinct II",
            "Hunting Instinct III": "Hunter's Instinct III",
        }.items()
    },
    "florence": {"Precision Anesthesia": "Precision Anethesia"},
    "liushih": {
        "We Fight as One": "Shared Vengeance",
        "Point-Defense Autocannon": "Gatling Cannon",
    },
    "mityl": {
        "Assault Shot": "Ambush",
        "Arc Shadow Assault": "Hologram Strike",
    },
    "tololo": {"Sync Standstill": "Call of the Stars"},
}


@dataclass(frozen=True)
class ReferenceSkill:
    name: str
    skill_type: str
    icon_url: str | None
    range_url: str | None


def fetch(url: str) -> bytes:
    encoded_url = quote(url, safe=":/?=&%")
    request = urllib.request.Request(encoded_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(char for char in value if char.isalnum())


NORMALIZED_SKILL_NAME_ALIASES = {
    slug: {normalize_name(local): normalize_name(reference) for local, reference in aliases.items()}
    for slug, aliases in SKILL_NAME_ALIASES.items()
}


def parse_reference(slug: str, html: bytes) -> list[ReferenceSkill]:
    text = html.decode("utf-8")
    marker = text.find(STATE_MARKER)
    object_start = text.find("{", marker) if marker >= 0 else -1
    if object_start < 0:
        context = text[max(0, marker - 80) : marker + 160] if marker >= 0 else text[:240]
        raise ValueError(
            f"{slug}: React Query state not found (bytes={len(html)}, marker={marker}, "
            f"context={context!r})"
        )
    state, _ = json.JSONDecoder().raw_decode(text[object_start:])
    doll = next(
        query["state"]["data"]
        for query in state["queries"]
        if query.get("queryKey", [None])[0] == "doll-v3"
    )
    return [
        ReferenceSkill(
            name=skill["name"],
            skill_type=skill.get("skillType") or "",
            icon_url=skill.get("imageUrl"),
            range_url=(skill.get("rangeMap") or {}).get("imageUrl"),
        )
        for skill in doll.get("skills", [])
    ]


def iter_local_skills(value: Any, breadcrumb: str = "") -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_breadcrumb = f"{breadcrumb}.{key}" if breadcrumb else key
            if key == "skills" and isinstance(child, list):
                for index, skill in enumerate(child):
                    if isinstance(skill, dict) and isinstance(skill.get("name"), str):
                        yield f"{child_breadcrumb}[{index}]", skill
            if key != "skills":
                yield from iter_local_skills(child, child_breadcrumb)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_local_skills(child, f"{breadcrumb}[{index}]")


def color_mask(raw: bytes, size: int = 96) -> bytes:
    with Image.open(io.BytesIO(raw)) as image:
        rgba = image.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        mask = bytearray()
        pixels = (
            rgba.get_flattened_data()
            if hasattr(rgba, "get_flattened_data")
            else rgba.getdata()
        )
        for red, green, blue, alpha in pixels:
            saturated = max(red, green, blue) - min(red, green, blue) >= 38
            mask.append(1 if alpha >= 32 and saturated and max(red, green, blue) >= 90 else 0)
    return bytes(mask)


def mask_similarity(left: bytes, right: bytes) -> float:
    intersection = sum(a and b for a, b in zip(left, right))
    union = sum(a or b for a, b in zip(left, right))
    return 1.0 if union == 0 else intersection / union


def local_image_masks(directory: Path) -> list[tuple[Path, bytes]]:
    result: list[tuple[Path, bytes]] = []
    for path in sorted(directory.glob("*")):
        if path.suffix.casefold() not in {".png", ".webp", ".jpg", ".jpeg"}:
            continue
        try:
            mask = color_mask(path.read_bytes())
        except Exception:
            continue
        result.append((path, mask))
    return result


def safe_stem(name: str) -> str:
    stem = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return stem or "skill"


def preferred_match(paths: list[Path], field: str, current: str | None) -> Path:
    if current:
        current_name = Path(current).name.casefold()
        for path in paths:
            if path.name.casefold() == current_name:
                return path
    suffix = "range" if field == "range_image" else "icon"
    return sorted(paths, key=lambda path: (suffix not in path.stem.casefold(), len(path.name), path.name))[0]


def unique_destination(directory: Path, name: str, field: str) -> Path:
    suffix = "range" if field == "range_image" else "icon"
    base = f"{safe_stem(name)}-{suffix}"
    candidate = directory / f"{base}.png"
    counter = 2
    while candidate.exists():
        candidate = directory / f"{base}-{counter}.png"
        counter += 1
    return candidate


def nested_slot_path(
    directory: Path,
    breadcrumb: str,
    reference: ReferenceSkill,
    field: str,
) -> Path | None:
    match = re.fullmatch(r"summons\[(\d+)\]\.skills\[(\d+)\]", breadcrumb)
    if not match:
        return None
    summon_number = int(match.group(1)) + 1
    skill_number = int(match.group(2)) + 1
    kind = normalize_name(reference.skill_type)
    if kind == "passive":
        stem = f"summon{summon_number}-passive{skill_number}"
    else:
        stem = f"summon{summon_number}-skill{skill_number}"
    suffix = "range" if field == "range_image" else "icon"
    return directory / f"{stem}-{suffix}.png"


def main_slot_path(
    directory: Path,
    slug: str,
    skill_index: int,
    reference: ReferenceSkill,
    field: str,
    current: str | None,
) -> Path:
    type_to_stem = {
        "basicattack": "skill1",
        "skill1": "skill2",
        "skill2": "skill3",
        "skill3": "ult",
        "passive": "passive",
    }
    stem = type_to_stem.get(normalize_name(reference.skill_type))
    if skill_index >= 5 or stem is None:
        if current and current.startswith(f"assets/images/characters/{slug}/"):
            return ROOT / current
        stem = f"skill{skill_index + 1}"
    if field == "range_image":
        return directory / f"{stem}-range.png"
    if stem == "passive":
        if current:
            current_path = ROOT / current
            if current_path.name in {"passive.png", "passive-icon.png"}:
                return current_path
        if (directory / "passive.png").exists():
            return directory / "passive.png"
        return directory / "passive-icon.png"
    return directory / f"{stem}-icon.png"


def reference_for_local_skill(
    skill: dict[str, Any],
    breadcrumb: str,
    slug: str,
    reference_by_name: dict[str, list[ReferenceSkill]],
    references: list[ReferenceSkill],
) -> ReferenceSkill | None:
    local_name = normalize_name(skill["name"])
    lookup_name = NORMALIZED_SKILL_NAME_ALIASES.get(slug, {}).get(local_name, local_name)
    candidates = reference_by_name.get(lookup_name, [])
    main_match = re.fullmatch(r"skills\[(\d+)\]", breadcrumb)
    if main_match:
        index = int(main_match.group(1))
        expected_types = ["basicattack", "skill1", "skill2", "skill3", "passive"]
        if index < len(expected_types):
            expected = expected_types[index]
            typed = [item for item in references if normalize_name(item.skill_type) == expected]
            if len(typed) == 1:
                return typed[0]
            typed_named = [item for item in candidates if normalize_name(item.skill_type) == expected]
            if len(typed_named) == 1:
                return typed_named[0]
    return candidates[0] if len(candidates) == 1 else None


def save_png(raw: bytes, destination: Path) -> None:
    with Image.open(io.BytesIO(raw)) as image:
        image.convert("RGBA").save(destination, "PNG", optimize=True)


def relative_asset_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write mappings and missing images")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("slugs", nargs="*")
    args = parser.parse_args()

    json_paths = sorted(DATA_DIR.glob("*.json"))
    if args.slugs:
        requested = set(args.slugs)
        json_paths = [path for path in json_paths if path.stem in requested]

    html_by_slug: dict[str, bytes] = {}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(fetch, f"https://dandegate.net/dolls/{path.stem}"): path.stem
            for path in json_paths
        }
        for future in as_completed(futures):
            slug = futures[future]
            try:
                html_by_slug[slug] = future.result()
            except Exception as exc:
                errors.append(f"{slug}: page fetch failed: {exc}")

    references: dict[str, list[ReferenceSkill]] = {}
    urls: set[str] = set()
    for slug, html in html_by_slug.items():
        try:
            references[slug] = parse_reference(slug, html)
            for skill in references[slug]:
                if skill.icon_url:
                    urls.add(skill.icon_url)
                if skill.range_url:
                    urls.add(skill.range_url)
        except Exception as exc:
            errors.append(str(exc))

    raw_by_url: dict[str, bytes] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                raw_by_url[url] = future.result()
            except Exception as exc:
                errors.append(f"asset fetch failed {url}: {exc}")

    changed_files = 0
    mapping_changes = 0
    saved_images = 0
    replaced_images = 0
    matched_skills = 0
    unmatched: list[str] = []
    changes: list[str] = []

    for json_path in json_paths:
        slug = json_path.stem
        if slug not in references:
            continue
        data = json.loads(json_path.read_text(encoding="utf-8"))
        directory = ASSET_DIR / slug
        local_masks = local_image_masks(directory)
        reference_by_name: dict[str, list[ReferenceSkill]] = {}
        for reference in references[slug]:
            reference_by_name.setdefault(normalize_name(reference.name), []).append(reference)

        file_changed = False
        claimed_destinations: dict[Path, str] = {}
        for breadcrumb, skill in iter_local_skills(data):
            reference = reference_for_local_skill(
                skill, breadcrumb, slug, reference_by_name, references[slug]
            )
            if reference is None:
                candidates = reference_by_name.get(normalize_name(skill["name"]), [])
                unmatched.append(
                    f"{slug}:{breadcrumb} {skill['name']!r} -> {len(candidates)} reference matches"
                )
                continue
            matched_skills += 1
            for field, url in (("icon", reference.icon_url), ("range_image", reference.range_url)):
                if not url or url not in raw_by_url:
                    continue
                raw = raw_by_url[url]
                reference_mask = color_mask(raw)
                current = skill.get(field)
                main_match = re.fullmatch(r"skills\[(\d+)\]", breadcrumb)
                if main_match:
                    destination = main_slot_path(
                        directory,
                        slug,
                        int(main_match.group(1)),
                        reference,
                        field,
                        current,
                    )
                else:
                    scored_paths = sorted(
                        ((mask_similarity(reference_mask, mask), path) for path, mask in local_masks),
                        key=lambda item: (-item[0], len(item[1].name), item[1].name),
                    )
                    best_score = scored_paths[0][0] if scored_paths else 0.0
                    minimum_score = 0.68 if field == "range_image" else 0.88
                    matching_paths = [
                        path for score, path in scored_paths
                        if score >= max(minimum_score, best_score - 0.015)
                    ]
                    if current and (ROOT / current).exists():
                        destination = ROOT / current
                    elif nested_destination := nested_slot_path(
                        directory, breadcrumb, reference, field
                    ):
                        destination = nested_destination
                    elif matching_paths:
                        destination = preferred_match(matching_paths, field, current)
                    else:
                        destination = unique_destination(directory, skill["name"], field)

                if (
                    destination in claimed_destinations
                    and claimed_destinations[destination] != url
                ):
                    destination = nested_slot_path(
                        directory, breadcrumb, reference, field
                    ) or unique_destination(directory, skill["name"], field)
                claimed_destinations[destination] = url

                existing_score = -1.0
                if destination.exists():
                    try:
                        existing_score = mask_similarity(reference_mask, color_mask(destination.read_bytes()))
                    except Exception:
                        existing_score = -1.0
                minimum_score = 0.55 if field == "range_image" else 0.88
                if existing_score < minimum_score:
                    existed = destination.exists()
                    if args.apply:
                        save_png(raw, destination)
                    local_masks.append((destination, reference_mask))
                    if existed:
                        replaced_images += 1
                        changes.append(
                            f"REPLACE {relative_asset_path(destination)} score={existing_score:.3f}"
                        )
                    else:
                        saved_images += 1
                        changes.append(f"SAVE {relative_asset_path(destination)}")

                desired = relative_asset_path(destination)
                if current != desired:
                    skill[field] = desired
                    mapping_changes += 1
                    file_changed = True
                    changes.append(f"MAP  {slug}:{breadcrumb}.{field}: {current!r} -> {desired}")

        if file_changed:
            changed_files += 1
            if args.apply:
                json_path.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"{mode}: characters={len(json_paths)} reference_pages={len(references)} "
        f"matched_skills={matched_skills} changed_files={changed_files} "
        f"mapping_changes={mapping_changes} saved_images={saved_images} "
        f"replaced_images={replaced_images}"
    )
    for change in changes:
        print(change)
    if unmatched:
        print(f"UNMATCHED ({len(unmatched)}):")
        for item in unmatched:
            print(item)
    if errors:
        print(f"ERRORS ({len(errors)}):", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
