#!/usr/bin/env python3
"""Soát prompt ảnh: chặn từ ngữ dạy AI vẽ nét loang / gãy khúc / trừu tượng.

Chạy: python3 tools/kiem_prompt_anh.py
In "SACH" khi không còn từ xấu; in danh sách mã ảnh vi phạm khi có.
Mã thoát 1 nếu có vi phạm, để dùng được trong CI.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import tools_server as TS  # noqa: E402

XAU = (
    "wet ink bleeding", "bleeding edges", "dry brush", "dry-brush", "paper fibre",
    "paper fiber", "suggested loosely", "loosely by", "ink splash", "blotchy",
    "wobbly edges", "rough handmade", "abstract scribble", "not detailed",
)
NET_LIEN = "continuous unbroken brush stroke"
GIAI_PHAU = "clear, correct human anatomy"


def main() -> int:
    bad = {a["key"]: [c for c in XAU if c in a["prompt"].lower()] for a in TS.ASSETS}
    bad = {k: v for k, v in bad.items() if v}
    thieu_net = [a["key"] for a in TS.ASSETS if NET_LIEN not in a["prompt"]]
    co_nguoi = [a for a in TS.ASSETS if a["key"].startswith(("nv_", "bc_", "vt_"))]
    thieu_gp = [a["key"] for a in co_nguoi
                if "human anatomy" in a["prompt"].lower() and GIAI_PHAU not in a["prompt"]]

    if bad:
        print("CÓ TỪ GÂY LOANG:")
        for k, v in bad.items():
            print(f"  {k}: {v}")
    if thieu_net:
        print("THIẾU CÂU NÉT LIỀN MẠCH:", thieu_net)
    if thieu_gp:
        print("CÓ NGƯỜI NHƯNG THIẾU GIẢI PHẪU:", thieu_gp)
    if bad or thieu_net or thieu_gp:
        return 1
    print("SACH")
    print(f"{len(TS.ASSETS)} prompt · {len(co_nguoi)} ảnh truyện/nhân vật")
    return 0


if __name__ == "__main__":
    sys.exit(main())
