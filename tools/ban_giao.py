"""Sinh danh sách link bàn giao cuối phiên làm việc.

Chạy TRƯỚC khi báo xong cho người dùng:

    python3 tools/ban_giao.py                 # trang đã đổi trong commit HEAD
    python3 tools/ban_giao.py --tu HEAD~3     # gộp 3 commit gần nhất
    python3 tools/ban_giao.py --khong-kiem    # in link, không gọi mạng

Script làm bốn việc, để không phải nhớ bằng trí:
1. Liệt kê trang `.html` đã đổi dưới `docs/` (gốc của GitHub Pages).
2. Đổi đường dẫn tệp thành URL công khai.
3. Gọi thử từng URL và báo mã trả về — không gửi link chết cho người dùng.
4. Nhắc nếu `tai-lieu/NHAT-KY.md` chưa có mục của hôm nay.

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
THU_MUC_WEB = "docs"  # docs/ là gốc Pages


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


def trang_da_doi(tu: str | None) -> list[str]:
    """Đường dẫn các tệp .html đã đổi dưới docs/, mới nhất trước."""
    if tu:
        pham_vi = [f"{tu}..HEAD"]
    else:
        pham_vi = ["HEAD~1..HEAD"]
    try:
        ra = git("diff", "--name-only", *pham_vi).splitlines()
    except subprocess.CalledProcessError:
        ra = []
    if not ra:
        ra = git("show", "--name-only", "--pretty=format:", "HEAD").splitlines()

    tep = []
    for d in ra:
        d = d.strip()
        if d.startswith(f"{THU_MUC_WEB}/") and d.endswith(".html"):
            if d not in tep:
                tep.append(d)
    return tep


def thanh_url(duong_dan: str) -> str:
    con = duong_dan[len(THU_MUC_WEB) + 1:]
    return f"{PAGES}/{con}"


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
    trang = trang_da_doi(a.tu)

    print("## Link bàn giao\n")
    if not trang:
        print("_Không có trang .html nào đổi trong khoảng này._\n")
    for d in trang:
        url = thanh_url(d)
        if a.khong_kiem:
            print(f"- {url}")
        else:
            ma = kiem(url)
            dau = "OK" if ma == 200 else f"**{ma}**"
            print(f"- [{ma}] {url}")
    print()

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
