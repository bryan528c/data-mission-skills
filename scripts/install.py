#!/usr/bin/env python3
"""Copy the complete skill into one project; offline, no overwrites."""
import argparse
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

SKILL_NAME = 'data-mission-partner'
SOURCE = Path(__file__).resolve().parents[1] / 'skills' / SKILL_NAME
REQUIRED_SOURCE_FILES = (
    'SKILL.md', 'agents/openai.yaml', 'NOTICE.md',
    'licenses/ColdTbrew-MIT.txt', 'licenses/JINwonLEE-MIT.txt',
    'licenses/JINwonLEE-UPSTREAM-NOTICE.txt',
    'licenses/pstack-NOTICE.txt', 'licenses/PROJECT-MIT.txt',
)


class InstallError(Exception):
    pass


class SourceError(InstallError):
    pass


def check_path(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError('Symbolic link is not supported: ' + str(part))
        if part.exists():
            info = part.lstat()
            if getattr(info, 'st_file_attributes', 0) & 0x400:
                raise InstallError('Linked directory is not supported: ' + str(part))


def validate_source(source):
    """Check the portable skill before planning any writes; shared with package checks."""
    try:
        source = Path(source).expanduser().absolute()
        check_path(source)
        if not source.is_dir():
            raise InstallError('Missing skill directory: ' + str(source))
        source = source.resolve()
        files = []
        pending = [source]
        while pending:
            for path in pending.pop().iterdir():
                check_path(path)
                if path.is_dir():
                    pending.append(path)
                elif stat.S_ISREG(path.stat().st_mode):
                    files.append(path)
                else:
                    raise InstallError('Source must contain regular files only.')
        for rel in REQUIRED_SOURCE_FILES:
            path = source / rel
            if not path.is_file() or not path.read_text(encoding='utf-8').strip():
                raise InstallError('Missing or empty required source file: ' + rel)
        core = (source / 'SKILL.md').read_text(encoding='utf-8')
        refs = list((source / 'references').glob('*.md'))
        if len(refs) != 5:
            raise InstallError('Expected five focused reference files.')
        for path in refs:
            if 'references/' + path.name not in core:
                raise InstallError('Unrouted reference: ' + path.name)
        # The package uses inline Markdown links. Check every local linked file,
        # including references between documents and the portable license notices.
        for document in files:
            if document.suffix != '.md':
                continue
            content = document.read_text(encoding='utf-8')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                target = target.strip()
                if target.startswith('<'):
                    target = target[1:target.index('>')]
                else:
                    target = target.split(' "', 1)[0].split(" '", 1)[0]
                url = urlsplit(target)
                if url.scheme in {'https', 'http', 'mailto'}:
                    continue
                if not url.path and not url.netloc and not url.scheme:
                    continue
                linked = document.parent / unquote(url.path)
                if url.scheme or url.netloc or Path(unquote(url.path)).is_absolute():
                    raise InstallError('Local link must stay inside the skill: ' + target)
                check_path(linked)
                linked = linked.resolve()
                if not linked.is_relative_to(source) or not linked.is_file():
                    raise InstallError('Missing or out-of-skill local link: ' + target)
        return source, sorted(files)
    except (InstallError, OSError, ValueError) as exc:
        raise SourceError('Source incomplete or unusable: ' + str(exc)) from exc


def make_plan(target, source=None):
    source, files = validate_source(SOURCE if source is None else source)
    target = Path(target).expanduser().absolute()
    check_path(target)
    if not target.is_dir() or target == Path(target.anchor) or target == Path.home():
        raise InstallError('Choose an existing task project directory.')
    target = target.resolve()
    destination = target / '.agents' / 'skills' / SKILL_NAME
    check_path(destination)
    resolved_destination = destination.resolve()
    if resolved_destination.is_relative_to(source) or source.is_relative_to(resolved_destination):
        raise InstallError('Source and destination overlap; nested or self-copy is not allowed.')
    pairs = []
    for path in files:
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
    except SourceError as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        print('Direct reading is not confirmed complete. Check SKILL.md and its linked files before using it.', file=sys.stderr)
        return 2
    except (InstallError, OSError, ValueError) as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        print('The source was checked. You can read it directly at ' + str(SOURCE / 'SKILL.md') + '; this is not host registration.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(run())
