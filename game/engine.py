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
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(ROOT, "game", "chapters")
SAVES_DIR = os.path.join(ROOT, "data", "saves")

HE_PHAP = ["kim", "moc", "thuy", "hoa", "tho", "loi", "phong", "bang", "doc"]

CANH_GIOI = [
    "Luyện Khí tầng 1", "Luyện Khí tầng 2", "Luyện Khí tầng 3", "Luyện Khí tầng 4",
    "Luyện Khí tầng 5", "Luyện Khí tầng 6", "Luyện Khí tầng 7", "Luyện Khí tầng 8",
    "Luyện Khí tầng 9", "Luyện Khí tầng 10", "Luyện Khí tầng 11", "Luyện Khí tầng 12",
    "Luyện Khí tầng 13", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần",
]


def _zero_he():
    return {h: 0 for h in HE_PHAP}


def trang_thai_moi(ten_nhan_vat: str, xuat_than: str = "") -> dict:
    """Tạo trạng thái nhân vật mới ở Luyện Khí tầng 1."""
    if not xuat_than.strip():
        xuat_than = "tán tu vô danh"
    return {
        "ten_nhan_vat": ten_nhan_vat.strip() or "Vô Danh",
        "xuat_than": xuat_than.strip(),
        "canh_gioi": CANH_GIOI[0],
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
            "tan_cong_phep": _zero_he(),
            "khang_phep": _zero_he(),
        },
        "linh_thach": 3,
        "tui_do": [
            {"ten": "Ngọc vụn bí ẩn", "so": 1, "mo_ta": "Mảnh ngọc còn ấm, phát sáng mờ khi gặp linh khí."},
            {"ten": "Linh thạch hạ phẩm", "so": 3, "mo_ta": "Tiền tệ tu tiên giới."},
        ],
        "ky_nang": ["Hô hấp pháp", "Nhận biết linh khí"],
        "co_su_kien": [],
        "npc_da_gap": {},
        "nhat_ky": [],
        "chuong": 1,
        "doan_hien_tai": None,
        "da_qua": [],
        "ket_thuc": False,
        "tao_luc": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------- nạp chương

_cache: dict[int, dict] = {}


def load_chuong(so: int) -> dict:
    if so in _cache:
        return _cache[so]
    path = os.path.join(CHAPTERS_DIR, f"chuong{so}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["_theo_id"] = {d["id"]: d for d in data["doan"]}
    _cache[so] = data
    return data


def _doan(state: dict) -> dict:
    ch = load_chuong(state["chuong"])
    did = state["doan_hien_tai"]
    if did is None:
        did = ch["doan"][0]["id"]
        state["doan_hien_tai"] = did
    return ch["_theo_id"][did]


# ---------------------------------------------------------------- tiện ích

def _dieu_kien_hop(state: dict, dk: dict | None) -> bool:
    """Kiểm tra điều kiện của một lựa chọn."""
    if not dk:
        return True
    if "linh_thach" in dk and state["linh_thach"] < dk["linh_thach"]:
        return False
    if "co_su_kien" in dk:
        if not all(f in state["co_su_kien"] for f in dk["co_su_kien"]):
            return False
    if "co_vat" in dk:
        co = {v["ten"] for v in state["tui_do"] if v.get("so", 0) > 0}
        if dk["co_vat"] not in co:
            return False
    return True


def _ap_hieu_ung(state: dict, hu: dict | None) -> list[str]:
    """Áp hiệu ứng của một lựa chọn. Trả về danh sách thông báo."""
    if not hu:
        return []
    tb = []
    if "linh_thach" in hu:
        state["linh_thach"] = max(0, state["linh_thach"] + hu["linh_thach"])
        tb.append(f"Linh thạch {'+' if hu['linh_thach'] > 0 else ''}{hu['linh_thach']}")
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
    if "npc" in hu:
        for ten, thai_do in hu["npc"].items():
            state["npc_da_gap"][ten] = thai_do
    if "them_vat" in hu:
        for v in hu["them_vat"]:
            state["tui_do"].append(copy.deepcopy(v))
            tb.append(f"Nhận: {v['ten']}")
    if "ky_nang" in hu:
        for k in hu["ky_nang"]:
            if k not in state["ky_nang"]:
                state["ky_nang"].append(k)
                tb.append(f"Học được: {k}")
    return tb


def _thang_cap(state: dict, tb: list[str]) -> None:
    """Tu vi đầy → lên tầng cảnh giới."""
    tv = state["tu_vi"]
    while tv["hien"] >= tv["max"]:
        idx = CANH_GIOI.index(state["canh_gioi"])
        if idx + 1 >= len(CANH_GIOI):
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


def _goi_y(state: dict) -> dict:
    """Trả về đoạn hiện tại ở dạng cho giao diện (giấu thông tin nội bộ)."""
    d = _doan(state)
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
        "ke": d.get("ke", ""),
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
        "canh_gioi": state["canh_gioi"],
        "tu_vi": dict(state["tu_vi"]),
        "sinh_luc": dict(cs["sinh_luc"]),
        "linh_luc": dict(cs["linh_luc"]),
        "than_niem": cs["than_niem"],
        "tan_cong": cs["tan_cong"],
        "phong_thu": cs["phong_thu"],
        "toc_do": cs["toc_do"],
        "linh_thach": state["linh_thach"],
        "tui_do": [dict(v) for v in state["tui_do"]],
        "ky_nang": list(state["ky_nang"]),
        "npc_da_gap": dict(state["npc_da_gap"]),
        "co_su_kien": list(state["co_su_kien"]),
        "chuong": state["chuong"],
    }


def chon(state: dict, chi_so: int) -> dict:
    """Người chơi bấm một lựa chọn."""
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


def hanh_dong_tu_do(state: dict, van_ban: str) -> dict:
    """Người chơi gõ hành động tự do.

    Ở chế độ không AI, engine trả về một đoạn kể chung và giữ nguyên đoạn hiện tại
    (không lạc truyện). Chế độ AI sẽ do lớp LLM đảm nhiệm.
    """
    van_ban = van_ban.strip()
    if not van_ban:
        return {"loi": "Hãy nhập hành động"}
    d = _doan(state)
    _ghi_nhat_ky(state, f"Tự do: {van_ban}")
    ket_qua = _goi_y(state)
    ket_qua["thong_bao"] = [f"(tự do) Ngươi {van_ban}…"]
    ket_qua["ke"] = (
        f"Ngươi {van_ban}. Chưa có gì đổi khác rõ rệt, nhưng ngươi cảm thấy "
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
        return json.load(f)


def tom_tat(state: dict) -> str:
    """Tóm tắt luỹ tiến — dùng cho thẻ ngữ cảnh gửi AI (tiết kiệm token)."""
    d = _doan(state)
    npcs = ", ".join(state["npc_da_gap"]) or "chưa gặp ai"
    return (
        f"Chương {state['chuong']}: {load_chuong(state['chuong'])['ten']}. "
        f"Đoạn {d['id']} ({d.get('boi_canh')}). "
        f"Cảnh giới {state['canh_gioi']}, linh thạch {state['linh_thach']}. "
        f"Nhân vật đã gặp: {npcs}. "
        f"Sự kiện: {', '.join(state['co_su_kien']) or 'chưa có'}."
    )
