"""Cảnh còn thiếu của Chương 2 — Tiểu hội Thái Nam Sơn Cốc.

Chương 2 hiện mượn 4 ảnh của Chương 1 vì hết hạn mức vẽ ảnh. Module này khai
bốn cảnh đúng nghĩa để xưởng ảnh nhắc việc và giữ prompt sẵn: vẽ xong, đặt file
vào assets/scene/ là chương 2 tự dùng ảnh mới, không phải sửa JSON.

Bốn key mượn tạm trong chuong2.json:
  bc_tan_hoang       → thay bằng bc_mac_phu_tang
  bc_duong_mon_nui   → thay bằng bc_thai_nam_hoi
  bc_san_tap_ngay    → thay bằng bc_dai_tuyen
  nv_tuyet_co_do_du  → thay bằng nv_do_linh_can
"""

# key, tên, mô tả dùng ở đâu, mô tả tiếng Anh cho AI vẽ (nối sau STYLE_MAU).
SCENES = [
    {
        "key": "bc_mac_phu_tang",
        "name": "Mạc phủ — tang lễ trong sân",
        "use": "Tang lễ Mạc Đại Phu: sân phủ treo vải trắng, khách khinh khỉnh (c2_d04).",
        "body": "The inner courtyard of a wealthy merchant manor in an ancient Chinese town, "
        "dressed for a funeral at grey morning light, seen at eye level. White hemp mourning "
        "cloth hangs in long strips from the eaves and across the gate, a plain coffin on trestles "
        "at the far side, a few mourners in coarse white standing with bowed heads. Near the gate "
        "a small cluster of well-dressed guests talk among themselves with cool indifferent faces. "
        "Wet flagstones, thin incense smoke, no bright colour anywhere. Composition keeps the upper "
        "third soft and empty for game text. Cold, formal, quietly contemptuous.",
    },
    {
        "key": "bc_thai_nam_hoi",
        "name": "Thái Nam Sơn Cốc — thung lũng hội ban đêm",
        "use": "Lần đầu tới Thái Nam Sơn Cốc: thung lũng đầy đèn lồng, người bay trên trời (c2_d09).",
        "body": "A wide mountain valley at dusk seen from a high ridge, an ancient Chinese cultivators' "
        "gathering filling the floor of the valley. Hundreds of small paper lanterns strung between "
        "tents and low halls glow warm orange in the blue dusk, cooking smoke and pale mist drift "
        "between them, and above the valley a handful of distant figures stand on flying swords, "
        "tiny and weightless against the sky. In the foreground a worn stone step and a thin pine. "
        "Composition keeps the upper sky calm and open for game text. Awe, hunger, a world far above.",
    },
    {
        "key": "bc_dai_tuyen",
        "name": "Đài tuyển — ba tông môn",
        "use": "Đài đá ba tông môn dựng để tuyển người (c2_d12).",
        "body": "A raised platform of packed earth and old stone in an ancient Chinese mountain valley, "
        "set for a sect recruitment at midday. Three tall wooden banners on poles stand behind it, each "
        "a different muted colour, their cloth stirring in the wind; a long plain table with a stone "
        "basin and a ledger sits at the centre. A loose crowd of ragged hopefuls waits below in a "
        "ragged line, and two robed examiners stand above them looking down. Clear hard light, dust, "
        "a ring of pine beyond. Composition keeps the sky and upper third calm for game text. Formal, "
        "judging, a gate that most will not pass.",
    },
    {
        "key": "nv_do_linh_can",
        "name": "Bà lão đo linh căn",
        "use": "Bà lão cầm viên đá đo linh căn, viên đá sáng trắng (c2_d11).",
        "body": "Close portrait of an old woman of an ancient Chinese fantasy world, upper body only, "
        "facing the viewer at a slight angle. A dried, weathered face with deep lines and narrow "
        "unimpressed eyes, grey hair pulled back in a plain bun with a wooden pin, a dull grey robe "
        "with a worn collar. In her raised hand she holds a smooth egg-shaped stone that glows a soft "
        "cold white, its light falling on her fingers and cheek. Behind her a blurred crowd of ragged "
        "youths in the dusk. Background left almost empty with soft ink wash so game text can sit "
        "beside. Weary, indifferent, faintly surprised.",
    },
]

NHOM_CANH = [
    {"ma": "c2-thieu", "phan": "c2", "ten": "Chương 2 — bốn cảnh còn thiếu",
     "mota": "Tang lễ Mạc phủ; thung lũng hội; đài tuyển; bà lão đo linh căn.",
     "keys": ["bc_mac_phu_tang", "bc_thai_nam_hoi", "bc_dai_tuyen", "nv_do_linh_can"],
     "mau": ["nv_chinh_mau"]},
]


def assets(style_mau: str) -> list:
    """Danh sách asset cho tools_server.ASSETS (prompt = STYLE_MAU + mô tả cảnh)."""
    return [
        {
            "key": s["key"],
            "name": s["name"],
            "ratio": "3:4 dọc (900×1200)",
            "file": f'{s["key"]}.jpg',
            "use": s["use"],
            "prompt": f'{style_mau} {s["body"]}',
        }
        for s in SCENES
    ]
