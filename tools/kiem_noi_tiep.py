"""Kiem tra noi tiep: canh moi co lap lai / mau thuan voi doan dich khong.

Hai phep kiem:
1. Lap: cum 6 tu o cuoi canh moi trung voi cum o dau doan dich.
2. Gia dinh hanh dong: doan dich mo dau bang "Ta ..." + dong tu hanh dong,
   trong khi lua chon khac lai noi nguoc lai.

Chay: python3 tools/kiem_noi_tiep.py
"""
import io
import json
import re
import sys

GOC = "/workspace/project"
sys.path.insert(0, GOC + "/tools")


def tu(s):
    return re.findall(r"[0-9A-Za-zÀ-ỹĐđ]+", s.lower())


def cum(t, n=6):
    return {" ".join(t[i:i + n]) for i in range(max(0, len(t) - n + 1))}


def main():
    import tach_canh

    D = {}
    for so in (1, 2):
        for x in json.loads(io.open(f"{GOC}/game/chapters/chuong{so}.json",
                                    encoding="utf-8").read())["doan"]:
            D[x["id"]] = x

    lap = []
    for (src, i), (van, _) in sorted(tach_canh.CANH.items()):
        if src not in D:
            continue
        den = D[src]["lua_chon"][i]["den"]
        goc = den.rsplit("_", 1)[0] if re.search(r"_\d+$", den) else den
        if goc not in D:
            continue
        c_cuoi = cum(tu(van.strip().split("\n\n")[-1]))
        c_dau = cum(tu(D[goc]["ke"].split("\n\n")[0]))
        chung = c_cuoi & c_dau
        if chung:
            lap.append((src, i, goc, sorted(chung)[:2]))

    print(f"Canh moi: {len(tach_canh.CANH)}")
    print(f"Lap cum 6 tu voi doan dich: {len(lap)}")
    for src, i, goc, vd in lap:
        print(f"  {src}[{i}] -> {goc}: {vd}")
    return 1 if lap else 0


sys.exit(main())
