# Markdown → PDF Notes

These rules apply only to Markdown/PDF notes. Keep the existing Notion method and template unchanged.

## Contents

1. Approval and scope
2. Four layers
3. Source sentences
4. Choose Level 4 by book type
5. Markdown example
6. Rendering and verification

## 1. Approval and scope

- Read the complete supplied book and track chapter/spine coverage before drafting. Exclude navigation, boilerplate, advertisements, and repetitive material; retain useful reasoning, limits, and examples.
- Submit a **complete Markdown note**, not only a sample or outline, and wait for the user's explicit approval of that version before any PDF export. A request to generate notes/PDF or approval of the format alone is not approval of the content.
- Apply feedback in Markdown first. If content changes after approval, resubmit the revised version. Layout-only fixes may be made without a new content approval.
- The approved Markdown is the PDF's content source. Do not independently rewrite, shorten, append, or add an outline while rendering.
- Summarize the book itself. Do not create separate `核心概念` / `特别概念`, `个人行动` / `个人应用` / `行动清单`, or `知识连接` sections. Do not import those sections from Notion.
- Explain necessary concepts in the ordinary body; keep actions that illustrate the book's methods inside the relevant Level 4 blockquote. Removing a standalone action list does **not** remove action examples.
- Preserve the existing Notion workflow when both outputs are requested. The two outputs share source understanding, not an identical template or all of the same sections.

## 2. Four layers

| Layer | Content | Markdown | PDF |
|---|---|---|---|
| 1 | Reconstructed knowledge map, usually 3–7 themes | `## 1. 主题` | Large numbered heading |
| 2 | A central conclusion under that theme | `**完整结论**`, standalone paragraph | Bold black text, kept with its explanation |
| 3 | Mechanism, reasoning, necessary definitions and limits | Ordinary paragraphs | Regular black body text |
| 4, optional | Action example, original-book case, or key detail | `> ...` | Indented text with a left rule; may be slightly smaller |

- Organize around the book's ideas, not a mechanical copy of its table of contents. A few clear conclusions under each theme are better than a fixed quota.
- Use the four visual formats directly. Do not add `###`/`####`/`#####` headings, yellow highlighting, or `•`/`-`/`✓` prefixes to represent the deeper layers.
- Reserve standalone bold paragraphs for core conclusions. Keep Level 3 normal-weight; do not turn every explanation into another highlighted insight.
- The first two layers should make the main ideas reviewable without reading every detail. Each lower layer should add support, not restate its parent.
- Put essential qualifications in Level 3. Do not hide a limitation in Level 4 if readers need it to understand the conclusion correctly.
- Do not force all four layers under every conclusion. Omit a Level 4 block when it adds no practical or explanatory value.

## 3. Source sentences

- **Prefer the book's original sentences for Level 2.** Select a concise, self-contained sentence that expresses the conclusion and is supported by the following explanation.
- Check each excerpt against the full source. A contiguous, complete clause is acceptable if it retains the original meaning; preserve negation, conditions, uncertainty, and speaker attribution.
- Do not splice distant fragments into an apparently verbatim sentence or polish a quote while still calling it original wording. Mark meaningful omissions; if no suitable excerpt exists, use a minimal faithful paraphrase and distinguish it from a verbatim excerpt.
- Avoid AI-style balancing formulas such as `不是……而是……`, `既……又……`, `虽然……但是……`, or `不能只看……更要……` when paraphrasing. Use a direct claim. Do not invent a counterpoint merely to make the sentence sound balanced. An original sentence's meaningful contrast need not be rewritten.
- Introduce the source convention briefly: bold conclusions are original excerpts (with any exceptions identified); explanatory paragraphs and blockquotes are summaries or examples unless expressly quoted.
- Preserve historical context for forecasts and dated claims. Do not turn the author's prediction, analogy, opinion, or illustrative number into a verified current fact.

## 4. Choose Level 4 by book type

**Favor practical action examples when the book supports them.** Cases and key details are additional choices, not a replacement for actions.

| Book / passage | Preferred Level 4 |
|---|---|
| Practical, procedural, method-heavy | Action example: exact steps, checklist, formula with a worked example, diagnostic questions, or an executable demonstration |
| Conceptual or framework-heavy | A representative original-book case that clarifies the idea; a key distinction, datum, or detail when a case is unnecessary |
| Case-heavy or reflective | A compact original-book case with relevant context and outcome; an action example if the author provides an applicable method |
| Mixed | Choose per conclusion. Prefer actions when they materially improve usability; otherwise use cases/details |

- An action example belongs under its conclusion, not in a separate personal action plan. It should show how the book's method works, with enough detail to execute or understand the procedure.
- Prefer original steps and worked examples. If demonstrating an original method in a new hypothetical scenario, label it `基于原书方法的演示` and mark invented inputs as hypothetical. Do not present it as an original-book case or add unsupported prescriptions, formulas, safety claims, or success guarantees.
- A conceptual book must not be turned into a self-help checklist. When no sound actionable method exists, use a case or key detail instead.
- Cases should preserve context → relevant decision/mechanism → result. Keep only details needed to explain the parent conclusion; do not dump the story.
- Optional labels inside the quote (`行动示例：`, `原书案例：`, `关键细节：`) may clarify its role. They are not a new heading level.
- For multi-step actions, prefix every line and blank line with `>` so the entire example remains one Level 4 block. Use simple numbered or bulleted lines; do not leave later steps outside the blockquote.

## 5. Markdown example

The following is a structural template, not a quotation from a real book:

```markdown
# 《书名》

作者与已有出版信息

说明：加粗结论优先摘自原文；普通正文和引用块为归纳转述或明确标注的演示。

用三句话交代全书主旨、主要论证方向和最终落点。

## 1. 第一主题

**从原书选取的完整核心结论。**

普通正文解释结论的含义、机制和适用条件。

> 行动示例：简要说明情境与目标。
>
> 1. 原书方法的第一步。
> 2. 原书方法的第二步。
> 3. 原书规定的检查方式。

**另一条从原书选取的核心结论。**

普通正文说明作者的论证。

> 原书案例：保留必要情境、关键过程和结果，说明它支持哪个观点。

## 2. 第二主题

**从原书选取的核心结论。**

普通正文解释。

> 关键细节：补充理解这一结论所需的原书信息。
```

Default order: book title and known metadata → brief provenance note where needed → three-sentence overview → four-layer body. Do not append standalone concept/action/link sections. A separate outline is optional only when requested or already approved in Markdown; PDF bookmarks do not add body content.

## 6. Rendering and verification

### Paths and dependencies

- Use the active workspace's prescribed deliverables directory for both the Markdown approval draft and final PDF. If none is prescribed, use `output/pdf/`. Keep scratch scripts and page renders in `work/` or the workspace's designated temporary directory, not in the installed Skill.
- Resolve the Skill directory and a Python 3.10+ executable. Prefer the bundled workspace dependencies and check `import reportlab`. If unavailable, use an isolated environment with ReportLab rather than changing system Python.
- Keep the original-language title in the document. An ASCII PDF filename is a safe default.

### Render only after approval

```bash
"<python>" "<skill-dir>/scripts/render_notes_pdf.py" \
  "<approved-source.md>" "<final-output.pdf>"
```

The renderer accepts paths; it cannot know whether the user approved the source. Verify approval in the conversation before running it. Preserve the exact source file used.

- The default reading layout uses a 17.5 pt theme heading, 12 pt bold conclusions, 11.5 pt regular body, and 10.5 pt indented details with a left rule. Body leading is 19 pt; keep all text black. These sizes are defaults from the accepted test, not a forced page count.
- On macOS, use Songti SC Regular for body and Heiti SC Medium for headings/conclusions when available. Embed Chinese fonts. The script has fallback fonts for other environments; unsupported or missing glyphs must be fixed, not silently dropped.
- Use `--regular-font` and `--bold-font` for explicit font files. TTC collections may also require `--regular-font-index` / `--bold-font-index` to choose the correct face.
- Keep headings and conclusions with following explanation, allow ordinary paragraphs to flow, and preserve every line of multi-step quote blocks. Do not force each theme onto a new page.

### Verify and deliver

1. Require exit status 0 and a non-empty final PDF. Open it with `pdfinfo` and record page count, page size, and encryption status.
2. Extract PDF text with `pdfplumber` or `pdftotext`. Compare it with the approved Markdown, ignoring only formatting syntax, line wrapping, and added page headers/footers. Check that no steps, formulas, punctuation, or source excerpts were lost or changed.
3. Render **every page** with `pdftoppm` and visually inspect all pages. Check Chinese glyphs, bold weight, four-layer distinction, quote rules, clipping, overlaps, isolated headings, sparse pages, and pagination.
4. Fix rendering defects without changing approved content, rerender, and repeat the text/visual checks. If content must change, return to Markdown approval.
5. Link the exact verified PDF with a standard absolute Markdown file link in Codex desktop. Preserve the approved Markdown; do not deliver a temporary PDF, raw path, or hidden citation directive in place of the link.

If a dependency or suitable Chinese font is missing, report that limitation or resolve it in the permitted environment. Do not skip verification or claim completion from the Markdown alone.
