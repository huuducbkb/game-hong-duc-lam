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
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import xuong_video as V  # noqa: E402

REPO = "huuducbkb/game-hong-duc-lam"
OUT = os.path.join(ROOT, "docs", "xuong-video", "index.html")
UPLOAD_URL = f"https://github.com/{REPO}/upload/main/docs/assets/video"
XEM_TRUOC = os.path.join(ROOT, "docs", "xuong-video", "xem-truoc.mp4")
INTRO_MP4 = os.path.join(ROOT, "docs", "assets", "video", "intro.mp4")


def _o_gui(c: dict) -> str:
    """Ô chọn + gửi ảnh cho một cảnh (giống Xưởng ảnh).

    Ô là <label> bọc <input type=file> phủ toàn bộ → chạm là mở thư viện ảnh trên
    iPad/iPhone. Ảnh được nén ngay trên máy rồi đẩy thẳng lên GitHub, không cần
    mở Issue, không cần terminal.
    """
    k = c["key"]
    return f"""
  <div class="gui-o" data-key="{k}" data-file="{c['file']}">
    <label class="gui-dan" data-key="{k}" tabindex="0"
           title="Bấm để chọn ảnh trong thư viện ảnh, hoặc dán/kéo thả ảnh">
      <input class="gui-file" type="file" accept="image/*">
      <span class="gui-nhac">📷 Bấm vào đây để chọn ảnh</span>
      <img class="gui-xem" alt="" hidden>
    </label>
    <div class="gui-hang">
      <button class="gui-gui" type="button" disabled>📤 Gửi ảnh này</button>
      <button class="gui-kt" type="button"
              title="Xem ảnh đã lên trang chưa — không cần tải lại">🔄 Kiểm tra</button>
    </div>
    <div class="gui-tt" hidden></div>
    <img class="gui-game" alt="" hidden>
  </div>"""


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
  {_o_gui(c)}
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


def _canh_json() -> str:
    """Danh sách cảnh cho JS: mã + tên file + tên, để khớp ảnh theo tên file."""
    ds = [{"k": c["key"], "f": c["file"], "ten": c.get("ten_en") or c["ten"]}
          for c in V.CANH_VIDEO]
    # "</" phải thoát, nếu không thẻ </script> trong chuỗi sẽ cắt sớm khối JS.
    return json.dumps(ds, ensure_ascii=False).replace("</", "<\\/")


def _xem_truoc() -> str:
    """Khối xem trước: video dựng tự động từ 14 ảnh, chỉ hiện khi đã có file."""
    if not os.path.exists(XEM_TRUOC):
        return ""
    if not all(V.da_co(c) for c in V.CANH_VIDEO):
        return ""
    return f"""
<h2>🎬 Xem trước</h2>
<div class="card">
  <p class="mota">Dựng tự động từ <b>14 ảnh</b> theo đúng timecode và chuyển động camera
  trong bảng bên dưới — <b>{V.mmss(V.tong_giay())}</b>, 720×1280, chưa có nhạc.
  Đây là bản nháp để bạn duyệt bố cục và nhịp; bản cuối dựng trong CapCut sẽ nét hơn
  và có nhạc.</p>
  <video controls playsinline preload="metadata" width="100%"
         style="border-radius:10px;border:1px solid var(--line);display:block;background:#000">
    <source src="xem-truoc.mp4" type="video/mp4">
    Trình duyệt không phát được video. <a href="xem-truoc.mp4">Tải về</a>.
  </video>
  <div class="row">
    <a class="dl" href="xem-truoc.mp4" download>⬇️ Tải video xem trước</a>
  </div>
</div>
"""


def _up_video() -> str:
    """Ô kéo-thả video intro. Tự chia khúc nên không giới hạn dung lượng.

    Trình duyệt chỉ gọi được api.github.com (uploads.github.com thiếu CORS), mà
    mỗi lần PUT ở đó bị trần ~30 MB (đo thật: 29 MB qua, 42 MB → 422). Vì vậy
    file được cắt thành nhiều mảnh ~8 MB, đẩy lần lượt vào xuong-video-inbox/,
    rồi workflow `ghep-video.yml` ghép lại → nén → đưa vào game → xoá mảnh.
    """
    co = os.path.exists(INTRO_MP4)
    if co:
        mb = os.path.getsize(INTRO_MP4) / 1024 / 1024
        hien_tai = (f'<div class="phim-xem"><video controls playsinline preload="metadata" '
                    f'src="../assets/video/intro.mp4"></video></div>'
                    f'<p class="mota">Đang phát bản <b>{mb:.1f} MB</b> ở đầu game. '
                    f'Thả video mới vào ô dưới để thay.</p>')
    else:
        hien_tai = ('<p class="mota">Chưa có video. Thả vào là game tự phát ở màn '
                    'giới thiệu.</p>')
    return f"""
<h2>🎬 Video intro</h2>
<div class="card">
  {hien_tai}
  <p class="mota">Xuất từ CapCut: <b>MP4 · H.264 · 1080×1920</b>. Dung lượng nào cũng
  được — trang tự cắt nhỏ để đưa lên, máy chủ tự ghép lại và nén xuống ~14 MB cho nhẹ
  khi người chơi mở game.</p>
  <label class="tha" id="tha-o" tabindex="0">
    <input type="file" id="intro-file" accept="video/mp4,video/quicktime,video/*">
    <span class="tha-icon">🎬</span>
    <span class="tha-chu">Thả video vào đây<br><small>hoặc bấm để chọn trong thư viện</small></span>
  </label>
  <div class="thanh" id="thanh" hidden><div class="thanh-ruot" id="thanh-ruot"></div></div>
  <div class="gui-tt" id="intro-tt" hidden></div>
</div>
"""


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
            .replace("__CANH_JSON__", _canh_json())
            .replace("__XEM_TRUOC__", _xem_truoc())
            .replace("__UPLOAD__", UPLOAD_URL)
            .replace("__UP_VIDEO__", _up_video()))


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
.tha{display:flex;flex-direction:column;align-items:center;gap:6px;margin-top:12px;
 padding:26px 14px;border:2px dashed var(--line);border-radius:12px;cursor:pointer;
 background:#0e1726;text-align:center;transition:border-color .15s,background .15s}
.tha:hover,.tha.hot{border-color:var(--jade);background:#101f33}
.tha:focus-visible{outline:2px solid var(--jade);outline-offset:2px}
.tha input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.tha-icon{font-size:26px;line-height:1}
.tha-chu{font-size:14px;color:var(--jade)}
.tha-chu small{color:var(--muted);font-size:12px}
.thanh{margin-top:12px;height:8px;border-radius:99px;background:#0a1220;overflow:hidden}
.thanh-ruot{height:100%;width:0;border-radius:99px;
 background:linear-gradient(90deg,var(--jade),#7fe0a8);transition:width .25s}
.phim-xem video{width:100%;max-width:300px;border-radius:10px;border:1px solid var(--line);
 display:block;background:#000}
.gui-o{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:10px;background:#0e1726}
.gui-dan{display:block;position:relative;border:2px dashed var(--line);border-radius:9px;
  padding:18px 12px;text-align:center;color:var(--muted);cursor:pointer}
.gui-dan:hover,.gui-dan.act{border-color:var(--jade);color:var(--jade)}
.gui-file{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;
  -webkit-appearance:none;font-size:0}
.gui-nhac,.gui-xem{pointer-events:none}
.gui-xem{max-width:100%;max-height:260px;border-radius:8px;display:block;margin:0 auto}
.gui-gui{flex:1;background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600}
.gui-gui:disabled{opacity:.45;cursor:not-allowed}
.gui-hang{display:flex;gap:8px;margin-top:8px}
.gui-kt{flex:0 0 auto;background:#1d2b45;color:var(--jade);border:1px solid #4a628c;
  font-size:13px;font-weight:600}
.gui-kt:hover{background:#243757;border-color:var(--jade)}
.gui-kt.dang{opacity:.6;cursor:wait}
.gui-game{max-width:100%;max-height:280px;border-radius:8px;display:block;margin:8px auto 0;
  border:1px solid var(--line)}
.gui-tt{margin-top:7px;font-size:12.5px}
.gui-tt .ok,.gui-tt .warn,.gui-tt .muted{display:block;padding:8px 10px;border-radius:8px}
.gui-tt .ok{background:#12351f;color:#7fe0a8}
.gui-tt .warn{background:#2a150d;color:#ffb98a}
.gui-tt .muted{background:#0a1220;color:var(--muted)}
.hang-loat{margin-top:10px}
.hang-loat .gui-dan{padding:26px 12px}
.lo-ds{margin:8px 0 0;font-size:12.5px;color:var(--muted)}
.lo-ds div{padding:3px 0;border-bottom:1px solid #1a2740}
.lo-ds .ok{color:#7fe0a8}
.lo-ds .warn{color:#ffb98a}
</style>
</head>
<body>

<h1>Xưởng video</h1>
<p class="muted">Hồng Đức Tu Tiên Lộ · trailer intro <b>__GIAY__ giây</b> (<b>__MMSS__</b>) ·
<b>__TONG__</b> cảnh · đã có <b>__DA_CO__</b>, còn thiếu <b>__CON__</b>.</p>

__XEM_TRUOC__

__UP_VIDEO__

<h2>⚡ Cách làm</h2>
<div class="card">
  <ol class="steps">
    <li><b>Kết nối GitHub</b> (một lần): dán token ở mục <b>🔑 Kết nối GitHub</b> bên dưới.</li>
    <li><b>Vẽ ảnh</b>: bấm <b>📋 Copy prompt tổng</b> (một lần cho cả 14 ảnh) hoặc copy
        prompt từng cảnh. Dán vào AI tạo ảnh. <b>Tỉ lệ bắt buộc 9:16 dọc</b> — không phải 3:4.</li>
    <li><b>Gửi ảnh</b>: ngay trên mỗi thẻ cảnh có ô <b>📷 Bấm vào đây để chọn ảnh</b> —
        chọn ảnh trong thư viện, bấm <b>📤 Gửi ảnh này</b>. Hệ thống nén ngay trên máy bạn
        rồi tự đưa lên đúng tên file, <b>không cần đặt tên, không cần mở Issue</b>.</li>
    <li><b>Dựng trong CapCut</b>: theo bảng thời gian bên dưới — mỗi cảnh đúng số giây,
        camera theo cột "camera", chuyển cảnh theo cột "chuyển cảnh".</li>
    <li><b>Xuất file</b>: MP4, H.264, 1080×1920, 30fps, 8–10 Mbps, <b>dưới 15 MB</b>.</li>
  </ol>
  <p class="muted" style="font-size:12.5px">Ảnh trailer <b>không dùng chung</b> với ảnh trong game.
  Ảnh game là thẻ 3:4 chừa chỗ cho chữ; ảnh trailer là khung 9:16 điện ảnh.
  Cắt ảnh game ra làm trailer sẽ mất bố cục và lộ khung.</p>
</div>

<h2>🔑 Kết nối GitHub</h2>
<div class="card">
  <p class="mota">Cần một lần duy nhất. Token chỉ lưu trong trình duyệt của bạn
  (<code>localStorage</code>), không gửi đi đâu khác ngoài GitHub.</p>
  <p class="mota">Tạo token: GitHub → <b>Settings → Developer settings → Personal access tokens
  → Fine-grained tokens</b> → chọn repo <code>huuducbkb/game-hong-duc-lam</code> →
  quyền <b>Contents: Read and write</b>.</p>
  <input id="gh-token" type="password" placeholder="Dán token vào đây"
         style="width:100%;font-size:14px;padding:11px;border-radius:9px;
                border:1px solid var(--line);background:#0a1220;color:var(--ink)">
  <div class="row">
    <button class="cp" type="button" onclick="ghLuuToken()">💾 Lưu token</button>
    <button class="dl" type="button" onclick="ghQuenToken()">🗑 Quên token</button>
  </div>
  <div class="gui-tt" id="gh-tt" hidden></div>
</div>

<h2>📤 Gửi cả loạt ảnh</h2>
<div class="card">
  <p class="mota">Chọn nhiều ảnh một lúc. Hệ thống lấy <b>tên file</b> để biết ảnh nào là cảnh nào —
  nên đặt tên đúng như thẻ ghi (<code>v01_pham_nhan.jpg</code>…), hoặc đổi tên ngay trên
  iPad trước khi chọn. Ảnh không khớp tên sẽ được báo lại để gửi riêng.</p>
  <div class="gui-o hang-loat">
    <label class="gui-dan" tabindex="0">
      <input class="gui-file" id="lo-file" type="file" accept="image/*" multiple>
      <span class="gui-nhac">📷 Bấm để chọn nhiều ảnh cùng lúc</span>
    </label>
    <div class="gui-hang">
      <button class="gui-gui" type="button" id="lo-gui" disabled>📤 Gửi tất cả</button>
    </div>
    <div class="gui-tt" id="lo-tt" hidden></div>
    <div class="lo-ds" id="lo-ds"></div>
  </div>
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
/* ===== Danh sách cảnh (sinh từ Python, khớp đúng mã + tên file) ===== */
const CANH = __CANH_JSON__;

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

/* ================= Kết nối GitHub (token lưu trong máy) ================= */
const GH_REPO='huuducbkb/game-hong-duc-lam';
const GH_BRANCH='main';
const GH_LS='xuong_video_gh_token';
const VIDEO_DIR='docs/assets/video/';

function ghToken(){ return localStorage.getItem(GH_LS)||''; }

function ghHienTT(el, loai, html){
  if(!el) return;
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
    if(!r.ok){
      ghHienTT(tt,'warn',`⚠️ Token không dùng được (HTTP ${r.status}). Kiểm tra lại quyền Contents: Read and write.`);
      return;
    }
    const j=await r.json();
    if(j.permissions && j.permissions.push === false){
      ghHienTT(tt,'warn','⚠️ Token chưa có quyền ghi (cần Contents: Read and write). Tạo lại token rồi thử lại.');
      return;
    }
    localStorage.setItem(GH_LS,t);
    ghHienTT(tt,'ok',`✅ Đã kết nối <b>${j.full_name}</b>. Từ giờ chọn ảnh ở thẻ cảnh rồi bấm Gửi là xong.`);
  }catch(e){ ghHienTT(tt,'warn',`⚠️ Lỗi kết nối: ${e}`); }
}

function ghQuenToken(){
  localStorage.removeItem(GH_LS);
  const inp=document.getElementById('gh-token'); if(inp) inp.value='';
  ghHienTT(document.getElementById('gh-tt'),'muted','Đã quên token trong trình duyệt này.');
}

/* Nén ngay trên máy. Ảnh trailer cần dọc 9:16 nên giữ cạnh dài tối đa 1920.
   Không cắt, không ép tỉ lệ — server đệm khung 1080x1920 để không méo mặt. */
function ghNenAnh(file, maxCanh=1920, q=0.9){
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
      cv.toBlob(b=>b?res({blob:b,duoi:'jpg'}):rej(new Error('nén lỗi')),'image/jpeg',q);
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

/* Đẩy ảnh lên xuong-inbox/<mã>/<mã>.jpg — thư mục con = mã cảnh, nên bot gán
   thẳng không cần AI đoán. Đặt ở inbox (không phải docs/assets/video) là cố ý:
   chỉ push vào xuong-inbox mới kích hoạt workflow dựng lại trang + cập nhật
   trạng thái đã có/còn thiếu. */
async function ghPutAnh(duong, b64){
  const t=ghToken();
  const laVideo=['.mp4','.webm','.mov'].some(d=>duong.toLowerCase().endsWith(d));
  const body={message:laVideo?`Xưởng video: cập nhật ${duong.split('/').pop()}`
                            :`Xưởng video: thêm ảnh ${duong.split('/').slice(-2)[0]}`,
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
  return true;
}

/* ================= Video intro: kéo-thả, tự chia khúc ================= */
/* Trình duyệt chỉ gọi được api.github.com — uploads.github.com (Release asset)
   không trả header CORS, đã kiểm tra bằng preflight OPTIONS. Mà mỗi PUT ở
   api.github.com bị trần ~30 MB (đo thật: 29.1 MB qua, 42.5 MB → 422 "too
   large", 61.6 MB → 504). Nên file lớn được cắt thành mảnh 8 MB, đẩy vào
   xuong-video-inbox/, workflow ghep-video.yml ghép lại rồi nén.
   Mảnh 8 MB: base64 phình 1/3 → ~11 MB, dưới trần 30 MB rất xa. */
const MANH_MB = 8;
const INBOX = 'xuong-video-inbox';

(function thaVideo(){
  const o = document.getElementById('tha-o');
  if(!o) return;
  const inp = document.getElementById('intro-file');
  const thanh = document.getElementById('thanh');
  const ruot = document.getElementById('thanh-ruot');
  const tt = document.getElementById('intro-tt');
  let dangGui = false;

  function veThanh(p){
    thanh.hidden = false;
    ruot.style.width = Math.round(p*100) + '%';
  }

  async function gui(file){
    if(dangGui) return;
    if(!ghToken()){
      ghHienTT(tt,'warn','⚠️ Chưa kết nối GitHub. Dán token ở mục <b>🔑 Kết nối GitHub</b> phía trên rồi thả lại.');
      return;
    }
    dangGui = true;
    const mb = file.size/1024/1024;
    const duoi = (file.name.split('.').pop()||'mp4').toLowerCase();
    // Mã lô = thời gian + ngẫu nhiên: nhiều lần thả không đè lên nhau.
    const lo = Date.now().toString(36) + Math.random().toString(36).slice(2,6);
    const co = Math.max(1, Math.ceil(file.size/(MANH_MB*1024*1024)));
    try{
      ghHienTT(tt,'muted',`Đang đưa lên: <b>${file.name}</b> — ${mb.toFixed(1)} MB, chia ${co} phần. Đừng đóng tab.`);
      for(let k=0;k<co;k++){
        const dau = k*MANH_MB*1024*1024;
        const manh = file.slice(dau, Math.min(file.size, dau+MANH_MB*1024*1024));
        const b64 = await blobB64(manh);
        // Tên mảnh có số thứ tự 5 chữ số để ghép đúng thứ tự.
        const ten = `${lo}-${String(k).padStart(5,'0')}.part`;
        await ghPutAnh(`${INBOX}/${ten}`, b64);
        veThanh((k+1)/co*0.9);
        ghHienTT(tt,'muted',`Đang đưa lên: phần ${k+1}/${co} — ${Math.round((k+1)/co*100)}%. Đừng đóng tab.`);
      }
      // Mẩu tin cuối: báo tổng số mảnh + tên gốc. Workflow chỉ chạy khi thấy nó,
      // nhờ vậy không ghép khi còn mảnh đang lên.
      const tin = {lo, co, ten: file.name, duoi, bytes: file.size};
      await ghPutAnh(`${INBOX}/${lo}.json`, await blobB64(
        new Blob([JSON.stringify(tin)],{type:'application/json'})));
      veThanh(1);
      ghHienTT(tt,'ok',`✅ Đã đưa lên xong (${co} phần). Máy chủ đang ghép lại và nén — `
        + `khoảng 2–3 phút nữa video mới hiện trong game. Theo dõi ở tab Actions nếu muốn.`);
    }catch(e){
      ghHienTT(tt,'warn',`⚠️ Gửi lỗi: ${e}. Thả lại để thử lại từ đầu.`);
      dangGui = false;
      return;
    }
    dangGui = false;
  }

  // Kéo thả
  ['dragenter','dragover'].forEach(t=>o.addEventListener(t, e=>{
    e.preventDefault(); o.classList.add('hot');
  }));
  ['dragleave','drop'].forEach(t=>o.addEventListener(t, e=>{
    e.preventDefault(); o.classList.remove('hot');
  }));
  o.addEventListener('drop', e=>{
    const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if(f) gui(f);
  });
  inp.addEventListener('change', ()=>{
    const f = inp.files && inp.files[0];
    if(f) gui(f);
  });
  // Bấm phím Enter/Space trên ô cũng mở hộp chọn file (bàn phím).
  o.addEventListener('keydown', e=>{
    if(e.key==='Enter'||e.key===' '){ e.preventDefault(); inp.click(); }
  });
})();

/* ================= Ô chọn ảnh dưới mỗi cảnh ================= */
let O_DANG_CHON=null;

function datAnhVaoO(o, file){
  if(!file || !file.type.startsWith('image/')) return;
  const hop=o.parentElement;
  const xem=o.querySelector('.gui-xem');
  const nhac=o.querySelector('.gui-nhac');
  const nut=hop.querySelector('.gui-gui');
  const tt=hop.querySelector('.gui-tt');
  o._file=file;
  xem.src=URL.createObjectURL(file); xem.hidden=false;
  if(nhac) nhac.hidden=true;
  o.classList.add('act');
  if(nut) nut.disabled=false;
  if(tt){ tt.hidden=true; tt.innerHTML=''; }
}

async function kiemTraAnh(hop, imLang){
  const tenFile=hop.dataset.file;
  const tt=hop.querySelector('.gui-tt');
  const nut=hop.querySelector('.gui-kt');
  const im=hop.querySelector('.gui-game');
  if(nut) nut.classList.add('dang');
  if(!imLang) ghHienTT(tt,'muted','Đang kiểm tra trên GitHub…');
  try{
    const t=ghToken();
    const r=await fetch(
      `https://api.github.com/repos/${GH_REPO}/commits?path=${VIDEO_DIR}${tenFile}&per_page=1`,
      {headers:t?{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}
                :{'Accept':'application/vnd.github+json'}});
    if(r.status===403 || r.status===429) throw new Error('GitHub tạm giới hạn lượt gọi — chờ chút rồi thử lại');
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const ds=await r.json();
    if(!Array.isArray(ds) || !ds.length){
      im.hidden=true; im.removeAttribute('src');
      ghHienTT(tt,'muted','⬜ Chưa có trên trang. Gửi ảnh rồi bấm 🔄 Kiểm tra lại (bot cần ~1–2 phút).');
      return {co:false};
    }
    const sha=ds[0].sha;
    im.src=`https://raw.githubusercontent.com/${GH_REPO}/${sha}/${VIDEO_DIR}${tenFile}`;
    im.hidden=false;
    const the=hop.closest('article');
    if(the){
      the.classList.add('done');
      const nh=the.querySelector('header .badge');
      if(nh){ nh.className='badge chac'; nh.textContent='✅ đã có'; }
    }
    const khi=new Date(ds[0].commit.author.date);
    const gio=isNaN(khi)?ds[0].commit.author.date
      :khi.toLocaleString('vi-VN',{hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'});
    ghHienTT(tt,'ok',`✅ Đã lên trang · ${gio} · <code>${sha.slice(0,7)}</code> — ảnh dưới là bản đang dùng.`);
    return {co:true};
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Không kiểm tra được: ${e}`);
    return {co:null};
  }finally{
    if(nut) nut.classList.remove('dang');
  }
}

/* Sau khi gửi: tự dò vài lần, người dùng không phải bấm gì. */
async function theoDoiAnh(hop){
  const tt=hop.querySelector('.gui-tt');
  for(let lan=1; lan<=10; lan++){
    await new Promise(r=>setTimeout(r, 15000));
    const kq=await kiemTraAnh(hop, true);
    if(kq.co){ ghHienTT(tt,'ok','🎉 Ảnh đã lên trang! (xem ảnh dưới)'); return; }
    if(kq.co===null) return;
    if(lan<10) ghHienTT(tt,'muted',
      `⏳ Bot đang xử lý… tự kiểm tra lại sau 15 giây (lần ${lan}/10). Cứ để trang mở.`);
  }
  ghHienTT(tt,'muted','⏳ Lâu hơn thường lệ. Bấm 🔄 Kiểm tra để thử lại.');
}

async function guiMotAnh(o, nut){
  const key=o.dataset.key;
  const tt=o.parentElement.querySelector('.gui-tt');
  const file=o._file;
  if(!ghToken()){
    ghHienTT(tt,'warn','⚠️ Chưa kết nối GitHub. Dán token ở mục <b>🔑 Kết nối GitHub</b> rồi thử lại.');
    return;
  }
  if(!file){ ghHienTT(tt,'warn','⚠️ Chưa có ảnh. Bấm vào ô để chọn ảnh.'); return; }
  nut.disabled=true;
  ghHienTT(tt,'muted','Đang nén ảnh…');
  try{
    const {blob,duoi}=await ghNenAnh(file);
    const b64=await blobB64(blob);
    ghHienTT(tt,'muted',`Đang gửi ảnh (${Math.round(blob.size/1024)} KB)…`);
    await ghPutAnh(`xuong-inbox/${key}/${key}.${duoi}`, b64);
    ghHienTT(tt,'ok',`✅ Đã gửi. Bot sẽ tự đưa ảnh vào đúng cảnh — trang tự báo khi xong.`);
    o.classList.remove('act');
    o._file=null;
    const xem=o.querySelector('.gui-xem'); if(xem){ xem.hidden=true; xem.removeAttribute('src'); }
    const nhac=o.querySelector('.gui-nhac'); if(nhac) nhac.hidden=false;
    const inp=o.parentElement.querySelector('input[type=file]'); if(inp) inp.value='';
    O_DANG_CHON=null;
    nut.disabled=true;
    theoDoiAnh(o.parentElement);
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Không gửi được: ${e}`);
    nut.disabled=false;
  }
}

/* ================= Gửi cả loạt ================= */
function canhTheoTen(ten){
  const t=(ten||'').toLowerCase();
  for(const c of CANH){
    if(t===c.f.toLowerCase()) return c;
  }
  for(const c of CANH){
    if(t.includes(c.k)) return c;
  }
  return null;
}

let LO_FILES=[];

function khoiTaoLo(){
  const inp=document.getElementById('lo-file');
  const nut=document.getElementById('lo-gui');
  const ds=document.getElementById('lo-ds');
  const tt=document.getElementById('lo-tt');
  if(!inp) return;
  inp.addEventListener('change',()=>{
    LO_FILES=[];
    ds.innerHTML='';
    for(const f of inp.files){
      const c=canhTheoTen(f.name);
      const d=document.createElement('div');
      d.innerHTML = c
        ? `<span class="ok">✅</span> ${f.name} → <code>${c.k}</code> ${c.ten?('· '+c.ten):''}`
        : `<span class="warn">⚠️</span> ${f.name} — không khớp cảnh nào (đổi tên thành <code>v01_pham_nhan.jpg</code>…)`;
      ds.appendChild(d);
      LO_FILES.push({file:f, canh:c, hang:d});
    }
    const khop=LO_FILES.filter(x=>x.canh).length;
    nut.disabled = khop===0;
    nut.textContent = khop ? `📤 Gửi ${khop} ảnh khớp` : '📤 Gửi tất cả';
    if(tt) tt.hidden=true;
  });
  nut.addEventListener('click', async ()=>{
    if(!ghToken()){
      ghHienTT(tt,'warn','⚠️ Chưa kết nối GitHub. Dán token ở mục <b>🔑 Kết nối GitHub</b> rồi thử lại.');
      return;
    }
    const dsKhop=LO_FILES.filter(x=>x.canh);
    if(!dsKhop.length) return;
    nut.disabled=true;
    let ok=0, loi=0;
    for(let i=0;i<dsKhop.length;i++){
      const {file,canh,hang:d}=dsKhop[i];
      ghHienTT(tt,'muted',`Đang gửi ${i+1}/${dsKhop.length}: <code>${canh.k}</code>…`);
      try{
        const {blob}=await ghNenAnh(file);
        const b64=await blobB64(blob);
        await ghPutAnh(`xuong-inbox/${canh.k}/${canh.k}.jpg`, b64);
        ok++;
        if(d) d.innerHTML=`<span class="ok">✅</span> ${file.name} → <code>${canh.k}</code> · đã gửi`;
      }catch(e){
        loi++;
        if(d) d.innerHTML=`<span class="warn">⚠️</span> ${file.name} → <code>${canh.k}</code> · lỗi: ${e}`;
      }
    }
    ghHienTT(tt, loi?'warn':'ok',
      `${loi?'⚠️':'🎉'} Đã gửi ${ok} ảnh${loi?`, ${loi} ảnh lỗi`:''}. `+
      `Bot cần ~1–2 phút để ghép. Mở thẻ cảnh bấm <b>🔄 Kiểm tra</b> để xem, hoặc tải lại trang sau 2 phút.`);
    nut.disabled=false;
  });
}

function khoiTaoO(){
  document.querySelectorAll('.gui-dan').forEach(o=>{
    const hop=o.parentElement;
    const inp=o.querySelector('input[type=file]');
    const nut=hop.querySelector('.gui-gui');
    const kt=hop.querySelector('.gui-kt');
    if(!o.dataset.key) return;   // ô gửi cả loạt xử lý riêng
    o.addEventListener('click',()=>{ O_DANG_CHON=o; });
    o.addEventListener('focus',()=>{ O_DANG_CHON=o; });
    if(inp) inp.addEventListener('change',()=>{ if(inp.files[0]) datAnhVaoO(o,inp.files[0]); });
    if(nut) nut.addEventListener('click',()=>guiMotAnh(o,nut));
    if(kt) kt.addEventListener('click',()=>kiemTraAnh(hop, false));
  });
  document.addEventListener('paste',e=>{
    const it=e.clipboardData&&e.clipboardData.items;
    if(!it) return;
    let f=null;
    for(const x of it){ if(x.type.startsWith('image/')){ f=x.getAsFile(); break; } }
    if(!f) return;
    const o=O_DANG_CHON || document.querySelector('.gui-dan.act');
    if(!o || !o.dataset.key) return;
    e.preventDefault();
    datAnhVaoO(o,f);
  });
}

document.addEventListener('DOMContentLoaded',()=>{
  const inp=document.getElementById('gh-token');
  if(inp && ghToken()) inp.value=ghToken();
  khoiTaoO();
  khoiTaoLo();
});
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
