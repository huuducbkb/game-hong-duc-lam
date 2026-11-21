"""Sinh trang Xưởng âm thanh từ game/du_lieu_am.py.

Chạy: python3 game/tao_xuong_am.py
Ra:   docs/xuong-am/index.html

Trang sinh sẵn (không gọi API lúc dựng) để mở được cả khi chưa có mạng, và để
workflow chỉ cần chạy lại script này khi thêm nhóm tiếng mới.
"""
import html
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from du_lieu_am import NHOM, CHUNG

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "docs", "xuong-am", "index.html")
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xuong_am.js")

# Tên file trên đĩa: <ma>.mp3 trong docs/assets/am/
DUONG = "assets/am/"


def esc(s):
    return html.escape(str(s), quote=True)


def the_canh(n, i):
    ma = n["ma"]
    prompt = n["prompt"].strip() + "\n\n" + CHUNG
    return f"""
<article class="canh" id="c-{ma}" data-ma="{ma}" data-file="{n['file']}">
  <header>
    <span class="so">{i}</span>
    <b>{esc(n['ten'])}</b>
    <code>{ma}</code>
    <span class="badge thieu" data-badge>⬜ chưa có</span>
  </header>
  <div class="meta">
    <div><span class="k">lưu là</span> <code>{DUONG}{esc(n['file'])}</code></div>
    <div><span class="k">dùng ở</span> {esc(n['dung'])}</div>
  </div>
  <p class="mota">{esc(n['mota'])}</p>

  <label class="nhan">Prompt tạo tiếng — dán vào công cụ sinh âm thanh</label>
  <textarea readonly rows="9" id="p-{ma}">{esc(prompt)}</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('p-{ma}', this)">📋 Copy prompt</button>
    <button class="dl" onclick="taiTxt('p-{ma}', '{ma}.txt')">⬇️ .txt</button>
  </div>

  <label class="nhan">Nghe thử bản đang dùng trong game</label>
  <div class="nghe" data-nghe>
    <audio controls playsinline preload="none" data-audio hidden></audio>
    <span class="chua" data-chua>⬜ Chưa có tiếng cho cảnh này — game đang dùng tiếng tổng hợp.</span>
  </div>

  <div class="gui" data-gui data-file="{n['file']}" data-ma="{ma}">
    <label class="tha-am" tabindex="0">
      <input type="file" data-chon
             accept="audio/mpeg,audio/mp3,audio/wav,audio/x-wav,audio/mp4,audio/x-m4a,audio/ogg,audio/flac,audio/*">
      <span class="tha-am-icon">🎵</span>
      <span class="tha-am-chu">Chạm để chọn file tiếng<small>hoặc kéo file vào đây</small></span>
    </label>
    <div class="thanh" data-thanh hidden><div class="thanh-ruot" data-ruot></div></div>
    <div class="row">
      <button type="button" class="gui-kt" data-gui-kt disabled>📤 Gửi tiếng này</button>
      <button type="button" class="gui-kt phu" data-kiem>🔄 Kiểm tra</button>
    </div>
    <div class="gui-tt" data-tt hidden></div>
  </div>
</article>"""


def sinh():
    ds = "\n".join(the_canh(n, i + 1) for i, n in enumerate(NHOM))
    so = len(NHOM)

    js = io.open(JS, encoding="utf-8").read()
    js = (js.replace("__REPO__", "huuducbkb/game-hong-duc-lam")
            .replace("__DIR__", DUONG)
            .replace("__INBOX__", "xuong-am-inbox"))
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xưởng âm thanh — Hồng Đức Tu Tiên Lộ</title>
<style>
:root{{--bg:#111a2b;--card:#182337;--ink:#e8e6df;--muted:#93a0b8;--gold:#ffd98a;
  --jade:#6fe0c0;--line:#2b3b57;--seal:#a8352a;--warn:#ffb98a}}
*{{box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);
  color:var(--ink);margin:0 auto;padding:18px;max-width:760px;line-height:1.55;
  -webkit-text-size-adjust:100%}}
h1{{font-size:20px;color:var(--gold);margin:6px 0 2px}}
h2{{font-size:16px;color:var(--jade);margin:30px 0 6px;display:flex;flex-wrap:wrap;
  gap:8px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:7px}}
p,li,td,th{{font-size:13.5px;color:#cbd4e4}}
.muted{{color:var(--muted)}}
code{{background:#0a1220;padding:1px 6px;border-radius:4px;color:var(--jade);font-size:12px}}
a{{color:var(--jade)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}}
.mota{{font-size:12.5px;color:var(--muted);margin:4px 0 10px}}
.ok{{color:#7fe0a8}} .warn{{color:var(--warn)}}
.canh{{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:13px;margin:12px 0;border-left:3px solid var(--jade)}}
.canh.done{{border-left-color:#2f8f5a}}
.canh header{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:14px}}
.so{{font-size:11px;color:#3a2600;background:var(--gold);padding:2px 7px;
  border-radius:99px;font-weight:700}}
.badge{{font-size:11px;padding:2px 8px;border-radius:99px}}
.badge.chac{{background:#12351f;color:#7fe0a8}}
.badge.thieu{{background:#2a150d;color:var(--warn)}}
.meta{{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12px;color:var(--muted);margin:8px 0}}
.meta .k{{color:#7f8ca3}}
.nhan{{display:block;font-size:12px;color:var(--muted);margin:12px 0 5px;font-weight:600}}
textarea{{width:100%;font-size:12.5px;line-height:1.5;background:#0a1220;color:#dfe7f5;
  border:1px solid var(--line);border-radius:8px;padding:10px;resize:vertical;
  font-family:ui-monospace,Menlo,monospace}}
.row{{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}}
button{{font:inherit;font-size:12.5px;padding:7px 12px;border-radius:8px;cursor:pointer;
  background:#1d2c44;color:var(--ink);border:1px solid var(--line)}}
button:active{{transform:translateY(1px)}}
button:disabled{{opacity:.45;cursor:not-allowed}}
button.phu{{background:transparent}}
.cp{{background:#243a2c;border-color:#2f6b4f;color:#a9f0c4}}
.dl{{background:transparent}}
.nghe{{margin:4px 0 0}}
.nghe audio{{width:100%;margin-top:6px}}
.chua{{font-size:12.5px;color:var(--muted)}}
.tha-am{{display:flex;flex-direction:column;align-items:center;gap:4px;
  background:#0a1220;border:1px dashed #3d5170;border-radius:10px;padding:18px 12px;
  cursor:pointer;text-align:center;margin-top:4px}}
.tha-am:active{{background:#0d1826}}
.tha-am input[type=file]{{display:none}}
.tha-am-icon{{font-size:24px;line-height:1}}
.tha-am-chu{{font-size:13px;color:#cbd4e4}}
.tha-am-chu small{{display:block;font-size:11.5px;color:var(--muted);margin-top:2px}}
.tha-am.co-file{{border-color:var(--jade);border-style:solid;background:#0d1f1a}}
.thanh{{height:6px;background:#0a1220;border-radius:99px;overflow:hidden;margin-top:8px}}
.thanh-ruot{{height:100%;width:0;background:var(--jade);transition:width .2s}}
.gui-tt{{font-size:12.5px;margin-top:8px;min-height:1em}}
.gui-kt.dang{{opacity:.6}}
.tom-tat{{background:#0e1726;border:1px solid var(--line);border-radius:12px;padding:12px 14px;
  margin:12px 0;font-size:13px}}
.tom-tat b{{color:var(--gold)}}
.ml{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}}
.ml a{{font-size:12px;background:#0e1726;border:1px solid var(--line);border-radius:99px;
  padding:3px 10px;text-decoration:none;color:#9fb2cf}}
.gh{{background:#0e1726;border:1px solid #31456a;border-radius:10px;padding:12px 14px;margin:12px 0}}
.gh input{{width:100%;font-size:12.5px;background:#0a1220;color:#dfe7f5;
  border:1px solid var(--line);border-radius:8px;padding:9px;margin:6px 0}}
.gh-tt{{font-size:12.5px;margin-top:6px}}
.ket-noi{{background:#0e1726;border:1px solid #31456a;border-radius:12px;
  padding:14px;margin:14px 0}}
.ket-noi input{{width:100%;font-size:12.5px;background:#0a1220;color:#dfe7f5;
  border:1px solid var(--line);border-radius:8px;padding:9px;margin:6px 0}}
footer{{margin-top:34px;padding-top:14px;border-top:1px solid var(--line);
  font-size:12px;color:var(--muted)}}
</style>
</head>
<body>

<h1>Xưởng âm thanh</h1>
<p class="muted">Tiếng nền cho từng cảnh. Chọn cảnh, copy prompt, tạo tiếng bằng công cụ anh
   thích, rồi tải lên đây — game tự dùng bản của anh.</p>

<div class="tom-tat">
  <b>{so} nhóm tiếng.</b> Mỗi cảnh trong game thuộc một nhóm, nên chỉ cần {so} file là phủ
  hết. Chưa tải lên nhóm nào thì game vẫn dùng tiếng tổng hợp sẵn trong máy — không bao giờ
  im.
  <div class="ml">
    {"".join(f'<a href="#c-{n["ma"]}">{esc(n["ten"])}</a>' for n in NHOM)}
  </div>
</div>

<h2>Cách làm</h2>
<div class="card">
  <ol style="margin:0;padding-left:20px">
    <li>Chọn cảnh ở dưới, bấm <b>📋 Copy prompt</b>.</li>
    <li>Dán vào công cụ sinh âm thanh. Nên chọn <b>30 giây</b>, có chế độ
        <b>loop / seamless</b> nếu công cụ có.</li>
    <li>Nghe lại. Ưng thì tải file về máy.</li>
    <li>Quay lại đây, <b>chọn file ngay dưới prompt</b> của đúng cảnh đó, bấm
        <b>📤 Gửi tiếng này</b>. Trang nén rồi tự đưa lên GitHub.</li>
    <li>Trang tự báo khi bot ghép xong và hiện ô nghe thử. Muốn xem lại thì bấm
        <b>🔄 Kiểm tra</b> trên thẻ — không cần tải lại trang.</li>
  </ol>
  <p class="muted" style="margin:10px 0 0">
    Định dạng nhận: <code>mp3</code>, <code>wav</code>, <code>m4a</code>, <code>ogg</code>,
    <code>flac</code>. File lớn cứ để nguyên, hệ thống tự nén về mp3 96 kbps và cân âm
    lượng về −18 LUFS.
  </p>
</div>

<div class="ket-noi">
  <p class="mota" style="margin-bottom:6px"><b>🔑 Kết nối GitHub (làm 1 lần)</b> — cần để trang
  tự đưa tiếng lên thay anh. Dán token vào đây; token chỉ lưu trong trình duyệt này
  (<code>localStorage</code>), không gửi đi đâu ngoài GitHub.</p>
  <input id="gh-token" type="password" autocomplete="off" spellcheck="false"
         placeholder="github_pat_… hoặc ghp_… (quyền: Contents = Read and write)">
  <div class="row">
    <button type="button" onclick="ghLuuToken()">💾 Lưu &amp; kiểm tra</button>
    <button type="button" class="phu" onclick="ghQuenToken()">🗑️ Quên token</button>
    <a class="dl" style="text-decoration:none;padding:7px 12px;border:1px solid var(--line);border-radius:8px"
       target="_blank"
       href="https://github.com/settings/personal-access-tokens/new?name=xuong-am&amp;description=Ti%E1%BA%BFng%20c%E1%BA%A3nh%20cho%20game&amp;contents=write">🔗 Tạo token (quyền Contents: Read and write)</a>
  </div>
  <div class="gui-tt" id="gh-tt" hidden></div>
  <p class="muted" style="font-size:12px;margin:8px 0 0">
    Chưa muốn dùng token? Vẫn còn
    <a href="https://github.com/huuducbkb/game-hong-duc-lam/issues/new?labels=xuong-am&amp;title=Ti%E1%BA%BFng%20c%E1%BA%A3nh%20m%E1%BB%9Bi"
       target="_blank">cách mở Issue rồi kéo file vào</a> — không cần token.
  </p>
</div>

<h2>Các nhóm tiếng</h2>
{ds}

<footer>
  Trang này sinh tự động từ <code>game/du_lieu_am.py</code>.<br>
  Tiếng do AI tạo (OpenHands) soạn prompt; bản ghi là do anh tạo và tải lên.
</footer>

<script>
{js}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    os.makedirs(os.path.dirname(RA), exist_ok=True)
    io.open(RA, "w", encoding="utf-8").write(sinh())
    print("da sinh", RA, os.path.getsize(RA), "bytes")
