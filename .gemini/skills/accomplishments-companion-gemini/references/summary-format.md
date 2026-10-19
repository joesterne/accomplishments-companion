# Summary contract

Before creating files, read [Gemini runtime and file delivery](gemini-runtime.md). Its host-specific output and privacy guidance takes precedence over local project defaults in the shared summary contract.

Read this contract only after the person accepts a summary offer, explicitly requests a summary, or asks to correct an existing one. Do not invoke the renderer while collecting accomplishments.

## Ground the content

Build both formats from the same structured content:

- The person's actual accomplishments, preserving meaning and modest scale.
- Brief reassurance grounded in those examples.
- A few optional, practical next steps related to the conversation, labeled as possibilities rather than completed actions.

Before rendering, compare every factual claim in the accomplishments, encouragement, and next steps with what the person said. Remove unsupported benefits, traits, and implications; the renderer cannot check fidelity. Preserve warmth by acknowledging the described action and the person's worth.

The template supplies a small future notice for stress management and mindfulness. Do not add guided exercises or a resource library.

## Render the summary

The helper is `scripts/render_summary.py`, relative to this skill folder. It requires Python 3.9+ and only standard-library modules. Run it with a deliberately selected output parent directory, normally the project's ignored `outputs/` folder:

```sh
python3 /absolute/path/to/skill/scripts/render_summary.py --input - --output-dir /absolute/path/to/project/outputs
```

Send one JSON object through standard input. Do not interpolate user content into shell commands. If the available file tool makes an input file necessary, keep it under the ignored outputs folder and remove only that temporary input after rendering; never delete a user-supplied original.

```json
{
  "title": "Your accomplishments",
  "accomplishments": [
    {
      "id": "a1",
      "text": "Helped a new teammate learn a process.",
      "source_excerpt": "I showed our new teammate how our process works."
    }
  ],
  "encouragement": ["You made time to help someone learn."],
  "next_steps": ["Consider writing down what you explained and how it helped."],
  "is_demo": false
}
```

Required fields: `title`, `accomplishments`, `encouragement`, `next_steps`, and boolean `is_demo`. There must be 1–50 accomplishments with unique IDs and nonempty text/source excerpts. Encouragement and next steps each contain 1–10 nonempty strings. Text fields are limited to 4,000 characters; title is limited to 160. Input is capped at 256 KiB. Limits protect rendering; do not ask people to fill them.

The helper cannot prove source fidelity. Compare each paraphrase with the person's actual words before rendering. Supporting excerpts are checked for presence but are not included in generated files. Mark only fictional demonstration data `is_demo: true`; this visibly labels both files.

Successful output is one JSON object containing absolute `html_path` and `text_path` values. Each run creates a fresh `revision-...` directory below `--output-dir`. Use the returned paths rather than predicting a filename or linking an earlier revision. Invalid input or failed writes produce a nonzero exit and no new complete revision; prior revisions remain intact.

The HTML contains fixed download controls, embedded styles, and an embedded text copy. User strings are text, never executable markup. The HTML remains readable offline with scripts disabled; the adjacent plain-text file is also available. If browser download controls fail, link the verified local files and explain browser Save As instead of claiming a download happened.

Pass structured content through standard input or a temporary local input file only when needed. Do not put personal content in public fixtures, commits, or shell arguments. Do not create a separate profile, database, or persistent raw transcript. The output directory does not make the host conversation private or local-only.

Choose the output location and file-delivery method using the Gemini runtime reference; the renderer does not make the host conversation private or local-only.

After a successful run, deliver the exact HTML and text files returned using the host-specific method in the Gemini runtime reference. Show the HTML when a file-viewing tool is available; otherwise explain how to open it in a browser. Readable content requires no server. Only report new files after the helper succeeds. Tell the person they can request corrections in the conversation.

## Correct through conversation

Accept natural-language corrections. If the target or change is unclear, ask one clarifying question. Update only the affected entry and its `source_excerpt`; retain unrelated IDs and content. Refresh encouragement or suggestions only when the correction makes them inaccurate. Render a fresh revision and return its new links. Earlier downloaded files do not update automatically.

If rendering fails, keep the conversation and prior successful summary, explain the failure briefly, and retry after addressing it. If correction context is unavailable, ask for the relevant content rather than pretending to remember it. Never read unrelated personal files to fill a gap.
