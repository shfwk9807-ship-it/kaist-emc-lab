"""Create a timestamped source snapshot; copy it to independent storage."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import zipfile

ROOT = Path(__file__).resolve().parent.parent
INCLUDE_DIRS = ('assets', 'data', '_data', '_layouts', 'scripts', 'tests', 'docs', '.github')
INCLUDE_FILES = ('index.html', 'professor.html', 'members.html', 'research.html',
                 'publications.html', 'projects.html', 'news.html', 'contact.html',
                 '_config.yml', '.pages.yml', 'Gemfile', 'README.md', '.gitignore')

def main():
    parser = argparse.ArgumentParser(description='Create a source backup (not Git history)')
    parser.add_argument('--output', type=Path, help='Output ZIP; must not already exist')
    args = parser.parse_args()
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    if args.output is None:
        (ROOT / '.backups').mkdir(exist_ok=True)
    output = args.output or ROOT / '.backups' / f'emclab-{now}.zip'
    output = output.resolve()
    if not output.parent.is_dir():
        raise SystemExit(f'Output directory does not exist: {output.parent}')
    files = [ROOT / name for name in INCLUDE_FILES if (ROOT / name).is_file()]
    for name in INCLUDE_DIRS:
        directory = ROOT / name
        if directory.is_dir():
            files.extend(p for p in directory.rglob('*') if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, path.relative_to(ROOT).as_posix())
    print(f'Backup created: {output}')
    print('Copy this snapshot to separate storage. It does not contain Git history.')

if __name__ == '__main__':
    main()
