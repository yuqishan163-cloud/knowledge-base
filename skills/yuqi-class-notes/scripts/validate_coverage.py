#!/usr/bin/env python3
"""Validate lesson classification and lesson-to-theme coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CLASSIFICATIONS = ("directly_processed", "supplemented", "missing", "unreadable")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Top-level JSON value must be an object: {path}")
    return value


def display(values: set[Any]) -> str:
    return ", ".join(map(str, sorted(values, key=lambda value: str(value)))) or "none"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("coverage", type=Path)
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="Allow missing or unreadable lessons when the final output explicitly discloses them",
    )
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
        coverage = load_json(args.coverage)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        errors.append("manifest.items must be a non-empty list")
        expected_ids: set[Any] = set()
    else:
        expected_ids = {item.get("id") for item in items if isinstance(item, dict) and item.get("id") is not None}

    manifest_expected = manifest.get("expected_video_count")
    coverage_expected = coverage.get("expected_video_count")
    if manifest_expected is not None and coverage_expected != manifest_expected:
        errors.append(
            f"expected_video_count differs: manifest={manifest_expected}, coverage={coverage_expected}"
        )

    classified: dict[str, set[Any]] = {}
    for key in CLASSIFICATIONS:
        values = coverage.get(key)
        if not isinstance(values, list):
            errors.append(f"{key} must be a list")
            classified[key] = set()
        else:
            classified[key] = set(values)

    for index, first in enumerate(CLASSIFICATIONS):
        for second in CLASSIFICATIONS[index + 1 :]:
            overlap = classified[first] & classified[second]
            if overlap:
                errors.append(f"classification overlap between {first} and {second}: {display(overlap)}")

    classified_ids = set().union(*classified.values())
    unclassified = expected_ids - classified_ids
    unknown = classified_ids - expected_ids
    if unclassified:
        errors.append(f"unclassified lessons: {display(unclassified)}")
    if unknown:
        errors.append(f"classification contains unknown lessons: {display(unknown)}")

    incomplete_ids = classified["missing"] | classified["unreadable"]
    if incomplete_ids:
        message = f"missing or unreadable lessons: {display(incomplete_ids)}"
        if args.allow_incomplete:
            warnings.append(message)
        else:
            errors.append(message + " (use --allow-incomplete only after explicit disclosure)")

    themes = coverage.get("themes")
    if not isinstance(themes, list) or not themes:
        errors.append("themes must be a non-empty list")
        themes = []

    theme_numbers: list[int] = []
    covered_ids: set[Any] = set()
    for position, theme in enumerate(themes, start=1):
        if not isinstance(theme, dict):
            errors.append(f"theme {position} must be an object")
            continue
        number = theme.get("number")
        if not isinstance(number, int):
            errors.append(f"theme {position} has a non-integer number")
        else:
            theme_numbers.append(number)
        videos = theme.get("videos")
        examples = theme.get("example_source_videos")
        if not isinstance(videos, list) or not videos:
            errors.append(f"theme {position} must list at least one source video")
            videos_set: set[Any] = set()
        else:
            videos_set = set(videos)
            covered_ids |= videos_set
        if not isinstance(examples, list) or not examples:
            errors.append(f"theme {position} has no course example source")
        else:
            example_set = set(examples)
            if not example_set <= videos_set:
                errors.append(f"theme {position} example sources must also appear in its videos list")
        if not str(theme.get("title_en", "")).strip():
            errors.append(f"theme {position} is missing title_en")
        if not str(theme.get("title_zh", "")).strip():
            errors.append(f"theme {position} is missing title_zh")

    if theme_numbers and theme_numbers != list(range(1, len(theme_numbers) + 1)):
        errors.append(f"theme numbers must be consecutive from 1; found {theme_numbers}")

    processable_ids = expected_ids - incomplete_ids
    uncovered = processable_ids - covered_ids
    unknown_theme_ids = covered_ids - expected_ids
    if uncovered:
        errors.append(f"processed lessons not mapped to a theme: {display(uncovered)}")
    if unknown_theme_ids:
        errors.append(f"themes contain unknown lessons: {display(unknown_theme_ids)}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Coverage valid: {len(expected_ids)} lesson(s) -> {len(themes)} theme(s)")
    print(f"Direct: {len(classified['directly_processed'])}")
    print(f"Supplemented: {len(classified['supplemented'])}")
    print(f"Missing: {len(classified['missing'])}")
    print(f"Unreadable: {len(classified['unreadable'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

