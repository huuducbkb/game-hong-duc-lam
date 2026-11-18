#!/usr/bin/env python3
"""Xử lý ảnh từ hai nguồn: thư mục xuong-inbox/ hoặc ảnh dán trong Issue.

Dùng trong GitHub Action. Ví dụ:
  python3 tools/xu_ly_inbox.py --inbox xuong-inbox --report /tmp/bao-cao.json
  python3 tools/xu_ly_inbox.py --urls-file /tmp/urls.txt --report /tmp/bao-cao.json

- inbox mode: quét ảnh trong xuong-inbox/ (đệ quy). Tên thư mục con = mã ảnh (hint).
  Xử lý xong thì XOÁ ảnh khỏi inbox (giữ file README/.gitkeep).
- urls mode: tải ảnh từ URL (ảnh dán trong Issue) rồi xử lý, không có hint.

In ra JSON báo cáo: {da_luu, can_xac_nhan, bo_qua, ghep, nhan_dien}.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import xuong_tu_dong as X  # noqa: E402

ANH_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")
GIU_LAI = {"readme.md", ".gitkeep", ".gitignore"}
TIMEOUT = 60


def _la_anh(ten: str) -> bool:
    return ten.lower().endswith(ANH_EXT)


def quet_inbox(thu_muc: str) -> list:
    """Trả [{name, data(b64), hint_key, duong_dan}]. hint_key = tên thư mục con."""
    ds = []
    for goc, _, files in os.walk(thu_muc):
        for fn in sorted(files):
            if not _la_anh(fn) or fn.lower() in GIU_LAI:
                continue
            p = os.path.join(goc, fn)
            rel = os.path.relpath(p, thu_muc)
            phan = rel.split(os.sep)
            hint = phan[0] if len(phan) > 1 else ""  # thư mục con = mã ảnh
            with open(p, "rb") as f:
                data = f.read()
            ds.append({"name": fn, "data": base64.b64encode(data).decode(),
                       "hint_key": hint, "duong_dan": p})
    return ds


def _tai(url: str) -> bytes | None:
    headers = {"User-Agent": "xuong-anh-bot"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok and "github" in url:
        headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read()
    except Exception:
        return None


def tai_tu_urls(urls: list) -> list:
    """Tải ảnh từ danh sách URL. Trả [{name, data(b64)}]."""
    ds = []
    for i, u in enumerate(urls, 1):
        u = u.strip()
        if not u:
            continue
        data = _tai(u)
        if not data:
            continue
        duoi = ".png"
        m = re.search(r"\.(png|jpe?g|webp|gif)(?:\?|$)", u, re.I)
        if m:
            duoi = "." + m.group(1).lower().replace("jpeg", "jpg")
        ds.append({"name": f"issue-{i}{duoi}", "data": base64.b64encode(data).decode()})
    return ds


def tach_url_anh(text: str) -> list:
    """Lấy URL ảnh trong nội dung Issue (markdown ảnh, HTML img, link trần)."""
    urls = []
    urls += re.findall(r"!\[[^\]]*\]\((https?://[^\s)]+)\)", text)      # ![](url)
    urls += re.findall(r'<img[^>]+src="(https?://[^"]+)"', text)         # <img src>
    for u in re.findall(r"(https?://[^\s)\"'>]+)", text):                # link trần
        if re.search(r"\.(png|jpe?g|webp|gif)(\?|$)", u, re.I) or "user-attachments" in u \
                or "user-images.githubusercontent" in u:
            urls.append(u)
    # bỏ trùng, giữ thứ tự
    thay, thay_ds = set(), []
    for u in urls:
        if u not in thay:
            thay.add(u)
            thay_ds.append(u)
    return thay_ds


def xoa_inbox(anh: list) -> None:
    for a in anh:
        p = a.get("duong_dan")
        if p and os.path.isfile(p):
            os.remove(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox", default="")
    ap.add_argument("--urls-file", default="")
    ap.add_argument("--report", default="")
    ap.add_argument("--giu-anh", action="store_true", help="không xoá ảnh khỏi inbox")
    args = ap.parse_args()

    anh = []
    nguon = ""
    if args.inbox and os.path.isdir(args.inbox):
        anh = quet_inbox(args.inbox)
        nguon = "inbox"
    elif args.urls_file and os.path.isfile(args.urls_file):
        with open(args.urls_file, encoding="utf-8") as f:
            urls = tach_url_anh(f.read())
        anh = tai_tu_urls(urls)
        nguon = "issue"

    if not anh:
        bc = {"da_luu": [], "can_xac_nhan": [], "bo_qua": [], "ghep": {}, "nhan_dien": [],
              "thong_diep": "Không tìm thấy ảnh nào để xử lý."}
        _ghi(bc, args.report)
        print(json.dumps(bc, ensure_ascii=False, indent=1))
        return 0

    bc = X.xu_ly(anh)
    bc["nguon"] = nguon

    # Xoá ảnh khỏi inbox khi đã lưu (giữ ảnh chưa xác nhận để xử lý lại).
    if nguon == "inbox" and not args.giu_anh:
        da_luu_name = {x["name"] for x in bc["da_luu"]}
        xoa_inbox([a for a in anh if a["name"] in da_luu_name])

    _ghi(bc, args.report)
    print(json.dumps(bc, ensure_ascii=False, indent=1))
    return 0


def _ghi(bc: dict, duong: str) -> None:
    if duong:
        with open(duong, "w", encoding="utf-8") as f:
            json.dump(bc, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    raise SystemExit(main())
