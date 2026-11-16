#!/usr/bin/env python3
"""Xưởng tài nguyên: cung cấp prompt để copy + nhận ảnh upload (dạng base64 JSON).
Chạy: python3 tools_server.py   -> mở http://<host>:12001
Là công cụ tạm, xóa sau khi xong việc."""
import base64
import html as html_lib
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = "/workspace/game-hong-duc-lam"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from game import nhan_dien_anh as ND  # nhận diện ảnh (Gemini vision)
except Exception:
    ND = None
try:
    from game import nen_anh as NEN  # nén ảnh trước khi lưu
except Exception:
    NEN = None
ENV_PATH = f"{ROOT}/.env"
UI_DIR = f"{ROOT}/assets/ui"
SCENE_DIR = f"{ROOT}/assets/scene"
FIELDS = ["OPENROUTER_API_KEY", "geminikey", "geminikey1", "geminikey2", "geminikey3"]

STYLE_GOC = (
    "Traditional East Asian ink wash painting (shui-mo / thủy mặc) on rough handmade mulberry (dó) paper. "
    "Monochrome black ink with subtle warm cream and pale sepia paper tones, visible paper fiber texture, "
    "wet ink bleeding edges, dry brush strokes, generous empty negative space (liubai), "
    "minimal and elegant ancient Chinese hanging-scroll aesthetic, muted and calm. "
)
NO_TEXT = (
    "IMPORTANT: absolutely no text, no letters, no numbers, no calligraphy, no signature, "
    "no watermark, no logo, no UI labels."
)
STYLE = STYLE_GOC + NO_TEXT
# Ấn son là ngoại lệ: chữ trong dấu là nội dung chính, không được cấm chữ.
STYLE_CHU = STYLE_GOC + (
    "IMPORTANT: the ONLY text allowed is the words inside the seal; "
    "no other letters, numbers, signature, watermark, logo or UI labels."
)

ASSETS = [
    {
        "key": "bg-main",
        "name": "1. Nền toàn màn hình",
        "ratio": "9:16 dọc (1080×1920)",
        "file": "bg-main.jpg",
        "use": "Nền sau tất cả (dùng background-size: cover).",
        "prompt": STYLE + " "
        "An almost empty aged-paper background for a mobile game screen, portrait orientation. "
        "Subtle paper texture with faint uneven washes of pale ink near the corners and edges, "
        "a very faint silhouette of distant misty mountains along the very top and bottom edges, "
        "a few tiny scattered ink specks and one or two faint dry-brush strokes at the margins. "
        "The whole center is left empty and light so game text can be placed on top. Low contrast, calm, quiet.",
    },
    {
        "key": "panel-character",
        "name": "2. Khung bảng nhân vật",
        "ratio": "3:4 dọc (900×1200)",
        "file": "panel-character.jpg",
        "use": "Khung bảng chỉ số nhân vật (cột trái). Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A vertical hanging-scroll card for a game interface, portrait orientation. "
        "The border is an irregular hand-painted black ink rectangle with dry-brush ends and slightly wobbly edges, "
        "a few small ink splashes near the corners, and a thin second inner line. "
        "The INSIDE of the panel is plain empty light paper with no decoration at all, reserved for text. "
        "One small red square seal stamp sits in the bottom-right corner of the border. "
        "Flat frontal view, centered, the frame fills almost the entire image with a small even margin.",
    },
    {
        "key": "panel-story",
        "name": "3. Khung bảng truyện",
        "ratio": "4:5 dọc (960×1200)",
        "file": "panel-story.jpg",
        "use": "Khung bảng nội dung câu chuyện. Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A large rectangular story panel for a game interface, portrait orientation, slightly softer and simpler than a scroll. "
        "A rough hand-painted black ink border with rounded irregular corners and light dry-brush texture, "
        "very subtle. The entire interior is plain empty light paper with nothing drawn inside, reserved for long text. "
        "No seal, no ornaments. Flat frontal view, the frame fills almost the whole image with a small even margin.",
    },
    {
        "key": "avatar-ring",
        "name": "4. Viền ảnh đại diện",
        "ratio": "1:1 vuông (1024×1024)",
        "file": "avatar-ring.png",
        "use": "Viền tròn quanh ảnh đại diện (sẽ đè lên ảnh người dùng).",
        "prompt": STYLE + " "
        "A single decorative circular ring for a game avatar frame, centered, on a plain empty light paper background. "
        "The ring is painted with bold black ink brush strokes, uneven and slightly broken, with dry-brush edges "
        "and a few tiny ink splashes. The inside of the circle and everything outside it is completely empty light paper. "
        "Only the ring itself, nothing else, no face, no figure.",
    },
    {
        "key": "btn-choice",
        "name": "5. Nền nút lựa chọn",
        "ratio": "5:1 ngang (1200×240)",
        "file": "btn-choice.jpg",
        "use": "Nền cho các nút chọn A/B/C. Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A wide horizontal blank plaque / name-plate shape for a game button, very wide and short. "
        "Drawn as a simple hand-painted black ink rounded rectangle with thin dry-brush border and slightly wobbly edges. "
        "The interior is plain empty light paper, reserved for a single line of text. Minimal, one ink brush stroke along the bottom edge. "
        "Flat frontal view, the plaque fills almost the whole image.",
    },
    {
        "key": "seal",
        "name": "6. Ấn son (con dấu)",
        "ratio": "1:1 vuông (512×512)",
        "file": "seal.png",
        "use": "Con dấu đỏ trang trí (góc bảng, góc tranh). Chữ bên trong: HỒNG ĐỨC — chữ Latin, font kiểu Hán, xếp DỌC (trên xuống).",
        "prompt": STYLE_CHU + " "
        "A single traditional red seal stamp (chop) on a plain empty light paper background, centered. "
        "A square vermilion-red stamped mark with rough uneven edges like a real ink seal impression, "
        "faded and slightly blotchy, authentic antique look. "
        "CRITICAL LAYOUT — the text inside the seal MUST be on TWO SEPARATE LINES stacked "
        "vertically, like two rows of a Chinese vertical banner read top-to-bottom. "
        "LINE 1 (top half of the square): the word \"HỒNG\". "
        "LINE 2 (bottom half of the square): the word \"ĐỨC\". "
        "Each word is written normally and stays UPRIGHT and readable (do NOT rotate or tilt the "
        "letters, do NOT write the words side by side on one single horizontal line, do NOT write "
        "\"HỒNG ĐỨC\" as one line). The two lines are centered, one above the other, in the Latin "
        "alphabet, ALL CAPITALS. "
        "The letters are NOT in a modern font: they are rendered in a traditional East Asian "
        "calligraphy style, as if the Latin letters were brushed with a Chinese ink brush — "
        "thick tapered brush strokes, angular Han-character (Hán) flavour, classical and ornamented, "
        "like an old Sino-Vietnamese seal inscription. "
        "The two stacked lines fill the square evenly, leaving a small even margin on all sides. "
        "The text is clearly legible and perfectly spelled. "
        "Only these two stacked lines of text, nothing else. Only the seal, nothing else.",
    },
    {
        "key": "divider-ink",
        "name": "7. Đường kẻ mực (tùy chọn)",
        "ratio": "10:1 ngang (1600×160)",
        "file": "divider-ink.jpg",
        "use": "Đường phân cách giữa các mục.",
        "prompt": STYLE + " "
        "A single horizontal decorative divider line for a game interface, extremely wide and short. "
        "A simple black ink brush stroke that starts thin, swells in the middle and fades to a dry broken end, "
        "with one or two small ink splashes. On a plain empty light paper background. "
        "Only the single brush stroke, nothing else.",
    },

    # ---- Bối cảnh truyện (Chương 1) — dùng chung 1 thư viện ảnh cho cả ảnh lẫn video ----
    {
        "key": "bc_cho_01",
        "name": "B.1 Chợ sớm Thất Huyền trấn",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_cho_01.jpg",
        "use": "Cảnh mở đầu — góc chợ sớm, quầy hàng, sọt rách. Dùng cho 6 đoạn (chợ, ngõ, quán nước).",
        "prompt": STYLE + " "
        "An early-morning market street in an ancient Chinese mountain town, seen at eye level. "
        "Rows of humble wooden stalls with awnings, baskets of dried fish and herbs, jars, "
        "a few distant figures in simple cloth robes suggested loosely by a few ink strokes. "
        "Dawn light, thin morning mist drifting between the stalls. "
        "Composition leaves the upper third and one side calm and empty for game text. "
        "Warm cream paper, quiet and lived-in, no dramatic action.",
    },
    {
        "key": "bc_tan_xa_dem",
        "name": "B.2 Tân xá — đêm (phòng tu luyện)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tan_xa_dem.jpg",
        "use": "Phòng ở tập thể môn phái, ban đêm — tu luyện, song tu, đột phá. Dùng nhiều nhất (14 đoạn).",
        "prompt": STYLE + " "
        "A simple communal sleeping quarters in an ancient Chinese martial sect at night, seen from inside. "
        "A low wooden sleeping platform with thin rolled bedding, a small paper-lantern window on one side, "
        "a plain low table with a bowl, bare timber walls and a beam. "
        "Cool blue night light from the window, one warm dim lamp glow, deep quiet shadow in the corners. "
        "Composition keeps the center low and calm so game text can sit above. "
        "Empty, still, faint incense smoke in the air.",
    },
    {
        "key": "vt_ngoc_cot",
        "name": "B.3 Ngọc cốt bí ẩn (vật phẩm cơ duyên)",
        "ratio": "1:1 vuông (1000×1000)",
        "file": "vt_ngoc_cot.jpg",
        "use": "Khối ngọc chứa Tuyết Cơ — hiện ở bảng thông tin cơ duyên + cảnh 'ngọc phát sáng' (6 đoạn).",
        "prompt": STYLE + " "
        "A single mysterious jade bone artifact resting on plain empty paper, centered, still life. "
        "A smooth pale bluish-white jade piece shaped like a slender bone or finger-bone, "
        "faintly glowing from within with a soft cold light, delicate carved cloud patterns on its surface. "
        "A few thin wisps of pale mist curling around it, tiny floating light motes. "
        "Faint reflection shadow beneath. Nothing else in the frame, generous empty space around it. "
        "Cold, mysterious, sacred.",
    },
    {
        "key": "nv_tuyet_co",
        "name": "B.4 Tuyết Cơ (nhân vật)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_tuyet_co.jpg",
        "use": "Nữ tu Hợp Hoan Tông trong ngọc cốt — chân dung gợi cảm, quyến rũ, bí ẩn (25 đoạn nhắc tên).",
        "prompt": STYLE + " "
        "Portrait of a stunningly beautiful, sensual and mysterious female cultivator of an ancient "
        "Chinese fantasy sect, upper body only, facing the viewer at a slight angle. Young woman with "
        "luminous pale jade-like skin, long black hair partly loose and partly pinned with a simple jade "
        "hairpin, a few loose strands falling across her cheek, slender willow brows, long half-lidded "
        "sultry eyes with a teasing, knowing gaze, and a faintly flirtatious half-smile. She wears "
        "flowing pale blue-and-white silk robes of thin translucent gauze that slip off one shoulder, "
        "revealing a bare collarbone, the soft curve of her neck and a hint of décolletage, the fabric "
        "clinging softly to her figure; a sheer gauze veil draping loosely around her bare arms. "
        "Faint cold mist and a subtle inner glow surround her, like a spirit sealed for ages — "
        "alluring yet dangerous and enigmatic. "
        "Background left almost empty with soft ink wash so game text can sit beside. "
        "Sensual, seductive, elegant, mysterious, ethereal.",
    },

    # ---- NHÁNH TÁN TU (Chương 1) — mạch miếu hoang & Hồng Trần Kiếm Hạp ----
    {
        "key": "bc_duong_mon_nui",
        "name": "C.1 Đường mòn lên núi — chạng vạng",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_duong_mon_nui.jpg",
        "use": "Đường mòn hẹp dẫn lên núi, cỏ dại cao quá đầu, trời nhá nhem (đoạn d03).",
        "prompt": STYLE + " "
        "A narrow steep mountain footpath at dusk, seen from the walker's eye level, leading up into "
        "dark wooded hills. Tall wild grass and weeds crowd both sides of the path higher than a person, "
        "a few bare rocks and twisted pine trunks, faint mist gathering low between the slopes. "
        "Deep blue-grey twilight sky, a sliver of pale moon just rising, the last dim light on the horizon. "
        "The path curves away into shadow and disappears, lonely and slightly ominous. "
        "Composition keeps the upper part calm and empty for game text. Quiet, solitary, a little eerie.",
    },
    {
        "key": "bc_mieu_hoang",
        "name": "C.2 Miếu hoang sau núi (bối cảnh chính nhánh tán tu)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_mieu_hoang.jpg",
        "use": "Miếu hoang — xương khô, vết cào trên vách, hộp gỗ đen (d04, d04b, d04c, d04d, d09, d10).",
        "prompt": STYLE + " "
        "The interior of a small abandoned wayside shrine deep in the mountains at night, seen from inside. "
        "Broken timber walls, a fallen roof beam, torn paper offerings and cobwebs, a cracked stone altar "
        "with a faded statue. Dry fallen leaves and dust on the floor, deep claw-mark scratches gouged "
        "across the wooden wall, a few scattered old bones in the shadowed corner. "
        "A cold shaft of moonlight falls through a gap in the roof onto the empty floor in the center. "
        "A long dark wooden box rests low and undisturbed in the middle of the beam of light. "
        "Composition keeps the center low and calm so game text can sit above. "
        "Ruined, silent, desolate, faintly menacing.",
    },
    {
        "key": "vt_kiem_hap",
        "name": "C.3 Hồng Trần Kiếm Hạp (vật phẩm cơ duyên nhánh tán tu)",
        "ratio": "1:1 vuông (1000×1000)",
        "file": "vt_kiem_hap.jpg",
        "use": "Hộp gỗ đen + cặp kiếm dài-ngắn chứa kiếm linh (d05, d08). Ảnh cho bảng Cơ duyên.",
        "prompt": STYLE + " "
        "A single ancient long black wooden sword box on plain empty paper, centered, still life. "
        "The box is open, dark lacquered wood carved with faint cloud-pattern lines, and inside it rest "
        "two swords — one long and one short — lying side by side, their sheaths plain dark with worn "
        "brass fittings, a faint cold light glimmering along the exposed blades. "
        "A few thin wisps of pale mist curling around the box, tiny floating light motes. "
        "Faint reflection shadow beneath. Nothing else in the frame, generous empty space around it. "
        "Ancient, solemn, mysterious, faintly dangerous.",
    },
    {
        "key": "nv_kiem_linh",
        "name": "C.4 Kiếm linh Hồng Trần (nhân vật)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_kiem_linh.jpg",
        "use": "Kiếm linh — thanh niên áo trắng, mặt lạnh, mắt sáng như kiếm quang (d06, d06b, d07, d07b).",
        "prompt": STYLE + " "
        "Portrait of a ghostly young male sword spirit of an ancient Chinese fantasy world, upper body only, "
        "facing the viewer at a slight angle. A pale slender young man in plain flowing white robes, "
        "long black hair tied loosely, a cold composed face, sharp bright eyes like the gleam of a blade, "
        "thin brows, a faintly stern unsmiling expression. He is a spirit, not fully solid — his form "
        "shimmers faintly and fades to mist at the edges, surrounded by a thin cold glow and a few drifting "
        "wisps of pale mist. One slender sword is half-raised behind him, catching a cold light. "
        "Background left almost empty with soft ink wash so game text can sit beside. "
        "Cold, ethereal, austere, dignified, a little haunting.",
    },
    {
        "key": "bc_tran_lua",
        "name": "C.5 Trấn Thất Huyền chìm trong lửa (Dã Lang Bang tập kích)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tran_lua.jpg",
        "use": "Trấn cháy, cướp Dã Lang Bang tấn công (d11, d12, d13 và p13, p14, p14b-e).",
        "prompt": STYLE + " "
        "An ancient Chinese mountain market town burning at night during a bandit raid, seen from a "
        "distance at eye level. Rows of wooden houses and stalls engulfed in tall orange flames, thick "
        "black smoke rolling up into the dark sky, sparks drifting in the air. Small distant silhouettes "
        "of fleeing townsfolk and mounted raiders suggested loosely by a few ink strokes. "
        "A broken gate and fallen banners at the town edge, embers glowing on the ground. "
        "Dramatic contrast of firelight against the deep night, but rendered in restrained ink-wash tones. "
        "Composition keeps the upper part smoky and calm for game text. Chaotic, tragic, tense.",
    },
    {
        "key": "bc_tan_hoang",
        "name": "C.6 Sau trận — giữa đống đổ nát (bình minh)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tan_hoang.jpg",
        "use": "Thất Huyền trấn / Thất Huyền Môn tan hoang khi trời gần sáng (d14, p16).",
        "prompt": STYLE + " "
        "The aftermath of a battle in an ancient Chinese mountain town at first grey dawn, seen from "
        "inside the ruins. Collapsed charred timber buildings, broken stone steps, torn banners lying in "
        "the dust, thin smoke still curling from the wreckage, ash scattered on the ground. "
        "A few weary distant figures quietly carrying the fallen, suggested loosely by a few ink strokes. "
        "Pale cold dawn light, low mist over the ruins, the sky almost empty and grey. "
        "Composition keeps the center low and calm so game text can sit above. "
        "Desolate, quiet, sorrowful, exhausted.",
    },
    {
        "key": "nv_han_lap",
        "name": "C.7 Hàn Lập (nhân vật — crossover Phàm Nhân Tu Tiên)",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_han_lap.jpg",
        "use": "Hàn Lập — thanh niên gầy, mắt sắc như dao, áo vải thô (d15, d16 và p17, p18a-d).",
        "prompt": STYLE + " "
        "Portrait of a lean, ordinary-looking young man of an ancient Chinese fantasy world, upper body "
        "only, facing the viewer at a slight angle. A thin plain-featured youth in coarse undyed cloth "
        "robes, simple cloth belt, black hair tied in a plain topknot, no ornament of any kind. "
        "His most striking feature is his eyes: calm, deep and sharp as a knife, watchful and unreadable, "
        "the gaze of someone far more than he appears. His expression is composed and reserved. "
        "He stands quietly in the shadow of a hillside at dusk, faint cold mist behind him. "
        "Background left almost empty with soft ink wash so game text can sit beside. "
        "Plain, quiet, sharp-eyed, quietly formidable, understated.",
    },
    {
        "key": "bc_binh_minh",
        "name": "C.8 Kết chương — bình minh Thất Huyền trấn",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_binh_minh.jpg",
        "use": "Ánh bình minh đầu tiên rọi lên vai áo rách — kết chương 1 (d17, p19).",
        "prompt": STYLE + " "
        "First dawn light breaking over an ancient Chinese mountain town and its hillside, seen at eye "
        "level. Soft warm sunrise glow spreading across the sky, long pale rays through low mist, the "
        "distant roofs and mountain ridges fading into gentle haze, a few birds in flight. "
        "The foreground is quiet and almost empty — a worn stone path and a thin bare tree by the way. "
        "Hopeful and calm after hardship, cool morning air. "
        "Composition keeps the upper third soft and empty for game text. Serene, gentle, new beginning.",
    },
]


def load_env():
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                env[k] = v
    return env


def save_env(pairs):
    lines = [f"{k}={v}" for k, v in pairs.items() if v]
    if "GEMINI_MODEL" not in pairs:
        lines.append("GEMINI_MODEL=gemini-2.5-flash-image")
    if "IMAGE_MODEL" not in pairs:
        lines.append("IMAGE_MODEL=google/gemini-3.1-flash-image")
    with open(ENV_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(ENV_PATH, 0o600)


def list_files(folder):
    if not os.path.isdir(folder):
        return []
    out = []
    for fn in sorted(os.listdir(folder)):
        p = os.path.join(folder, fn)
        if os.path.isfile(p):
            out.append((fn, os.path.getsize(p)))
    return out


def build_prompts_html():
    blocks = []
    for a in ASSETS:
        got = ""
        for fn, size in list_files(UI_DIR) + list_files(SCENE_DIR):
            if fn == a["file"]:
                got = f'<span class="got">✔ đã nhận ({size//1024} KB)</span>'
        blocks.append(f"""
<div class="card">
  <div class="head"><b>{a['name']}</b> <span class="ratio">{a['ratio']}</span> {got}</div>
  <div class="use">{a['use']} &nbsp;·&nbsp; tên file khi lưu: <code>{a['file']}</code></div>
  <textarea readonly rows="6" onclick="this.select()">{a['prompt']}</textarea>
  <button class="cp" onclick="cp(this)">📋 Copy prompt</button>
</div>""")
    return "\n".join(blocks)


def build_received_html():
    rows = []
    for folder, label in ((UI_DIR, "Giao diện"), (SCENE_DIR, "Bối cảnh")):
        for fn, size in list_files(folder):
            rows.append(f"<li>{label}: <b>{fn}</b> — {size//1024} KB</li>")
    thieu = con_thieu_anh()
    tong = len(ASSETS)
    if thieu:
        ds = ", ".join(f"<code>{a['file']}</code>" for a in thieu)
        nhac = (f"<p class='warn'>⚠️ Còn thiếu <b>{len(thieu)}/{tong}</b> ảnh: {ds}</p>")
    else:
        nhac = f"<p class='ok'>✅ Đã đủ {tong}/{tong} ảnh.</p>"
    if not rows:
        return nhac + "<p class='muted'>Chưa nhận được ảnh nào.</p>"
    return nhac + "<ul>" + "".join(rows) + "</ul>"


def _prompt_than(a: dict) -> str:
    """Bỏ phần phong cách chung, chỉ giữ mô tả riêng của asset."""
    p = a.get("prompt", "")
    for pref in (STYLE_CHU, STYLE):
        if p.startswith(pref):
            return p[len(pref):].strip()
    return p.strip()


def build_gop_prompt() -> str:
    """Một prompt gộp: dán 1 lần vào AI chat là nó vẽ lần lượt cả bộ ảnh."""
    dong = [
        'TASK: Create the full image set for a Vietnamese cultivation game named '
        '"Hồng Đức Tu Tiên Lộ".',
        "Produce the images ONE BY ONE, in the order below, each as a SEPARATE image at its "
        "own aspect ratio.",
        "If you cannot finish them all in one reply, make as many as you can and then stop; "
        'I will reply "tiếp tục" to get the next batch.',
        "",
        "SHARED ART STYLE (apply to EVERY image): " + STYLE_GOC.strip(),
        "",
        "TEXT RULE: no text, no letters, no numbers, no calligraphy, no signature, no watermark, "
        "no logo in ANY image. The ONLY exception is image 6 (the seal): inside the seal it must show "
        "the words \"HỒNG\" and \"ĐỨC\" in Latin capitals, drawn in a Chinese ink-brush (Hán) "
        "calligraphy style and stacked vertically one above the other (HỒNG on top, ĐỨC below), "
        "and nothing else.",
        "",
    ]
    for i, a in enumerate(ASSETS, 1):
        dong.append(f"{i}. {a['file']} — {a['ratio']} — {a['name']}")
        dong.append(f"   {_prompt_than(a)}")
        dong.append("")
    return "\n".join(dong)


def page():
    env = load_env()
    keys_html = "".join(
        f'<label>{k}</label><input name="{k}" placeholder="{"sk-or-v1-..." if "OPENROUTER" in k else "AIza... / AQ..."}" '
        f'value="{env.get(k, "")[:0]}" autocomplete="off" autocapitalize="off">'
        for k in FIELDS
    )
    html = PAGE_TMPL
    html = html.replace("__PROMPTS__", build_prompts_html())
    html = html.replace("__RECEIVED__", build_received_html())
    html = html.replace("__KEYS__", keys_html)
    ds = [{"key": a["key"], "name": a["name"]} for a in ASSETS]
    html = html.replace("__ASSET_JSON__", json.dumps(ds, ensure_ascii=False))
    html = html.replace("__GOP_PROMPT__", html_lib.escape(build_gop_prompt()))
    return html


PAGE_TMPL = """<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xưởng tài nguyên — Hồng Đức Tu Tiên Lộ</title>
<style>
 :root{--bg:#111a2b;--card:#182337;--ink:#e8e6df;--muted:#93a0b8;--gold:#ffd98a;--jade:#6fe0c0;--line:#2b3b57}
 *{box-sizing:border-box}
 body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--ink);
   margin:0;padding:18px;max-width:720px;margin:0 auto;line-height:1.55;-webkit-text-size-adjust:100%}
 h1{font-size:19px;color:var(--gold);margin:6px 0 2px}
 h2{font-size:15px;color:var(--jade);margin:26px 0 8px;border-bottom:1px solid var(--line);padding-bottom:6px}
 p,li{font-size:13.5px;color:#cbd4e4}
 .muted{color:var(--muted)}
 code{background:#0a1220;padding:1px 6px;border-radius:4px;color:var(--jade);font-size:12px}
 .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
 .head{font-size:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
 .ratio{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
 .got{font-size:11px;color:#7fe0a8;background:#12351f;padding:2px 8px;border-radius:99px}
 .use{font-size:12px;color:var(--muted);margin:6px 0 8px}
 textarea{width:100%;font-size:12.5px;line-height:1.5;background:#0a1220;color:#dfe7f5;border:1px solid var(--line);
   border-radius:8px;padding:10px;resize:vertical;font-family:ui-monospace,Menlo,monospace}
 button{font-family:inherit;font-size:14px;font-weight:600;border:0;border-radius:10px;padding:11px 16px;cursor:pointer}
 .cp{margin-top:8px;background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600;width:100%}
 .cp.done{background:#2f8f5a;color:#eafff3}
 .up{background:linear-gradient(135deg,#2f8f7a,#6fe0c0);color:#04231c;width:100%;margin-top:10px}
 .ok{background:#12351f;border:1px solid #2f8f5a;padding:12px;border-radius:10px;color:#7fe0a8;font-size:13px}
 .warn{background:#3a1a10;border:1px solid #a05a2a;padding:12px;border-radius:10px;color:#ffb98a;font-size:13px}
 label{display:block;font-size:12px;color:var(--muted);margin:12px 0 4px}
 input{width:100%;padding:12px;font-size:14px;border-radius:9px;border:1px solid var(--line);
   background:#0a1220;color:var(--ink)}
 #drop{border:2px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--muted);
   font-size:13px;margin:10px 0;cursor:pointer}
 #drop.hot{border-color:var(--jade);color:var(--jade);background:#0f2230}
 ul{padding-left:18px}
 details{margin-top:22px}
 summary{cursor:pointer;color:var(--muted);font-size:13px}
 .steps li{margin:5px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:10px 0}
.item{background:#0f1728;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.item img{width:100%;height:150px;object-fit:cover;display:block;background:#0a1220}
.item .meta{padding:8px}
.item select{width:100%;margin:6px 0 4px;padding:8px;border-radius:8px;border:1px solid var(--line);
  background:#0a1220;color:var(--ink);font-size:12.5px}
.badge{display:inline-block;font-size:11px;padding:2px 8px;border-radius:99px;background:#0a1220;color:var(--muted)}
.badge.chac{background:#12351f;color:#7fe0a8}
</style></head><body>

<h1>Xưởng tài nguyên</h1>
<p class="muted">Hồng Đức Tu Tiên Lộ · quy trình: bạn copy prompt → AI của bạn vẽ → bạn tải ảnh lên đây → tôi ghép vào game.</p>

<h2>Cách làm</h2>
<ol class="steps">
  <li><b>Cách nhanh:</b> ở khu <b>🎨 Vẽ cả bộ bằng 1 prompt</b> bên dưới, bấm <b>Copy</b> rồi dán
      <b>một lần</b> vào AI của bạn — nó vẽ lần lượt cả bộ ảnh. Hết lượt thì nhắn <b>“tiếp tục”</b>.</li>
  <li><b>Cách lẻ:</b> hoặc copy từng prompt ở danh sách dưới, dán vào AI, chọn đúng <b>tỷ lệ</b> ghi trên thẻ.</li>
  <li>Lưu ảnh về máy — <b>không cần đổi tên</b> (tên <code>IMG_1234.JPG</code> cũng được).</li>
  <li>Kéo <b>tất cả</b> ảnh vào ô <b>Tải ảnh lên</b> ở cuối trang (chọn nhiều ảnh một lúc).</li>
  <li>AI tự đoán mỗi ảnh thuộc prompt nào (theo tỷ lệ + nội dung). Ảnh nào chắc chắn thì tự gán;
      ảnh nào chưa chắc thì hiện lưới để bạn <b>xác nhận</b>.</li>
  <li>Bấm <b>Lưu ảnh</b> — xong, không cần đặt tên file bao giờ.</li>
</ol>
<p class="muted">Lưu ý: prompt đã ghi rõ <b>không có chữ/ký tự</b> trong ảnh (trừ ảnh ấn son — chữ Hồng Đức),
vì chữ do AI vẽ thường sai. Chữ trong game do tôi viết bằng code.</p>

<h2>🎨 Vẽ cả bộ bằng 1 prompt (đỡ copy từng cái)</h2>
<div class="card">
  <p class="muted">Bấm <b>Copy</b> rồi dán <b>một lần</b> vào Gemini chat — nó sẽ vẽ lần lượt
  các ảnh theo đúng tỷ lệ. Hết lượt thì nhắn <b>“tiếp tục”</b> để lấy ảnh còn lại.</p>
  <textarea readonly rows="10" id="gop" onclick="this.select()">__GOP_PROMPT__</textarea>
  <button class="cp" onclick="cpText('gop', this)">📋 Copy prompt gộp</button>
  <button class="up" onclick="taiPromptGop()">⬇️ Tải về file .txt</button>
</div>

<h2>Danh sách prompt</h2>
__PROMPTS__

<h2>Ảnh đã nhận</h2>
<div class="card">__RECEIVED__</div>

<h2>Tải ảnh lên</h2>
<div class="card">
  <div id="drop">Bấm để chọn ảnh, hoặc kéo ảnh vào đây<br><span class="muted">(chọn nhiều ảnh một lúc — tên gì cũng được)</span></div>
  <input id="file" type="file" accept="image/*" multiple hidden>
  <button class="up" onclick="document.getElementById('file').click()">Chọn ảnh để tải lên</button>
  <div id="msg"></div>
</div>

<div id="review" style="display:none">
  <h2>Duyệt ảnh</h2>
  <p class="muted" id="reviewHint"></p>
  <div class="grid" id="grid"></div>
  <button class="up" id="saveBtn" onclick="luuLoat()">💾 Lưu ảnh</button>
  <div id="saveMsg"></div>
</div>

<details>
  <summary>Cập nhật key (chỉ khi cần đổi)</summary>
  <form method="POST" action="/keys">
    __KEYS__
    <button class="up" type="submit" style="margin-top:14px">Lưu key</button>
  </form>
</details>

<script>
const DANH_SACH = __ASSET_JSON__;
function cp(btn){ cpText(null, btn); }
function cpText(id, btn){
  const ta = id ? document.getElementById(id) : btn.parentElement.querySelector('textarea');
  ta.select(); ta.setSelectionRange(0, 999999);
  const done = () => { btn.classList.add('done'); btn.textContent='✅ Đã copy';
    setTimeout(()=>{btn.classList.remove('done');btn.textContent='📋 Copy prompt';},1600); };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(ta.value).then(done).catch(()=>{ try{document.execCommand('copy');done();}catch(e){} });
  } else { try{document.execCommand('copy');done();}catch(e){} }
}
function taiPromptGop(){
  const txt = document.getElementById('gop').value;
  const blob = new Blob([txt], {type:'text/plain;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'hong-duc-prompt-ve-anh.txt';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
}
const drop=document.getElementById('drop'), fileInput=document.getElementById('file'), msg=document.getElementById('msg');
drop.onclick=()=>fileInput.click();
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.add('hot');}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.remove('hot');}));
drop.addEventListener('drop',ev=>nhanAnh(ev.dataTransfer.files));
fileInput.onchange=()=>nhanAnh(fileInput.files);

function docB64(f){return new Promise(res=>{const r=new FileReader();r.onload=()=>res(r.result.split(',')[1]);r.readAsDataURL(f);});}

async function nhanAnh(files){
  if(!files || !files.length) return;
  msg.innerHTML='<p class="muted">Đang đọc ảnh…</p>';
  const anh=[];
  for(const f of files){
    if(!f.type.startsWith('image/')) continue;
    anh.push({name:f.name, data:await docB64(f)});
  }
  if(!anh.length){ msg.innerHTML='<p class="warn">Không có ảnh hợp lệ.</p>'; return; }
  msg.innerHTML=`<p class="muted">Đang để AI nhận diện ${anh.length} ảnh… (chờ chút)</p>`;
  try{
    const r = await fetch('/doan_anh',{method:'POST',headers:{'Content-Type':'application/json'},
      body: JSON.stringify({anh})});
    const j = await r.json();
    if(!j.ok){ msg.innerHTML=`<p class="warn">⚠️ ${j.error||'lỗi'}</p>`; return; }
    hienDuyet(j.ket_qua, anh);
    msg.innerHTML=`<p class="ok">✅ Đã nhận diện ${anh.length} ảnh — xem khu <b>Duyệt ảnh</b> bên dưới.</p>`;
  }catch(e){ msg.innerHTML=`<p class="warn">⚠️ Lỗi: ${e}</p>`; }
}

let HANG_DOI = [];
function hienDuyet(ket_qua, anh){
  HANG_DOI = ket_qua.map((k,i)=>({...k, data: (anh[i]||{}).data}));
  const grid=document.getElementById('grid');
  const chac = HANG_DOI.filter(k=>k.tu_dong).length;
  document.getElementById('review').style.display='block';
  document.getElementById('reviewHint').textContent =
    `${HANG_DOI.length} ảnh · ${chac} ảnh AI chắc chắn (tự gán) · ${HANG_DOI.length-chac} ảnh cần bạn xác nhận.`;
  grid.innerHTML = HANG_DOI.map((k,i)=>`
    <div class="item">
      <img src="data:image/jpeg;base64,${k.data||''}" alt="">
      <div class="meta">
        <div><span class="badge ${k.tu_dong?'chac':''}">${k.tu_dong?'AI chắc':'Cần duyệt'} · ${k.do_tin_cay||0}%</span></div>
        <div class="muted" style="font-size:11px;margin-top:4px">${k.kich_thuoc||''}</div>
        <select id="sel${i}" onchange="HANG_DOI[${i}].key=this.value">
          <option value="">— chọn prompt —</option>
          ${DANH_SACH.map(a=>`<option value="${a.key}" ${a.key===k.key?'selected':''}>${a.name}</option>`).join('')}
        </select>
        <div class="muted" style="font-size:11px">${k.mo_ta?k.mo_ta:''}</div>
      </div>
    </div>`).join('');
}

async function luuLoat(){
  const ds = HANG_DOI.filter(k=>k.key).map(k=>({key:k.key, data:k.data}));
  if(!ds.length){ document.getElementById('saveMsg').innerHTML='<p class="warn">Chưa chọn prompt nào.</p>'; return; }
  document.getElementById('saveMsg').innerHTML='<p class="muted">Đang lưu…</p>';
  try{
    const r = await fetch('/luu_loat',{method:'POST',headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ds})});
    const j = await r.json();
    if(!j.ok){ document.getElementById('saveMsg').innerHTML=`<p class="warn">⚠️ ${j.error||'lỗi'}</p>`; return; }
    document.getElementById('saveMsg').innerHTML =
      `<p class="ok">✅ Đã lưu ${j.da_luu.length} ảnh: ${j.da_luu.map(x=>x.file).join(', ')}</p>
       <p class="muted">Tải lại trang để xem danh sách "Ảnh đã nhận".</p>`;
  }catch(e){ document.getElementById('saveMsg').innerHTML=`<p class="warn">⚠️ Lỗi: ${e}</p>`; }
}
</script>
</body></html>"""


def keys_page(msg=""):
    env = load_env()
    keys_html = "".join(
        f'<label>{k}</label><input name="{k}" autocomplete="off" autocapitalize="off">' for k in FIELDS
    )
    return f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Cập nhật key</title>
<style>body{{font-family:-apple-system,sans-serif;background:#111a2b;color:#e8e6df;padding:20px;max-width:560px;margin:auto}}
label{{display:block;font-size:13px;color:#93a0b8;margin:14px 0 5px}}
input{{width:100%;padding:13px;border-radius:9px;border:1px solid #2b3b57;background:#0a1220;color:#e8e6df}}
button{{width:100%;margin-top:20px;padding:15px;border:0;border-radius:11px;font-size:16px;font-weight:600;
  background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600}}
.ok{{background:#12351f;border:1px solid #2f8f5a;padding:12px;border-radius:10px;color:#7fe0a8}}
a{{color:#6fe0c0}}</style></head><body>
<h1 style="font-size:18px;color:#ffd98a">Cập nhật key</h1>
{msg}
<form method="POST" action="/keys">{keys_html}<button type="submit">Lưu key</button></form>
<p><a href="/">← về Xưởng</a></p>
</body></html>"""


def luu_anh(name: str, b64: str, dich_ten: str = "", key: str = "") -> str:
    """Lưu ảnh upload (đã nén) vào assets/ và bản web docs/assets/.

    - Ảnh cảnh (bc_/vt_/nv_) -> assets/scene/ + docs/assets/scene/
    - Ảnh giao diện còn lại -> assets/ui/ + docs/assets/ui/
    - Bản gốc (chưa nén) lưu vào assets/ui-orig/ hoặc assets/scene-orig/ (đã gitignore).
    - Nén theo game.nen_anh; thiếu Pillow thì lưu nguyên gốc.

    dich_ten: đặt tên file theo tên này (bỏ qua tên gốc) khi đã xác nhận asset.
    key: dùng để tra quy tắc nén (tỷ lệ/định dạng/cỡ đích).
    """
    name = os.path.basename(dich_ten or name or "image.png") or "image.png"
    if not re.search(r"\.(png|jpe?g|webp|gif)$", name, re.I):
        name += ".png"
    goc = base64.b64decode(b64)

    la_canh = bool(re.match(r"^(bc_|vt_|nv_)", name))
    if la_canh:
        dest, web, orig = SCENE_DIR, f"{ROOT}/docs/assets/scene", f"{ROOT}/assets/scene-orig"
    else:
        dest, web, orig = UI_DIR, f"{ROOT}/docs/assets/ui", f"{ROOT}/assets/ui-orig"

    # Bản gốc để riêng (không commit), phòng khi cần nén lại.
    os.makedirs(orig, exist_ok=True)
    with open(os.path.join(orig, name), "wb") as f:
        f.write(goc)

    data = None
    if NEN is not None:
        data = NEN.nen(goc, key=key, ten_file=name)
    if data is None:
        data = goc  # không nén được: vẫn lưu nguyên để không vỡ luồng

    for folder in (dest, web):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, name), "wb") as f:
            f.write(data)
    return name


def luu_theo_key(key: str, b64: str) -> str:
    """Lưu ảnh vào đúng tên file của asset (theo key). Trả tên file đã lưu."""
    for a in ASSETS:
        if a["key"] == key:
            return luu_anh(a["file"], b64, key=key)
    raise ValueError(f"Không có asset với key {key!r}")


def con_thieu_anh() -> list:
    """Danh sách asset chưa có file (để nhắc người dùng vẽ gì tiếp)."""
    co = {fn for fn, _ in list_files(UI_DIR) + list_files(SCENE_DIR)}
    return [a for a in ASSETS if a["file"] not in co]


# ------------------------------------------------------- xử lý yêu cầu (dùng chung)
def _asset_theo_key(key: str):
    for a in ASSETS:
        if a["key"] == key:
            return a
    return None


def xu_ly_nhan_dien(anh_list: list, env: dict) -> dict:
    """Nhận diện loạt ảnh. anh_list: [{name, data(base64)}].

    Trả {ket_qua: [{name, kich_thuoc, ung_vien, key, ten, do_tin_cay, mo_ta, ly_do, tu_dong}],
         loi}.
    `tu_dong` = True khi độ tin cậy >= 80 (giao diện tự gán, không cần người dùng xác nhận).
    """
    if ND is None:
        return {"loi": "Thiếu mô-đun nhận diện ảnh", "ket_qua": []}
    kq = []
    for item in anh_list or []:
        ten_goc = os.path.basename(item.get("name", "") or "image")
        try:
            data = base64.b64decode(item.get("data", ""))
        except Exception:
            kq.append({"name": ten_goc, "loi": "Dữ liệu ảnh hỏng"})
            continue
        mime = "image/jpeg" if re.search(r"\.jpe?g$", ten_goc, re.I) else "image/png"
        if re.search(r"\.webp$", ten_goc, re.I):
            mime = "image/webp"
        if re.search(r"\.gif$", ten_goc, re.I):
            mime = "image/gif"
        r = ND.goi_y_mot_anh(data, mime, ASSETS, env)
        a = _asset_theo_key(r.get("key") or "")
        r["name"] = ten_goc
        r["ten"] = a["name"] if a else ""
        r["file"] = a["file"] if a else ""
        r["tu_dong"] = bool(r.get("key") and r.get("do_tin_cay", 0) >= 80)
        kq.append(r)
    return {"ket_qua": kq, "loi": ""}


def xu_ly_luu_loat(ds: list) -> dict:
    """Lưu loạt ảnh đã xác nhận. ds: [{key, data(base64)}]. Trả {da_luu, loi}."""
    da_luu = []
    for item in ds or []:
        key = item.get("key") or ""
        if not key:
            continue
        try:
            ten = luu_theo_key(key, item.get("data", ""))
            da_luu.append({"key": key, "file": ten})
        except Exception as e:
            return {"da_luu": da_luu, "loi": str(e)}
    return {"da_luu": da_luu, "loi": ""}


class H(BaseHTTPRequestHandler):
    def _send(self, body, code=200, ctype="text/html; charset=utf-8"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.startswith("/keys"):
            self._send(keys_page())
        elif self.path.startswith("/upload"):
            self._send(json.dumps({"ok": False, "error": "dùng POST"}), ctype="application/json")
        else:
            self._send(page())

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)
        if self.path.startswith("/upload"):
            try:
                j = json.loads(raw.decode())
                name = luu_anh(j.get("name", "image.png"), j["data"], j.get("dich_ten", ""))
                self._send(json.dumps({"ok": True, "saved": name}), ctype="application/json")
            except Exception as e:
                self._send(json.dumps({"ok": False, "error": str(e)}), ctype="application/json")
            return
        if self.path.startswith("/doan_anh"):
            try:
                j = json.loads(raw.decode())
                r = xu_ly_nhan_dien(j.get("anh", []), load_env())
                self._send(json.dumps({"ok": True, **r}, ensure_ascii=False),
                           ctype="application/json")
            except Exception as e:
                self._send(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False),
                           ctype="application/json")
            return
        if self.path.startswith("/luu_loat"):
            try:
                j = json.loads(raw.decode())
                r = xu_ly_luu_loat(j.get("ds", []))
                self._send(json.dumps({"ok": True, **r}, ensure_ascii=False),
                           ctype="application/json")
            except Exception as e:
                self._send(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False),
                           ctype="application/json")
            return
        # /keys
        from urllib.parse import parse_qs
        data = parse_qs(raw.decode())
        env = load_env()
        for k in FIELDS:
            v = (data.get(k, [""])[0] or "").strip()
            if v:
                env[k] = v
        save_env(env)
        self._send(keys_page('<p class="ok">✅ Đã lưu key.</p>'))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Xưởng chạy tại http://0.0.0.0:12001")
    HTTPServer(("0.0.0.0", 12001), H).serve_forever()
