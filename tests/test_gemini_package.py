import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts import package_gemini as package
from scripts import skill_package as common

ROOT = Path(__file__).resolve().parents[1]


class GeminiPackageTests(unittest.TestCase):
    def test_upload_archive_has_root_skill_and_only_supported_resources(self):
        files = package.package_files()
        archive_data = package.archive_bytes(files)
        self.assertEqual(archive_data, package.archive_bytes(files))
        with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
            self.assertEqual(set(archive.namelist()), {
                'SKILL.md', 'LICENSE.txt', 'references/gemini-runtime.md',
                'references/summary-format.md', 'scripts/render_summary.py', 'assets/summary.html'})
            for name in common.SHARED:
                self.assertEqual(archive.read(name),
                                 (ROOT / '.agents/skills/accomplishments-companion' / name).read_bytes())
            # The upload instructions use the same distinct name as the CLI folder.
            self.assertIn(('name: ' + package.NAME + '\n').encode(), archive.read('SKILL.md'))
            self.assertNotEqual(package.NAME, 'accomplishments-companion')

    def test_extracted_package_handles_correction_without_source_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            installed = root / 'installed skill'
            with zipfile.ZipFile(io.BytesIO(package.archive_bytes(package.package_files()))) as archive:
                archive.extractall(installed)
            data = json.loads((ROOT / 'examples/demo-summary.json').read_text())
            helper = installed / 'scripts/render_summary.py'
            def render(script, payload, output):
                result = subprocess.run([sys.executable, str(script), '--input', '-',
                                         '--output-dir', str(output)], input=json.dumps(payload).encode(),
                                        capture_output=True, cwd=root, check=True)
                return json.loads(result.stdout)
            before = render(helper, data, root / 'Gemini output')
            before_bytes = {key: Path(value).read_bytes() for key, value in before.items()}
            expected = render(ROOT / '.agents/skills/accomplishments-companion/scripts/render_summary.py',
                              data, root / 'Codex output')
            self.assertEqual(before_bytes, {key: Path(value).read_bytes() for key, value in expected.items()})
            data['accomplishments'][0]['text'] = 'Helped a teammate understand a monthly report.'
            data['accomplishments'][0]['source_excerpt'] = 'It was monthly.'
            after = render(helper, data, root / 'Gemini output')
            self.assertNotEqual(before, after)
            for key, value in before.items():
                self.assertEqual(Path(value).read_bytes(), before_bytes[key])
            text = Path(after['text_path']).read_text()
            self.assertIn(data['accomplishments'][0]['text'], text)
            for entry in data['accomplishments'][1:]:
                self.assertIn(entry['text'], text)

    def test_generated_install_matches_sources_and_detects_drift(self):
        files = package.package_files()
        destination = ROOT / '.gemini/skills' / package.NAME
        self.assertEqual(common.check_skill(destination, files), [])
        with tempfile.TemporaryDirectory() as temp:
            installed = Path(temp).resolve() / 'skill'
            common.write_skill(installed, files)
            (installed / 'references/gemini-runtime.md').write_text('stale')
            self.assertEqual(common.check_skill(installed, files), ['references/gemini-runtime.md'])


if __name__ == '__main__':
    unittest.main()
