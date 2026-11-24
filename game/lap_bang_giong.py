"""Lập bảng giọng: nhân vật nào nói cảnh nào, giọng chuẩn là câu nào.

Đọc thẳng từ PROMPT nên bảng luôn khớp với prompt thật.
"""
import io
import re
import sys

sys.path.insert(0, "game")
import prompt_am

NHAN_VAT = [
    {
        "ma": "tuyet_co",
        "ten": "Tuyết Cơ",
        "tuoi": "18",
        "gioi": "nữ",
        "mo_ta": "Người quan trọng nhất chương một, xuất hiện nhiều nhất",
        "khop": ["girl's voice, eighteen, sweet"],
        "chuan": "A girl's voice, eighteen, sweet and sultry, breathy, teasing",
        "bien_the": [
            ("trêu đùa, bình thường", "sweet and sultry, breathy, teasing, a little flirtatious"),
            ("khen ngợi", "sweet and sultry, pleased, teasing"),
            ("nghiêm túc, cảnh báo", "sweet but cool and displeased, the teasing gone"),
            ("sốt ruột", "sweet but urgent, then fading"),
            ("mừng, ngạc nhiên", "sweet and delighted, teasing"),
            ("yếu, vừa tỉnh", "sweet and lazy, almost fond"),
            ("song tu", "sweet and breathy, trembling, teasing"),
        ],
    },
    {
        "ma": "nvc",
        "ten": "Nhân vật chính (người chơi)",
        "tuoi": "16",
        "gioi": "nam",
        "mo_ta": "Người chơi — phải cùng một giọng ở mọi cảnh",
        "khop": ["boy's voice, sixteen"],
        "chuan": "A boy's voice, sixteen, low and warm, pleasant",
        "bien_the": [],
    },
    {
        "ma": "kiem_linh",
        "ten": "Kiếm Linh (Hồng Trần)",
        "tuoi": "30",
        "gioi": "nam",
        "mo_ta": "Thanh kiếm nói trong đầu, giọng ma quái",
        "khop": ["man's voice, thirty"],
        "chuan": "A man's voice, thirty, deep and grave, flat and icy",
        "bien_the": [
            ("lạnh, dứt khoát", "deep and clipped, cold"),
            ("đều, vô cảm", "deep and grave, even and emotionless"),
            ("dịu (hiếm khi)", "deep and grave, quiet and unusually gentle"),
        ],
    },
    {
        "ma": "han_lap",
        "ten": "Hàn Lập",
        "tuoi": "18",
        "gioi": "nam",
        "mo_ta": "Đồng môn, lạnh lùng, nói ít",
        "khop": ["young man's voice, eighteen"],
        "chuan": "A young man's voice, eighteen, low and cold",
        "bien_the": [
            ("gần ấm", "low and cool, almost warm"),
            ("có ẩn ý", "low and cold, an edge under it"),
        ],
    },
    {
        "ma": "do_tam",
        "ten": "Đỗ Tam",
        "tuoi": "~40",
        "gioi": "nam",
        "mo_ta": "Kẻ bắt nạt ở tân xá",
        "khop": ["heavy man's voice"],
        "chuan": "A heavy man's voice, around forty, hoarse and gloating",
        "bien_the": [],
    },
    {
        "ma": "mac_dai_phu",
        "ten": "Mạc Đại Phu",
        "tuoi": "~60",
        "gioi": "nam",
        "mo_ta": "Thầy thuốc ở vườn thuốc",
        "khop": ["old man's voice"],
        "chuan": "An old man's voice, quiet and steady",
        "bien_the": [
            ("khô, chậm", "dry and unhurried"),
            ("dò hỏi", "casual but probing"),
        ],
    },
    {
        "ma": "hung_ba",
        "ten": "Hùng Bá",
        "tuoi": "~45",
        "gioi": "nam",
        "mo_ta": "Bang chủ Dã Lang Bang, nói từ xa",
        "khop": ["hoarse heavy male voice"],
        "chuan": "A hoarse heavy male voice, a man around forty-five",
        "bien_the": [],
    },
    {
        "ma": "ga_rau",
        "ten": "Gã râu quai nón",
        "tuoi": "~40",
        "gioi": "nam",
        "mo_ta": "Dân trong thị trấn",
        "khop": ["bearded man's voice"],
        "chuan": "A bearded man's voice, around forty, dropped low and secretive",
        "bien_the": [],
    },
    {
        "ma": "su_huynh_to",
        "ten": "Sư huynh to con",
        "tuoi": "~30",
        "gioi": "nam",
        "mo_ta": "Kẻ bắt nạt ở sân tập",
        "khop": ["big young man's voice", "big man's voice"],
        "chuan": "A big young man's voice, loud and sneering",
        "bien_the": [
            ("giận", "big young man's voice, furious"),
            ("huyênh hoang", "big man's voice, around thirty, loud and blustering"),
        ],
    },
    {
        "ma": "su_huynh_thi_thao",
        "ten": "Sư huynh (chứng kiến)",
        "tuoi": "~25",
        "gioi": "nam",
        "mo_ta": "Người đứng xem, sửng sốt",
        "khop": ["hushed voice"],
        "chuan": "A young man's hushed voice, around twenty-five, startled",
        "bien_the": [],
    },
    {
        "ma": "de_tu_nho",
        "ten": "Đệ tử nhỏ",
        "tuoi": "~14",
        "gioi": "nam",
        "mo_ta": "Đứa trẻ được cứu trong trận",
        "khop": ["around fourteen"],
        "chuan": "A boy's voice, around fourteen, thin and broken",
        "bien_the": [],
    },
    {
        "ma": "phu_khuan_vac",
        "ten": "Phu khuân vác",
        "tuoi": "~35",
        "gioi": "nam",
        "mo_ta": "Người gánh hàng ở chợ",
        "khop": ["porter"],
        "chuan": "A rough male porter's voice, around thirty-five, hoarse and impatient",
        "bien_the": [],
    },
    {
        "ma": "an_may_que",
        "ten": "Lão ăn mày què",
        "tuoi": "~60",
        "gioi": "nam",
        "mo_ta": "Người báo tin ở chợ đêm",
        "khop": ["lame old beggar"],
        "chuan": "A lame old beggar, a man around sixty, mutters low and hoarse",
        "bien_the": [],
    },
    {
        "ma": "hai_de_tu",
        "ten": "Hai đệ tử luyện võ",
        "tuoi": "~20",
        "gioi": "nam",
        "mo_ta": "Hai người nói chuyện ở sân tập",
        "khop": ["two young male disciples"],
        "chuan": "Two young male disciples, both around twenty",
        "bien_the": [],
    },
    {
        "ma": "he_thong",
        "ten": "Hệ thống",
        "tuoi": "—",
        "gioi": "máy",
        "mo_ta": "Giọng máy trong đầu, không ngữ điệu",
        "khop": ["machine-even voice"],
        "chuan": "A flat machine-even voice inside the head",
        "bien_the": [],
    },
]


def lap():
    prompt = prompt_am.PROMPT
    canh_cua = {n["ma"]: [] for n in NHAN_VAT}
    for ma_canh in sorted(prompt):
        than = prompt[ma_canh]
        if "「" not in than:
            continue
        thap = than.lower()
        for n in NHAN_VAT:
            if any(k.lower() in thap for k in n["khop"]):
                canh_cua[n["ma"]].append(ma_canh)
    return canh_cua


def cau_giong(canh):
    """Câu mô tả giọng thật đang dùng trong cảnh đó."""
    than = prompt_am.PROMPT[canh]
    mau = re.findall(
        r"[Aa](?:n |\s)?[\w\s']{0,30}voice[^.:]{0,110}|An old man's voice[^.:]{0,80}"
        r"|Two young male disciples[^:]{0,60}|A lame old beggar[^:]{0,80}",
        than,
    )
    return [m.strip() for m in mau]


if __name__ == "__main__":
    canh_cua = lap()
    tong = sum(len(v) for v in canh_cua.values())
    print(f"cảnh có thoại: {len(prompt_am.PROMPT)} prompt, gán {tong} lượt")
    for n in NHAN_VAT:
        print(f"  {n['ma']:20s} {len(canh_cua[n['ma']]):3d} cảnh")
