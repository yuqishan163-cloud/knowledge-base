"""Run with Python/ReportLab and usable Chinese fonts: python -m unittest discover -s tests."""
import importlib.util
import unittest
from pathlib import Path

from reportlab.platypus import Paragraph

spec = importlib.util.spec_from_file_location('renderer', Path(__file__).parents[1] / 'scripts/render_notes_pdf.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        renderer.register_fonts()

    def test_four_layers_are_distinct_and_content_is_preserved(self):
        source = '# 测试书\n\n## 1. 主题\n\n**原文结论。**\n\n解释原理。\n\n> 原书案例：具体情境。'
        paragraphs = [p for p in renderer.parse_markdown(source, renderer.styles()) if isinstance(p, Paragraph)]
        self.assertEqual([p.style.name for p in paragraphs], ['Title','Theme','Core','Body','Detail'])
        self.assertEqual([p.getPlainText() for p in paragraphs], ['测试书','1. 主题','原文结论。','解释原理。','原书案例：具体情境。'])

    def test_action_steps_stay_in_one_quote_with_line_breaks(self):
        source = '> 行动示例：验证方法。\n>\n> 1. 写下假设。\n> 2. 测量结果。\n> 3. 比较差异。\n\n后续正文。'
        story = renderer.parse_markdown(source, renderer.styles())
        self.assertEqual(len(story), 2)
        quote = story[0]
        self.assertIsInstance(quote, renderer.DetailParagraph)
        self.assertEqual(quote.text.count('<br/>'), 4)
        for step in ['1. 写下假设。','2. 测量结果。','3. 比较差异。']:
            self.assertIn(step, quote.getPlainText())
        self.assertEqual(story[1].getPlainText(), '后续正文。')

    def test_long_quote_remains_a_quote_when_split(self):
        source = '> ' + '这是需要跨页保留的案例细节。' * 35
        quote = renderer.parse_markdown(source, renderer.styles())[0]
        quote.wrap(220, 1000)
        parts = quote.split(220, 85)
        self.assertEqual(len(parts), 2)
        self.assertTrue(all(isinstance(p, renderer.DetailParagraph) for p in parts))
        for part in parts:
            self.assertEqual(part.style.name, 'Detail')

    def test_wrapped_paragraph_and_inline_special_characters(self):
        source = '第一行解释\n第二行解释\n\n> **案例**：比较 <AI> & 人。'
        story = renderer.parse_markdown(source, renderer.styles())
        self.assertEqual(len(story), 2)
        self.assertIn('第一行解释', story[0].getPlainText())
        self.assertIn('第二行解释', story[0].getPlainText())
        self.assertIsInstance(story[1], renderer.DetailParagraph)
        self.assertEqual(story[1].getPlainText(), '案例：比较 <AI> & 人。')

    def test_source_cannot_be_overwritten_by_output(self):
        with self.assertRaisesRegex(ValueError, 'different files'):
            renderer.render('same.md', 'same.md')


if __name__ == '__main__':
    unittest.main()
