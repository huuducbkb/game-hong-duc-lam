#!/usr/bin/env python3
"""Tách nền alpha + tối ưu ảnh cho web (phương pháp INKFRAME, bước ④ GHÉP).

Hai chế độ:

  1. alpha — biến ảnh "giấy sáng + mực đậm" thành PNG trong suốt (giấy → alpha thấp,
     mực → alpha cao). Dùng cho tài nguyên ĐÈ lên nền: viền avatar, ấn son, hoạ tiết.

  2. jpeg — thu nhỏ rồi lưu JPEG. Dùng cho KHUNG / NỀN / NÚT (không cần trong suốt).

Cách dùng:
    python3 prep_assets.py alpha assets/ui-orig/avatar-ring.png assets/ui/avatar-ring.png --width 512
    python3 prep_assets.py jpeg  assets/ui-orig/bg-main.png     assets/ui/bg-main.jpg     --width 820 --quality 80

Ghi chú: luôn giữ bản gốc ở thư mục riêng (ví dụ assets/ui-orig/), chỉ tối ưu bản dùng cho web.
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Thiếu Pillow. Cài: pip install Pillow")


def resize(im, width):
    if not width or width >= im.width:
        return im
    nh = round(im.height * width / im.width)
    return im.resize((width, nh), Image.LANCZOS)


def do_alpha(src, dst, width, gamma, thresh):
    im = resize(Image.open(src).convert("RGB"), width)
    w, h = im.size
    px = im.load()
    out = Image.new("RGBA", (w, h))
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            d = max(0, 255 - lum - thresh)
            a = int(min(255, (d / 255.0) ** (1.0 / gamma) * 255))
            op[x, y] = (r, g, b, a)
    out.save(dst)
    print(f"alpha: {src} -> {dst}  {out.size}  {os.path.getsize(dst) // 1024} KB")


def do_jpeg(src, dst, width, quality):
    im = resize(Image.open(src).convert("RGB"), width)
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"jpeg : {src} -> {dst}  {im.size}  {os.path.getsize(dst) // 1024} KB")


def main():
    ap = argparse.ArgumentParser(description="Tách nền alpha / tối ưu ảnh cho web (INKFRAME)")
    ap.add_argument("mode", choices=["alpha", "jpeg"], help="alpha = tách nền trong suốt; jpeg = nén")
    ap.add_argument("src", help="ảnh nguồn")
    ap.add_argument("dst", help="ảnh đích")
    ap.add_argument("--width", type=int, default=0, help="chiều rộng đích (0 = giữ nguyên)")
    ap.add_argument("--quality", type=int, default=82, help="chất lượng JPEG (mặc định 82)")
    ap.add_argument("--gamma", type=float, default=2.0, help="gamma cho alpha (mặc định 2.0)")
    ap.add_argument("--thresh", type=int, default=8, help="ngưỡng bỏ qua giấy sáng (mặc định 8)")
    args = ap.parse_args()

    if args.mode == "alpha":
        do_alpha(args.src, args.dst, args.width, args.gamma, args.thresh)
    else:
        do_jpeg(args.src, args.dst, args.width, args.quality)


if __name__ == "__main__":
    main()
