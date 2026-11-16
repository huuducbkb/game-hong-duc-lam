#!/usr/bin/env python3
"""Nén ảnh tài nguyên trước khi lưu vào game (mức "vừa").

Quy tắc:
  - Ảnh cần trong suốt (seal, avatar-ring) -> giữ PNG + alpha, thu nhỏ.
  - Ảnh khung dùng border-image (panel-story, btn-choice) -> GIỮ NGUYÊN CỠ,
    chỉ nén JPEG, vì CSS cắt viền theo pixel cố định nên đổi cỡ sẽ méo.
  - Còn lại -> thu nhỏ theo bề rộng + JPEG q80.

Thiếu Pillow thì trả None để nơi gọi lưu ảnh nguyên gốc (không vỡ luồng).
"""

from __future__ import annotations

import io
import os

try:
    from PIL import Image
except Exception:
    Image = None

JPEG_Q = 80

# key -> (kiểu, bề rộng đích). kiểu: "jpeg" (nền/khung), "png" (giữ trong suốt).
# Bề rộng phải khớp cỡ ảnh game đang dùng: panel-story/btn-choice cắt viền bằng
# border-image theo pixel cố định nên đổi cỡ sẽ lệch viền.
QUY_TAC = {
    "bg-main": ("jpeg", 820),
    "panel-character": ("jpeg", 800),
    "panel-story": ("jpeg", 800),
    "btn-choice": ("jpeg", 1100),
    "divider-ink": ("jpeg", 1400),
    "avatar-ring": ("png", 512),
    "seal": ("png", 300),
    "bc_cho_01": ("jpeg", 900),
    "bc_tan_xa_dem": ("jpeg", 900),
    "vt_ngoc_cot": ("jpeg", 900),
    "nv_tuyet_co": ("jpeg", 900),
}

MAC_DINH = ("jpeg", 900)


def co_pillow() -> bool:
    return Image is not None


def quy_tac(key: str, ten_file: str) -> tuple:
    """Trả (kiểu, bề rộng). Suy theo key; ảnh cảnh (bc_/vt_/nv_) luôn JPEG."""
    if key in QUY_TAC:
        return QUY_TAC[key]
    if ten_file.endswith(".png") and key in ("seal", "avatar-ring"):
        return ("png", 512)
    return MAC_DINH


def nen(data: bytes, key: str = "", ten_file: str = "") -> bytes:
    """Nén bytes ảnh theo quy tắc. Trả bytes mới, hoặc None nếu không nén được."""
    if Image is None:
        return None
    kieu, rong = quy_tac(key, ten_file)
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return None

    # Giữ đúng định dạng theo quy tắc để đuôi file (.png/.jpg) khớp nội dung.
    if rong and rong < im.width:
        cao = round(im.height * rong / im.width)
        im = im.resize((rong, cao), Image.LANCZOS)

    out = io.BytesIO()
    if kieu == "png":
        im.convert("RGBA").save(out, "PNG", optimize=True)
    else:
        im.convert("RGB").save(out, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    return out.getvalue()
