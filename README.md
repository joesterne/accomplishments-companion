# Accomplishments Companion

A Codex skill that helps a discouraged job seeker recognize real accomplishments and keep a supportive summary for motivation or future résumé work.

**Proof of concept:** nine renderer tests and skill validation pass. Fictional Codex trials verified the three-accomplishment offer and an explicit early summary; both browser downloads and initial keyboard/layout checks passed. The learner accepted the first-use trial; specific/ambiguous corrections, pause behavior, and corrected downloads also passed. The learner accepted both hands-on trials and the final review. The [remaining accessibility checks](docs/accessibility.md) are documented. This is not a claim of Section 508 conformance.

## Try it in Codex

Open this repository as a Codex project and ask to use **Accomplishments Companion** (or mention `$accomplishments-companion`). The skill lives in `.agents/skills/accomplishments-companion/`. If a newly added skill is not discovered, start a fresh task or restart the host.

Talk about things you have done or feel proud of. The companion uses relevant questions about work and everyday life when examples are hard to find. It offers a summary after three distinct accomplishments, or honors an earlier explicit request. Corrections stay in the conversation.

The helper uses Python 3.9+ and only its standard library; no extra API key or runtime packages are required. Conversation access and usage limits come from your existing Codex setup.

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

The tests cover output consistency, a one-accomplishment summary, source-excerpt exclusion, Unicode and literal markup, invalid input, revisions, and failed-write recovery. They do not establish conversational behavior or browser accessibility. See [verification notes](docs/verification.md) for the actual boundaries.

## How the pieces fit

- `SKILL.md`: the reusable conversation workflow.
- `references/summary-format.md`: the structured input contract.
- `scripts/render_summary.py`: validation and consistent HTML/text generation.
- `assets/summary.html`: the offline visual template and download controls.

These files are self-contained. Discovery paths, UI metadata, permissions, and file presentation vary between agents. Claude and Gemini compatibility has not been tested.

## Privacy and boundaries

The helper makes no network calls and does not save a raw transcript. It renders the content passed to it into local files. Codex's conversation retention still follows its own settings; this is not a promise of local-only AI processing. Generated revisions remain until you delete them.

`outputs/`, local credentials, and the personal learner profile are excluded from commits. Supporting excerpts used to check accomplishment fidelity do not appear in generated documents. The companion does not invent achievements, provide guided mindfulness exercises, or guarantee employment or emotional improvement.

## Project progress

The approved scope, requirements, and technical plan are in `devpost/`. The [build checklist](devpost/checklist.md) records unfinished work and the learn-mode checkpoints. The hackathon's final demo video and submission are not complete.

## Corrections and recovery

In the same conversation, identify the accomplishment and corrected detail, such as "Change three days to two days; keep the other accomplishments the same." The companion should clarify an ambiguous edit and give you links to a new revision. Previously downloaded copies remain unchanged.

If generation fails, use the previous successful files while retrying. If browser downloads are unavailable, use the exact local HTML/text paths the helper returned. Open the HTML in an ordinary browser and use Save As. The Codex in-app browser used for testing blocks local-file URLs; the recorded browser tests used a loopback server restricted to fictional demo files.
