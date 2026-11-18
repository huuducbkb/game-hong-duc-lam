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
ISSUE_URL = (f"https://github.com/{REPO}/issues/new"
             "?template=gui-anh-xuong.md&labels=xuong-anh&title=%E1%BA%A2nh%20m%E1%BB%9Bi")


ten_sach = TS.ten_sach


def co_anh(a: dict) -> bool:
    return os.path.isfile(os.path.join(TS.SCENE_DIR, a["file"])) or \
        os.path.isfile(os.path.join(TS.UI_DIR, a["file"]))


def _the_anh(a: dict) -> str:
    co = co_anh(a)
    doan = TS.doan_cua(a["key"])
    noi = ", ".join(doan) if doan else "—"
    nhan = ("<span class='badge chac'>✅ đã có</span>" if co
            else "<span class='badge thieu'>⬜ còn thiếu</span>")
    so = TS.so_hien_thi().get(a["key"], "?")
    gop = H.escape(TS.prompt_gui_ai(a))
    sid = "p-" + a["key"].replace("_", "-")
    return f"""
<article class="asset{' done' if co else ''}" id="{sid}">
  <header>
    <span class="so">{so}</span>
    <b>{H.escape(ten_sach(a))}</b>
    {nhan}
    <span class="ratio">{H.escape(a['ratio'])}</span>
  </header>
  <div class="meta">
    <div><span class="k">mã</span> <code>{a['key']}</code></div>
    <div><span class="k">dùng ở</span> {H.escape(noi)}</div>
    <div><span class="k">lưu là</span> <code>{a['file']}</code></div>
  </div>
  <textarea readonly rows="5" id="{sid}">{gop}</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('{sid}', this)">📋 Copy prompt ảnh</button>
    <button class="dl" onclick="taiTxt('{sid}', '{a['key']}.txt')">⬇️ .txt</button>
  </div>
</article>"""


def _the_nhom(nhom: dict) -> str:
    """Một nhóm cảnh: prompt gộp cả nhóm + từng ảnh trong nhóm."""
    theo_key = {a["key"]: a for a in TS.ASSETS}
    ds = [theo_key[k] for k in nhom["keys"] if k in theo_key]
    if not ds:
        return ""
    so_map = TS.so_hien_thi()
    con = sum(1 for a in ds if not co_anh(a))
    sid = "g-" + nhom["ma"]
    if nhom.get("mau"):
        ten_mau = ", ".join(TS.ANH_MAU_TEN.get(k, k) for k in nhom["mau"])
        nhac = f'<b>Đính kèm:</b> <span class="mau">{H.escape(ten_mau)}</span>'
    else:
        nhac = '<b>Đính kèm:</b> <span class="muted">không cần</span>'
    nhan_so = " · ".join(so_map.get(a["key"], "?") for a in ds)
    gop = H.escape(TS.build_gop_prompt_canh(nhom))
    the_anh = "\n".join(_the_anh(a) for a in ds)
    return f"""
<section class="nhom" id="{sid}">
  <h3>{H.escape(nhom['ten'])}
    <span class="dem">{len(ds) - con}/{len(ds)} đã có</span></h3>
  <p class="mota">{H.escape(nhom['mota'])} <span class="so-ds">({nhan_so})</span></p>
  <div class="use">{nhac}</div>
  <details class="gop" open>
    <summary>🎬 Prompt vẽ CẢ NHÓM ({len(ds)} ảnh) — dán 1 lần, AI vẽ lần lượt</summary>
    <textarea readonly rows="9" id="{sid}">{gop}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{sid}', this)">📋 Copy prompt cả nhóm</button>
      <button class="dl" onclick="taiTxt('{sid}', '{nhom['ma']}.txt')">⬇️ .txt</button>
    </div>
  </details>
  <div class="ds-anh">{the_anh}</div>
</section>"""


def _the_phan(phan: dict) -> str:
    ds_nhom = [n for n in TS.NHOM_CANH if n["phan"] == phan["ma"]]
    tong = sum(len(n["keys"]) for n in ds_nhom)
    con = sum(1 for n in ds_nhom for k in n["keys"]
              if not co_anh(next(a for a in TS.ASSETS if a["key"] == k)))
    pid = "phan-" + phan["ma"]
    gop = H.escape(TS.build_gop_prompt_phan(phan["ma"]))
    than = "\n".join(_the_nhom(n) for n in ds_nhom)
    return f"""
<section class="phan" id="{pid}">
  <h2>{phan['icon']} {H.escape(phan['ten'])}
    <span class="dem">{tong - con}/{tong} đã có</span></h2>
  <p class="mota">{H.escape(phan['mota'])}</p>
  <details class="gop-phan">
    <summary>📦 Prompt vẽ TOÀN BỘ phần này ({tong} ảnh) — dán 1 lần cho cả phần</summary>
    <textarea readonly rows="10" id="{pid}">{gop}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{pid}', this)">📋 Copy prompt toàn phần</button>
      <button class="dl" onclick="taiTxt('{pid}', '{phan['ma']}.txt')">⬇️ .txt</button>
    </div>
  </details>
  {than}
</section>"""


def _thu_vien() -> str:
    ds = [a for a in TS.ASSETS if a["key"] in TS.THU_VIEN_THU_TU]
    ds.sort(key=lambda a: TS.THU_VIEN_THU_TU.index(a["key"]))
    the = []
    for a in ds:
        co = co_anh(a)
        the.append(f"""
<div class="item{' thieu' if not co else ''}">
  <img src="../assets/scene/{a['file']}" alt="{H.escape(ten_sach(a))}" loading="lazy">
  <div class="cap">
    <b>{H.escape(TS.ANH_MAU_TEN.get(a['key'], ten_sach(a)))}</b>
    <span class="muted">{a['file']}</span>
    <a class="dl" href="../assets/scene/{a['file']}" download="{a['file']}">⬇️ Tải ảnh</a>
  </div>
</div>""")
    return "\n".join(the)


def _muc_luc() -> str:
    """Mục lục nhanh: nhảy tới từng phần / nhóm cảnh."""
    dong = []
    for p in TS.XUONG_PHAN:
        ds = [n for n in TS.NHOM_CANH if n["phan"] == p["ma"]]
        con = []
        for n in ds:
            con.append(f'<a href="#g-{n["ma"]}">{H.escape(n["ten"])}</a>')
        dong.append(f"""
<div class="ml-phan">
  <a class="ml-ten" href="#phan-{p['ma']}">{p['icon']} {H.escape(p['ten'])}</a>
  <div class="ml-con">{' · '.join(con)}</div>
</div>""")
    return "\n".join(dong)


def _inbox() -> str:
    """Hộp nhận ảnh — sắp theo từng phần/nhóm cảnh, chỉ liệt kê ảnh còn thiếu."""
    khoi = []
    so_map = TS.so_hien_thi()
    for p in TS.XUONG_PHAN:
        ds = [a for a in TS.ASSETS
              if TS.phan_cua(a["key"]) == p["ma"] and not co_anh(a)]
        if not ds:
            continue
        hang = "\n".join(
            f"<tr><td>{so_map.get(a['key'],'?')}</td><td><code>{a['key']}</code></td>"
            f"<td>{H.escape(ten_sach(a))}</td>"
            f"<td class='muted'>{H.escape(', '.join(TS.doan_cua(a['key'])) or '—')}</td></tr>"
            for a in ds)
        khoi.append(f"""
<div class="inbox-khoi">
  <h3>{p['icon']} {H.escape(p['ten'])} <span class="dem">{len(ds)} ảnh chờ</span></h3>
  <table><thead><tr><th>#</th><th>mã</th><th>loại</th><th>dùng ở</th></tr></thead>
  <tbody>{hang}</tbody></table>
</div>""")
    if not khoi:
        return "<p class='ok'>🎉 Tất cả ảnh đã có — không còn gì chờ!</p>"
    return "\n".join(khoi)


def build() -> str:
    tong = len(TS.ASSETS)
    con = sum(1 for a in TS.ASSETS if not co_anh(a))
    khoi_html = "\n".join(_the_phan(p) for p in TS.XUONG_PHAN)
    return TEMPLATE.replace("__TONG__", str(tong)).replace("__CON__", str(con)) \
        .replace("__DA_CO__", str(tong - con)) \
        .replace("__MUC_LUC__", _muc_luc()).replace("__KHOI__", khoi_html) \
        .replace("__THUVIEN__", _thu_vien()).replace("__INBOX__", _inbox()) \
        .replace("__UPLOAD__", UPLOAD_URL).replace("__ISSUE__", ISSUE_URL)


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
.nhom{background:transparent;border:0;padding:0;margin:26px 0}
.nhom h3{font-size:14.5px;color:#dbe4f3;margin:0 0 4px;display:flex;flex-wrap:wrap;
  gap:8px;align-items:baseline;border-left:3px solid var(--jade);padding-left:9px}
.nhom .so-ds{color:var(--muted);font-size:11.5px;font-weight:400}
.phan{margin:34px 0}
.phan>h2{font-size:18px;color:var(--gold);border-bottom:2px solid var(--line);
  padding-bottom:8px;margin-top:38px}
.phan>.mota{font-size:13px;color:var(--muted);margin:6px 0 4px}
details.gop,details.gop-phan{margin:10px 0 16px;border:1px solid var(--line);
  border-radius:10px;background:#0e1726;padding:10px 12px}
details.gop summary,details.gop-phan summary{color:var(--jade);font-size:13px;
  font-weight:600;padding:2px 0}
details.gop-phan{margin:14px 0 22px;background:#101c2e;border-color:#31456a}
.ds-anh{display:flex;flex-direction:column;gap:12px}
.muc-luc{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:12px 14px;margin:14px 0}
.ml-phan{margin:9px 0}
.ml-ten{color:var(--gold);font-weight:600;font-size:13.5px;text-decoration:none}
.ml-con{font-size:12.5px;margin:3px 0 0 4px;line-height:1.9}
.ml-con a{color:#9fb2cf;text-decoration:none;border-bottom:1px dotted #3d5170}
.ml-con a:hover{color:var(--jade)}
.mau{color:var(--gold);font-weight:600}
.use{font-size:12.5px;color:var(--muted);margin:4px 0 8px}
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
<p class="muted">Hồng Đức Tu Tiên Lộ · đã có <b>__DA_CO__/__TONG__</b> ảnh, còn thiếu
<b>__CON__</b>. Công việc của bạn: <b>copy prompt → vẽ → dán ảnh vào Issue</b>. Phần còn lại tự động.</p>

<h2>⚡ Cách làm — 3 bước</h2>
<div class="card">
  <ol class="steps">
    <li><b>Copy prompt</b>: bấm <b>📋 Copy</b> — có 3 mức: <b>prompt từng ảnh</b>,
        <b>prompt cả nhóm cảnh</b>, hoặc <b>prompt toàn bộ một phần</b>. Dán vào AI tạo ảnh (Gemini…).
        Nhớ chọn đúng <b>tỷ lệ</b> ghi trên thẻ.</li>
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

<h2>🗺️ Mục lục</h2>
<div class="muc-luc">
__MUC_LUC__
</div>

<h2>📥 Hộp nhận ảnh — theo phần</h2>
<div class="card">
  <p class="mota">Danh sách ảnh <b>còn thiếu</b>, xếp theo từng phần. Vẽ xong ảnh nào thì
  ảnh đó biến khỏi danh sách này.</p>
  __INBOX__
</div>

<h2>🎨 Prompt theo phần · nhóm cảnh · từng ảnh</h2>
<p class="muted" style="font-size:12.5px">Mỗi phần có prompt gộp <b>toàn phần</b>; mỗi nhóm cảnh có
prompt gộp <b>cả nhóm</b>; mỗi ảnh có prompt <b>riêng</b>. Dán cái nào cũng được — AI vẽ lần lượt.</p>
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
