"""Shared packaging for host adapters and deterministic skill archives."""
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION = ('Help job seekers recognize real accomplishments, create a supportive HTML/text '
               'summary, and correct it through conversation. Use for accomplishments reflection, '
               'not resume rewriting.')
SUMMARY_REFERENCE = 'references/summary-format.md'
SHARED = ('scripts/render_summary.py', 'assets/summary.html')


def package_files(host, name, root=ROOT):
    source = root / '.agents/skills/accomplishments-companion'
    original = (source / 'SKILL.md').read_text(encoding='utf-8')
    _, _, body = original.split('---', 2)
    summary = (source / SUMMARY_REFERENCE).read_text(encoding='utf-8')
    replacements = {
        'The renderer creates outputs under an ignored local folder; it does not make the host conversation private or local-only.':
        'Choose the output location and file-delivery method using the {host} runtime reference; the renderer does not make the host conversation private or local-only.',
        'After a successful run, provide links to the exact HTML and text paths returned.':
        'After a successful run, deliver the exact HTML and text files returned using the host-specific method in the {host} runtime reference.',
    }
    for old, new in replacements.items():
        if summary.count(old) != 1:
            raise ValueError('Shared skill changed; review the ' + host + ' adapter before packaging.')
        summary = summary.replace(old, new.format(host=host.capitalize()))
    summary = summary.replace('# Summary contract', '# Summary contract\n\n'
        f'Before creating files, read [{host.capitalize()} runtime and file delivery]({host}-runtime.md). '
        'Its host-specific output and privacy guidance takes precedence over local project defaults '
        'in the shared summary contract.', 1)
    files = {'SKILL.md': ('---\nname: ' + name + '\ndescription: ' + DESCRIPTION + '\n---' + body).encode('utf-8')}
    files[SUMMARY_REFERENCE] = summary.encode('utf-8')
    files.update({name: (source / name).read_bytes() for name in SHARED})
    files['references/' + host + '-runtime.md'] = (root / 'packaging' / (host + '-runtime.md')).read_bytes()
    files['LICENSE'] = (root / 'LICENSE').read_bytes()
    return files


def archive_bytes(files, folder):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo((folder + '/' if folder else '') + name, date_time=(2026, 1, 1, 0, 0, 0))
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
