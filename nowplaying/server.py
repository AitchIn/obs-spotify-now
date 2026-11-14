import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .state import config, cover, info

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/custom.css": ("custom.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}

_server = None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, name, ctype):
        try:
            with open(os.path.join(WEB_DIR, name), "rb") as f:
                body = f.read()
        except OSError:
            body = b""
        self._send(200, ctype, body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ROUTES:
            self._file(*ROUTES[path])
        elif path == "/info":
            self._send(200, "application/json", json.dumps(info).encode())
        elif path == "/config":
            self._send(200, "application/json", json.dumps(config).encode())
        elif path == "/cover":
            data = cover["data"]
            ctype = "image/png" if data[:4] == b"\x89PNG" else "image/jpeg"
            self._send(200 if data else 404, ctype, data)
        else:
            self._send(404, "text/plain", b"not found")


def port():
    return _server.server_address[1] if _server else None


def start(new_port):
    global _server
    stop()
    try:
        _server = ThreadingHTTPServer(("127.0.0.1", new_port), Handler)
    except OSError as e:
        print(f"[Spotify NowPlaying] Port {new_port} unavailable: {e}")
        return
    threading.Thread(target=_server.serve_forever, daemon=True).start()
    print(f"[Spotify NowPlaying] Overlay running at http://localhost:{new_port}/")


def stop():
    global _server
    if _server:
        _server.shutdown()
        _server.server_close()
        _server = None
