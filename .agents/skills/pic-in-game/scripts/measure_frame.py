#!/usr/bin/env python3
"""Đo khung ảnh vẽ tay để sinh CSS border-image (phương pháp INKFRAME, bước ③ ĐO).

Với mỗi cạnh, quét từ mép vào theo hàng/cột giữa ảnh, tìm dải điểm tối (nét mực),
rồi đề xuất giá trị slice cho border-image = mép trong + biên an toàn.

Cách dùng:
    python3 measure_frame.py assets/ui/panel-character.jpg
    python3 measure_frame.py assets/ui/btn-choice.jpg --threshold 160 --safety 10

Đầu ra: độ dày viền 4 cạnh, độ sáng ruột khung (để chọn màu chữ), và dòng CSS sẵn dùng.
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Thiếu Pillow. Cài: pip install Pillow")


def scan_band(values, threshold):
    """Trả về (đầu, cuối) của dải điểm tối đầu tiên trong dãy, hoặc None."""
    start = None
    end = None
    for i, v in enumerate(values):
        if v < threshold:
            if start is None:
                start = i
            end = i
        elif start is not None:
            return (start, end)
    if start is not None:
        return (start, end)
    return None


def measure(path, threshold=150, safety=8):
    im = Image.open(path).convert("L")
    w, h = im.size
    px = im.load()
    midy, midx = h // 2, w // 2

    row = [px[x, midy] for x in range(w)]
    col = [px[midx, y] for y in range(h)]

    left = scan_band(row, threshold)
    right = scan_band(row[::-1], threshold)
    top = scan_band(col, threshold)
    bottom = scan_band(col[::-1], threshold)

    li = left[1] + 1 if left else None
    ri = right[1] + 1 if right else None
    ti = top[1] + 1 if top else None
    bi = bottom[1] + 1 if bottom else None

    def slice_of(inner_edge, fallback=12):
        return max(inner_edge + safety, fallback) if inner_edge else fallback

    slice_top = slice_of(ti)
    slice_right = slice_of(ri)
    slice_bottom = slice_of(bi)
    slice_left = slice_of(li)

    inset_x = max(slice_left, slice_right, 20)
    inset_y = max(slice_top, slice_bottom, 20)
    inner_img = im.crop((inset_x, inset_y, w - inset_x, h - inset_y))
    hist = inner_img.histogram()
    total = sum(hist)
    avg = sum(i * c for i, c in enumerate(hist)) / total if total else 0

    def show(label, value, outer, size):
        if value is None:
            print(f"  {label}: không thấy")
        else:
            print(f"  {label}: {outer:>5} px  ({outer / size * 100:.1f}%)")

    print(f"\nẢnh: {path}  ({w}×{h})  ngưỡng={threshold}")
    show("viền trái ", li, li or 0, w)
    show("viền phải ", ri, (w - ri) if ri else 0, w)
    show("viền trên ", ti, ti or 0, h)
    show("viền dưới ", bi, (h - bi) if bi else 0, h)

    print(f"  ruột khung: độ sáng trung bình L={avg:.0f}  →", end=" ")
    if avg >= 180:
        print("SÁNG → dùng chữ mực đậm (ví dụ #1b1915)")
    elif avg >= 120:
        print("TRUNG BÌNH → dùng chữ đậm, kiểm tra tương phản")
    else:
        print("TỐI → dùng chữ sáng")

    print("\n  CSS border-image (slice: trên phải dưới trái):")
    print(f'    border-image:url("../{path}") '
          f"{slice_top} {slice_right} {slice_bottom} {slice_left} fill / 9px 9px / 0 stretch;")


def main():
    ap = argparse.ArgumentParser(description="Đo khung ảnh để sinh CSS border-image (INKFRAME)")
    ap.add_argument("path", help="đường dẫn ảnh khung")
    ap.add_argument("--threshold", type=int, default=150, help="ngưỡng điểm tối (mặc định 150)")
    ap.add_argument("--safety", type=int, default=8, help="biên an toàn cộng vào slice (mặc định 8)")
    args = ap.parse_args()
    measure(args.path, args.threshold, args.safety)


if __name__ == "__main__":
    main()
