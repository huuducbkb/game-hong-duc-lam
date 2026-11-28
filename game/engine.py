"""Engine game Hồng Đức Tu Tiên Lộ — cơ chế "chương + đoạn".

Mỗi chương là một chuỗi đoạn (18 đoạn ≈ 45 phút). Đoạn đi một chiều, đánh dấu `da_qua`
để chống lặp. Trạng thái lưu ra file, nạp lại mỗi lượt để AI không "quên".

Không phụ thuộc thư viện ngoài — chỉ dùng thư viện chuẩn Python.
"""

from __future__ import annotations

import copy
import json
import os
import random
import re
import unicodedata
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(ROOT, "game", "chapters")
SAVES_DIR = os.path.join(ROOT, "data", "saves")
XUAT_THAN_PATH = os.path.join(ROOT, "game", "xuat_than.json")

HE_PHAP = ["kim", "moc", "thuy", "hoa", "tho", "loi", "phong", "bang", "doc"]

CANH_GIOI = [
    "Luyện Khí tầng 1", "Luyện Khí tầng 2", "Luyện Khí tầng 3", "Luyện Khí tầng 4",
    "Luyện Khí tầng 5", "Luyện Khí tầng 6", "Luyện Khí tầng 7", "Luyện Khí tầng 8",
    "Luyện Khí tầng 9", "Luyện Khí tầng 10", "Luyện Khí tầng 11", "Luyện Khí tầng 12",
    "Luyện Khí tầng 13", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần",
]

# 6 mức hảo cảm (thấp → cao)
MUC_HAO_CAM = [
    (-100, -60, "tử địch"),
    (-59, -20, "thù địch"),
    (-19, 19, "người dưng"),
    (20, 49, "quen biết"),
    (50, 79, "thân thiết"),
    (80, 100, "tri kỷ"),
]


def muc_hao_cam(diem: int) -> str:
    for lo, hi, ten in MUC_HAO_CAM:
        if lo <= diem <= hi:
            return ten
    return "người dưng"



def _zero_he():
    return {h: 0 for h in HE_PHAP}


# ---------------------------------------------------------------- tu luyện
#
# Phần "Tiến vào tu luyện": nhân vật vào động phủ, tiêu ngày để luyện/cày, rồi
# quay ra truyện với chỉ số đã đổi. Ngân sách ngày dùng CHUNG cho cả chương
# (cách A): vào nhiều lần vẫn còn ngần ấy ngày, tiêu hết là hết.
#
# Mọi phép đổ xúc xắc dùng số ngẫu nhiên CÓ HẠT GIỐNG, sinh từ (tên nhân vật,
# số ngày đã dùng). Chơi lại cùng nhân vật ở cùng ngày ra cùng kết quả, nên
# test kiểm được. Bản Python và bản JS phải cho ra đúng cùng một dãy số —
# sửa một bên là phải sửa bên kia (test đối chiếu ở khối TL).

NGAY_MOI_CHUONG = 30

# Trần cảnh giới theo chương: cày bao nhiêu cũng không vượt. Chương 2 viết cho
# Luyện Khí, nên chặn ở tầng 6 — cũng là lý do phải tìm đường khác qua cổng boss.
TRAN_CANH_GIOI = {2: "Luyện Khí tầng 6"}

TL_VIEC = {
    "da_toa": {"ten": "Đả tọa", "ngay": 3},
    "san": {"ten": "Săn yêu thú", "ngay": 2},
    "luyen_dan": {"ten": "Luyện đan", "ngay": 1},
    "cho": {"ten": "Đi chợ", "ngay": 1},
    "do_la": {"ten": "Dò la", "ngay": 2},
}

# 8 chỉ cho 80 tu vi trong 30 ngày, mà cần 88 để lên tầng 2 — không lên nổi tầng
# nào. 12 cho 120, đủ lên tầng 2 rồi còn 6 ngày. Giữ nguyên tỉ lệ thắng để độ khó
# đánh nhau vẫn thật, chỉ mở đường tu luyện.
TL_TU_VI_DA_TOA = 12

# Yêu thú vùng Thái Nam Sơn Cốc. `bac` là bậc trong CANH_GIOI; `hang` chia độ khó:
# "thuong" (dễ, cho người mới), "tinh_anh" (khá), "yeu_vuong" (boss nhỏ, thưởng lớn).
# `nguy_hiem` là % bị cắn mỗi lần săn. `tu_vi` là tu vi khi giết được.
TL_YEU_THU = [
    # --- Thường: vào được ngay từ Luyện Khí tầng 1 ---
    {"ma": "son_tru", "ten": "Sơn Trư", "hang": "thuong", "bac": 1, "vat": "Nanh sói", "so_vat": 1, "tu_vi": 14, "nguy_hiem": 25},
    {"ma": "thanh_xa", "ten": "Thanh Xà", "hang": "thuong", "bac": 1, "vat": "Mật xà", "so_vat": 1, "tu_vi": 14, "nguy_hiem": 30},
    {"ma": "bach_tho", "ten": "Bạch Thố Tinh", "hang": "thuong", "bac": 1, "vat": "Linh thảo", "so_vat": 2, "tu_vi": 12, "nguy_hiem": 15},
    {"ma": "da_lang", "ten": "Dã Lang", "hang": "thuong", "bac": 2, "vat": "Nanh sói", "so_vat": 2, "tu_vi": 16, "nguy_hiem": 35},
    {"ma": "hac_thu", "ten": "Hắc Thử", "hang": "thuong", "bac": 1, "vat": "Bạc vụn", "so_vat": 2, "tu_vi": 12, "nguy_hiem": 20},
    # --- Tinh anh: cần Luyện Khí tầng 3 trở lên mới nên đụng ---
    {"ma": "hac_lang", "ten": "Hắc Lang Tinh Anh", "hang": "tinh_anh", "bac": 3, "vat": "Nanh sói", "so_vat": 3, "tu_vi": 26, "nguy_hiem": 40},
    {"ma": "thiet_giap", "ten": "Thiết Giáp Thử", "hang": "tinh_anh", "bac": 3, "vat": "Mật xà", "so_vat": 2, "tu_vi": 26, "nguy_hiem": 40},
    {"ma": "xich_vien", "ten": "Xích Viên Tinh Anh", "hang": "tinh_anh", "bac": 4, "vat": "Linh thảo", "so_vat": 3, "tu_vi": 30, "nguy_hiem": 45},
    # --- Yêu vương: chỉ nên đánh khi đã Luyện Khí tầng 5-6 ---
    {"ma": "bach_lang_vuong", "ten": "Bạch Lang Yêu Vương", "hang": "yeu_vuong", "bac": 5, "vat": "Nanh sói", "so_vat": 5, "tu_vi": 48, "nguy_hiem": 55},
    {"ma": "hac_xa_vuong", "ten": "Hắc Xà Yêu Vương", "hang": "yeu_vuong", "bac": 6, "vat": "Mật xà", "so_vat": 5, "tu_vi": 56, "nguy_hiem": 60},
]

# Tu vi khi THUA: cọ xát cũng ngộ đạo, nhưng ít hơn thắng nhiều. Nhờ đây mà đường
# săn tự lên được tầng, không phải chỉ đả tọa. Xem cách tính trong tl_danh.
TL_TU_VI_THUA = 7

# Tỉ lệ gặp theo hạng. Yêu vương hiếm — gặp phải là chuyện lớn, không phải ngày thường.
TL_GAP = {"thuong": 62, "tinh_anh": 30, "yeu_vuong": 8}

# Hạng nào thì cần cảnh giới nào mới săn được. Dưới ngưỡng vẫn gặp nhưng tỉ lệ
# thắng rất thấp — không chặn cứng, để người chơi tự thấy mình yếu.
TL_NGUONG = {"thuong": 0, "tinh_anh": 2, "yeu_vuong": 4}

# Công thức luyện đan. `can` là nguyên liệu, `bac` là tiền, `ti_le` là % thành công.
TL_CONG_THUC = [
    {
        "ma": "tu_khi_dan", "ten": "Tụ Khí Đan", "ngay": 1, "bac": 2, "ti_le": 70,
        "can": {"Nanh sói": 1, "Linh thảo": 2}, "tu_vi": 15,
        "mo_ta": "Đan dược cơ bản, tụ khí vào đan điền.",
    },
    {
        "ma": "hoi_luc_dan", "ten": "Hồi Lực Đan", "ngay": 1, "bac": 3, "ti_le": 65,
        "can": {"Mật xà": 1, "Linh thảo": 1}, "sinh_luc": 12,
        "mo_ta": "Hồi sinh lực, dùng được sau khi bị thương.",
    },
]

# Tin dò la được. Mỗi tin mở MỘT đường qua cổng boss — cày kiểu nào cũng có ích.
TL_TIN = [
    {"ma": "bi_thuong", "ten": "Kẻ gác cổng bị thương ở vai",
     "ke": "Nghe nói kẻ gác cổng bị thương ở vai, mỗi đêm phải ra suối rửa vết."},
    {"ma": "thoi_quen", "ten": "Nó ngủ say trước giờ Dần",
     "ke": "Một lão tiều phu nói kẻ gác cổng ngủ say trước giờ Dần, gọi mãi không dậy."},
    {"ma": "so_lenh_bai", "ten": "Lệnh bài cũ bán ở chợ đen",
     "ke": "Chợ đen dưới chân núi có bán lệnh bài cũ, kẻ gác cổng thấy là cho qua."},
]

TL_CHO_HANG = [
    {"ma": "linh_thao", "ten": "Linh thảo", "gia": 2, "so": 1, "mo_ta": "Nguyên liệu luyện đan."},
    {"ma": "banh_nuong", "ten": "Bánh nướng", "gia": 1, "so": 1, "mo_ta": "Ăn hồi 3 sinh lực."},
]

# Giá BÁN lại. Chợ mua của ngươi rẻ hơn giá bán ra, nên không lấy chợ làm máy in bạc.
# Đây là đường để nguyên liệu săn được biến thành bạc — trước đây săn xong chỉ có
# một đống nguyên liệu nằm chết trong túi vì chợ chỉ bán mà không thu.
TL_BAN_GIA = {
    "Nanh sói": 1,
    "Mật xà": 1,
    "Linh thảo": 1,
    "Tụ Khí Đan": 6,
    "Hồi Lực Đan": 8,
}


def _hat_giong(ten: str, ngay: int) -> int:
    """Băm FNV-1a 32 bit — bản JS phải cho đúng cùng một số."""
    h = 2166136261
    for b in (str(ten) + "|" + str(ngay)).encode("utf-8"):
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _ngau_nhien(hat: int, buoc: int) -> float:
    """LCG 32 bit → số thực [0, 1). Bản JS dùng Math.imul, phải khớp tuyệt đối."""
    x = (hat + buoc * 2654435761) & 0xFFFFFFFF
    x = (x * 1664525 + 1013904223) & 0xFFFFFFFF
    return x / 4294967296.0


def tl_moi() -> dict:
    return {"ngay_con": NGAY_MOI_CHUONG, "ngay_da_dung": 0, "nhat_ky": [], "tin_da_biet": []}


def _tl(state: dict) -> dict:
    """Lấy khối tu luyện, tạo nếu bản lưu cũ chưa có."""
    tl = state.get("tu_luyen")
    if not isinstance(tl, dict):
        tl = tl_moi()
        state["tu_luyen"] = tl
    tl.setdefault("ngay_con", NGAY_MOI_CHUONG)
    tl.setdefault("ngay_da_dung", 0)
    tl.setdefault("nhat_ky", [])
    tl.setdefault("tin_da_biet", [])
    return tl


def _tl_ngau(state: dict) -> float:
    """Số ngẫu nhiên kế tiếp. Mỗi lần gọi là một số MỚI.

    Trước đây khoá theo `ngay_da_dung` và số dòng nhật ký. Hai thứ đó chỉ đổi khi
    tốn ngày, nên "Đổi con khác" (không tốn ngày) trả về đúng một số — bấm 20 lần
    vẫn ra cùng con. Bộ đếm `luot_ngau` tách rời khỏi ngày, và vẫn ghi vào hạt
    giống để chơi lại cùng tên vẫn ra cùng dãy.
    """
    tl = _tl(state)
    luot = tl.get("luot_ngau", 0)
    tl["luot_ngau"] = luot + 1
    return _ngau_nhien(
        _hat_giong(state.get("ten_nhan_vat", ""), tl["ngay_da_dung"]),
        luot,
    )


def _tl_ghi(state: dict, viec: str, ngay: int) -> None:
    tl = _tl(state)
    tl["ngay_con"] = max(0, tl["ngay_con"] - ngay)
    tl["ngay_da_dung"] += ngay
    tl["nhat_ky"].append(f"Ngày {tl['ngay_da_dung']}: {viec}")
    if len(tl["nhat_ky"]) > 40:
        tl["nhat_ky"] = tl["nhat_ky"][-40:]


def _tl_con_ngay(state: dict, ngay: int) -> bool:
    return _tl(state)["ngay_con"] >= ngay


def _tl_co(state: dict, ma_vat: str) -> int:
    for v in state["tui_do"]:
        if v.get("ten") == ma_vat:
            return v.get("so") or 0
    return 0


def _tl_bot(state: dict, ma_vat: str, so: int) -> None:
    for v in list(state["tui_do"]):
        if v.get("ten") == ma_vat:
            v["so"] = (v.get("so") or 0) - so
            if v["so"] <= 0:
                state["tui_do"].remove(v)
            return


def _tl_chi_so(state: dict) -> dict:
    cs = state["chi_so"]
    tl = _tl(state)
    return {
        "ngay_con": tl["ngay_con"],
        "ngay_da_dung": tl["ngay_da_dung"],
        "trong_dong": state.get("trong_dong", False),
        "canh_gioi": state["canh_gioi"],
        "tran": TRAN_CANH_GIOI.get(state.get("chuong")),
        "tu_vi": dict(state["tu_vi"]),
        "sinh_luc": dict(cs["sinh_luc"]),
        "linh_luc": dict(cs["linh_luc"]),
        "bac": state["bac"],
        "tan_cong": cs["tan_cong"],
        "phong_thu": cs["phong_thu"],
        "nhat_ky": list(tl["nhat_ky"][-8:]),
        "tin_da_biet": [
            {"ma": t["ma"], "ten": t["ten"]} for t in TL_TIN if t["ma"] in tl["tin_da_biet"]
        ],
        "con_suc": _tl_con_suc(state),
    }


def _tl_con_suc(state: dict) -> bool:
    """Bị thương nặng thì phải nghỉ, không săn được cho tới khi hồi."""
    sl = state["chi_so"]["sinh_luc"]
    return sl["hien"] > sl["max"] * 0.3


def tl_trang_thai(state: dict) -> dict:
    """Màn Động phủ: chỉ số + danh sách việc kèm GIÁ và DỰ KIẾN trước khi bấm."""
    chi = _tl_chi_so(state)
    viec = []
    for ma, v in TL_VIEC.items():
        duoc = chi["ngay_con"] >= v["ngay"]
        ghi_chu = ""
        if ma == "san" and not chi["con_suc"]:
            duoc = False
            ghi_chu = "Đang bị thương — nghỉ trước đã"
        if ma == "da_toa":
            ghi_chu = f"+{TL_TU_VI_DA_TOA} tu vi"
            if chi["tran"] and chi["canh_gioi"] == chi["tran"]:
                ghi_chu = "Đã chạm trần chương"
        if ma == "san":
            ghi_chu = ghi_chu or "Săn yêu thú, lấy nguyên liệu"
        if ma == "luyen_dan":
            ghi_chu = f"{len(TL_CONG_THUC)} công thức"
        if ma == "cho":
            ghi_chu = f"{len(TL_CHO_HANG)} món bán"
        if ma == "do_la":
            ghi_chu = "Có thể nghe tin về kẻ gác cổng"
        viec.append({
            "ma": ma, "ten": v["ten"], "ngay": v["ngay"],
            "ghi_chu": ghi_chu, "duoc": duoc,
        })
    return {"chi_so": chi, "viec": viec}


def _tl_kiem_tra(state: dict, ma_viec: str) -> dict | None:
    """Trả lỗi nếu không làm được việc này; None nếu được."""
    v = TL_VIEC.get(ma_viec)
    if v is None:
        return {"loi": "Việc không có trong động phủ"}
    if state.get("ket_thuc"):
        return {"loi": "Chương đã khép lại — không tu luyện được nữa"}
    if not _tl_con_ngay(state, v["ngay"]):
        return {"loi": f"Không đủ ngày (cần {v['ngay']}, còn {_tl(state)['ngay_con']})"}
    if ma_viec == "san" and not _tl_con_suc(state):
        return {"loi": "Đang bị thương nặng — nghỉ cho hồi sinh lực đã"}
    return None


def tl_da_toa(state: dict) -> dict:
    """Đả tọa: ăn chắc tu vi, không rủi ro. Đường chính để lên cảnh giới."""
    loi = _tl_kiem_tra(state, "da_toa")
    if loi:
        return loi
    _tl_ghi(state, "đả tọa", TL_VIEC["da_toa"]["ngay"])
    tb = _ap_hieu_ung(state, {"tu_vi": TL_TU_VI_DA_TOA})
    return {"ok": True, "thong_bao": tb or [f"Tu vi +{TL_TU_VI_DA_TOA}"],
            "chi_so": _tl_chi_so(state)}


def _tl_con_thua(state: dict) -> list[str]:
    """Mã những con ĐÃ THUA mà chưa giết lại được — không gặp lại cho tới khi thắng."""
    return list(_tl(state).get("da_thua", []))


def _tl_xao(state: dict, hat: int) -> float:
    """Xáo một số ngẫu nhiên mà KHÔNG đụng bộ đếm `luot_ngau`.

    Dùng khi cần nhiều số trong cùng một lượt (chọn hạng rồi chọn con). Nếu gọi
    `_tl_ngau` hai lần thì mỗi lượt đổi con lại nhảy hai bước, dãy ra bị xen kẽ
    đều đặn — nhìn như "chỉ có 2 con".
    """
    return _ngau_nhien(hat, 7919)


def _tl_chon_thu(state: dict) -> dict:
    """Chọn yêu thú cho lượt này.

    Hai điều bắt buộc:
    1. Con vừa thua thì KHÔNG gặp lại ngay — người chơi kẹt cứng vì cứ gặp đúng
       con mình không đánh lại được (lỗi báo 2026-11-28).
    2. Hạng phải theo cảnh giới: tầng 1 không gặp yêu vương, trừ khi xui rất hiếm.
    """
    tl = _tl(state)
    da_thua = _tl_con_thua(state)
    bac_minh = CANH_GIOI.index(state["canh_gioi"])

    # Chỉ những hạng đã đủ ngưỡng. Yêu vương cần Luyện Khí tầng 5.
    hop = [h for h, nguong in TL_NGUONG.items() if bac_minh >= nguong]
    if not hop:
        hop = ["thuong"]

    # Bỏ con vừa đánh (dù thắng hay thua) — gặp lại y nguyên con cũ ngay lượt sau
    # là đúng cái người dùng báo là "kẹt".
    vua = tl.get("vua_gap")
    loai = set(da_thua) | ({vua} if vua else set())
    ung_vien = [t for t in TL_YEU_THU if t["hang"] in hop and t["ma"] not in loai]
    if not ung_vien:
        # Thua hết cả nhóm. Ban vĩnh viễn là sai: bảng sẽ cạn và quay lại đúng
        # con vừa thua. Thay vào đó cho thử lại từ đầu, nhưng VẪN tránh con vừa
        # đánh — nên không bao giờ trả về y nguyên con vừa gặp.
        tl["da_thua"] = []
        ung_vien = [t for t in TL_YEU_THU if t["hang"] in hop and t["ma"] != vua]
    if not ung_vien:
        ung_vien = [t for t in TL_YEU_THU if t["hang"] == "thuong" and t["ma"] != vua]
    if not ung_vien:
        ung_vien = TL_YEU_THU

    # Chọn hạng theo tỉ lệ, rồi chọn con trong hạng đó.
    r = _tl_ngau(state)
    tong = sum(TL_GAP[h] for h in hop) or 1
    diem = r * tong
    chon_hang = hop[0]
    for h in hop:
        diem -= TL_GAP[h]
        if diem <= 0:
            chon_hang = h
            break
    trong_hang = [t for t in ung_vien if t["hang"] == chon_hang]
    if not trong_hang:  # hạng này vừa thua hết — lấy tạm hạng khác còn ứng viên
        trong_hang = ung_vien
    # Bước chọn con dùng số phái sinh từ `r`, không lấy thêm số mới.
    r2 = _tl_xao(state, int(r * 4294967296))
    thu = trong_hang[int(r2 * len(trong_hang)) % len(trong_hang)]
    tl["muc_tieu"] = thu["ma"]
    tl["vua_gap"] = thu["ma"]
    return thu


def tl_san(state: dict) -> dict:
    """Đi săn: chọn mục tiêu rồi đánh luôn một trận ngắn."""
    return tl_danh(state)


def tl_dau(state: dict) -> dict:
    """Xem trận trước: hiện con đang nhắm và tỉ lệ thắng BẰNG SỐ.

    Không tốn ngày và KHÔNG bị khoá khi đang bị thương — xem còn xem được, chỉ
    đánh mới cần sức. Trước đây hàm này khoá luôn nên người chơi kẹt: bị thương,
    bấm Săn chỉ ra đúng con cũ, không xem được con khác.
    """
    if state.get("ket_thuc"):
        return {"loi": "Chương đã khép lại — không tu luyện được nữa"}
    tl = _tl(state)
    # Nhắm lại con cũ nếu còn đó; hết lượt thì chọn con mới.
    ma = tl.get("muc_tieu")
    thu = next((t for t in TL_YEU_THU if t["ma"] == ma), None)
    if thu is None or ma in _tl_con_thua(state):
        thu = _tl_chon_thu(state)
    return {
        "ok": True,
        "tran": {
            "ma": thu["ma"], "ten": thu["ten"], "hang": thu["hang"],
            "bac": CANH_GIOI[thu["bac"]], "ti_le": _ti_le_thang(state, thu),
            "vat": thu["vat"], "so_vat": thu["so_vat"],
        },
    }


def _ti_le_thang(state: dict, thu: dict) -> int:
    """Tỉ lệ thắng 0–95: chênh cảnh giới là yếu tố chính, cộng tấn công."""
    cs = state["chi_so"]
    bac_minh = CANH_GIOI.index(state["canh_gioi"])
    chenh = bac_minh - thu["bac"]
    goc = 50 + chenh * 22 + (cs["tan_cong"] - 5) * 3
    return max(5, min(95, goc))


def tl_danh(state: dict, so_hiep: int = 3) -> dict:
    """Đánh con đang nhắm. Thua thì bị thương, không chết, và KHÔNG gặp lại nó.

    Điểm quan trọng: thua xong thì con đó vào sổ `da_thua`, lượt sau bốc con khác.
    Người chơi không bao giờ bị kẹt với đúng con mình không đánh lại được.
    """
    loi = _tl_kiem_tra(state, "san")
    if loi:
        return loi
    tl = _tl(state)
    ma = tl.get("muc_tieu")
    thu = next((t for t in TL_YEU_THU if t["ma"] == ma), None)
    if thu is None or ma in _tl_con_thua(state):
        thu = _tl_chon_thu(state)
    ti_le = _ti_le_thang(state, thu)
    _tl_ghi(state, f"đánh {thu['ten']}", TL_VIEC["san"]["ngay"])
    cs = state["chi_so"]["sinh_luc"]
    dong = []
    thang = _tl_ngau(state) * 100 < ti_le
    for i in range(so_hiep):
        # Mỗi hiệp 1–2 sinh lực. Ba hiệp mất 3–6, một trận cả thua lẫn nghỉ vẫn
        # đánh tiếp được. Đo: 30 ngày săn thuần lên được tầng 2 ở 33/40 ván.
        tru = 1 + int(_tl_ngau(state) * 2)
        cs["hien"] = max(1, cs["hien"] - tru)
        dong.append(f"Hiệp {i + 1}: ngươi bị cắn, sinh lực -{tru} (còn {cs['hien']})")
        if cs["hien"] <= cs["max"] * 0.3:
            break
    tb = []
    if thang:
        _ap_hieu_ung(state, {"them_vat": [{"ten": thu["vat"], "so": thu["so_vat"]}]})
        tb = _ap_hieu_ung(state, {"tu_vi": thu["tu_vi"]})
        dong.append(f"— THẮNG: {thu['ten']} gục, {thu['vat']} +{thu['so_vat']}")
        if thu["ma"] in tl.get("da_thua", []):
            tl["da_thua"].remove(thu["ma"])
        tl["muc_tieu"] = None
    else:
        mat = 3
        cs["hien"] = max(1, cs["hien"] - mat)
        da_thua = tl.setdefault("da_thua", [])
        if thu["ma"] not in da_thua:
            da_thua.append(thu["ma"])
        tl["muc_tieu"] = None
        # Thua vẫn được tu vi: sống sót qua một trận là học được điều gì đó. Nếu
        # không có phần này thì săn cả 30 ngày chỉ được ~19 tu vi (cần 100) và
        # người chơi kẹt ở tầng 1 mãi.
        tb = _ap_hieu_ung(state, {"tu_vi": TL_TU_VI_THUA})
        dong.append(f"— THUA: bị thương, sinh lực -{mat}, tu vi +{TL_TU_VI_THUA}. "
                    "Lượt sau sẽ gặp con khác.")
    goi_y = _tl_chon_thu(state)
    return {"ok": True, "thang": thang, "dong": dong,
            "thong_bao": tb, "chi_so": _tl_chi_so(state),
            "muc_tieu_sau": {"ten": goi_y["ten"], "hang": goi_y["hang"],
                             "ti_le": _ti_le_thang(state, goi_y)}}


def tl_cong_thuc(state: dict) -> list[dict]:
    """Danh sách công thức kèm nguyên liệu ĐANG CÓ / CẦN, để bấm là biết ngay."""
    ra = []
    for ct in TL_CONG_THUC:
        can = []
        du = True
        for ten, so in ct["can"].items():
            co = _tl_co(state, ten)
            if co < so:
                du = False
            can.append({"ten": ten, "can": so, "co": co})
        if _tl_co(state, "Bạc vụn") < ct["bac"] and state["bac"] < ct["bac"]:
            du = False
        ra.append({**ct, "can_chi_tiet": can, "duoc": du})
    return ra


def tl_luyen_dan(state: dict, ma: str) -> dict:
    ct = next((c for c in TL_CONG_THUC if c["ma"] == ma), None)
    if ct is None:
        return {"loi": "Công thức không có"}
    if not _tl_con_ngay(state, ct["ngay"]):
        return {"loi": f"Không đủ ngày (cần {ct['ngay']})"}
    for ten, so in ct["can"].items():
        if _tl_co(state, ten) < so:
            return {"loi": f"Thiếu {ten} (cần {so}, có {_tl_co(state, ten)})"}
    if state["bac"] < ct["bac"]:
        return {"loi": f"Không đủ bạc (cần {ct['bac']})"}
    for ten, so in ct["can"].items():
        _tl_bot(state, ten, so)
    state["bac"] -= ct["bac"]
    _tl_ghi(state, f"luyện {ct['ten']}", ct["ngay"])
    if _tl_ngau(state) * 100 < ct["ti_le"]:
        tb = []
        hieu = {}
        if "tu_vi" in ct:
            hieu["tu_vi"] = ct["tu_vi"]
        if "sinh_luc" in ct:
            hieu["sinh_luc"] = ct["sinh_luc"]
        hieu["them_vat"] = [{"ten": ct["ten"], "so": 1}]
        tb += _ap_hieu_ung(state, hieu)
        return {"ok": True, "thanh_cong": True,
                "thong_bao": [f"Ra lò {ct['ten']}!"] + tb, "chi_so": _tl_chi_so(state)}
    return {"ok": True, "thanh_cong": False,
            "thong_bao": [f"Mẻ {ct['ten']} hỏng — mất nguyên liệu"], "chi_so": _tl_chi_so(state)}


def tl_cho(state: dict) -> list[dict]:
    return [dict(h) for h in TL_CHO_HANG]


def tl_mua(state: dict, ma: str) -> dict:
    hang = next((h for h in TL_CHO_HANG if h["ma"] == ma), None)
    if hang is None:
        return {"loi": "Món này không bán"}
    if not _tl_con_ngay(state, TL_VIEC["cho"]["ngay"]):
        return {"loi": "Không đủ ngày"}
    if state["bac"] < hang["gia"]:
        return {"loi": f"Không đủ bạc (cần {hang['gia']}, có {state['bac']})"}
    state["bac"] -= hang["gia"]
    _tl_ghi(state, f"mua {hang['ten']}", TL_VIEC["cho"]["ngay"])
    _ap_hieu_ung(state, {"them_vat": [{"ten": hang["ten"], "so": hang["so"]}]})
    tb = []
    return {"ok": True, "thong_bao": [f"Mua {hang['ten']} (-{hang['gia']} bạc)"] + tb,
            "chi_so": _tl_chi_so(state)}


def tl_ban(state: dict, ten: str, so: int = 1) -> dict:
    """Bán nguyên liệu hoặc đan dược lấy bạc.

    Chợ trước đây chỉ bán ra, nên mọi thứ săn được đều nằm chết trong túi: người
    chơi có 20 nanh sói mà không có bạc để mua linh thảo luyện đan. Đó là ngõ cụt
    kinh tế, không phải chuyện cân bằng.
    """
    so = max(1, int(so or 1))
    if state.get("ket_thuc"):
        return {"loi": "Chương đã khép lại — không tu luyện được nữa"}
    gia = TL_BAN_GIA.get(ten)
    if gia is None:
        return {"loi": f"Chợ không thu {ten}"}
    if not _tl_con_ngay(state, TL_VIEC["cho"]["ngay"]):
        return {"loi": "Không đủ ngày"}
    co = _tl_co(state, ten)
    if co < so:
        return {"loi": f"Không đủ {ten} (cần {so}, có {co})"}
    _tl_ghi(state, f"bán {ten} x{so}", TL_VIEC["cho"]["ngay"])
    _tl_bot(state, ten, so)
    state["bac"] += gia * so
    return {"ok": True, "thong_bao": [f"Bán {ten} x{so} (+{gia * so} bạc)"],
            "chi_so": _tl_chi_so(state)}


def tl_ban_duoc(state: dict) -> list[dict]:
    """Những thứ trong túi mà chợ thu, kèm giá — để giao diện hiện trước khi bấm."""
    ra = []
    for v in state.get("tui_do", []):
        ten, so = v.get("ten"), v.get("so") or 0
        gia = TL_BAN_GIA.get(ten)
        if gia is not None and so > 0:
            ra.append({"ten": ten, "so": so, "gia": gia})
    return ra


def tl_do_la(state: dict) -> dict:
    """Dò la: TỐN ngày, tin ra NGẪU NHIÊN (có hạt giống) — không chắc ra tin quan trọng."""
    loi = _tl_kiem_tra(state, "do_la")
    if loi:
        return loi
    _tl_ghi(state, "dò la", TL_VIEC["do_la"]["ngay"])
    tl = _tl(state)
    con = [t for t in TL_TIN if t["ma"] not in tl["tin_da_biet"]]
    r = _tl_ngau(state)
    if r < 0.55 or not con:
        return {"ok": True, "tin": None,
                "thong_bao": ["Dò la cả buổi, chỉ nghe chuyện vặt — không có gì dùng được"],
                "chi_so": _tl_chi_so(state)}
    tin = con[int(r * 1000) % len(con)]
    tl["tin_da_biet"].append(tin["ma"])
    return {"ok": True, "tin": tin,
            "thong_bao": [f"Nghe được: {tin['ke']}"], "chi_so": _tl_chi_so(state)}


def tl_nghi(state: dict) -> dict:
    """Nghỉ một ngày để hồi sinh lực — cần thiết sau khi bị thương."""
    if not _tl_con_ngay(state, 1):
        return {"loi": "Không còn ngày để nghỉ"}
    _tl_ghi(state, "nghỉ cho hồi sức", 1)
    tb = _ap_hieu_ung(state, {"sinh_luc": 12})
    return {"ok": True, "thong_bao": ["Nghỉ một ngày."] + tb, "chi_so": _tl_chi_so(state)}


def vao_dong(state: dict) -> dict:
    """Bước vào động phủ. Chỉ số nền không đổi — đây là chế độ, không phải hành động."""
    if state.get("ket_thuc"):
        return {"loi": "Chương đã khép lại — không tu luyện được nữa"}
    state["trong_dong"] = True
    return {"ok": True, **tl_trang_thai(state)}


def ra_dong(state: dict) -> dict:
    """Xuất động: trả về màn truyện, chỉ số đã đổi. Đây là cầu nối hai phần."""
    state["trong_dong"] = False
    _ghi_nhat_ky(state, f"Xuất động (tu vi {state['tu_vi']['hien']}, {state['canh_gioi']})")
    kq = _goi_y(state) if not state.get("ket_thuc") else _man_ket_chuong(state)
    kq["thong_bao"] = [f"Xuất động: {state['canh_gioi']}, tu vi {state['tu_vi']['hien']}"]
    return kq





# ---------------------------------------------------------------- xuất thân

_xt_cache: dict | None = None


def load_xuat_than() -> dict:
    """Nạp bảng xuất thân (5 nhóm chơi được + 1 nhóm ẩn)."""
    global _xt_cache
    if _xt_cache is None:
        with open(XUAT_THAN_PATH, encoding="utf-8") as f:
            _xt_cache = json.load(f)
    return _xt_cache


def ds_xuat_than(ke_ca_an: bool = False) -> list[dict]:
    """Danh sách nhóm xuất thân cho giao diện (mặc định giấu nhóm ẩn)."""
    return [n for n in load_xuat_than()["nhom"] if ke_ca_an or not n.get("an")]


def _khong_dau(s: str) -> str:
    """Bỏ dấu tiếng Việt để dò từ khoá chắc chắn hơn."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")


def nhan_dien_xuat_than(xuat_than: str) -> str:
    """Xếp xuất thân tự do vào mã nhóm (không dùng AI — chỉ dò từ khoá).

    Không khớp gì → 'tan_tu'. Nhóm ẩn (Tuyết Cơ) KHÔNG bao giờ tự nhận.
    """
    t = _khong_dau(xuat_than or "")
    for n in load_xuat_than()["nhom"]:
        if n.get("an"):
            continue
        for tk in n.get("tu_khoa", []):
            if _khong_dau(tk) in t:
                return n["ma"]
    return "tan_tu"


def doan_dau_cua(nhom: str, so_chuong: int | None = None) -> str | None:
    """Đoạn mở đầu của một nhóm xuất thân trong một chương.

    Thứ tự dò: bảng `doan_dau_theo_nhom[nhóm]` của chương → khoá `chung` của bảng
    (chương đã gộp nhánh) → `doan_dau` của nhóm trong xuat_than.json → đoạn đầu
    tiên của chương. Bậc cuối là để chương gộp nhánh không làm chết người chơi.
    """
    if so_chuong is None:
        for n in load_xuat_than()["nhom"]:
            if n["ma"] == nhom:
                return n.get("doan_dau")
        return None
    try:
        ch = load_chuong(so_chuong)
    except FileNotFoundError:
        return None
    bang = ch.get("doan_dau_theo_nhom") or {}
    if nhom in bang:
        return bang[nhom]
    if "chung" in bang:
        return bang["chung"]
    for n in load_xuat_than()["nhom"]:
        if n["ma"] == nhom and n.get("doan_dau") in ch["_theo_id"]:
            return n["doan_dau"]
    dau = ch["doan"]
    return dau[0]["id"] if dau else None


# Chỉ số khởi đầu dùng chung khi nhóm không khai `chi_so_dau` (vd nhóm ẩn).
CHI_SO_DAU_MAC_DINH = {
    "bac": 3,
    "tu_vi": {"hien": 12, "max": 100},
    "chi_so": {
        "sinh_luc": {"hien": 30, "max": 30},
        "linh_luc": {"hien": 10, "max": 10},
        "than_niem": 8,
        "tan_cong": 5,
        "phong_thu": 3,
        "chi_mang": 2,
        "bao_kich": 150,
        "xuyen_giap": 0,
        "toc_do": 10,
    },
    "ky_nang": ["Hô hấp pháp", "Nhận biết linh khí"],
}


def chi_so_dau_cua(nhom: str) -> dict:
    """Chỉ số khởi đầu riêng của từng xuất thân (khai ở `chi_so_dau` trong JSON).

    Thiếu thì dùng bảng mặc định — nhóm ẩn không khai, và dữ liệu cũ vẫn chạy.
    """
    for n in load_xuat_than()["nhom"]:
        if n["ma"] == nhom and n.get("chi_so_dau"):
            return n["chi_so_dau"]
    return CHI_SO_DAU_MAC_DINH


def trang_thai_moi(ten_nhan_vat: str, xuat_than: str = "", nhom: str = "") -> dict:
    """Tạo trạng thái nhân vật mới ở Luyện Khí tầng 1.

    `nhom`: mã nhóm xuất thân (nếu người chơi bấm nút chọn sẵn). Bỏ trống thì
    tự xếp theo từ khoá trong `xuat_than`. Quyết định đoạn mở đầu của hành trình.
    """
    if not xuat_than.strip():
        xuat_than = "tán tu vô danh"
    hop_le = {n["ma"] for n in ds_xuat_than()}
    if nhom not in hop_le:
        nhom = nhan_dien_xuat_than(xuat_than)
    dau = chi_so_dau_cua(nhom)
    return {
        "ten_nhan_vat": ten_nhan_vat.strip() or "Vô Danh",
        "xuat_than": xuat_than.strip(),
        "nhom_xuat_than": nhom,
        "canh_gioi": CANH_GIOI[0],
        "tu_vi": dict(dau["tu_vi"]),
        "chi_so": {
            **{k: dict(v) if isinstance(v, dict) else v
               for k, v in dau["chi_so"].items()},
            "tan_cong_phep": _zero_he(),
            "khang_phep": _zero_he(),
        },
        "bac": dau["bac"],
        "tui_do": [
            {"ten": "Bạc vụn", "so": dau["bac"], "mo_ta": "Tiền tệ nơi phàm trần."},
        ],
        "ky_nang": list(dau["ky_nang"]),
        "co_su_kien": [],
        "npc": {},
        "nhat_ky": [],
        "tu_luyen": tl_moi(),
        "trong_dong": False,
        "chuong": 1,
        "doan_hien_tai": None,
        "da_qua": [],
        "ket_thuc": False,
        "tao_luc": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------- nạp chương

_cache: dict[int, dict] = {}


def kiem_chuong(data: dict) -> list[str]:
    """Liệt kê lỗi dữ liệu của một chương: mã đoạn trùng, đích trỏ vào hư không.

    Chạy ngay sau khi nạp để một chữ gõ sai báo lỗi rõ ràng, thay vì âm thầm
    đặt `ket_thuc` và cắt ngang chương giữa đường.
    """
    loi: list[str] = []
    ids = [d.get("id") for d in data.get("doan") or []]
    trung = {i for i in ids if ids.count(i) > 1}
    if trung:
        loi.append(f"mã đoạn trùng: {sorted(trung)}")
    co = set(ids)
    for d in data.get("doan") or []:
        for lc in d.get("lua_chon") or []:
            den = lc.get("den")
            if den != "__ket_thuc__" and den not in co:
                loi.append(f"{d.get('id')} → '{den}' không có đoạn này")
    for nhom, did in (data.get("doan_dau_theo_nhom") or {}).items():
        if did not in co:
            loi.append(f"doan_dau_theo_nhom[{nhom}] → '{did}' không có đoạn này")
    return loi


def load_chuong(so: int) -> dict:
    if so in _cache:
        return _cache[so]
    path = os.path.join(CHAPTERS_DIR, f"chuong{so}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    loi = kiem_chuong(data)
    if loi:
        raise ValueError(f"chuong{so}.json hỏng: " + "; ".join(loi[:5]))
    data["_theo_id"] = {d["id"]: d for d in data["doan"]}
    _cache[so] = data
    return data


def co_chuong(so: int) -> bool:
    """Chương đã có file dữ liệu chưa (dùng để khoá nút chuyển chương)."""
    return os.path.exists(os.path.join(CHAPTERS_DIR, f"chuong{so}.json"))


def _doan(state: dict) -> dict:
    ch = load_chuong(state["chuong"])
    did = state["doan_hien_tai"]
    if did is None:
        nhom = state.get("nhom_xuat_than") or "tan_tu"
        did = (doan_dau_cua(nhom, state["chuong"])
               or next(iter(ch["doan"]))["id"])
        if did not in ch["_theo_id"]:
            # Đoán bừa sẽ ném người chơi về đoạn 1 mà không ai biết vì sao.
            raise KeyError(
                f"Chương {state['chuong']} không có đoạn mở đầu '{did}' "
                f"cho nhóm '{nhom}' — kiểm doan_dau_theo_nhom trong chuong{state['chuong']}.json"
            )
        state["doan_hien_tai"] = did
    if did not in ch["_theo_id"]:
        raise KeyError(
            f"Chương {state['chuong']} không có đoạn '{did}' — "
            f"bản lưu trỏ tới đoạn không tồn tại"
        )
    d = ch["_theo_id"][did]
    _ap_hieu_ung_vao(state, d)
    return d


def _ap_hieu_ung_vao(state: dict, d: dict) -> None:
    """Hiệu ứng của chính đoạn, áp đúng một lần khi người chơi bước vào.

    Dùng cho thứ phải có mặt NGAY lúc mở đoạn — bạn đồng hành xuất hiện trong
    sổ NPC, cờ sự kiện bật sẵn — chứ không phải đợi bấm lựa chọn đầu tiên.
    """
    hu = d.get("hieu_ung_vao")
    if not hu:
        return
    da_ap = state.setdefault("da_ap_vao", [])
    if d["id"] in da_ap:
        return
    da_ap.append(d["id"])
    _ap_hieu_ung(state, hu)


# ---------------------------------------------------------------- tiện ích

def _dieu_kien_hop(state: dict, dk: dict | None) -> bool:
    """Kiểm tra điều kiện của một lựa chọn."""
    if not dk:
        return True
    if "nhom" in dk:
        ds = dk["nhom"]
        if isinstance(ds, str):
            ds = [ds]
        if (state.get("nhom_xuat_than") or "") not in ds:
            return False
    tien = dk.get("bac", dk.get("linh_thach"))
    if tien is not None and state["bac"] < tien:
        return False
    if "co_su_kien" in dk:
        if not all(f in state["co_su_kien"] for f in dk["co_su_kien"]):
            return False
    if "co_vat" in dk:
        co = {v["ten"] for v in state["tui_do"] if v.get("so", 0) > 0}
        if dk["co_vat"] not in co:
            return False
    if "hao_cam" in dk:
        for ten, toi_thieu in dk["hao_cam"].items():
            if state["npc"].get(ten, {}).get("hao_cam", 0) < toi_thieu:
                return False
    if "hao_cam_max" in dk:
        for ten, toi_da in dk["hao_cam_max"].items():
            if state["npc"].get(ten, {}).get("hao_cam", 0) > toi_da:
                return False
    if "canh_gioi" in dk:
        # Cổng boss: chỉ mở đường "đánh thẳng" khi đã đủ cảnh giới. So theo bậc
        # trong CANH_GIOI chứ không so chuỗi, để "tầng 10" không bị coi là thấp.
        can = dk["canh_gioi"]
        if state["canh_gioi"] not in CANH_GIOI or can not in CANH_GIOI:
            return False
        if CANH_GIOI.index(state["canh_gioi"]) < CANH_GIOI.index(can):
            return False
    if "tin" in dk:
        # Đường mưu qua cổng boss: phải dò la ra tin tương ứng trước.
        if dk["tin"] not in _tl(state)["tin_da_biet"]:
            return False
    if "co_tin" in dk:
        if not all(t in _tl(state)["tin_da_biet"] for t in dk["co_tin"]):
            return False
    return True


def _gap_npc(state: dict, ten: str, info: dict | None = None) -> None:
    """Ghi nhận đã gặp NPC; chỉ lưu chỉ số lần đầu, KHÔNG ghi đè hảo cảm đã có."""
    moi = ten not in state["npc"]
    if moi:
        state["npc"][ten] = {"hao_cam": 0, "thai_do": "người dưng"}
    if info:
        for k, v in info.items():
            if k == "hao_cam":
                if moi:
                    state["npc"][ten]["hao_cam"] = max(-100, min(100, v))
            else:
                state["npc"][ten][k] = v
    state["npc"][ten]["thai_do"] = muc_hao_cam(state["npc"][ten]["hao_cam"])


def _doi_hao_cam(state: dict, ten: str, delta: int) -> str:
    """Thay đổi hảo cảm với một NPC, trả về thông báo."""
    if ten not in state["npc"]:
        state["npc"][ten] = {"hao_cam": 0, "thai_do": "người dưng"}
    cu = state["npc"][ten]["hao_cam"]
    moi = max(-100, min(100, cu + delta))
    state["npc"][ten]["hao_cam"] = moi
    state["npc"][ten]["thai_do"] = muc_hao_cam(moi)
    dau = "+" if delta > 0 else ""
    return f"Hảo cảm {ten} {dau}{delta} ({muc_hao_cam(moi)})"


def _ap_hieu_ung(state: dict, hu: dict | None) -> list[str]:
    """Áp hiệu ứng của một lựa chọn. Trả về danh sách thông báo."""
    if not hu:
        return []
    tb = []
    tien = hu.get("bac", hu.get("linh_thach"))
    if tien is not None:
        state["bac"] = max(0, state["bac"] + tien)
        tb.append(f"Bạc {'+' if tien > 0 else ''}{tien}")
    if "tu_vi" in hu:
        tv = state["tu_vi"]
        tv["hien"] = min(tv["max"], tv["hien"] + hu["tu_vi"])
        tb.append(f"Tu vi +{hu['tu_vi']}")
        _thang_cap(state, tb)
    if "sinh_luc" in hu:
        sl = state["chi_so"]["sinh_luc"]
        sl["hien"] = max(0, min(sl["max"], sl["hien"] + hu["sinh_luc"]))
        tb.append(f"Sinh lực {'+' if hu['sinh_luc'] > 0 else ''}{hu['sinh_luc']}")
    if "than_niem" in hu:
        state["chi_so"]["than_niem"] = max(0, state["chi_so"]["than_niem"] + hu["than_niem"])
        tb.append(f"Thần niệm {'+' if hu['than_niem'] > 0 else ''}{hu['than_niem']}")
    if "co_su_kien" in hu:
        for f in hu["co_su_kien"]:
            if f not in state["co_su_kien"]:
                state["co_su_kien"].append(f)
    if "gap_npc" in hu:
        for ten, info in hu["gap_npc"].items():
            _gap_npc(state, ten, info)
            tb.append(f"Gặp: {ten}")
    if "hao_cam" in hu:
        for ten, delta in hu["hao_cam"].items():
            tb.append(_doi_hao_cam(state, ten, delta))
    if "them_vat" in hu:
        for v in hu["them_vat"]:
            _nhan_vat(state, v)
            tb.append(f"Nhận: {v['ten']}")
    if "doi_trang_thai" in hu:
        for ten, tt_moi in hu["doi_trang_thai"].items():
            for v in state["tui_do"]:
                if v["ten"] == ten:
                    v["trang_thai"] = tt_moi
                    tb.append(f"{ten}: {tt_moi}")
                    break
    if "ky_nang" in hu:
        for k in hu["ky_nang"]:
            if k not in state["ky_nang"]:
                state["ky_nang"].append(k)
                tb.append(f"Học được: {k}")
    return tb


def _nhan_vat(state: dict, v: dict) -> None:
    """Thêm vật phẩm vào túi, gộp số lượng nếu đã có món cùng tên cùng trạng thái."""
    if not isinstance(v, dict) or not (v.get("ten") or "").strip():
        return
    for cu in state["tui_do"]:
        if cu.get("ten") == v["ten"] and cu.get("trang_thai") == v.get("trang_thai"):
            cu["so"] = (cu.get("so") or 0) + (v.get("so") or 1)
            return
    moi = copy.deepcopy(v)
    moi.setdefault("so", 1)
    state["tui_do"].append(moi)


def _thang_cap(state: dict, tb: list[str]) -> None:
    """Tu vi đầy → lên tầng cảnh giới, nhưng không vượt trần của chương."""
    tv = state["tu_vi"]
    tran = TRAN_CANH_GIOI.get(state.get("chuong"))
    while tv["hien"] >= tv["max"]:
        idx = CANH_GIOI.index(state["canh_gioi"])
        if idx + 1 >= len(CANH_GIOI):
            break
        if tran is not None and idx + 1 >= CANH_GIOI.index(tran) + 1:
            # Chạm trần: giữ tu vi đầy, không lên tầng, báo để người chơi biết vì sao.
            tv["hien"] = tv["max"]
            if not any("chạm trần" in t for t in tb):
                tb.append(f"⚠ Đã chạm trần chương này ({tran}) — cần cơ duyên mới vượt được")
            break
        state["canh_gioi"] = CANH_GIOI[idx + 1]
        tv["hien"] = 0
        tv["max"] = int(tv["max"] * 1.35)
        cs = state["chi_so"]
        cs["sinh_luc"]["max"] += 6
        cs["sinh_luc"]["hien"] = cs["sinh_luc"]["max"]
        cs["linh_luc"]["max"] += 4
        cs["linh_luc"]["hien"] = cs["linh_luc"]["max"]
        cs["than_niem"] += 4
        cs["tan_cong"] += 2
        cs["phong_thu"] += 1
        tb.append(f"⚡ ĐỘT PHÁ: {state['canh_gioi']}!")


# ---------------------------------------------------------------- API chính

def bat_dau(state: dict) -> dict:
    """Vào đoạn đầu tiên của chương hiện tại."""
    return _goi_y(state)


def _ke_theo_hao_cam(d: dict, state: dict) -> str:
    """Chọn biến thể đoạn kể theo mức hảo cảm hiện tại với NPC của đoạn.

    Đoạn có thể khai báo `bien_the`: danh sách {npc, muc, ke}. Chọn biến thể
    có `muc` khớp (hoặc thấp hơn gần nhất) mức hảo cảm hiện tại của NPC đó.
    Không có biến thể nào khớp thì trả về `ke` gốc.
    """
    bts = d.get("bien_the") or []
    if not bts:
        return d.get("ke", "")
    thu_tu = [m[2] for m in MUC_HAO_CAM]  # tử địch … tri kỷ
    tot_nhat = None
    hang_tot_nhat = -99
    for bt in bts:
        npc = bt.get("npc")
        if npc and npc not in state["npc"]:
            continue
        diem = state["npc"].get(npc, {}).get("hao_cam", 0) if npc else 0
        muc_hien = muc_hao_cam(diem)
        if bt.get("muc") not in thu_tu:
            continue
        hang = thu_tu.index(bt["muc"])
        # Khớp đúng thì luôn thắng; không có khớp đúng thì lấy bậc thấp hơn gần
        # nhất — nhờ vậy một đoạn chỉ cần vài biến thể, không cần đủ sáu bậc.
        if hang <= thu_tu.index(muc_hien) and hang > hang_tot_nhat:
            hang_tot_nhat = hang
            tot_nhat = bt
    if tot_nhat is None:
        # NPC không có mặt trong cảnh (chưa từng gặp) thì dùng văn bản gốc; chỉ
        # khi NPC CÓ mặt mà hảo cảm còn thấp hơn biến thể thấp nhất mới lấy biến
        # thể thấp nhất.
        thu = [bt for bt in bts
               if (not bt.get("npc") or bt["npc"] in state["npc"])
               and bt.get("muc") in thu_tu]
        if thu:
            tot_nhat = min(thu, key=lambda bt: thu_tu.index(bt["muc"]))
    return tot_nhat["ke"] if tot_nhat else d.get("ke", "")


def _man_ket_chuong(state: dict) -> dict:
    """Màn hình khi đã khép chương (thay vì tra đoạn không tồn tại).

    Lời kết nằm trong chính file chương (`ket`), không viết cứng ở đây — nếu không,
    sang chương 2 sẽ vẫn hiện lời kết của chương 1.
    """
    ch = load_chuong(state["chuong"])
    ket = ch.get("ket") or {}
    sau = ket.get("chuong_sau") or state["chuong"] + 1
    return {
        "doan_id": "__ket_thuc__",
        "hoi": "Kết",
        "boi_canh": ket.get("boi_canh") or f"Chương {state['chuong']} — hết",
        "chuong": state["chuong"],
        "ten_chuong": ch["ten"],
        "ke": ket.get("ke") or f"Chương {state['chuong']} khép lại.",
        "hinh_anh": ket.get("hinh_anh"),
        "video": None,
        "lua_chon": [],
        "cho_phep_tu_do": False,
        "ket_thuc": True,
        "chuong_sau": sau,
        "chuong_sau_mo": co_chuong(sau),
        "thong_bao": [],
        "trang_thai": _trang_thai_gon(state),
    }


def sang_chuong(state: dict, so: int | None = None) -> dict:
    """Mang nguyên nhân vật sang chương sau, đứng ở đoạn mở đầu của nhóm mình.

    Chỉ đổi `chuong` + `doan_hien_tai`; cảnh giới, bạc, túi đồ, hảo cảm, cờ sự kiện
    giữ nguyên. `da_qua` cũng giữ nguyên vì mã đoạn có tiền tố chương nên không đụng nhau.
    """
    so = so if so is not None else (load_chuong(state["chuong"]).get("ket") or {}).get(
        "chuong_sau", state["chuong"] + 1)
    if not co_chuong(so):
        return {"loi": f"Chương {so} chưa mở"}
    state["chuong"] = so
    state["doan_hien_tai"] = None
    state["ket_thuc"] = False
    # Mỗi chương một ngân sách ngày riêng. Giữ `ngay_da_dung` để dãy ngẫu nhiên
    # không lặp lại y nguyên ở chương sau; tin đã biết cũng mang theo.
    tl = _tl(state)
    tl["ngay_con"] = NGAY_MOI_CHUONG
    tl["nhat_ky"].append(f"— Chương {so}: ngày mới, {NGAY_MOI_CHUONG} ngày —")
    _ghi_nhat_ky(state, f"Sang chương {so}")
    kq = _goi_y(state)
    kq["thong_bao"] = [f"— Chương {so}: {load_chuong(so)['ten']} —"]
    return kq


def _npc_trong_canh(d: dict, state: dict) -> list[dict]:
    """NPC của đoạn kèm mức hảo cảm hiện tại.

    Nguồn: `npc` khai báo ở đoạn, cộng mọi NPC mà `bien_the` nhắm tới — đoạn có
    biến thể giọng mà quên khai `npc` vẫn phải báo đúng thái độ cho AI kể.
    """
    ten = []
    for t in d.get("npc") or []:
        if t not in ten:
            ten.append(t)
    for bt in d.get("bien_the") or []:
        t = bt.get("npc")
        if t and t not in ten:
            ten.append(t)
    ra = []
    for t in ten:
        info = state["npc"].get(t)
        if info is None:
            # Chưa gặp thì chưa có thái độ — đừng bịa mức "người dưng".
            continue
        ra.append({
            "ten": t,
            "hao_cam": info.get("hao_cam", 0),
            "thai_do": info.get("thai_do") or muc_hao_cam(info.get("hao_cam", 0)),
        })
    return ra


def _doan_thua(state: dict) -> dict | None:
    """Đoạn kết thua đang đứng, nếu có.

    Kết thua là đoạn khai `ket_thuc: true` (+ `thua: true`) nằm trong chương,
    khác màn khép chương. Trả None khi đang ở màn khép chương bình thường.
    """
    if not state.get("ket_thuc"):
        return None

    ch = load_chuong(state["chuong"])
    d = ch["_theo_id"].get(state.get("doan_hien_tai"))
    if d and d.get("ket_thuc") and d.get("thua"):
        return d
    return None


def _man_ket_thua(state: dict, d: dict) -> dict:
    """Màn kết thua: không có nút sang chương, chỉ có lùi lại hoặc chơi lại."""
    return {
        "doan_id": d["id"],
        "hoi": d.get("hoi") or "Kết",
        "boi_canh": d.get("boi_canh"),
        "chuong": state["chuong"],
        "ten_chuong": load_chuong(state["chuong"])["ten"],
        "ke": d.get("ke", ""),
        "hinh_anh": d.get("hinh_anh"),
        "video": d.get("video"),
        "lua_chon": [],
        "cho_phep_tu_do": False,
        "ket_thuc": True,
        "thua": True,
        "chuong_sau": None,
        "chuong_sau_mo": False,
        "thong_bao": [],
        "trang_thai": _trang_thai_gon(state),
    }


def _goi_y(state: dict) -> dict:
    """Trả về đoạn hiện tại ở dạng cho giao diện (giấu thông tin nội bộ)."""
    if state.get("ket_thuc"):
        d_thua = _doan_thua(state)
        if d_thua:
            return _man_ket_thua(state, d_thua)
        return _man_ket_chuong(state)
    d = _doan(state)
    if d.get("thua") and d.get("ket_thuc"):
        # Đặt cờ để bản lưu và payload khớp nhau; `_doan_thua` dựa vào cờ này.
        state["ket_thuc"] = True
        return _man_ket_thua(state, d)

    lua_chon = []
    for i, lc in enumerate(d.get("lua_chon", [])):
        hop = _dieu_kien_hop(state, lc.get("dieu_kien"))
        lua_chon.append({
            "chi_so": i,
            "chu": lc["chu"],
            "khoa": not hop,
            "ly_do_khoa": lc.get("ly_do_khoa", "Chưa đủ điều kiện") if not hop else None,
        })
    return {
        "doan_id": d["id"],
        "hoi": d.get("hoi"),
        "boi_canh": d.get("boi_canh"),
        "chuong": state["chuong"],
        "ten_chuong": load_chuong(state["chuong"])["ten"],
        "ke": _ke_theo_hao_cam(d, state),
        "npc_trong_canh": _npc_trong_canh(d, state),
        "hinh_anh": d.get("hinh_anh"),
        "video": d.get("video"),
        "lua_chon": lua_chon,
        "cho_phep_tu_do": d.get("cho_phep_tu_do", True),
        "ket_thuc": d.get("ket_thuc", False),
        "thong_bao": [],
        "trang_thai": _trang_thai_gon(state),
    }


def goi_y_hien_tai(state: dict) -> dict:
    """Trả về đoạn đang dừng (dùng khi nạp lại phiên)."""
    return _goi_y(state)


def _trang_thai_gon(state: dict) -> dict:
    cs = state["chi_so"]
    return {
        "ten_nhan_vat": state["ten_nhan_vat"],
        "xuat_than": state["xuat_than"],
        "nhom_xuat_than": state.get("nhom_xuat_than", ""),
        "canh_gioi": state["canh_gioi"],
        "tu_vi": dict(state["tu_vi"]),
        "sinh_luc": dict(cs["sinh_luc"]),
        "linh_luc": dict(cs["linh_luc"]),
        "than_niem": cs["than_niem"],
        "tan_cong": cs["tan_cong"],
        "phong_thu": cs["phong_thu"],
        "toc_do": cs["toc_do"],
        "bac": state["bac"],
        "linh_thach": state["bac"],
        "tui_do": [dict(v) for v in state["tui_do"]],
        "ky_nang": list(state["ky_nang"]),
        "npc": {k: dict(v) for k, v in state["npc"].items()},
        "co_su_kien": list(state["co_su_kien"]),
        "chuong": state["chuong"],
    }


def chon(state: dict, chi_so: int) -> dict:
    """Người chơi bấm một lựa chọn."""
    if state.get("ket_thuc"):
        return _goi_y(state)
    try:
        chi_so = int(chi_so)
    except (TypeError, ValueError):
        return {"loi": "Lựa chọn không hợp lệ"}
    d = _doan(state)
    lcs = d.get("lua_chon", [])
    if not (0 <= chi_so < len(lcs)):
        return {"loi": "Lựa chọn không hợp lệ"}
    lc = lcs[chi_so]
    if not _dieu_kien_hop(state, lc.get("dieu_kien")):
        return {"loi": lc.get("ly_do_khoa", "Chưa đủ điều kiện")}

    tb = _ap_hieu_ung(state, lc.get("hieu_ung"))
    _ghi_nhat_ky(state, f"Chọn: {lc['chu']}")
    _chuyen_doan(state, lc["den"])

    ket_qua = _goi_y(state)
    ket_qua["thong_bao"] = tb
    return ket_qua


def _boi_canh(state: dict) -> str:
    """Bối cảnh ngắn cho AI nhận diện hành động tự do."""
    if state.get("ket_thuc"):
        return "Chương đã khép lại."
    d = _doan(state)
    npc = ", ".join(f"{ten} (hảo cảm {v['hao_cam']})" for ten, v in state["npc"].items())
    return (
        f"Xuất thân người chơi: {state.get('xuat_than', '')}. "
        f"Đoạn: {d.get('boi_canh', '')}. Cảnh giới: {state['canh_gioi']}. "
        f"Sinh lực {state['chi_so']['sinh_luc']['hien']}/{state['chi_so']['sinh_luc']['max']}. "
        f"NPC đã gặp: {npc or 'chưa gặp ai'}."
    )


def _so_nguyen(v) -> int | None:
    """Ép về số nguyên nếu hợp lệ; ngược lại trả None."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return int(v)


def _loc_y_dinh(state: dict, y: dict) -> dict:
    """Chỉ giữ thay đổi hợp lệ: khoá đã biết + NPC đã gặp + trong giới hạn.

    Chống dữ liệu rác từ AI: None, chuỗi, số ngoài miền, NPC lạ.
    """
    hu: dict = {}
    for khoa, (lo, hi) in (("sinh_luc", (-15, 10)), ("tu_vi", (0, 8)),
                           ("bac", (-10, 10)), ("than_niem", (0, 2))):
        n = _so_nguyen(y.get(khoa))
        if n is not None:
            hu[khoa] = max(lo, min(hi, n))
    hc = {}
    hc_in = y.get("hao_cam")
    if not isinstance(hc_in, dict):
        hc_in = {}
    for ten, delta in hc_in.items():
        n = _so_nguyen(delta)
        if n is not None and ten in state["npc"]:  # chỉ đổi hảo cảm với NPC đã gặp
            hc[ten] = max(-10, min(10, n))
    if hc:
        hu["hao_cam"] = hc
    return hu


def hanh_dong_tu_do(state: dict, van_ban: str, AI=None) -> dict:
    """Người chơi gõ hành động tự do.

    Chế độ không AI: trả về đoạn kể chung và GIỮ NGUYÊN đoạn hiện tại (không lạc truyện).
    Chế độ có AI: AI đọc hành động → áp thay đổi chỉ số NHỎ (đã lọc), rồi kể lại đoạn.
    Đoạn truyện KHÔNG đổi — chỉ chỉ số/hảo cảm thay đổi.
    """
    van_ban = van_ban.strip() if isinstance(van_ban, str) else ""
    if not van_ban:
        return {"loi": "Hãy nhập hành động"}
    if state.get("ket_thuc"):
        return {"loi": "Chương đã khép lại"}
    d = _doan(state)
    _ghi_nhat_ky(state, f"Tự do: {van_ban}")
    hien_thi = van_ban[3:] if van_ban.lower().startswith("ta ") else van_ban
    tb = [f"(tự do) Ta {hien_thi}…"]
    y_dinh: dict = {}
    if AI is not None:
        try:
            if AI.san_sang():
                y_dinh = AI.nhan_dien(van_ban, _boi_canh(state))
        except Exception:  # noqa: BLE001 - AI lỗi thì bỏ qua, không áp gì
            y_dinh = {}
    if not isinstance(y_dinh, dict):
        y_dinh = {}
    hu = _loc_y_dinh(state, y_dinh)
    if hu:
        tb.extend(_ap_hieu_ung(state, hu))
    if y_dinh.get("nhan_xet"):
        tb.append(f"⟡ {y_dinh['nhan_xet']}")

    ket_qua = _goi_y(state)
    ket_qua["thong_bao"] = tb
    if AI is not None:
        try:
            if AI.san_sang():
                thay_doi = "; ".join(tb[1:]) or "không đổi chỉ số"
                ket_qua["ke"] = AI.ke_lai(d.get("ke", ""), van_ban, thay_doi)
                tb.append("AI kể: kết quả có thể khác mỗi lần")
                return ket_qua
        except Exception:  # noqa: BLE001 - AI lỗi thì rơi về chế độ viết sẵn
            pass
    ket_qua["ke"] = (
        f"Ta {van_ban}. Chưa có gì đổi khác rõ rệt, nhưng ta cảm thấy "
        f"thời cơ đang tới gần.\n\n" + (d.get("ke", "") or "")
    )
    return ket_qua


def _chuyen_doan(state: dict, den: str) -> None:
    if state["doan_hien_tai"] not in state["da_qua"]:
        state["da_qua"].append(state["doan_hien_tai"])
    state["doan_hien_tai"] = den
    ch = load_chuong(state["chuong"])
    if den not in ch["_theo_id"]:
        state["ket_thuc"] = True


def _ghi_nhat_ky(state: dict, viec: str) -> None:
    state["nhat_ky"].append({"luc": datetime.now().isoformat(timespec="seconds"), "viec": viec})
    if len(state["nhat_ky"]) > 60:
        state["nhat_ky"] = state["nhat_ky"][-60:]


# ---------------------------------------------------------------- lưu / nạp

def _safe_name(ten: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", ten)[:40] or "khach"


def luu(state: dict, slot: str) -> str:
    os.makedirs(SAVES_DIR, exist_ok=True)
    path = os.path.join(SAVES_DIR, f"{_safe_name(slot)}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return path


def nap(slot: str) -> dict | None:
    path = os.path.join(SAVES_DIR, f"{_safe_name(slot)}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        state = json.load(f)
    # Bản lưu cũ dùng "linh_thach" → nay là "bac"
    if "bac" not in state:
        state["bac"] = state.pop("linh_thach", 0)
    return state


def tom_tat(state: dict) -> str:
    """Tóm tắt luỹ tiến — dùng cho thẻ ngữ cảnh gửi AI (tiết kiệm token)."""
    if state.get("ket_thuc"):
        return f"Chương {state['chuong']} đã khép lại."
    d = _doan(state)
    npcs = ", ".join(
        f"{ten} ({v.get('hao_cam', 0):+d})" for ten, v in state["npc"].items()
    ) or "chưa gặp ai"
    return (
        f"Chương {state['chuong']}: {load_chuong(state['chuong'])['ten']}. "
        f"Đoạn {d['id']} ({d.get('boi_canh')}). "
        f"Cảnh giới {state['canh_gioi']}, bạc {state['bac']}. "
        f"Nhân vật đã gặp: {npcs}. "
        f"Sự kiện: {', '.join(state['co_su_kien']) or 'chưa có'}."
    )
