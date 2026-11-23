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
from du_lieu_am import CANH, NHOM, TEN_NHOM, canh_theo_nhom
from prompt_am import PROMPT

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "docs", "xuong-am", "index.html")
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xuong_am.js")

# Tên file trên đĩa: <ma>.mp3 trong docs/assets/am/
DUONG = "assets/am/"
# Ảnh cảnh trong game, bản thu nhỏ 300px (gốc 900px nặng gấp 10 lần).
ANH = "/assets/scene/nho/"


def da_co():
    """Mã cảnh/nhóm đã có file tiếng trên đĩa, đọc từ danh-sach.json."""
    import json
    p = os.path.join(GOC, "docs", "assets", "am", "danh-sach.json")
    if not os.path.isfile(p):
        return set()
    try:
        return set(json.load(io.open(p, encoding="utf-8")))
    except Exception:  # noqa: BLE001 - file hỏng thì coi như chưa có gì
        return set()


def esc(s):
    return html.escape(str(s), quote=True)


def khoi_prompt(n):
    """Khối prompt tạo tiếng của một cảnh."""
    ma = n["ma"]
    p = PROMPT.get(ma)
    if not p:
        return ""
    nut = (f'<button type="button" class="cp" '
           f'onclick="cpChu(this,{esc(repr(p))})">📋 Chép prompt</button>')
    n_ky = len(p)
    dem = (f'<span class="dem-ky{" qua" if n_ky > 450 else ""}">'
           f'{n_ky}/450 ký tự</span>')
    return f"""<label class="nhan">Prompt tạo tiếng — dán vào công cụ tạo âm thanh</label>
<div class="prompt" id="p-{ma}">{esc(p)}</div>
<div class="row">{nut}{dem}</div>
<p class="mota" style="margin:6px 0 0">Prompt tả âm thanh, không kể chuyện: mở bằng câu
khai báo có chất âm, rồi tới sát tai — vài mét — xa, kèm chỗ tiếng đổi chất (tường dội,
phòng kín, ngoài trời). Không có lời nói, chỉ thở, hừ, la, khóc. Có sẵn "no music",
"no speech", "seamless loop". Ô prompt của ElevenLabs chỉ nhận 450 ký tự.</p>"""


def the_canh(n, i):
    ma = n["ma"]
    anh = n["anh"]
    co = da_co()
    if ma in co:
        trang_thai = "✅ Đã có tiếng riêng cho cảnh này."
    else:
        trang_thai = "⬜ Chưa có tiếng — cảnh này đang im. Gửi file ở dưới để thêm."
    return f"""
<article class="canh" id="c-{ma}" data-ma="{ma}" data-file="{n['file']}">
  <header>
    <span class="so">{i}</span>
    <b>{esc(n['ten'])}</b>
    <code>{ma}</code>
    <span class="badge thieu" data-badge>⬜ chưa có</span>
  </header>

  <figure class="anh-mot" onclick="xemAnh(this)">
    <img loading="lazy" src="..{ANH}{esc(anh)}" alt="{esc(n['ten'])}">
    <figcaption>{esc(anh)} — bấm để xem to</figcaption>
  </figure>

  <p class="mota">{esc(n['mota'])}</p>
  <div class="meta">
    <div><span class="k">lưu là</span> <code>{DUONG}{esc(n['file'])}</code></div>
  </div>

  {khoi_prompt(n)}

  <label class="nhan">Từ khoá tìm trên thư viện âm thanh</label>
  <div class="tukhoa">
    {"".join(f'<button type="button" class="tk" onclick="cpChu(this,{esc(repr(k))})">{esc(k)}</button>' for k in n["tim"])}
  </div>
  <p class="mota" style="margin:6px 0 0">Dán vào ô tìm của Freesound, Pixabay, YouTube.
     Tìm bằng tiếng Anh mới ra; tiếng Việt gần như không có.</p>

  <label class="nhan">Từ khoá mô tả âm thanh — dán vào Google</label>
  <div class="tukhoa">
    {"".join(f'<button type="button" class="tk mo" onclick="cpChu(this,{esc(repr(k))})">{esc(k)}</button>' for k in n["mo_ta"])}
  </div>
  <p class="mota" style="margin:6px 0 0">Dùng khi muốn tìm hiểu tiếng này gọi là gì,
     hoặc tìm nguồn ở chỗ khác.</p>

  <label class="nhan">Nghe thử bản đang dùng trong game</label>
  <div class="nghe" data-nghe>
    <audio controls playsinline preload="none" data-audio hidden></audio>
    <span class="chua" data-chua>{esc(trang_thai)}</span>
  </div>

  <div class="gui" data-gui data-file="{n['file']}" data-ma="{ma}">
    <label class="tha-am" tabindex="0">
      <input type="file" data-chon
             accept="audio/*,video/mp4,video/quicktime,video/webm,video/x-matroska,video/3gpp,video/x-msvideo,video/*,.mp3,.wav,.m4a,.ogg,.flac,.mp4,.mov,.m4v,.webm,.mkv,.avi,.3gp">
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
    dem = 0
    phan = []
    for ma_nhom, ten_nhom in NHOM:
        ds_nhom = canh_theo_nhom(ma_nhom)
        if not ds_nhom:
            continue
        phan.append(f'<h2 id="n-{ma_nhom}">{esc(ten_nhom)}'
                    f'<span class="dem">{len(ds_nhom)} cảnh</span></h2>')
        for n in ds_nhom:
            dem += 1
            phan.append(the_canh(n, dem))
    ds = "\n".join(phan)
    so = len(CANH)

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
.dem-ky{{font-size:11.5px;color:var(--muted);margin-left:auto;align-self:center;
  font-variant-numeric:tabular-nums}}
.dem-ky.qua{{color:#ff9a8a;font-weight:600}}
.prompt{{background:#0a1220;border:1px solid var(--line);border-radius:8px;padding:10px;
  font-size:12.5px;line-height:1.6;color:#dfe7f5;white-space:pre-wrap;
  font-family:ui-monospace,Menlo,monospace;-webkit-user-select:text;user-select:text}}
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
.anh-mot{{margin:10px 0 0;cursor:pointer}}
.anh-mot img{{width:100%;max-width:300px;aspect-ratio:3/4;object-fit:cover;
  border-radius:9px;display:block;border:1px solid var(--line);background:#0a1220}}
.anh-mot figcaption{{font-size:10.5px;color:var(--muted);margin-top:3px}}
.dem{{font-size:11.5px;color:var(--muted);font-weight:400}}
.tk.mo{{background:#131f2e;border-color:#3a4d66;color:#a8bdd6}}
.luoi-anh{{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:2px 0 0}}
.luoi-anh figure{{margin:0;cursor:pointer}}
.luoi-anh img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:7px;
  display:block;border:1px solid var(--line);background:#0a1220}}
.luoi-anh figcaption{{font-size:10.5px;color:var(--muted);line-height:1.3;margin-top:3px}}
.xem-anh{{position:fixed;inset:0;z-index:50;display:none;align-items:center;
  justify-content:center;padding:16px;background:rgba(6,10,18,.94)}}
.xem-anh.mo{{display:flex}}
.xem-anh img{{max-width:100%;max-height:82vh;border-radius:10px}}
.xem-anh .nen{{position:absolute;inset:0}}
.xem-anh .chu{{position:absolute;bottom:14px;left:0;right:0;text-align:center;
  font-size:13px;color:#dfe7f5;padding:0 16px}}
.tukhoa{{display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 0}}
.tk{{background:#0e1c2a;border:1px solid #2b4a63;color:#9fd8e8;font-size:12px;
  padding:6px 11px;border-radius:99px;font-family:ui-monospace,Menlo,monospace}}
.tk:active{{background:#12303f}}
.tk.da{{background:#123a2c;border-color:#2f6b4f;color:#a9f0c4}}
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
  <b>{so} cảnh, mỗi cảnh một file riêng.</b> Mỗi ảnh trong game là một cảnh, có tiếng
  riêng và từ khoá riêng. Cảnh nào chưa có file thì im — không lấy tiếng của cảnh khác,
  không chèn nhạc tổng hợp.
  <div class="ml">
    {"".join(f'<a href="#n-{ma}">{esc(ten)}</a>' for ma, ten in NHOM if canh_theo_nhom(ma))}
  </div>
</div>

<h2>Cách làm</h2>
<div class="card">
  <ol style="margin:0;padding-left:20px">
    <li>Nhìn <b>ảnh</b> ở mỗi cảnh để chắc đúng ngữ cảnh anh cần.</li>
    <li>Bấm một <b>từ khoá</b> để copy.</li>
    <li>Dán vào ô tìm của thư viện (Freesound, Pixabay, YouTube…). Tìm bằng tiếng Anh
        mới ra; tiếng Việt gần như không có.</li>
    <li>Tải file về máy. <b>Dài bao nhiêu cũng được</b> — 2 phút, 5 phút, không sao.</li>
    <li>Quay lại đây, <b>chọn file dưới đúng cảnh</b>, bấm <b>📤 Gửi tiếng này</b>.</li>
    <li>Bot tự lấy <b>12 giây đầu</b>, chuyển mp3, cân âm lượng, rồi ghép vào game.</li>
    <li><b>Gửi được cả video.</b> Chọn video (mp4, mov, webm…) là trình duyệt tự trích
    tiếng, nén thành mp3 ngay trên máy anh rồi chỉ gửi đoạn mp3 đó —
    <b>video không được tải lên</b>, nên không nằm trong repo. Video dưới <b>5 MB</b>;
    lớn hơn thì giải mã trên điện thoại rất chậm, cắt bớt trước. Video không có tiếng
    thì báo lỗi ngay, không gửi file rỗng.</li>
  </ol>

  <div class="card" style="background:#0e1726;margin:14px 0 0;padding:12px">
    <p style="margin:0 0 8px;font-size:12.5px"><b>Hai bộ từ khoá khác nhau:</b></p>
    <ul style="margin:0;padding-left:18px;font-size:12.5px">
      <li><b>Từ khoá tìm</b> — để tìm file trên thư viện. Đây là thứ người ta đặt tên
          cho file âm thanh.</li>
      <li><b>Từ khoá mô tả</b> — để dán vào Google khi muốn hiểu tiếng đó gọi là gì,
          hoặc tìm nguồn ở chỗ khác.</li>
    </ul>
  </div>

  <div class="card" style="background:#0e1726;margin:10px 0 0;padding:12px">
    <p style="margin:0;font-size:12.5px"><b>Về 12 giây:</b> file anh gửi dài bao nhiêu
    cũng được, hệ thống <b>tự cắt 12 giây đầu</b>. Cảnh trong game chỉ 10 giây, nên 12
    giây là dư một chút để vòng lặp không chạm mép file. File ngắn hơn 12 giây thì giữ
    nguyên, không cắt.</p>
  </div>

  <p class="muted" style="margin:10px 0 0">
    Định dạng nhận: <code>mp3</code>, <code>wav</code>, <code>m4a</code>, <code>ogg</code>,
    <code>flac</code>, hoặc video <code>mp4</code>/<code>mov</code>/<code>webm</code>.
    Gửi thẳng được tới <b>24 MB</b>; lớn hơn thì nén bớt trước. Sau khi
    gửi, bot tự lấy 12 giây đầu, chuyển về mp3 96 kbps và cân âm lượng về −18 LUFS.
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

{ds}

<footer>
  Trang này sinh tự động từ <code>game/du_lieu_am.py</code>.<br>
  Tiếng do AI tạo (OpenHands) soạn prompt; bản ghi là do anh tạo và tải lên.<br>
  Nén mp3 trong trình duyệt dùng <a href="lamejs.NOTICE.txt">lamejs</a> (LAME, LGPL-3.0).
</footer>

<div class="xem-anh" id="xem-anh" onclick="dongAnh()">
  <div class="nen"></div>
  <img id="xem-anh-img" alt="">
  <div class="chu" id="xem-anh-chu"></div>
</div>

<script src="lamejs.js"></script>
<script>
function xemAnh(fig){{
  const img = fig.querySelector('img');
  const chu = fig.querySelector('figcaption');
  const hop = document.getElementById('xem-anh');
  document.getElementById('xem-anh-img').src = img.src.replace('/nho/', '/');
  document.getElementById('xem-anh-chu').textContent = chu ? chu.textContent : '';
  hop.classList.add('mo');
}}
function dongAnh(){{
  document.getElementById('xem-anh').classList.remove('mo');
}}
document.addEventListener('keydown', e => {{ if(e.key === 'Escape') dongAnh(); }});
{js}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    os.makedirs(os.path.dirname(RA), exist_ok=True)
    io.open(RA, "w", encoding="utf-8").write(sinh())
    print("da sinh", RA, os.path.getsize(RA), "bytes")
