import unittest
from pathlib import Path

from scripts import package_claude, package_copilot, package_gemini


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/accomplishments-companion/SKILL.md'
SUMMARY_CONTRACT = ROOT / '.agents/skills/accomplishments-companion/references/summary-format.md'


class SkillPromptTests(unittest.TestCase):
    def test_always_loaded_skill_stays_within_prompt_budget(self):
        self.assertLessEqual(len(SKILL.read_bytes()), 5_000)

    def test_summary_mechanics_are_deferred_to_linked_reference(self):
        skill = SKILL.read_text(encoding='utf-8')
        contract = SUMMARY_CONTRACT.read_text(encoding='utf-8')
        self.assertIn('(references/summary-format.md)', skill)
        self.assertNotIn('python3 /absolute/path/to/skill/scripts/render_summary.py', skill)
        self.assertNotIn('output location and file-delivery method', skill)
        self.assertIn('python3 /absolute/path/to/skill/scripts/render_summary.py', contract)

    def test_host_delivery_guidance_is_also_deferred(self):
        packages = (
            (package_claude, 'claude'),
            (package_gemini, 'gemini'),
            (package_copilot, 'copilot'),
        )
        for package, runtime in packages:
            with self.subTest(package=package.NAME):
                files = package.package_files()
                skill = files['SKILL.md'].decode('utf-8')
                contract = files['references/summary-format.md'].decode('utf-8')
                self.assertNotIn('runtime and file delivery', skill)
                self.assertIn('runtime and file delivery', contract)
                self.assertIn(f'({runtime}-runtime.md)', contract)


if __name__ == '__main__':
    unittest.main()
