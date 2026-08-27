#!/usr/bin/env python3
"""Render an approved four-layer Markdown book note without rewriting its content."""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, CondPageBreak, Frame, PageTemplate, Paragraph, Spacer


REGULAR_CANDIDATES = [
    ('/System/Library/Fonts/Supplemental/Songti.ttc', 6),
    ('/System/Library/Fonts/STHeiti Light.ttc', 1),
    ('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf', 0),
    ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 0),
    ('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 0),
]
BOLD_CANDIDATES = [
    ('/System/Library/Fonts/STHeiti Medium.ttc', 1),
    ('/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttf', 0),
    ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 0),
    ('/System/Library/Fonts/Supplemental/Songti.ttc', 1),
]
SANS_CANDIDATES = [('/System/Library/Fonts/STHeiti Light.ttc', 1)]


def register_one(name, explicit, index, candidates):
    choices = [(str(explicit), index)] if explicit else candidates
    errors = []
    for path, face in choices:
        if not Path(path).is_file():
            errors.append(f'{path}: missing')
            continue
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=face))
            return path, face
        except Exception as exc:
            errors.append(f'{path} face {face}: {exc}')
    raise RuntimeError(f'No usable Chinese font for {name}; supply an explicit font. ' + '; '.join(errors))


def register_fonts(regular=None, bold=None, regular_index=0, bold_index=0):
    normal = register_one('BookRegular', regular, regular_index, REGULAR_CANDIDATES)
    strong = register_one('BookBold', bold, bold_index, BOLD_CANDIDATES)
    register_one('BookSans', None, 0, SANS_CANDIDATES + [normal])
    pdfmetrics.registerFontFamily('BookRegular', normal='BookRegular', bold='BookBold')
    pdfmetrics.registerFontFamily('BookBold', normal='BookBold', bold='BookBold')
    pdfmetrics.registerFontFamily('BookSans', normal='BookSans', bold='BookBold')
    return normal, strong


def inline_markup(value):
    """Escape book text before applying the small supported inline syntax."""
    parts = re.split(r'(\*\*.+?\*\*)', value)
    return ''.join('<b>' + html.escape(p[2:-2]) + '</b>'
                   if p.startswith('**') and p.endswith('**') else html.escape(p)
                   for p in parts)


def styles():
    common = dict(textColor=colors.black, wordWrap='CJK', splitLongWords=True,
                  allowWidows=0, allowOrphans=0)
    return {
        'title': ParagraphStyle('Title', fontName='BookBold', fontSize=25, leading=34,
                                spaceAfter=10, keepWithNext=True, **common),
        'meta': ParagraphStyle('Metadata', fontName='BookSans', fontSize=9.3, leading=15,
                               spaceAfter=10, keepWithNext=True, **common),
        'note': ParagraphStyle('SourceNote', fontName='BookRegular', fontSize=9.5, leading=15.5,
                               spaceAfter=12, **common),
        'theme': ParagraphStyle('Theme', fontName='BookBold', fontSize=17.5, leading=25,
                                spaceBefore=18, spaceAfter=9, keepWithNext=True, **common),
        'core': ParagraphStyle('Core', fontName='BookBold', fontSize=12, leading=20,
                               spaceBefore=10, spaceAfter=6, keepWithNext=True, **common),
        'body': ParagraphStyle('Body', fontName='BookRegular', fontSize=11.5, leading=19,
                               spaceAfter=7, **common),
        'quote': ParagraphStyle('Detail', fontName='BookRegular', fontSize=10.5, leading=17.5,
                                leftIndent=18, rightIndent=6, spaceBefore=1, spaceAfter=12,
                                **common),
    }


class DetailParagraph(Paragraph):
    """Left rule survives Paragraph splitting across pages."""
    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(colors.HexColor('#A8ADB3'))
        self.canv.setLineWidth(1.25)
        self.canv.line(4, 1, 4, self.height - 1)
        self.canv.restoreState()
        super().draw()


def markdown_blocks(text):
    """Group ordinary wrapped lines and complete multiline blockquotes."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('>'):
            quote = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                quote.append(re.sub(r'^\s*> ?', '', lines[i]))
                i += 1
            yield 'quote', '\n'.join(quote)
            continue
        heading = re.match(r'^(#{1,5})\s+(.+)$', line)
        if heading:
            level = len(heading.group(1))
            # Existing legacy Markdown remains readable, without its old yellow blocks.
            kind = {1:'title', 2:'theme', 3:'core', 4:'body', 5:'quote'}[level]
            yield kind, heading.group(2)
            i += 1
            continue
        if re.fullmatch(r'\*\*[^*]+\*\*', line):
            yield 'core', line[2:-2]
            i += 1
            continue
        if line == '---':
            yield 'space', ''
            i += 1
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip():
            next_line = lines[i].strip()
            if (next_line.startswith(('>', '#')) or next_line == '---'
                    or re.fullmatch(r'\*\*[^*]+\*\*', next_line)):
                break
            paragraph.append(next_line)
            i += 1
        yield 'body', '\n'.join(paragraph)


def quote_markup(value):
    # Preserve line breaks, including blank quote lines and numbered action steps.
    return '<br/>'.join(inline_markup(line) for line in value.split('\n'))


def parse_markdown(text, style):
    story = []
    in_prelude = True
    after_title = False
    for kind, value in markdown_blocks(text):
        if kind == 'space':
            story.append(Spacer(1, 4 * mm))
            continue
        if kind == 'title':
            after_title = True
        elif kind == 'theme':
            in_prelude = False
            after_title = False
            story.append(CondPageBreak(115))
        elif kind == 'body' and in_prelude:
            if after_title and len(value) < 180 and ('｜' in value or '|' in value):
                kind = 'meta'
            elif '原文' in value and ('转述' in value or '归纳' in value):
                kind = 'note'
            after_title = False
        cls = DetailParagraph if kind == 'quote' else Paragraph
        markup = quote_markup(value) if kind == 'quote' else inline_markup(value)
        # Preserve ordinary multiline numbered/bulleted lists if present in approved Markdown.
        if kind == 'body' and any(re.match(r'^(?:\d+[.)]|[-*])\s', l) for l in value.splitlines()):
            markup = '<br/>'.join(inline_markup(l) for l in value.splitlines())
        font = pdfmetrics.getFont(style[kind].fontName)
        missing = sorted({c for c in value if not c.isspace() and ord(c) not in font.face.charToGlyph})
        if missing:
            raise ValueError(f'Missing glyphs in {kind}: {missing}; select a suitable Chinese font')
        story.append(cls(markup, style[kind]))
    return story


class BookDocument(BaseDocTemplate):
    def __init__(self, output, title):
        super().__init__(str(output), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=19*mm, bottomMargin=19*mm, title=title,
                         subject='Four-layer book notes from approved Markdown', pageCompression=1)
        self.running_title = title
        self.theme_number = 0
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='reading', frames=[frame], onPage=self.page_chrome))

    def page_chrome(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont('BookSans', 8)
        if doc.page > 1:
            title = self.running_title
            while title and pdfmetrics.stringWidth(title, 'BookSans', 8) > self.width:
                title = title[:-1]
            canvas.drawString(self.leftMargin, A4[1] - 11*mm, title)
        canvas.drawCentredString(A4[0]/2, 10*mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'Theme':
            self.theme_number += 1
            key = f'theme-{self.theme_number}'
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=0)


def render(source, output, regular=None, bold=None, regular_index=0, bold_index=0):
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve():
        raise ValueError('Source Markdown and output PDF must be different files')
    text = source.read_text(encoding='utf-8')
    register_fonts(regular, bold, regular_index, bold_index)
    title = next((v for k,v in markdown_blocks(text) if k == 'title'), source.stem)
    story = parse_markdown(text, styles())
    if not story:
        raise ValueError('Source Markdown is empty')
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BookDocument(output, title)
    doc.build(story)
    return doc.page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Complete Markdown explicitly approved by the user')
    parser.add_argument('output', type=Path)
    parser.add_argument('--regular-font')
    parser.add_argument('--bold-font')
    parser.add_argument('--regular-font-index', type=int, default=0)
    parser.add_argument('--bold-font-index', type=int, default=0)
    args = parser.parse_args()
    render(args.source, args.output, args.regular_font, args.bold_font,
           args.regular_font_index, args.bold_font_index)
    print(args.output.resolve())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
