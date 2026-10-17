"""Build the Claude skill and a deterministic upload ZIP from shared sources."""
import argparse
import sys

if __package__:
    from . import skill_package as common
else:
    import skill_package as common

ROOT = common.ROOT
NAME = 'accomplishments-companion'
DESCRIPTION = common.DESCRIPTION
SHARED = common.SHARED
write_skill = common.write_skill
check_skill = common.check_skill


def package_files(root=ROOT):
    return common.package_files('claude', NAME, root)


def archive_bytes(files):
    return common.archive_bytes(files, NAME)


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
