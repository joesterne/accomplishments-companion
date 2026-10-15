#!/usr/bin/env python3
"""Build the Gemini CLI skill and a Gemini Apps ZIP with SKILL.md at its root."""
import argparse
import sys

if __package__:
    from . import skill_package as common
else:
    import skill_package as common

ROOT = common.ROOT
NAME = 'accomplishments-companion-gemini'


def package_files(root=ROOT):
    files = common.package_files('gemini', NAME, root)
    # Use a documented text extension for the Gemini Apps uploader.
    files['LICENSE.txt'] = files.pop('LICENSE')
    return files


def archive_bytes(files):
    # Gemini Apps specifies SKILL.md in the archive's main folder.
    return common.archive_bytes(files, '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check the Gemini copy without writing')
    args = parser.parse_args()
    try:
        files = package_files()
        destination = ROOT / '.gemini/skills' / NAME
        if args.check:
            drift = common.check_skill(destination, files)
            if drift:
                print('Gemini package differs: ' + ', '.join(drift), file=sys.stderr)
                return 1
            print('Gemini skill matches its shared sources and runtime adapter.')
        else:
            common.write_skill(destination, files)
            archive = ROOT / 'outputs/packages/accomplishments-companion-gemini.zip'
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(archive_bytes(files))
            print('Gemini CLI skill: ' + str(destination))
            print('Gemini Apps upload ZIP: ' + str(archive))
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
