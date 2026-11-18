#!/usr/bin/env python3
"""Xử lý ảnh Xưởng TỰ ĐỘNG: nhận diện → nén → lưu → ghép vào đúng đoạn.

Đầu vào: danh sách ảnh [{name, data(base64), hint_key?}].
  - hint_key: nếu biết chắc key (ví dụ thư mục upload tên đúng key) thì bỏ qua AI.
  - Không có hint_key → dùng AI vision đối chiếu với các asset CÒN THIẾU.

Việc làm:
  1. Nhận diện mỗi ảnh ứng với asset (prompt) nào.
  2. Nén theo quy tắc (game.nen_anh) và lưu vào assets/ + docs/assets/.
  3. Ghép vào đúng đoạn trong chuong1.json (cả bản Python lẫn bản JS).
  4. Cập nhật docs/assets/library/index.json.

Trả báo cáo: {da_xu_ly: [...], can_nguoi_xac_nhan: [...], bo_qua: [...]}.
"""

from __future__ import annotations

import base64
import json
import os
import re

import tools_server as TS
from game import nhan_dien_anh as ND

ROOT = os.path.dirname(os.path.abspath(__file__))

CHUONG_FILES = [
    "game/chapters/chuong1.json",
    "docs/game/du-lieu/chuong1.json",
]
LIB_FILE = "docs/assets/library/index.json"

NGUONG_TU_DONG = 80  # độ tin cậy tối thiểu để tự gán


# ------------------------------------------------------------------ nhận diện
def _mime(ten: str) -> str:
    t = ten.lower()
    if t.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if t.endswith(".webp"):
        return "image/webp"
    if t.endswith(".gif"):
        return "image/gif"
    return "image/png"


def asset_con_thieu() -> list:
    """Các asset chưa có file trong game (ứng viên để nhận diện)."""
    co = {fn for fn, _ in TS.list_files(TS.UI_DIR) + TS.list_files(TS.SCENE_DIR)}
    return [a for a in TS.ASSETS if a["file"] not in co]


def _asset_theo_key(key: str):
    return next((a for a in TS.ASSETS if a["key"] == key), None)


def nhan_dien(anh_list: list, env: dict, chi_con_thieu: bool = True) -> list:
    """Nhận diện từng ảnh. Trả [{name, key, do_tin_cay, mo_ta, ly_do, kich_thuoc, cach, data}]."""
    ung_vien = asset_con_thieu() if chi_con_thieu else list(TS.ASSETS)
    hop_le = {a["key"] for a in ung_vien}
    kq = []
    for item in anh_list:
        ten = os.path.basename(item.get("name", "") or "image")
        data = base64.b64decode(item.get("data", ""))
        hint = (item.get("hint_key") or "").strip()

        # Có gợi ý key (thư mục đặt đúng tên key) → tin tuyệt đối.
        if hint and _asset_theo_key(hint):
            kq.append({"name": ten, "data": data, "key": hint, "do_tin_cay": 100,
                       "cach": "thu-muc", "mo_ta": "", "ly_do": "Thư mục upload đặt đúng mã ảnh.",
                       "kich_thuoc": ""})
            continue

        # Nếu trong tên file có sẵn mã key → nhận luôn (không cần AI).
        khop = next((k for k in hop_le if k in ten), "")
        if khop:
            kq.append({"name": ten, "data": data, "key": khop, "do_tin_cay": 100,
                       "cach": "ten-file", "mo_ta": "", "ly_do": "Tên file chứa mã ảnh.",
                       "kich_thuoc": ""})
            continue

        r = ND.goi_y_mot_anh(data, _mime(ten), ung_vien, env)
        r.update({"name": ten, "data": data, "cach": "ai"})
        kq.append(r)
    return kq


# ------------------------------------------------------------------ ghép dữ liệu
def _nap_json(rel: str):
    p = os.path.join(ROOT, rel)
    with open(p, encoding="utf-8") as f:
        return p, json.load(f)


def _ghi_json(p: str, obj) -> None:
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _gan_doan(chuong: dict, key: str, ten_file: str) -> list:
    """Gán tên ảnh cho các đoạn của asset. Trả danh sách đoạn đã gán."""
    doan_ids = TS.doan_cua(key)
    if not doan_ids:
        return []
    theo_id = {d["id"]: d for d in chuong.get("doan", [])}
    da_gan = []
    for did in doan_ids:
        d = theo_id.get(did)
        if d is None:
            continue
        d.setdefault("hinh_anh", {})["anh"] = ten_file
        da_gan.append(did)
    return da_gan


def _cap_nhat_thu_vien(lib: dict, key: str, ten_file: str, da_gan: list) -> None:
    """Thêm/sửa mục thư viện: ảnh này dùng ở `da_gan`, gỡ khỏi các ảnh khác."""
    anh = lib.setdefault("anh", {})
    a = _asset_theo_key(key)
    # gỡ các đoạn này khỏi mọi mục khác
    for fn, muc in anh.items():
        if fn == ten_file:
            continue
        if isinstance(muc.get("dung_o"), list):
            muc["dung_o"] = [x for x in muc["dung_o"] if x not in da_gan]
    muc = anh.get(ten_file) or {}
    muc.setdefault("loai", _loai_cua(key))
    muc.setdefault("mo_ta", (a or {}).get("use", "")[:200])
    muc.setdefault("tags", [])
    muc["dung_o"] = da_gan
    anh[ten_file] = muc


def _loai_cua(key: str) -> str:
    if key.startswith("bc_"):
        return "boi_canh"
    if key.startswith("vt_"):
        return "vat_pham"
    if key.startswith("nv_"):
        return "nhan_vat"
    return "giao_dien"


def luu_va_ghep(ket_qua: list) -> dict:
    """Lưu ảnh đã xác định key + ghép vào đoạn. Trả báo cáo."""
    da_luu, bo_qua = [], []
    can_xac_nhan = []
    for r in ket_qua:
        key = r.get("key") or ""
        if not key or not _asset_theo_key(key):
            can_xac_nhan.append({"name": r.get("name"), "ly_do": r.get("ly_do") or "AI không chắc",
                                 "mo_ta": r.get("mo_ta") or "", "do_tin_cay": r.get("do_tin_cay", 0)})
            continue
        if r.get("cach") == "ai" and r.get("do_tin_cay", 0) < NGUONG_TU_DONG:
            can_xac_nhan.append({"name": r.get("name"), "key": key,
                                 "do_tin_cay": r.get("do_tin_cay", 0),
                                 "ly_do": r.get("ly_do") or "", "mo_ta": r.get("mo_ta") or ""})
            continue
        b64 = base64.b64encode(r["data"]).decode() if isinstance(r.get("data"), (bytes, bytearray)) else r.get("data")
        try:
            ten_file = TS.luu_theo_key(key, b64)
            da_luu.append({"name": r.get("name"), "key": key, "file": ten_file,
                           "cach": r.get("cach"), "do_tin_cay": r.get("do_tin_cay")})
        except Exception as e:  # noqa: BLE001
            bo_qua.append({"name": r.get("name"), "key": key, "ly_do": str(e)})

    if not da_luu:
        return {"da_luu": [], "can_xac_nhan": can_xac_nhan, "bo_qua": bo_qua,
                "ghep": {}, "thong_diep": "Không có ảnh nào được lưu."}

    # ghép vào dữ liệu chương (cả 2 bản)
    ghep = {}
    for rel in CHUONG_FILES:
        p, chuong = _nap_json(rel)
        for x in da_luu:
            gan = _gan_doan(chuong, x["key"], x["file"])
            if gan:
                ghep.setdefault(x["file"], gan)
        _ghi_json(p, chuong)

    # cập nhật thư viện
    p, lib = _nap_json(LIB_FILE)
    for x in da_luu:
        _cap_nhat_thu_vien(lib, x["key"], x["file"], ghep.get(x["file"], []))
    _ghi_json(p, lib)

    return {"da_luu": da_luu, "can_xac_nhan": can_xac_nhan, "bo_qua": bo_qua, "ghep": ghep,
            "thong_diep": f"Đã lưu và ghép {len(da_luu)} ảnh."}


def xu_ly(anh_list: list, env: dict | None = None, chi_con_thieu: bool = True) -> dict:
    """Luồng đầy đủ: nhận diện → lưu → ghép."""
    env = env or TS.load_env()
    ket_qua = nhan_dien(anh_list, env, chi_con_thieu=chi_con_thieu)
    bc = luu_va_ghep(ket_qua)
    bc["nhan_dien"] = [{k: v for k, v in r.items() if k != "data"} for r in ket_qua]
    return bc
