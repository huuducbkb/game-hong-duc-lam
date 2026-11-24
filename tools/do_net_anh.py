#!/usr/bin/env python3
"""Đo chất lượng nét của ảnh mực: mép có mềm không, và mực có bị vụn không.

Hai đại lượng, chọn theo đúng thứ người dùng nhìn thấy:

  MEM  (độ mềm mép) — độ rộng vùng chuyển tiếp sáng→tối ở mép hình, tính bằng
       điểm ảnh. Đo bằng tương phản cục bộ chia cho độ lớn gradient. Mép vẽ bằng
       một nét viền cứng chuyển sáng-tối trong 1-2 điểm ảnh (MEM ≈ 0.5); mép hội
       họa chuyển dần qua 4-8 điểm ảnh (MEM ≈ 1.2+). Đây là đại lượng chính, vì
       hướng sửa mới là "soft blended edges".

  VUN  (độ vụn) — tỉ lệ mực nằm trong các mảng nhỏ rời rạc. Bắt lỗi "nét chắp
       vụn", "chấm li ti". Không phụ thuộc kiểu vẽ nên dùng được cho cả ảnh cũ
       lẫn ảnh mới.

    MEM >= 1.00 và VUN <= 0.15 → đạt
    MEM >= 1.15 và VUN <= 0.10 → mềm rõ (mức nên hướng tới)

Ngưỡng lấy từ ảnh tổng hợp dựng tay ở `--tu-kiem`, không phải số đoán.

Chạy: python3 tools/do_net_anh.py [thư mục]
Kiểm chính thước: python3 tools/do_net_anh.py --tu-kiem
"""
import glob
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAC_DINH = os.path.join(GOC, "docs", "assets", "scene")

NGUONG_MEM = 1.00
NGUONG_MEM_TOT = 1.15
NGUONG_VUN = 0.15
NGUONG_VUN_TOT = 0.10


def _nen(a):
    """Ngưỡng mực theo tương phản của chính ảnh (nền giấy sáng không đều)."""
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    if hi - lo < 12:
        return None, None, None
    return lo, hi, a < (lo + 0.45 * (hi - lo))


def do_mem(a):
    """Độ rộng chuyển tiếp ở mép, đơn vị điểm ảnh."""
    _, _, ink = _nen(a)
    if ink is None or ink.sum() < 2000:
        return None
    g = ndi.gaussian_filter(a.astype(np.float32), 1.0)
    mag = np.hypot(ndi.sobel(g, 0), ndi.sobel(g, 1))
    sel = mag > np.percentile(mag, 97)
    if sel.sum() < 100:
        return None
    # Tương phản trong cửa sổ 9x9 quanh mỗi điểm biên: mép càng mềm thì gradient
    # càng nhỏ so với tương phản, nên thương số càng lớn.
    tuong_phan = (ndi.maximum_filter(g, 9) - ndi.minimum_filter(g, 9))[sel]
    return float(np.median(tuong_phan / np.maximum(mag[sel], 1e-6)))


def do_vun(a):
    """Tỉ lệ mực nằm trong các mảng nhỏ rời rạc."""
    _, _, ink = _nen(a)
    if ink is None or ink.sum() < 2000:
        return None
    nhan, so = ndi.label(ink)
    if so == 0:
        return None
    dt = np.asarray(ndi.sum(ink, nhan, range(1, so + 1)))
    tong = float(dt.sum())
    # Mảng "nhỏ" = dưới 0.5% tổng mực. Cánh tay hay vạt áo lớn hơn nhiều; chỉ
    # chấm li ti và vệt chắp vụn mới rơi vào nhóm này.
    return float(dt[dt < max(25.0, tong / 200.0)].sum() / tong) if tong else 0.0


def do(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    mem, vun = do_mem(a), do_vun(a)
    if mem is None or vun is None:
        return None
    return mem, vun, float((a < np.percentile(a, 40)).mean() * 100)


def danh_gia(mem, vun):
    # Xét vụn trước: ảnh vụn vặt cũng có gradient nhỏ ở mép, dễ bị chấm nhầm là
    # "mép cứng" trong khi bệnh chính là mực rời rạc.
    if vun > NGUONG_VUN:
        return "còn vụn"
    if mem >= NGUONG_MEM_TOT:
        return "mềm rõ"
    if mem >= NGUONG_MEM:
        return "đạt"
    return "mép cứng"


def _anh_tong_hop():
    """Ba ảnh dựng tay, biết trước đáp án, để kiểm thước."""
    rng = np.random.default_rng(7)
    h = w = 600
    yy, xx = np.mgrid[0:h, 0:w]
    tam = [(180, 200, 110), (380, 380, 140), (200, 450, 80)]

    def mep(sigma):
        a = np.full((h, w), 235.0, np.float32)
        for cy, cx, r in tam:
            d = np.hypot(yy - cy, xx - cx)
            a -= 150 / (1 + np.exp(np.clip((d - r) / sigma, -60, 60)))
        return a

    # Vụn: cùng bố cục nhưng vỡ thành hàng trăm chấm nhỏ, mép vẫn mềm.
    vun = np.full((h, w), 235.0, np.float32)
    for _ in range(900):
        cy, cx = rng.integers(40, h - 40), rng.integers(40, w - 40)
        d = np.hypot(yy - cy, xx - cx)
        vun -= rng.uniform(80, 170) / (1 + np.exp(np.clip((d - rng.integers(3, 9)) / 1.2, -60, 60)))
    return [("mép mềm rõ", mep(4.0), "mềm rõ"),
            ("mép cứng (nét viền)", mep(0.35), "mép cứng"),
            ("vụn (chấm li ti)", vun, "còn vụn")]


def _tu_kiem():
    ok = True
    for ten, anh, mong in _anh_tong_hop():
        mem, vun = do_mem(anh), do_vun(anh)
        if mem is None or vun is None:
            print(f"  {ten:22} -> không đo được")
            return False
        d = danh_gia(mem, vun)
        dung = d == mong
        print(f"  {ten:22} mem={mem:5.2f} vụn={vun:5.3f} -> {d:9} "
              f"(mong {mong}) {'ĐÚNG' if dung else 'SAI'}")
        ok = ok and dung
    return ok


def main() -> int:
    if "--tu-kiem" in sys.argv:
        print("Tự kiểm thước trên ảnh tổng hợp:")
        ok = _tu_kiem()
        print("\nThước phân biệt đúng." if ok else "\nTHƯỚC SAI — phải sửa trước khi dùng.")
        return 0 if ok else 1

    d = sys.argv[1] if len(sys.argv) > 1 else MAC_DINH
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "*.jpg"))):
        r = do(p)
        if r:
            rows.append((os.path.basename(p), r[0], r[1]))
    if not rows:
        print("không có ảnh nào để đo trong", d)
        return 1

    rows.sort(key=lambda x: x[1])
    print(f"{'ảnh':30}{'mép mềm':>9}{'vụn':>8}  đánh giá")
    for n, mem, vun in rows:
        print(f"{n:30}{mem:9.2f}{vun:8.3f}  {danh_gia(mem, vun)}")

    dat = sum(1 for r in rows if danh_gia(r[1], r[2]) in ("đạt", "mềm rõ"))
    print(f"\n{len(rows)} ảnh · {dat} đạt · {len(rows) - dat} chưa đạt")
    print(f"Ngưỡng: mép mềm >= {NGUONG_MEM} (nên >= {NGUONG_MEM_TOT}), "
          f"vụn <= {NGUONG_VUN} (nên <= {NGUONG_VUN_TOT}).")
    print("Ảnh vẽ trước khi đổi prompt vẫn mang nét viền cứng — phải vẽ lại.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
