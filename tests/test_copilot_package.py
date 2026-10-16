import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts import package_copilot as package
from scripts import skill_package as common

ROOT = Path(__file__).resolve().parents[1]


class CopilotPackageTests(unittest.TestCase):
    def test_distribution_contains_only_self_contained_skill_and_license(self):
        files = package.package_files()
        data = package.archive_bytes(files)
        self.assertEqual(data, package.archive_bytes(files))
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            expected = {'SKILL.md', 'LICENSE', 'references/copilot-runtime.md',
                        'references/summary-format.md', 'scripts/render_summary.py', 'assets/summary.html'}
            self.assertEqual(set(archive.namelist()), {package.NAME + '/' + n for n in expected})
            for name in common.SHARED:
                self.assertEqual(archive.read(package.NAME + '/' + name),
                                 (ROOT / '.agents/skills/accomplishments-companion' / name).read_bytes())
            self.assertIn(('name: ' + package.NAME + '\n').encode(),
                          archive.read(package.NAME + '/SKILL.md'))

    def test_extracted_helper_renders_from_another_directory_and_rejects_bad_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            with zipfile.ZipFile(io.BytesIO(package.archive_bytes(package.package_files()))) as archive:
                archive.extractall(root / 'installed')
            helper = root / 'installed' / package.NAME / 'scripts/render_summary.py'
            output = root / 'Copilot output'
            command = [sys.executable, str(helper), '--input', '-', '--output-dir', str(output)]
            result = subprocess.run(command, input=(ROOT / 'examples/demo-summary.json').read_bytes(),
                                    cwd=root, capture_output=True, check=True)
            paths = json.loads(result.stdout)
            contents = {key: Path(value).read_bytes() for key, value in paths.items()}
            canonical = subprocess.run([sys.executable,
                str(ROOT / '.agents/skills/accomplishments-companion/scripts/render_summary.py'),
                '--input', '-', '--output-dir', str(root / 'canonical')],
                input=(ROOT / 'examples/demo-summary.json').read_bytes(),
                cwd=root, capture_output=True, check=True)
            self.assertEqual(contents, {key: Path(value).read_bytes()
                                      for key, value in json.loads(canonical.stdout).items()})
            before = set(output.iterdir())
            invalid = subprocess.run(command, input=b'{invalid', cwd=root, capture_output=True)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertEqual(before, set(output.iterdir()))
            self.assertEqual(contents, {key: Path(value).read_bytes() for key, value in paths.items()})

    def test_installed_package_matches_sources_and_missing_template_is_detected(self):
        files = package.package_files()
        self.assertEqual(common.check_skill(ROOT / '.github/skills' / package.NAME, files), [])
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp).resolve() / 'skill'
            common.write_skill(destination, files)
            (destination / 'assets/summary.html').unlink()
            self.assertEqual(common.check_skill(destination, files), ['assets/summary.html'])


if __name__ == '__main__':
    unittest.main()
