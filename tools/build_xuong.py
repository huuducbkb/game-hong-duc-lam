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
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import tools_server as TS  # noqa: E402

REPO = "huuducbkb/game-hong-duc-lam"
OUT = os.path.join(ROOT, "docs", "xuong", "index.html")
UPLOAD_URL = f"https://github.com/{REPO}/upload/main/xuong-inbox"
ISSUE_URL = (f"https://github.com/{REPO}/issues/new"
             "?template=gui-anh-xuong.md&labels=xuong-anh&title=%E1%BA%A2nh%20m%E1%BB%9Bi")


def _gui_url(body: str, tieu_de: str) -> str:
    """Link mở Issue điền sẵn mã ảnh — bot đọc mã nên gán thẳng, không cần đoán."""
    q = urllib.parse.urlencode({"labels": "xuong-anh", "title": tieu_de, "body": body})
    return f"https://github.com/{REPO}/issues/new?{q}"


def _folder_url(key: str) -> str:
    """Link mở trang upload GitHub đã trỏ sẵn vào xuong-inbox/<mã>/.

    Kéo ảnh vào đó rồi Commit → bot thấy thư mục con trùng mã nên gán thẳng.
    """
    return f"https://github.com/{REPO}/upload/main/xuong-inbox/{key}"


def _body_nhom(keys: list) -> str:
    return ("".join(f"mã-ảnh: {k}\n" for k in keys)
            + "\nDán ảnh vào đây ĐÚNG THỨ TỰ trên (kéo thả từng ảnh):\n")


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
    tid = sid + "-t"
    k = a["key"]
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
  <textarea readonly rows="5" id="{tid}">{gop}</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('{tid}', this)">📋 Copy prompt ảnh</button>
    <button class="dl" onclick="taiTxt('{tid}', '{k}.txt')">⬇️ .txt</button>
  </div>
  <div class="gui-o" data-key="{k}">
    <label class="gui-dan" data-key="{k}" tabindex="0"
           title="Bấm để chọn ảnh trong thư viện ảnh (điện thoại) hoặc dán/kéo thả (máy tính)">
      <input class="gui-file" type="file" accept="image/*">
      <span class="gui-nhac">📷 Bấm vào đây để chọn ảnh</span>
      <img class="gui-xem" alt="" hidden>
    </label>
    <button class="gui-gui" type="button" disabled>📤 Gửi ảnh này</button>
    <div class="gui-tt" hidden></div>
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
    tid = sid + "-t"
    if nhom.get("mau"):
        ten_mau = ", ".join(TS.ANH_MAU_TEN.get(k, k) for k in nhom["mau"])
        nhac = f'<b>Đính kèm:</b> <span class="mau">{H.escape(ten_mau)}</span>'
    else:
        nhac = '<b>Đính kèm:</b> <span class="muted">không cần</span>'
    nhan_so = " · ".join(so_map.get(a["key"], "?") for a in ds)
    gop = H.escape(TS.build_gop_prompt_canh(nhom))
    gui_nhom = _gui_url(_body_nhom(nhom["keys"]), f"Ảnh nhóm {nhom['ten']}")
    nut_nhom = ("" if len(ds) < 2 else
                f'<a class="gui nhom-gui" href="{H.escape(gui_nhom)}" target="_blank">'
                f'📤 Gửi ảnh cho CẢ NHÓM này ({len(ds)} ảnh)</a>')
    the_anh = "\n".join(_the_anh(a) for a in ds)
    return f"""
<section class="nhom" id="{sid}">
  <h3>{H.escape(nhom['ten'])}
    <span class="dem">{len(ds) - con}/{len(ds)} đã có</span></h3>
  <p class="mota">{H.escape(nhom['mota'])} <span class="so-ds">({nhan_so})</span></p>
  <div class="use">{nhac}</div>
  {nut_nhom}
  <details class="gop" open>
    <summary>🎬 Prompt vẽ CẢ NHÓM ({len(ds)} ảnh) — dán 1 lần, AI vẽ lần lượt</summary>
    <textarea readonly rows="9" id="{tid}">{gop}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{tid}', this)">📋 Copy prompt cả nhóm</button>
      <button class="dl" onclick="taiTxt('{tid}', '{nhom['ma']}.txt')">⬇️ .txt</button>
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
    tid = pid + "-t"
    gop = H.escape(TS.build_gop_prompt_phan(phan["ma"]))
    than = "\n".join(_the_nhom(n) for n in ds_nhom)
    return f"""
<section class="phan" id="{pid}">
  <h2>{phan['icon']} {H.escape(phan['ten'])}
    <span class="dem">{tong - con}/{tong} đã có</span></h2>
  <p class="mota">{H.escape(phan['mota'])}</p>
  <details class="gop-phan">
    <summary>📦 Prompt vẽ TOÀN BỘ phần này ({tong} ảnh) — dán 1 lần cho cả phần</summary>
    <textarea readonly rows="10" id="{tid}">{gop}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{tid}', this)">📋 Copy prompt toàn phần</button>
      <button class="dl" onclick="taiTxt('{tid}', '{phan['ma']}.txt')">⬇️ .txt</button>
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
            f"<td class='muted'>{H.escape(', '.join(TS.doan_cua(a['key'])) or '—')}</td>"
            f"<td><a class='dl tm-nho' href='{H.escape(_folder_url(a['key']))}' target='_blank'"
            f" title='Mở GitHub trỏ sẵn vào xuong-inbox/{H.escape(a['key'])}/'>📁 Up</a></td></tr>"
            for a in ds)
        khoi.append(f"""
<div class="inbox-khoi">
  <h3>{p['icon']} {H.escape(p['ten'])} <span class="dem">{len(ds)} ảnh chờ</span></h3>
  <table><thead><tr><th>#</th><th>mã</th><th>loại</th><th>dùng ở</th><th>up</th></tr></thead>
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
.gui{display:block;text-align:center;margin-top:8px;background:#1d2b45;color:var(--gold);
  border:1px dashed #4a628c;border-radius:9px;padding:10px 14px;font-size:13.5px;
  font-weight:600;text-decoration:none}
.gui:hover{background:#243757;border-color:var(--gold)}
.gui.nhom-gui{margin:8px 0 4px;font-size:13px}
.gui.thu-muc{background:#2a2338;border-color:#6b5a8c;color:#d9c7ff;font-size:12.5px;
  padding:9px 12px}
.gui.thu-muc:hover{background:#352c48;border-color:#a68cf0;color:#efe6ff}
.gui.thu-muc code{font-size:11.5px;color:#c9b6ff}
.ket-noi{margin:12px 0}
.ket-noi input{width:100%;font-size:13px;padding:9px 10px;border-radius:8px;
  border:1px solid var(--line);background:#0a1220;color:#dfe7f5;
  font-family:ui-monospace,Menlo,monospace}
.ket-noi .row{flex-wrap:wrap}
.ket-noi button{background:#1d2b45;color:var(--gold);border:1px solid #4a628c}
.ket-noi button:hover{background:#243757}
.gui-o{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:10px;background:#0e1726}
.gui-dan{display:block;position:relative;border:2px dashed var(--line);border-radius:9px;
  padding:22px 12px;text-align:center;cursor:pointer;color:var(--muted);font-size:13.5px;
  transition:.15s;-webkit-tap-highlight-color:transparent}
.gui-dan:hover,.gui-dan.act{border-color:var(--jade);color:var(--jade)}
.gui-file{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;
  font-size:0;border:0;padding:0}
.gui-nhac,.gui-xem{pointer-events:none}
.gui-xem{max-width:100%;max-height:260px;border-radius:8px;display:block;margin:0 auto}
.gui-gui{display:block;width:100%;margin-top:8px;background:linear-gradient(135deg,#f7b32b,#ffd166);
  color:#3a2600;padding:14px;border-radius:9px;font-weight:700;border:0;cursor:pointer;
  font-size:15px;font-family:inherit}
.gui-gui:disabled{opacity:.45;cursor:not-allowed}
.gui-tt{margin-top:7px;font-size:12.5px}
.gui-tt .ok,.gui-tt .warn{display:block;padding:8px 10px;border-radius:8px}
.gui-tt .muted{display:block}
.dl.tm-nho{padding:5px 10px;font-size:12px;white-space:nowrap}
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
<b>__CON__</b>. Công việc của bạn: <b>copy prompt → vẽ → chọn ảnh ngay dưới prompt</b>. Phần còn lại tự động.</p>

<h2>⚡ Cách làm — 2 bước</h2>
<div class="card">
  <ol class="steps">
    <li><b>Copy prompt</b>: bấm <b>📋 Copy</b> — có 3 mức: <b>prompt từng ảnh</b>,
        <b>prompt cả nhóm cảnh</b>, hoặc <b>prompt toàn bộ một phần</b>. Dán vào AI tạo ảnh (Gemini…).
        Nhớ chọn đúng <b>tỷ lệ</b> ghi trên thẻ.</li>
    <li><b>Vẽ ảnh</b>: nếu thẻ ghi <b>đính kèm ảnh mẫu</b>, tải ảnh mẫu ở mục
        <a href="#thuvien">📚 Thư viện ảnh mẫu</a> và đính kèm để giữ mặt nhân vật.</li>
    <li><b>Chọn ảnh ngay dưới prompt</b>: vẽ xong, <b>bấm vào ô 📷 ngay dưới prompt</b> của
        thẻ đó → chọn ảnh trong <b>thư viện ảnh</b> (điện thoại) hoặc hộp chọn file (máy tính).
        Trên máy tính còn có thể <b>dán Ctrl+V</b> hoặc <b>kéo thả</b> ảnh vào ô.
        Rồi bấm <b>📤 Gửi ảnh này</b>. Ảnh được nén ngay trên máy bạn rồi tự đưa lên GitHub —
        <b>không cần mở Issue</b>, hệ thống gán <b>đúng ảnh theo mã trên thẻ, không đoán sai</b>.</li>
  </ol>
  <p class="muted" style="font-size:12.5px">Gửi nhiều ảnh một lúc thì dùng nút
  <b>📤 Gửi ảnh cho CẢ NHÓM</b> ở đầu mỗi nhóm — dán ảnh <b>đúng thứ tự</b> như danh sách mã.
  Không cần đổi tên ảnh, không cần gõ gì thêm.</p>

  <div class="ket-noi">
    <p class="mota" style="margin-bottom:6px"><b>🔑 Kết nối GitHub (làm 1 lần)</b> — cần để trang
    tự đưa ảnh lên thay bạn. Dán token vào đây; token chỉ lưu trong trình duyệt này
    (<code>localStorage</code>), không gửi đi đâu ngoài GitHub.</p>
    <input id="gh-token" type="password" autocomplete="off" spellcheck="false"
           placeholder="github_pat_… hoặc ghp_… (quyền: Contents = Read and write)">
    <div class="row">
      <button type="button" onclick="ghLuuToken()">💾 Lưu &amp; kiểm tra</button>
      <button type="button" onclick="ghQuenToken()">🗑️ Quên token</button>
      <a class="dl" style="text-decoration:none" target="_blank"
         href="https://github.com/settings/personal-access-tokens/new?name=xuong-anh&amp;description=D%C3%A1n%20%E1%BA%A3nh%20v%C3%A0o%20X%C6%B0%E1%BB%9Fng&amp;contents=write">🔗 Tạo token (quyền Contents: Read and write)</a>
    </div>
    <div class="gui-tt" id="gh-tt" hidden></div>
  </div>

  <a class="dl big" href="__ISSUE__" target="_blank">💬 Hoặc mở Issue trống để dán ảnh (cách cũ)</a>
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
  if(!ta){return;}
  const val=(ta.value!==undefined?ta.value:ta.textContent)||'';
  const nhan=btn.textContent;
  const done=()=>{btn.classList.add('done');btn.textContent='✅ Đã copy';
    setTimeout(()=>{btn.classList.remove('done');btn.textContent=nhan;},1600);};
  const duPhong=()=>{
    const tam=document.createElement('textarea');
    tam.value=val; tam.style.position='fixed'; tam.style.top='-1000px'; tam.style.opacity='0';
    document.body.appendChild(tam); tam.focus(); tam.select();
    let ok=false; try{ok=document.execCommand('copy');}catch(e){}
    tam.remove(); if(ok){done();}
  };
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(val).then(done).catch(duPhong);
  } else { duPhong(); }
}
function taiTxt(id, ten){
  const txt=document.getElementById(id).value;
  const blob=new Blob([txt],{type:'text/plain;charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=ten||'prompt.txt';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}

/* ================= Kết nối GitHub (token trong máy) ================= */
const GH_REPO='huuducbkb/game-hong-duc-lam';
const GH_BRANCH='main';
const GH_LS='xuong_gh_token';

function ghToken(){ return localStorage.getItem(GH_LS)||''; }

function ghHienTT(el, loai, html){
  el.hidden=false;
  el.innerHTML = `<span class="${loai}">${html}</span>`;
}

async function ghLuuToken(){
  const inp=document.getElementById('gh-token');
  const tt=document.getElementById('gh-tt');
  const t=(inp.value||'').trim();
  if(!t){ ghHienTT(tt,'warn','⚠️ Chưa dán token.'); return; }
  ghHienTT(tt,'muted','Đang kiểm tra token…');
  try{
    const r=await fetch(`https://api.github.com/repos/${GH_REPO}`,{
      headers:{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}});
    if(!r.ok){ ghHienTT(tt,'warn',`⚠️ Token không dùng được (HTTP ${r.status}). Kiểm tra lại quyền Contents: Read and write.`); return; }
    const j=await r.json();
    if(j.permissions && j.permissions.push === false){
      ghHienTT(tt,'warn','⚠️ Token chưa có quyền ghi (cần Contents: Read and write). Tạo lại token rồi thử lại.');
      return;
    }
    localStorage.setItem(GH_LS,t);
    ghHienTT(tt,'ok',`✅ Đã kết nối <b>${j.full_name}</b>. Từ giờ dán ảnh vào ô dưới mỗi prompt rồi bấm Gửi là xong.`);
  }catch(e){ ghHienTT(tt,'warn',`⚠️ Lỗi kết nối: ${e}`); }
}

function ghQuenToken(){
  localStorage.removeItem(GH_LS);
  const inp=document.getElementById('gh-token'); if(inp) inp.value='';
  ghHienTT(document.getElementById('gh-tt'),'muted','Đã quên token trong trình duyệt này.');
}

/* Nén ảnh ngay trên máy: giữ PNG (có trong suốt), còn lại JPEG. */
function ghNenAnh(file, maxCanh=1600, q=0.9){
  return new Promise((res,rej)=>{
    const url=URL.createObjectURL(file);
    const im=new Image();
    im.onload=()=>{
      URL.revokeObjectURL(url);
      let {width:w,height:h}=im;
      const tiLe=Math.min(1, maxCanh/Math.max(w,h));
      w=Math.round(w*tiLe); h=Math.round(h*tiLe);
      const cv=document.createElement('canvas'); cv.width=w; cv.height=h;
      const cx=cv.getContext('2d');
      cx.drawImage(im,0,0,w,h);
      const giuPng = file.type==='image/png';
      cv.toBlob(b=>b?res({blob:b,duoi:giuPng?'png':'jpg'}):rej(new Error('nén lỗi')),
                giuPng?'image/png':'image/jpeg', q);
    };
    im.onerror=()=>{ URL.revokeObjectURL(url); rej(new Error('không đọc được ảnh')); };
    im.src=url;
  });
}

function blobB64(blob){
  return new Promise((res,rej)=>{
    const r=new FileReader();
    r.onload=()=>res(r.result.split(',')[1]);
    r.onerror=()=>rej(new Error('đọc file lỗi'));
    r.readAsDataURL(blob);
  });
}

async function ghLaySha(duong){
  const t=ghToken();
  const r=await fetch(`https://api.github.com/repos/${GH_REPO}/contents/${duong}?ref=${GH_BRANCH}`,
    {headers:{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}});
  if(r.status===200){ const j=await r.json(); return j.sha||null; }
  return null; // 404 = file chưa có
}

async function ghPutAnh(duong, b64, thayThe){
  const t=ghToken();
  const body={message:`Xưởng: ${thayThe?'thay':'thêm'} ảnh ${duong.split('/').slice(-2,-1)[0]}`,
              content:b64, branch:GH_BRANCH};
  const sha=await ghLaySha(duong);
  if(sha) body.sha=sha;
  const r=await fetch(`https://api.github.com/repos/${GH_REPO}/contents/${duong}`,{
    method:'PUT',
    headers:{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json',
             'Content-Type':'application/json'},
    body:JSON.stringify(body)});
  if(!r.ok){
    let loi='';
    try{ const j=await r.json(); loi=j.message||''; }catch(e){}
    throw new Error(`HTTP ${r.status}${loi?' — '+loi:''}`);
  }
  return !!sha;
}

/* ================= Ô chọn ảnh dưới mỗi prompt ================= */
/* Ô là <label> bọc <input type=file> phủ toàn ô → chạm là mở thư viện ảnh
   (điện thoại) hoặc hộp chọn file (máy tính). Kéo-thả do input tự nhận. */
let O_DANG_CHON=null;   // ô vừa chạm (để Ctrl+V trên máy tính dán đúng ô)

function datAnhVaoO(o, file){
  if(!file || !file.type.startsWith('image/')) return;
  const hop=o.parentElement;
  const xem=o.querySelector('.gui-xem');
  const nhac=o.querySelector('.gui-nhac');
  const nut=hop.querySelector('.gui-gui');
  const tt=hop.querySelector('.gui-tt');
  o._file=file;
  const url=URL.createObjectURL(file);
  xem.src=url; xem.hidden=false;
  if(nhac) nhac.hidden=true;
  o.classList.add('act');
  nut.disabled=false;
  if(tt){ tt.hidden=true; tt.innerHTML=''; }
}

function khoiTaoO(){
  document.querySelectorAll('.gui-dan').forEach(o=>{
    const hop=o.parentElement;
    const inp=o.querySelector('input[type=file]');
    const nut=hop.querySelector('.gui-gui');
    // Chạm vào ô: đánh dấu ô này để Ctrl+V dán đúng đây (máy tính).
    o.addEventListener('click',()=>{ O_DANG_CHON=o; });
    o.addEventListener('focus',()=>{ O_DANG_CHON=o; });
    if(inp) inp.addEventListener('change',()=>{ if(inp.files[0]) datAnhVaoO(o,inp.files[0]); });
    if(nut) nut.addEventListener('click',()=>guiMotAnh(o,nut));
  });
  // Máy tính: Ctrl+V dán ảnh vào ô vừa chạm.
  document.addEventListener('paste',e=>{
    const it=e.clipboardData&&e.clipboardData.items;
    if(!it) return;
    let f=null;
    for(const x of it){ if(x.type.startsWith('image/')){ f=x.getAsFile(); break; } }
    if(!f) return;
    const o=O_DANG_CHON || document.querySelector('.gui-dan.act');
    if(!o) return;
    e.preventDefault();
    datAnhVaoO(o,f);
  });
}

async function guiMotAnh(o, nut){
  const key=o.dataset.key;
  const tt=o.parentElement.querySelector('.gui-tt');
  const file=o._file;
  if(!ghToken()){
    ghHienTT(tt,'warn','⚠️ Chưa kết nối GitHub. Dán token ở mục <b>🔑 Kết nối GitHub</b> phía trên rồi thử lại.');
    return;
  }
  if(!file){ ghHienTT(tt,'warn','⚠️ Chưa có ảnh. Bấm vào ô rồi dán ảnh (Ctrl+V), hoặc kéo thả ảnh vào ô.'); return; }
  nut.disabled=true;
  ghHienTT(tt,'muted','Đang nén ảnh…');
  try{
    const {blob,duoi}=await ghNenAnh(file);
    const b64=await blobB64(blob);
    ghHienTT(tt,'muted',`Đang gửi ảnh (${Math.round(blob.size/1024)} KB)…`);
    const duong=`xuong-inbox/${key}/${key}.${duoi}`;
    await ghPutAnh(duong,b64,false);
    ghHienTT(tt,'ok',`✅ Đã gửi <code>${key}.${duoi}</code>. Hệ thống tự ghép vào game trong ~1–2 phút; `+
      `tải lại trang này để xem thẻ chuyển “đã có”.`);
    o.classList.remove('act');
    o._file=null;
    const xem=o.querySelector('.gui-xem'); if(xem){ xem.hidden=true; xem.removeAttribute('src'); }
    const nhac=o.querySelector('.gui-nhac'); if(nhac) nhac.hidden=false;
    const inp=o.parentElement.querySelector('input[type=file]'); if(inp) inp.value='';
    O_DANG_CHON=null;
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Không gửi được: ${e}`);
    nut.disabled=false;
    return;
  }
}

khoiTaoO();
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
