"""Dựng video xem trước trailer từ 14 ảnh: Ken Burns + chữ tiếng Việt trên hình.

Chỉ để duyệt bố cục và nhịp — bản cuối dựng trong CapCut sẽ nét hơn và có nhạc.

    python3 tools/dung_video_xem_truoc.py

Ghi ra docs/xuong-video/xem-truoc.mp4 (720x1280, 24 fps, không nhạc).
"""

from __future__ import annotations

import io
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

import xuong_video as V

W, H, FPS = 720, 1280, 24
ROOT = V.ROOT
RA = os.path.join(ROOT, "docs", "xuong-video")
DICH = os.path.join(RA, "xem-truoc.mp4")
TAM = os.path.join(RA, ".tam")

FONT_DAM = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_THUONG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def _camera(c: dict) -> tuple[str, str, str]:
    """Biểu thức zoompan (z, x, y) cho từng kiểu chuyển động trong CANH_VIDEO."""
    cam, n = c["chuyen_dong"], int(c["giay"] * FPS)
    if "Zoom out" in cam:
        z = f"1.10-0.10*on/{n}"
    elif "Zoom in nhanh" in cam:
        z = f"1.00+0.18*on/{n}"
    elif "Zoom in" in cam:
        z = f"1.00+0.12*on/{n}"
    else:
        z = "1.04"
    if "phải" in cam:
        x, y = f"(iw-iw/zoom)*on/{n}", "(ih-ih/zoom)/2"
    elif "trái" in cam:
        x, y = f"(iw-iw/zoom)*(1-on/{n})", "(ih-ih/zoom)/2"
    elif "lên" in cam:
        x, y = "(iw-iw/zoom)/2", f"(ih-ih/zoom)*(1-on/{n})"
    else:
        x, y = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    return z, x, y


def _ngat_dong(draw, chu: str, font, rong: int) -> list[str]:
    """Ngắt câu thành dòng vừa bề rộng cho trước."""
    dong, hien = [], ""
    for tu in chu.split():
        thu = (hien + " " + tu).strip()
        if draw.textlength(thu, font=font) <= rong or not hien:
            hien = thu
        else:
            dong.append(hien)
            hien = tu
    if hien:
        dong.append(hien)
    return dong


def _anh_chu(chu: str) -> str | None:
    """Vẽ chữ thành PNG nền trong suốt, có bóng đổ. Trả về đường dẫn hoặc None."""
    if not chu:
        return None
    la_tieu_de = "/" in chu
    if la_tieu_de:
        dong = [d.strip() for d in chu.split("/")]
        font = ImageFont.truetype(FONT_DAM, 62)
    else:
        font = ImageFont.truetype(FONT_DAM, 44)

    lop = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lop)
    rong = int(W * 0.84)

    if la_tieu_de:
        khoi = [(dong[0], font), (dong[1], ImageFont.truetype(FONT_THUONG, 34))]
        cao = sum(f.size + 18 for _, f in khoi)
        y = (H - cao) // 2
        for text, f in khoi:
            while d.textlength(text, font=f) > rong and f.size > 20:
                f = ImageFont.truetype(f.path, f.size - 2)
            x = (W - d.textlength(text, font=f)) / 2
            for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
                d.text((x + dx, y + dy), text, font=f, fill=(0, 0, 0, 190))
            d.text((x, y), text, font=f, fill=(246, 238, 214, 255))
            y += f.size + 18
    else:
        ds_dong = _ngat_dong(d, chu, font, rong)
        cao = len(ds_dong) * (font.size + 12)
        y = H - int(H * 0.19) - cao
        for text in ds_dong:
            x = (W - d.textlength(text, font=font)) / 2
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (3, 3)):
                d.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 200))
            d.text((x, y), text, font=font, fill=(246, 238, 214, 255))
            y += font.size + 12

    ra = os.path.join(TAM, f"chu_{abs(hash(chu))}.png")
    lop.save(ra)
    return ra


def _doan(c: dict, i: int) -> str:
    """Dựng một đoạn: ảnh + camera + chữ. Trả về đường dẫn mp4."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    n = int(c["giay"] * FPS)
    z, x, y = _camera(c)
    ra = os.path.join(TAM, f"s{i:02d}.mp4")
    vf = (f"scale={W * 2}:{H * 2},"
          f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p")

    chu = _anh_chu(c.get("chu", ""))
    lenh = [ff, "-y", "-loop", "1", "-i", os.path.join(V.VIDEO_DIR, c["file"])]
    if chu:
        lenh += ["-loop", "1", "-i", chu, "-filter_complex",
                 f"[0:v]{vf}[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
                 "-map", "[v]"]
    else:
        lenh += ["-vf", vf]
    lenh += ["-t", str(c["giay"]), "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "26", ra]
    r = subprocess.run(lenh, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"{c['key']}: {r.stderr.decode()[-400:]}")
    return ra


def dung(ghi: bool = True) -> str:
    os.makedirs(TAM, exist_ok=True)
    doan = []
    for i, c in enumerate(V.CANH_VIDEO):
        thieu = not os.path.isfile(os.path.join(V.VIDEO_DIR, c["file"]))
        print(f"  {c['key']} {c['giay']:>2}s{' (thiếu ảnh!)' if thieu else ''}")
        if thieu:
            raise FileNotFoundError(f"Thiếu ảnh {c['file']} — không dựng được")
        doan.append(_doan(c, i))

    ds = os.path.join(TAM, "list.txt")
    with open(ds, "w") as f:
        for d in doan:
            f.write(f"file '{d}'\n")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    tam = os.path.join(TAM, "ghep.mp4")
    subprocess.run([ff, "-y", "-f", "concat", "-safe", "0", "-i", ds, "-c", "copy", tam],
                   check=True, capture_output=True)
    if ghi:
        subprocess.run([ff, "-y", "-i", tam, "-c:v", "libx264", "-preset", "slow",
                        "-crf", "30", "-maxrate", "1200k", "-bufsize", "2400k",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", DICH],
                       check=True, capture_output=True)
        for f in os.listdir(TAM):
            os.remove(os.path.join(TAM, f))
        os.rmdir(TAM)
        return DICH
    return tam


if __name__ == "__main__":
    print(f"Dựng {len(V.CANH_VIDEO)} cảnh · {V.tong_giay()}s · {W}x{H}@{FPS}")
    ra = dung()
    print("Xong:", ra, round(os.path.getsize(ra) / 1024 / 1024, 2), "MB")
