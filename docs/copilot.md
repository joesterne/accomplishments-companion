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

## Verification — October 15–16, 2026

All 19 local tests pass: nine renderer tests plus ten packaging tests across Claude, Gemini, and Copilot. All three adapter consistency checks pass. The Copilot ZIP contains six intended files, rebuilds reproducibly, and its extracted helper works without the source repository. These checks are separate from the live host trial below.

### Live VS Code trial

Tested in VS Code 1.139.0, Copilot Chat Agent mode, with Auto routing to GPT-6 Luna. The workspace contained a copy of the packaged `.github/skills/accomplishments-companion-copilot/` directory and an ignored `outputs/` folder. All conversation examples and files were explicitly fictional. Existing account configuration and default tool permissions were used; renderer execution and browser opening used scoped approvals.

| Check | Observed result |
| --- | --- |
| Discovery and activation | Copilot visibly loaded the named skill from `.github/skills/` and read its runtime and summary references. |
| No examples | Acknowledged discouragement and asked one focused question about an ordinary responsibility. No invented accomplishment or output. |
| Two examples | Recognized the checklist update and one library volunteer shift, then asked for another example. No automatic summary offer. |
| Three examples | Adding a walking routine triggered an offer. No summary was generated until the offer was accepted. |
| Creation | Acceptance produced a labeled HTML/text pair using the bundled renderer. |
| Ambiguous correction | “One accomplishment is wrong” prompted a clarifying question rather than a guessed edit. |
| Specific correction | Changed the walking routine from three to two days a week. IDs remained `a1`, `a2`, and `a3`; the other accomplishments were preserved. The text diff contained only the requested frequency change; encouragement and next steps were unchanged. |
| Revision preservation | SHA-256 checks confirmed both original files remained unchanged after correction. |
| Explicit early summary | A fresh chat requested a summary of one grocery-carrying example. Copilot created exactly one accomplishment without asking for two more or importing examples from the earlier trial. |
| Local file delivery | The generated and corrected HTML opened in VS Code's integrated browser. Both download controls opened native save dialogs and saved files. The downloaded text was byte-identical to its generated source; the HTML retained the content and embedded text, with normal DOM serialization differences. |
| Temporary inputs | Temporary JSON inputs created for the main and correction trials were removed. The early-summary trial used standard input. |

The live preview exposed a host-specific sentence in the shared template: “your Codex conversation.” It now says “this conversation” in the canonical template and all three generated adapters. The corrected live output verified this wording.

Local evidence is intentionally ignored rather than published: `outputs/copilot-live-workspace/outputs/revision-d68ead97d593/` (initial), `revision-5314f3a3f800/` (correction), and `revision-c69182416c8e/` (early summary). The two test downloads are named `copilot-fictional-check-5314f3a3f800.html` and `.txt` in the local Downloads folder.

### Remaining boundaries

Copilot CLI is still untested: `copilot` was not available on the shell path. VS Code was installed even though `code` was not on that path. VS Code results do not establish CLI, remote-workspace, cloud-agent, Microsoft 365 Copilot, or Copilot Studio behavior. Direct chat-link clicking was not verified; file delivery was verified through the integrated preview and its download controls. This was a fictional functional trial, not a new Section 508 conformance assessment or proof of emotional benefit.

## Official references

Checked October 15, 2026:

- [GitHub: adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — supported skill folders, metadata, script resources, and directory installation.
- [VS Code: agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) — agent skill discovery and usage in VS Code.
