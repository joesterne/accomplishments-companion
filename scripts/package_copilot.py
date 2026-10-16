#!/usr/bin/env python3
"""Build the GitHub Copilot skill and an installable directory ZIP."""
import argparse
import sys

if __package__:
    from . import skill_package as common
else:
    import skill_package as common

ROOT = common.ROOT
NAME = 'accomplishments-companion-copilot'


def package_files(root=ROOT):
    return common.package_files('copilot', NAME, root)


def archive_bytes(files):
    return common.archive_bytes(files, NAME)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check the Copilot copy without writing')
    args = parser.parse_args()
    try:
        files = package_files()
        destination = ROOT / '.github/skills' / NAME
        if args.check:
            drift = common.check_skill(destination, files)
            if drift:
                print('Copilot package differs: ' + ', '.join(drift), file=sys.stderr)
                return 1
            print('Copilot skill matches its shared sources and runtime adapter.')
        else:
            common.write_skill(destination, files)
            archive = ROOT / 'outputs/packages/accomplishments-companion-copilot.zip'
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(archive_bytes(files))
            print('GitHub Copilot skill: ' + str(destination))
            print('Copilot distribution ZIP: ' + str(archive))
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
