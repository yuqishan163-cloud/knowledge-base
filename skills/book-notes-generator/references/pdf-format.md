# PDF Format

## Contents

1. Source Markdown
2. Numbering
3. Section order
4. Rendering and verification

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

## Rendering and verification

1. Run `scripts/render_notes_pdf.py source.md output.pdf` with Python 3.10+.
2. If the default Python lacks ReportLab, load the workspace's bundled dependencies and use its Python executable, or install `reportlab>=4.0,<5` in an isolated environment.
3. Use a Chinese font with both regular and bold faces. The renderer searches common macOS and Linux font locations; pass `--regular-font` and `--bold-font` if needed. Avoid emoji in PDF headings unless the selected font is confirmed to support them.
4. Inspect PDF metadata and page count with `pdfinfo`.
5. Render all pages with `pdftoppm -png`.
6. Inspect the first page, every section transition, pages containing long lists or formulas, and the final page. For a short document, inspect every page.
7. Correct broken glyphs, orphan headings, clipped text, overlapping elements, inconsistent numbering, weak bold emphasis, and excess blank space.
8. Default to a comfortable reading size: 11.5 pt body text with approximately 20 pt leading; scale headings proportionally.
9. Use an ASCII-compatible final filename such as `financial-freedom-book-notes.pdf`. Keep the original-language title inside the document.
10. Save the final file under the active workspace's `output/pdf/` unless the user explicitly requests another visible destination. Never save the only copy under a temporary directory or the Skill installation directory.
11. Confirm the file exists, is non-empty, and opens with `pdfinfo`.
12. Deliver a standard clickable Markdown link using its absolute path. If the environment also requires a file citation, include it, but never make it the only way to access the PDF.
13. Deliver only the final PDF, not intermediate Markdown or PNGs, unless requested.
