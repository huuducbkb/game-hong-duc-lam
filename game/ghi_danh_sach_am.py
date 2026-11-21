"""Ghi danh sách file tiếng cảnh đang có vào docs/assets/am/danh-sach.json.

Game đọc file này để biết nhóm nào đã có bản ghi thật, nhóm nào còn dùng tiếng
tổng hợp. Không đọc trực tiếp thư mục được (GitHub Pages không có directory
listing), nên phải ghi sẵn.

Chạy: python3 game/ghi_danh_sach_am.py
"""
import io
import json
import os

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = ["docs/assets/am", "assets/am"]


def quet(thu_muc):
    ra = {}
    if not os.path.isdir(thu_muc):
        return ra
    for ten in sorted(os.listdir(thu_muc)):
        if not ten.lower().endswith(".mp3"):
            continue
        duong = os.path.join(thu_muc, ten)
        ra[ten[:-4]] = {"file": ten, "bytes": os.path.getsize(duong)}
    return ra


if __name__ == "__main__":
    ds = quet(os.path.join(GOC, "docs", "assets", "am"))
    chu = json.dumps(ds, ensure_ascii=False, indent=2, sort_keys=True)
    for d in DS:
        p = os.path.join(GOC, d, "danh-sach.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, "w", encoding="utf-8").write(chu + "\n")
    print(f"da ghi {len(ds)} nhom tieng:", ", ".join(ds) or "(chua co)")
