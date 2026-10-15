import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
from scripts import package_claude as package


class ClaudePackageTests(unittest.TestCase):
    def test_archive_is_reproducible_and_contains_only_skill_resources(self):
        files = package.package_files()
        first = package.archive_bytes(files)
        self.assertEqual(first, package.archive_bytes(files))
        expected = {'SKILL.md', 'LICENSE', 'scripts/render_summary.py',
                    'assets/summary.html', 'references/summary-format.md',
                    'references/claude-runtime.md'}
        with zipfile.ZipFile(io.BytesIO(first)) as archive:
            self.assertEqual(set(archive.namelist()), {package.NAME + '/' + p for p in expected})
            for name in package.SHARED:
                self.assertEqual(archive.read(package.NAME + '/' + name),
                                 (ROOT / '.agents/skills' / package.NAME / name).read_bytes())
        self.assertLessEqual(len(package.DESCRIPTION), 200)

    def test_extracted_package_renders_without_repository_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp).resolve()
            with zipfile.ZipFile(io.BytesIO(package.archive_bytes(package.package_files()))) as archive:
                archive.extractall(folder / 'installed')
            helper = folder / 'installed' / package.NAME / 'scripts/render_summary.py'
            payload = (ROOT / 'examples/demo-summary.json').read_bytes()
            def run(script, output):
                result = subprocess.run([sys.executable, str(script), '--input', '-',
                                         '--output-dir', str(output)], input=payload,
                                        capture_output=True, cwd=folder, check=True)
                return {key: Path(value).read_bytes() for key, value in json.loads(result.stdout).items()}
            actual = run(helper, folder / 'Claude outputs with spaces')
            expected = run(ROOT / '.agents/skills' / package.NAME / 'scripts/render_summary.py', folder / 'codex')
            self.assertEqual(actual, expected)

    def test_sync_check_detects_missing_and_modified_resources(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp).resolve() / 'skill'
            files = package.package_files()
            package.write_skill(destination, files)
            self.assertEqual(package.check_skill(destination, files), [])
            (destination / 'scripts/render_summary.py').write_text('changed')
            (destination / 'assets/summary.html').unlink()
            self.assertEqual(set(package.check_skill(destination, files)),
                             {'scripts/render_summary.py', 'assets/summary.html'})

    def test_builder_refuses_symlink_target_without_modifying_other_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp).resolve()
            original = folder / 'original'
            original.write_text('keep')
            destination = folder / 'skill'
            destination.mkdir()
            (destination / 'LICENSE').symlink_to(original)
            with self.assertRaises(ValueError):
                package.write_skill(destination, package.package_files())
            self.assertEqual(original.read_text(), 'keep')
            self.assertFalse((destination / 'SKILL.md').exists())


if __name__ == '__main__':
    unittest.main()
