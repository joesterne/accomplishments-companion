# Claude runtime and file delivery

Use the same conversation rules and JSON contract on both hosts. Resolve bundled paths from the installed skill's directory, not the shell's current directory. The helper requires Python 3.9+ and no extra packages, network requests, or API keys.

## Claude Code

This repository installs the skill at `.claude/skills/accomplishments-companion/`. A personal installation may instead be under `~/.claude/skills/`. Use the actual loaded location.

Choose the project's ignored `outputs/` folder for generated files. If running outside this repository, confirm that the chosen output location is outside version control or ignored before writing personal material. Pass structured input through stdin or a temporary file in that output folder. Remove only temporary input you created after rendering; never delete user-provided originals.

Run `scripts/render_summary.py` from the installed skill using the summary contract. Return links to the exact absolute HTML and text paths reported by the helper. If previewing HTML is unavailable, tell the person how to open the HTML file in their browser. Do not require Codex tools or start a web server automatically.

## Claude chat with code execution and file creation

Use Claude's available execution environment and file-delivery instructions. Discover the installed skill directory; do not assume the repository exists or write into the skill installation.

Choose a writable output location that Claude can expose as downloadable files, using the artifact directory specified by the current host. Create an `accomplishments-companion` subdirectory there for the revision folders. Do not assume a fixed mount path across Claude products. These are files in Claude's execution environment, not files already saved to the person's computer, and they are not covered by this repository's `.gitignore`.

Run the bundled Python helper with the same JSON contract. Use the host's attachment/presentation mechanism to expose both successful output files. Follow its actual file-link convention instead of inventing a URL or copying a convention from another agent. Do not claim a raw internal path is a working download. Keep any temporary JSON input in a private scratch directory, outside the exposed artifact folder, and remove only that temporary input after rendering.

If an HTML preview blocks its embedded download controls, provide the two original files as attachments. The person can download HTML, open it locally, or use the text file directly. Preserve revision directories when correcting content. Remind the person to download files they want to keep; do not promise permanent hosted storage.

If code execution or file creation is unavailable, explain that limitation. Continue the conversation and, if requested, provide the summary as text in chat; do not claim that an HTML or text file was generated. Suggest enabling code execution/file creation or using the Claude Code installation for file output.

## Privacy

Claude's conversation processing and retention follow the person's Claude account and organization settings. The renderer itself makes no network calls; that does not make the conversation local-only or guarantee confidentiality. Do not read unrelated files, retain a raw transcript, or upload generated personal summaries elsewhere.
