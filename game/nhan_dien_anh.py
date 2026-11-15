#!/usr/bin/env python3
"""Nhận diện ảnh người dùng gửi thuộc prompt nào trong Xưởng.

Ý tưởng (nâng cấp "cách B"):
  - Lớp 1: đọc kích thước ảnh (thuần Python, không cần thư viện) → loại ứng viên sai tỷ lệ.
  - Lớp 2: đưa AI đọc NGUYÊN VĂN prompt tiếng Anh đã dùng để vẽ (khớp câu gốc).
  - Lớp 3: bắt AI "tả trước, chọn sau" → trả JSON có mô tả + độ tin cậy + lý do.
  - Lớp 4: do_tin_cay thấp → giao diện để người dùng tự xác nhận.

Không cài thêm gì. Mọi lỗi mạng/API đều bị nuốt (trả gợi ý rỗng) để Xưởng vẫn chạy.
"""

from __future__ import annotations

import base64
import json
import re
import struct
import urllib.error
import urllib.request

TIMEOUT = 30

# model thử theo thứ tự (model cũ có thể bị khai tử với tài khoản mới)
MODEL_DU_PHONG = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
]


# ---------------------------------------------------------------- Lớp 1: kích thước
def kich_thuoc_anh(data: bytes):
    """Đọc (rộng, cao) từ header PNG/JPEG/GIF/WebP. Không cần PIL. Lỗi → None."""
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", data[16:24])
            return int(w), int(h)
        if data[:3] == b"GIF":
            w, h = struct.unpack("<HH", data[6:10])
            return int(w), int(h)
        if data[:2] == b"\xff\xd8":  # JPEG: quét marker SOF
            i = 2
            n = len(data)
            while i + 9 < n:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                              0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return int(w), int(h)
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                seg = struct.unpack(">H", data[i + 2:i + 4])[0]
                i += 2 + seg
            return None
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            fmt = data[12:16]
            if fmt == b"VP8X":
                w = 1 + int.from_bytes(data[24:27], "little")
                h = 1 + int.from_bytes(data[27:30], "little")
                return w, h
            if fmt == b"VP8 ":
                w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
                h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
                return w, h
            if fmt == b"VP8L":
                bits = int.from_bytes(data[21:25], "little")
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
            return None
    except Exception:
        return None
    return None


def ty_le_muc_tieu(ratio: str):
    """'3:4 dọc (900×1200)' → 0.75. Ưu tiên số pixel nếu có, không thì tỷ lệ chữ."""
    m = re.search(r"(\d+)\s*[×xX]\s*(\d+)", ratio)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        if h:
            return w / h
    m = re.search(r"(\d+)\s*:\s*(\d+)", ratio)
    if m and int(m.group(2)):
        return int(m.group(1)) / int(m.group(2))
    return None


def khop_ty_le(w: int, h: int, ratio: str, dung_sai: float = 0.06) -> bool:
    """Ảnh có đúng tỷ lệ mục tiêu không (cho phép lệch nhỏ)."""
    t = ty_le_muc_tieu(ratio)
    if not t or not h:
        return True  # không rõ → không loại
    return abs((w / h) - t) / t <= dung_sai


def loc_ung_vien(kich_thuoc, assets):
    """Lớp 1: giữ asset khớp tỷ lệ. Nếu không còn gì → trả hết (để AI vẫn có cơ hội)."""
    if not kich_thuoc:
        return list(assets)
    w, h = kich_thuoc
    giu = [a for a in assets if khop_ty_le(w, h, a.get("ratio", ""))]
    return giu or list(assets)


# ---------------------------------------------------------------- Lớp 2+3: AI nhìn ảnh
def _prompt_chon(ung_vien, kich_thuoc) -> str:
    ds = []
    for a in ung_vien:
        ds.append(
            f'- key: "{a["key"]}"\n'
            f'  ten: {a.get("name", "")}\n'
            f'  ti_le: {a.get("ratio", "")}\n'
            f'  prompt_goc: {a.get("prompt", "")}'
        )
    kt = f"Kich thuoc anh nguoi dung gui: {kich_thuoc[0]}x{kich_thuoc[1]} px." if kich_thuoc else ""
    return (
        "Ban la nguoi kiem tra tai nguyen hinh anh cho mot game tu tien. "
        "Nguoi dung vua ve mot anh bang AI tu MOT trong cac prompt duoi day, "
        "nhung ten file co the bi doi (vi du IMG_4821.JPG).\n\n"
        f"{kt}\n\n"
        "CAC UNG VIEN:\n" + "\n".join(ds) + "\n\n"
        "Hay lam theo thu tu:\n"
        "1) Mo ta ngan gon (1 cau, tieng Viet) nhung gi BAN THAY trong anh "
        "(bo cuc, doi tuong, co nguoi hay khong, co vat the gi, sang hay toi).\n"
        "2) Doi chieu voi tung prompt_goc, roi chon key khop nhat.\n"
        "3) Cho do_tin_cay 0-100: tren 80 = rat chac; 50-80 = kha chac; duoi 50 = doan mo ho.\n\n"
        "TRA VE DUY NHAT mot doi tuong JSON, khong them chu nao khac:\n"
        '{"mo_ta": "...", "key": "<key hoac rong>", "do_tin_cay": 0, "ly_do": "..."}'
    )


def _goi_vision(env: dict, b64: str, mime: str, prompt: str):
    """Gọi Gemini nhìn ảnh. Trả dict JSON hoặc None."""
    key = next((env[k] for k in ("geminikey", "geminikey1", "geminikey2", "geminikey3")
                if env.get(k)), "")
    if not key:
        return None
    chi_dinh = env.get("GEMINI_TEXT_MODEL") or env.get("TEXT_MODEL") or ""
    ds = ([chi_dinh] if chi_dinh else []) + MODEL_DU_PHONG
    for model in ds:
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{model}:generateContent?key={key}")
        body = json.dumps({
            "contents": [{"parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime, "data": b64}},
            ]}],
            "generationConfig": {
                "maxOutputTokens": 400,
                "temperature": 0,
                "responseMimeType": "application/json",
            },
        }).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8"))
            parts = (data.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
            txt = "".join(p.get("text", "") for p in parts).strip()
            j = _tach_json(txt)
            if j is not None:
                return j
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403):
                return None  # key sai/hết quyền → dừng
            continue
        except Exception:
            continue
    return None


def _tach_json(txt: str):
    if not txt:
        return None
    try:
        return json.loads(txt)
    except Exception:
        pass
    m = re.search(r"\{.*\}", txt, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None


# ---------------------------------------------------------------- đầu mối
def goi_y_mot_anh(data: bytes, mime: str, assets, env: dict) -> dict:
    """Gợi ý 1 ảnh: {kich_thuoc, ung_vien, key, do_tin_cay, mo_ta, ly_do}."""
    kt = kich_thuoc_anh(data)
    ung_vien = loc_ung_vien(kt, assets)
    kq = {
        "kich_thuoc": f"{kt[0]}x{kt[1]}" if kt else "",
        "ung_vien": [a["key"] for a in ung_vien],
        "key": "",
        "do_tin_cay": 0,
        "mo_ta": "",
        "ly_do": "",
    }
    if len(ung_vien) == 1:
        a = ung_vien[0]
        kq.update(key=a["key"], do_tin_cay=100, ly_do="Chi mot ung vien khop ti le.")
        return kq
    b64 = base64.b64encode(data).decode()
    j = _goi_vision(env, b64, mime, _prompt_chon(ung_vien, kt))
    if j:
        key = j.get("key") or ""
        hop_le = {a["key"] for a in ung_vien}
        kq["key"] = key if key in hop_le else ""
        try:
            kq["do_tin_cay"] = max(0, min(100, int(j.get("do_tin_cay") or 0)))
        except Exception:
            kq["do_tin_cay"] = 0
        kq["mo_ta"] = str(j.get("mo_ta") or "")[:300]
        kq["ly_do"] = str(j.get("ly_do") or "")[:300]
    return kq
