"""Decode GFL2 ``LangPackageTable*.bytes`` localization files."""

from __future__ import annotations

import argparse
import csv
import json
import struct
from pathlib import Path


def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while True:
        if pos >= len(buf):
            raise ValueError("truncated varint")
        byte = buf[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7
        if shift >= 70:
            raise ValueError("varint is too long")


def parse_bytes(data: bytes) -> list[dict[str, int | str | None]]:
    if len(data) < 4:
        raise ValueError("file is shorter than its 4-byte header length")
    header_length = struct.unpack_from("<I", data, 0)[0]
    body_start = 4 + header_length
    if body_start > len(data):
        raise ValueError("header length exceeds file size")

    body = data[body_start:]
    pos = 0
    entries: list[dict[str, int | str | None]] = []
    while pos < len(body):
        tag, pos = read_varint(body, pos)
        field_number, wire_type = tag >> 3, tag & 7
        if wire_type != 2:
            raise ValueError(f"unexpected outer wire type {wire_type}, field {field_number}")
        length, pos = read_varint(body, pos)
        end = pos + length
        if end > len(body):
            raise ValueError("outer message exceeds body size")
        chunk = body[pos:end]
        pos = end

        inner_pos = 0
        record_id = None
        text = None
        while inner_pos < len(chunk):
            inner_tag, inner_pos = read_varint(chunk, inner_pos)
            inner_field, inner_wire = inner_tag >> 3, inner_tag & 7
            if inner_wire == 0:
                value, inner_pos = read_varint(chunk, inner_pos)
                if inner_field == 1:
                    record_id = value
            elif inner_wire == 2:
                inner_length, inner_pos = read_varint(chunk, inner_pos)
                inner_end = inner_pos + inner_length
                if inner_end > len(chunk):
                    raise ValueError("inner value exceeds message size")
                value = chunk[inner_pos:inner_end]
                inner_pos = inner_end
                if inner_field == 2:
                    text = value.decode("utf-8", errors="replace")
            else:
                raise ValueError(f"unexpected inner wire type {inner_wire}, field {inner_field}")
        entries.append({"id": record_id, "text": text})
    return entries


def parse_file(path: str | Path) -> list[dict[str, int | str | None]]:
    return parse_bytes(Path(path).read_bytes())


def write_outputs(source: Path, entries: list[dict], output_dir: Path | None = None) -> tuple[Path, Path]:
    destination = output_dir or source.resolve().parent
    destination.mkdir(parents=True, exist_ok=True)
    json_path = destination / f"{source.stem}_decoded.json"
    csv_path = destination / f"{source.stem}_decoded.csv"
    json_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "text"])
        writer.writerows((item["id"], item["text"]) for item in entries)
    return json_path, csv_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--no-write", action="store_true", help="validate and count entries only")
    args = parser.parse_args()

    entries = parse_file(args.path)
    print(f"total entries parsed: {len(entries)}")
    if not args.no_write:
        json_path, csv_path = write_outputs(args.path, entries, args.output_dir)
        print(f"done -> {json_path} / {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
