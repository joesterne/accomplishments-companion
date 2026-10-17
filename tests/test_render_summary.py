import base64
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / '.agents/skills/accomplishments-companion/scripts/render_summary.py'
spec = importlib.util.spec_from_file_location('render_summary', HELPER)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
FIXTURE = json.loads((ROOT / 'examples/demo-summary.json').read_text())


class DocumentReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_hidden = 0
        self.text = []
        self.scripts = []
        self.script_id = None
        self.headings = []
        self.current_heading = None
        self.language = None
        self.accomplishments = {}
        self.current_accomplishment = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.in_hidden += 1
        if tag == 'script':
            self.script_id = attrs.get('id')
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag in ('h1', 'h2'):
            self.current_heading = tag
        if tag == 'li' and attrs.get('id', '').startswith('accomplishment-'):
            self.current_accomplishment = attrs['id']
            self.accomplishments[self.current_accomplishment] = ''

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_hidden -= 1
            self.script_id = None
        if tag in ('h1', 'h2'):
            self.current_heading = None
        if tag == 'li':
            self.current_accomplishment = None

    def handle_data(self, data):
        if self.script_id == 'plain-text-data':
            self.scripts.append(data)
        if not self.in_hidden:
            self.text.append(data)
            if self.current_heading:
                self.headings.append((self.current_heading, data))
            if self.current_accomplishment:
                self.accomplishments[self.current_accomplishment] += data


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.parent = Path(self.directory.name) / 'outputs'
        self.data = copy.deepcopy(FIXTURE)

    def render(self, data=None):
        paths = renderer.render(self.data if data is None else data, self.parent)
        html = Path(paths['html_path']).read_text()
        text = Path(paths['text_path']).read_text()
        reader = DocumentReader()
        reader.feed(html)
        return paths, html, text, reader

    def test_three_examples_have_matching_text_and_accessible_structure(self):
        paths, _html, text, reader = self.render()
        self.assertTrue(Path(paths['html_path']).is_absolute())
        self.assertEqual(reader.language, 'en')
        self.assertEqual(sum(tag == 'h1' for tag, content in reader.headings), 1)
        self.assertEqual(len(reader.accomplishments), 3)
        for entry in self.data['accomplishments']:
            self.assertEqual(reader.accomplishments['accomplishment-' + entry['id']], entry['text'])
            self.assertIn(entry['text'], text)
        self.assertEqual(base64.b64decode(''.join(reader.scripts)).decode('utf-8'), text)
        self.assertIn('FICTIONAL DEMO', text)

    def test_explicit_early_summary_supports_one_accomplishment(self):
        self.data['accomplishments'] = self.data['accomplishments'][:1]
        _, _, text, reader = self.render()
        self.assertEqual(len(reader.accomplishments), 1)
        self.assertNotIn('2. ', text)

    def test_personal_output_has_no_demo_marker_or_supporting_quotes(self):
        self.data['is_demo'] = False
        self.data['accomplishments'][0]['source_excerpt'] = 'PRIVATE SUPPORTING QUOTE FOR CHECKING ONLY'
        _, html, text, _ = self.render()
        self.assertNotIn('Fictional demo', html)
        self.assertNotIn('FICTIONAL DEMO', text)
        self.assertNotIn('PRIVATE SUPPORTING QUOTE', html + text)

    def test_markup_unicode_and_template_tokens_remain_literal(self):
        literal = '<img src=x onerror="alert(1)"> résumé 🪴 @@TITLE@@ </script>'
        self.data['accomplishments'][0]['text'] = literal
        self.data['encouragement'] = ['You used <care> & patience.']
        _, html, text, reader = self.render()
        self.assertEqual(reader.accomplishments['accomplishment-a1'], literal)
        self.assertIn(literal, text)
        self.assertNotIn('<img src=x', html)
        self.assertEqual(base64.b64decode(''.join(reader.scripts)).decode('utf-8'), text)

    def test_empty_or_duplicate_accomplishments_rejected_before_writing(self):
        for entries in ([], [self.data['accomplishments'][0]] * 2):
            bad = copy.deepcopy(self.data)
            bad['accomplishments'] = entries
            with self.assertRaises(renderer.SummaryError):
                renderer.render(bad, self.parent)
        self.assertFalse(self.parent.exists())

    def test_invalid_types_and_missing_provenance_rejected(self):
        mutations = [
            lambda data: data.update(is_demo='false'),
            lambda data: data.update(encouragement=[]),
            lambda data: data['accomplishments'][0].pop('source_excerpt'),
            lambda data: data['accomplishments'][0].update(text='   '),
            lambda data: data.update(title='x' * 161),
            lambda data: data.update(title='bad\x00text'),
            lambda data: data.update(title='bad\ud800text'),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.data)
                mutation(data)
                with self.assertRaises(renderer.SummaryError):
                    renderer.render(data, self.parent)
        self.assertFalse(self.parent.exists())

    def test_oversized_and_malformed_input_rejected(self):
        for raw in (b'x' * (renderer.MAX_BYTES + 1), b'{bad', b'\xff'):
            with self.assertRaises(renderer.SummaryError):
                renderer.load_input(io.BytesIO(raw))

    def test_revision_preserves_unrelated_content_and_previous_files(self):
        first, first_html, first_text, first_reader = self.render()
        self.data['accomplishments'][0]['text'] = 'Helped a teammate understand the monthly reporting process.'
        self.data['accomplishments'][0]['source_excerpt'] = 'It was monthly, not weekly.'
        second, _, second_text, second_reader = self.render()
        self.assertNotEqual(first['html_path'], second['html_path'])
        self.assertEqual(Path(first['html_path']).read_text(), first_html)
        self.assertEqual(Path(first['text_path']).read_text(), first_text)
        self.assertIn('monthly reporting', second_text)
        for identifier in ('accomplishment-a2', 'accomplishment-a3'):
            self.assertEqual(first_reader.accomplishments[identifier], second_reader.accomplishments[identifier])

    def test_failed_second_write_leaves_no_partial_revision(self):
        previous, _, previous_text, _ = self.render()
        before = set(self.parent.iterdir())
        original = Path.write_text
        def fail_text(path, *args, **kwargs):
            if path.name == 'summary.txt':
                raise OSError('simulated write failure')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'write_text', fail_text), self.assertRaises(OSError):
            renderer.render(self.data, self.parent)
        self.assertEqual(set(self.parent.iterdir()), before)
        self.assertEqual(Path(previous['text_path']).read_text(), previous_text)


if __name__ == '__main__':
    unittest.main()
