"""Nhận file tiếng hoặc video từ Issue GitHub (không cần token) hoặc từ
xuong-am-inbox/. Video thì chỉ lấy luồng tiếng, bỏ phần hình (-vn).

Dùng khi người dùng chỉ có điện thoại: kéo file tiếng vào ô nội dung Issue, GitHub
biến nó thành URL `user-attachments`, workflow tải về rồi chuyển qua đây.

Cách nhận ra file thuộc nhóm nào, theo thứ tự ưu tiên:
  1. Tên file có chứa mã nhóm ("cho.mp3", "tieng-cho-v2.wav").
  2. Dòng ngay trên link có đúng mã nhóm ("cho", "mã: cho", "**cho**").
  3. Có đúng một file và đúng một mã được nhắc trong bài → gán cho mã đó.

Chạy:
  python3 tools/xu_ly_am.py --urls-file /tmp/issue.md --report /tmp/bao-cao-am.json
  python3 tools/xu_ly_am.py --inbox xuong-am-inbox --report /tmp/bao-cao-am.json
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC, "game"))
from du_lieu_am import CANH, THEO_MA  # noqa: E402

MA = [c["ma"] for c in CANH]
DICH = [os.path.join(GOC, "docs", "assets", "am"), os.path.join(GOC, "assets", "am")]
DUOI_AM = ("mp3", "wav", "m4a", "aac", "ogg", "opus", "flac", "aiff", "aif",
           "mp4", "mov", "m4v", "webm", "mkv", "avi", "3gp", "mpg", "mpeg", "wmv")
TIMEOUT = 120


def tai_ve(url: str, ra: str) -> None:
    """Tải file. URL user-attachments đã ký sẵn, gửi kèm Authorization sẽ bị 400."""
    headers = {"User-Agent": "xuong-am"}
    tok = os.environ.get("GITHUB_TOKEN") or ""
    if tok and "user-attachments" not in url and "githubusercontent" not in url:
        headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r, open(ra, "wb") as f:
        f.write(r.read())


def tach_url(text: str) -> list:
    """URL file âm thanh trong nội dung Issue: markdown, HTML, link trần."""
    urls = []
    urls += re.findall(r"\[[^\]]*\]\((https?://[^\s)]+)\)", text)
    urls += re.findall(r'<a[^>]+href="(https?://[^"]+)"', text)
    for u in re.findall(r"(https?://[^\s)\"'>]+)", text):
        if "user-attachments" in u or "githubusercontent" in u:
            urls.append(u)
        elif re.search(r"\.(" + "|".join(DUOI_AM) + r")(\?|$)", u, re.I):
            urls.append(u)
    thay, ra = set(), []
    for u in urls:
        if u not in thay:
            thay.add(u)
            ra.append(u)
    return ra


# Mã cảnh dài trước: "cho_01" phải khớp trước "cho", nếu không file
# "cho_01.mp3" sẽ bị nhận thành nhóm cũ "cho".
MA_DAI_TRUOC = sorted(MA, key=len, reverse=True)


def ma_tu_ten(ten: str):
    t = os.path.basename(ten).lower()
    t = re.sub(r"\.[a-z0-9]+$", "", t)
    for m in MA_DAI_TRUOC:
        if re.search(r"(^|[^a-z])" + re.escape(m) + r"([^a-z]|$)", t):
            return m
    return None


def ma_tu_dong_truoc(text: str, url: str):
    """Dòng ngay trên link (bỏ dòng trống), nếu dòng đó chỉ là một mã nhóm.

    Chỉ xét đúng một dòng: quét ngược nhiều dòng sẽ gán nhầm mã của link trước
    cho link sau khi người dùng dán nhiều file liền nhau.
    """
    ds = text.splitlines()
    for i, dong in enumerate(ds):
        if url not in dong:
            continue
        j = i - 1
        while j >= 0 and not ds[j].strip():
            j -= 1
        if j < 0:
            return None
        s = ds[j].strip().strip("*_`#> -")
        s = re.sub(r"^(mã|ma|code)\s*[:：]\s*", "", s, flags=re.I).strip()
        return s.lower() if s.lower() in THEO_MA else None
    return None


# Chỉ lấy 12 giây đầu. Cảnh trong game chỉ 10 giây, nên 12 giây là dư một chút
# để vòng lặp không chạm mép file. File nhỏ thì tải nhanh trên điện thoại.
GIAY_LAY = 12

MUC_LUFS = -18  # tiếng nền phát qua loa điện thoại; -23 (chuẩn phát thanh) nghe quá nhỏ
DINH_TP = -2


def do_am_thanh(src: str):
    """Đo loudness thật của file. Trả về (integrated LUFS, true peak dBTP)."""
    kq = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-vn", "-t", str(GIAY_LAY), "-i", src,
         "-af", f"loudnorm=I={MUC_LUFS}:TP={DINH_TP}:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True)
    chu = kq.stderr
    dau, cuoi = chu.rfind("{"), chu.rfind("}")
    if dau < 0 or cuoi < 0:
        raise RuntimeError("loudnorm không trả JSON: " + chu[-400:])
    j = json.loads(chu[dau:cuoi + 1])
    return float(j["input_i"]), float(j["input_tp"]), j


# Mã hoá MP3 tạo đỉnh vượt giữa mẫu: PCM đã hạn chế đúng −2 dBTP mà file mp3
# đo lại vẫn lên −1,1 dBTP (đã gặp thật ở "san"). Vì vậy hạn chế đỉnh xuống
# thấp hơn mục tiêu một chút, rồi đo lại file đã mã hoá và hạ thêm nếu vẫn vượt.
DINH_MARGIN = 0.5     # dB dự phòng cho đỉnh vượt do mã hoá


def _ma_hoa(src: str, ra: str, loc: str, them: str = "") -> None:
    if them:
        loc = loc + "," + them
    subprocess.run(
        # -vn: bỏ luồng hình. File vào có thể là video; không có cờ này thì
        # ffmpeg cố mang cả hình sang mp3 và báo lỗi.
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-vn",
         "-t", str(GIAY_LAY), "-i", src,
         "-af", loc, "-ac", "2", "-ar", "44100",
         "-c:a", "libmp3lame", "-b:a", "96k", ra],
        check=True)


def chuyen(src: str, ma: str) -> str:
    """Chuẩn hoá về mp3 96 kbps, cân âm lượng, đỉnh dưới −2 dB.

    loudnorm một lượt đo sai trên file ngắn (đã đo thật: đặt −23 LUFS nhưng ra
    −24.3 dBTP, tức là nhỏ hơn cả mục tiêu). Phải đo trước rồi áp số đo được.

    Sau khi mã hoá phải đo lại: loudnorm chỉ hạn chế đỉnh trên PCM, còn MP3 tạo
    thêm đỉnh vượt giữa mẫu. Vượt thì hạ thêm đúng phần dư rồi mã hoá lại.
    """
    ra = os.path.join(DICH[0], f"{ma}.mp3")
    os.makedirs(DICH[0], exist_ok=True)
    _, _, j = do_am_thanh(src)
    dinh = DINH_TP - DINH_MARGIN
    loc = (
        f"loudnorm=I={MUC_LUFS}:TP={dinh}:LRA=11"
        f":measured_I={j['input_i']}:measured_TP={j['input_tp']}"
        f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}"
        f":offset={j['target_offset']}:linear=true"
    )
    _ma_hoa(src, ra, loc)
    # Đo lại file đã mã hoá. Còn vượt thì hạ đúng phần dư; lặp tối đa 2 lần để
    # không rơi vào vòng lặp vô hạn nếu file có đỉnh kỳ dị.
    for _ in range(2):
        _, tp, _ = do_am_thanh(ra)
        du = DINH_TP - tp
        if du >= 0:
            break
        _ma_hoa(src, ra, loc, f"volume={du:.2f}dB")
    for d in DICH[1:]:
        os.makedirs(d, exist_ok=True)
        with open(ra, "rb") as f, open(os.path.join(d, f"{ma}.mp3"), "wb") as g:
            g.write(f.read())
    return ra


def xu_ly(text: str, nguon: str, bao_cao: dict) -> None:
    urls = tach_url(text)
    if not urls:
        bao_cao["loi"].append("Không thấy link file âm thanh nào trong bài.")
        return
    nhac = [m for m in MA if re.search(r"(^|[^a-z])" + m + r"([^a-z]|$)", text.lower())]
    for i, u in enumerate(urls, 1):
        ma = ma_tu_ten(u) or ma_tu_dong_truoc(text, u)
        if not ma and len(urls) == 1 and len(nhac) == 1:
            ma = nhac[0]
        if not ma:
            bao_cao["chua_ro"].append({"url": u, "ly_do": "không đoán được cảnh"})
            continue
        tam = f"/tmp/am-{i}"
        try:
            tai_ve(u, tam)
        except Exception as e:  # noqa: BLE001
            bao_cao["loi"].append(f"tải {u} lỗi: {e}")
            continue
        try:
            ra = chuyen(tam, ma)
        except subprocess.CalledProcessError as e:
            bao_cao["loi"].append(f"chuyển {ma} lỗi: {e}")
            continue
        finally:
            try:
                os.remove(tam)
            except OSError:
                pass
        bao_cao["da_luu"].append({"ma": ma, "file": os.path.basename(ra), "nguon": nguon})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls-file", default="")
    ap.add_argument("--inbox", default="")
    ap.add_argument("--report", default="")
    a = ap.parse_args()

    bao_cao = {"da_luu": [], "chua_ro": [], "loi": []}
    if a.urls_file and os.path.isfile(a.urls_file):
        with open(a.urls_file, encoding="utf-8") as f:
            xu_ly(f.read(), "issue", bao_cao)
    elif a.inbox and os.path.isdir(a.inbox):
        for thu_muc in sorted(os.listdir(a.inbox)):
            d = os.path.join(a.inbox, thu_muc)
            if not os.path.isdir(d) or thu_muc.startswith("."):
                continue
            for ten in sorted(os.listdir(d)):
                p = os.path.join(d, ten)
                if not os.path.isfile(p) or ten.startswith("."):
                    continue
                try:
                    ra = chuyen(p, thu_muc)
                except subprocess.CalledProcessError as e:
                    bao_cao["loi"].append(f"{p}: {e}")
                    continue
                bao_cao["da_luu"].append(
                    {"ma": thu_muc, "file": os.path.basename(ra), "nguon": "inbox"})
                os.remove(p)

    chu = json.dumps(bao_cao, ensure_ascii=False, indent=2)
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            f.write(chu)
    print(chu)
    return 0 if not bao_cao["loi"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
