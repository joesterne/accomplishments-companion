# Gemini installation and validation

The Gemini adapter keeps the same conversation and document behavior as the Codex version: real accomplishments only, one focused question at a time, an offer after three distinct examples, an earlier summary when requested, and corrections that preserve unrelated entries. The helper uses Python 3.9+ and standard-library modules with no network calls.

## Gemini CLI

Open this repository in Gemini CLI using your normal authentication and workspace trust flow. Run `/skills list` (or `gemini skills list` from a terminal) and look for **accomplishments-companion-gemini**. Ask:

> Use accomplishments-companion-gemini to help me recognize my accomplishments.

Approve the host's skill activation prompt if shown. This is a skill name, not a custom `/accomplishments-companion-gemini` slash command. Existing sessions can refresh discovery with `/skills reload`.

The self-contained installation lives in `.gemini/skills/accomplishments-companion-gemini/`. Its distinct name matters: Gemini CLI also discovers `.agents/skills/` and gives that alias priority when names match. This repository therefore exposes both the original shared skill and the explicit Gemini adapter. Choose the suffixed name to exercise the Gemini-specific instructions.

To install in another workspace, copy that entire folder into its `.gemini/skills/` directory without overwriting an existing installation. No global installation, API key, hook, model override, or permission change is supplied by this project. Normal Gemini account requirements and usage limits apply.

The helper writes HTML and text into a chosen ignored or unversioned folder. Open the exact returned HTML path in your browser. For a local fictional render without a model:

```sh
python3 .gemini/skills/accomplishments-companion-gemini/scripts/render_summary.py --input examples/demo-summary.json --output-dir outputs/gemini-demo
```

## Gemini Apps

Build the upload archive:

```sh
python3 scripts/package_gemini.py
```

Upload `outputs/packages/accomplishments-companion-gemini.zip` from **Customize → Skills → Upload**, review it, and create the skill. The ZIP puts `SKILL.md` directly at its root and includes the Python helper, HTML template, Markdown references, and `LICENSE.txt`. It contains no generated personal summaries, credentials, hidden runtime files, or course skills.

Google documents a gradual rollout, so Skills may not yet be available for an account. Follow the current account requirements shown by Google; this package does not change activity or privacy settings. Once available, ask Gemini to use the skill by name or select it from the app's skill picker.

The included helper needs Python execution and a way to expose generated files. Uploading supported source files alone does not verify those capabilities. The adapter uses the actual host's artifact directory and attachment mechanism; it does not assume Codex or Claude paths. If execution or attachment delivery is unavailable, it explains that limitation and can provide a text summary on request. Gemini CLI is the alternative for generating the consistent HTML/text pair. HTML previews may restrict JavaScript; use the original attachments if in-preview download buttons do not work.

## Shared implementation

The common conversation source remains `.agents/skills/accomplishments-companion/`. Both host adapters use `scripts/skill_package.py` for allowlisted copying, metadata adaptation, deterministic archives, and consistency checks. `scripts/package_claude.py` preserves the existing Claude commands and ZIP layout; `scripts/package_gemini.py` selects Gemini's name and archive layout. Host-specific guidance lives in `packaging/claude-runtime.md` and `packaging/gemini-runtime.md`.

The renderer, template, and JSON contract remain byte-for-byte identical across all three installations. Edit common sources and runtime guidance, then regenerate; do not edit generated skill copies directly.

```sh
python3 scripts/package_claude.py
python3 scripts/package_gemini.py
python3 scripts/package_claude.py --check
python3 scripts/package_gemini.py --check
python3 -m unittest discover -s tests -v
```

## Verification — October 15, 2026

Historical packaging baseline. The October 17 live CLI results below supersede the live activation and conversation gaps in this section.

- All 16 tests pass: nine renderer tests, four Claude packaging tests, and three Gemini packaging tests.
- Gemini skill format validation and both package consistency checks pass.
- An extracted Gemini ZIP renders from an unrelated directory, without the source repository, producing bytes identical to the original renderer. A correction creates new files and leaves the previous revision and unrelated accomplishment text intact.
- The Gemini ZIP is reproducible and contains exactly the six intended resources. Its root layout and text/code resource types match the documented uploader format. This is a local packaging check, not a successful account upload.
- Gemini CLI 0.63.0 successfully lists both skill names as enabled at their correct paths in an isolated test workspace containing copies of the shared and Gemini skills. The test used a temporary CLI profile with trust restricted to that temporary workspace; the user's account settings and trusted folders were not changed. No model request was made.
- The first discovery attempt under the existing local profile did not return output before it was stopped. A clean profile initially reported the expected untrusted-workspace restriction; the isolated trusted-fixture test above then established discovery. This does not verify the user's normal profile or authentication.
- Live Gemini activation and conversation, the three-example offer, ambiguous correction behavior, and Gemini Apps upload/download delivery remain unverified. Test with fictional data before using a personal summary.

## Live Gemini CLI trial — October 17, 2026

Gemini CLI 0.63.0 used the existing signed-in profile, with Auto selecting `gemini-3.8-flash`. The temporary test folder was trusted and skill activation and local operations used normal approval prompts. The user's existing local hooks remained active. The named Gemini adapter loaded successfully.

The two/three-example offer boundary, accepted generation, ambiguous correction, specific walking-frequency correction, and a fresh one-example summary all worked. The correction changed only the requested accomplishment in the text output. IDs and unrelated entries were preserved, original-file hashes were unchanged, and temporary JSON inputs were removed. All three HTML/text pairs matched, including their embedded downloadable text.

**Grounding follow-up:** the initial encouragement inferred qualities such as reliability from a single action. After strengthening the shared instructions and regenerating all adapters, fresh Gemini 3.8 Flash retests of the three-example and single-grocery scenarios avoided those traits and unconfirmed benefits. One renderer invocation needed an argument-type correction, which Gemini made successfully. See [the full CLI report](cli-validation-2026-10-17.md). Local file paths and contents were verified; terminal-link clicking and Gemini Apps upload/download delivery remain unverified.

## Official references

Checked October 15, 2026:

- [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/) — discovery, `.agents` precedence, activation, and skill management.
- [Creating Agent Skills](https://geminicli.com/docs/cli/creating-skills/) — folder structure, scripts, and resources.
- [Create and manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296?hl=en) — current rollout, upload format, supported files, and restrictions on external actions.
