"""Validate editable lab data; usable locally and in CI without dependencies."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
TYPES = {'International Journal Papers', 'International Conference Papers', 'Domestic Publications', 'Patents'}
GROUPS = {'Professor', 'Ph.D. Students', 'M.S. Students', 'Alumni'}
STATUSES = {'Ongoing Projects', 'Completed Projects'}

def validate(root):
    errors = []
    def problem(path, text):
        errors.append(f'{path.relative_to(root)}: {text}')
    def read(path, expected):
        try:
            value = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(value, expected):
                raise ValueError(f'expected {expected.__name__}')
            return value
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            problem(path, str(exc))
            return None
    def required_string(obj, path, key):
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            problem(path, f'{key} must be nonempty text')
    for kind in ('publications', 'news'):
        directory = root / '_data' / kind
        if not directory.is_dir():
            errors.append(f'Missing directory: _data/{kind}')
            continue
        for path in sorted(directory.glob('*.json')):
            obj = read(path, dict)
            if obj is None:
                continue
            required_string(obj, path, 'title')
            if kind == 'publications':
                for key in ('authors', 'venue'):
                    required_string(obj, path, key)
                if obj.get('type') not in TYPES:
                    problem(path, 'type must be one of the four publication types')
                year = obj.get('year')
                if isinstance(year, bool) or not isinstance(year, int) or not 1000 <= year <= 9999:
                    problem(path, 'year must be a four-digit number')
                doi = obj.get('doi', '')
                if doi and (not isinstance(doi, str) or not re.fullmatch(r'(?:https?://(?:dx\.)?doi\.org/)?10\.\d{4,9}/\S+', doi, re.I)):
                    problem(path, 'doi must be a DOI or a doi.org URL')
            else:
                raw_date = obj.get('date')
                try:
                    if not isinstance(raw_date, str) or date.fromisoformat(raw_date).isoformat() != raw_date:
                        raise ValueError()
                except ValueError:
                    problem(path, 'date must be YYYY-MM-DD')
                required_string(obj, path, 'category')
                required_string(obj, path, 'summary')
                url = obj.get('url', '')
                if url and (not isinstance(url, str) or urlparse(url).scheme not in ('http', 'https') or not urlparse(url).netloc):
                    problem(path, 'url must be an absolute HTTP(S) URL or empty')
    for name, allowed, field in [('members', GROUPS, 'group'), ('projects', STATUSES, 'status')]:
        path = root / 'data' / f'{name}.json'
        value = read(path, list)
        if value is None:
            continue
        for i, obj in enumerate(value):
            if not isinstance(obj, dict):
                problem(path, f'item {i+1} must be an object')
                continue
            required_string(obj, path, 'name' if name == 'members' else 'title')
            if obj.get(field) not in allowed:
                problem(path, f'item {i+1}: invalid {field}')
    path = root / 'data' / 'announcement.json'
    notice = read(path, dict)
    if notice is not None:
        if not isinstance(notice.get('enabled'), bool):
            problem(path, 'enabled must be true or false')
        if notice.get('enabled'):
            for field in ('id', 'title', 'message'):
                required_string(notice, path, field)
        hours = notice.get('dismiss_hours')
        if isinstance(hours, bool) or not isinstance(hours, (int, float)) or not 0 < hours <= 720:
            problem(path, 'dismiss_hours must be greater than 0 and no more than 720')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print('Content validation passed.')
