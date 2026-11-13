#!/usr/bin/env python3
"""Kiểm chứng giao diện từ ảnh chụp trình duyệt (phương pháp INKFRAME, bước ⑤).

Vẽ BẢN ĐỒ MẬT ĐỘ MỰC: chia ảnh chụp thành lưới ô, đếm điểm tối mỗi ô.
Ô đậm = nét mực / chữ / viền; ô trống = vùng sáng.
Dùng để xác nhận viền khung hiện đúng vị trí và chữ nằm trong ruột khung.

Cách dùng:
    python3 verify_shot.py screenshot.png
    python3 verify_shot.py screenshot.png --cols 46 --rows 26 --threshold 125
    python3 verify_shot.py screenshot.png --region 700 0 1220 1080   # chỉ soi vùng app
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Thiếu Pillow. Cài: pip install Pillow")

SYMBOLS = [(0.06, "·"), (0.20, "░"), (0.45, "▒"), (1.01, "█")]


def symbol(ratio):
    for edge, ch in SYMBOLS:
        if ratio < edge:
            return ch
    return "█"


def analyze(path, cols, rows, threshold, region):
    im = Image.open(path).convert("L")
    if region:
        im = im.crop(tuple(region))
    w, h = im.size
    px = im.load()

    grid = [[0] * cols for _ in range(rows)]
    cell_px = (w / cols) * (h / rows)
    for y in range(h):
        gy = y * rows // h
        for x in range(w):
            if px[x, y] < threshold:
                grid[gy][x * cols // w] += 1

    print(f"Ảnh: {path}  ({w}×{h})  lưới {cols}×{rows}  ngưỡng={threshold}")
    print("Bản đồ mật độ mực (█ đậm → · trống):")
    for r in range(rows):
        line = "".join(symbol(grid[r][c] / cell_px) for c in range(cols))
        print("  " + line)

    dark = sum(sum(row) for row in grid)
    print(f"\nTổng điểm tối: {dark} / {w * h} ({dark / (w * h) * 100:.2f}%)")
    print("Đối chiếu: viền khung phải tạo đường liền ở rìa vùng app;")
    print("ruột khung phải TRỐNG (ô '·') ở giữa để chữ nằm gọn.")


def main():
    ap = argparse.ArgumentParser(description="Bản đồ mật độ mực từ ảnh chụp (INKFRAME)")
    ap.add_argument("path", help="ảnh chụp màn hình")
    ap.add_argument("--cols", type=int, default=46)
    ap.add_argument("--rows", type=int, default=26)
    ap.add_argument("--threshold", type=int, default=125, help="ngưỡng điểm tối (mặc định 125)")
    ap.add_argument("--region", type=int, nargs=4, metavar=("X0", "Y0", "X1", "Y1"),
                    help="chỉ soi vùng này (mặc định cả ảnh)")
    args = ap.parse_args()
    analyze(args.path, args.cols, args.rows, args.threshold, args.region)


if __name__ == "__main__":
    main()
