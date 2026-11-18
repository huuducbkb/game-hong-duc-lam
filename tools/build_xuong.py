#!/usr/bin/env python3
"""Dựng Xưởng ảnh TĨNH cho GitHub Pages: docs/xuong/index.html.

Xưởng tĩnh có: prompt từng ảnh + nút copy + tải .txt, bố cục theo từng chương,
trạng thái ảnh đã có / còn thiếu, hướng dẫn tải ảnh lên, thư viện ảnh mẫu.

Chạy: python3 tools/build_xuong.py
Tự chạy lại trong GitHub Action sau mỗi lần nhận ảnh để cập nhật trạng thái.
"""

from __future__ import annotations

import html as H
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import tools_server as TS  # noqa: E402

REPO = "huuducbkb/game-hong-duc-lam"
OUT = os.path.join(ROOT, "docs", "xuong", "index.html")
UPLOAD_URL = f"https://github.com/{REPO}/upload/main/xuong-inbox"
ISSUE_URL = f"https://github.com/{REPO}/issues/new"


def co_anh(a: dict) -> bool:
    return os.path.isfile(os.path.join(TS.SCENE_DIR, a["file"])) or \
        os.path.isfile(os.path.join(TS.UI_DIR, a["file"]))


def _the_anh(a: dict, so: int) -> str:
    co = co_anh(a)
    doan = TS.doan_cua(a["key"])
    noi = ", ".join(doan) if doan else "—"
    nhan = "<span class='badge chac'>✅ đã có</span>" if co else "<span class='badge thieu'>⬜ còn thiếu</span>"
    gop = H.escape(TS.prompt_gui_ai(a))
    return f"""
<article class="asset{' done' if co else ''}" id="a{so}">
  <header>
    <span class="so">#{so}</span>
    <b>{H.escape(a['name'])}</b>
    {nhan}
    <span class="ratio">{H.escape(a['ratio'])}</span>
  </header>
  <div class="meta">
    <div><span class="k">mã</span> <code>{a['key']}</code></div>
    <div><span class="k">dùng ở</span> {H.escape(noi)}</div>
    <div><span class="k">lưu là</span> <code>{a['file']}</code></div>
  </div>
  <textarea readonly rows="6" id="p{so}" onclick="this.select()">{gop}</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('p{so}', this)">📋 Copy prompt</button>
    <button class="dl" onclick="taiTxt('p{so}', '{a['key']}.txt')">⬇️ .txt</button>
  </div>
</article>"""


def _nhom(khoi: dict) -> str:
    ds = [a for a in TS.ASSETS if TS.nhom_cua(a["key"]) == khoi["ma"]]
    if not ds:
        return ""
    so_map = TS.so_thu_tu()
    con = sum(1 for a in ds if not co_anh(a))
    the = "\n".join(_the_anh(a, so_map[a["key"]]) for a in ds)
    return f"""
<section class="khoi">
  <h2>{H.escape(khoi['ten'])}
    <span class="dem">{len(ds) - con}/{len(ds)} đã có</span></h2>
  <p class="mota">{H.escape(khoi['mota'])}</p>
  {the}
</section>"""


def _thu_vien() -> str:
    ds = [a for a in TS.ASSETS if TS.nhom_cua(a["key"]) == "mau" or
          a["key"] in TS.THU_VIEN_THU_TU]
    the = []
    for a in ds:
        co = co_anh(a)
        the.append(f"""
<div class="item{' thieu' if not co else ''}">
  <img src="../assets/scene/{a['file']}" alt="{H.escape(a['name'])}" loading="lazy">
  <div class="cap">
    <b>{H.escape(TS.ANH_MAU_TEN.get(a['key'], a['name']))}</b>
    <span class="muted">{a['file']}</span>
    <a class="dl" href="../assets/scene/{a['file']}" download="{a['file']}">⬇️ Tải ảnh</a>
  </div>
</div>""")
    return "\n".join(the)


def _inbox() -> str:
    """Hộp nhận ảnh — sắp theo từng chương, chỉ liệt kê ảnh còn thiếu."""
    khoi = []
    for k in TS.NHOM_BO_CUC:
        ds = [a for a in TS.ASSETS
              if TS.nhom_cua(a["key"]) == k["ma"] and not co_anh(a)]
        if not ds:
            continue
        so_map = TS.so_thu_tu()
        hang = "\n".join(
            f"<tr><td>#{so_map[a['key']]}</td><td><code>{a['key']}</code></td>"
            f"<td>{H.escape(a['name'])}</td><td class='muted'>{H.escape(', '.join(TS.doan_cua(a['key'])) or '—')}</td></tr>"
            for a in ds)
        khoi.append(f"""
<div class="inbox-khoi">
  <h3>{H.escape(k['ten'])} <span class="dem">{len(ds)} ảnh chờ</span></h3>
  <table><thead><tr><th>#</th><th>mã</th><th>loại</th><th>dùng ở</th></tr></thead>
  <tbody>{hang}</tbody></table>
</div>""")
    if not khoi:
        return "<p class='ok'>🎉 Tất cả ảnh đã có — không còn gì chờ!</p>"
    return "\n".join(khoi)


def build() -> str:
    tong = len(TS.ASSETS)
    con = sum(1 for a in TS.ASSETS if not co_anh(a))
    khoi_html = "\n".join(_nhom(k) for k in TS.NHOM_BO_CUC)
    return TEMPLATE.replace("__TONG__", str(tong)).replace("__CON__", str(con)) \
        .replace("__KHOI__", khoi_html).replace("__THUVIEN__", _thu_vien()) \
        .replace("__INBOX__", _inbox()).replace("__UPLOAD__", UPLOAD_URL) \
        .replace("__ISSUE__", ISSUE_URL)


TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xưởng ảnh — Hồng Đức Tu Tiên Lộ</title>
<style>
:root{--bg:#111a2b;--card:#182337;--ink:#e8e6df;--muted:#93a0b8;--gold:#ffd98a;
  --jade:#6fe0c0;--line:#2b3b57;--seal:#a8352a}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);
  color:var(--ink);margin:0 auto;padding:18px;max-width:760px;line-height:1.55;-webkit-text-size-adjust:100%}
h1{font-size:20px;color:var(--gold);margin:6px 0 2px}
h2{font-size:16px;color:var(--jade);margin:30px 0 6px;display:flex;flex-wrap:wrap;
  gap:8px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:7px}
h3{font-size:14px;color:#cbd4e4;margin:16px 0 6px}
p,li,td{font-size:13.5px;color:#cbd4e4}
.muted{color:var(--muted)}
code{background:#0a1220;padding:1px 6px;border-radius:4px;color:var(--jade);font-size:12px}
a{color:var(--jade)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
.dem{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
.mota{font-size:12.5px;color:var(--muted);margin:4px 0 10px}
.asset{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:13px;margin:12px 0;border-left:3px solid var(--jade)}
.asset.done{border-left-color:#2f8f5a;opacity:.72}
.asset header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:14px}
.so{font-size:11px;color:#3a2600;background:var(--gold);padding:2px 7px;border-radius:99px;font-weight:700}
.ratio{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
.badge{font-size:11px;padding:2px 8px;border-radius:99px}
.badge.chac{background:#12351f;color:#7fe0a8}
.badge.thieu{background:#2a150d;color:#ffb98a}
.meta{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12px;color:var(--muted);margin:8px 0}
.meta .k{color:#7f8ca3}
textarea{width:100%;font-size:12.5px;line-height:1.5;background:#0a1220;color:#dfe7f5;
  border:1px solid var(--line);border-radius:8px;padding:10px;resize:vertical;
  font-family:ui-monospace,Menlo,monospace}
button{font-family:inherit;font-size:13.5px;font-weight:600;border:0;border-radius:9px;
  padding:10px 14px;cursor:pointer}
.row{display:flex;gap:8px;margin-top:8px}
.cp{flex:1;background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600}
.cp.done{background:#2f8f5a;color:#eafff3}
.dl{background:linear-gradient(135deg,#2f8f7a,#6fe0c0);color:#04231c;text-decoration:none;
  display:inline-block;padding:10px 14px;border-radius:9px;font-size:13.5px;font-weight:600;
  text-align:center;border:0;cursor:pointer;font-family:inherit}
.big{display:block;text-align:center;margin:10px 0;font-size:15px;padding:14px}
.ok{background:#12351f;border:1px solid #2f8f5a;padding:12px;border-radius:10px;color:#7fe0a8;font-size:13px}
.warn{background:#3a1a10;border:1px solid #a05a2a;padding:12px;border-radius:10px;color:#ffb98a;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.item{background:#0f1728;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.item.thieu{border-color:#a05a2a}
.item img{width:100%;height:150px;object-fit:cover;display:block;background:#0a1220}
.item .cap{padding:8px;font-size:12px;display:flex;flex-direction:column;gap:5px}
.inbox-khoi{margin:14px 0}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600;font-size:11.5px}
ol{padding-left:20px}
ol li{margin:5px 0}
.steps code{font-size:12px}
details{margin:14px 0}
summary{cursor:pointer;color:var(--jade);font-size:13.5px;padding:6px 0}
</style>
</head>
<body>

<h1>Xưởng ảnh</h1>
<p class="muted">Hồng Đức Tu Tiên Lộ · <b>__CON__/__TONG__</b> ảnh còn thiếu.
Công việc của bạn: <b>copy prompt → vẽ → dán ảnh vào Issue</b>. Phần còn lại tự động.</p>

<h2>⚡ Cách làm — 3 bước</h2>
<div class="card">
  <ol class="steps">
    <li><b>Copy prompt</b>: bấm <b>📋 Copy prompt</b> ở ảnh bạn muốn vẽ (hoặc copy cả nhóm bên dưới),
        dán vào AI tạo ảnh (Gemini…). Nhớ chọn đúng <b>tỷ lệ</b> ghi trên thẻ.</li>
    <li><b>Vẽ ảnh</b>: nếu thẻ ghi <b>đính kèm ảnh mẫu</b>, tải ảnh mẫu ở mục
        <a href="#thuvien">📚 Thư viện ảnh mẫu</a> và đính kèm để giữ mặt nhân vật.</li>
    <li><b>Dán ảnh vào Issue</b>: mở <a href="__ISSUE__" target="_blank">trang tạo Issue</a>
        (hoặc Issue có sẵn), <b>kéo tất cả ảnh</b> vào ô bình luận rồi bấm <b>Comment</b>.
        Hệ thống tự nhận diện, nén, ghép vào đúng đoạn và cập nhật game.</li>
  </ol>
  <p class="muted" style="font-size:12.5px">Không cần đổi tên ảnh, không cần gõ gì thêm.
  Ảnh nào AI không chắc sẽ được <b>báo lại</b> để bạn xác nhận — không tự gán bừa.</p>
  <a class="dl big" href="__ISSUE__" target="_blank">💬 Mở Issue để dán ảnh</a>
  <details>
    <summary>Cách khác: tải ảnh lên thư mục (nếu bạn thích)</summary>
    <p class="muted" style="font-size:12.5px">Bấm nút dưới để mở trang upload của GitHub, kéo ảnh vào
    thư mục <code>xuong-inbox/</code> rồi bấm <b>Commit changes</b>. Hệ thống cũng tự xử lý.</p>
    <a class="dl big" href="__UPLOAD__" target="_blank">📤 Mở trang tải ảnh lên</a>
  </details>
</div>

<h2>📥 Hộp nhận ảnh — theo từng chương</h2>
<div class="card">
  <p class="mota">Danh sách ảnh <b>còn thiếu</b>, xếp theo chương/nhánh. Vẽ xong ảnh nào thì
  ảnh đó biến khỏi danh sách này.</p>
  __INBOX__
</div>

<h2>🎨 Prompt từng ảnh</h2>
__KHOI__

<h2 id="thuvien">📚 Thư viện ảnh mẫu</h2>
<div class="card">
  <p class="mota">Tải về để <b>đính kèm</b> khi vẽ ảnh cảnh — giữ cùng gương mặt nhân vật
  qua mọi cảnh. Trên iPad: bấm giữ ảnh → <b>“Lưu vào Ảnh”</b>.</p>
  <div class="grid">__THUVIEN__</div>
</div>

<script>
function cpText(id, btn){
  const ta=document.getElementById(id);
  ta.select(); ta.setSelectionRange(0,999999);
  const nhan=btn.textContent;
  const done=()=>{btn.classList.add('done');btn.textContent='✅ Đã copy';
    setTimeout(()=>{btn.classList.remove('done');btn.textContent=nhan;},1600);};
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(ta.value).then(done).catch(()=>{try{document.execCommand('copy');done();}catch(e){}});
  } else { try{document.execCommand('copy');done();}catch(e){} }
}
function taiTxt(id, ten){
  const txt=document.getElementById(id).value;
  const blob=new Blob([txt],{type:'text/plain;charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=ten||'prompt.txt';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}
</script>
</body></html>
"""


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"Đã dựng {OUT}")


if __name__ == "__main__":
    main()
