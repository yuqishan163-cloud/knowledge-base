# Independent Article PDF Format

Create a self-contained article. Keep research provenance and coverage records outside the published document.

## Source Markdown

```markdown
# Stand-alone article title

A concise subtitle that explains the article's practical value when useful.

## Outline

1. First theme
2. Second theme

## Three-sentence summary

- First sentence.
- Second sentence.
- Third sentence.

## 1. First theme

### • Core takeaway

#### - Explanation

Supporting detail. **Bold only the highest-value information.**

##### ✓ Example

Describe a concrete example directly, without mentioning where it was watched, taught, or extracted.

## Action list

- [ ] A concrete action.

## Special concepts

### Concept name

Short explanation.

## Knowledge connections

- Include only genuinely useful connections.
```

For Chinese, translate the labels while keeping the same hierarchy and numbering.

## Hierarchy markers

- Number only Level 1 themes: `1.`, `2.`, `3.`. Always include the period.
- Render Level 1 themes larger than deeper layers.
- Mark Level 2 insights with `•` and render the complete line with a light-yellow highlight.
- Mark Level 3 explanations with `-`.
- Mark Level 4 course examples with `✓`.
- Use stable markers throughout; do not mix numbered and symbolic styles below Level 1.
- Keep outline wording identical to Level 1 body headings.
- Do not add filler labels such as `Theme:` or `Point:`.

## Color and typography

- Render all text in black, including headings, body text, quotes, links, and page numbers.
- Permit only the light-yellow background highlight behind Level 2 lines.
- Default to A4 with 20 mm margins.
- Default body text to 11.5 pt with approximately 20 pt leading.
- Default Level 1 headings to 22 pt and Levels 2-4 to 18 pt.
- Use a Unicode font with complete English and Simplified Chinese glyph coverage.
- Avoid emoji unless the selected font supports them.

## Optional illustrations

- Add illustrations only when requested.
- Use deep navy `#061629`, cobalt `#276BFF`, ice blue `#57C2FF`, white `#F5F9FF`, and muted blue-gray `#AFC9E8`.
- Use a clean technology style: generous negative space, thin crisp outlines, restrained blue glow, subtle grid, and strong hierarchy.
- Avoid purple, green, yellow, portraits, creator likenesses, subtitles, watermarks, platform badges, fake UI labels, and source labels.
- Prefer 16:9 concept diagrams or illustrations. Keep embedded wording exact, or move wording into editable document captions.

## Section order

1. Stand-alone title and optional value-focused subtitle.
2. Short introduction or three-sentence summary.
3. Outline when the article is long enough to need one.
4. Numbered progressive body with natural examples.
5. Action list.
6. Special concepts, when useful.
7. Knowledge connections, when genuine.

Do not publish source metadata, links, creator or platform names, lesson mapping, coverage statements, timestamps, extraction notes, or phrases that reveal the input was a recording or course.

## Visual QA

- Render every page to PNG at 150 DPI or higher.
- Inspect every page at least once.
- Re-render after correcting any broken glyph, clipping, overlap, orphan heading, inconsistent numbering, weak emphasis, or excess blank space.
- Deliver only the final verified PDFs; keep Markdown and previews in temporary workspace folders unless the user requests them.
