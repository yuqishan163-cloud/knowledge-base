# PDF Format

## Contents

1. Source Markdown
2. Numbering
3. Section order
4. Execution checklist

## Source Markdown

Create one final Markdown file as the PDF source. Use this structure:

```markdown
# 书名

## 大纲

1. 第一主题
2. 第二主题
3. 第三主题

## 三句话总结

- 第一句
- 第二句
- 第三句

## 1 第一主题

### ◆ **核心洞察**

#### • 解释标题

普通说明文字。**最高价值的信息加粗。**

##### → 行动示例

具体步骤、公式、清单或例子。

## 行动清单

- [ ] 具体行动

## 特别概念

### 概念名称

简短解释。

## 知识连接

- 只写真正有用的连接。
```

Do not reproduce Notion toggles or enhanced Markdown tags in PDF source.

## Hierarchy markers

- Number only Level 1 themes: `1`, `2`, `3`.
- Mark Level 2 insights with `◆`.
- Mark Level 3 explanations with `•`.
- Mark optional Level 4 action examples with `→`.
- Keep each marker stable throughout the document; do not mix numbered and symbolic styles below Level 1.
- Keep the outline wording identical to Level 1 body headings.
- Do not add labels such as `主题：` or `观点：`.

## Section order

1. Title and available book metadata.
2. Outline as the first content section.
3. Three-sentence summary.
4. Numbered progressive body.
5. Action list.
6. Special concepts, when useful.
7. Knowledge connections, when genuine.

The outline must appear before the summary and detailed body.

## Execution checklist

Complete every step. A successful render alone is not completion.

### 1. Prepare paths and dependencies

- Resolve the active workspace, the absolute Skill directory, and a Python 3.10+ executable. When available, load the workspace's bundled dependency paths and use its Python, `pdfinfo`, and `pdftoppm` executables.
- Confirm ReportLab before rendering:

```bash
"<python>" -c "import reportlab"
```

- If the import fails, use the bundled Python. If no bundled runtime is available, install `reportlab>=4.0,<5` in an isolated environment and test the import again.
- Create these workspace paths:
  - Source: `<workspace>/tmp/pdfs/<ascii-name>.md`
  - Final PDF: `<workspace>/output/pdf/<ascii-name>.pdf`
  - Page previews: `<workspace>/tmp/pdfs/<ascii-name>-page`
- Keep the original-language book title inside the document. Use an ASCII-compatible filename such as `financial-freedom-book-notes.pdf`.

### 2. Render the final PDF

Run the bundled renderer with absolute paths:

```bash
"<python>" "<skill-dir>/scripts/render_notes_pdf.py" \
  "<workspace>/tmp/pdfs/<ascii-name>.md" \
  "<workspace>/output/pdf/<ascii-name>.pdf"
```

The renderer searches common macOS and Linux Chinese fonts. When the user chooses a font, or the defaults lack Chinese glyphs, add both `--regular-font <absolute-path>` and `--bold-font <absolute-path>`. Avoid emoji unless the selected font supports them.

Require exit status 0 and a non-empty final file:

```bash
test -s "<workspace>/output/pdf/<ascii-name>.pdf"
```

Never keep the only deliverable in a temporary directory or the Skill installation directory.

### 3. Verify structure and appearance

Inspect metadata and render every page:

```bash
"<pdfinfo>" "<workspace>/output/pdf/<ascii-name>.pdf"
"<pdftoppm>" -png -r 150 \
  "<workspace>/output/pdf/<ascii-name>.pdf" \
  "<workspace>/tmp/pdfs/<ascii-name>-page"
```

- Confirm the PDF opens, is not encrypted, and has the expected page count and page size.
- Visually inspect every generated PNG. For long documents, inspect at minimum every page once at normal detail, then inspect pages with dense lists, formulas, or section transitions more closely.
- Correct broken glyphs, orphan headings, clipped or overlapping text, inconsistent numbering, weak bold emphasis, and excess blank space. Render and verify again after every correction.
- Default to a comfortable reading size: 11.5 pt body text with approximately 20 pt leading; scale headings proportionally.

### 4. Deliver the verified file

- Deliver only the final PDF unless the user requests the Markdown or page previews.
- In Codex desktop, insert one standard Markdown file link using the absolute local path:

```markdown
[打开 PDF](/absolute/path/book-notes.pdf)
```

- Use the Markdown link as the primary delivery method. Do not use `:codex-file-citation{...}` in Codex desktop because it may be hidden without producing a persistent attachment.
- Do not wrap the live link in backticks or a code block. Do not show only a plain path.
- The link target must be the verified final PDF under the workspace's `output/pdf/`, not a temporary file.

### Failure handling

- ReportLab import failure: switch to the bundled Python or install ReportLab in an isolated environment, then retry.
- Missing Chinese glyphs: supply verified regular and bold Chinese font files and rerender.
- Missing `pdfinfo` or `pdftoppm`: resolve the bundled Poppler executables; do not skip PDF verification.
- Output exists only under `tmp/`: render or copy the verified final PDF into `output/pdf/` before delivery.
- Link fails to open: confirm the target still exists, then resend the same existing PDF with the absolute-path Markdown link above. Regenerating the PDF is unnecessary when file validation passed.
