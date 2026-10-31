import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

validator = module('validate_content')
preview = module('preview')

class ContentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ('_data/publications', '_data/news', 'data'):
            (self.root / name).mkdir(parents=True)
        self.write('data/members.json', [])
        self.write('data/projects.json', [])
        self.write('data/announcement.json', {'enabled': False, 'dismiss_hours': 24})

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def test_individual_records_are_read_and_validated(self):
        paper = {'title': 'Example test paper', 'authors': 'A. Author', 'venue': 'Test journal',
                 'year': 2024, 'type': 'International Journal Papers', 'doi': '10.1234/example'}
        news = {'title': 'Test update', 'date': '2024-05-09', 'category': 'NEWS', 'summary': 'Test'}
        self.write('_data/publications/one.json', paper)
        self.write('_data/news/one.json', news)
        self.assertEqual(validator.validate(self.root), [])
        self.assertEqual(preview.load_entries('publications', self.root), [paper])
        self.assertEqual(preview.load_entries('news', self.root), [news])

    def test_invalid_records_report_errors(self):
        self.write('_data/publications/bad.json', {'title':'', 'year':'2024','type':'wrong'})
        self.write('_data/news/bad.json', {'title':'A', 'date':'bad', 'category':'NEWS', 'summary':'X', 'url':'javascript:alert(1)'})
        errors = '\n'.join(validator.validate(self.root))
        self.assertIn('year', errors)
        self.assertIn('date', errors)
        self.assertIn('url', errors)
        self.assertIn('title', errors)

    def test_bad_json_is_not_silently_ignored(self):
        (self.root / '_data/news/broken.json').write_text('{', encoding='utf-8')
        self.assertTrue(validator.validate(self.root))
        with self.assertRaises(json.JSONDecodeError):
            preview.load_entries('news', self.root)

if __name__ == '__main__':
    unittest.main()
