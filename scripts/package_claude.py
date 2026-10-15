#!/usr/bin/env python3
"""Build the Claude skill and a deterministic upload ZIP from allowlisted sources."""
import argparse
import io
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'accomplishments-companion'
DESCRIPTION = ('Help job seekers recognize real accomplishments, create a supportive HTML/text '
               'summary, and correct it through conversation. Use for accomplishments reflection, '
               'not resume rewriting.')
SHARED = ('references/summary-format.md', 'scripts/render_summary.py', 'assets/summary.html')


def package_files(root=ROOT):
    source = root / '.agents/skills' / NAME
    original = (source / 'SKILL.md').read_text(encoding='utf-8')
    _, _, body = original.split('---', 2)
    replacements = {
        'The renderer creates outputs under an ignored local folder; it does not make the host conversation private or local-only.':
        'Choose the output location and file-delivery method using the Claude runtime reference; the renderer does not make the host conversation private or local-only.',
        'After a successful run, provide links to the exact HTML and text paths returned.':
        'After a successful run, deliver the exact HTML and text files returned using the host-specific method in the Claude runtime reference.',
    }
    for old, new in replacements.items():
        if body.count(old) != 1:
            raise ValueError('Shared skill changed; review the Claude adapter before packaging.')
        body = body.replace(old, new)
    body = body.replace('# Accomplishments Companion', '# Accomplishments Companion\n\n'
        'Before creating files, read [Claude runtime and file delivery](references/claude-runtime.md). '
        'Its host-specific output and privacy guidance takes precedence over local project defaults '
        'in the shared summary contract.', 1)
    files = {'SKILL.md': ('---\nname: ' + NAME + '\ndescription: ' + DESCRIPTION + '\n---' + body).encode('utf-8')}
    files.update({name: (source / name).read_bytes() for name in SHARED})
    files['references/claude-runtime.md'] = (root / 'packaging/claude-runtime.md').read_bytes()
    files['LICENSE'] = (root / 'LICENSE').read_bytes()
    return files


def archive_bytes(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(NAME + '/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    return buffer.getvalue()


def write_skill(destination, files):
    if destination.is_symlink():
        raise ValueError('Refusing to replace a symlinked skill directory.')
    # Preflight every path before writes, leaving unrelated skills untouched.
    for name in files:
        path = destination / name
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('Refusing to write through a symlink.')
        if path.exists() and not path.is_file():
            raise ValueError('Expected a regular skill file: ' + str(path))
    for name, content in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def check_skill(destination, files):
    return [name for name, data in files.items()
            if not (destination / name).is_file() or (destination / name).read_bytes() != data]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check the tracked Claude copy without writing')
    args = parser.parse_args()
    try:
        files = package_files()
        destination = ROOT / '.claude/skills' / NAME
        if args.check:
            drift = check_skill(destination, files)
            if drift:
                print('Claude package differs: ' + ', '.join(drift), file=sys.stderr)
                return 1
            print('Claude skill matches its shared sources and runtime adapter.')
        else:
            write_skill(destination, files)
            archive = ROOT / 'outputs/packages' / (NAME + '-claude.zip')
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(archive_bytes(files))
            print('Claude Code skill: ' + str(destination))
            print('Claude upload ZIP: ' + str(archive))
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
