#!/usr/bin/env python3
"""Xuất bản thảo chương ra Markdown + HTML để người dùng đọc và duyệt.

Dùng:
    python3 tools/export_ban_thao.py                # xuất mọi chương
    python3 tools/export_ban_thao.py 1              # chỉ Chương 1

Kết quả:
    docs/ban-thao/chuong1.md    — bản thảo dạng văn bản (xem trên GitHub)
    docs/ban-thao/chuong1.html  — trang đọc (mở trên Safari)
    docs/ban-thao/index.html    — mục lục các chương
"""

from __future__ import annotations

import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_DIR = os.path.join(ROOT, "game", "chapters")
OUT_DIR = os.path.join(ROOT, "docs", "ban-thao")

HOI_TEN = {"Mở": "Hồi Mở", "Thân": "Hồi Thân", "Kết": "Hồi Kết"}


def _ke_html(ke: str) -> str:
    return "".join(f"<p>{html.escape(p)}</p>" for p in ke.split("\n\n") if p.strip())


def _hieu_ung_txt(hu: dict) -> str:
    if not hu:
        return ""
    phan = []
    if hu.get("linh_thach"):
        phan.append(f"linh thạch {hu['linh_thach']:+d}")
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


def xuat_md(ch: dict) -> str:
    L = []
    L.append(f"# Chương {ch['chuong']} — {ch['ten']}")
    L.append("")
    if ch.get("tom_tat"):
        L.append(f"> **Tóm tắt:** {ch['tom_tat']}")
        L.append("")
    L.append(f"*Tổng {len(ch['doan'])} đoạn.*")
    L.append("")
    L.append("---")
    L.append("")

    hoi_truoc = None
    for d in ch["doan"]:
        if d.get("hoi") != hoi_truoc:
            hoi_truoc = d.get("hoi")
            L.append(f"## {HOI_TEN.get(hoi_truoc, hoi_truoc)}")
            L.append("")
        L.append(f"### Đoạn `{d['id']}` — {d.get('boi_canh', '')}")
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
.het{text-align:center;color:var(--seal);letter-spacing:4px;margin:30px 0;font-size:15px}
hr{border:0;border-top:1px dashed var(--edge);margin:30px 0}
a{color:var(--seal)}
.back{display:inline-block;margin-bottom:20px;font-size:14px}
"""


def xuat_html(ch: dict) -> str:
    H = ["<!DOCTYPE html><html lang='vi'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         f"<title>Bản thảo Chương {ch['chuong']}</title>",
         "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,600;1,400&display=swap' rel='stylesheet'>",
         f"<style>{CSS}</style></head><body><div class='wrap'>",
         "<a class='back' href='index.html'>← Mục lục bản thảo</a>",
         f"<h1>Chương {ch['chuong']} — {html.escape(ch['ten'])}</h1>"]
    if ch.get("tom_tat"):
        H.append(f"<div class='tom'><b>Tóm tắt:</b> {html.escape(ch['tom_tat'])}</div>")
    H.append(f"<div class='meta'>Tổng {len(ch['doan'])} đoạn · bản thảo để duyệt</div>")

    hoi_truoc = None
    for d in ch["doan"]:
        if d.get("hoi") != hoi_truoc:
            hoi_truoc = d.get("hoi")
            H.append(f"<h2>{html.escape(HOI_TEN.get(hoi_truoc, hoi_truoc or ''))}</h2>")
        H.append(f"<h3>{html.escape(d.get('boi_canh', ''))} "
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


def xuat_index(chuongs: list[dict]) -> str:
    H = ["<!DOCTYPE html><html lang='vi'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         "<title>Bản thảo — Hồng Đức Tu Tiên Lộ</title>",
         "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;600&display=swap' rel='stylesheet'>",
         f"<style>{CSS}</style></head><body><div class='wrap'>",
         "<h1>Bản thảo — Hồng Đức Tu Tiên Lộ</h1>",
         "<div class='meta'>Các chương đã viết, để người dùng đọc và duyệt</div>"]
    for ch in chuongs:
        so_doan = len(ch["doan"])
        H.append(f"<div class='choice'><h4>Chương {ch['chuong']}</h4>"
                 f"<p style='margin:0 0 8px'><b>{html.escape(ch['ten'])}</b></p>"
                 f"<div class='to'>{so_doan} đoạn</div>"
                 f"<p style='margin:10px 0 0'><a href='chuong{ch['chuong']}.html'>Đọc bản thảo →</a> "
                 f"· <a href='chuong{ch['chuong']}.md'>Markdown</a></p></div>")
    H.append("</div></body></html>")
    return "\n".join(H)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chon = sys.argv[1:] if len(sys.argv) > 1 else None
    files = sorted(f for f in os.listdir(CH_DIR) if f.startswith("chuong") and f.endswith(".json"))
    chuongs = []
    for f in files:
        so = f.replace("chuong", "").replace(".json", "")
        if chon and so not in chon:
            continue
        ch = json.load(open(os.path.join(CH_DIR, f), encoding="utf-8"))
        chuongs.append(ch)
        md = xuat_md(ch)
        open(os.path.join(OUT_DIR, f"chuong{ch['chuong']}.md"), "w", encoding="utf-8").write(md)
        open(os.path.join(OUT_DIR, f"chuong{ch['chuong']}.html"), "w", encoding="utf-8").write(xuat_html(ch))
        print(f"Chương {ch['chuong']}: {len(ch['doan'])} đoạn → chuong{ch['chuong']}.md / .html "
              f"({len(md)} ký tự)")
    if chuongs:
        open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(xuat_index(chuongs))
        print(f"Mục lục → {os.path.relpath(os.path.join(OUT_DIR, 'index.html'), ROOT)}")


if __name__ == "__main__":
    main()
