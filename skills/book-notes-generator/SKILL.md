---
name: book-notes-generator
description: Read complete books from EPUB, PDF, TXT, Markdown, or other supplied files and extract high-value ideas with Progressive Summarization into reusable Notion pages or polished PDF reading notes. Use when the user asks Codex to read a whole book for them, distill it into layered notes, add practical actions or distinctive concepts, connect it to their knowledge base, preview or create a Notion book-note page, or export layered book notes as PDF.
---

# Book Notes Generator

Turn a complete book into a compact knowledge asset that supports fast review, application, and future creation. Optimize for the user's future projects and decisions.

## Workflow

1. Confirm the source file is readable and identify its format.
2. Read the complete book before drafting conclusions.
3. Confirm the requested output: Notion, PDF, or both. Default to Notion when the user mentions their knowledge base; otherwise ask when the destination is unclear.
4. For Notion, inspect the destination database, schema, and current book-note template. Search for existing pages with the same title; create a fresh page by default and preserve older notes.
5. Classify the book's dominant style and choose the appropriate depth.
6. Build the knowledge structure independently of the original table of contents.
7. Draft and quality-check the complete note.
8. If the user requests a preview, create only a short representative preview in the requested destination and wait for approval.
9. Write the complete output, verify it in its final form, and return the Notion link or PDF file.

## Read the complete source

- For EPUB, run `scripts/extract_epub.py <book.epub> --output-dir <temporary-directory>` and inspect `manifest.json` plus every extracted spine document.
- For PDF, use the available PDF-reading workflow and verify all pages were processed.
- For TXT or Markdown, inspect the whole file in chunks.
- Exclude navigation, copyright boilerplate, advertisements, repeated headers, and publisher back matter from synthesis.
- Track coverage by chapter or spine item. Do not infer a whole-book note from the cover, synopsis, table of contents, scattered highlights, or web summaries.
- If extraction is incomplete, encrypted, or corrupted, stop before Notion writing and report the exact limitation.

## Apply the capture filter

Retain information that meets at least one criterion:

- Inspiration: opens a useful direction or question.
- Usefulness: can improve a project, task, decision, or behavior.
- Personal relevance: connects to the user's goals, work, recurring problems, or prior thinking.
- Novelty: challenges an assumption or supplies a memorable new model.

Remove repeated explanations, authorial setup, emotional padding, generic advice, and case details that do not transfer. Preserve examples when they explain causality, show a procedure, establish limits, or make an action executable.

Read `references/note-method.md` before synthesizing. It defines book-style selection, layering, application depth, and quality gates.

## Build progressive layers

Use nested Notion toggles so each layer expands into the next:

- Level 1 — Knowledge map: 3–7 short phrases or short sentences. Avoid labels such as `问题：答案`.
- Level 2 — Bold insight: a decisive, memorable claim under each Level 1 theme.
- Level 3 — Supporting information: explanation, reasoning, boundaries, and only the necessary examples.
- Optional Level 4 — Action example: add beneath Level 3 for practical books when a formula, checklist, script, worked example, or concrete procedure materially improves execution.

Keep Personal Application separate from the nested knowledge map. Put its strongest actions in the template's action callout.

## Adapt to the book

- Framework-heavy books: emphasize architecture, causal relationships, distinctions, and reusable models.
- Practical books: preserve exact steps, formulas, checklists, decision questions, and representative worked examples. Add Level 4 action toggles where useful.
- Case-heavy books: compress stories into context → decision → result → transferable lesson.
- Reflective or psychological books: distinguish the author's interpretation from evidence and turn applicable ideas into prompts or experiments.
- Time-sensitive domains such as finance, health, law, software, and platform growth: label historical claims and verify current facts before recommending action.

## Choose the output structure

- Notion: use nested toggles so Level 1 expands to Level 2, then Level 3, with optional Level 4 action examples.
- PDF: place a compact outline before the body; number only Level 1 themes (`1.`, `2.`, `3.`), then mark deeper layers with `•` for bold Level 2 insights, `-` for Level 3 explanations, and `✓` for optional Level 4 action examples. Use black text throughout.
- Both: synthesize once, then render the same knowledge structure into both formats. Do not independently rewrite the ideas.

## Write to Notion

Read `references/notion-format.md` before any Notion write.

- Use the user's existing book database and current template. Fetch them each time; do not assume the schema is unchanged.
- Duplicate the existing template when possible, then update the new page's properties and content.
- Populate other template fields as supported by the source: title, author, source type, category, tags, status, dates, rating, cover, or other current properties. Never invent unknown metadata.
- Keep “特别概念” for distinctive, surprising, author-specific, or memorable concepts. Leave it empty or omit it when no concept earns inclusion.
- Add “知识连接” only for strong, useful relationships. Search existing notes first and link the actual Notion pages. Leave the section empty or omit it when connections are weak.
- Do not delete comments or older pages unless the user explicitly asks.
- After writing, fetch the page and verify properties, nesting, bold text, toggles, callouts, links, and missing template sections.

## Export PDF

Read `references/pdf-format.md` before creating a PDF.

1. Create the final PDF-source Markdown under the active workspace's `tmp/pdfs/`. Use the hierarchy in `references/pdf-format.md`; represent Notion callouts as ordinary sections and do not simulate toggles.
2. Resolve an absolute path for the Skill directory and for a Python 3.10+ executable. Prefer the workspace's bundled dependency runtime when available, and confirm that the selected Python can import ReportLab.
3. Choose an ASCII-compatible final filename under the active workspace's `output/pdf/`. Keep the original-language book title inside the PDF.
4. Run the renderer with absolute paths: `<python> <skill-dir>/scripts/render_notes_pdf.py <source.md> <output.pdf>`. Pass `--regular-font` and `--bold-font` only when a specific font has been selected or the defaults lack Chinese glyphs.
5. Require a successful renderer exit, then confirm the final PDF exists and is non-empty. Do not treat the Markdown source or a temporary PDF as the deliverable.
6. Inspect metadata and page count with `pdfinfo`, render every page to PNG with `pdftoppm`, and visually inspect every rendered page. Fix clipped text, broken glyphs, poor page breaks, weak hierarchy, or inconsistent numbering, then rerun the checks.
7. Deliver only the verified PDF with a standard Markdown file link whose target is the absolute local path: `[打开 PDF](/absolute/path/book-notes.pdf)`.
8. In Codex desktop, use the Markdown link as the primary delivery method. Do not use `:codex-file-citation{...}` there: the directive may be hidden without producing a persistent attachment. Do not wrap the link in backticks or show only a plain path.

## Quality gate

Before delivery, confirm:

- The full source was covered.
- A reader can understand the thesis in under one minute from the three-sentence summary and Level 1 map.
- Every Level 2 insight is supported by Level 3 content.
- Practical advice includes enough detail to perform it.
- Examples add transfer value rather than length.
- Actions are observable and specific.
- Special concepts are genuinely distinctive.
- Knowledge links are real and useful.
- The hierarchy is visually correct in the fetched Notion page.
- For PDF, the outline matches the numbered body and every rendered page is legible.
- No repeated idea appears in multiple sections without a new purpose.

## Improvement rule

Treat this as an MVP. Record unusual failures, but update the reusable method only when the same issue appears in at least two books or the failure risks factual accuracy, data loss, or unusable output.
