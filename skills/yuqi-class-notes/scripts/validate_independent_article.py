#!/usr/bin/env python3
"""Reject published drafts that expose recording or course provenance."""

from __future__ import annotations

import argparse
from pathlib import Path


BANNED_PHRASES = (
    "视频来源",
    "来源：",
    "来源:",
    "本视频",
    "视频中",
    "视频例子",
    "视频示例",
    "片中",
    "博主",
    "讲师",
    "课程中",
    "本节课",
    "观看",
    "视频时长",
    "时间戳",
    "source video",
    "in the video",
    "in this course",
    "the instructor",
    "watch the video",
    "timestamp",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()

    article = args.draft.read_text(encoding="utf-8")
    lowered = article.lower()
    hits = []
    for phrase in BANNED_PHRASES:
        haystack = lowered if phrase.isascii() else article
        needle = phrase.lower() if phrase.isascii() else phrase
        if needle in haystack:
            hits.append(phrase)

    if hits:
        print("Independent-article validation failed:")
        for phrase in hits:
            print(f"- {phrase}")
        return 1

    print("Independent-article validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
