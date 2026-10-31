"""Smoke-test the real Jekyll build on an isolated copy with synthetic records."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='emclab-build-') as tmp:
    work = Path(tmp) / 'source'
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.backups', '.previous-local-design', '_site', '__pycache__', '.bundle'))
    paper = {'title': 'Synthetic CI paper', 'authors': 'Test Author', 'venue': 'Test Venue',
             'year': 2024, 'type': 'International Journal Papers', 'doi': '10.1234/example'}
    news = {'title': 'Synthetic CI news', 'date': '2024-05-09', 'category': 'NEWS', 'summary': 'Test'}
    for kind, record in [('publications', paper), ('news', news)]:
        (work / '_data' / kind / 'ci-test.json').write_text(json.dumps(record), encoding='utf-8')
    out = Path(tmp) / 'site'
    subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--source', str(work), '--destination', str(out), '--baseurl', '/kaist-emc-lab'], cwd=ROOT, check=True)
    for kind, record in [('publications', paper), ('news', news)]:
        result = json.loads((out / 'data' / f'{kind}.json').read_text(encoding='utf-8-sig'))
        assert record in result, f'{kind} entry missing from built JSON'
    for page in ['index', 'professor', 'members', 'research', 'publications', 'projects', 'news', 'contact']:
        html = (out / f'{page}.html').read_text(encoding='utf-8-sig')
        assert f'data-page="{page}"' in html and 'assets/announcement.js' in html, page
    print('Jekyll build and generated content passed.')
