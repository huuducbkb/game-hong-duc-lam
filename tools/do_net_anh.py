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
from PIL import Image, ImageFilter
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


def vung_dac_muc(a, ti_le=0.34):
    """Tìm ô vuông nhiều ĐƯỜNG NÉT nhất.

    Chọn theo mật độ cạnh (Sobel) chứ không theo lượng mực: vùng nhiều mực nhất
    thường là mảng đen đặc, cắt vào đó chỉ thấy một khối đen, không thấy nét.
    """
    h, w = a.shape
    s = int(min(h, w) * ti_le)
    buoc = max(8, s // 12)
    g = np.asarray(Image.fromarray(a).filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    canh = (g > 60).astype(np.float32)
    tich = np.pad(np.cumsum(np.cumsum(canh, 0), 1), ((1, 0), (1, 0)))

    def tong(y, x):
        return tich[y + s, x + s] - tich[y, x + s] - tich[y + s, x] + tich[y, x]

    tot, cho = -1.0, (0, 0)
    for y in range(0, h - s + 1, buoc):
        for x in range(0, w - s + 1, buoc):
            t = tong(y, x)
            if t > tot:
                tot, cho = t, (y, x)
    return cho[1], cho[0], s


def cat_can_mat(src, dst, phong=2):
    """Cắt vùng nhiều nét nhất và phóng bằng NEAREST.

    Không dùng LANCZOS: nội suy làm mượt đúng chỗ nét gãy cần phơi ra.
    """
    im = Image.open(src).convert("RGB")
    a = np.asarray(im.convert("L"))
    x, y, s = vung_dac_muc(a)
    o = im.crop((x, y, x + s, y + s)).resize((s * phong, s * phong), Image.NEAREST)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    o.save(dst, quality=92)
    return o.size, do_bytes(a[y:y + s, x:x + s])


def do_bytes(a):
    """Độ gãy tính trên vùng cắt nguyên độ phân giải (cùng thang với số toàn ảnh)."""
    ink = a < 115
    if ink.sum() < 2000:
        return 0.0, float(ink.mean() * 100)
    sm = ndi.binary_closing(ink, structure=np.ones((5, 5)))
    sm = ndi.binary_opening(sm, structure=np.ones((3, 3)))
    sm = ndi.gaussian_filter(sm.astype(np.float32), 2.0) > 0.5
    return chu_vi(ink) / max(chu_vi(sm), 100), float(ink.mean() * 100)


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
