# Accomplishments Companion

A skill for Codex, Claude, Gemini, and GitHub Copilot that helps a discouraged job seeker recognize real accomplishments and keep a supportive summary for motivation or future résumé work.

**Proof of concept:** nine renderer tests and skill validation pass. Fictional Codex trials verified the three-accomplishment offer and an explicit early summary; both browser downloads and initial keyboard/layout checks passed. The learner accepted the first-use trial; specific/ambiguous corrections, pause behavior, and corrected downloads also passed. The learner accepted both hands-on trials and the final review. The [remaining accessibility checks](docs/accessibility.md) are documented. This is not a claim of Section 508 conformance.

## Try it in Codex

Open this repository as a Codex project and ask to use **Accomplishments Companion** (or mention `$accomplishments-companion`). The skill lives in `.agents/skills/accomplishments-companion/`. If a newly added skill is not discovered, start a fresh task or restart the host.

Talk about things you have done or feel proud of. The companion uses relevant questions about work and everyday life when examples are hard to find. It offers a summary after three distinct accomplishments, or honors an earlier explicit request. Corrections stay in the conversation.

A concrete action is enough to count; you do not need a metric or a job title. Once an example is clear, the companion moves to another experience, normally asking at most one follow-up unless clarification is needed or you want to explore further. If Codex appears stuck without replying, check its turn/approval status: host request delays can happen before the skill responds. See the [pacing and delayed-response investigation](docs/verification.md#october-19-2026-delayed-codex-turn-and-conversation-pacing).

The helper uses Python 3.9+ and only its standard library; no extra API key or runtime packages are required. Conversation access and usage limits come from your existing Codex setup.

## Try it in Claude

**Claude Code:** open this repository in Claude Code and enter `/accomplishments-companion`. The self-contained skill is in `.claude/skills/accomplishments-companion/`; it uses the same renderer and template as Codex.

**Claude chat:** run `python3 scripts/package_claude.py`, then upload `outputs/packages/accomplishments-companion-claude.zip` under **Customize → Skills** and enable it. Code execution and file creation must be available. Ask Claude to use Accomplishments Companion.

See [Claude setup and validation](docs/claude.md) for installation details and file-delivery differences. A live Claude Code trial completed the conversation, file-generation, correction, and early-summary workflow, with initial grounding findings addressed in [focused fresh-session retests](docs/cli-validation-2026-10-17.md). Claude chat uploads and hosted downloads remain unverified.

## Try it in Gemini

**Gemini CLI:** open this repository, check `/skills list`, and ask to use **accomplishments-companion-gemini**. The distinct name avoids a collision with the original skill in `.agents/skills/`.

**Gemini Apps:** run `python3 scripts/package_gemini.py` and upload `outputs/packages/accomplishments-companion-gemini.zip` under **Customize → Skills → Upload**, if Skills is available for your account. The package includes the same Python renderer, with host-specific file-delivery guidance and a text fallback when execution is unavailable.

See [Gemini setup and validation](docs/gemini.md). A signed-in Gemini CLI trial completed discovery, conversation, generation, corrections, and an early summary, with initial grounding findings addressed in [focused fresh-session retests](docs/cli-validation-2026-10-17.md). Gemini Apps uploads and hosted downloads remain unverified.

## Try it in GitHub Copilot

Open this repository in **VS Code with Copilot Agent mode** or an interactive **Copilot CLI** session. Ask to use **accomplishments-companion-copilot**. The self-contained adapter lives in `.github/skills/accomplishments-companion-copilot/`.

For another workspace, run `python3 scripts/package_copilot.py`, extract `outputs/packages/accomplishments-companion-copilot.zip`, and copy the skill folder into that workspace's `.github/skills/`. See [Copilot setup and validation](docs/copilot.md).

## Compatibility and verification

“Passed” means a check was actually performed. Local renderer tests do not establish a host's conversation or download behavior.

| Host | Local package/renderer | Skill discovery in host | Conversation and corrections | Host file delivery |
| --- | --- | --- | --- | --- |
| Codex | Passed | Passed | Passed in fictional and learner trials | HTML/text and browser downloads passed |
| Claude Code | Passed | Passed in isolated workspace | Workflow passed; focused grounding retests passed | HTML/text files and exact paths verified; terminal-link clicking not tested |
| Claude chat | Passed | Upload/activation pending | Pending | Hosted attachments pending |
| Gemini CLI | Passed | Passed in isolated workspace | Workflow passed; focused grounding retests passed | HTML/text files and exact paths verified; terminal-link clicking not tested |
| Gemini Apps | Passed | Upload/activation pending | Pending | Hosted attachments pending |
| Copilot in VS Code | Passed | Passed in isolated workspace | Passed in fictional trial, including early summary | Integrated preview and HTML/text downloads passed |
| Copilot CLI | Passed | Passed in isolated workspace | Passed in fictional trial, including early summary | HTML/text files and exact paths verified; terminal-link clicking not tested |

See the host guides, [live CLI results and grounding follow-up](docs/cli-validation-2026-10-17.md), and [verification notes](docs/verification.md) for evidence and limits. Copilot support here targets interactive sessions; Microsoft 365 Copilot and Copilot Studio are not included.

## Render the fictional demo

From the repository root:

```sh
python3 .agents/skills/accomplishments-companion/scripts/render_summary.py --input examples/demo-summary.json --output-dir outputs/demo
```

Open the exact `html_path` and `text_path` printed after success. Each run creates a complete new revision under the chosen output parent. The HTML is a standalone browser document with HTML and plain-text download controls; both files are also directly available on disk. No hosting is required.

The fixture is fictional and visibly marked as a demonstration. Never replace it with personal conversation data in a public commit.

## Test

```sh
python3 -m unittest discover -s tests -v
```

The 19 tests cover Claude/Gemini/Copilot packaging and isolated rendering as well as output consistency, a one-accomplishment summary, source-excerpt exclusion, Unicode and literal markup, invalid input, revisions, and failed-write recovery. They do not establish conversational behavior or browser accessibility. See [verification notes](docs/verification.md) for the actual boundaries.

## How the pieces fit

- `SKILL.md`: the reusable conversation workflow.
- `references/summary-format.md`: the structured input contract.
- `scripts/render_summary.py`: validation and consistent HTML/text generation.
- `assets/summary.html`: the offline visual template and download controls.

These files are self-contained. Discovery paths, UI metadata, permissions, and file presentation vary between agents. The Claude, Gemini, and Copilot packages reuse the conversation workflow, JSON contract, renderer, and template, with small host-specific adapters. All three packages are tested locally and have completed live CLI workflow trials. Initial Claude and Gemini wording issues prompted stronger shared instructions; focused retests no longer reproduced those unsupported inferences. Copilot in VS Code also passed a fictional conversation, correction, early-summary, and browser-download trial. Hosted Claude chat and Gemini Apps delivery remain unverified.

## Privacy and boundaries

The helper makes no network calls and does not save a raw transcript. It renders the content passed to it into local files. Each host's conversation retention still follows its own settings; this is not a promise of local-only AI processing. Generated revisions remain until you delete them.

`outputs/`, local credentials, and the personal learner profile are excluded from commits. Supporting excerpts used to check accomplishment fidelity do not appear in generated documents. The companion is instructed to avoid invented achievements, guided mindfulness exercises, and guarantees of employment or emotional improvement. Review generated wording for accuracy; focused retests passed after addressing unsupported inferences observed in the initial Claude and Gemini trials.

## Project progress

The approved scope, requirements, and technical plan are in `devpost/`. The [build checklist](devpost/checklist.md) records both completed build steps and learner reviews. The [app map](devpost/app-map.html) explains the code, its portability boundaries, and where to make changes. The hackathon's final demo video and submission are not complete.

## Corrections and recovery

In the same conversation, identify the accomplishment and corrected detail, such as "Change three days to two days; keep the other accomplishments the same." The companion should clarify an ambiguous edit and give you links to a new revision. Previously downloaded copies remain unchanged.

If generation fails, use the previous successful files while retrying. If browser downloads are unavailable, use the exact local HTML/text paths the helper returned. Open the HTML in an ordinary browser and use Save As. The Codex in-app browser used for testing blocks local-file URLs; the recorded browser tests used a loopback server restricted to fictional demo files.

## License

[MIT License](LICENSE). Copyright (c) 2026 Joe Sterne.
