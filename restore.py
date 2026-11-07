"""Restore recently installed user skills from pinned GitHub sources."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    lock = json.loads((root / 'skills-lock.json').read_text(encoding='utf-8'))
    if lock.get('format_version') != 1:
        raise ValueError('Unsupported lock format')
    codex_home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Show the plan without downloading or installing')
    parser.add_argument('--dest', type=Path, default=codex_home / 'skills', help='Target user skill directory')
    parser.add_argument('--installer', type=Path, help='Optional path to the Codex install-skill-from-github.py helper')
    args = parser.parse_args()
    dest = args.dest.expanduser().absolute()
    helper = args.installer or codex_home / 'skills' / '.system' / 'skill-installer' / 'scripts' / 'install-skill-from-github.py'
    names = set()
    jobs = []
    skipped = 0
    for source in lock['sources']:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source['repository']):
            raise ValueError('Invalid repository')
        if not re.fullmatch(r'[0-9a-f]{40}', source['commit']):
            raise ValueError('Source is not pinned to a full commit')
        pending = []
        for path in source['paths']:
            parts = PurePosixPath(path).parts
            if not parts or any(not re.fullmatch(r'[a-z0-9][a-z0-9-]*', p) for p in parts):
                raise ValueError('Invalid skill path: ' + path)
            name = parts[-1]
            if name in names:
                raise ValueError('Duplicate skill: ' + name)
            names.add(name)
            target = dest / name
            if target.exists() or target.is_symlink():
                if not (target / 'SKILL.md').is_file():
                    raise ValueError('Existing destination is not a skill: ' + str(target))
                print('SKIP existing skill (version not verified): ' + name)
                skipped += 1
            else:
                pending.append(path)
        if pending:
            jobs.append((source, pending))
    if len(names) != lock['skill_count']:
        raise ValueError('Skill count mismatch')
    print('Collections: %d; skills: %d; to install: %d; existing: %d' % (
        len(lock['sources']), len(names), sum(len(paths) for _, paths in jobs), skipped))
    print('Destination: ' + str(dest))
    if args.dry_run:
        for source, paths in jobs:
            print('%s @ %s: %d skills' % (source['repository'], source['commit'], len(paths)))
        return 0
    if jobs and not helper.is_file():
        raise ValueError('Codex skill installer not found. Use --installer to specify its location, or ask Codex to install the sources in skills-lock.json.')
    for source, paths in jobs:
        subprocess.run([
            sys.executable, str(helper), '--repo', source['repository'],
            '--ref', source['commit'], '--method', 'git', '--dest', str(dest),
            '--path', *paths,
        ], check=True)
    missing = [name for name in names if not (dest / name / 'SKILL.md').is_file()]
    if missing:
        raise ValueError('Missing skills after installation: ' + ', '.join(sorted(missing)))
    print('All %d user skill folders are present. Open a new Codex chat.' % len(names))
    if skipped:
        print('Existing skills were kept; their versions may differ from the lock file.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
