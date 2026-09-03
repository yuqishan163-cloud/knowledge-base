# Coverage and Summary Schema

Create a machine-checkable `coverage.json` before drafting final notes.

## Required JSON shape

```json
{
  "expected_video_count": 21,
  "directly_processed": [1, 2, 3, 4],
  "supplemented": [7],
  "missing": [],
  "unreadable": [],
  "themes": [
    {
      "number": 1,
      "title_en": "A useful English title",
      "title_zh": "对应的中文标题",
      "videos": [1],
      "example_source_videos": [1]
    },
    {
      "number": 2,
      "title_en": "A consolidated theme",
      "title_zh": "合并后的主题",
      "videos": [2, 3],
      "example_source_videos": [2]
    }
  ]
}
```

Use integer lesson identifiers. If source files do not have numeric identifiers, use stable string identifiers consistently in both the manifest and coverage map.

## Classification rules

- `directly_processed`: transcript, subtitles, audio, or hard subtitles from the actual video were read.
- `supplemented`: the lesson itself was unavailable or unreadable and a clearly labeled secondary source was used.
- `missing`: no usable source was available.
- `unreadable`: the file existed but could not be decoded or extracted.

Every expected lesson must appear in exactly one classification list. Classification lists must not overlap.

## Theme rules

- Number themes consecutively from 1.
- Cover every expected lesson in at least one theme.
- Give every theme at least one `example_source_videos` entry.
- Ensure example source lessons also occur in that theme's `videos` list.
- Keep English and Chinese titles semantically equivalent.
- Permit one lesson to support multiple themes when the content genuinely does so.

## Reporting count changes

Record lesson-to-theme count changes and mappings only in `coverage.json` and the internal delivery audit. Do not place them in the published article.

Use the internal mapping to prove completeness, but present only the consolidated ideas and natural examples in the final document. Never publish lesson identifiers, input-medium labels, coverage statements, creator or platform names, timestamps, or extraction details.
