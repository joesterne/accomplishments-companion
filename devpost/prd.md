---
doc: prd
status: approved
---

# Accomplishments Companion — Product Requirements

Working title retained from the approved scope. A supportive conversation for discouraged job seekers that turns their real accomplishments into a visual, downloadable summary.

Source: `scope.md > The Unique Kernel`, `Who It's For`, and `The Core Loop`.

## The Core Journey

1. The person begins a conversation. The companion acknowledges their discouragement, offers reassurance, and invites them to talk about something they have done or feel proud of.
2. The companion helps unpack their examples. If they draw a blank, it asks targeted questions about work history or experiences outside work: volunteering, family responsibilities, or exercise. Questions follow what the person shares rather than demanding answers in every category.
3. Once the person has described at least three distinct accomplishments, the companion offers to create their summary. The person can accept or keep talking.
4. The visual summary lists their accomplishments, includes reassurance, and suggests possible next steps. Stress management and mindfulness appear only as a clearly labeled future section.
5. The person can correct an accomplishment in the same conversation. The companion applies the correction and produces an updated summary.
6. The person downloads the current summary for day-to-day motivation or as input to résumé work.

Success means their actual examples are recognizable in the summary, a requested correction appears in the revised version, and the downloaded copy matches that version.

## Screens and Layout

Two surfaces within one experience: the conversation and the generated summary. Corrections stay in the conversation; a separate editing screen is not required. Whether the summary is displayed inside the host agent or opened as a companion document depends on the technical plan.

Summary reading order: **Your accomplishments**, **Encouragement to keep**, **Possible next steps**, then a small **Stress management and mindfulness — planned for later** notice. A clearly named download action makes the current summary available to keep. This section order was approved during the product-plan review.

Source: `scope.md > The Core Loop` and `The POC Boundary`.

## Look and Feel

Clean and modern, with accessibility built into the design. Use readable text, clear headings and lists, generous spacing, and restrained decoration. No specific typeface or palette has been chosen; the technical plan will translate this direction into styling.

The learner explicitly selected Section 508 as the accessibility target. The relevant electronic-content baseline references WCAG 2.0 Level A and AA, with applicability depending on the output format. See the [U.S. Access Board's Revised Standards](https://www.access-board.gov/ict/) and [document testing baseline announcement](https://www.access-board.gov/news/2024/09/30/new-ict-testing-baseline-for-documents-released/).

The build must check applicable requirements for the generated summary and download, including reading order and structure, contrast, text resizing, descriptive controls, and keyboard access where interactive. Record actual results and gaps; a visual inspection alone does not establish conformance. The selected host's own interface must be distinguished from the output this project controls.

Source: `scope.md > Inspiration & Identity`, refined by the product interview.

## Features and Behavior

### Supportive Accomplishment Discovery

Offer encouragement without making up qualifications, outcomes, or guarantees about getting hired. Recognize experiences outside paid work as valid material for personal motivation. Use the person's examples as the basis for each accomplishment; ask a clarifying question when a detail is unclear.

- [ ] Someone who starts with no examples receives a targeted, relevant question rather than an invented accomplishment.
- [ ] Work and non-work examples can both appear in the summary.
- [ ] Every accomplishment can be traced to information the person actually supplied. No invented metrics, employers, roles, or achievements.

### Summary Offer

The system prompts once there are three or more distinct accomplishments. A correction to an existing accomplishment does not count as another accomplishment. This is an offer to generate, not automatic generation.

- [ ] At two accomplishments, the automatic offer has not appeared.
- [ ] At three accomplishments, the offer appears and the person can accept or continue.
- [ ] Continuing the conversation preserves the existing examples.

### Visual Summary and Download

Provide the actual list of accomplishments, reassurance grounded in those examples, and possible next steps. Suggestions are possibilities rather than claims about actions already taken. Keep the future mindfulness section clearly marked and non-interactive; no guided exercise is included. Do not invent stories or quotations from other job seekers.

- [ ] The result contains all three working content sections and a clearly labeled future-section notice.
- [ ] The person can read the summary visually and access its text and structure with assistive technology in the supported output format.
- [ ] A downloaded copy opens, remains readable, and contains the same current content as the preview.
- [ ] Applicable accessibility checks are documented with any unverified areas or failures identified.

### Corrections Through Conversation

The person can say which accomplishment is incorrect and supply a change in ordinary language. If the target or intended change is unclear, the companion asks for clarification. It updates that accomplishment without changing unrelated ones and refreshes the available summary.

- [ ] A specific correction appears in the preview and newly downloaded copy.
- [ ] Unrelated accomplishments remain intact.
- [ ] An ambiguous correction leads to clarification rather than a guessed edit.

Source for all four behaviors: `scope.md > The Core Loop`, `What "Working" Looks Like`, and `The POC Boundary`.

## States and Boundaries

- **First use / no accomplishments:** reassurance and targeted questions; no fabricated summary content.
- **Gathering examples:** the person can continue discussing work or non-work experiences.
- **Ready:** at least three accomplishments trigger the offer to make a summary.
- **Reviewing / correcting:** the current summary remains the basis for conversational revisions; download uses the latest completed version.
- **Creation or download failure:** explain the failure plainly, preserve the available conversation and readable summary, and allow a retry. Never claim that an unavailable file was created.
- **Early finish:** three is the automatic-prompt threshold, not a compulsory quota. If the person explicitly requests a summary earlier, offer one using only the examples actually supplied. With none, explain that there is nothing to list yet and let them stop or continue.
- **Session boundary:** the downloaded copy is what the person keeps. The PoC adds no account or cross-session memory of its own. The host agent may retain conversations under its own settings; do not promise local-only or private processing.

The learner approved these defaults during the product-plan review, including shorter summaries on explicit request, retry behavior, and no separate account or cross-session memory.

## Product Decisions

- Summaries contain accomplishments, reassurance, and possible next steps.
- Stress management and mindfulness remain a placeholder rather than active exercises.
- When someone is stuck, explore work history and non-work experiences to surface overlooked accomplishments.
- Use a clean, modern look with Section 508 as the accessibility target.
- Prompt to create a summary after three or more accomplishments.
- Make corrections through the existing conversation.

## What We're Building

The focused conversation-to-summary experience above, with targeted discovery, the three-accomplishment offer, conversational corrections, a readable and accessible visual result, and a downloadable copy. The skill-oriented format remains the desired direction; the host and file format are chosen in the technical plan.

## Deferred From the POC

VR integration, a broader resource library, and guided grounding exercises remain deferred as agreed in `scope.md > Later`. Active stress-management and mindfulness content belongs there too. Existing résumé and job tracker tools are context, not integrations to build.

## Non-Goals

A complete résumé builder, job tracker, or guarantee of employment or emotional improvement. The output is material the person can reuse. Multi-agent portability is a learning topic, not a promise of tested compatibility with every named tool.

## Open Questions

- **For technical planning:** choose the supported host, invocation path, output/download format, and how the applicable accessibility requirements will be checked. Avoid claiming host accessibility or cross-tool compatibility without evidence.
- **Working title:** Accomplishments Companion remains a temporary name; naming does not block the proof of concept.
