"""Sinh trang đọc cốt truyện cho điện thoại — docs/nhap/cot-truyen-chuong2.html

Đọc thẳng từ game/chapters/chuong2.json nên trang không bao giờ lệch với game.
Mỗi nhánh xuất thân in một mạch chính liền mạch, các đoạn rẽ in riêng bên dưới.
"""
import html
import json
import os
import re
import sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC, "game", "chapters", "chuong2.json")
RA = os.path.join(GOC, "docs", "nhap", "cot-truyen-chuong2.html")

TEN_NHOM = {"tan_tu": "Tán tu", "mon_phai": "Môn phái"}


def doc():
    with open(NGUON, encoding="utf-8") as f:
        return json.load(f)


def doan_van(chu):
    o = []
    for p in chu.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        an = html.escape(p)
        an = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", an)
        lop = ' class="he"' if an.startswith("👁") else ""
        o.append(f"<p{lop}>{an}</p>")
    return "\n".join(o)


def mach_chinh(D, dau):
    """Đi theo lựa chọn đầu tiên ở mỗi đoạn, tới khi hết lựa chọn."""
    ids, cur, thay = [], dau, set()
    while cur and cur in D and cur not in thay:
        thay.add(cur)
        ids.append(cur)
        lc = D[cur].get("lua_chon") or []
        if not lc:
            break
        cur = lc[0]["den"]
    return ids


def chuoi_re(D, dau, mach):
    """Các đoạn nối tiếp nhau rời khỏi mạch chính, cho tới khi quay lại."""
    ra, cur, thay = [], dau, set()
    while cur in D and cur not in mach and cur not in thay:
        thay.add(cur)
        ra.append(cur)
        lc = D[cur].get("lua_chon") or []
        cur = lc[0]["den"] if lc else None
    return ra


def the_doan(D, ma):
    d = D[ma]
    anh = (d.get("hinh_anh") or {}).get("anh")
    o = [f'<article class="doan" id="{ma}">']
    if anh:
        o.append(f'<img src="../assets/scene/{html.escape(anh)}" alt="" loading="lazy">')
    if d.get("boi_canh"):
        o.append(f'<p class="canh">{html.escape(d["boi_canh"])}</p>')
    o.append(doan_van(d.get("ke") or ""))
    return "\n".join(o) + "</article>"


def nhan_chon(chu):
    """Lời chọn đã có ngoặc kép thì không bọc thêm lần nữa."""
    chu = chu.strip()
    if chu[:1] in ("“", '"', "‘"):
        return html.escape(chu)
    return "“" + html.escape(chu) + "”"


def the_mach(D, mach, xong):
    """In một mạch liền mạch; mỗi đoạn rẽ in gọn trong thẻ mở được.

    `xong` là mọi đoạn thuộc bất kỳ mạch nào đã in, để chuỗi rẽ dừng lại thay vì
    chạy tuốt sang phần đã in ở nơi khác.
    """
    o = []
    for vi_tri, ma in enumerate(mach):
        o.append(the_doan(D, ma))
        ke_tiep = mach[vi_tri + 1] if vi_tri + 1 < len(mach) else None
        for chon in D[ma].get("lua_chon") or []:
            if chon["den"] == ke_tiep:
                continue
            re_ = chuoi_re(D, chon["den"], xong)
            if not re_:
                continue
            o.append('<details class="nhanh-phu">')
            o.append(f'<summary>Chọn: {nhan_chon(chon["chu"])}</summary>')
            for ma_re in re_:
                o.append(the_doan(D, ma_re))
            o.append("</details>")
    return "\n".join(o)


def sinh():
    d = doc()
    D = {x["id"]: x for x in d["doan"]}
    o = []
    o.append("""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cốt truyện Chương 2 — Tiểu hội Thái Nam Sơn Cốc</title>
<style>
  :root{--giay:#f4ecd8;--muc:#241c14;--son:#8a3a20;--luc:#3f7d4e}
  *{box-sizing:border-box}
  body{margin:0;background:#14100b;color:var(--muc);
       font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
       line-height:1.7;-webkit-text-size-adjust:100%}
  .khung{max-width:720px;margin:0 auto;padding:18px 14px 64px}
  .to{background:var(--giay);border-radius:14px;padding:20px 16px;
      box-shadow:0 10px 40px rgba(0,0,0,.5)}
  h1{font-size:22px;line-height:1.3;margin:0 0 6px;color:var(--son)}
  .phu{font-size:13px;color:#6b5b48;margin:0 0 16px}
  h2{font-size:17px;margin:30px 0 12px;color:var(--son);
     border-bottom:1px solid rgba(138,58,32,.25);padding-bottom:6px}
  h3{font-size:14px;margin:22px 0 6px;color:#5a3a22;letter-spacing:.3px;
     text-transform:uppercase}
  .tomtat{background:rgba(138,58,32,.07);border-left:3px solid var(--son);
          border-radius:0 8px 8px 0;padding:12px 14px;margin:14px 0;font-size:14.5px}
  .doan{margin:0 0 4px}
  .doan img{display:block;width:100%;height:auto;border-radius:10px;
            margin:16px 0 10px;box-shadow:0 4px 18px rgba(0,0,0,.25)}
  .doan p{font-size:15.5px;margin:11px 0}
  .doan p.he{font-size:14px;color:var(--luc);background:rgba(63,125,78,.09);
             border-left:3px solid var(--luc);border-radius:0 8px 8px 0;
             padding:9px 12px;margin:13px 0}
  .canh{font-size:12px;color:#8b7a63;text-transform:uppercase;
        letter-spacing:.7px;margin:18px 0 2px!important}
  em{color:#5a3a22}
  .nut-nhanh{display:flex;gap:8px;margin:14px 0}
  .nut-nhanh a{flex:1;text-align:center;background:rgba(138,58,32,.1);
               color:var(--son);text-decoration:none;padding:11px;border-radius:9px;
               font-size:14px;font-weight:600;border:1px solid rgba(138,58,32,.3)}
  details{background:rgba(36,28,20,.045);border-radius:10px;padding:0 13px;
          margin:14px 0;border:1px solid rgba(36,28,20,.12)}
  summary{padding:12px 0;font-size:14px;font-weight:600;color:#5a3a22;
          cursor:pointer;list-style:none}
  summary::-webkit-details-marker{display:none}
  summary::before{content:"▸ ";color:var(--son)}
  details[open] summary::before{content:"▾ "}
  details .doan p{font-size:15px}
  details .doan img{margin-top:8px}
  .nhanh-phu{border-left:3px solid rgba(138,58,32,.35)}
  .ghi{font-size:12.5px;color:#6b5b48;font-style:italic;margin:6px 0 0}
  .luoi{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
  .luoi div{background:rgba(36,28,20,.05);border-radius:8px;padding:9px 11px;
            font-size:13.5px}
  .luoi b{display:block;font-size:19px;color:var(--son);
          font-family:ui-monospace,Menlo,monospace}
  .dai{font-size:13px;color:#6b5b48;margin-top:26px;padding-top:12px;
       border-top:1px solid rgba(36,28,20,.15)}
  a{color:var(--son)}
</style>
</head>
<body>
<div class="khung">
<div class="to">""")

    o.append(f'<h1>Chương 2 — {html.escape(d["ten"])}</h1>')
    o.append('<p class="phu">Toàn văn cốt truyện · sinh thẳng từ dữ liệu game · '
             'đọc trên điện thoại</p>')
    o.append(f'<div class="tomtat">{html.escape(d["tom_tat"])}</div>')

    so_lc = sum(len(x.get("lua_chon") or []) for x in d["doan"])
    o.append('<div class="luoi">')
    o.append(f'<div><b>{len(d["doan"])}</b>đoạn</div>')
    o.append(f'<div><b>{so_lc}</b>lựa chọn</div>')
    o.append(f'<div><b>2</b>nhánh xuất thân</div>')
    o.append(f'<div><b>23</b>ảnh</div>')
    o.append("</div>")

    # Điểm gặp nhau của hai nhánh
    machs = {nhom: mach_chinh(D, dau) for nhom, dau in d["doan_dau_theo_nhom"].items()}
    chung = set(machs["tan_tu"]) & set(machs["mon_phai"])
    diem_gap = None
    for ma in machs["tan_tu"]:
        if ma in chung:
            diem_gap = ma
            break

    o.append('<h2>Hai lối vào</h2>')
    o.append('<p>Chương 2 có hai lối vào khác nhau tuỳ xuất thân. Đọc lối vào của '
             'mình, rồi đọc tiếp phần <b>mạch chung</b> bên dưới — từ Thái Nam sơn '
             'trở đi hai nhánh nhập làm một.</p>')
    o.append('<div class="nut-nhanh">'
             '<a href="#tan-tu">Tán tu</a>'
             '<a href="#mon-phai">Môn phái</a></div>')

    # Mạch chung: phần cả hai nhánh cùng đi, tính từ đoạn gặp nhau
    mach_chung = [ma for ma in machs["tan_tu"][machs["tan_tu"].index(diem_gap):]
                  if ma in chung]

    xong = set(mach_chung)
    for m in machs.values():
        xong |= set(m)

    for nhom in ("tan_tu", "mon_phai"):
        mach = machs[nhom]
        rieng = mach[:mach.index(diem_gap)]
        o.append(f'<h2 id="{nhom.replace("_", "-")}">'
                 f'Lối vào — {TEN_NHOM[nhom]} '
                 f'<span class="ghi">({len(rieng)} đoạn, rồi nhập mạch chung)</span></h2>')
        o.append(the_mach(D, rieng, xong))

    o.append('<h2 id="mach-chung">Mạch chung</h2>')
    o.append('<p class="ghi">Từ đây hai nhánh đi cùng một đường: tới Thái Nam sơn, '
             'xuống hội chợ, rồi tới ngày cuối.</p>')
    o.append(the_mach(D, mach_chung, xong))

    # Lời kết
    o.append('<h2>Lời kết chương</h2>')
    o.append('<p class="ghi">Hiện cho cả hai nhánh, nên chữ ở đây cố ý trung tính.</p>')
    o.append('<article class="doan">' + doan_van(d["ket"]["ke"]) + "</article>")

    o.append('<p class="dai">Trang này sinh từ <code>game/chapters/chuong2.json</code> '
             'bằng <code>tools/tao_trang_cot_truyen.py</code>. '
             'Sửa truyện thì chạy lại script, đừng sửa tay trang này.<br>'
             '<a href="chuong2-thai-nam.html">← Báo cáo Chương 2</a> · '
             '<a href="../game/play.html">Vào chơi →</a></p>')
    o.append("</div></div></body></html>")

    os.makedirs(os.path.dirname(RA), exist_ok=True)
    with open(RA, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return RA, len(d["doan"]), so_lc


if __name__ == "__main__":
    ra, so_doan, so_lc = sinh()
    print(f"Đã ghi {ra} — {so_doan} đoạn, {so_lc} lựa chọn")
