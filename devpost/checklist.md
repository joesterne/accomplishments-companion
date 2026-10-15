---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn — explicitly selected by the learner.

## Project Setup

Scope, product requirements, and technical specification are approved. A separate repository is initialized in this project, with origin pointing to the public joesterne/accomplishments-companion repository. The learner also requested GitHub setup; inspect existing access rather than asking for credentials in chat. Do not modify the parent repository.

Preserve existing ignore rules for the learner profile and credential files. Before generating personal outputs or committing, add rules for `/outputs/`, Python bytecode, and `.DS_Store`; inspect tracked/staged files and intended diffs. Commit only the project's intended source, fictional examples, tests, public documentation, and planning documents. Never commit the learner profile or actual user summaries.

## Slices

- [x] **1. Talk through accomplishments and keep a first summary**
  Becomes usable: A discoverable Codex skill guides a supportive conversation, helps find work or non-work accomplishments, offers a summary after three distinct examples, honors an explicit earlier request, and produces readable HTML and text files with download controls.
  Why now: Proves the distinctive conversation-to-summary experience immediately, including the real Codex invocation and document output that the rest of the build depends on.
  PRD ref: `prd.md > The Core Journey`, `Supportive Accomplishment Discovery`, `Summary Offer`, `Visual Summary and Download`, `Look and Feel`
  Spec ref: `spec.md > Conversation Skill`, `Document Renderer`, `Browser Summary Template`, `Data Model`, `Where It Runs and How Someone Tries It`, `File Structure`
  Build: Include project setup in this working step. Create the self-contained repository skill, input contract, standard-library Python helper, offline HTML template, fictional demo fixture, meaningful renderer tests, and trial instructions. Use complete revision directories from the start so HTML/text always come from the same content. Apply the approved visual direction and basic accessibility structure. Keep raw conversation storage out of the helper and generated documents out of commits.
  Verify (mechanical): Run the skill validator and `python3 -m unittest discover -s tests -v`. Render the fictional fixture and open the exact returned files. Inspect real Codex trials for no initial examples, two-to-three threshold, and explicit early-summary requests; record observed responses and fidelity separately from renderer tests. Use both download controls and verify content against the generated files. Check initial layout, keyboard access, readable structure, and contrast. Record results in `docs/verification.md`; do not mark unperformed host or assistive-technology checks as passes.
  Learner check: Start a fresh Codex task in this project, invoke the Accomplishments Companion skill, and try the conversation using fictional or non-sensitive examples. Accept a summary, open both outputs, and report whether the questions, encouragement, and visual result fit the intended experience.
  Commit: `Add Codex accomplishments conversation and downloadable summaries`

- [x] **2. Correct the summary and verify the complete experience**
  Becomes usable: The person corrects an accomplishment through the same conversation and gets an accurate revised summary; ambiguous edits, failed generation, and download problems have understandable recovery paths. The final experience has documented accessibility and behavioral checks.
  Why now: Builds on a working conversation and renderer, incorporates early learner feedback, and proves that the take-away remains trustworthy after changes or failures.
  PRD ref: `prd.md > Corrections Through Conversation`, `States and Boundaries`, `Visual Summary and Download`, `Look and Feel`
  Spec ref: `spec.md > Conversational Revision`, `Important Failure Modes`, `Verification Approach`, `Evidence and Demo Materials`, `Look and Feel`, `Decisions and Open Issues`
  Build: Complete and exercise the revision workflow using stable IDs and source excerpts, clarify ambiguous requests, preserve unaffected entries and prior successful revisions, and supply verified local-file fallbacks for browser failures. Add relevant failure and revision tests, finish applicable output-accessibility checks, and document startup, usage, privacy boundaries, actual validation, and portable versus Codex-specific pieces in README and verification notes. Keep the mindfulness section a future notice only.
  Verify (mechanical): Run the full renderer suite and skill validation after changes. Test faithful revisions, unchanged unrelated entries, invalid or oversized input, literal markup and Unicode, and a failed write without damaging a prior successful result. Inspect real Codex conversations for both specific and ambiguous corrections. Reopen a corrected summary and compare both downloaded outputs. Check keyboard focus/order, heading/read order, contrast, zoom to 200%, and a narrow viewport; perform assistive-technology checks when available and record untested criteria explicitly. Verify the README's real invocation/rendering path with fictional content.
  Learner check: Correct one accomplishment in the same Codex conversation, inspect the revised summary and text copy, and try an unclear correction or early finish. Explore freely and describe anything broken, confusing, or worth changing. This is the final hands-on review for the small proof of concept.
  Commit: `Complete conversational revisions and verify accessible summary outputs`

## Hands-on Checkpoints

- [x] Early usable behavior explored — after slice 1, before its commit in learn mode; before slice 2 in fast mode
- [x] Final kick-the-tires exploration and feedback completed — after slice 2's mechanical verification

Learn mode pauses after each verified step for an explanation and learner trial before committing. Fast mode uses less explanation while retaining the planned early and final hands-on checks. With two slices, the main difference is depth of walkthrough, not removal of learner ownership.

## Final Review

- [x] Final review complete — feedback resolved and learner confirms ready to ship

Record actual feedback and any agreed refinements here as they arise. A report that no changes are needed is a valid outcome. Fixes require verification, commit, and a learner retry of affected behavior before final completion.

## Code Tour and App Map

- [x] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [x] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [x] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: Source-based recap connected the actual correction trial to the learner's skill/agent portability goal. The map was shown in the browser; source paths and symbols were checked. No learner-led editor navigation, optional edit, or mastery is claimed.
Route and stops: `SKILL.md > Correct through conversation`; `render_summary.py > validate(), html_document(), render()`; `assets/summary.html > .intro, download-html, download-text`. These are a reference route, not completed learner navigation.
Edit outcome: Optional safe introductory-text edit offered in the map; not performed or required.
Reflection: Optional transfer question offered with the wrap-up; no answer required and no learner response invented.
Activity mode: Brief source recap and browser-shown standalone map. Native editor inspection was unavailable; this was not an interactive editor exercise.
Map checks: All relative source links resolve in the repository, named symbols exist, content has no script/network dependency, browser structure and layout inspected, and a details control collapsed/expanded with Enter. Snapshot implementation commit: `dcc1b08`.

## Revisions

- The learner explicitly requested an initial GitHub push before the usage reset, ahead of the learn-mode trial. Publish the verified renderer and skill checkpoint now, keep both slice boxes unchecked, and resume the remaining slice 1 checks and learner trial afterward. This does not mark the first slice or build complete.
- Initial checkpoint: nine renderer tests pass; the opening no-accomplishments conversation trial passed through explicit skill loading. Browser downloads, full conversational trials, accessibility verification, and the learner check remain pending. The bundled validator needs PyYAML, which is absent from both checked Python runtimes.

- October 14 resume: initial checkpoint `08a94b9` is pushed to GitHub. Nine renderer tests and the bundled skill validator pass. Fictional agent trials passed the two-to-three offer, acceptance, early summary, and fresh-agent catalog discovery. Browser HTML/text downloads, content comparison, keyboard order/skip navigation, narrow layout, and sampled contrast checks passed. Details and remaining boundaries are in `docs/verification.md`. Slice 1 remains unchecked pending the learner trial; slice 2 has not begun.
- The October 13, 9:41 p.m. Eastern follow-up was not scheduled before interruption. Work resumed manually October 14; no new future schedule was created.

- October 14 learner feedback: "ok tested it and it works as expected". Early hands-on checkpoint accepted with no requested changes. Slice 1 is complete; proceed to slice 2 verification and its final learner trial.

- Slice 2 verification: specific/ambiguous corrections and pause behavior passed. Corrected HTML/text downloads match and preserve unrelated content and prior revisions. Renderer tests and validator pass. Scoped accessibility review is in `docs/accessibility.md`; native browser zoom and screen-reader checks are explicitly unverified, with doubled-text QA recorded separately. No code repair was needed. Await the final learner correction trial before the slice-2 commit and completion box.
- Optional Discord projects-forum sharing suggestion given after the slice-1 checkpoint.

- Final learner response on October 14: "It works" following the correction and final-review prompt. Final hands-on checkpoint and review accepted with no requested changes. Slice 2 complete with documented accessibility verification limits retained.

- Learning wrap-up delivered as an evidence-based source recap with `devpost/app-map.html`; optional practice and reflection do not block shipping. All build-workflow checkpoints are now recorded.
