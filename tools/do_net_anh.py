#!/usr/bin/env python3
"""Đo chất lượng mực của ảnh line-art: mực có đặc không, có bị loang lỗ không.

Hướng vẽ hiện tại là line-art: nét đen sắc, một nét liền, tô mực đặc bên trong nét.
Hai kiểu hỏng thật gặp phải, và cách đo chúng:

  LOANG (mực loang lỗ) — tỉ lệ điểm nằm BÊN TRONG thân mực mà vẫn còn sáng. Mực tô
       đặc cho 0.00; mực loang lỗ cho 0.15–0.46. Đây là bệnh chính: nhìn như tranh
       trừu tượng vì mảng mực không kín, vá víu sáng tối.

  DOT (đốm sáng) — tỉ lệ điểm sáng nằm trong các LỖ NHỎ khoét giữa thân mực. Khác
       với lỗ lớn: lỗ lớn chính là mảng giấy trắng nằm trong nét bao, hoàn toàn hợp lệ
       với line-art (kỹ thuật liubai / 留白). Chỉ lỗ nhỏ li ti mới là lỗi.

  NET (nét gãy) — độ nhất quán hướng nét dọc đường biên. Nét kéo một hơi thì hướng
       đi đều; nét chắp vụn thì hướng đảo liên tục. Chỉ dùng để soi ảnh bất thường,
       không có ngưỡng tuyệt đối, vì ảnh nhiều chi tiết thật (tóc, vân vải) cũng
       làm số tụt.

Ngưỡng lấy từ ảnh tổng hợp ở `--tu-kiem`, không phải số đoán.

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

NGUONG_LOANG = 0.15      # trên mức này là mực loang lỗ
NGUONG_LOANG_TOT = 0.08
NGUONG_DOT = 0.03        # trên mức này là có đốm sáng li ti
NGUONG_NET_CANH_BAO = 0.45


def _muc(a):
    """Mặt nạ mực + hai mốc sáng tối của chính ảnh (nền giấy sáng không đều)."""
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    if hi - lo < 12:
        return None, lo, hi
    return a < (lo + 0.45 * (hi - lo)), lo, hi


def do_loang(a):
    """Tỉ lệ điểm còn sáng nằm trong thân mực (đã lấp các lỗ)."""
    m, lo, hi = _muc(a)
    if m is None or m.sum() < 2000:
        return None
    than = ndi.binary_fill_holes(m)
    if than.sum() == 0:
        return None
    return float((a[than] > lo + 0.35 * (hi - lo)).sum() / than.sum())


def do_dot(a):
    """Tỉ lệ điểm sáng nằm trong các lỗ NHỎ khoét giữa thân mực."""
    m, _, _ = _muc(a)
    if m is None or m.sum() < 2000:
        return None
    lo_hong = ndi.binary_fill_holes(m) & ~m
    if not lo_hong.any():
        return 0.0
    nhan, so = ndi.label(lo_hong)
    if so == 0:
        return 0.0
    dt = np.asarray(ndi.sum(lo_hong, nhan, range(1, so + 1)))
    # Lỗ nhỏ = dưới 0.2% lượng mực. Mảng giấy trắng giữa nét bao lớn hơn nhiều.
    return float(dt[dt < max(40.0, m.sum() * 0.002)].sum() / m.sum())


def do_net(a):
    """Độ nhất quán hướng nét dọc đường biên của các mảng mực lớn."""
    m, _, _ = _muc(a)
    if m is None:
        return None
    nhan, so = ndi.label(m)
    if so == 0:
        return None
    dt = np.asarray(ndi.sum(m, nhan, range(1, so + 1)))
    lon = np.isin(nhan, [i + 1 for i in range(so) if dt[i] >= 3000])
    if lon.sum() < 3000:
        return None
    g = ndi.gaussian_filter(a.astype(np.float32), 1.5)
    gx, gy = ndi.sobel(g, 1), ndi.sobel(g, 0)
    jxx, jyy = ndi.uniform_filter(gx * gx, 9), ndi.uniform_filter(gy * gy, 9)
    jxy = ndi.uniform_filter(gx * gy, 9)
    nhat_quan = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / np.maximum(jxx + jyy, 1e-6)
    bien = lon & ~ndi.binary_erosion(lon, iterations=1)
    if bien.sum() < 200:
        return None
    return float(np.median(nhat_quan[bien]))


def do(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    loang, dot, net = do_loang(a), do_dot(a), do_net(a)
    if loang is None or dot is None:
        return None
    return loang, dot, net


def danh_gia(loang, dot, net):
    # Xét loang trước: mực loang lỗ tự sinh ra nhiều lỗ nhỏ, nên nếu xét đốm trước
    # thì ảnh loang bị gọi nhầm là "có đốm sáng". Đốm chỉ là lỗi riêng khi thân mực
    # vốn đặc.
    if loang > NGUONG_LOANG:
        return "mực loang lỗ"
    if dot > NGUONG_DOT:
        return "có đốm sáng"
    if loang > NGUONG_LOANG_TOT:
        return "đạt"
    return "mực đặc"


def _anh_tong_hop():
    """Ảnh dựng tay, biết trước đáp án, để kiểm thước."""
    h = w = 600
    yy, xx = np.mgrid[0:h, 0:w]
    tam = [(180, 200, 110), (380, 380, 140), (200, 450, 80)]
    rng = np.random.default_rng(11)

    def ve(do_loang):
        a = np.full((h, w), 235.0, np.float32)
        m = np.zeros((h, w), bool)
        for cy, cx, r in tam:
            m |= np.hypot(yy - cy, xx - cx) < r
        a[m] = 60.0
        if do_loang:
            n = ndi.gaussian_filter(rng.normal(0, 1, (h, w)).astype(np.float32), 2.0)
            n /= max(np.abs(n).max(), 1e-6)
            a[m] = 60.0 + n[m] * do_loang * 300.0
        return a

    # Đốm: mực đặc nhưng bị khoét nhiều lỗ nhỏ.
    dot = np.full((h, w), 235.0, np.float32)
    m = np.zeros((h, w), bool)
    for cy, cx, r in tam:
        m |= np.hypot(yy - cy, xx - cx) < r
    dot[m] = 60.0
    for _ in range(700):
        cy, cx = rng.integers(60, h - 60), rng.integers(60, w - 60)
        dot[np.hypot(yy - cy, xx - cx) < rng.integers(2, 5)] = 235.0

    return [("mực đặc, sạch", ve(0.0), "mực đặc"),
            ("mực loang lỗ", ve(0.7), "mực loang lỗ"),
            ("có đốm sáng", dot, "có đốm sáng")]


def _tu_kiem():
    ok = True
    for ten, anh, mong in _anh_tong_hop():
        loang, dot, net = do_loang(anh), do_dot(anh), do_net(anh)
        if loang is None or dot is None:
            print(f"  {ten:18} -> không đo được")
            return False
        d = danh_gia(loang, dot, net)
        dung = d == mong
        print(f"  {ten:18} loang={loang:5.3f} đốm={dot:5.3f} "
              f"nét={(net if net is not None else float('nan')):5.3f} -> {d:14} "
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
            rows.append((os.path.basename(p), r[0], r[1], r[2]))

    if not rows:
        print("không có ảnh nào để đo trong", d)
        return 1

    rows.sort(key=lambda x: -x[1])
    print(f"{'ảnh':30}{'loang':>8}{'đốm':>8}{'nét':>7}  đánh giá")
    for n, loang, dot, net in rows:
        canh_bao = "" if net is None or net >= NGUONG_NET_CANH_BAO else "  ⚠ nét gãy"
        print(f"{n:30}{loang:8.3f}{dot:8.3f}"
              f"{(net if net is not None else float('nan')):7.3f}  "
              f"{danh_gia(loang, dot, net)}{canh_bao}")

    dat = sum(1 for r in rows if danh_gia(r[1], r[2], r[3]) in ("đạt", "mực đặc"))
    loangs = [r[1] for r in rows]
    print(f"\n{len(rows)} ảnh · {dat} đạt · {len(rows) - dat} chưa đạt")
    print(f"Loang: trung vị {np.median(loangs):.3f}, thấp nhất {min(loangs):.3f} "
          f"(ngưỡng {NGUONG_LOANG}).")
    print(f"Đốm: ngưỡng {NGUONG_DOT}. Nét: cảnh báo dưới {NGUONG_NET_CANH_BAO}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
