# GitHub Copilot setup and validation

This adapter targets interactive GitHub Copilot in VS Code agent mode and Copilot CLI. It keeps the same real-accomplishments conversation, three-example offer, early-summary option, and conversational corrections. It is not a Microsoft 365 Copilot or Copilot Studio integration.

## Use in VS Code

1. Open this repository in VS Code with GitHub Copilot available under your normal account.
2. Open Copilot Chat and select Agent mode so the helper can run through the host's tool permissions.
3. Ask: **Use accomplishments-companion-copilot to help me recognize my accomplishments.**
4. Follow the conversation, accept the summary offer, and open the resulting HTML or text file.

The skill is at `.github/skills/accomplishments-companion-copilot/SKILL.md`. If the host does not discover it, start a new agent session and check the current host's skill settings. The suffixed name distinguishes it from other adapters Copilot may also discover in `.agents/skills/` and `.claude/skills/`.

The renderer requires Python 3.9+ on the execution machine and no extra packages or API key. Use the normal host approval flow for execution. The skill does not pre-approve shell tools or change permissions. Open HTML in a regular browser if an editor preview does not support its download buttons.

## Use in Copilot CLI

Start an interactive Copilot CLI session in the repository and ask to use **accomplishments-companion-copilot**. The helper returns absolute file paths; open the HTML in a browser or use the text file directly. A remote workspace's files must be transferred through that host's supported download mechanism before they are on your computer.

Copilot cloud coding tasks and automated code review are not verified user-facing conversation surfaces for this companion. Personal accomplishments should not be turned into public issues, commits, or pull requests to deliver results.

## Install elsewhere

Build a distribution archive:

```sh
python3 scripts/package_copilot.py
```

Extract `outputs/packages/accomplishments-companion-copilot.zip`. Copy the extracted `accomplishments-companion-copilot` directory into another repository's `.github/skills/`, without overwriting an existing installation. For a Copilot personal installation, GitHub also documents `~/.copilot/skills/`; check the specific host's supported personal paths before using it.

This ZIP is a directory distribution to extract and install, not a claimed chat-attachment installer. It includes the complete skill, host runtime instructions, contract, helper, template, and MIT license. Generated summaries and private learning files are excluded.

## Maintaining the adapter

`packaging/copilot-runtime.md` contains the host instructions. `scripts/package_copilot.py` uses `scripts/skill_package.py` to generate the Copilot folder and deterministic ZIP from an explicit file allowlist. The shared conversation source is under `.agents/skills/accomplishments-companion/`; the renderer, template, and JSON contract remain identical across hosts. Edit sources and rebuild rather than changing the generated copy directly.

```sh
python3 scripts/package_copilot.py --check
python3 -m unittest discover -s tests -v
```

To render fictional output without running a model:

```sh
python3 .github/skills/accomplishments-companion-copilot/scripts/render_summary.py --input examples/demo-summary.json --output-dir outputs/copilot-demo
```

## Verification — October 15, 2026

- All 19 tests pass: nine renderer tests plus ten packaging tests across Claude, Gemini, and Copilot.
- Skill-format validation and all three adapter consistency checks pass.
- The Copilot ZIP contains exactly six intended files under one named root folder and rebuilds reproducibly.
- Its extracted helper runs from an unrelated directory without the source repository and produces HTML/text bytes identical to the original helper. Invalid input leaves prior successful output intact.
- Neither `copilot` nor `code` was available on the development shell's command path. This does not establish whether a desktop application is installed elsewhere.
- **Pending:** actual VS Code/Copilot CLI discovery, activation, conversation, corrections, and file opening. No model trial or account changes were performed.

For a live trial, use fictional examples. Check that two examples do not trigger the automatic offer, three trigger an offer that waits for acceptance, an explicit one-example summary works, ambiguous corrections prompt clarification, and a specific correction preserves unrelated entries and previous files. Verify the actual generated HTML/text paths can be opened.

## Official references

Checked October 15, 2026:

- [GitHub: adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — supported skill folders, metadata, script resources, and directory installation.
- [VS Code: agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) — agent skill discovery and usage in VS Code.
