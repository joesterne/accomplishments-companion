# Gemini runtime and file delivery

Use the shared conversation rules and JSON contract. Resolve resources relative to the loaded skill directory. Python 3.9+ and its standard library are sufficient; the renderer makes no network calls and needs no API key. Treat account access and model usage as part of the person's Gemini host, not this helper.

## Gemini CLI

This adapter is named `accomplishments-companion-gemini` and installed at `.gemini/skills/accomplishments-companion-gemini/`. The distinct name avoids collision with the shared skill in `.agents/skills/`, which Gemini CLI prefers when names match. A user installation can instead be under `~/.gemini/skills/`; resolve from the actual loaded location.

Respect Gemini's activation and tool approval flow. Once active, keep the supportive conversation in the main session. Do not switch to a coding task, delegate the person's conversation, or generate files before they request or accept a summary.

Run the bundled `scripts/render_summary.py` using the summary contract. In this repository, choose the ignored `outputs/` directory. Elsewhere choose an ignored or unversioned location before saving personal content. Use stdin or a temporary JSON file in that private output location; remove only temporary input you created, never a user-provided original. Return the exact absolute HTML/text paths from the successful helper result. Use links supported by the terminal or editor and explain how to open the HTML in a browser when necessary. Do not assume a Codex viewer, Claude attachment tool, or hosted sandbox URL.

## Gemini Apps with uploaded skills

Discover the installed skill resources and execution/file-delivery capabilities provided by the current Gemini app. Do not assume a local project checkout, a fixed mount path, or that uploaded Python is executable just because it can be read.

When Python execution and downloadable files are available, run the bundled helper with the JSON contract. Use a writable artifact directory provided by the host as output parent, retaining each revision folder. Keep temporary input with supporting excerpts in private scratch space outside the exposed artifact directory and remove only that input afterward. Expose both successful output files through Gemini's actual file-delivery mechanism; do not invent links or claim a file was downloaded to the person's device.

If HTML preview disables download buttons, present the original HTML and text attachments. If execution or attachments are unavailable, explain that limitation briefly and, on request, provide the summary as readable text in chat. Offer the Gemini CLI path for the consistent downloadable document pair. Do not promise a file, simulate renderer success, or replace the verified template with an untested app.

Only provide file links after success. On correction, create new revisions and keep previous successful files. Hosted storage may be temporary; encourage downloading copies they want to keep. The repository's `.gitignore` does not protect files in Gemini's hosted execution environment.

## Privacy and scope

Gemini processing, retention, and activity settings belong to the person's account and organization. Do not change them. The helper's lack of networking does not make an AI conversation local-only or guarantee confidentiality. Never search unrelated files, email, or Drive for accomplishments. Do not publish summaries, upload them elsewhere, or save raw transcripts. Keep guided mindfulness, VR, and the resource library deferred.
