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


def ke_lai(doan_ke: str, hanh_dong: str) -> str:
    """AI kể lại đoạn theo hành động tự do của người chơi (giữ nguyên khung)."""
    env = load_env()
    prompt = (
        "Bạn là người dẫn chuyện tiên hiệp Việt, ngôi thứ nhất 'ta'. "
        "Viết lại đoạn sau thật sinh động, có nội tâm, 3-5 câu, KHÔNG đổi sự kiện:\n\n"
        f"ĐOẠN GỐC:\n{doan_ke}\n\n"
        f"HÀNH ĐỘNG CỦA NGƯỜI CHƠI: {hanh_dong}\n\n"
        "Chỉ trả về đoạn kể, không giải thích."
    )
    return _goi_gemini(env, prompt, max_token=500)
