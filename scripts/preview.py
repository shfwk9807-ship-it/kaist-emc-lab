"""Preview this project's simple Jekyll layout without installing Ruby.

This helper is for local preview only. GitHub Pages uses Jekyll itself.
"""
from functools import partial
from html import escape
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = {"index", "professor", "members", "research", "publications", "projects", "news", "contact"}

def load_entries(kind, root=ROOT):
    directory = root / "_data" / kind
    entries = []
    for item in sorted(directory.glob("*.json")):
        with item.open(encoding="utf-8-sig") as stream:
            value = json.load(stream)
        if not isinstance(value, dict):
            raise ValueError(f"{item} must contain a JSON object")
        entries.append(value)
    return entries

class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path in ("/data/publications.json", "/data/news.json"):
            try:
                data = json.dumps(load_entries(Path(path).stem), ensure_ascii=False).encode("utf-8")
            except (OSError, ValueError, json.JSONDecodeError):
                self.send_error(500, "Content data could not be read; run scripts/validate_content.py")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        name = "index" if path == "/" else Path(path).stem
        if (path == "/" or path == f"/{name}.html") and name in PAGES:
            try:
                raw = (ROOT / f"{name}.html").read_text(encoding="utf-8-sig")
                parts = raw.split("---", 2)
                if len(parts) != 3:
                    raise ValueError("Missing page front matter")
                metadata = dict(line.split(":", 1) for line in parts[1].strip().splitlines())
                layout = (ROOT / "_layouts" / "default.html").read_text(encoding="utf-8-sig")
                html = layout.replace("{{ page.title | escape }}", escape(metadata["title"].strip(), quote=True))
                html = html.replace("{{ page.page_id | escape }}", escape(metadata["page_id"].strip(), quote=True))
                html = html.replace("{{ content }}", parts[2])
                data = html.encode("utf-8")
            except (OSError, ValueError, KeyError):
                self.send_error(500, "Preview template could not be rendered")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path.startswith('/assets/') or path.startswith('/data/'):
            return super().do_GET()
        self.send_error(404)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preview the KAIST EMC Lab site locally')
    parser.add_argument('--port', type=int, default=8001)
    args = parser.parse_args()
    handler = partial(PreviewHandler, directory=str(ROOT))
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        print(f'Preview: http://127.0.0.1:{args.port}/', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
