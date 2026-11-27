"""Sinh danh sách link bàn giao cuối phiên làm việc.

Chạy TRƯỚC khi báo xong cho người dùng:

    python3 tools/ban_giao.py                 # trang đã đổi trong commit HEAD
    python3 tools/ban_giao.py --tu HEAD~3     # gộp 3 commit gần nhất
    python3 tools/ban_giao.py --khong-kiem    # in link, không gọi mạng

Người dùng muốn một danh sách **cố định năm link**, không phải link trang đã
đổi — họ mở đúng năm chỗ đó để làm việc. Script in đúng năm, theo thứ tự:

  1. Xưởng âm thanh
  2. Xưởng ảnh
  3. Xưởng video
  4. Game để chơi
  5. Sơ đồ cốt truyện

Việc script làm:
1. Dựng URL của năm chỗ đó.
2. Gọi thử từng URL và báo mã trả về — không gửi link chết cho người dùng.
3. In link commit của khoảng đang báo.
4. Nhắc nếu nhật ký / sổ việc chưa được commit cùng phiên.

Người dùng chỉ có điện thoại, không có terminal: link chết là mất luôn khả năng
kiểm chứng. Vì vậy bước 3 không được bỏ.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
PAGES = "https://huuducbkb.github.io/game-hong-duc-lam"
REPO = "https://github.com/huuducbkb/game-hong-duc-lam"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=GOC, capture_output=True,
                          text=True, check=True).stdout


def commit_trong_khoang(tu: str | None) -> list[tuple[str, str]]:
    """[(sha, tiêu đề)] của HEAD, hoặc của `tu..HEAD` khi có `tu`."""
    dai = "--format=%h\t%s"
    if tu:
        dong = git("log", f"{tu}..HEAD", dai).strip()
    else:
        dong = git("log", "-1", dai).strip()
    ra = []
    for d in dong.splitlines():
        if "\t" in d:
            sha, tieu_de = d.split("\t", 1)
            ra.append((sha.strip(), tieu_de.strip()))
    return ra


# Năm chỗ người dùng mở để làm việc. Đây là danh sách gửi cuối phiên, không
# phải "mọi trang vừa đổi" — người dùng đã nói rõ như vậy.
NAM_LINK = [
    ("Xưởng âm thanh", "xuong-am/"),
    ("Xưởng ảnh", "xuong/"),
    ("Xưởng video", "xuong-video/"),
    ("Game để chơi", "game/"),
    ("Sơ đồ cốt truyện", "nhap/so-do-cot-truyen.html"),
]


def thanh_url(duong_dan: str) -> str:
    return f"{PAGES}/{duong_dan}"


def kiem(url: str, so_lan: int = 3, cho: int = 12) -> int | str:
    """Mã HTTP. Pages mất chút thời gian triển khai nên thử lại vài lần."""
    for lan in range(so_lan):
        try:
            req = urllib.request.Request(
                f"{url}?v={int(time.time())}",
                headers={"User-Agent": "ban-giao/1"},
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status
        except urllib.error.HTTPError as e:
            ma = e.code
            if ma != 404 or lan == so_lan - 1:
                return ma
        except Exception as e:  # mạng hỏng, DNS, timeout
            if lan == so_lan - 1:
                return type(e).__name__
        time.sleep(cho)
    return "?"


def kiem_nhat_ky(tu: str | None) -> list[str]:
    """Cảnh báo khi nhật ký hoặc sổ việc chưa được commit cùng việc vừa làm.

    So theo ngày tuyệt đối là không đáng tin: đồng hồ trong máy chạy và ngày
    trong đầu phiên chat lệch nhau (đã gặp: máy 2026-11-27, phiên ghi 2026-11-17).
    Vì vậy chỉ kiểm điều đo được chắc chắn — tệp bàn giao có nằm trong commit
    của khoảng đang báo hay không.
    """
    nk = GOC / "tai-lieu" / "NHAT-KY.md"
    if not nk.exists():
        return ["KHÔNG CÓ tai-lieu/NHAT-KY.md — chưa có gì để bàn giao"]

    pham_vi = [f"{tu}..HEAD"] if tu else ["HEAD~1..HEAD"]
    try:
        doi = git("diff", "--name-only", *pham_vi).splitlines()
    except subprocess.CalledProcessError:
        doi = []

    nhac = []
    if "tai-lieu/NHAT-KY.md" not in doi:
        nhac.append("NHAT-KY.md chưa được commit trong khoảng này — "
                    "phiên sau sẽ không biết việc vừa làm")
    if "tai-lieu/VIEC-CAN-LAM.md" not in doi:
        nhac.append("VIEC-CAN-LAM.md chưa được commit trong khoảng này")
    return nhac


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tu", help="ref mốc, vd HEAD~3 — gộp nhiều commit")
    ap.add_argument("--khong-kiem", action="store_true", help="không gọi mạng")
    a = ap.parse_args()

    commits = commit_trong_khoang(a.tu)

    print("## Link bàn giao\n")
    hong = []
    for ten, duong_dan in NAM_LINK:
        url = thanh_url(duong_dan)
        if a.khong_kiem:
            print(f"- **{ten}** — {url}")
            continue
        ma = kiem(url)
        if ma == 200:
            print(f"- **{ten}** — {url}")
        else:
            print(f"- **{ten}** — {url}  ⚠ [{ma}]")
            hong.append(ten)
    print()
    if hong:
        print(f"⚠ Link hỏng: {', '.join(hong)} — Pages có thể chưa deploy xong.\n")

    if commits:
        print("## Commit\n")
        for sha, tieu_de in commits:
            print(f"- [{sha}]({REPO}/commit/{sha}) — {tieu_de}")
        print()

    nhac = kiem_nhat_ky(a.tu)
    if nhac:
        print("## ⚠ Chưa xong bàn giao\n")
        for n in nhac:
            print(f"- {n}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
