"""Nén video intro về dung lượng nhẹ để phát trên điện thoại.

Người dùng xuất từ CapCut thường ra 40–90 MB (CapCut mặc định ~8–10 Mbps cho 1080p).
Video đó phát được nhưng bắt người chơi tải quá nặng, nên đưa về mục tiêu ~14 MB.

    python3 tools/nen_video.py <vao.mp4> <ra.mp4> [--muc-tieu-mb 14]

Nếu file đã nhẹ và đúng khung hình thì chép nguyên (không mã hoá lại, khỏi giảm chất).
"""

from __future__ import annotations


import os
import shutil
import subprocess
import sys

MAX_W, MAX_H = 1080, 1920
AM_THANH_KBPS = 96


def _ffmpeg() -> str:
    """Ưu tiên ffmpeg hệ thống (nhanh), thiếu thì dùng bản bundled của imageio."""
    he_thong = shutil.which("ffmpeg")
    if he_thong:
        return he_thong
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _thong_tin(ff: str, vao: str) -> dict:
    """Đọc thời lượng / khung hình từ output của ffmpeg.

    Bản ffmpeg bundled của imageio không kèm ffprobe, nên parse text thay vì JSON.
    """
    r = subprocess.run([ff, "-hide_banner", "-i", vao],
                       capture_output=True, text=True)
    tho = r.stderr
    if "Duration:" not in tho:
        raise RuntimeError(f"Không đọc được thông tin video: {vao}")

    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", tho)
    if not m:
        raise RuntimeError(f"Không đọc được thời lượng: {vao}")
    gio, phut, giay = int(m.group(1)), int(m.group(2)), float(m.group(3))
    tong_giay = gio * 3600 + phut * 60 + giay

    dong = [d for d in tho.split("\n") if "Video:" in d]
    if not dong:
        raise RuntimeError("File không có hình — có phải video không?")
    k = re.search(r"(\d{2,5})x(\d{2,5})", dong[0])
    if not k:
        raise RuntimeError(f"Không đọc được khung hình: {dong[0][:120]}")
    rong, cao = int(k.group(1)), int(k.group(2))
    co_tieng = any("Audio:" in d for d in tho.split("\n"))
    return {"giay": tong_giay, "rong": rong, "cao": cao, "co_tieng": co_tieng}


def nen(vao: str, ra: str, muc_tieu_mb: float = 14.0) -> tuple[str, str]:
    """Nén `vao` thành `ra`. Trả về (đường dẫn, ghi chú)."""
    ff = _ffmpeg()
    tt = _thong_tin(ff, vao)
    giay = tt["giay"]
    if giay <= 0:
        raise RuntimeError("Video không có thời lượng — file hỏng?")
    rong, cao, co_tieng = tt["rong"], tt["cao"], tt["co_tieng"]

    goc_mb = os.path.getsize(vao) / 1024 / 1024
    # Đã nhẹ và không quá khung thì giữ nguyên, không mã hoá lại.
    if goc_mb <= muc_tieu_mb and rong <= MAX_W and cao <= MAX_H:
        if os.path.abspath(vao) != os.path.abspath(ra):
            shutil.copyfile(vao, ra)
        return ra, f"giữ nguyên ({goc_mb:.1f} MB, {rong}×{cao}) — không cần nén"

    # Chia ngân sách bitrate cho hình sau khi trừ tiếng.
    tong_kbps = muc_tieu_mb * 8 * 1024 / giay
    hinh_kbps = max(400, int(tong_kbps - (AM_THANH_KBPS if co_tieng else 0)))

    # Bitrate thấp mà giữ 1080×1920 thì nhoè; dưới 1.2 Mbps hạ khung cho nét hơn.
    if hinh_kbps < 1200:
        MAX_W_LOCAL, MAX_H_LOCAL = 720, 1280
    else:
        MAX_W_LOCAL, MAX_H_LOCAL = MAX_W, MAX_H

    # -2 giữ chiều còn lại chia hết cho 2, không kéo méo hình.
    loc = (f"scale=w='min({MAX_W_LOCAL},iw)':h=-2:flags=lanczos,"
           f"scale=w=-2:h='min({MAX_H_LOCAL},ih)':flags=lanczos")

    thu_muc = os.path.dirname(os.path.abspath(ra))
    os.makedirs(thu_muc, exist_ok=True)
    nhat_ky = os.path.join(thu_muc, ".nen_pass.log")

    def chay(them: list[str], dich: str) -> None:
        lenh = [ff, "-y", "-i", vao, "-vf", loc,
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
                "-b:v", f"{hinh_kbps}k", "-maxrate", f"{int(hinh_kbps * 1.3)}k",
                "-bufsize", f"{int(hinh_kbps * 2)}k",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart"] + them
        if co_tieng:
            lenh += ["-c:a", "aac", "-b:a", f"{AM_THANH_KBPS}k", "-ac", "2"]
        else:
            lenh += ["-an"]
        lenh.append(dich)
        r = subprocess.run(lenh, capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"ffmpeg lỗi: {r.stderr.decode()[-500:]}")

    # Hai lượt cho dung lượng bám sát mục tiêu (một lượt thường lệch 10–25%).
    chay(["-pass", "1", "-passlogfile", nhat_ky, "-an", "-f", "null"], "/dev/null")
    chay(["-pass", "2", "-passlogfile", nhat_ky], ra)
    for f in os.listdir(thu_muc):
        if f.startswith(".nen_pass.log"):
            os.remove(os.path.join(thu_muc, f))

    ra_mb = os.path.getsize(ra) / 1024 / 1024
    return ra, (f"{goc_mb:.1f} MB → {ra_mb:.1f} MB "
                f"({rong}×{cao} → tối đa {MAX_W_LOCAL}×{MAX_H_LOCAL}, "
                f"{hinh_kbps} kbps)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    vao, ra = sys.argv[1], sys.argv[2]
    muc = 14.0
    if "--muc-tieu-mb" in sys.argv:
        muc = float(sys.argv[sys.argv.index("--muc-tieu-mb") + 1])
    duong, ghi_chu = nen(vao, ra, muc)
    print(ghi_chu)
    print("Ghi ra:", duong)
