---
name: yuqi-class-notes
description: Turn a complete class, course, lecture, workshop, webinar, YouTube video, playlist, or folder of segmented local videos into a polished, stand-alone article and verified PDF notes. Use when Codex must inventory every lesson, extract subtitles or transcribe audio, prove internal coverage, remove source-medium framing from the published article, consolidate repetition, create matching English and Chinese versions, optionally add consistent blue technology illustrations, and export visually verified documents.
---

# Yuqi Class Notes

## Overview

Process the complete supplied material before drafting. Preserve practical information and attach an evidence-grounded example to every main point. Keep all provenance, extraction, and coverage details internal. Make the final document read as an original, self-contained article.

Create separate English and Chinese PDFs when bilingual output is requested. Keep their structure and meaning aligned.

## Published-Article Rule

Treat recordings, subtitles, transcripts, filenames, creators, platforms, and links only as research inputs. Never expose that research workflow in the visible article.

- Do not include source metadata, platform names, links, creator names, lesson counts, coverage tables, timestamps, transcription notes, or processing limitations in the article.
- Do not use provenance framing such as `视频来源`, `来源`, `本视频`, `视频中`, `视频例子`, `视频示例`, `片中`, `博主`, `讲师`, `课程中`, `本节课`, `观看`, `时长`, or `时间戳`.
- Do not write phrases such as `the source video`, `in the video`, `in this course`, `the instructor`, `watch`, or `timestamp` in the published English version.
- Present ideas directly. Convert `视频例子` or `视频示例` into `举例`, `比如`, or `例如`; convert `视频中演示了……` into a direct procedural statement.
- Use `视频` only when indispensable to the article's actual subject, such as an article about video production. Never use it to identify the input medium or provenance.
- Apply the rule to the title, cover, abstract, body, examples, captions, callouts, headers, footers, appendices, and document metadata.
- Keep coverage and provenance evidence under `<workspace>/tmp/class-video/`; do not copy it into the deliverable.

## Required Workflow

### 1. Establish the source set

Identify the source type:

- a YouTube video or playlist;
- one local video;
- a folder of lesson clips;
- video files plus subtitle or transcript files.

Record the expected lesson count when it is stated or inferable from stable numbering. Treat filenames such as `001`, `002`, and `007` as lesson identifiers, not as presentation order alone.

For a local folder, run:

```bash
python3 "<skill-dir>/scripts/inventory_videos.py" \
  "<video-folder>" \
  --expected-count <N> \
  --output "<workspace>/tmp/class-video/manifest.json"
```

Do not begin the final synthesis until every expected item is either directly processed or explicitly marked missing, unreadable, or supplemented.

### 2. Extract the course content

Use this evidence order:

1. supplied sidecar subtitle or transcript files (`.srt`, `.vtt`, `.txt`, `.md`);
2. embedded subtitle tracks;
3. an official transcript from the source page;
4. audio transcription;
5. hard-subtitle OCR as a fallback.

On macOS, compile and run the bundled Vision OCR helper only when the text is visibly burned into the video:

```bash
swiftc -module-cache-path "<workspace>/tmp/swift-module-cache" \
  "<skill-dir>/scripts/ocr_hardsub_video.swift" \
  -o "<workspace>/tmp/class-video/ocr_hardsub_video"

"<workspace>/tmp/class-video/ocr_hardsub_video" \
  "<video-file>" 2 > "<workspace>/tmp/class-video/<lesson-id>.jsonl"
```

Adjust the sampling interval when subtitles change faster than the default two seconds. Treat OCR as noisy evidence and reconcile repeated or partial lines before summarizing.

Use third-party notes or web summaries only as labeled supplementation. Never present them as proof that a video was directly watched or transcribed.

### 3. Build a coverage map before writing

Read [references/coverage-and-summary-schema.md](references/coverage-and-summary-schema.md) and create `<workspace>/tmp/class-video/coverage.json`.

Map every expected lesson to at least one final theme. A lesson may appear in more than one theme when necessary. Record count changes in the internal coverage file and delivery audit only; never place them in the published article.

Validate the map:

```bash
python3 "<skill-dir>/scripts/validate_coverage.py" \
  "<workspace>/tmp/class-video/manifest.json" \
  "<workspace>/tmp/class-video/coverage.json"
```

Resolve every reported gap before claiming complete coverage. If the user elects to proceed with missing material, label the limitation in the summary and delivery note.

After that explicit decision, rerun the validator with `--allow-incomplete`. This permits delivery with a visible limitation; it does not permit calling the coverage complete.

### 4. Synthesize without unnecessary repetition

Create one fact structure from the source evidence, then render it in the requested language or languages. Do not independently invent the two language versions.

Apply these content rules:

- retain practical methods, prompts, steps, warnings, and decision rules;
- remove statements that repeat the same meaning without adding a useful detail;
- preserve meaningful distinctions between similar lessons;
- give every numbered theme at least one concrete example grounded in the processed material;
- keep example provenance internal and rewrite examples as natural article examples;
- keep timestamps only in internal evidence files;
- avoid adding external facts unless clearly labeled as context;
- write the English version first and the Chinese version second when the user requests that order;
- keep numbering, examples, and section order matched across translated versions.

Use the structure in [references/pdf-format.md](references/pdf-format.md). Keep the outline wording identical to the numbered body headings.

Before rendering, validate that the draft has no source-medium framing:

```bash
python3 "<skill-dir>/scripts/validate_independent_article.py" \
  "<workspace>/tmp/pdfs/course-summary-chinese.md"
```

Resolve every reported phrase. If the article's actual subject requires the word `视频`, manually confirm that each occurrence describes the topic rather than the input source.

### Optional illustration style

Add illustrations only when the user requests images or a visual document.

- Use the `design-taste-frontend` Skill to set the visual direction and `imagegen` when an AI-generated raster image is appropriate.
- Keep one fixed system: deep navy `#061629`, cobalt blue `#276BFF`, ice blue `#57C2FF`, white `#F5F9FF`, and muted blue-gray `#AFC9E8`.
- Use a clean technology style with generous negative space, crisp thin outlines, restrained glow, subtle grid texture, and clear information hierarchy.
- Prefer 16:9 diagrams or concept illustrations. Use asymmetry only when it improves hierarchy.
- Do not use purple, green, yellow, generic multicolor gradients, portraits, creator likenesses, subtitles, watermarks, platform badges, or fake source labels.
- Preserve required wording exactly when an image contains text. Otherwise prefer diagrams without embedded text and place editable captions in the document.
- Make every illustration materially distinct from the input screenshot; do not pass off a slight hue shift as a redesign.

### 5. Create the PDF source files

Write final Markdown under `<workspace>/tmp/pdfs/`. Use ASCII-compatible filenames. For bilingual work, create two sources and two PDFs, for example:

- `course-summary-english.md` → `course-summary-english.pdf`
- `course-summary-chinese.md` → `course-summary-chinese.pdf`

Do not change approved wording while rendering. Use headings and markers to express hierarchy; do not reproduce UI toggles or unsupported enhanced Markdown.

### 6. Render and verify every PDF

Confirm ReportLab, then render with absolute paths:

```bash
python3 -c "import reportlab"

python3 "<skill-dir>/scripts/render_course_pdf.py" \
  "<workspace>/tmp/pdfs/course-summary-english.md" \
  "<workspace>/output/pdf/course-summary-english.pdf"
```

Supply `--regular-font` and `--bold-font` when the default candidates lack Chinese glyphs.

Require a non-empty output and inspect metadata:

```bash
test -s "<workspace>/output/pdf/course-summary-english.pdf"
pdfinfo "<workspace>/output/pdf/course-summary-english.pdf"
pdftoppm -png -r 150 \
  "<workspace>/output/pdf/course-summary-english.pdf" \
  "<workspace>/tmp/pdfs/course-summary-english-page"
```

Visually inspect every rendered page. Correct broken glyphs, clipping, overlaps, orphan headings, inconsistent numbering, excessive blank space, or mismatched bilingual structure, then render and inspect again.

## Completion Gate

Do not deliver until all applicable checks pass:

- expected source count is known or the uncertainty is disclosed;
- every source is classified as direct, supplemented, missing, or unreadable;
- every expected lesson appears in the coverage map;
- lesson count and consolidated-theme count are recorded internally when they differ;
- every numbered theme contains a natural, evidence-grounded example;
- English and Chinese versions have matching theme numbers and examples;
- the final article contains no source-medium framing or provenance section;
- the independent-article validator passes before rendering;
- requested illustrations follow the fixed navy/cobalt/ice-blue technology style;
- all visible text, including page numbers, is black;
- every PDF page has been visually inspected;
- final PDFs are stored under `<workspace>/output/pdf/`, not only in a temporary or Skill folder.

## Delivery

Lead with the result. Link each verified PDF once using its absolute local path. Briefly report:

- whether internal coverage passed;
- any genuine missing or unreadable material that affects reliability, without inserting it into the article;
- number of consolidated themes, only in the delivery message when useful;
- whether every PDF page passed visual inspection.

Tell the user exactly what remains incomplete if any completion-gate item could not be satisfied.
