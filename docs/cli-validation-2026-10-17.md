# Live CLI validation — October 17, 2026

Real, authenticated model sessions exercised the packaged skill in Claude Code, Gemini CLI, and GitHub Copilot CLI. All three completed the conversation, generation, correction, and explicit early-summary workflow. The initial trials found unsupported inferences in Claude and Gemini. **The shared instructions were subsequently strengthened, and focused fresh-session retests no longer reproduced those findings.** The original observations and follow-up limits are recorded below.

## Environment and method

| Host | Version used | Observed model |
| --- | --- | --- |
| Claude Code | 2.1.276 | `claude-sonnet-5` |
| Gemini CLI | 0.63.0 | Auto selected `gemini-3.8-flash` |
| GitHub Copilot CLI | 1.0.98 | Auto selected `gpt-6-luna` |

Each host ran in a separate temporary workspace containing only its packaged skill and an `outputs/` ignore rule. The tested packages match the repository copies byte-for-byte at source checkpoint `f2400d9`. No personal accomplishments were used. Existing account authentication was used without copying credentials into prompts or test files. Copilot CLI was installed under a temporary directory, not globally.

The main scenario began with a discouraged fictional job seeker who could not name an accomplishment. Two examples followed: updating a team handover checklist with the steps actually used, and sorting donated books during one library volunteer shift. The third example was a ten-minute walk three days a week for the last month. After generation, an ambiguous correction was followed by a specific change from three walking days to two. A fresh session then requested a summary of just one example: helping a neighbor carry groceries upstairs yesterday.

Initial read-only/noninteractive harness permissions prevented Claude and Copilot from generating files. Both explained that limitation instead of claiming success. Generation was retried interactively after workspace trust and required local operations were permitted. Claude's existing Auto mode was active; Gemini and Copilot showed per-operation approvals. No bypass-permissions or YOLO option was used. Gemini's existing local hooks remained active. These are local CLI trials, not tests of a blank account configuration. Claude also announced a background update; the already-running process remained the version listed above.

## Observed workflow results

| Check | Claude Code | Gemini CLI | Copilot CLI |
| --- | --- | --- | --- |
| Named skill discovered and loaded | Passed | Passed | Passed |
| No examples: supportive opening and one focused question | Passed | Passed | Passed |
| Two examples: no automatic summary offer | Passed | Passed | Passed |
| Third example: offer and wait for acceptance | Passed | Passed | Passed |
| Acceptance: bundled renderer creates HTML and text | Passed after permission retry | Passed | Passed after permission retry |
| Ambiguous correction: clarify instead of guessing | Passed | Passed | Passed through the host's question UI |
| Specific correction: walking frequency changes to two days | Passed | Passed | Passed |
| Stable IDs and unchanged unrelated accomplishments | Passed | Passed | Passed |
| Original HTML/text remain unchanged after correction | Passed, SHA-256 comparison | Passed, SHA-256 comparison | Passed, SHA-256 comparison |
| Fresh session: explicit one-example summary | Passed | Passed | Passed |
| Temporary input cleanup | No input files remained | No input files remained | Used standard input |

All nine revisions contain both files, a visible fictional-demo notice, and the expected number of accomplishments. The HTML's embedded downloadable text is byte-identical to its adjacent `summary.txt`; listed accomplishments match between formats. Supporting `source_excerpt` fields are absent from the output documents. The early summaries contain only the grocery example, without importing the main scenario's examples.

The Claude correction changes the walking entry and the encouragement sentence that also mentioned its frequency. Gemini and Copilot change only the requested accomplishment in the text output. All three preserve IDs `a1`, `a2`, and `a3`, the first two entries, and the earlier files.

## Initial grounding findings

These are observed wording deviations from the shared instruction to avoid invented outcomes or personal characteristics. They do not indicate a renderer defect.

1. **Claude added an unconfirmed benefit.** The checklist accomplishment became “making it more accurate for whoever relies on it next.” Earlier conversation also said the person “caught gaps that could trip up a teammate.” The supplied example established an update, but did not confirm gaps or downstream effects. Encouragement further asserted that the update made things easier for other people. The summary should keep the supplied action or ask about its effect before adding that claim.
2. **Claude and Gemini inferred enduring qualities from limited evidence.** In the one-example trial, Claude called grocery-carrying “everyday reliability” and suggested documenting being “dependable”; Gemini said it showed “kindness, reliability, and community care.” Gemini's main summary also described “steady discipline.” Encouragement should recognize the action without presenting broader personal traits as established facts. Copilot's early summary stayed with the practical help described.

The initial testing pass made no skill or renderer changes. The authorized follow-up below changes the shared instructions and verifies the affected cases. One successful trial per scenario is not a statistical reliability evaluation.

## Follow-up: grounding fix and focused retests

The canonical `SKILL.md` now applies the evidence requirement explicitly to conversational replies, accomplishment text, encouragement, and suggested résumé/interview wording. It distinguishes a described action from an unconfirmed benefit or enduring trait, includes short checklist/grocery/walking examples, and requires a factual review before rendering. Claude, Gemini, and Copilot installations and distribution archives were regenerated from that source. The renderer, template, schema, and product scope are unchanged.

Fresh sessions received the fictional examples without the earlier conclusions or expected answers. The checklist case supplied all three original examples together and explicitly requested a summary; it did not repeat the full multi-turn offer/correction workflow. The grocery case requested an early summary of the same single example. Each host used its regenerated package.

| Retest | Observed result | Revision |
| --- | --- | --- |
| Claude Sonnet 5: checklist, volunteering, walking | Kept the described actions; no claimed checklist benefit or discipline trait. Encouragement recognized the actual examples. | `743219b23710` |
| Claude Sonnet 5: groceries | Listed the one action and encouraged recognition of the practical help; no reliability/dependability claim in the summary or next steps. | `c4a97c4ae1e8` |
| Gemini 3.8 Flash: checklist, volunteering, walking | Kept the described actions; no claimed accuracy improvement or discipline trait. | `31af4654734e` |
| Gemini 3.8 Flash: groceries | Listed only the grocery-carrying example and acknowledged the practical task; no inferred personal trait. | `79404b971035` |

Claude Code had automatically updated to 2.1.302 and changed its default to Opus 5.5. An initial extra Opus run also produced a grounded three-example summary (`040a634d4dbf`), but the two primary Claude retests explicitly selected the original `claude-sonnet-5` model. Gemini remained CLI 0.63.0 with `gemini-3.8-flash`. This controls the primary model identity, but the changed Claude CLI version and combined checklist prompt mean these are focused regression checks, not a controlled causal study.

Gemini's first checklist invocation constructed a Python subprocess with byte input and `text=True`, causing an argument-type error before rendering. Gemini corrected its invocation and then produced both files. The bundled renderer required no fix. This demonstrates recovery in that run, not flawless execution on every attempt.

The four primary retest pairs and the additional Opus pair were checked for matching embedded text, visible demo notices, expected accomplishment counts, and omission of supporting excerpts. Selected conversation text and artifacts are stored locally under ignored `outputs/grounding-retest/`. All 19 existing tests, all three package consistency checks, and the canonical skill validator passed after regeneration.

The two original grounding findings are addressed and did not recur in these focused retests. Broader wording reliability remains an ongoing review responsibility. The updated Copilot package passed regeneration and consistency checks; a new live Copilot conversation was not needed for these Claude/Gemini findings and was not run. No browser or hosted-upload claims are added by this follow-up.

## Evidence and limits

Ignored local evidence is saved in `outputs/cli-validation-2026-10-17/`: selected conversation text, copied HTML/text artifacts, correction diffs, and `checks.json` with file hashes and structural checks. Raw host account metadata and hidden model reasoning are not included in the selected conversation exports. None of these local evidence files are intended for a public commit.

| Host | Initial revision | Corrected revision | Early-summary revision |
| --- | --- | --- | --- |
| Claude | `8d2fe670f29a` | `a97be8f34b03` | `9012a969e0ce` |
| Gemini | `2a3b566cc055` | `d4dbfd593c85` | `9094d269ac10` |
| Copilot | `68470a0235eb` | `1c01ef4fae0a` | `73d5d09ed25e` |

Each CLI returned the exact local file paths. This pass verified files on disk and parsed content; it did not click terminal links or repeat browser download, screen-reader, or zoom testing. Existing browser evidence is documented separately in [verification](verification.md) and [Copilot's VS Code trial](copilot.md).

Claude chat uploads/downloads, Gemini Apps uploads/downloads, remote workspace delivery, other models, and other operating systems remain unverified. These findings do not establish Section 508 conformance or emotional benefit.
