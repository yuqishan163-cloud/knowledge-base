---
name: book-notes-generator
description: Read complete books from EPUB, PDF, TXT, Markdown, or other supplied files and extract high-value ideas with Progressive Summarization into reusable Notion pages or Markdown reading notes that require user approval before PDF export. Use when the user asks Codex to read a whole book, distill layered notes, add practical actions or distinctive concepts, connect it to their knowledge base, preview or create a Notion book-note page, or generate Markdown/PDF book summaries.
---

# Book Notes Generator

Turn a complete book into a compact knowledge asset that supports fast review, application, and future creation. Optimize for the user's future projects and decisions.

## Workflow

1. Confirm the source file is readable and identify its format.
2. Read the complete book before drafting conclusions.
3. Confirm the requested output: Notion, Markdown/PDF, or both. Default to Notion when the user mentions their knowledge base; otherwise ask when the destination is unclear.
4. For Notion, inspect the destination database, schema, and current book-note template. Search for existing pages with the same title; create a fresh page by default and preserve older notes.
5. Classify the book's dominant style and choose the appropriate depth.
6. Build the knowledge structure independently of the original table of contents.
7. Draft and quality-check the complete note.
8. For Notion, if the user requests a preview, create only a short representative preview in the requested destination and wait for approval. Otherwise retain the existing complete-write and readback workflow.
9. For Markdown/PDF, deliver the **complete Markdown note** and stop for explicit user approval. A short sample, approval of a format, or the initial request for a PDF does not approve the complete content. Apply requested revisions in Markdown and wait again before exporting.
10. Write the approved/requested final output for its mode, verify it, and return the Notion link or PDF file. A Markdown-only request ends with the Markdown; do not export automatically.

## Read the complete source

- For EPUB, run `scripts/extract_epub.py <book.epub> --output-dir <temporary-directory>` and inspect `manifest.json` plus every extracted spine document.
- For PDF, use the available PDF-reading workflow and verify all pages were processed.
- For TXT or Markdown, inspect the whole file in chunks.
- Exclude navigation, copyright boilerplate, advertisements, repeated headers, and publisher back matter from synthesis.
- Track coverage by chapter or spine item. Do not infer a whole-book note from the cover, synopsis, table of contents, scattered highlights, or web summaries.
- If extraction is incomplete, encrypted, or corrupted, stop before writing notes or exporting and report the exact limitation.

## Apply the capture filter

Retain information that meets at least one criterion:

- Inspiration: opens a useful direction or question.
- Usefulness: can improve a project, task, decision, or behavior.
- Personal relevance: connects to the user's goals, work, recurring problems, or prior thinking.
- Novelty: challenges an assumption or supplies a memorable new model.

Remove repeated explanations, authorial setup, emotional padding, generic advice, and case details that do not transfer. Preserve examples when they explain causality, show a procedure, establish limits, or make an action executable.

For Notion, read `references/note-method.md` before synthesizing; its existing method, application sections, and quality gates are unchanged. For Markdown/PDF, read `references/pdf-format.md` before drafting; it defines the PDF-specific synthesis and approval rules. Do not apply the Notion-only separate action list, special-concept section, or knowledge links to PDF notes.

## Build progressive layers

### Notion — existing behavior

Use nested Notion toggles so each layer expands into the next:

- Level 1 — Knowledge map: 3–7 short phrases or short sentences. Avoid labels such as `问题：答案`.
- Level 2 — Bold insight: a decisive, memorable claim under each Level 1 theme.
- Level 3 — Supporting information: explanation, reasoning, boundaries, and only the necessary examples.
- Optional Level 4 — Action example: add beneath Level 3 for practical books when a formula, checklist, script, worked example, or concrete procedure materially improves execution.

Keep Personal Application separate from the nested knowledge map. Put its strongest actions in the template's action callout.

### Markdown/PDF

Use **large numbered theme headings → standalone bold core conclusions → normal explanatory paragraphs → indented blockquotes**. Level 4 remains optional: prefer actionable examples for practical books; use original-book cases or key details for conceptual/case-heavy books. Choose per idea in mixed books, favoring useful action examples when supported. See `references/pdf-format.md` for source-quotation and example rules.

## Adapt to the book

- Framework-heavy books: emphasize architecture, causal relationships, distinctions, and reusable models.
- Practical books: preserve exact steps, formulas, checklists, decision questions, and representative worked examples. Use the existing Level 4 action toggles in Notion; use Level 4 blockquotes in Markdown/PDF.
- Case-heavy books: compress stories into context → decision → result → transferable lesson.
- Reflective or psychological books: distinguish the author's interpretation from evidence. In Notion, retain prompts or experiments for applicable ideas; in Markdown/PDF, choose supported Level 4 material by book type without inventing personal recommendations.
- Time-sensitive domains such as finance, health, law, software, and platform growth: label historical claims and verify current facts before recommending action.

## Choose the output structure

- Notion: use nested toggles so Level 1 expands to Level 2, then Level 3, with optional Level 4 action examples.
- Markdown/PDF: follow the four visual levels in `references/pdf-format.md`, with no separate core/special concepts, personal action/application, or knowledge-connection sections. Retain necessary definitions in explanatory paragraphs and practical examples inside Level 4. Prefer exact source sentences for bold conclusions; avoid formulaic AI-style balancing sentences.
- Both: share the full-source reading and factual basis, but prepare the two output structures separately. Keep all existing Notion template sections and workflow. Deliver the complete PDF-source Markdown for approval; do not export Notion blocks or write its extra sections into the PDF.

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

Read `references/pdf-format.md` before drafting or exporting.

1. Save and deliver a complete Markdown approval draft in the workspace's deliverables directory. Wait for explicit approval of that version. Keep scratch files in `work/` (or the workspace's prescribed temporary directory).
2. After approval, render that exact Markdown. Do not silently add an outline, rewrite, shorten, or add sections. Substantive content changes require a revised Markdown and renewed approval; layout-only corrections do not.
3. Resolve the Skill directory and a Python 3.10+ executable; prefer the bundled workspace runtime and confirm ReportLab is available. Follow workspace output conventions; otherwise use `output/pdf/` for the final PDF.
4. Run `<python> <skill-dir>/scripts/render_notes_pdf.py <approved.md> <output.pdf>` with absolute paths. Use explicit font options only when needed. The renderer does not establish user approval; check it in the conversation before invoking it.
5. Confirm a successful renderer exit and a non-empty PDF. Compare extracted PDF text to the approved Markdown, ignoring only markup, wrapping, and page furniture. Inspect metadata, render every page with `pdftoppm`, and visually check every page. Correct rendering defects and repeat verification.
6. Deliver the verified PDF using an absolute Markdown file link: `[打开 PDF](/absolute/path/book-notes.pdf)`. Preserve the approved Markdown. In Codex desktop, do not substitute a `:codex-file-citation{...}` directive, a temporary file, or an unlinked path.

## Quality gate

Before delivery, confirm:

- The full source was covered.
- A reader can understand the thesis in under one minute from the three-sentence summary and Level 1 map.
- Every Level 2 insight is supported by Level 3 content.
- Practical advice includes enough detail to perform it.
- Examples add transfer value rather than length.
- Actions are observable and specific.
- For Notion, special concepts are genuinely distinctive, knowledge links are real and useful, and the hierarchy is visually correct in the fetched page.
- For PDF, the complete Markdown was explicitly approved; bold source excerpts were checked against the book; Level 4 fits the book and favors useful action examples without forcing them; no standalone concept/application/link sections were added; the PDF matches the approved content and every page is legible.
- No repeated idea appears in multiple sections without a new purpose.

## Improvement rule

Treat this as an MVP. Record unusual failures, but update the reusable method only when the same issue appears in at least two books or the failure risks factual accuracy, data loss, or unusable output.
