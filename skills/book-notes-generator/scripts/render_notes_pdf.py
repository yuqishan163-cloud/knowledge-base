#!/usr/bin/env python3
"""Render hierarchical Chinese Markdown book notes as a polished PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer


REGULAR_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf",
]

BOLD_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttf",
]


def find_font(explicit: str | None, candidates: list[str]) -> str:
    if explicit:
        path = Path(explicit)
        if not path.is_file():
            raise FileNotFoundError(path)
        return str(path)
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError("No Chinese font found; pass --regular-font and --bold-font")


def inline_markup(value: str) -> str:
    pieces = re.split(r"(\*\*.+?\*\*)", value)
    rendered = []
    for piece in pieces:
        if piece.startswith("**") and piece.endswith("**"):
            rendered.append(f"<b>{html.escape(piece[2:-2])}</b>")
        else:
            rendered.append(html.escape(piece))
    return "".join(rendered)


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    ink = colors.black
    return {
        "title": ParagraphStyle("BookTitle", parent=base["Title"], fontName="BookBold", fontSize=28, leading=39, alignment=TA_CENTER, textColor=ink, spaceAfter=15 * mm),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName="BookBold", fontSize=22, leading=31, textColor=ink, spaceBefore=7 * mm, spaceAfter=3 * mm, keepWithNext=True),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontName="BookBold", fontSize=18, leading=27, textColor=ink, spaceBefore=5 * mm, spaceAfter=2 * mm, keepWithNext=True),
        "h4": ParagraphStyle("H4", parent=base["Heading4"], fontName="BookRegular", fontSize=18, leading=27, textColor=ink, leftIndent=4 * mm, spaceBefore=4 * mm, spaceAfter=1.5 * mm, keepWithNext=True),
        "h5": ParagraphStyle("H5", parent=base["Heading5"], fontName="BookRegular", fontSize=18, leading=27, textColor=ink, leftIndent=8 * mm, spaceBefore=3 * mm, spaceAfter=1 * mm, keepWithNext=True),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="BookRegular", fontSize=11.5, leading=20, textColor=ink, spaceAfter=2.5 * mm, wordWrap="CJK"),
        "quote": ParagraphStyle("Quote", parent=base["BodyText"], fontName="BookRegular", fontSize=11.5, leading=20, leftIndent=7 * mm, rightIndent=5 * mm, borderColor=ink, borderWidth=1.5, borderPadding=(1 * mm, 0, 1 * mm, 4 * mm), textColor=ink, spaceAfter=3 * mm, wordWrap="CJK"),
        "list": ParagraphStyle("List", parent=base["BodyText"], fontName="BookRegular", fontSize=11.5, leading=20, leftIndent=2 * mm, textColor=ink, wordWrap="CJK"),
    }


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("BookRegular", 9)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, str(doc.page))
    canvas.restoreState()


def parse_markdown(text: str, style: dict[str, ParagraphStyle]):
    story = []
    list_items: list[tuple[str, str]] = []

    def flush_list() -> None:
        nonlocal list_items
        if not list_items:
            return
        ordered = all(kind == "ordered" for kind, _ in list_items)
        items = [ListItem(Paragraph(inline_markup(value), style["list"]), leftIndent=4 * mm) for _, value in list_items]
        options = {"bulletType": "1" if ordered else "bullet", "leftIndent": 8 * mm, "bulletFontName": "BookRegular", "bulletFontSize": 10}
        if ordered:
            options["start"] = "1"
        story.append(ListFlowable(items, **options))
        story.append(Spacer(1, 2 * mm))
        list_items = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            flush_list()
            continue
        match = re.match(r"^(#{1,5})\s+(.+)$", line)
        if match:
            flush_list()
            level = len(match.group(1))
            key = "title" if level == 1 else f"h{level}"
            if level > 1:
                minimum_space = {2: 38, 3: 30, 4: 24, 5: 20}[level]
                story.append(CondPageBreak(minimum_space * mm))
            story.append(Paragraph(inline_markup(match.group(2)), style[key]))
            if level == 1:
                story.append(Spacer(1, 3 * mm))
            continue
        ordered = re.match(r"^\d+[.)]\s+(.+)$", line)
        bullet = re.match(r"^[-*]\s+(?:\[[ xX]\]\s*)?(.+)$", line)
        if ordered:
            list_items.append(("ordered", ordered.group(1)))
        elif bullet:
            list_items.append(("bullet", bullet.group(1)))
        elif line.startswith(">"):
            flush_list()
            story.append(Paragraph(inline_markup(line[1:].strip()), style["quote"]))
        elif line == "---":
            flush_list()
            story.append(Spacer(1, 4 * mm))
        else:
            flush_list()
            story.append(Paragraph(inline_markup(line), style["body"]))
    flush_list()
    return story


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--regular-font")
    parser.add_argument("--bold-font")
    args = parser.parse_args()

    regular = find_font(args.regular_font, REGULAR_CANDIDATES)
    bold = find_font(args.bold_font, BOLD_CANDIDATES)
    pdfmetrics.registerFont(TTFont("BookRegular", regular))
    pdfmetrics.registerFont(TTFont("BookBold", bold))
    pdfmetrics.registerFontFamily("BookRegular", normal="BookRegular", bold="BookBold")
    pdfmetrics.registerFontFamily("BookBold", normal="BookBold", bold="BookBold")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(args.output), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm, title=args.source.stem)
    story = parse_markdown(args.source.read_text(encoding="utf-8"), styles())
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
