"""Sua ba cho doan dich con gia dinh san hanh dong cua mot lua chon.

1. c2_p04: "Han Lap di tu luc troi chua sang... chi con cai bong ao xam"
   -> chi dung khi nguoi choi chon di sau. Di cung thi phai co canh rieng.
2. c2_d26: "Kiem linh im rat lau khi nhin cai binh" -> gia dinh da nho kiem linh xem.
3. c2_p23: "Han Lap cat cai binh vao ao" -> gia dinh nguoi choi khong giu binh.

Chay: python3 tools/sua_gia_dinh.py [--ghi]
"""
import io
import json
import sys

GOC = "/workspace/project"


def main():
    ghi = "--ghi" in sys.argv
    p = f"{GOC}/game/chapters/chuong2.json"
    ch = json.loads(io.open(p, encoding="utf-8").read())
    D = {x["id"]: x for x in ch["doan"]}

    # --- 1. c2_p04: tach canh "di cung" ra node rieng
    if "c2_p04di" not in D:
        src = D["c2_p03"]
        di_cung = src["lua_chon"][0]
        assert di_cung["den"] == "c2_p04_0", di_cung["den"]
        moi = {
            "id": "c2_p04di",
            "hoi": src.get("hoi"),
            "boi_canh": "Cổng môn — trước khi trời sáng",
            "ke": (
                "Chúng ta ra khỏi cổng môn khi trời còn tối.\n\n"
                "Hàn Lập đi trước, bước nhanh và không ngoái lại. Ta đi sau nửa bước, "
                "cái hòm gỗ trên lưng hắn, còn ta thì mang túi áo nhẹ — mấy nén bạc, "
                "khối ngọc cốt, và không có gì khác.\n\n"
                "“Ngươi đi chậm quá,” — hắn nói, không quay đầu.\n\n"
                "“Ta đi vừa sức ta.”\n\n"
                "“Vậy thì ta đi chậm lại.” — Và hắn chậm lại thật.\n\n"
                "Chúng ta đi về phía nam, và trên đường ấy, hắn không hỏi ta một câu nào "
                "về việc ta là ai. Ta biết hắn đang chờ ta tự nói."
            ),
            "lua_chon": [{"chu": "Xuống núi", "den": "c2_p05"}],
        }
        vi_tri = next(k for k, x in enumerate(ch["doan"]) if x["id"] == "c2_p04")
        ch["doan"].insert(vi_tri, moi)
        di_cung["den"] = "c2_p04di"
        print("  c2_p03[0] -> c2_p04di (canh di cung) -> c2_p05")

    # --- 2. c2_d26: mo dau trung tinh
    cu = ("Kiếm linh im rất lâu khi nhìn cái bình.\n\n"
          "Rồi nó nói, và giọng nó khác hẳn mọi khi — không lạnh, không khô, "
          "mà như có gì đó bị nén lại:")
    moi = ("Cái bình nằm trên tảng đá. Nhỏ, men xanh, sứt một miếng — và nó không "
           "phản chiếu ánh lửa như mọi thứ khác trong khe đá này.\n\n"
           "Rồi kiếm linh nói, và giọng nó khác hẳn mọi khi — không lạnh, không khô, "
           "mà như có gì đó bị nén lại:")
    if cu in D["c2_d26"]["ke"]:
        D["c2_d26"]["ke"] = D["c2_d26"]["ke"].replace(cu, moi, 1)
        print("  c2_d26: mo dau trung tinh")

    # --- 3. c2_p23: tach canh "nguoi choi giu binh"
    if "c2_p23giu" not in D:
        src = D["c2_p22"]
        giu = src["lua_chon"][2]
        assert giu["den"] == "c2_p23_2", giu["den"]
        moi = {
            "id": "c2_p23giu",
            "hoi": src.get("hoi"),
            "boi_canh": "Khe đá — đêm ngày cuối",
            "ke": (
                "Cái bình nằm trong túi áo ta, lạnh như một viên đá sông.\n\n"
                "Hàn Lập không hỏi thêm. Nhưng trước khi quay đi, hắn nói: "
                "“Nếu ngươi đổi ý, cứ đưa lại. Ta không giận.”\n\n"
                "Bên ngoài, khói đã dày đặc. Tiếng chân người chạy qua khe đá, "
                "rồi tiếng một vật nặng đổ.\n\n"
                "“Ra ngoài xem,” — Hàn Lập nói, đứng dậy.\n\n"
                "Ta theo hắn ra. Tay ta vẫn đặt trên túi áo, chỗ cái bình."
            ),
            "lua_chon": [{"chu": "Nhìn kỹ", "den": "c2_p24"}],
        }
        vi_tri = next(k for k, x in enumerate(ch["doan"]) if x["id"] == "c2_p23")
        ch["doan"].insert(vi_tri, moi)
        giu["den"] = "c2_p23giu"
        print("  c2_p22[2] -> c2_p23giu (nguoi choi giu binh) -> c2_p24")

    print(f"chuong2: {len(ch['doan'])} doan")
    if ghi:
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(ch, ensure_ascii=False, indent=2) + "\n")
        print("da ghi")
    else:
        print("(chay lai voi --ghi)")


main()
