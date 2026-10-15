# Output accessibility review

Date: October 14, 2026. Scope: generated English HTML summary, its two download links, and the fictional fixtures tested in Codex's in-app browser. Codex's chat UI, other browsers, and arbitrary future content are outside this review. This is a proof-of-concept evidence record, not a conformance certification.

Reference basis: [Access Board Web Baseline](https://ictbaseline.access-board.gov/web-baselines/) and [WCAG 2.0](https://www.w3.org/TR/WCAG20/). The baseline covers the Revised Section 508 web requirements and references WCAG 2.0 A/AA. The following is a scoped review, not execution of every baseline procedure.

| Area / criterion | Observed result and boundary |
| --- | --- |
| Non-text content (1.1.1) | Decorative arrow has `aria-hidden`; branding is text. No informative images in tested outputs. |
| Media (1.2.1–1.2.5), audio control (1.4.2) | Not applicable: no audio, video, or media player. |
| Structure and sequence (1.3.1, 1.3.2) | Headings, ordered/unordered lists, labeled sections, main region, and reading order exposed in the browser accessibility tree. Screen-reader traversal remains untested. |
| Sensory cues and color (1.3.3, 1.4.1) | Controls have text labels; no instruction or state relies on color, shape, or position alone. |
| Contrast (1.4.3) | Measured primary text pairs range from 5.72:1 to 10.51:1. See verification notes for exact pairs. This is a sampled check, not every interaction state. |
| Text resize (1.4.4) | QA-only copy doubled root text size; body font measured 34px versus 17px. At a 563px content viewport, document scroll/client widths matched and download text fit controls. Native 200% browser zoom remains unverified: keyboard zoom had no effect and native Codex inspection was unavailable to the tool. |
| Images of text (1.4.5) | Not applicable: all content is selectable text. |
| Keyboard and traps (2.1.1, 2.1.2) | Tab/Shift-Tab order observed; skip-link Enter moved focus to main. Both download controls saved matching files when activated with Enter. No custom key handler or trap in source. |
| Timing/motion/flashing (2.2.1, 2.2.2, 2.3.1) | Not applicable: no timers, animation, moving content, or flashing. |
| Bypass and title (2.4.1, 2.4.2) | Skip link works; page title names the summary and product. |
| Focus, links, headings (2.4.3, 2.4.4, 2.4.6, 2.4.7) | Logical focus order, named download links, descriptive headings, and visible 3px focus outline observed. |
| Multiple ways (2.4.5) | Not applicable to this individual standalone document; no site navigation collection. |
| Language (3.1.1, 3.1.2) | `lang="en"` present. Tested content is English; language changes in arbitrary submitted content are not modeled or verified. |
| Predictability (3.2.1–3.2.4) | Focus does not navigate automatically; controls have consistent labels. No input fields or multi-page navigation system. |
| Input assistance (3.3.1–3.3.4) | No form submission in the output. Conversation corrections and helper validation are separately tested; host chat accessibility is outside this review. |
| Parsing and control semantics (4.1.1, 4.1.2) | Generated structure, unique accomplishment IDs, escaped input, and native link names inspected/tested. Formal HTML conformance validation and assistive-technology interoperability remain untested. |

## Remaining manual checks

Use a browser with native zoom controls to test at 200% and traverse headings/lists/links with VoiceOver or another screen reader. Verify the downloaded copies in that environment. These checks are not replaced by an accessibility-tree snapshot or the doubled-text fixture. Full Section 508 claims require a complete applicable evaluation.
