"""Kiểm một commit có kèm bàn giao hay không.

Chốt chặn cho lỗi "làm xong việc nhưng quên ghi nhật ký / sổ việc". Lỗi này
đã lặp lại hai lần (2026-11-27, 2026-11-28) dù luật đã ghi trong AGENTS.md
và script ban_giao.py đã có — vì bước cuối chỉ dựa vào trí nhớ.

Chạy tay:

    python3 tools/kiem_ban_giao.py                # HEAD
    python3 tools/kiem_ban_giao.py --commit HEAD~3
    python3 tools/kiem_ban_giao.py --ngay-cay      # bỏ qua, không phạt

Dùng như hàm:

    from tools.kiem_ban_giao import thieu_ban_giao
    thieu = thieu_ban_giao("HEAD~1")

Thoát mã 1 khi thiếu — nghĩa là commit đó chưa bàn giao xong.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

# Hai tệp bắt buộc phải có trong commit, vì phiên sau chỉ đọc được repo.
BAT_BUOC = ["tai-lieu/NHAT-KY.md", "tai-lieu/VIEC-CAN-LAM.md"]

# Đuôi tệp KHÔNG phải mã: ảnh, âm thanh, video, dữ liệu sinh tự động.
# Commit chỉ có những thứ này thì không cần bàn giao — đó là kết quả của việc
# đã ghi trước đó, không phải việc mới.
#
# `.html` CỐ Ý không nằm ở đây: trang HTML viết tay là việc làm thật, phải bàn
# giao. Trang sinh tự động thì script sinh ra không kèm nhật ký, nên nếu chặn
# sẽ chặn oan — cách xử là `--ngay-cay`, không phải nới danh sách này.
KHONG_CAN = (
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico",
    ".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm",
    ".pyc", ".lock", ".json",
)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=GOC, capture_output=True,
                          text=True, check=True).stdout


def commit_ton_tai(ref: str) -> bool:
    try:
        git("rev-parse", "--verify", f"{ref}^{{commit}}")
        return True
    except subprocess.CalledProcessError:
        return False


def tep_trong_commit(ref: str) -> list[str]:
    """Tệp commit này thay đổi, so với cha nó."""
    ra = git("diff-tree", "--no-commit-id", "--name-only", "-r", ref)
    return [d for d in ra.splitlines() if d.strip()]


def thieu_ban_giao(ref: str = "HEAD") -> list[str]:
    """Danh sách tệp bàn giao bị thiếu. Rỗng nghĩa là đạt.

    Bỏ qua (trả rỗng) khi:
    - ref không tồn tại (commit đầu tiên, hoặc đang kiểm trước khi commit)
    - commit chỉ đụng ảnh/dữ liệu sinh tự động
    """
    if not commit_ton_tai(ref):
        return []
    tep = tep_trong_commit(ref)
    if not tep:
        return []
    if all(t.lower().endswith(KHONG_CAN) for t in tep):
        return []
    return [t for t in BAT_BUOC if t not in tep]


def thieu_trong_cay() -> list[str]:
    """Kiểm TRƯỚC khi commit: cây làm việc có sửa mã mà chưa sửa bàn giao.

    Cần hàm này vì chốt chặn theo commit chỉ bắt được lỗi SAU khi commit —
    lúc chạy test thì commit chưa có. Đây là chỗ bắt đúng thời điểm.
    """
    ra = git("status", "--porcelain")
    tep = []
    for dong in ra.splitlines():
        if len(dong) < 4:
            continue
        duong = dong[3:].strip().strip('"')
        if " -> " in duong:                 # đổi tên: lấy tên mới
            duong = duong.split(" -> ")[-1]
        tep.append(duong)
    if not tep:
        return []                           # cây sạch: không có gì để bàn giao
    if all(t.lower().endswith(KHONG_CAN) for t in tep):
        return []
    return [t for t in BAT_BUOC if t not in tep]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--commit", default="HEAD", help="ref cần kiểm, mặc định HEAD")
    ap.add_argument("--ngay-cay", action="store_true",
                    help="bỏ qua kiểm (dùng khi chỉ commit ảnh/dữ liệu)")
    ap.add_argument("--cay", action="store_true",
                    help="kiểm cây làm việc chưa commit thay vì một commit")
    a = ap.parse_args()

    if a.ngay_cay:
        print("Bỏ qua kiểm bàn giao (--ngay-cay).")
        return

    if a.cay:
        thieu = thieu_trong_cay()
        if not thieu:
            print("✓ Cây làm việc: bàn giao đã cập nhật (hoặc không có gì để bàn giao).")
            return
        print("✗ Cây làm việc có thay đổi nhưng CHƯA cập nhật bàn giao:")
        for t in thieu:
            print(f"  - {t}")
        print("\nXong việc thì ghi nhật ký + sổ việc TRƯỚC khi báo xong cho người dùng.")
        sys.exit(1)

    if not commit_ton_tai(a.commit):
        print(f"Bỏ qua: {a.commit} chưa tồn tại.")
        return

    thieu = thieu_ban_giao(a.commit)
    if not thieu:
        print(f"✓ {a.commit} có đủ bàn giao.")
        return

    print(f"✗ {a.commit} THIẾU bàn giao:")
    for t in thieu:
        print(f"  - {t} chưa được sửa trong commit này")
    print("\nPhiên sau mở repo sẽ không biết việc vừa làm. Sửa rồi commit lại,")
    print("hoặc dùng --ngay-cay nếu commit này chỉ có ảnh/dữ liệu sinh tự động.")
    sys.exit(1)


if __name__ == "__main__":
    main()
