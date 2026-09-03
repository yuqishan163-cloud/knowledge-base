#!/usr/bin/env python3
"""Inventory class video files and detect missing numbered lessons."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}


def natural_key(path: Path) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def lesson_id(path: Path) -> int | str:
    match = re.match(r"^\s*(\d{1,4})(?=\D|$)", path.stem)
    return int(match.group(1)) if match else path.stem


def duration_seconds(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return round(float(result.stdout.strip()), 3)
    except ValueError:
        return None


def collect(source: Path) -> list[Path]:
    if source.is_file():
        if source.suffix.lower() not in VIDEO_EXTENSIONS:
            raise ValueError(f"Not a supported video file: {source}")
        return [source.resolve()]
    if not source.is_dir():
        raise FileNotFoundError(source)
    return sorted(
        (path.resolve() for path in source.rglob("*") if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS),
        key=natural_key,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Video file or folder")
    parser.add_argument("--expected-count", type=int, help="Expected numbered lessons, starting at 1")
    parser.add_argument("--output", type=Path, required=True, help="Manifest JSON path")
    args = parser.parse_args()

    if args.expected_count is not None and args.expected_count < 1:
        parser.error("--expected-count must be positive")

    try:
        paths = collect(args.source.expanduser())
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    identifiers = [lesson_id(path) for path in paths]
    numeric_ids = [value for value in identifiers if isinstance(value, int)]
    duplicate_ids = sorted({value for value in numeric_ids if numeric_ids.count(value) > 1})
    missing_ids: list[int] = []
    extra_ids: list[int] = []
    if args.expected_count is not None:
        expected = set(range(1, args.expected_count + 1))
        actual = set(numeric_ids)
        missing_ids = sorted(expected - actual)
        extra_ids = sorted(actual - expected)

    items = []
    for identifier, path in zip(identifiers, paths):
        stat = path.stat()
        items.append(
            {
                "id": identifier,
                "filename": path.name,
                "path": str(path),
                "bytes": stat.st_size,
                "duration_seconds": duration_seconds(path),
                "status": "unprocessed",
            }
        )

    count_mismatch = args.expected_count is not None and len(paths) != args.expected_count
    complete_inventory = not count_mismatch and not missing_ids and not duplicate_ids and not extra_ids
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(args.source.expanduser().resolve()),
        "expected_video_count": args.expected_count,
        "discovered_video_count": len(paths),
        "complete_inventory": complete_inventory,
        "missing_ids": missing_ids,
        "duplicate_ids": duplicate_ids,
        "extra_ids": extra_ids,
        "items": items,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Discovered: {len(paths)} video(s)")
    if args.expected_count is not None:
        print(f"Expected: {args.expected_count}")
    print(f"Missing IDs: {missing_ids or 'none'}")
    print(f"Duplicate IDs: {duplicate_ids or 'none'}")
    print(f"Manifest: {args.output.resolve()}")
    return 0 if complete_inventory else 1


if __name__ == "__main__":
    raise SystemExit(main())

