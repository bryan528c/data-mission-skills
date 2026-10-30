#!/usr/bin/env python3
"""Copy the complete skill into one project; offline, no overwrites."""
import argparse
from pathlib import Path
import stat
import sys

SKILL_NAME = 'data-mission-partner'
SOURCE = Path(__file__).resolve().parents[1] / 'skills' / SKILL_NAME


class InstallError(Exception):
    pass


def check_path(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError('Symbolic link is not supported: ' + str(part))
        if part.exists():
            info = part.lstat()
            if getattr(info, 'st_file_attributes', 0) & 0x400:
                raise InstallError('Linked directory is not supported: ' + str(part))


def make_plan(target, source=SOURCE):
    target = Path(target).expanduser().absolute()
    check_path(target)
    if not target.is_dir() or target == Path(target.anchor) or target == Path.home():
        raise InstallError('Choose an existing task project directory.')
    target = target.resolve()
    check_path(source)
    if not (source / 'SKILL.md').is_file():
        raise InstallError('The source skill is incomplete.')
    destination = target / '.agents' / 'skills' / SKILL_NAME
    pairs = []
    for path in sorted(source.rglob('*')):
        check_path(path)
        if path.is_dir():
            continue
        if not stat.S_ISREG(path.stat().st_mode):
            raise InstallError('Source must contain regular files only.')
        dest = destination / path.relative_to(source)
        check_path(dest)
        try:
            dest.resolve().relative_to(target)
        except ValueError:
            raise InstallError('Destination escapes the project.')
        for parent in dest.parents:
            if parent.exists() and not parent.is_dir():
                raise InstallError('A destination directory is a file: ' + str(parent))
        if dest.exists() and (not dest.is_file() or dest.read_bytes() != path.read_bytes()):
            raise InstallError('Existing content preserved; conflict: ' + str(dest))
        pairs.append((path, dest))
    return target, pairs


def run(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    try:
        target, pairs = make_plan(args.target)
        missing = [(src, dst) for src, dst in pairs if not dst.exists()]
        if args.check:
            if missing:
                raise InstallError('Some skill files have not been installed.')
            print('FILES MATCH. Host discovery and behavior have not been tested.')
            return 0
        for src, dst in missing:
            print(('COPY ' if args.apply else 'WOULD COPY ') + str(dst.relative_to(target)))
            if args.apply:
                dst.parent.mkdir(parents=True, exist_ok=True)
                check_path(dst)
                with dst.open('xb') as stream:
                    stream.write(src.read_bytes())
        print('INSTALLED.' if args.apply else 'PREVIEW ONLY. No files changed.')
        print('The whole skill, references and notices travel together. Check discovery in your host.')
        return 0
    except (InstallError, OSError, ValueError) as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(run())
