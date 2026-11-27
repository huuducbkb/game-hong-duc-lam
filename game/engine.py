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



def _noi_chuyen_tiep(ket_qua: dict, lc: dict) -> None:
    """Nối câu chuyển tiếp của lựa chọn vào đầu đoạn kế.

    Nhiều lựa chọn cùng trỏ về một đoạn (để khỏi nhân bản cảnh). Không có câu
    nối thì người chơi bấm "Hỏi" hay "Rời đi" đều thấy y hệt một cảnh, không
    biết mình vừa chọn gì. Câu nối lấy từ `lua_chon[].ket_qua`.
    """
    noi = (lc.get("ket_qua") or "").strip()
    if not noi:
        return
    ke = ket_qua.get("ke") or ""
    ket_qua["ke"] = f"{noi}\n\n{ke}" if ke else noi


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


def _goi_y(state: dict) -> dict:
    """Trả về đoạn hiện tại ở dạng cho giao diện (giấu thông tin nội bộ)."""
    if state.get("ket_thuc"):
        return _man_ket_chuong(state)
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
    _noi_chuyen_tiep(ket_qua, lc)
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
