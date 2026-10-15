# Summary contract

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
