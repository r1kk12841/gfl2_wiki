from __future__ import annotations

import argparse
import copy
import json
import os
import re
import socket
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.editor_core.bundle import stage_i18n_bundle
from tools.editor_core.transaction import RepositoryTransaction
from tools.effects_catalog import canonicalize_effects, effect_id

ALLOWED_EFFECT_TYPES = {"buff", "debuff", "effect"}
SLUG_PATTERN = re.compile(r"^[a-z0-9_-]+$")


class EditorServerError(ValueError):
    pass


class EditorServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass: type, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
        self.server_bind()
        self.server_activate()

    def server_bind(self) -> None:
        if sys.platform == "win32":
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


class EditorServerHandler(SimpleHTTPRequestHandler):
    server: EditorServer

    def __init__(self, *args: Any, **kwargs: Any):
        # We pass directory to SimpleHTTPRequestHandler
        super().__init__(*args, **kwargs)

    @property
    def repo_root(self) -> Path:
        return self.server.repo_root

    def translate_path(self, path: str) -> str:
        # Override to ensure static files are served relative to repo_root
        parsed = urlparse(path)
        clean_path = unquote(parsed.path).lstrip("/")
        candidate = (self.repo_root / clean_path).resolve()
        try:
            candidate.relative_to(self.repo_root)
        except ValueError:
            return str(self.repo_root / "__invalid_static_path__")
        return str(candidate)

    # --- HTTP Method Dispatchers ---

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.handle_health()
            return
        elif path == "/api/effects":
            self.handle_list_effects()
            return
        elif path.startswith("/api/guides/"):
            slug = unquote(path[len("/api/guides/") :])
            self.handle_get_guide(slug)
            return

        # Fall back to static files
        super().do_GET()

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/api/effects/"):
            effect_id = unquote(path[len("/api/effects/") :])
            self.handle_update_effect(effect_id)
            return
        elif path.startswith("/api/characters/"):
            slug = unquote(path[len("/api/characters/") :])
            lang = query.get("lang", ["en"])[0]
            self.handle_update_character(slug, lang)
            return
        elif path.startswith("/api/guides/"):
            slug = unquote(path[len("/api/guides/") :])
            self.handle_update_guide(slug)
            return

        self.send_json_error(HTTPStatus.NOT_FOUND, "Không tìm thấy endpoint API.")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/guides":
            self.handle_create_guide()
            return
        elif path == "/api/effects":
            self.handle_create_effect()
            return

        self.send_json_error(HTTPStatus.NOT_FOUND, "Không tìm thấy endpoint API.")

    # --- Helper Methods ---

    def read_json_payload(self, max_bytes: int = 2 * 1024 * 1024) -> dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if not length_header:
            raise EditorServerError("Thiếu header Content-Length.")
        try:
            content_length = int(length_header)
        except ValueError:
            raise EditorServerError("Header Content-Length không hợp lệ.")
        if content_length > max_bytes:
            raise EditorServerError(f"Payload vượt quá dung lượng cho phép ({max_bytes} bytes).")
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise EditorServerError(f"JSON payload không hợp lệ: {exc}")
        if not isinstance(payload, dict):
            raise EditorServerError("Payload phải là một JSON Object.")
        return payload

    def send_json(self, status: int, data: dict[str, Any]) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json_error(self, status: int, message: str) -> None:
        self.send_json(status, {"error": message})

    # --- Route Handlers ---

    def handle_health(self) -> None:
        self.send_json(
            HTTPStatus.OK,
            {
                "service": "gfl2-editor-server",
                "api_version": 1,
                "root": str(self.repo_root),
                "capabilities": ["characters", "effects", "guides"],
            },
        )

    def handle_list_effects(self) -> None:
        effects_file = self.repo_root / "data" / "effects_vi.json"
        if not effects_file.exists():
            self.send_json(HTTPStatus.OK, {"effects": []})
            return

        try:
            raw_data = json.loads(effects_file.read_text(encoding="utf-8-sig"))
            canonical = canonicalize_effects(raw_data)
        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi đọc catalog effects: {exc}")
            return

        # Compute referenced_by
        referenced_by: dict[str, list[dict[str, str]]] = {eff_id: [] for eff_id in canonical}
        for source_id, entry in canonical.items():
            for target_id in entry.get("sub_effect_ids", []):
                if target_id in referenced_by:
                    referenced_by[target_id].append(
                        {
                            "id": source_id,
                            "name_en": str(entry["name_en"]),
                            "name": str(entry.get("name", entry["name_en"])),
                        }
                    )

        rows = []
        for eff_id, entry in canonical.items():
            row = copy.deepcopy(entry)
            row["referenced_by"] = sorted(
                referenced_by[eff_id], key=lambda item: item["name_en"].casefold()
            )
            rows.append(row)
        rows.sort(key=lambda item: item["name_en"].casefold())
        self.send_json(HTTPStatus.OK, {"effects": rows})

    def handle_update_effect(self, effect_id: str) -> None:
        try:
            payload = self.read_json_payload()
        except EditorServerError as err:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(err))
            return

        new_name = str(payload.get("name", "")).strip()
        new_desc = str(payload.get("desc", "")).strip()
        new_type = str(payload.get("type", "")).strip().lower()

        if not new_name:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Tên tiếng Việt không được để trống.")
            return
        if not new_desc:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Mô tả tiếng Việt không được để trống.")
            return
        if new_type not in ALLOWED_EFFECT_TYPES:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Loại hiệu ứng phải là buff, debuff hoặc effect.")
            return

        tx = RepositoryTransaction(self.repo_root)
        try:
            with tx:
                effects_path = self.repo_root / "data" / "effects_vi.json"
                i18n_path = self.repo_root / "data" / "i18n_vi.json"

                effects_data = json.loads(effects_path.read_text(encoding="utf-8-sig"))
                i18n_data = json.loads(i18n_path.read_text(encoding="utf-8-sig"))
                canonical = canonicalize_effects(effects_data)

                if effect_id not in canonical:
                    self.send_json_error(HTTPStatus.NOT_FOUND, f"Hiệu ứng ID '{effect_id}' không tồn tại.")
                    return

                target_entry = copy.deepcopy(canonical[effect_id])
                target_entry["name"] = new_name
                target_entry["desc"] = new_desc
                target_entry["type"] = new_type

                # Process sub_effect_ids if supplied
                if "sub_effect_ids" in payload:
                    sub_ids = payload["sub_effect_ids"]
                    if not isinstance(sub_ids, list):
                        self.send_json_error(HTTPStatus.BAD_REQUEST, "sub_effect_ids phải là mảng chuỗi.")
                        return

                    # Self-reference validation
                    if effect_id in sub_ids:
                        self.send_json_error(
                            HTTPStatus.BAD_REQUEST,
                            "Không thể tự tham chiếu chính mình làm hiệu ứng con (self-reference).",
                        )
                        return

                    # Validate existence of all sub-effect IDs
                    clean_subs: list[str] = []
                    for sid in sub_ids:
                        if not isinstance(sid, str) or not sid.strip():
                            continue
                        sid = sid.strip()
                        if sid not in canonical:
                            self.send_json_error(
                                HTTPStatus.BAD_REQUEST, f"Hiệu ứng con ID '{sid}' không tồn tại."
                            )
                            return
                        if sid not in clean_subs:
                            clean_subs.append(sid)

                    target_entry["sub_effect_ids"] = clean_subs

                canonical[effect_id] = target_entry

                # Stage and commit via bundle helper
                stage_i18n_bundle(self.repo_root, tx, i18n_bundle=i18n_data, effects_data=canonical)
                tx.commit()

            # Return updated effect
            self.send_json(HTTPStatus.OK, {"effect": target_entry})

        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi lưu effect: {exc}")

    def handle_create_effect(self) -> None:
        try:
            payload = self.read_json_payload()
        except EditorServerError as err:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(err))
            return

        name_en = str(payload.get("name_en", "")).strip()
        name = str(payload.get("name", "")).strip()
        desc = str(payload.get("desc", "")).strip()
        desc_en = str(payload.get("desc_en", "")).strip()
        new_type = str(payload.get("type", "effect")).strip().lower()

        if not name_en:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Tên tiếng Anh không được để trống.")
            return
        if not name:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Tên tiếng Việt không được để trống.")
            return
        if not desc:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Mô tả tiếng Việt không được để trống.")
            return
        if new_type not in ALLOWED_EFFECT_TYPES:
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Loại hiệu ứng phải là buff, debuff hoặc effect.")
            return

        tx = RepositoryTransaction(self.repo_root)
        try:
            with tx:
                effects_path = self.repo_root / "data" / "effects_vi.json"
                i18n_path = self.repo_root / "data" / "i18n_vi.json"

                effects_data = json.loads(effects_path.read_text(encoding="utf-8-sig"))
                i18n_data = json.loads(i18n_path.read_text(encoding="utf-8-sig"))
                canonical = canonicalize_effects(effects_data)

                eff_id = effect_id(name_en)
                if eff_id in canonical or any(e["name_en"].casefold() == name_en.casefold() for e in canonical.values()):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, f"Hiệu ứng tiếng Anh '{name_en}' đã tồn tại.")
                    return

                clean_subs: list[str] = []
                if "sub_effect_ids" in payload:
                    sub_ids = payload["sub_effect_ids"]
                    if not isinstance(sub_ids, list):
                        self.send_json_error(HTTPStatus.BAD_REQUEST, "sub_effect_ids phải là mảng chuỗi.")
                        return
                    for sid in sub_ids:
                        if not isinstance(sid, str) or not sid.strip():
                            continue
                        sid = sid.strip()
                        if sid not in canonical:
                            self.send_json_error(
                                HTTPStatus.BAD_REQUEST, f"Hiệu ứng con ID '{sid}' không tồn tại."
                            )
                            return
                        if sid not in clean_subs:
                            clean_subs.append(sid)

                new_entry = {
                    "id": eff_id,
                    "name": name,
                    "name_en": name_en,
                    "desc": desc,
                    "desc_en": desc_en or desc,
                    "type": new_type,
                    "sub_effect_ids": clean_subs,
                }

                canonical[eff_id] = new_entry
                stage_i18n_bundle(self.repo_root, tx, i18n_bundle=i18n_data, effects_data=canonical)
                tx.commit()

            self.send_json(HTTPStatus.CREATED, {"effect": new_entry})
        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi tạo effect: {exc}")

    def handle_update_character(self, slug: str, lang: str) -> None:
        if not SLUG_PATTERN.match(slug):
            self.send_json_error(HTTPStatus.BAD_REQUEST, f"Slug nhân vật '{slug}' không hợp lệ.")
            return

        lang = lang.lower().strip()
        if lang not in ("en", "vi"):
            self.send_json_error(HTTPStatus.BAD_REQUEST, "Tham số lang phải là 'en' hoặc 'vi'.")
            return

        try:
            payload = self.read_json_payload()
        except EditorServerError as err:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(err))
            return

        tx = RepositoryTransaction(self.repo_root)
        try:
            with tx:
                if lang == "en":
                    char_path = self.repo_root / "data" / "characters" / f"{slug}.json"
                    if not char_path.exists():
                        self.send_json_error(HTTPStatus.NOT_FOUND, f"Nhân vật '{slug}' không tồn tại trong data/characters/.")
                        return
                    existing = json.loads(char_path.read_text(encoding="utf-8-sig"))
                    payload_slug = str(payload.get("slug", slug)).strip()
                    if payload_slug != slug:
                        self.send_json_error(HTTPStatus.BAD_REQUEST, "Không được đổi slug khi cập nhật nhân vật gốc.")
                        return
                    merged = copy.deepcopy(existing)
                    merged.update(copy.deepcopy(payload))
                    tx.stage_write(char_path, json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
                    tx.commit()
                    self.send_json(HTTPStatus.OK, {"slug": slug, "lang": "en", "path": f"data/characters/{slug}.json"})
                    return
                else:
                    i18n_path = self.repo_root / "data" / "i18n_vi.json"
                    i18n_data = json.loads(i18n_path.read_text(encoding="utf-8-sig"))
                    characters = i18n_data.get("characters")
                    if not isinstance(characters, dict) or slug not in characters:
                        self.send_json_error(
                            HTTPStatus.NOT_FOUND,
                            f"Bản ghi characters.{slug} không tồn tại trong i18n_vi.json; không tạo mới.",
                        )
                        return
                    existing = characters[slug]
                    merged = copy.deepcopy(existing)
                    merged.update(copy.deepcopy(payload))
                    characters[slug] = merged

                    stage_i18n_bundle(self.repo_root, tx, i18n_bundle=i18n_data)
                    tx.commit()
                    self.send_json(HTTPStatus.OK, {"slug": slug, "lang": "vi", "path": f"data/i18n_vi.json#characters.{slug}"})
                    return

        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi lưu nhân vật: {exc}")

    def handle_get_guide(self, slug: str) -> None:
        if not SLUG_PATTERN.match(slug):
            self.send_json_error(HTTPStatus.BAD_REQUEST, f"Slug guide '{slug}' không hợp lệ.")
            return

        guide_path = self.repo_root / "data" / "guides" / f"{slug}.json"
        if not guide_path.exists():
            self.send_json_error(HTTPStatus.NOT_FOUND, f"Guide '{slug}' không tồn tại.")
            return

        try:
            data = json.loads(guide_path.read_text(encoding="utf-8-sig"))
            self.send_json(HTTPStatus.OK, data)
        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi đọc guide: {exc}")

    def handle_update_guide(self, slug: str) -> None:
        if not SLUG_PATTERN.match(slug):
            self.send_json_error(HTTPStatus.BAD_REQUEST, f"Slug guide '{slug}' không hợp lệ.")
            return

        guide_path = self.repo_root / "data" / "guides" / f"{slug}.json"
        if not guide_path.exists():
            self.send_json_error(HTTPStatus.NOT_FOUND, f"Guide '{slug}' không tồn tại.")
            return

        try:
            payload = self.read_json_payload()
        except EditorServerError as err:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(err))
            return

        tx = RepositoryTransaction(self.repo_root)
        try:
            with tx:
                tx.stage_write(guide_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
                tx.commit()
            self.send_json(HTTPStatus.OK, {"slug": slug, "path": f"data/guides/{slug}.json"})
        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi lưu guide: {exc}")

    def handle_create_guide(self) -> None:
        try:
            payload = self.read_json_payload()
        except EditorServerError as err:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(err))
            return

        slug = str(payload.get("slug", "")).strip()
        if not SLUG_PATTERN.match(slug):
            self.send_json_error(HTTPStatus.BAD_REQUEST, f"Slug guide '{slug}' không hợp lệ.")
            return

        guide_path = self.repo_root / "data" / "guides" / f"{slug}.json"
        guide_path.parent.mkdir(parents=True, exist_ok=True)

        tx = RepositoryTransaction(self.repo_root)
        try:
            with tx:
                tx.stage_write(guide_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
                tx.commit()
            self.send_json(HTTPStatus.OK, {"slug": slug, "path": f"data/guides/{slug}.json"})
        except Exception as exc:
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Lỗi tạo guide: {exc}")


def create_editor_server(
    repo_root: Path,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> EditorServer:
    server_address = (host, port)
    return EditorServer(server_address, EditorServerHandler, repo_root=Path(repo_root))


def main() -> None:
    parser = argparse.ArgumentParser(description="GFL2 Exilium Wiki Unified Editor Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (mặc định: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen (mặc định: 8000)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    server = create_editor_server(repo_root=repo_root, host=args.host, port=args.port)
    actual_port = server.server_port
    print(f"=== GFL2 Editor Server đang chạy tại: http://{args.host}:{actual_port} ===")
    print(f"Mở Editor Hub: http://{args.host}:{actual_port}/tools/index.html")
    print("Nhấn Ctrl+C để dừng server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐang dừng Editor Server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
