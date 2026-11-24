#!/usr/bin/env python3
"""Đo độ gãy khúc của nét mực trong ảnh (chỉ số "răng cưa" mà người dùng thấy).

Cách đo: đếm chu vi của mảng mực đậm, rồi làm trơn hình học (đóng/mở + gaussian) và
đếm lại. Nét liền mạch thì hai chu vi sát nhau; nét chắp vụn / zíc-zắc thì chu vi thô
lớn hơn nhiều lần.

  tỉ lệ < 1.3  : nét liền mạch, tốt
  tỉ lệ 1.3-2  : hơi gãy
  tỉ lệ > 3    : gãy nặng, đọc ra như tranh trừu tượng

Chạy: python3 tools/do_net_anh.py [thư mục]
"""
import glob
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

MAC_DINH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "docs", "assets", "scene")


def chu_vi(m):
    return int((m & ~np.roll(m, 1, 0)).sum() + (m & ~np.roll(m, -1, 0)).sum()
               + (m & ~np.roll(m, 1, 1)).sum() + (m & ~np.roll(m, -1, 1)).sum())


def do(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32) / 255.0
    ink = a < 0.45
    if ink.sum() < 2000:
        return None
    tho = chu_vi(ink)
    sm = ndi.binary_closing(ink, structure=np.ones((5, 5)))
    sm = ndi.binary_opening(sm, structure=np.ones((3, 3)))
    sm = ndi.gaussian_filter(sm.astype(np.float32), 2.0) > 0.5
    muot = chu_vi(sm)
    if muot < 100:
        return None
    return tho / muot, float(ink.mean() * 100)


def main() -> int:
    d = sys.argv[1] if len(sys.argv) > 1 else MAC_DINH
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "*.jpg"))):
        r = do(p)
        if r:
            rows.append((os.path.basename(p), r[0], r[1]))
    if not rows:
        print("không có ảnh nào để đo trong", d)
        return 1

    rows.sort(key=lambda x: -x[1])
    print(f"{'ảnh':32}{'mực%':>7}{'gãy':>8}  đánh giá")
    for n, ty, muc in rows:
        danh = "NẶNG" if ty > 3 else ("hơi gãy" if ty > 1.3 else "liền mạch")
        print(f"{n:32}{muc:6.1f}{ty:8.2f}  {danh}")

    tb = sum(r[1] for r in rows) / len(rows)
    nang = sum(1 for r in rows if r[1] > 3)
    print(f"\n{len(rows)} ảnh · trung bình {tb:.2f} · gãy nặng {nang} ảnh")
    print("Nét liền mạch cần < 1.3. Ảnh tạo trước khi sửa prompt sẽ vẫn gãy — phải tạo lại.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
