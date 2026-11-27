"""Kiem tra dau tieng Viet trong van moi, doi chieu voi van da duyet.

Van da duyet (chuong 1-2) dung lam tu dien chuan. Tu nao trong van moi
khong xuat hien trong van da duyet thi bao ra de nguoi viet xem lai.

Chay: python3 tools/kiem_dau.py
"""
import io
import json
import re
import sys

GOC = "/workspace/project"


def tach_tu(s):
    return re.findall(r"[0-9A-Za-zÀ-ỹĐđ]+", s.lower())


def tu_dien_chuan():
    tu = set()
    for so in (1, 2):
        ch = json.loads(io.open(f"{GOC}/game/chapters/chuong{so}.json",
                                encoding="utf-8").read())
        for x in ch["doan"]:
            tu.update(tach_tu(x.get("ke") or ""))
            for bt in x.get("bien_the") or []:
                tu.update(tach_tu(bt.get("ke") or ""))
            for lc in x.get("lua_chon") or []:
                tu.update(tach_tu(lc.get("chu") or ""))
    return tu


def main():
    chuan = tu_dien_chuan()
    sys.path.insert(0, f"{GOC}/tools")
    import tach_canh

    tong_tu = 0
    la = {}
    for khoa, (van_ban, _) in tach_canh.CANH.items():
        tu = tach_tu(van_ban)
        tong_tu += len(tu)
        for t in tu:
            if t not in chuan:
                la.setdefault(t, []).append(khoa)

    print(f"Van moi: {tong_tu} tu, {len(tach_canh.CANH)} canh")
    print(f"Tu khong co trong van da duyet: {len(la)}")
    for t, ds in sorted(la.items()):
        print(f"  {t!r}  ({len(ds)} cho, vi du {ds[0]})")
    return 1 if la else 0


sys.exit(main())
