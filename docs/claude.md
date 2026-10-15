# Claude installation and validation

The Claude version preserves the same product behavior: one focused question at a time, real accomplishments only, an offer after three distinct examples, earlier summaries on request, and corrections through conversation. It produces the same HTML and plain-text files. VR, guided mindfulness, and the resource library remain deferred.

## Claude Code

1. Open this repository as a Claude Code project. Authenticate through Claude's own sign-in flow if needed; do not share credentials in chat.
2. Start a fresh session and enter `/accomplishments-companion`.
3. Talk about your accomplishments, or request a fictional demonstration.
4. Accept the summary offer, then open the returned HTML or text file. Ask for a correction in the same conversation.

The project skill is already installed at `.claude/skills/accomplishments-companion/`. It needs Python 3.9+ on the execution machine. It adds no API key requirement beyond your normal Claude access and does not change permissions, models, hooks, or account settings.

For use outside this repository, copy that entire skill folder into your project's `.claude/skills/` or your personal `~/.claude/skills/` directory. Check for an existing installation before copying. The folder is self-contained and has no symlinks. Choose an ignored or unversioned output location for personal summaries in another project.

## Claude chat

Build the upload archive from the repository root:

```sh
python3 scripts/package_claude.py
```

Upload `outputs/packages/accomplishments-companion-claude.zip` under **Customize → Skills**, then enable it and start a conversation asking to use Accomplishments Companion. Code execution and file creation must be enabled and permitted by the account or organization. Upload through the skill settings, not merely as an ordinary chat attachment.

The ZIP has one root folder, `accomplishments-companion/`, containing the skill instructions, JSON contract, Claude runtime instructions, Python helper, HTML template, and MIT license. It contains no personal profile, generated summaries, raw transcripts, course skills, or Codex UI metadata.

Hosted Claude must present both generated files through its own file-delivery mechanism. The skill does not assume a fixed filesystem mount or a Codex-specific preview tool. If the HTML preview restricts download buttons, use the original HTML and text attachments. Download files you want to retain; this package does not promise permanent hosted storage. Without code execution, the conversation and a text response can continue, but file generation is unavailable.

## Maintaining the two versions

The existing `.agents/skills/accomplishments-companion/` remains the shared source for the conversation and renderer. `packaging/claude-runtime.md` holds the Claude-specific file-delivery guidance. `scripts/package_claude.py` uses the shared `scripts/skill_package.py` utility to combine an explicit allowlist of these files into the Claude Code folder and upload ZIP. It shortens the Claude discovery description, routes to runtime instructions, and adjusts two local-file assumptions. The renderer, template, and JSON contract remain byte-for-byte identical.

Edit the shared source or runtime adapter, then rebuild. Do not edit the generated Claude copy directly. Check for stale generated files with:

```sh
python3 scripts/package_claude.py --check
python3 -m unittest discover -s tests -v
```

This is what portability means here: common instructions and executable files, plus different discovery and file-delivery integration. Matching file formats alone does not prove matching model behavior.

## Verification — October 15, 2026

- All nine existing renderer tests and four packaging tests pass (13 total).
- The upload ZIP is reproducible, contains only the six intended files, and includes its license.
- An extracted ZIP executes its helper from an unrelated directory, without the source repository, including output paths containing spaces. Its HTML/text bytes match the Codex helper's output.
- The consistency check detects missing or modified resources; packaging refuses symlink targets without altering their contents.
- Claude Code 2.1.276 is installed on the development machine. `claude auth status` reports `loggedIn: false`. No model request was made and no authentication settings were changed.
- **Pending:** live Claude skill discovery, conversational behavior, and Claude-hosted downloads. Local rendering tests do not establish these.

After signing in, use fictional examples to check: a blank start prompts a useful question; two examples do not automatically trigger a summary; three trigger an offer that waits for acceptance; an explicit one-example summary works; an ambiguous correction prompts clarification; a specific correction preserves unrelated entries and creates new files. In Claude chat, also verify both attachments can actually be downloaded. Record results before claiming end-to-end Claude support.

## Authoritative setup references

Checked October 15, 2026:

- [Claude Code skills documentation](https://code.claude.com/docs/en/skills) — project/personal skill discovery and slash-command invocation.
- [Create custom Claude skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) — metadata, resources, and ZIP structure.
- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) — enabling skills and code execution.
