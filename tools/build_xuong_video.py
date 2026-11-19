#!/usr/bin/env python3
"""Dựng Xưởng VIDEO tĩnh cho GitHub Pages: docs/xuong-video/index.html.

Song song với Xưởng ảnh (tools/build_xuong.py), nhưng dành cho trailer intro:
  · prompt TỔNG (14 ảnh, dán 1 lần)
  · prompt theo PHẦN (mở / tiên giới / sức mạnh / mất mát / kết)
  · prompt từng CẢNH, kèm timecode, chuyển động camera, chữ trên hình
  · prompt NHẠC
  · bảng dựng CapCut + thông số xuất file

Chạy: python3 tools/build_xuong_video.py
"""

from __future__ import annotations

import html as H
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import xuong_video as V  # noqa: E402

REPO = "huuducbkb/game-hong-duc-lam"
OUT = os.path.join(ROOT, "docs", "xuong-video", "index.html")
UPLOAD_URL = f"https://github.com/{REPO}/upload/main/docs/assets/video"


def _the_canh(c: dict) -> str:
    moc = V.moc_thoi_gian()[c["key"]]
    co = V.da_co(c)
    sid = "c-" + c["key"]
    tid = sid + "-t"
    aid = sid + "-a"
    nhan = ("<span class='badge chac'>✅ đã có</span>" if co
            else "<span class='badge thieu'>⬜ còn thiếu</span>")
    anh = (f'<img class="xem" src="../assets/video/{c["file"]}" alt="" loading="lazy">'
           if co else "")
    chu = (f'<div class="chu"><span class="k">chữ trên hình</span> {H.escape(c["chu"])}</div>'
           if c.get("chu") else '<div class="chu"><span class="k">chữ trên hình</span> —</div>')
    return f"""
<article class="canh{' done' if co else ''}" id="{sid}">
  <header>
    <span class="so">{moc['bat_dau']}–{moc['ket_thuc']}</span>
    <b>{H.escape(c['ten'])}</b>
    {nhan}
    <span class="ratio">{c['giay']}s</span>
  </header>
  <div class="meta">
    <div><span class="k">mã</span> <code>{c['key']}</code></div>
    <div><span class="k">lưu là</span> <code>{c['file']}</code></div>
    <div><span class="k">camera</span> {H.escape(c['chuyen_dong'])}</div>
    <div><span class="k">chuyển cảnh</span> {H.escape(c['chuyen_canh'])}</div>
  </div>
  {chu}
  {anh}
  <textarea readonly rows="6" id="{tid}">{H.escape(V.prompt_canh(c))}</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('{tid}', this)">📋 Copy prompt ảnh</button>
    <button class="dl" onclick="taiTxt('{tid}', '{c['key']}.txt')">⬇️ .txt</button>
  </div>
  <details class="phu">
    <summary>🎬 Prompt chuyển động (nếu bạn dùng công cụ ảnh → video)</summary>
    <textarea readonly rows="4" id="{aid}">{H.escape(V.prompt_am_thanh(c))}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{aid}', this)">📋 Copy prompt chuyển động</button>
    </div>
  </details>
</article>"""


def _the_phan(p: dict) -> str:
    ds = V.canh_cua_phan(p["ma"])
    con = sum(1 for c in ds if not V.da_co(c))
    pid = "phan-" + p["ma"]
    tid = pid + "-t"
    return f"""
<section class="phan" id="{pid}">
  <h2>{p['icon']} {H.escape(p['ten'])}
    <span class="dem">{len(ds) - con}/{len(ds)} đã có</span></h2>
  <p class="mota">{H.escape(p['mota'])}</p>
  <details class="gop-phan">
    <summary>📦 Prompt vẽ TOÀN BỘ phần này ({len(ds)} ảnh) — dán 1 lần cho cả phần</summary>
    <textarea readonly rows="10" id="{tid}">{H.escape(V.build_gop_prompt_phan(p['ma']))}</textarea>
    <div class="row">
      <button class="cp" onclick="cpText('{tid}', this)">📋 Copy prompt toàn phần</button>
      <button class="dl" onclick="taiTxt('{tid}', '{p['ma']}.txt')">⬇️ .txt</button>
    </div>
  </details>
  <div class="ds-anh">{"".join(_the_canh(c) for c in ds)}</div>
</section>"""


def _bang_canh() -> str:
    hang = []
    for c in V.CANH_VIDEO:
        m = V.moc_thoi_gian()[c["key"]]
        hang.append(
            f"<tr><td>{m['bat_dau']}–{m['ket_thuc']}</td><td>{c['giay']}s</td>"
            f"<td><a href='#c-{c['key']}'>{H.escape(c['ten'])}</a></td>"
            f"<td class='muted'>{H.escape(c['chuyen_dong'])}</td></tr>")
    return ("<table><thead><tr><th>thời gian</th><th>dài</th><th>cảnh</th>"
            "<th>camera</th></tr></thead><tbody>" + "".join(hang) + "</tbody></table>")


def _bang_nhac() -> str:
    return ("<table><thead><tr><th>mốc</th><th>làm gì</th></tr></thead><tbody>"
            + "".join(f"<tr><td><code>{H.escape(a)}</code></td><td>{H.escape(b)}</td></tr>"
                      for a, b, _en in V.GOI_Y_NHAC)
            + "</tbody></table>")


def _muc_luc() -> str:
    dong = []
    for p in V.PHAN_VIDEO:
        con = " · ".join(
            f'<a href="#c-{c["key"]}">{H.escape(c["ten"])}</a>'
            for c in V.canh_cua_phan(p["ma"]))
        dong.append(f"""
<div class="ml-phan">
  <a class="ml-ten" href="#phan-{p['ma']}">{p['icon']} {H.escape(p['ten'])}</a>
  <div class="ml-con">{con}</div>
</div>""")
    return "\n".join(dong)


def _con_thieu() -> str:
    thieu = [c for c in V.CANH_VIDEO if not V.da_co(c)]
    if not thieu:
        return "<p class='ok'>🎉 Đủ 14 ảnh — dựng video được rồi!</p>"
    hang = "".join(
        f"<tr><td>{V.moc_thoi_gian()[c['key']]['bat_dau']}</td>"
        f"<td><code>{c['key']}</code></td><td>{H.escape(c['ten'])}</td>"
        f"<td class='muted'><code>{c['file']}</code></td></tr>" for c in thieu)
    return ("<table><thead><tr><th>mốc</th><th>mã</th><th>cảnh</th><th>lưu là</th></tr></thead>"
            f"<tbody>{hang}</tbody></table>")


def build() -> str:
    tong = len(V.CANH_VIDEO)
    co = V.so_da_co()
    khoi = "".join(_the_phan(p) for p in V.PHAN_VIDEO)
    return (TEMPLATE
            .replace("__TONG__", str(tong))
            .replace("__DA_CO__", str(co))
            .replace("__CON__", str(tong - co))
            .replace("__GIAY__", str(V.tong_giay()))
            .replace("__MMSS__", V.mmss(V.tong_giay()))
            .replace("__MUC_LUC__", _muc_luc())
            .replace("__BANG_CANH__", _bang_canh())
            .replace("__BANG_NHAC__", _bang_nhac())
            .replace("__CON_THIEU__", _con_thieu())
            .replace("__PROMPT_TONG__", H.escape(V.build_gop_prompt_tat_ca()))
            .replace("__PROMPT_NHAC__", H.escape(V.prompt_nhac()))
            .replace("__KHOI__", khoi)
            .replace("__UPLOAD__", UPLOAD_URL))


TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xưởng video — Hồng Đức Tu Tiên Lộ</title>
<style>
:root{--bg:#111a2b;--card:#182337;--ink:#e8e6df;--muted:#93a0b8;--gold:#ffd98a;
  --jade:#6fe0c0;--line:#2b3b57;--seal:#a8352a}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);
  color:var(--ink);margin:0 auto;padding:18px;max-width:760px;line-height:1.55;-webkit-text-size-adjust:100%}
h1{font-size:20px;color:var(--gold);margin:6px 0 2px}
h2{font-size:16px;color:var(--jade);margin:30px 0 6px;display:flex;flex-wrap:wrap;
  gap:8px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:7px}
p,li,td,th{font-size:13.5px;color:#cbd4e4}
.muted{color:var(--muted)}
code{background:#0a1220;padding:1px 6px;border-radius:4px;color:var(--jade);font-size:12px}
a{color:var(--jade)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
.dem{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
.mota{font-size:12.5px;color:var(--muted);margin:4px 0 10px}
.ok{color:#7fe0a8}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:12.5px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.5px}
.phan{margin:34px 0}
.phan>h2{font-size:18px;color:var(--gold);border-bottom:2px solid var(--line);
  padding-bottom:8px;margin-top:38px}
.phan>.mota{font-size:13px;color:var(--muted);margin:6px 0 4px}
details.gop,details.gop-phan,details.phu{margin:10px 0 16px;border:1px solid var(--line);
  border-radius:10px;background:#0e1726;padding:10px 12px}
details.gop summary,details.gop-phan summary,details.phu summary{color:var(--jade);font-size:13px;
  font-weight:600;padding:2px 0;cursor:pointer}
details.gop-phan{margin:14px 0 22px;background:#101c2e;border-color:#31456a}
details.phu{margin:8px 0 0;background:#0b1420}
.ds-anh{display:flex;flex-direction:column;gap:12px}
.muc-luc{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:12px 14px;margin:14px 0}
.ml-phan{margin:9px 0}
.ml-ten{color:var(--gold);font-weight:600;font-size:13.5px;text-decoration:none}
.ml-con{font-size:12.5px;margin:3px 0 0 4px;line-height:1.9}
.ml-con a{color:#9fb2cf;text-decoration:none;border-bottom:1px dotted #3d5170}
.ml-con a:hover{color:var(--jade)}
.canh{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:13px;margin:12px 0;border-left:3px solid var(--jade)}
.canh.done{border-left-color:#2f8f5a;opacity:.78}
.canh header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:14px}
.so{font-size:11px;color:#3a2600;background:var(--gold);padding:2px 7px;border-radius:99px;font-weight:700}
.ratio{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
.badge{font-size:11px;padding:2px 8px;border-radius:99px}
.badge.chac{background:#12351f;color:#7fe0a8}
.badge.thieu{background:#2a150d;color:#ffb98a}
.meta{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12px;color:var(--muted);margin:8px 0}
.meta .k,.chu .k{color:#7f8ca3}
.chu{font-size:12.5px;margin:6px 0;color:#e4d9b8}
.xem{width:100%;max-width:240px;display:block;margin:8px 0;border-radius:8px;
  border:1px solid var(--line)}
textarea{width:100%;font-size:12.5px;line-height:1.5;background:#0a1220;color:#dfe7f5;
  border:1px solid var(--line);border-radius:8px;padding:10px;resize:vertical;
  font-family:ui-monospace,Menlo,monospace}
button{font-family:inherit;font-size:13.5px;font-weight:600;border:0;border-radius:9px;
  padding:10px 14px;cursor:pointer}
.row{display:flex;gap:8px;margin-top:8px}
.cp{flex:1;background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600}
.cp.done{background:#2f8f5a;color:#eafff3}
.dl{background:#1d2b45;color:var(--gold);border:1px solid #4a628c;padding:10px 14px;
  border-radius:9px;font-size:13px;font-weight:600;text-decoration:none;cursor:pointer}
.big{display:block;text-align:center;margin:10px 0;border-style:dashed}
.steps li{margin:7px 0}
</style>
</head>
<body>

<h1>Xưởng video</h1>
<p class="muted">Hồng Đức Tu Tiên Lộ · trailer intro <b>__GIAY__ giây</b> (<b>__MMSS__</b>) ·
<b>__TONG__</b> cảnh · đã có <b>__DA_CO__</b>, còn thiếu <b>__CON__</b>.</p>

<h2>⚡ Cách làm</h2>
<div class="card">
  <ol class="steps">
    <li><b>Vẽ ảnh</b>: bấm <b>📋 Copy prompt tổng</b> (một lần cho cả 14 ảnh) hoặc copy
        prompt từng cảnh. Dán vào AI tạo ảnh. <b>Tỉ lệ bắt buộc 9:16 dọc</b> — không phải 3:4.</li>
    <li><b>Đặt tên file đúng như thẻ ghi</b> (<code>v01_pham_nhan.jpg</code>…) rồi tải lên thư mục
        <code>docs/assets/video/</code>. Sai tên là hệ thống không nhận.</li>
    <li><b>Dựng trong CapCut</b>: theo bảng thời gian bên dưới — mỗi cảnh đúng số giây,
        camera theo cột "camera", chuyển cảnh theo cột "chuyển cảnh".</li>
    <li><b>Xuất file</b>: MP4, H.264, 1080×1920, 30fps, 8–10 Mbps, <b>dưới 15 MB</b>.</li>
  </ol>
  <a class="dl big" href="__UPLOAD__" target="_blank">📤 Mở trang tải ảnh lên docs/assets/video/</a>
  <p class="muted" style="font-size:12.5px">Ảnh trailer <b>không dùng chung</b> với ảnh trong game.
  Ảnh game là thẻ 3:4 chừa chỗ cho chữ; ảnh trailer là khung 9:16 điện ảnh.
  Cắt ảnh game ra làm trailer sẽ mất bố cục và lộ khung.</p>
</div>

<h2>🎯 Prompt TỔNG — dán 1 lần, vẽ cả 14 ảnh</h2>
<div class="card">
  <p class="mota">Dán nguyên khối này vào AI chat. Nó vẽ lần lượt từng cảnh, đúng thứ tự video.
  Nếu AI dừng giữa chừng, nhắn <b>"tiếp tục"</b> để lấy phần còn lại.</p>
  <textarea readonly rows="14" id="tong-t">__PROMPT_TONG__</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('tong-t', this)">📋 Copy prompt tổng</button>
    <button class="dl" onclick="taiTxt('tong-t', 'prompt-tong-trailer.txt')">⬇️ .txt</button>
  </div>
</div>

<h2>🎵 Prompt nhạc nền</h2>
<div class="card">
  <p class="mota">Mô tả nhạc khớp đúng nhịp 72 giây của trailer. Dùng để tìm nhạc có sẵn
  hoặc đưa cho công cụ tạo nhạc.</p>
  <textarea readonly rows="12" id="nhac-t">__PROMPT_NHAC__</textarea>
  <div class="row">
    <button class="cp" onclick="cpText('nhac-t', this)">📋 Copy prompt nhạc</button>
    <button class="dl" onclick="taiTxt('nhac-t', 'prompt-nhac.txt')">⬇️ .txt</button>
  </div>
  __BANG_NHAC__
</div>

<h2>🗺️ Mục lục</h2>
<div class="muc-luc">
__MUC_LUC__
</div>

<h2>📋 Bảng dựng — thời gian từng cảnh</h2>
<div class="card">
  <p class="mota">Cộng lại đúng <b>__GIAY__ giây</b>. Đây là bảng để dựng trong CapCut.</p>
  __BANG_CANH__
</div>

<h2>📥 Ảnh còn thiếu</h2>
<div class="card">
  __CON_THIEU__
</div>

<h2>🎨 Prompt theo phần · từng cảnh</h2>
<p class="muted" style="font-size:12.5px">Mỗi phần có prompt gộp <b>toàn phần</b>; mỗi cảnh có prompt
<b>riêng</b> kèm timecode, camera và chữ trên hình.</p>
__KHOI__

<h2>📌 Ghi chú dựng phim</h2>
<div class="card">
  <ul>
    <li><b>Nhịp</b>: chậm ở 15 giây đầu, bùng ở cảnh tiên giới (0:15), lặng trước tiêu đề (0:56).</li>
    <li><b>Cắt thẳng</b> ở các chỗ đánh dấu — đừng dùng dissolve hết, sẽ mất lực.</li>
    <li><b>Ken Burns</b>: mỗi ảnh phóng 105–118% và dịch chậm. Ảnh đứng yên trông như slide.</li>
    <li><b>Chữ</b>: font serif nét mảnh (Noto Serif, Playfair Display). Cỡ nhỏ, nhiều khoảng trống.</li>
    <li><b>Bản quyền</b>: cuối video ghi <i>"Đồng nhân lấy bối cảnh Phàm Nhân Tu Tiên."</i></li>
  </ul>
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
  const el=document.getElementById(id);
  const txt=(el.value!==undefined?el.value:el.textContent)||'';
  const blob=new Blob([txt],{type:'text/plain;charset=utf-8'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=ten||'prompt.txt';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}
</script>
</body></html>
"""


def build_va_ghi() -> str:
    """Dựng trang và ghi ra đĩa. Trả đường dẫn file."""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    os.makedirs(V.VIDEO_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    return OUT


if __name__ == "__main__":
    duong_dan = build_va_ghi()
    print(f"Đã dựng {duong_dan}")
    print(f"  {len(V.CANH_VIDEO)} cảnh · {V.tong_giay()}s · đã có {V.so_da_co()} ảnh")
