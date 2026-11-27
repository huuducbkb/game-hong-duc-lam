"""Lắp Chương 2: hai nhánh đi riêng, không đoạn nào dùng chung.

Giữ nguyên văn phần đầu mỗi nhánh đã duyệt (tán tu `c2_d01`…`c2_d10`,
môn phái `c2_p01`…`c2_p06`) và nối vào phần Thái Nam viết mới.
"""

import json
import os
import sys

GOC = os.path.join(os.path.dirname(__file__), "..", "game", "chapters", "chuong2.json")
DUONG_RA = GOC

# Đoạn cuối phần đầu mỗi nhánh trỏ vào đâu trong phần mới.
NOI = {
    "c2_d10": ("c2_d11", "tan_tu"),
    "c2_p06": ("c2_p07", "mon_phai"),
}

# Phần đầu hai nhánh đã duyệt — giữ nguyên văn, không bao giờ sinh lại.
GIU = ["c2_d01", "c2_d01b", "c2_d02", "c2_d03", "c2_d04", "c2_d05", "c2_d06",
       "c2_d07", "c2_d08", "c2_d08b", "c2_d09", "c2_d10",
       "c2_p01", "c2_p01b", "c2_p02", "c2_p03", "c2_p04", "c2_p05", "c2_p06"]



def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import dung_chuong2_tantu as T
    import dung_chuong2_monphai as P

    goc = json.load(open(GOC, encoding="utf-8"))
    theo_id = {x["id"]: x for x in goc["doan"]}
    giu = {i: theo_id[i] for i in GIU}

    # Bạn đồng hành phải có mặt trong sổ NPC với hảo cảm 100 ngay khi mở đoạn
    # đầu mỗi nhánh — gắn vào đoạn (hieu_ung_vao) chứ không vào lựa chọn, vì
    # người chơi vào thẳng Chương 2 sẽ không đi qua bước nào của Chương 1.
    for did, ten in (("c2_d01", "Hồng Trần"), ("c2_p01", "Tuyết Cơ")):
        giu[did]["hieu_ung_vao"] = {"gap_npc": {ten: {"hao_cam": 100}}}


    for did, (moi, _) in NOI.items():
        x = giu[did]
        assert len(x["lua_chon"]) == 1, f"{did} phải có đúng 1 lựa chọn"
        x["lua_chon"][0]["den"] = moi

    moi_t = T.dung()
    moi_p = P.dung()
    tat_ca = list(giu.values()) + moi_t + moi_p

    ids = [x["id"] for x in tat_ca]
    trung = {i for i in ids if ids.count(i) > 1}
    assert not trung, f"mã đoạn trùng: {sorted(trung)}"

    co = set(ids)
    hong = [(x["id"], lc["den"]) for x in tat_ca for lc in x["lua_chon"]
            if lc["den"] != "__ket_thuc__" and lc["den"] not in co]
    assert not hong, f"đích trỏ vào hư không: {hong}"

    ra = {
        "chuong": 2,
        "ten": goc["ten"],
        "tom_tat": goc["tom_tat"],
        "doan_dau_theo_nhom": {"tan_tu": "c2_d01", "mon_phai": "c2_p01"},
        "doan": tat_ca,
        "ket": {
            "boi_canh": "Chương 2 — hết",
            "ke": "Thái Nam Cốc khép lại. Thung lũng trống, lều đã dỡ, đèn lồng tắt hết — "
                  "chỉ còn những vệt linh khí bay lơ lửng như chưa từng có gì xảy ra trong đó.\n\n"
                  "Hai người ra khỏi cốc bằng hai con đường khác nhau, mang theo hai thứ khác nhau, "
                  "và cùng một cái tên phải nhớ.\n\n"
                  "*Chương sau: mỗi người một hướng.*",
        },
    }
    with open(DUONG_RA, "w", encoding="utf-8") as f:
        json.dump(ra, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"tán tu : {len([i for i in ids if i.startswith('c2_d')])} đoạn")
    print(f"môn phái: {len([i for i in ids if i.startswith('c2_p')])} đoạn")
    print(f"tổng   : {len(ids)} đoạn")
    print(f"lựa chọn: {sum(len(x['lua_chon']) for x in tat_ca)}")


if __name__ == "__main__":
    main()
