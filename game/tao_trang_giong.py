"""Sinh trang tra giọng NPC cho điện thoại — docs/nhap/giong-nhan-vat.html

Đọc thẳng từ PROMPT và bảng trong lap_bang_giong.py, nên trang không bao giờ
lệch với prompt thật.
"""
import html
import io
import sys

sys.path.insert(0, "game")
import lap_bang_giong as L
import prompt_am

THOAI = prompt_am.PROMPT
CANH_CUA = L.lap()


def ten_canh(ma):
    return ma.replace("_", " ")


def the_nhan_vat(nguoi, ds_canh):
    o = []
    o.append(f'<section class="nv" id="{nguoi["ma"]}">')
    o.append(
        f'<h2>{html.escape(nguoi["ten"])}'
        f'<span class="dem">{len(ds_canh)} cảnh</span></h2>'
    )
    o.append(
        '<p class="tt"><span class="nhan">Tuổi</span> '
        f'{html.escape(nguoi["tuoi"])} · <span class="nhan">Giới</span> '
        f'{html.escape(nguoi["gioi"])}</p>'
    )
    o.append(f'<p class="mt">{html.escape(nguoi["mo_ta"])}</p>')

    o.append('<p class="nhan">Câu dùng trong prompt</p>')
    o.append(f'<p class="cau">{html.escape(nguoi["chuan"])}</p>')

    if nguoi["bien_the"]:
        o.append('<p class="nhan">Đổi đuôi theo tình huống</p>')
        o.append('<ul class="bt">')
        for nhan, cau in nguoi["bien_the"]:
            o.append(f"<li><b>{html.escape(nhan)}</b><br>{html.escape(cau)}</li>")
        o.append("</ul>")

    if ds_canh:
        o.append('<p class="nhan">Cảnh có lời người này</p>')
        o.append('<div class="ds">')
        for c in ds_canh:
            o.append(f'<span class="ma">{html.escape(c)}</span>')
        o.append("</div>")
    else:
        o.append('<p class="mt trong">Chương một chưa có cảnh nào.</p>')
    o.append("</section>")
    return "\n".join(o)


def sinh():
    tong = len(THOAI)
    co_thoai = sum(1 for v in THOAI.values() if "「" in v)
    dem = sorted(
        ((len(v), k) for k, v in CANH_CUA.items()), reverse=True
    )
    muc_luc = "".join(
        f'<a href="#{n["ma"]}">{html.escape(n["ten"])}'
        f'<span class="n2">{len(CANH_CUA[n["ma"]])}</span></a>'
        for _, k in dem
        for n in L.NHAN_VAT
        if n["ma"] == k
    )

    than = "\n".join(
        the_nhan_vat(n, CANH_CUA[n["ma"]])
        for _, k in dem
        for n in L.NHAN_VAT
        if n["ma"] == k
    )

    return f"""<!doctype html>
<html lang="vi">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Giọng nhân vật — tra nhanh</title>
<style>
 :root{{--n:#17202b;--m:#5c6b7a;--v:#e6ecf3;--x:#0f6b3f;--nen:#fbfcfe}}
 *{{box-sizing:border-box}}
 body{{margin:0 auto;padding:16px 14px 60px;max-width:720px;font:16.5px/1.62
   -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--n);background:var(--nen)}}
 h1{{font-size:22px;line-height:1.3;margin:4px 0 6px}}
 .dan{{color:var(--m);font-size:14.5px;margin:0 0 18px}}
 .so{{display:flex;gap:8px;margin:0 0 20px}}
 .so div{{flex:1;background:#fff;border:1px solid var(--v);border-radius:9px;padding:9px 4px;text-align:center}}
 .so b{{display:block;font-size:21px;line-height:1.2}}
 .so span{{font-size:11.5px;color:var(--m);line-height:1.25;display:block}}
 .ml{{background:#fff;border:1px solid var(--v);border-radius:11px;padding:6px;margin:0 0 22px}}
 .ml a{{display:flex;justify-content:space-between;align-items:center;padding:9px 10px;
   border-radius:7px;color:var(--n);text-decoration:none;font-size:15px}}
 .ml a:active{{background:#eef3f8}}
 .ml .n2{{color:var(--m);font-size:13px;background:#eef2f7;border-radius:20px;
   padding:1px 8px;min-width:26px;text-align:center}}
 .nv{{background:#fff;border:1px solid var(--v);border-radius:13px;padding:14px 15px 16px;
   margin:0 0 14px;scroll-margin-top:12px}}
 .nv h2{{font-size:18.5px;margin:0 0 6px;display:flex;justify-content:space-between;
   align-items:baseline;gap:10px;line-height:1.3}}
 .dem{{font-size:12px;color:var(--m);font-weight:500;white-space:nowrap}}
 .tt{{margin:0 0 2px;font-size:14.5px;color:#33414f}}
 .mt{{margin:0 0 12px;font-size:14px;color:var(--m)}}
 .mt.trong{{margin:6px 0 0;font-style:italic}}
 .nhan{{font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
   color:var(--m);margin:12px 0 5px}}
 .cau{{margin:0;background:#0f1a24;color:#e8f0f7;padding:10px 12px;border-radius:8px;
   font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;overflow-x:auto;
   white-space:pre-wrap;word-break:break-word}}
 ul.bt{{list-style:none;margin:0;padding:0;font-size:14px}}
 ul.bt li{{background:#f4f7fa;border-radius:7px;padding:7px 10px;margin:0 0 5px;line-height:1.45}}
 ul.bt b{{color:#33414f;font-size:13px}}
 .ds{{display:flex;flex-wrap:wrap;gap:5px;margin-top:2px}}
 .ma{{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef2f7;
   color:#26333f;padding:2px 7px;border-radius:5px}}
 .cuoi{{margin:26px 0 0;padding-top:16px;border-top:1px solid var(--v);color:var(--m);font-size:13.5px}}
 code{{background:#eef2f7;padding:1px 5px;border-radius:4px;font-size:13.5px}}
</style>

<h1>Giọng nhân vật — tra nhanh</h1>
<p class="dan">Bảng này đọc thẳng từ prompt thật, nên không bao giờ lệch. Muốn biết
một NPC giọng thế nào thì tìm tên ở đây.</p>

<div class="so">
 <div><b>{len(L.NHAN_VAT)}</b><span>nhân vật</span></div>
 <div><b>{tong}</b><span>cảnh</span></div>
 <div><b>{co_thoai}</b><span>cảnh có thoại</span></div>
</div>

<nav class="ml">{muc_luc}</nav>

{than}

<p class="cuoi">Tệp gốc: <code>game/GIONG_NPC.md</code>. Sinh lại trang bằng
<code>python3 game/tao_trang_giong.py</code> sau khi sửa prompt.</p>
</html>
"""


if __name__ == "__main__":
    noi_dung = sinh()
    io.open("docs/nhap/giong-nhan-vat.html", "w", encoding="utf-8").write(noi_dung)
    print(f"da sinh docs/nhap/giong-nhan-vat.html {len(noi_dung)} bytes")
