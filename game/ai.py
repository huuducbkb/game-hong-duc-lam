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
    """AI kể lại đoạn theo hành động tự do của người chơi (giữ nguyên khung).

    Bản AI viết hỏng (Hán-Việt rác, dính chữ, sai độ dài) → trả "" để nơi gọi
    dùng lại văn bản gốc.
    """
    env = load_env()
    phan_thay_doi = f"\nCÁC THAY ĐỔI ĐÃ ÁP DỤNG (phải khớp với truyện): {thay_doi}" if thay_doi else ""
    prompt = (
        "Bạn là người dẫn chuyện tiên hiệp Việt, ngôi thứ nhất 'ta'. "
        "Viết lại đoạn sau thật sinh động, có nội tâm, 3-5 câu, KHÔNG đổi sự kiện:\n\n"
        f"ĐOẠN GỐC:\n{doan_ke}\n\n"
        f"HÀNH ĐỘNG CỦA NGƯỜI CHƠI: {hanh_dong}{phan_thay_doi}\n\n"
        "Dùng tiếng Việt thuần, KHÔNG chêm chữ Hán (dị hương, khứu đại, triệt ngộ…). "
        "Chỉ trả về đoạn kể, không giải thích."
    )
    try:
        moi = _goi_gemini(env, prompt, max_token=500).strip()
    except Exception:  # noqa: BLE001 - AI lỗi → nơi gọi dùng bản gốc
        return ""
    dung, _ = van_ban_dung(moi, doan_ke)
    return moi if dung else ""


# --------------------------------------------------- kể lại đoạn theo văn phong
# Tên riêng / thuật ngữ trong truyện — AI không được đổi (vd 'tân xá' → 'quán trọ').
TEN_RIENG = ["Hàn Lập", "Thất Huyền Môn", "Thất Huyền quyền", "Thất Huyền trấn",
             "Dã Lang Bang", "Lý Hổ", "Tần Báo", "Tuyết Cơ", "Mạc Đại Phu",
             "Hùng Bá", "Hợp Hoan Tông", "tân xá", "ngọc cốt", "hậu sơn",
             "hắc quáng động"]

# Cache kết quả kể lại: khoá = (đoạn gốc, hành động). Trong RAM, mất khi tắt máy chủ.
_cache_ke: dict = {}
CACHE_TOI_DA = 500


def _khoa_cache(doan_ke: str, hanh_dong: str, npc: tuple = ()) -> tuple:
    return (doan_ke, hanh_dong, npc)


# Giọng kể phải đổi theo thái độ, nhưng sự kiện thì không được đổi — nếu không,
# người chơi hảo cảm thấp sẽ đọc một cốt truyện khác hẳn.
_GIONG_THEO_THAI_DO = {
    "tử địch": "căm thù, dè chừng, muốn tránh xa",
    "thù địch": "lạnh nhạt, cộc, không giải thích, không đùa",
    "người dưng": "dè dặt, lịch sự nhưng xa cách",
    "quen biết": "thoải mái vừa phải, đã bớt cảnh giác",
    "thân thiết": "ấm áp, tin nhau, nói thẳng",
    "tri kỷ": "thân tình, hiểu nhau không cần nói hết",
}


def _phan_thai_do(npc) -> str:
    """Khối prompt mô tả thái độ hiện tại của NPC trong cảnh."""
    if not npc:
        return ""
    dong = []
    for n in npc:
        ten = n.get("ten") or ""
        thai_do = n.get("thai_do") or "người dưng"
        giong = _GIONG_THEO_THAI_DO.get(thai_do, _GIONG_THEO_THAI_DO["người dưng"])
        dong.append(f"- {ten}: thái độ với người kể là “{thai_do}” → {giong} "
                    f"(hảo cảm {n.get('hao_cam', 0)})")
    if not dong:
        return ""
    return (
        "\nTHÁI ĐỘ NHÂN VẬT TRONG CẢNH (bắt buộc đổi giọng theo):\n"
        + "\n".join(dong) + "\n"
        "- Đổi CÁCH NÓI của nhân vật đó và cách người kể nhìn họ cho khớp thái độ.\n"
        "- TUYỆT ĐỐI không đổi sự việc: cùng hành động, cùng ai làm gì, cùng kết quả.\n"
        "- Không thêm lời thoại mới, không bớt lời thoại cũ; chỉ đổi sắc thái câu chữ.\n"
    )


# ------------------------------------------- chặn AI viết hỏng (Hán-Việt rác)
# Model hay "cổ phong hoá" quá tay: ghép chữ Hán nửa vời, dính chữ ("mộtỗ"),
# sai ngữ pháp ("u lan chi khí ấy lại tùng hình nàng mà chí"), dùng từ sai
# nghĩa ("mai táng" cho khối ngọc). Truyện gốc sạch nên lấy chính nó làm chuẩn.
_NGUONG_TU_LA = 0.12        # gốc: 0.0% · bản AI hỏng: 12–45%
_NGUONG_PHINH = 1.40        # dài hơn gốc quá mức = AI thêm câu
_NGUONG_NGAN = 0.70         # ngắn hơn = AI tóm tắt, mất chi tiết truyện
_KY_TU_RAC = set("øØæÆðÐþÞß")

# Từ Hán-Việt rác đã gặp thật trong bản AI viết hỏng (xem lịch sử lỗi người chơi báo).
_TU_RAC = (
    "khứu đại", "dị hương", "triệt ngộ", "tùng hình", "nguyệt thăng", "u lan",
    "tịch mịch", "tịch dương", "mai táng", "vị tằng", "phương tri", "hà xứ",
    "nhi lai", "đồng thời khắc", "nhất lũ", "nhất vị", "nhất đạo", "chủng hoa",
    "độc năng", "tị quan", "nhục thân chân thật", "mộc sàng", "bích quang",
    "chân quang", "ôn nhuận", "hữu mạch", "thanh sở", "ma ty", "nguyệt hoa",
    "lăng tại", "chí nghẹn", "thiên niên", "nhu như ti",
)

_vocab_chuan: set | None = None

# Nhật ký các bản AI bị chặn — để xem lại vì sao, không hiện ra người chơi.
_so_lan_chan: list = []


def _kho_tu_chuan() -> set:
    """Từ vựng lấy từ chính truyện trong repo — nguồn chuẩn, không cần file ngoài."""
    global _vocab_chuan
    if _vocab_chuan is not None:
        return _vocab_chuan
    import glob
    import re as _re
    tu: set = set()
    goc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for f in glob.glob(os.path.join(goc, "game", "chapters", "*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:  # noqa: BLE001 - file hỏng thì bỏ qua
            continue
        for d in data.get("doan", []) or []:
            for truong in ("ke", "boi_canh"):
                tu |= set(_re.findall(r"[^\W\d_]+", (d.get(truong) or "").lower(),
                                      _re.UNICODE))
    _vocab_chuan = tu
    return tu


def _ty_le_tu_la(van_ban: str) -> float:
    """Tỉ lệ từ không có trong truyện gốc. Cao = AI bịa chữ Hán."""
    import re as _re
    tu = _re.findall(r"[^\W\d_]+", (van_ban or "").lower(), _re.UNICODE)
    if not tu:
        return 0.0
    chuan = _kho_tu_chuan()
    if not chuan:                      # không đọc được truyện → không chặn
        return 0.0
    return sum(1 for w in tu if w not in chuan) / len(tu)


def _co_chu_dinh(van_ban: str) -> bool:
    """Chữ dính nhau — dấu hiệu AI nuốt mất khoảng trắng ('mộtỗ').

    Chỉ báo khi từ đó KHÔNG có trong truyện gốc: 'chỗ', 'gỗ', 'vỗ' là từ thật.
    """
    import re as _re
    chuan = _kho_tu_chuan()
    for m in _re.finditer(r"[^\W\d_]{2,}ỗ\b", (van_ban or "").lower(), _re.UNICODE):
        if m.group(0) not in chuan:
            return True
    return False


def van_ban_dung(ban_ai: str, ban_goc: str) -> tuple[bool, str]:
    """Bản AI có dùng được không. Trả (dùng_được, lý_do_từ_chối)."""
    if not ban_ai or not ban_ai.strip():
        return False, "AI trả về rỗng"
    if any(c in _KY_TU_RAC for c in ban_ai):
        return False, "có ký tự rác ngoài tiếng Việt"
    thap = ban_ai.lower()
    for tu in _TU_RAC:
        if tu in thap:
            return False, f"có từ Hán-Việt rác ({tu!r})"
    if _co_chu_dinh(ban_ai):
        return False, "có chữ dính nhau (vd 'mộtỗ')"
    if not ban_ai.rstrip().endswith((".", "!", "?", "”", '"', "*", "…")):
        return False, "câu bị cắt giữa chừng"
    ty = _ty_le_tu_la(ban_ai)
    if ty > _NGUONG_TU_LA:
        return False, f"quá nhiều từ lạ ({ty:.0%})"
    if ban_goc:
        mat = [t for t in TEN_RIENG if t in ban_goc and t not in ban_ai]
        if mat:
            return False, f"đổi mất tên riêng ({', '.join(mat[:3])})"
        if ban_goc.count("\n\n") and ban_ai.count("\n\n") < ban_goc.count("\n\n") - 1:
            return False, "gộp mất dòng trống giữa các đoạn"
        ti = len(ban_ai) / max(1, len(ban_goc))
        if ti > _NGUONG_PHINH:
            return False, f"dài hơn bản gốc {ti:.0%}"
        if ti < _NGUONG_NGAN:
            return False, f"ngắn hơn bản gốc {ti:.0%} (mất chi tiết)"
    return True, ""


def ke_lai_tien_hiep(doan_ke: str, boi_canh: str = "", hanh_dong: str = "",
                     npc=None) -> str:
    """AI kể lại một đoạn cốt truyện theo văn phong tiên hiệp (GIỮ NGUYÊN sự kiện).

    `npc` là danh sách {ten, hao_cam, thai_do} của cảnh: AI đổi GIỌNG lời thoại theo
    thái độ, nhưng không được đổi sự việc. Kết quả được NHỚ theo (đoạn, hành động,
    thái độ) — cùng đoạn với hai mức hảo cảm khác nhau phải ra hai bản khác nhau.
    Lỗi mạng/API → trả "" để nơi gọi dùng lại văn bản gốc.
    """
    doan_ke = (doan_ke or "").strip()
    if not doan_ke:
        return ""
    npc = npc or []
    khoa_npc = tuple(sorted((n.get("ten") or "", n.get("thai_do") or "")
                            for n in npc))
    khoa = _khoa_cache(doan_ke, hanh_dong, khoa_npc)
    if khoa in _cache_ke:
        return _cache_ke[khoa]

    env = load_env()
    phan_boi_canh = f"\nBỐI CẢNH: {boi_canh}" if boi_canh else ""
    phan_hanh_dong = f"\nHÀNH ĐỘNG VỪA RỒI CỦA NGƯỜI CHƠI: {hanh_dong}" if hanh_dong else ""
    prompt = (
        "Bạn là người kể chuyện tiếng Việt. Kể lại đoạn dưới bằng TIẾNG VIỆT HIỆN ĐẠI, "
        "trong sáng, dễ hiểu — vẫn giữ không khí kiếm hiệp.\n\n"
        "GIỮ NGUYÊN:\n"
        "- Ngôi thứ nhất 'ta' (KHÔNG đổi thành 'tôi', 'mình').\n"
        "- Mọi sự việc, nhân vật, địa điểm, thứ tự câu. Không thêm, không bớt.\n"
        "- Độ dài tương đương bản gốc (không tóm tắt).\n"
        "- Giữ nguyên tên riêng, thuật ngữ: " + ", ".join(TEN_RIENG) + ".\n"
        "- Nội tâm trong *…*, lời thoại trong “…” như bản gốc.\n"
        "- Giữ đúng các đoạn: chỗ nào bản gốc có dòng trống thì giữ dòng trống.\n\n"
        "TUYỆT ĐỐI KHÔNG dùng từ Hán-Việt cổ. Sai: 'tịch mịch', 'dị hương', 'khứu đại', "
        "'triệt ngộ', 'nguyệt thăng', 'tùng hình', 'u lan', 'mai táng', 'vị tằng', "
        "'phương tri', 'nhất lũ'. Đúng: 'im lặng', 'mùi lạ', 'mũi', 'hiểu ra', "
        "'trăng lên', 'theo nàng mà tới', 'chưa từng', 'mới biết', 'một'.\n"
        "- 'mai táng' chỉ dùng cho chôn người chết. Chôn đồ vật thì dùng 'chôn', 'vùi', 'lấp đất'.\n"
        + _phan_thai_do(npc) +
        "\nViết trọn câu, kết thúc bằng dấu chấm. Chỉ trả về đoạn kể, không giải thích.\n\n"
        f"ĐOẠN GỐC:\n{doan_ke}{phan_boi_canh}{phan_hanh_dong}"
    )
    try:
        ket_qua = _goi_gemini(env, prompt, max_token=1600).strip()
    except Exception:  # noqa: BLE001 - AI lỗi → nơi gọi dùng văn bản gốc
        return ""
    if not ket_qua:
        return ""
    dung, ly_do = van_ban_dung(ket_qua, doan_ke)
    if not dung:
        _so_lan_chan.append((ly_do, ket_qua[:120]))
        return ""
    if len(_cache_ke) >= CACHE_TOI_DA:  # xoá bớt khi cache đầy
        for k in list(_cache_ke)[:100]:
            del _cache_ke[k]
    _cache_ke[khoa] = ket_qua
    return ket_qua


# --------------------------------------------------- nhận diện hành động tự do
# Tập hành động được phép + giới hạn mỗi chỉ số (engine sẽ cắt lại lần nữa).
HANH_DONG_HOP_LE = ["tấn công", "tặng quà", "trò chuyện", "di chuyển",
                    "quan sát", "nghỉ", "khác"]

GIOI_HAN = {
    "sinh_luc": (-15, 10),
    "tu_vi": (0, 8),
    "bac": (-10, 10),
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
        ' "bac": <-10..10>,\n'
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
    for k in ("sinh_luc", "tu_vi", "bac", "than_niem"):
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
