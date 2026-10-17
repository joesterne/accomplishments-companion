"""Render a faithful, offline summary pair without network calls or saved input."""
import argparse
import base64
import html
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

MAX_BYTES = 256 * 1024
MAX_TEXT = 4000
NOTICE = 'Stress management and mindfulness — planned for later. Guided exercises are not part of this version.'


class SummaryError(ValueError):
    pass


def clean_text(value, label, limit=MAX_TEXT):
    if not isinstance(value, str) or not value.strip():
        raise SummaryError(label + ' must be nonempty text.')
    value = value.strip()
    if len(value) > limit:
        raise SummaryError(label + ' is too long.')
    if any(ord(char) < 32 and char not in '\n\t' for char in value):
        raise SummaryError(label + ' contains unsupported control characters.')
    # Reject isolated surrogates before any output directories are created.
    try:
        value.encode('utf-8')
    except UnicodeError as error:
        raise SummaryError(label + ' contains invalid Unicode.') from error
    return value


def validate(raw):
    if not isinstance(raw, dict):
        raise SummaryError('Summary must be a JSON object.')
    required = {'title', 'accomplishments', 'encouragement', 'next_steps', 'is_demo'}
    if set(raw) != required:
        raise SummaryError('Summary fields do not match the documented contract.')
    result = {'title': clean_text(raw['title'], 'Title', 160)}
    if type(raw['is_demo']) is not bool:
        raise SummaryError('is_demo must be true or false.')
    result['is_demo'] = raw['is_demo']
    entries = raw['accomplishments']
    if not isinstance(entries, list) or not 1 <= len(entries) <= 50:
        raise SummaryError('Provide between one and fifty accomplishments.')
    result['accomplishments'] = []
    seen = set()
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict) or set(entry) != {'id', 'text', 'source_excerpt'}:
            raise SummaryError('Each accomplishment needs id, text, and source_excerpt.')
        identifier = clean_text(entry['id'], 'Accomplishment ID', 64)
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', identifier) or identifier in seen:
            raise SummaryError('Accomplishment IDs must be unique letters, numbers, hyphens, or underscores.')
        seen.add(identifier)
        result['accomplishments'].append({
            'id': identifier,
            'text': clean_text(entry['text'], 'Accomplishment ' + str(index)),
            'source_excerpt': clean_text(entry['source_excerpt'], 'Supporting excerpt ' + str(index)),
        })
    for field in ('encouragement', 'next_steps'):
        items = raw[field]
        if not isinstance(items, list) or not 1 <= len(items) <= 10:
            raise SummaryError(field + ' must contain between one and ten items.')
        result[field] = [clean_text(item, field) for item in items]
    return result


def text_document(data):
    lines = [data['title'], '']
    if data['is_demo']:
        lines += ['FICTIONAL DEMO — these examples are not a real person\'s record.', '']
    lines += ['YOUR ACCOMPLISHMENTS', '']
    for index, entry in enumerate(data['accomplishments'], 1):
        lines.append(str(index) + '. ' + entry['text'])
    for key, heading in [('encouragement', 'ENCOURAGEMENT TO KEEP'), ('next_steps', 'POSSIBLE NEXT STEPS')]:
        lines += ['', heading, '']
        lines += ['- ' + item for item in data[key]]
    lines += ['', NOTICE, '', 'You can revisit this summary for motivation or use your own examples as input to resume work.', '']
    return '\n'.join(lines)


def html_document(data, text):
    template_path = Path(__file__).resolve().parents[1] / 'assets' / 'summary.html'
    template = template_path.read_text(encoding='utf-8')
    values = {
        'TITLE': html.escape(data['title']),
        'DEMO': '<p class="demo">Fictional demo · These examples are not a real person’s record.</p>' if data['is_demo'] else '',
        'ACCOMPLISHMENTS': '\n'.join('<li id="accomplishment-' + entry['id'] + '"><p>' + html.escape(entry['text']) + '</p></li>' for entry in data['accomplishments']),
        'ENCOURAGEMENT': '\n'.join('<p>' + html.escape(item) + '</p>' for item in data['encouragement']),
        'NEXT_STEPS': '\n'.join('<li>' + html.escape(item) + '</li>' for item in data['next_steps']),
        'NOTICE': html.escape(NOTICE),
        'TEXT_B64': base64.b64encode(text.encode('utf-8')).decode('ascii'),
    }
    # Single-pass substitution prevents user text that resembles a token from being reinterpreted.
    return re.sub(r'@@([A-Z_0-9]+)@@', lambda match: values[match.group(1)], template)


def load_input(stream):
    payload = stream.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise SummaryError('Input exceeds 256 KiB.')
    try:
        return json.loads(payload.decode('utf-8'))
    except (UnicodeError, ValueError, RecursionError) as error:
        raise SummaryError('Input must be valid UTF-8 JSON.') from error


def render(raw, output_dir):
    data = validate(raw)
    text = text_document(data)
    page = html_document(data, text)
    parent = Path(output_dir).expanduser().resolve()
    parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.summary-', dir=str(parent)))
    destination = parent / ('revision-' + uuid.uuid4().hex[:12])
    try:
        (temporary / 'summary.html').write_text(page, encoding='utf-8')
        (temporary / 'summary.txt').write_text(text, encoding='utf-8')
        # Same-filesystem rename makes the pair visible only after both writes complete.
        os.rename(str(temporary), str(destination))
    except Exception:
        shutil.rmtree(str(temporary), ignore_errors=True)
        raise
    return {'html_path': str(destination / 'summary.html'), 'text_path': str(destination / 'summary.txt')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='-', help='UTF-8 JSON input file, or - for standard input')
    parser.add_argument('--output-dir', required=True, help='Parent directory for complete revisions')
    args = parser.parse_args()
    try:
        if args.input == '-':
            raw = load_input(sys.stdin.buffer)
        else:
            with open(args.input, 'rb') as stream:
                raw = load_input(stream)
        result = render(raw, args.output_dir)
    except (SummaryError, OSError) as error:
        # Validation errors contain field names only; never echo the person's submitted content.
        message = str(error) if isinstance(error, SummaryError) else 'Could not read input or write the summary files. Check file access and retry.'
        print(message, file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
