---
doc: spec
status: approved
---

# Accomplishments Companion — Technical Spec

## How This Works, In Plain Language

The person uses a skill inside Codex. The skill is a small set of reusable instructions: it guides the supportive conversation, helps uncover accomplishments, and offers a summary after three examples. Codex supplies the conversational intelligence.

When the person wants the summary, Codex passes the agreed content to a small document-making helper. That helper creates a clean browser document and a plain-text copy from the same content. It handles layout consistently rather than asking the AI to redesign the page every time. Corrections happen in Codex; running the helper again produces the revised documents.

The conversation uses the person's existing Codex access. This project adds no separate AI service, account system, or database. The downloaded files are the take-away; Codex's own conversation retention still follows the host's settings.

## The Core Journey Through the System

Implements `prd.md > The Core Journey`.

1. The person invokes the Accomplishments Companion skill in a Codex task opened in this project.
2. Codex reads the skill and asks supportive, relevant questions. It tracks distinct accomplishments and their supporting user statements in the current conversation.
3. At three accomplishments, Codex offers a summary. An explicit earlier request is allowed; zero examples lead to clarification, not fabricated content.
4. Once the person accepts, Codex structures the accomplishments, encouragement, and suggested next steps into a small data object. Each accomplishment retains a supporting excerpt from the person's statements for checking accuracy; that excerpt is not separately displayed or stored by the helper.
5. A Python helper checks the structure and creates HTML and text outputs. User text is escaped before insertion into HTML. The helper formats supplied content; it does not invent suggestions or call a model.
6. Codex links the files. The HTML opens in a browser and offers clearly named download controls for the HTML and text versions.
7. A correction updates the relevant entry in the conversation. Codex clarifies ambiguous edits, rebuilds the output, and links the revised version.

## Stack

- **Codex skill:** learner-selected host and workflow. Repository-local `SKILL.md` instructions plus a helper script. [Official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills).
- **Python standard library:** proposed routine implementation detail for the accepted document helper. Local Python 3.9.6 was verified; keep the helper compatible with Python 3.9+ without third-party runtime packages. Use [JSON](https://docs.python.org/3/library/json.html) for structured input and [HTML escaping](https://docs.python.org/3/library/html.html) for safe text rendering.
- **Standalone HTML and CSS:** the learner accepted a browser document plus plain text. Inline styles, system fonts, and a small inline download script; no remote assets, CDN, or web framework. The document body remains readable without JavaScript; direct file links and browser Save As remain fallbacks.
- **Tests:** standard-library `unittest` for the helper, browser inspection for the artifact, and real Codex conversational trials for the skill. Mechanical renderer tests do not establish conversational behavior.

## Where It Runs and How Someone Tries It

First supported environment: local Codex desktop on this Mac, with Python 3 and an ordinary browser. Codex CLI can load the same repository skill, but desktop is the demonstrated experience; do not claim other-host runtime verification without running it.

Planned discovery location: `.agents/skills/accomplishments-companion/SKILL.md`. The user opens this repository in Codex and asks it to use the Accomplishments Companion skill. If discovery has not refreshed, a new task or restart may be required. Verify actual discovery in the build.

Planned renderer smoke-demo command, from the project root:

```sh
python3 .agents/skills/accomplishments-companion/scripts/render_summary.py --input examples/demo-summary.json --output-dir outputs/demo
```

`--output-dir` names the parent of the generated revision directories. Open the exact HTML and text paths printed after the command succeeds (for example, `outputs/demo/revision-<unique-id>/summary.html` and `summary.txt`). These files do not require deployment or a continuously running server. A loopback-only preview server may be used during browser QA if the in-app browser cannot open local files; it must serve only the intended output directory.

Normal skill use passes the data object on standard input (`--input -`) so the helper does not require a saved raw conversation file. The helper accepts a deliberate output directory. Generated results live under ignored `outputs/` by default, separate from public source and fictional demo fixtures.

For the required demo video: invoke the real skill, supply fictional examples from work and everyday life, observe the offer after three, generate the summary, correct one accomplishment, and open/download the revised version. The public repository and demo video are required; deployment is optional and not selected for this version.

## Look and Feel

Implements `prd.md > Look and Feel` and `Screens and Layout`.

Carry forward the approved clean, modern direction. Proposed implementation: a white or warm-neutral background, very dark text, a restrained dark-teal accent, a system sans-serif typeface, spacious single-column layout, and clear numbered accomplishments. Use a readable maximum width, responsive spacing, and no decorative animation. Exact colors are implementation choices subject to contrast checks.

Reading order: title, short introduction, accomplishments, encouragement, possible next steps, future mindfulness notice. Put download controls in a clearly labeled area. Use real headings and lists, visible focus indicators, descriptive control names, document language, and selectable text. Support keyboard operation and enlarged text without clipping.

Section 508 is the target; map applicable criteria to the chosen HTML output using the [Access Board's Web Baseline](https://ictbaseline.access-board.gov/web-baselines/). Verification includes structure and reading order, keyboard access, focus, contrast, and 200% text zoom. Use an assistive-technology check when available. Record pass/fail/not-tested for applicable criteria; these example checks alone are not a full conformance claim. Host-interface accessibility is a separate dependency outside the generated document's controls. The text copy provides reuse and fallback, not a substitute for making HTML accessible.

## Components

### Conversation Skill

Implements `prd.md > Supportive Accomplishment Discovery` and `Summary Offer`.

`SKILL.md` contains the workflow and specific rules that matter: support before advice; targeted work/non-work questions; count distinct accomplishments; offer at three; respect explicit earlier requests; clarify missing detail; never invent achievements, numbers, or other people's stories. Follow the person's answers and respect a wish to skip or stop. Avoid presenting encouragement as a guarantee or diagnosis.

Instructions link to the data contract and helper command when a summary is needed. Discovery metadata is concise and scoped to accomplishments reflection and summary creation; it should not activate for ordinary debugging or all job-related work.

### Document Renderer

Implements `prd.md > Visual Summary and Download` and `States and Boundaries`.

`render_summary.py` validates bounded input, unique accomplishment IDs, nonempty content, and the presence of a supporting user excerpt for each accomplishment. This checks the contract, not whether an AI paraphrase is faithful; conversational verification covers that separately.

Build HTML and plain text from one normalized object. Escape user strings for HTML; never evaluate content as code or interpolate it into executable JavaScript. Use a fixed HTML template with clear substitution points. Put download text into the document as safely escaped text, and have fixed JavaScript read it as text rather than interpreting it as markup.

Create both files in a temporary directory, then move the completed directory into a new revision location. Print file paths only after both outputs succeed. Do not overwrite a prior successful revision; the latest returned links identify the current one. This prevents a partial write from presenting mismatched HTML and text as current. Older downloads remain unchanged, as ordinary documents do.

### Browser Summary Template

Implements `prd.md > Screens and Layout`, `Look and Feel`, and `Visual Summary and Download`.

An offline HTML template provides consistent structure, styles, and download controls. The HTML download saves the standalone document; the text download uses the same normalized content as `summary.txt`. Test downloads in the demonstrated browser instead of assuming support. If a browser prevents scripted download, retain direct file links and explain how to save the already-created files.

### Conversational Revision

Implements `prd.md > Corrections Through Conversation`.

Use stable accomplishment IDs within the structured object. An edit updates only the matching entry and its supporting user excerpt. Other entries retain their IDs and content. A correction does not increase the count. Regenerate from the updated object; do not patch raw HTML by guessing text matches. No extra editing interface is added.

### Evidence and Demo Materials

Implements `prd.md > Features and Behavior` acceptance criteria.

Keep fictional fixtures and test scenarios in source control. Record helper test results and browser/accessibility observations separately from real conversation trials. Document what was actually exercised. Personal trials and generated user summaries stay outside commits.

## Data Model

The helper input is a JSON object, assembled from the conversation:

```json
{
  "title": "Your accomplishments",
  "accomplishments": [
    {
      "id": "a1",
      "text": "Helped a new teammate learn the team's process.",
      "source_excerpt": "I showed our new teammate how our process works."
    }
  ],
  "encouragement": ["That example reflects your willingness to support someone else."],
  "next_steps": ["Consider noting what you explained and how it helped."],
  "is_demo": true
}
```

No names, employer details, or sensitive personal identifiers are required. The renderer permits one or more accomplishments; the three-item automatic-offer rule lives in the skill. Suggested validation bounds: maximum input 256 KB, at most 50 accomplishments, and bounded text fields. These are implementation safeguards, not prompts asking people for that much content.

The conversation is the working source for revisions, retained according to Codex's settings. The helper processes JSON in memory and writes only the requested HTML/text artifacts; it does not add a separate user database or raw transcript archive. Revisions are kept in the selected output directory until the user deletes them. If conversation context is unavailable, ask for the relevant content rather than claiming to remember it. A previous summary can be supplied explicitly by the user.

## File Structure

```text
project/
├── .agents/skills/accomplishments-companion/
│   ├── SKILL.md                    # Conversation, triggering, and rendering workflow
│   ├── agents/openai.yaml          # Codex display metadata
│   ├── references/summary-format.md # Input contract and rendering instructions
│   ├── scripts/render_summary.py  # Validation and HTML/text generation
│   └── assets/summary.html         # Offline accessible document template
├── examples/demo-summary.json     # Clearly fictional helper fixture
├── tests/test_render_summary.py   # Renderer behavior and failure tests
├── tests/conversation-scenarios.md # Real-skill trials and expected observable behavior
├── docs/verification.md           # Actual checks and known limitations
├── outputs/                      # Ignored generated personal/demo revisions
├── devpost/                      # Existing curriculum documents and learner profile
├── .gitignore                    # Preserve existing rules; ignore generated outputs
└── README.md                     # How to try, demo, dependencies, and portability notes
```

Existing curriculum skills remain untouched. The skill folder is self-contained so it can later be copied or packaged without reaching into unrelated course files.

## External Services and Dependencies

Codex provides the conversation through the user's existing configured account and model. The helper makes no direct API calls and requires no new API key. Normal Codex usage limits still apply; no claim of free or unlimited use is made. Python and the browser perform document generation/viewing locally; the conversation itself is not represented as local-only processing.

No database, hosted backend, analytics, connector, or remote font is required. Repository sharing and the demo video are handled in the shipping step. A plugin package and other-agent adapters are not needed to prove this repository skill.

## Verification Approach

1. Validate the skill's metadata and references, then confirm actual discovery/invocation in Codex.
2. Run renderer tests for one and three accomplishments, preserved Unicode and literal markup, unchanged unrelated entries after a revision, consistent HTML/text content, invalid input rejection, and preservation of a previous successful result after failure.
3. Exercise real conversations: no initial examples; two-to-three threshold; early-summary request; and specific/ambiguous corrections. Check source fidelity and absence of fabricated outcomes. Inspect actual responses, not merely instruction wording.
4. Open the generated artifact, use both download controls, compare saved contents, and check responsive layout, keyboard focus, headings/reading order, contrast, and zoom. Record assistive-technology results or the specific untested boundary.
5. Have the learner try the core experience and request revisions before calling the build complete.

## Important Failure Modes

- **No examples or unclear correction:** ask a targeted question; no invented content or guessed edit.
- **Invalid structured input:** helper reports a concise validation error and writes no completed revision. Codex repairs the structure from known conversation content or asks for missing information.
- **Filesystem or browser failure:** preserve the last completed artifact, explain what failed, and retry or provide verified local-file links. Never claim a new download exists without evidence.
- **Codex unavailable or rate-limited:** no new conversational output can be promised; already-created HTML/text remains usable offline.

## What Was Simplified and Why

- Use the existing Codex conversation and account; build only the skill and document helper.
- Use standalone HTML and text; avoid adding a PDF pipeline, hosting requirement, or document editor.
- Keep corrections in conversation and generate new document revisions; no additional editing screen or account database.
- Keep stress management and mindfulness as a future-section notice, consistent with the approved boundary.

## Decisions and Open Issues

**Learner decisions:** Codex first; conversation in Codex; browser document plus reusable plain text; clean modern appearance; Section 508 target; approved product behavior and deferred features.

**Implementation choices proposed in this blueprint:** a standard-library Python helper, repository-local skill, single offline template, structured in-memory input, revision directories under ignored outputs, and the validation strategy above. These follow from the accepted architecture and are included in the technical-plan review.

**Learning question:** how skills interact with an agent and transfer between agents. The reusable workflow is in `SKILL.md`; the helper and template are portable files, while discovery paths, UI metadata, permissions, and execution tools depend on the host. During the build, trace one conversation-to-document action through those pieces and identify the Codex-specific parts. This does not establish Claude or Gemini compatibility without trials there.

**Validation risks, not unresolved product choices:** verify actual Codex discovery, browser downloads, faithful conversational behavior, and applicable accessibility requirements. If a required capability cannot be demonstrated, explain the limitation and agree any behavior change before changing the product.

The learner approved this blueprint, including the proposed implementation choices. The build checklist will specify the ordered work and learner checkpoints.

## Sharing Instructions

Public source: https://github.com/joesterne/accomplishments-companion (anonymous access checked October 14, 2026). Use this repository URL in the submission's Try it out field. The planning documents remain under `devpost/`.

Demo video: not yet recorded or linked. The actual form requires a video link; a YouTube channel URL is not a recording. Follow the current [official rules](https://learn-ai-basics.devpost.com/rules) and verify reviewer access after upload. Add the final video URL here once supplied and checked.

License: the actual submission form requires a URL to an open-source license file within the repository. The proposed MIT file is pending owner approval; do not claim the repository is MIT-licensed until it is published.

Shipping progress and remaining learner-owned tasks: `devpost/shipping.md`. No optional deployment is selected.
