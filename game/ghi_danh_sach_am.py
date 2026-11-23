"""Ghi danh sách file tiếng cảnh đang có vào docs/assets/am/danh-sach.json.

Game đọc file này để biết nhóm nào đã có bản ghi thật, nhóm nào còn dùng tiếng
tổng hợp. Không đọc trực tiếp thư mục được (GitHub Pages không có directory
listing), nên phải ghi sẵn.

Mỗi mục ghi kèm `giay` — độ dài cảnh lấy từ du_lieu_am.py. Game dùng số này để
biết phát bao lâu: cảnh mở cửa 2 giây, cảnh thoại 3–6 giây, bối cảnh 10 giây.
Không cố định 10 giây cho mọi cảnh.

Mỗi mục cũng ghi `v` — 8 ký tự đầu của mã băm nội dung file. GitHub Pages gửi
`cache-control: max-age=600`, nên khi thay tiếng của một cảnh mà giữ nguyên tên
file, trình duyệt vẫn phát bản cũ tới 10 phút. Game gắn `?v=<mã băm>` vào địa chỉ
nên mỗi lần nội dung đổi là một địa chỉ mới, không dính bộ nhớ đệm.

Chạy: python3 game/ghi_danh_sach_am.py
"""
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from du_lieu_am import THEO_MA, GIAY_MAC_DINH  # noqa: E402

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = ["docs/assets/am", "assets/am"]


def bam(duong):
    h = hashlib.sha256()
    with open(duong, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 16), b""):
            h.update(khoi)
    return h.hexdigest()[:8]


def quet(thu_muc):
    ra = {}
    if not os.path.isdir(thu_muc):
        return ra
    for ten in sorted(os.listdir(thu_muc)):
        if not ten.lower().endswith(".mp3"):
            continue
        duong = os.path.join(thu_muc, ten)
        ma = ten[:-4]
        canh = THEO_MA.get(ma)
        ra[ma] = {
            "file": ten,
            "bytes": os.path.getsize(duong),
            "giay": canh["giay"] if canh else GIAY_MAC_DINH,
            "v": bam(duong),
        }
    return ra


if __name__ == "__main__":
    ds = quet(os.path.join(GOC, "docs", "assets", "am"))
    chu = json.dumps(ds, ensure_ascii=False, indent=2, sort_keys=True)
    for d in DS:
        p = os.path.join(GOC, d, "danh-sach.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, "w", encoding="utf-8").write(chu + "\n")
    print(f"da ghi {len(ds)} nhom tieng:", ", ".join(ds) or "(chua co)")
