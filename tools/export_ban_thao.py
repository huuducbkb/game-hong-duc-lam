#!/usr/bin/env python3
"""Xuất bản thảo chương ra Markdown + HTML để người dùng đọc và duyệt.

Mỗi XUẤT THÂN là một nhánh truyện riêng, nên bản thảo được TÁCH THEO NHÁNH
(không nối 5 nhánh vào một file gây cảm giác "truyện khởi động lại").

Dùng:
    python3 tools/export_ban_thao.py                  # xuất mọi chương, mọi nhánh
    python3 tools/export_ban_thao.py 1                # chỉ Chương 1 (mọi nhánh)
    python3 tools/export_ban_thao.py 1 --nhanh mon_phai   # chỉ nhánh môn phái

Kết quả (ví dụ Chương 1):
    docs/ban-thao/index.html               — mục lục: chương + từng nhánh
    docs/ban-thao/chuong1-mon-phai.html    — đọc trên Safari
    docs/ban-thao/chuong1-mon-phai.md      — xem trên GitHub

Đoạn nào thuộc nhánh nào được xác định bằng CÁCH ĐI THEO LIÊN KẾT từ đoạn mở
đầu của nhánh (không dựa vào tiền tố mã đoạn).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_DIR = os.path.join(ROOT, "game", "chapters")
OUT_DIR = os.path.join(ROOT, "docs", "ban-thao")
XUAT_THAN = os.path.join(ROOT, "game", "xuat_than.json")

HOI_TEN = {"Mở": "Hồi Mở", "Thân": "Hồi Thân", "Kết": "Hồi Kết"}


# ------------------------------------------------------------------ dữ liệu

def doc_nhom() -> list[dict]:
    """Danh sách nhánh chơi được (bỏ nhóm ẩn chưa mở)."""
    d = json.load(open(XUAT_THAN, encoding="utf-8"))
    return [n for n in d["nhom"] if not n.get("an")]


def slug(ma: str) -> str:
    return ma.replace("_", "-")


def doan_theo_nhanh(ch: dict, doan_dau: str) -> list[dict]:
    """Các đoạn thuộc một nhánh: đi theo liên kết từ đoạn mở đầu.

    Giữ đúng thứ tự trong JSON để bản thảo đọc mạch lạc.
    """
    theo_id = {d["id"]: d for d in ch["doan"]}
    if doan_dau not in theo_id:
        return []
    tham = set()
    cho = [doan_dau]
    while cho:
        i = cho.pop()
        if i in tham or i not in theo_id:
            continue
        tham.add(i)
        for lc in theo_id[i].get("lua_chon", []):
            cho.append(lc["den"])
    return [d for d in ch["doan"] if d["id"] in tham]


def doan_mo_coi(ch: dict, nhom: list[dict]) -> list[dict]:
    """Đoạn không thuộc nhánh nào (liên kết đứt / rác) — để cảnh báo."""
    thuoc = set()
    for n in nhom:
        if n.get("doan_dau"):
            thuoc |= {d["id"] for d in doan_theo_nhanh(ch, n["doan_dau"])}
    return [d for d in ch["doan"] if d["id"] not in thuoc]


# ------------------------------------------------------------------ kết xuất

def _ke_html(ke: str) -> str:
    def _p(p: str) -> str:
        e = html.escape(p)
        # *…* → nội tâm in nghiêng
        e = re.sub(r"\*([^*]+)\*", r"<em class='noi-tam'>\1</em>", e)
        return f"<p>{e}</p>"

    return "".join(_p(p) for p in ke.split("\n\n") if p.strip())


def _hieu_ung_txt(hu: dict) -> str:
    if not hu:
        return ""
    phan = []
    tien = hu.get("bac", hu.get("linh_thach"))
    if tien:
        phan.append(f"bạc {tien:+d}")
    if hu.get("tu_vi"):
        phan.append(f"tu vi {hu['tu_vi']:+d}")
    if hu.get("sinh_luc"):
        phan.append(f"sinh lực {hu['sinh_luc']:+d}")
    if hu.get("than_niem"):
        phan.append(f"thần niệm {hu['than_niem']:+d}")
    if hu.get("co_su_kien"):
        phan.append("mở cờ: " + ", ".join(hu["co_su_kien"]))
    if hu.get("npc"):
        phan.append("NPC: " + ", ".join(f"{k} ({v})" for k, v in hu["npc"].items()))
    if hu.get("them_vat"):
        phan.append("nhận: " + ", ".join(v["ten"] for v in hu["them_vat"]))
    if hu.get("ky_nang"):
        phan.append("học: " + ", ".join(hu["ky_nang"]))
    return "; ".join(phan)


def phan_tich_nhanh(ch: dict, doan: list[dict], doan_dau: str | None):
    """Phát hiện điểm rẽ nhánh đầu tiên + nhãn đường cho từng đoạn.

    Trả về (danh_sách_đoạn, nhãn_đường, dòng_sơ_đồ). Không rẽ nhánh → (doan, {}, None).
    Đoạn đi được từ ≥2 nhánh (hội tụ) coi là dùng chung, không gắn nhãn.
    """
    if not doan_dau:
        return doan, {}, None
    theo = {d["id"]: d for d in ch["doan"]}
    trong = {d["id"] for d in doan}
    if doan_dau not in theo:
        return doan, {}, None

    duong = [doan_dau]
    cur = doan_dau
    while True:
        lcs = [l["den"] for l in theo[cur].get("lua_chon", []) if l["den"] in trong]
        if len(lcs) != 1:
            break
        cur = lcs[0]
        duong.append(cur)
    lcs_re = [l for l in theo[cur].get("lua_chon", []) if l["den"] in trong]
    if len(lcs_re) < 2:
        return doan, {}, None

    def reach(start):
        tham, cho = set(), [start]
        while cho:
            i = cho.pop()
            if i in tham or i not in trong:
                continue
            tham.add(i)
            for l in theo[i].get("lua_chon", []):
                cho.append(l["den"])
        return tham

    tap = [reach(l["den"]) for l in lcs_re]
    nhanh: dict[str, int | None] = {}
    for idx, r in enumerate(tap):
        for i in r:
            nhanh[i] = None if i in nhanh else idx

    def lay(ids):
        return [d for d in doan if d["id"] in ids]

    def cha_trong(tap_ids):
        ch = {}
        for d in doan:
            if d["id"] not in tap_ids:
                continue
            for l in theo[d["id"]].get("lua_chon", []):
                if l["den"] in tap_ids:
                    ch.setdefault(l["den"], set()).add(d["id"])
        return ch

    def gom_song_song(ids):
        """Nối các đoạn liền nhau có CÙNG tập cha bằng ' / ' (lựa chọn song song)."""
        ch = cha_trong(set(ids))
        ra, i = [], 0
        while i < len(ids):
            nhom = [ids[i]]
            j = i + 1
            while (j < len(ids) and ch.get(ids[j]) and ch.get(ids[j]) == ch.get(ids[i])
                   and ch.get(ids[i])):
                nhom.append(ids[j]); j += 1
            ra.append(" / ".join(nhom))
            i = j
        return " · ".join(ra)

    dau = set(duong)
    sap_xep = lay(dau)
    for idx in range(len(tap)):
        sap_xep += lay({i for i, v in nhanh.items() if v == idx})
    sap_xep += lay({i for i, v in nhanh.items() if v is None} - dau)

    nhan = {i: v for i, v in nhanh.items() if v is not None}

    sd = ["  ".join(duong) + f"   ← rẽ {len(tap)} hướng"]
    for idx, l in enumerate(lcs_re):
        ma = chr(0x2460 + idx)
        nhanh_ids = [d["id"] for d in doan if nhanh.get(d["id"]) == idx]
        goc = "└─" if idx == len(tap) - 1 else "├─"
        sd.append(f"  {goc} {ma} {l['chu']}")
        if nhanh_ids:
            sd.append(f"  │     " + gom_song_song(nhanh_ids))
        else:
            sd.append(f"  │     (đi thẳng tới hội tụ)")
    chung = [d["id"] for d in doan
             if nhanh.get(d["id"]) is None and d["id"] not in dau]
    if chung:
        sd.append("  ↓")
        sd.append("  Hội tụ → " + " · ".join(chung[:4] + (["…"] if len(chung) > 4 else []))
                  + "   (mọi đường dùng chung)")
    return sap_xep, nhan, sd


def xuat_md(ch: dict, doan: list[dict], ten_nhanh: str | None = None,
            doan_dau: str | None = None) -> str:
    L = [f"# Chương {ch['chuong']} — {ch['ten']}"]
    if ten_nhanh:
        L.append(f"## Nhánh: {ten_nhanh}")
    L.append("")
    if ch.get("tom_tat"):
        L.append(f"> **Tóm tắt:** {ch['tom_tat']}")
        L.append("")
    L.append(f"*Nhánh này gồm {len(doan)} đoạn.*")
    L.append("")

    doan, nhan, so_do = phan_tich_nhanh(ch, doan, doan_dau)
    if so_do:
        L.append("**Sơ đồ nhánh** — cùng một nhánh, nhưng rẽ thành nhiều hướng; "
                 "mỗi hướng là một cách gặp cơ duyên riêng:")
        L.append("")
        L.append("```")
        L.extend(so_do)
        L.append("```")
        L.append("")
        L.append("> Các đoạn có nhãn **[ĐƯỜNG ①/②/③]** là đường riêng — "
                 "người chơi chỉ đi MỘT đường. Đoạn không nhãn là dùng chung.")
        L.append("")

    L.append("---")
    L.append("")

    da_in_hoi = set()
    for d in doan:
        if d.get("hoi") not in da_in_hoi:
            da_in_hoi.add(d.get("hoi"))
            L.append(f"## {HOI_TEN.get(d.get('hoi'), d.get('hoi') or '')}")
            L.append("")
        nhan_d = f" · **[ĐƯỜNG {chr(0x2460 + nhan[d['id']])}]**" if d["id"] in nhan else ""
        L.append(f"### Đoạn `{d['id']}` — {d.get('boi_canh', '')}{nhan_d}")
        L.append("")
        if d.get("hinh_anh"):
            L.append(f"*Ảnh:* `{', '.join(d['hinh_anh'].get('tags', []))}`")
            L.append("")
        if d.get("video"):
            L.append(f"*Video:* `{d['video'].get('mau', '')}`")
            L.append("")
        for p in (d.get("ke") or "").split("\n\n"):
            if p.strip():
                L.append(p.strip())
                L.append("")
        lcs = d.get("lua_chon", [])
        if lcs:
            L.append("**Lựa chọn:**")
            L.append("")
            for lc in lcs:
                dong = f"- {lc['chu']}  \n  → `{lc['den']}`"
                if lc.get("dieu_kien"):
                    dong += f" *(điều kiện: {json.dumps(lc['dieu_kien'], ensure_ascii=False)})*"
                if lc.get("ly_do_khoa"):
                    dong += f" — *khoá: {lc['ly_do_khoa']}*"
                hu = _hieu_ung_txt(lc.get("hieu_ung"))
                if hu:
                    dong += f"  \n  ✦ {hu}"
                L.append(dong)
            L.append("")
        if d.get("ket_thuc"):
            L.append("**— Hết chương —**")
            L.append("")
        L.append("---")
        L.append("")
    return "\n".join(L)


CSS = """
:root{--ink:#1b1915;--ink-soft:#3a342b;--ink-faint:#6d6454;--seal:#a8352a;--edge:rgba(40,34,26,.15)}
*{box-sizing:border-box}
body{margin:0;background:#e7dcc4;color:var(--ink);
  font-family:"Noto Serif","Times New Roman",serif;font-size:17px;line-height:1.75}
.wrap{max-width:720px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:27px;margin:0 0 6px;line-height:1.25}
h2{font-size:19px;margin:38px 0 14px;padding-bottom:7px;border-bottom:2px solid var(--seal);
  color:var(--seal);letter-spacing:.5px}
h3{font-size:16px;margin:26px 0 8px;color:var(--ink-soft)}
.tom{background:rgba(255,253,246,.75);border-left:4px solid var(--seal);padding:12px 16px;
  border-radius:8px;font-size:15px;color:var(--ink-soft);margin:16px 0}
.meta{font-size:13px;color:var(--ink-faint);letter-spacing:.5px;margin-bottom:22px}
.id{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ink-faint);
  background:rgba(255,253,246,.6);padding:2px 7px;border-radius:5px}
.tags{font-size:12.5px;color:var(--ink-faint);margin:4px 0 12px}
p{margin:0 0 15px;text-align:justify}
.choice{margin:18px 0 0;padding:14px 16px;background:rgba(255,253,246,.72);
  border:1px solid var(--edge);border-radius:10px}
.choice h4{margin:0 0 10px;font-size:13px;letter-spacing:1.5px;color:var(--seal);
  text-transform:uppercase}
.choice ol{margin:0;padding-left:22px}
.choice li{margin-bottom:11px;line-height:1.55}
.to{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ink-faint)}
.hu{font-size:13.5px;color:var(--seal);margin-top:3px}
.khoa{font-size:13px;color:#8a7d63;font-style:italic}
.noi-tam{font-style:italic;color:#5b5443}
.het{text-align:center;color:var(--seal);letter-spacing:4px;margin:30px 0;font-size:15px}
hr{border:0;border-top:1px dashed var(--edge);margin:30px 0}
a{color:var(--seal)}
.back{display:inline-block;margin-bottom:20px;font-size:14px}
"""


def xuat_html(ch: dict, doan: list[dict], ten_nhanh: str | None = None,
              doan_dau: str | None = None) -> str:
    H = ["<!DOCTYPE html><html lang='vi'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         f"<title>Bản thảo Chương {ch['chuong']}"
         + (f" — {html.escape(ten_nhanh)}" if ten_nhanh else "") + "</title>",
         "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,600;1,400&display=swap' rel='stylesheet'>",
         f"<style>{CSS}</style></head><body><div class='wrap'>",
         "<a class='back' href='index.html'>← Mục lục bản thảo</a>",
         f"<h1>Chương {ch['chuong']} — {html.escape(ch['ten'])}</h1>"]
    if ten_nhanh:
        H.append(f"<div class='tom'><b>Nhánh:</b> {html.escape(ten_nhanh)}</div>")
    elif ch.get("tom_tat"):
        H.append(f"<div class='tom'><b>Tóm tắt:</b> {html.escape(ch['tom_tat'])}</div>")
    H.append(f"<div class='meta'>Nhánh này gồm {len(doan)} đoạn · bản thảo để duyệt</div>")

    doan, nhan, so_do = phan_tich_nhanh(ch, doan, doan_dau)
    if so_do:
        H.append("<div class='choice'><h4>Sơ đồ nhánh</h4>"
                 "<div style='font-size:13px;color:#6d6454;margin-bottom:8px'>"
                 "Cùng một nhánh, nhưng rẽ thành nhiều hướng — mỗi hướng là một cách gặp cơ duyên riêng. "
                 "Các đoạn có nhãn <b>[ĐƯỜNG ①/②/③]</b> là đường riêng (người chơi chỉ đi MỘT đường). "
                 "Đoạn không nhãn là dùng chung.</div>"
                 "<pre style='margin:0;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;"
                 "white-space:pre-wrap;color:#3a342b'>"
                 + html.escape("\n".join(so_do)) + "</pre></div>")

    da_in_hoi = set()
    for d in doan:
        if d.get("hoi") not in da_in_hoi:
            da_in_hoi.add(d.get("hoi"))
            H.append(f"<h2>{html.escape(HOI_TEN.get(d.get('hoi'), d.get('hoi') or ''))}</h2>")
        nhan_d = (f" <span style='color:#a8352a;font-size:13px'>· ĐƯỜNG "
                  f"{chr(0x2460 + nhan[d['id']])}</span>") if d["id"] in nhan else ""
        H.append(f"<h3>{html.escape(d.get('boi_canh', ''))}{nhan_d} "
                 f"<span class='id'>{d['id']}</span></h3>")
        tags = []
        if d.get("hinh_anh"):
            tags.append("Ảnh: " + ", ".join(d["hinh_anh"].get("tags", [])))
        if d.get("video"):
            tags.append("Video: " + d["video"].get("mau", ""))
        if tags:
            H.append(f"<div class='tags'>{html.escape(' · '.join(tags))}</div>")
        H.append(_ke_html(d.get("ke") or ""))

        lcs = d.get("lua_chon", [])
        if lcs:
            H.append("<div class='choice'><h4>Lựa chọn</h4><ol>")
            for lc in lcs:
                H.append(f"<li>{html.escape(lc['chu'])}<div class='to'>→ {lc['den']}</div>")
                if lc.get("dieu_kien"):
                    H.append(f"<div class='khoa'>điều kiện: {html.escape(json.dumps(lc['dieu_kien'], ensure_ascii=False))}"
                             + (f" — {html.escape(lc['ly_do_khoa'])}" if lc.get("ly_do_khoa") else "") + "</div>")
                hu = _hieu_ung_txt(lc.get("hieu_ung"))
                if hu:
                    H.append(f"<div class='hu'>✦ {html.escape(hu)}</div>")
                H.append("</li>")
            H.append("</ol></div>")
        if d.get("ket_thuc"):
            H.append("<div class='het'>— HẾT CHƯƠNG —</div>")
        H.append("<hr>")
    H.append("</div></body></html>")
    return "\n".join(H)


def xuat_index(chuongs: list[dict], nhom: list[dict]) -> str:
    H = ["<!DOCTYPE html><html lang='vi'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         "<title>Bản thảo — Hồng Đức Tu Tiên Lộ</title>",
         "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;600&display=swap' rel='stylesheet'>",
         f"<style>{CSS}</style></head><body><div class='wrap'>",
         "<h1>Bản thảo — Hồng Đức Tu Tiên Lộ</h1>",
         "<div class='meta'>Mỗi xuất thân là một nhánh truyện riêng. Bấm vào nhánh để đọc.</div>"]
    for ch in chuongs:
        H.append(f"<h2>Chương {ch['chuong']} — {html.escape(ch['ten'])}</h2>")
        for n in nhom:
            if not n.get("doan_dau"):
                continue
            doan = doan_theo_nhanh(ch, n["doan_dau"])
            if not doan:
                continue
            s = slug(n["ma"])
            H.append(f"<div class='choice'><h4>{html.escape(n['ten'])}</h4>"
                     f"<div class='to'>{len(doan)} đoạn</div>"
                     f"<p style='margin:10px 0 0'>"
                     f"<a href='chuong{ch['chuong']}-{s}.html'>Đọc bản thảo →</a> "
                     f"· <a href='chuong{ch['chuong']}-{s}.md'>Markdown</a></p></div>")
    H.append("</div></body></html>")
    return "\n".join(H)


# ------------------------------------------------------------------ điều khiển

def main():
    ap = argparse.ArgumentParser(description="Xuất bản thảo theo nhánh")
    ap.add_argument("chuong", nargs="*", help="số chương (bỏ trống = mọi chương)")
    ap.add_argument("--nhanh", help="chỉ xuất một nhánh (mã: tan_tu, mon_phai)")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    nhom = doc_nhom()
    if args.nhanh:
        nhom = [n for n in nhom if n["ma"] == args.nhanh]
        if not nhom:
            raise SystemExit(f"Không có nhánh '{args.nhanh}'. Chọn: "
                             + ", ".join(n["ma"] for n in doc_nhom()))

    files = sorted(f for f in os.listdir(CH_DIR)
                   if f.startswith("chuong") and f.endswith(".json"))
    chuongs = []
    for f in files:
        so = f.replace("chuong", "").replace(".json", "")
        if args.chuong and so not in args.chuong:
            continue
        ch = json.load(open(os.path.join(CH_DIR, f), encoding="utf-8"))
        chuongs.append(ch)
        for n in nhom:
            doan = doan_theo_nhanh(ch, n["doan_dau"])
            if not doan:
                continue
            s = slug(n["ma"])
            md = xuat_md(ch, doan, n["ten"], n["doan_dau"])
            open(os.path.join(OUT_DIR, f"chuong{ch['chuong']}-{s}.md"), "w",
                 encoding="utf-8").write(md)
            open(os.path.join(OUT_DIR, f"chuong{ch['chuong']}-{s}.html"), "w",
                 encoding="utf-8").write(xuat_html(ch, doan, n["ten"], n["doan_dau"]))
            print(f"Chương {ch['chuong']} · nhánh {n['ten']}: {len(doan)} đoạn "
                  f"→ chuong{ch['chuong']}-{s}.md / .html")
        mo_coi = doan_mo_coi(ch, doc_nhom())
        if mo_coi:
            print(f"  ⚠ {len(mo_coi)} đoạn không thuộc nhánh nào: "
                  + ", ".join(d["id"] for d in mo_coi))

    if chuongs and not args.nhanh:
        open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(
            xuat_index(chuongs, doc_nhom()))
        print("Mục lục → " + os.path.relpath(os.path.join(OUT_DIR, "index.html"), ROOT))


if __name__ == "__main__":
    main()
