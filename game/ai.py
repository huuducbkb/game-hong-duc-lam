#!/usr/bin/env python3
"""Kiểm tra khả dụng của AI + gọi AI kể chuyện (chế độ có AI).

Nguyên tắc:
  - Không có key, hoặc key hỏng → `san_sang()` trả False.
  - Kết quả thử được NHỚ trong RAM (không gọi lại mỗi lượt).
  - Mọi lỗi mạng/API đều bị nuốt, coi như AI không sẵn sàng (game vẫn chạy).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
TIMEOUT = 12

# chỉ số kết quả thử (None = chưa thử)
_trang_thai: dict = {"da_thu": False, "ok": False, "ly_do": ""}


def load_env() -> dict:
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _gemini_key(env: dict) -> str:
    for k in ("geminikey", "geminikey1", "geminikey2", "geminikey3"):
        if env.get(k):
            return env[k]
    return ""


# model thử theo thứ tự (model cũ có thể bị khai tử với tài khoản mới)
MODEL_DU_PHONG = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
]


def _gemini_model(env: dict) -> str:
    return env.get("GEMINI_TEXT_MODEL") or env.get("TEXT_MODEL") or ""


def _goi_gemini(env: dict, prompt: str, max_token: int = 400) -> str:
    key = _gemini_key(env)
    if not key:
        raise RuntimeError("Thiếu key Gemini")
    chi_dinh = _gemini_model(env)
    ds = ([chi_dinh] if chi_dinh else []) + MODEL_DU_PHONG
    loi_cuoi = None
    for model in ds:
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{model}:generateContent?key={key}")
        body = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max(max_token, 256), "temperature": 0.9},
        }).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8"))
            cand = (data.get("candidates") or [{}])[0]
            parts = cand.get("content", {}).get("parts", [])
            txt = "".join(p.get("text", "") for p in parts).strip()
            if txt:
                return txt
            loi_cuoi = f"{model}: không có nội dung trả về"
        except urllib.error.HTTPError as e:
            # 404 = model bị khai tử → thử model kế; 429/503 = quá tải → thử tiếp
            loi_cuoi = f"{model}: HTTP {e.code}"
            if e.code in (400, 401, 403):
                raise  # key sai/hết quyền → dừng ngay
            continue
        except Exception as e:  # noqa: BLE001 - mạng/timeout → thử model kế
            loi_cuoi = f"{model}: {type(e).__name__}"
            continue
    raise RuntimeError(loi_cuoi or "Không gọi được model nào")


def thu_ket_noi(force: bool = False) -> dict:
    """Thử gọi AI một lần (nhớ kết quả). Trả {ok, ly_do}."""
    if _trang_thai["da_thu"] and not force:
        return {"ok": _trang_thai["ok"], "ly_do": _trang_thai["ly_do"]}
    env = load_env()
    if not _gemini_key(env) and not env.get("OPENROUTER_API_KEY"):
        _trang_thai.update(da_thu=True, ok=False, ly_do="Chưa cấu hình key AI")
        return {"ok": False, "ly_do": _trang_thai["ly_do"]}
    try:
        _goi_gemini(env, "Trả lời đúng một chữ: OK", max_token=256)
        _trang_thai.update(da_thu=True, ok=True, ly_do="")
    except urllib.error.HTTPError as e:
        _trang_thai.update(da_thu=True, ok=False, ly_do=f"Key bị từ chối (HTTP {e.code})")
    except Exception as e:  # noqa: BLE001 - nuốt mọi lỗi, AI chỉ là phần phụ
        _trang_thai.update(da_thu=True, ok=False, ly_do=str(e)[:120])
    return {"ok": _trang_thai["ok"], "ly_do": _trang_thai["ly_do"]}


def san_sang() -> bool:
    return thu_ket_noi()["ok"]


def ke_lai(doan_ke: str, hanh_dong: str, thay_doi: str = "") -> str:
    """AI kể lại đoạn theo hành động tự do của người chơi (giữ nguyên khung)."""
    env = load_env()
    phan_thay_doi = f"\nCÁC THAY ĐỔI ĐÃ ÁP DỤNG (phải khớp với truyện): {thay_doi}" if thay_doi else ""
    prompt = (
        "Bạn là người dẫn chuyện tiên hiệp Việt, ngôi thứ nhất 'ta'. "
        "Viết lại đoạn sau thật sinh động, có nội tâm, 3-5 câu, KHÔNG đổi sự kiện:\n\n"
        f"ĐOẠN GỐC:\n{doan_ke}\n\n"
        f"HÀNH ĐỘNG CỦA NGƯỜI CHƠI: {hanh_dong}{phan_thay_doi}\n\n"
        "Chỉ trả về đoạn kể, không giải thích."
    )
    return _goi_gemini(env, prompt, max_token=500)


# --------------------------------------------------- nhận diện hành động tự do
# Tập hành động được phép + giới hạn mỗi chỉ số (engine sẽ cắt lại lần nữa).
HANH_DONG_HOP_LE = ["tấn công", "tặng quà", "trò chuyện", "di chuyển",
                    "quan sát", "nghỉ", "khác"]

GIOI_HAN = {
    "sinh_luc": (-15, 10),
    "tu_vi": (0, 8),
    "linh_thach": (-10, 10),
    "than_niem": (0, 2),
    "hao_cam": (-10, 10),
}


def _tach_json(txt: str) -> dict:
    """Bóc JSON khỏi văn bản (AI có thể bọc trong ```json ... ```)."""
    txt = txt.strip()
    if txt.startswith("```"):
        txt = txt.split("```", 2)[1] if txt.count("```") >= 2 else txt.strip("`")
        if txt.lstrip().startswith("json"):
            txt = txt.lstrip()[4:]
    dau, cuoi = txt.find("{"), txt.rfind("}")
    if dau < 0 or cuoi < dau:
        raise ValueError("Không thấy JSON")
    return json.loads(txt[dau:cuoi + 1])


def nhan_dien(van_ban: str, boi_canh: str) -> dict:
    """AI đọc hành động tự do → trả ý định đã LỌC (chỉ khoá hợp lệ, trong giới hạn).

    Không gọi được AI hoặc AI trả rác → trả {} (game xử như không đổi chỉ số).
    """
    env = load_env()
    prompt = (
        "Bạn là bộ máy luật cho game nhập vai tu tiên. Người chơi gõ một hành động tự do.\n"
        "Nhiệm vụ: phân loại hành động và đề xuất thay đổi chỉ số NHỎ, hợp lý. CHỈ TRẢ JSON.\n\n"
        f"BỐI CẢNH:\n{boi_canh}\n\n"
        f"HÀNH ĐỘNG NGƯỜI CHƠI: {van_ban}\n\n"
        "Khuôn JSON (bỏ khoá nào không áp dụng):\n"
        '{"hanh_dong": "' + "|".join(HANH_DONG_HOP_LE) + '",\n'
        ' "sinh_luc": <số nguyên -15..10>,\n'
        ' "tu_vi": <0..8>,\n'
        ' "linh_thach": <-10..10>,\n'
        ' "than_niem": <0..2>,\n'
        ' "hao_cam": {"<tên NPC đã gặp>": <-10..10>},\n'
        ' "nhan_xet": "<một câu tiếng Việt ngắn>"}\n'
        "Quy tắc: thay đổi phải NHỎ; chỉ dùng NPC đã liệt kê trong bối cảnh; "
        "KHÔNG bịa sự kiện, KHÔNG đổi đoạn truyện. Chỉ trả JSON, không giải thích."
    )
    try:
        raw = _goi_gemini(env, prompt, max_token=400)
    except Exception:  # noqa: BLE001 - AI lỗi → coi như không có ý định
        return {}
    try:
        d = _tach_json(raw)
    except Exception:  # noqa: BLE001
        return {}
    if not isinstance(d, dict):
        return {}
    y: dict = {}
    if d.get("hanh_dong") in HANH_DONG_HOP_LE:
        y["hanh_dong"] = d["hanh_dong"]
    for k in ("sinh_luc", "tu_vi", "linh_thach", "than_niem"):
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0:
            lo, hi = GIOI_HAN[k]
            y[k] = max(lo, min(hi, int(v)))
    hc = d.get("hao_cam")
    if isinstance(hc, dict):
        loc = {}
        for ten, v in hc.items():
            if isinstance(ten, str) and isinstance(v, (int, float)) \
                    and not isinstance(v, bool) and v != 0:
                lo, hi = GIOI_HAN["hao_cam"]
                loc[ten] = max(lo, min(hi, int(v)))
        if loc:
            y["hao_cam"] = loc
    if isinstance(d.get("nhan_xet"), str):
        y["nhan_xet"] = d["nhan_xet"].strip()[:160]
    return y
