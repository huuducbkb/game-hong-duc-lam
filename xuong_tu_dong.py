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
import sys

import tools_server as TS
from game import nhan_dien_anh as ND

# tools/ chứa xuong_video.py và build_xuong_video.py — thêm vào path để import được
# dù chạy từ gốc repo (GitHub Action chạy `python3 tools/xu_ly_inbox.py`).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))

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


# --------------------------------------------------- ảnh TRAILER (Xưởng video)
# Ảnh trailer dùng mã v01..v14 và lưu ở docs/assets/video/ — KHÔNG phải asset game.
# Phải chặn trước khi nhận diện, nếu không AI sẽ gán nhầm sang asset game và
# ghi đè ảnh đang dùng trong game.
def _canh_video():
    import xuong_video as XV
    return XV


def _la_anh_trailer(ten: str, hint: str) -> dict | None:
    """Trả cảnh trailer nếu ảnh này thuộc Xưởng video, ngược lại None."""
    try:
        XV = _canh_video()
    except Exception:  # noqa: BLE001 — thiếu module thì bỏ qua, giữ luồng cũ
        return None
    theo_key = {c["key"]: c for c in XV.CANH_VIDEO}
    if hint in theo_key:
        return theo_key[hint]
    for k, c in theo_key.items():
        if k in ten or c["file"] == ten:
            return c
    return None


def _luu_anh_trailer(c: dict, data: bytes) -> str:
    """Lưu ảnh trailer đúng tên file, đưa về khung 1080x1920.

    Giữ đúng tỉ lệ: vừa khung rồi đệm hai bên (hoặc trên dưới) bằng màu viền
    trung bình của chính ảnh. KHÔNG ép phẳng về 1080x1920 vì sẽ kéo méo mặt.
    """
    XV = _canh_video()
    os.makedirs(XV.VIDEO_DIR, exist_ok=True)
    dich = os.path.join(XV.VIDEO_DIR, c["file"])
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(data))
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        rong, cao = XV.KHUNG
        if im.size != (rong, cao):
            ti_le = min(rong / im.width, cao / im.height)
            moi = (max(1, round(im.width * ti_le)), max(1, round(im.height * ti_le)))
            im = im.resize(moi, Image.LANCZOS)
            nen = _mau_vien(im)
            khung = Image.new("RGB", (rong, cao), nen)
            khung.paste(im, ((rong - moi[0]) // 2, (cao - moi[1]) // 2))
            im = khung
        im.save(dich, "JPEG", quality=90, optimize=True)
    except Exception:  # noqa: BLE001 — Pillow lỗi thì ghi nguyên bản
        with open(dich, "wb") as f:
            f.write(data)
    return c["file"]


def _mau_vien(im) -> tuple:
    """Màu trung bình của 4 cạnh — dùng làm nền khi đệm khung."""
    from PIL import ImageStat
    rong, cao = im.size
    dai = max(1, min(rong, cao) // 20)
    vien = [im.crop((0, 0, rong, dai)), im.crop((0, cao - dai, rong, cao)),
            im.crop((0, 0, dai, cao)), im.crop((rong - dai, 0, rong, cao))]
    tong = [0, 0, 0]
    for v in vien:
        st = ImageStat.Stat(v)
        for i in range(3):
            tong[i] += st.mean[i]
    return tuple(int(t / len(vien)) for t in tong)


def nhan_dien(anh_list: list, env: dict, chi_con_thieu: bool = True) -> list:
    """Nhận diện từng ảnh. Trả [{name, key, do_tin_cay, mo_ta, ly_do, kich_thuoc, cach, data}]."""
    ung_vien = asset_con_thieu() if chi_con_thieu else list(TS.ASSETS)
    hop_le = {a["key"] for a in ung_vien}
    kq = []
    for item in anh_list:
        ten = os.path.basename(item.get("name", "") or "image")
        data = base64.b64decode(item.get("data", ""))
        hint = (item.get("hint_key") or "").strip()

        # Ảnh trailer (v01..v14) — nhận thẳng, KHÔNG đưa cho AI đoán, để không
        # bao giờ bị gán nhầm sang asset game rồi ghi đè ảnh trong game.
        canh = _la_anh_trailer(ten, hint)
        if canh:
            kq.append({"name": ten, "data": data, "key": canh["key"], "do_tin_cay": 100,
                       "cach": "trailer", "mo_ta": canh["ten"], "ly_do": "Ảnh trailer Xưởng video.",
                       "kich_thuoc": ""})
            continue

        # Có gợi ý key (thư mục đặt đúng tên key, hoặc dòng 'mã-ảnh' trong Issue)
        # → tin tuyệt đối.
        if hint and _asset_theo_key(hint):
            cach = item.get("hint_cach") or "thu-muc"
            ly_do = ("Issue ghi rõ mã ảnh." if cach == "ma-anh"
                     else "Thư mục upload đặt đúng mã ảnh.")
            kq.append({"name": ten, "data": data, "key": hint, "do_tin_cay": 100,
                       "cach": cach, "mo_ta": "", "ly_do": ly_do,
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


# Bỏ các từ chung không dùng làm thẻ tìm kiếm.
_TU_CHUNG = {"ke", "kẻ", "cua", "của", "va", "và", "tai", "tại", "o", "ở", "trong",
             "mot", "một", "anh", "ảnh", "nhieu", "nhiều", "hinh", "hình", "mau", "mẫu"}


def _tags_cua(key: str) -> list:
    """Sinh thẻ tìm kiếm từ tên + mô tả asset (ảnh do bot thêm chưa có thẻ viết tay)."""
    a = _asset_theo_key(key) or {}
    nguon = f"{a.get('name', '')} {a.get('use', '')}"
    nguon = re.sub(r"\([^)]*\)", " ", nguon)          # bỏ phần trong ngoặc
    nguon = nguon.split("—", 1)[-1] if "—" in nguon else nguon
    tags, thay = [], set()
    for t in re.split(r"[^\wÀ-ỹ]+", nguon, flags=re.UNICODE):
        t = t.strip().lower()
        if len(t) < 2 or t in _TU_CHUNG or t in thay:
            continue
        thay.add(t)
        tags.append(t)
    return tags[:8]


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
    if not muc.get("tags"):
        muc["tags"] = _tags_cua(key)
    muc["dung_o"] = da_gan
    anh[ten_file] = muc


def luu_va_ghep(ket_qua: list) -> dict:
    """Lưu ảnh đã xác định key + ghép vào đoạn. Trả báo cáo."""
    da_luu, bo_qua = [], []
    can_xac_nhan = []
    for r in ket_qua:
        key = r.get("key") or ""

        # Ảnh trailer (v01..v14) đi đường riêng — lưu vào docs/assets/video/.
        # Không được rơi vào nhánh asset game, tránh ghi đè ảnh đang dùng trong game.
        if r.get("cach") == "trailer":
            canh = _la_anh_trailer(os.path.basename(r.get("name") or ""), "")
            if not canh:
                canh = next((c for c in _canh_video().CANH_VIDEO if c["key"] == key), None)
            if not canh:
                bo_qua.append({"name": r.get("name"), "key": key, "ly_do": "Không khớp cảnh trailer"})
                continue
            data = r.get("data")
            if isinstance(data, str):
                data = base64.b64decode(data)
            try:
                ten_file = _luu_anh_trailer(canh, data)
                da_luu.append({"name": r.get("name"), "key": canh["key"], "file": ten_file,
                               "cach": "trailer", "do_tin_cay": 100})
            except Exception as e:  # noqa: BLE001
                bo_qua.append({"name": r.get("name"), "key": canh["key"], "ly_do": str(e)})
            continue

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

    # Ảnh trailer không có đoạn truyện và không thuộc thư viện ảnh game —
    # tách ra để hai phần dưới chỉ xử lý ảnh game.
    anh_game = [x for x in da_luu if x.get("cach") != "trailer"]
    anh_trailer = [x for x in da_luu if x.get("cach") == "trailer"]

    # ghép vào dữ liệu chương (cả 2 bản)
    ghep = {}
    if anh_game:
        for rel in CHUONG_FILES:
            p, chuong = _nap_json(rel)
            for x in anh_game:
                gan = _gan_doan(chuong, x["key"], x["file"])
                if gan:
                    ghep.setdefault(x["file"], gan)
            _ghi_json(p, chuong)

        # cập nhật thư viện
        p, lib = _nap_json(LIB_FILE)
        for x in anh_game:
            _cap_nhat_thu_vien(lib, x["key"], x["file"], ghep.get(x["file"], []))
        _ghi_json(p, lib)

    if anh_trailer:
        import build_xuong_video as BV
        BV.build_va_ghi()

    thong_diep = f"Đã lưu và ghép {len(anh_game)} ảnh game"
    if anh_trailer:
        thong_diep += f", {len(anh_trailer)} ảnh trailer"
    return {"da_luu": da_luu, "can_xac_nhan": can_xac_nhan, "bo_qua": bo_qua, "ghep": ghep,
            "thong_diep": thong_diep + "."}


def xu_ly(anh_list: list, env: dict | None = None, chi_con_thieu: bool = True) -> dict:
    """Luồng đầy đủ: nhận diện → lưu → ghép."""
    env = env or TS.load_env()
    ket_qua = nhan_dien(anh_list, env, chi_con_thieu=chi_con_thieu)
    bc = luu_va_ghep(ket_qua)
    bc["nhan_dien"] = [{k: v for k, v in r.items() if k != "data"} for r in ket_qua]
    return bc
