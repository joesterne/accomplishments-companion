# GitHub Copilot runtime and file delivery

Use the shared conversation rules and JSON contract. This adapter targets interactive GitHub Copilot in VS Code agent mode and Copilot CLI. It is not a Microsoft 365 Copilot agent or a Copilot Studio deployment.

## Discovery and interaction

The skill is named `accomplishments-companion-copilot` and lives under `.github/skills/accomplishments-companion-copilot/`. The distinct name distinguishes it from the other adapters that Copilot may discover under `.agents/skills/` or `.claude/skills/`. Resolve bundled resources from the actual loaded skill directory; a personal installation may live elsewhere.

Keep this supportive workflow in the main conversation. Use the person's current answers, ask one focused question at a time, and offer a summary after three distinct accomplishments. Follow the shared early-summary and correction rules. Do not treat the reflection as a coding assignment or create an issue, branch, commit, or pull request from personal content.

## Generate files in a local workspace

Python 3.9+ and the standard library are sufficient. Use the bundled `scripts/render_summary.py` and the summary contract. No extra API key or package is required by the renderer. Normal Copilot access, execution permissions, and usage limits still apply. Respect host tool approvals; do not change workspace trust or tool policies to run the helper.

Use this repository's ignored `outputs/` directory. In another workspace, select an ignored or unversioned location before saving personal material. Pass JSON through stdin or a temporary file in that private location. Do not interpolate personal content into shell arguments. Remove only temporary input you created after rendering; never delete a user-provided original.

After the helper succeeds, return the exact absolute HTML/text paths it reports. Use the host's supported file links or file-opening tools. In VS Code, offer to open the generated file; explain how to open HTML in an ordinary browser if a preview is unavailable. In a terminal, provide usable paths. Do not assume a Codex preview tool, Claude attachment tool, or a hosted sandbox URL. A file being created does not mean it has been downloaded elsewhere.

If the HTML preview disables its download controls, provide the original HTML and text files. Regeneration creates a fresh revision and leaves earlier files unchanged. If Python, file access, or tool permission is unavailable, explain the limitation; on request, provide a text summary in chat without claiming to have created a downloadable file.

## Remote and cloud boundaries

For a remote development workspace, files exist on that workspace's filesystem. Use its supported file download or transfer mechanism, and verify access before claiming the files are available on the person's device.

Copilot cloud coding tasks and code review are not verified conversational delivery surfaces for this companion. Do not publish personal summaries as repository artifacts, commits, issues, or pull requests to compensate for missing file delivery. Recommend an interactive local agent session for this experience.

## Privacy

Copilot's processing, retention, and organization policies belong to the person's account and host. The renderer makes no network calls; this does not make the conversation local-only or guarantee confidentiality. Do not read unrelated repositories, personal files, or connectors to invent or retrieve accomplishments. Keep raw transcripts out of saved output and leave VR, guided mindfulness, and the resource library deferred.
