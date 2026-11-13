#!/usr/bin/env python3
"""Máy chủ game Hồng Đức Tu Tiên Lộ.

Phục vụ:
  - /game          trang chơi (game/play.html)
  - /api/*         API game (tạo nhân vật, chọn, hành động tự do, lưu/nạp)
  - /              tệp tĩnh trong dự án (demo/, assets/…)
  - /keys /upload  Xưởng ảnh (dùng lại từ tools_server)

Chạy: python3 game_server.py   (mặc định cổng 12001)
"""

import json
import os
import re
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from game import engine as E  # noqa: E402

try:
    import tools_server as TS  # Xưởng ảnh (prompt + upload)
except Exception:
    TS = None

PORT = int(os.environ.get("PORT", "12001"))

_phien: dict[str, dict] = {}  # id phiên -> trạng thái (giữ trong RAM)


def _phien_id(handler) -> str:
    """Lấy/đặt id phiên qua cookie đơn giản."""
    cookie = handler.headers.get("Cookie", "")
    m = re.search(r"phien=([A-Za-z0-9_-]+)", cookie)
    if m:
        return m.group(1)
    return ""


class Handler(BaseHTTPRequestHandler):
    server_version = "HongDucGame/1.0"

    # ---------------------------------------------------------- tiện ích
    def _send(self, body, code=200, ctype="text/html; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200, extra=None):
        self._send(json.dumps(obj, ensure_ascii=False), code, "application/json; charset=utf-8", extra)

    def _body_json(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    def _state(self) -> dict | None:
        return _phien.get(_phien_id(self))

    def _set_state(self, state: dict) -> str:
        sid = _phien_id(self)
        if not sid:
            sid = os.urandom(9).hex()
        _phien[sid] = state
        return sid

    # ---------------------------------------------------------- GET
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path in ("/game", "/game/"):
            return self._serve_file("game/play.html")
        if path.startswith("/api/state"):
            st = self._state()
            if not st:
                return self._json({"co_phien": False})
            return self._json({"co_phien": True, "trang_thai": E._trang_thai_gon(st)})
        if path.startswith("/api/doan"):
            st = self._state()
            if not st:
                return self._json({"loi": "Chưa có phiên chơi"}, 400)
            return self._json(E.goi_y_hien_tai(st))

        # Xưởng ảnh
        if TS and path.startswith("/keys"):
            return self._send(TS.keys_page())
        if TS and path.startswith("/upload"):
            return self._send(TS.page())

        # tệp tĩnh
        return self._serve_file(path.lstrip("/") or "demo/index.html")

    # ---------------------------------------------------------- POST
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        data = self._body_json()

        if path == "/api/new":
            ten = (data.get("ten") or "").strip()
            if not ten:
                return self._json({"loi": "Hãy nhập tên nhân vật"}, 400)
            st = E.trang_thai_moi(ten, data.get("xuat_than") or "")
            sid = self._set_state(st)
            kq = E.bat_dau(st)
            return self._json({"phien": sid, **kq},
                              extra={"Set-Cookie": f"phien={sid}; Path=/; Max-Age=604800"})

        st = self._state()
        if not st:
            return self._json({"loi": "Chưa có phiên chơi. Hãy tạo nhân vật."}, 400)

        if path == "/api/chon":
            return self._json(E.chon(st, int(data.get("chi_so", -1))))
        if path == "/api/tu_do":
            return self._json(E.hanh_dong_tu_do(st, data.get("van_ban") or ""))
        if path == "/api/luu":
            p = E.luu(st, data.get("slot") or st["ten_nhan_vat"])
            return self._json({"ok": True, "tep": os.path.basename(p)})

        if TS and path.startswith("/upload"):
            return self._delegate_studio()

        return self._json({"loi": "Không rõ đường dẫn"}, 404)

    # ---------------------------------------------------------- phụ trợ
    def _delegate_studio(self):
        """Chuyển POST upload cho tools_server xử lý."""
        try:
            handler = TS.Handler
            handler.path = self.path
            handler.headers = self.headers
            handler.rfile = self.rfile
            handler.wfile = self.wfile
            handler.send_response = self.send_response
            handler.send_header = self.send_header
            handler.end_headers = self.end_headers
            handler.do_POST()
        except Exception as ex:
            self._send(f"Lỗi upload: {ex}", 500)

    def _serve_file(self, rel: str):
        rel = rel.split("?")[0]
        path = os.path.normpath(os.path.join(ROOT, rel))
        if not path.startswith(ROOT) or not os.path.isfile(path):
            return self._send("Không tìm thấy", 404, "text/plain; charset=utf-8")
        ext = os.path.splitext(path)[1].lower()
        ctype = {
            ".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml", ".webp": "image/webp", ".ico": "image/x-icon",
        }.get(ext, "application/octet-stream")
        with open(path, "rb") as f:
            return self._send(f.read(), 200, ctype)

    def log_message(self, *a):
        pass


def main():
    os.makedirs(E.SAVES_DIR, exist_ok=True)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Máy chủ game chạy ở cổng {PORT} — mở /game để chơi")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
