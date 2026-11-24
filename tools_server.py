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

ROOT = os.path.dirname(os.path.abspath(__file__))
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
    "Painterly cinematic East Asian ink painting, in the manner of a realistic historical "
    "illustration, on smooth handmade mulberry (dó) paper. Soft blended edges, volumetric shading, "
    "atmospheric depth, realistic anatomy, detailed fabric folds. Muted desaturated palette, mostly "
    "black ink and bare paper, restrained washes, calm and elegant hanging-scroll mood. "
    "NOT folk art, NOT flat cartoon, NOT comic-book linework. "
)
# Chống nét gãy, nhưng KHÔNG ép nét viền sắc: chính viền đen sắc trên nền phẳng là thứ
# đọc ra thành răng cưa. Khối lượng do nhiều lớp wash chuyển dần, mép tan vào giấy.
NET_MEM = (
    "Build every form with soft blended edges and graduated tone instead of hard black contours: "
    "no bold black outline, no flat fill, no clean crisp comic linework. Volume comes from layered "
    "washes turning gradually from dark to light, with the edges of shadows melting into the paper. "
    "Even so, never jagged: no zigzag edges, no sketchy broken lines, no short choppy overlapping "
    "strokes, no scribbled shapes, no speckle, no splatter, no bleeding halo. "
)
# 彩墨 (cǎi-mò) — thủy mặc ĐIỂM MÀU: vẫn chủ đạo mực đen trên giấy dó, chỉ phủ thêm
# vài mảng màu trầm. Dùng cho ảnh truyện/nhân vật (không dùng cho ảnh giao diện).
MAU_GOC = (
    "Painterly cinematic East Asian colour-ink painting (cǎi-mò / 彩墨) in the manner of a realistic "
    "historical illustration, on smooth handmade mulberry (dó) paper. Soft blended edges, volumetric "
    "shading, atmospheric depth, realistic anatomy, detailed fabric folds. The picture stays dominated "
    "by black ink and bare pale dó paper, with only restrained, muted washes of soft colour laid over "
    "the ink, so the palette stays desaturated and quiet: soft indigo and slate blue for sky and water, "
    "jade and olive green for foliage, warm ochre and sepia for earth and wood, off-white and pale blue "
    "for cloth, and a single restrained accent of vermilion or ember orange for fire and lamps. "
    "Never bright, never saturated, never a full-colour painting. "
    "NOT folk art, NOT flat cartoon, NOT comic-book linework. "
)
# Chân dung người là chỗ dễ hỏng nhất: nét gãy làm mặt méo, áo nát. Ép giải phẫu và khối.
NET_NGUOI = (
    "Render the figure with correct, realistic human anatomy and a convincing sense of volume: one "
    "well-formed face with readable eyes, nose and mouth, modelled cheekbones and jaw, and clothing "
    "painted as large smooth folds with real weight and drape. Do not fragment the face or the "
    "garments into loose patches, dots or scattered marks. "
)
# Ảnh GIAO DIỆN (nền, khung, viền, nút, ấn son, đường kẻ) là ngoại lệ: chúng phải giữ cạnh
# sắc, tô phẳng, ruột trống — nếu làm mềm thì chữ trong game khó đọc.
STYLE_UI = (
    "Traditional East Asian ink work on smooth handmade mulberry (dó) paper, treated as a flat "
    "graphic interface element: monochrome black ink with subtle warm cream and pale sepia paper "
    "tones, minimal and elegant ancient Chinese hanging-scroll aesthetic, muted and calm. "
)
NET_UI = (
    "Draw the shapes as clean, even, straight-edged hand-painted ink strokes with smooth solid "
    "stroke ends, flat even ink coverage and crisp well-defined edges, with no bleeding halo and "
    "no speckle, so that text placed on top stays fully legible. "
)
NO_TEXT = (
    "IMPORTANT: absolutely no text, no letters, no numbers, no calligraphy, no signature, "
    "no watermark, no logo, no UI labels."
)
STYLE = STYLE_GOC + NET_MEM + NO_TEXT
STYLE_MAU = MAU_GOC + NET_MEM + NO_TEXT
# Ấn son là ngoại lệ: chữ trong dấu là nội dung chính, không được cấm chữ.
STYLE_CHU = STYLE_UI + NET_UI + (
    "IMPORTANT: the ONLY text allowed is the words inside the seal; "
    "no other letters, numbers, signature, watermark, logo or UI labels."
)

# Ảnh truyện/nhân vật → tô màu điểm (彩墨). Ảnh giao diện (nền, khung, nút) giữ mực đen
# để chữ trong game luôn dễ đọc.
MAU_KEYS = [
    "bc_cho_01", "bc_tan_xa_dem", "vt_ngoc_cot", "nv_tuyet_co",
    "bc_duong_mon_nui", "bc_mieu_hoang", "vt_kiem_hap", "nv_kiem_linh",
    "bc_tran_lua", "bc_tan_hoang", "nv_han_lap", "bc_binh_minh",
]

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
        "and one or two soft even washes at the margins. "
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
        "The border is a clean hand-painted black ink rectangle with straight, even edges and "
        "smooth solid stroke ends, and a thin second inner line. "
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
        "A clean hand-painted black ink border with gently rounded corners and a smooth even stroke, "
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
        "The ring is painted with bold black ink brush strokes, smooth and unbroken all the way round. "
        "The inside of the circle and everything outside it is completely empty light paper. "
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
        "Drawn as a simple hand-painted black ink rounded rectangle with a thin smooth border and even edges. "
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
        "A square vermilion-red stamped mark with slightly uneven edges like a real ink seal impression, "
        "faded a little, authentic antique look. "
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
        "A simple black ink brush stroke that starts thin, swells smoothly in the middle and tapers to a clean point. "
        "On a plain empty light paper background. "
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
        "a few distant figures in simple cloth robes, each modelled with soft shaded volume and a readable posture. "
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
        "black smoke rolling up into the dark sky, sparks drifting in the air. Small distant figures of "
        "fleeing townsfolk and mounted raiders, softly shaded so each posture reads clearly against the firelight. "
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
        "A few weary distant figures quietly carrying the fallen, softly shaded so each posture reads clearly. "
        "Pale cold dawn light, low mist over the ruins, the sky almost empty and grey. "
        "Composition keeps the center low and calm so game text can sit above. "
        "Desolate, quiet, sorrowful, exhausted.",
    },
    {
        "key": "bc_mieu_hoang_nghi_dem",
        "name": "C.6b Miếu hoang — một mình trong đêm",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_mieu_hoang_nghi_dem.jpg",
        "use": "Tán tu về miếu hoang nghỉ sau trận, kiếm linh lên tiếng (d14b).",
        "prompt": STYLE + " "
        "The interior of a small ruined roadside shrine at night, just before dawn, seen from "
        "inside at seated eye level. A broken roof open to a sliver of dark sky, a rotting wooden "
        "pillar, a cracked stone altar with dust and dry leaves, thin ash drifted across the stone "
        "floor. A narrow gap in the plank wall lets cold wind through, faint mist hanging low. "
        "A sheathed long sword leans against the pillar, a short sword laid beside it. No people. "
        "Cold blue-grey moonlight, deep shadow in the corners, restrained ink-wash tones. "
        "Composition keeps the upper part dark and calm for game text. "
        "Lonely, cold, exhausted, quiet.",
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
    # ── Nhánh MÔN PHÁI: ảnh riêng, không dùng chung với nhánh tán tu ──
    {
        "key": "bc_quan_nuoc",
        "name": "Quán nước đầu trấn — dò tin",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_quan_nuoc.jpg",
        "use": "Quán nước đầu trấn nơi khách giang hồ tụ tập, nghe ngóng tin Dã Lang Bang (p05).",
        "prompt": STYLE_MAU + " "
        "A humble wayside tea stall at the edge of an ancient Chinese mountain town, seen at eye level. "
        "A low thatched awning on rough wooden posts, a few worn benches and low tables, a steaming "
        "iron kettle on a clay stove, rows of coarse ceramic bowls. A handful of travelling men in "
        "plain robes sitting close together and talking in low voices, each drawn with clean continuous "
        "strokes; no faces in detail. Late-afternoon light, thin smoke from the stove, dust in the air. "
        "Composition leaves the upper third and one side calm and empty for game text. "
        "Quiet, watchful, a place where rumours change hands.",
    },
    {
        "key": "bc_mon_phai_tan_hoang",
        "name": "Thất Huyền Môn — sau trận, Mạc Đại Phu cứu người",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_mon_phai_tan_hoang.jpg",
        "use": "Thất Huyền Môn tổn thất nặng sau trận; Mạc Đại Phu xách hòm thuốc cứu chữa (p16).",
        "prompt": STYLE_MAU + " "
        "The aftermath of a battle inside an ancient Chinese martial sect at first grey dawn, seen from "
        "the ruined training courtyard. A broken stone gate and a collapsed wall, splintered wooden "
        "weapon racks and fallen practice poles, torn blue banners lying in the dust, thin smoke still "
        "curling from a burnt storehouse. An old physician in a plain long robe bends over the wounded, "
        "a wooden medicine box open at his feet; a few weary disciples sit or kneel nearby, suggested "
        "outlines and simple readable faces. Pale cold dawn light, low mist, ash on the "
        "ground. Composition keeps the center low and calm so game text can sit above. "
        "Solemn, exhausted, stubbornly unbroken.",
    },
    {
        "key": "bc_binh_minh_ngoc_cot",
        "name": "Bình minh — ngọc cốt trong vạt áo",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_binh_minh_ngoc_cot.jpg",
        "use": "Bình minh đầu tiên sau đêm đầu; khối ngọc cốt khẽ ấm trong vạt áo — kết chương (p19).",
        "prompt": STYLE_MAU + " "
        "First dawn light over the quiet back hill of an ancient Chinese martial sect, seen at eye "
        "level. Soft warm sunrise glow spreading across the sky, long pale rays through low mist, the "
        "distant roofs of the sect and mountain ridges fading into gentle haze. In the foreground, the "
        "shadowed figure of a young disciple seen from behind and to one side, worn robe torn at the "
        "hem, one hand pressed lightly to the chest where a faint warm jade-coloured glow seeps through "
        "the cloth — a small jade-bone relic hidden in the robe. Face not visible. A worn stone path "
        "and a thin bare tree by the way. Composition keeps the upper third soft and empty for game "
        "text. Quiet, guarded hope, a secret carried into the morning.",
    },
    {
        "key": "nv_chinh_mau",
        "name": "MẪU Nhân vật chính",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_chinh_mau.jpg",
        "nhom": "mau",
        "use": "Ảnh MẪU tham chiếu — đính kèm khi vẽ ảnh cảnh để giữ nhân vật nhất quán.",
        "prompt": STYLE_MAU + " " + "Character reference sheet for a game: one single figure, full body, front view, neutral standing pose, centred on plain bare paper. No scenery, no props, no other objects. Clear, simple, consistent design reference with generous empty space around. " + "A poor young male drifter of an ancient Chinese fantasy world, about 16-17 years old. Thin, slightly underfed build. Short messy black hair tied back with a rough cord. Sun-tanned skin, sharp cheekbones, dark watchful eyes with a quiet modern alertness. Wearing coarse patched frayed grey-brown hemp clothes too large for him, sleeves rolled up, a rope belt. Calloused hands with dark-rimmed nails. Guarded, calculating expression. No jewellery, no ornaments.",
    },

    {
        "key": "nv_mac_dai_phu_mau",
        "name": "MẪU Mạc Đại Phu",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_mac_dai_phu_mau.jpg",
        "nhom": "mau",
        "use": "Ảnh MẪU tham chiếu — đính kèm khi vẽ ảnh cảnh để giữ nhân vật nhất quán.",
        "prompt": STYLE_MAU + " " + "Character reference sheet for a game: one single figure, full body, front view, neutral standing pose, centred on plain bare paper. No scenery, no props, no other objects. Clear, simple, consistent design reference with generous empty space around. " + "An old herbalist man of an ancient Chinese martial sect. Wiry and upright, grey hair and a short grey beard. Wearing a plain grey-brown robe like a village doctor. Rough steady hands, movements slow but precise. Aged yet strangely bright, piercing eyes. Carries bundles of dried herbs and a medicine bag. Calm, inscrutable expression.",
    },

    {
        "key": "nv_do_tam_mau",
        "name": "MẪU Đỗ Tam",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_do_tam_mau.jpg",
        "nhom": "mau",
        "use": "Ảnh MẪU tham chiếu — đính kèm khi vẽ ảnh cảnh để giữ nhân vật nhất quán.",
        "prompt": STYLE_MAU + " " + "Character reference sheet for a game: one single figure, full body, front view, neutral standing pose, centred on plain bare paper. No scenery, no props, no other objects. Clear, simple, consistent design reference with generous empty space around. " + "A burly, muscular rogue cultivator and bandit of an ancient Chinese fantasy world. Heavy build, a long scar running diagonally across his left eye, thick stubble, harsh weathered face. Wearing rough dark leather-and-cloth traveller's garb. Carrying a heavy chipped broad saber. Brutish, greedy, contemptuous expression.",
    },

    {
        "key": "nv_hung_ba_mau",
        "name": "MẪU Hùng Bá",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_hung_ba_mau.jpg",
        "nhom": "mau",
        "use": "Ảnh MẪU tham chiếu — đính kèm khi vẽ ảnh cảnh để giữ nhân vật nhất quán.",
        "prompt": STYLE_MAU + " " + "Character reference sheet for a game: one single figure, full body, front view, neutral standing pose, centred on plain bare paper. No scenery, no props, no other objects. Clear, simple, consistent design reference with generous empty space around. " + "A bandit leader of an ancient Chinese fantasy world. Tall, broad-shouldered, heavy-set. Fierce face with a thick beard and hard eyes. Wearing dark bandit armour over rough cloth, with a wolf-pelt mantle over one shoulder. Carrying a heavy blade. Arrogant, cruel expression.",
    },

    {
        "key": "bc_cho_02",
        "name": "D.2 Ngõ nhỏ sau chợ — lời đồn",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_cho_02.jpg",
        "nhom": "dot1",
        "use": "Ngõ nhỏ sau chợ — đám ăn mày quanh đống lửa, nghe lời đồn Dã Lang Bang (d02).",
        "prompt": STYLE_MAU + " " + "A narrow back alley behind an ancient Chinese market town at dusk, seen from inside the alley. A small fire burning in a broken clay brazier, ragged beggars huddled around it in silhouette, bundles of straw and cast-off baskets along the walls, laundry strung overhead. Warm firelight against cool blue twilight shadow. Composition keeps the center low and calm so game text can sit above. Wary, hushed, conspiratorial.",
    },

    {
        "key": "bc_cho_03",
        "name": "D.2b Góc chợ — một ngày mòn mỏi",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_cho_03.jpg",
        "nhom": "dot1",
        "use": "Góc chợ — ngày dài xin ăn, mòn mỏi (d02b).",
        "prompt": STYLE_MAU + " " + "A forgotten corner of an ancient Chinese market town in the harsh afternoon, seen at eye level. Empty wooden stalls shuttered and bare, scattered straw and broken baskets on the swept ground, a single thin stray dog lying in the shadow of a wall. Long lonely shadows, dusty pale light, no people. Composition keeps the upper part quiet and empty for game text. Weary, bleak, solitary.",
    },

    {
        "key": "bc_mieu_trong",
        "name": "D.4b Trong miếu — xác người còn ấm",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_mieu_trong.jpg",
        "nhom": "dot1",
        "use": "Trong miếu — phát hiện xác người mới chết còn ấm (d04b).",
        "prompt": STYLE_MAU + " " + "The interior of a small abandoned wayside shrine in the mountains at night, seen from inside. Broken timber walls, torn paper offerings, dust and old bones. On the floor beside ancient dry bones lies a freshly dead man in coarse cloth, one hand still gripping a dagger, a dark wound at his throat. A cold shaft of moonlight falls across the floor. Composition keeps the center low and calm so game text can sit above. Grim, hushed, ominous.",
    },

    {
        "key": "nv_do_tam_mieu",
        "name": "D.4c Đỗ Tam — kẻ tranh giành",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_do_tam_mieu.jpg",
        "nhom": "dot1",
        "use": "Đỗ Tam chặn cửa miếu, đòi tranh hộp kiếm (d04c).",
        "prompt": STYLE_MAU + " " + "A burly scarred rogue cultivator blocking the doorway of a ruined mountain shrine at night, seen from inside at eye level. A heavy-set man with a long scar across his left eye, thick stubble, rough dark leather-and-cloth garb, gripping a chipped broad saber. Behind him the dark mountain night; before him the dim shrine interior. Composition keeps the upper area quiet for game text. Threatening, brutish, greedy.",
    },

    {
        "key": "bc_doat_hop",
        "name": "D.4d Đoạt hộp — Đỗ Tam phản phệ",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_doat_hop.jpg",
        "nhom": "dot1",
        "use": "Đoạt hộp kiếm — Đỗ Tam chém trúng vai, phản phệ (d04d).",
        "prompt": STYLE_MAU + " " + "A violent struggle inside a ruined mountain shrine at night, seen at eye level. Two blurred figures grapple over a long dark wooden box — one young and ragged, one burly and scarred. A broad saber mid-swing, cloth torn, blood spattering. Overturned dust and straw, cold moonlight through the broken roof. Composition keeps the upper part dark and quiet for game text. Desperate, chaotic, brutal.",
    },

    {
        "key": "bc_tu_khiem",
        "name": "D.9 Tu luyện kiếm đạo — đêm đầu",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tu_khiem.jpg",
        "nhom": "dot1",
        "use": "Tu luyện kiếm đạo đêm đầu — dẫn khí vào lưỡi kiếm (d09).",
        "prompt": STYLE_MAU + " " + "Inside a ruined mountain shrine at night: a ragged young man sits cross-legged on the floor in meditation, a slender sword lying across his knees, faint cold light gathering along the blade. A ghostly white-robed sword spirit stands watching him in the shadow. Dust motes drifting in a cold moonbeam. Composition keeps the center low and calm so game text can sit above. Focused, still, austere.",
    },

    {
        "key": "bc_dot_pha",
        "name": "D.10 Đột phá Luyện Khí",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_dot_pha.jpg",
        "nhom": "dot1",
        "use": "Đột phá Luyện Khí tầng một — kiếm khí chảy trong kinh mạch (d10).",
        "prompt": STYLE_MAU + " " + "Inside a ruined mountain shrine at dawn: a ragged young man sits in meditation, faint pale light and thin swirling mist rising around him as if from within, a slender sword resting before him on the floor. The first grey light seeps through the broken roof. Composition keeps the center low and calm so game text can sit above. Quiet breakthrough, solemn, uplifted.",
    },

    {
        "key": "vt_kiem_hap_nhan",
        "name": "D.8 Nhận chủ — máu nhỏ lên kiếm",
        "ratio": "3:4 dọc (900×1200)",
        "file": "vt_kiem_hap_nhan.jpg",
        "nhom": "dot1",
        "use": "Nhận chủ — kiếm linh rạch tay, máu nhỏ lên hai thanh kiếm (d08).",
        "prompt": STYLE_MAU + " " + "Close still-life inside a ruined shrine at night: an open long dark wooden sword box on the floor, a slender sword raised just above it, a thin line of blood running down the blade and soaking in, the metal glowing faintly. A few wisps of pale mist. Cold moonlight from one side. Composition centred and calm with empty space for game text. Solemn, binding, mysterious.",
    },

    {
        "key": "nv_kiem_linh_thu",
        "name": "D.6b Kiếm linh — thử thách",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_kiem_linh_thu.jpg",
        "nhom": "dot1",
        "use": "Kiếm linh thử thách — kiếm lơ lửng trước mặt (d06b).",
        "prompt": STYLE_MAU + " " + "A ghostly young male sword spirit in plain flowing white robes, upper body, facing the viewer at a slight angle inside a ruined shrine at night. Cold composed face, sharp bright eyes, pale and half-translucent, edges fading to mist. A single slender sword floats upright before him, tip pointed down, held by no hand. Background left almost empty with soft ink wash for game text. Cold, testing, dignified.",
    },

    {
        "key": "nv_kiem_linh_than",
        "name": "D.7 Kiếm linh giới thiệu thân phận",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_kiem_linh_than.jpg",
        "nhom": "dot1",
        "use": "Kiếm linh kể thân phận — Hồng Trần Kiếm, kiếm tu ngã xuống ngàn năm trước (d07).",
        "prompt": STYLE_MAU + " " + "A ghostly young male sword spirit in plain flowing white robes, upper body, turned slightly aside, speaking inside a ruined shrine at night. Cold composed face, sharp bright eyes, form shimmering faintly and fading to mist at the edges. Behind him, half in shadow, a long dark sword box rests open. Background left almost empty with soft ink wash for game text. Grave, ancient, austere.",
    },

    {
        "key": "nv_kiem_linh_dieu",
        "name": "D.7b Điều kiện nhận chủ",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_kiem_linh_dieu.jpg",
        "nhom": "dot1",
        "use": "Kiếm linh ra điều kiện — phải lăn lộn giữa hồng trần (d07b).",
        "prompt": STYLE_MAU + " " + "A ghostly young male sword spirit in plain flowing white robes, upper body, facing the viewer steadily inside a ruined shrine at night, one hand lifted as if stating a condition. Cold composed face, sharp bright eyes, pale half-translucent form fading to mist at the edges. Background left almost empty with soft ink wash for game text. Stern, solemn, uncompromising.",
    },

    {
        "key": "bc_tran_lua_2",
        "name": "D.12 Xuống trấn — cứu dân",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tran_lua_2.jpg",
        "nhom": "dot1",
        "use": "Xuống trấn cứu dân — lần đầu giết người (d12).",
        "prompt": STYLE_MAU + " " + "An ancient Chinese market town ablaze at night, seen at eye level from a street in chaos. Wooden houses burning, thick black smoke rolling up, townsfolk fleeing, mounted raiders with blades cutting through the crowd. In the foreground a ragged youth lunges forward with a drawn sword toward a raider seizing a child. Restrained ink-wash tones with a single ember-orange accent for the fire. Composition keeps the upper part smoky and calm for game text. Desperate, chaotic, tragic.",
    },

    {
        "key": "bc_tran_lua_3",
        "name": "D.13 Thất Huyền Môn — cổng vỡ",
        "ratio": "3:4 dọc (900×1200)",
        "file": "bc_tran_lua_3.jpg",
        "nhom": "dot1",
        "use": "Thất Huyền Môn cổng vỡ — đệ tử ngã la liệt (d13).",
        "prompt": STYLE_MAU + " " + "The broken gate of an ancient Chinese martial sect at night during a raid, seen from outside at eye level. The gate smashed open, fallen disciples in blue robes strewn across the ground, raiders pushing through thick smoke, flames at the edges of the frame. A ragged youth with a drawn sword stands among the fallen, mid-guard. Restrained ink-wash tones with a single ember-orange accent for fire. Composition keeps the upper part smoky and calm for game text. Tragic, chaotic, defiant.",
    },

    {
        "key": "nv_han_lap_2",
        "name": "D.16 Đối thoại với Hàn Lập",
        "ratio": "3:4 dọc (900×1200)",
        "file": "nv_han_lap_2.jpg",
        "nhom": "dot1",
        "use": "Đối thoại với Hàn Lập sau trận — hắn đã ghi nhớ ta (d16).",
        "prompt": STYLE_MAU + " " + "Portrait of a lean, ordinary-looking young man of an ancient Chinese fantasy world, upper body, facing the viewer at a slight angle, at night on a hillside. A thin plain-featured youth in coarse undyed cloth robes, simple cloth belt, black hair in a plain topknot, no ornament. His eyes are calm, deep and sharp as a knife, watchful and unreadable. He is quietly wiping blood from his sleeve, as if the matter is settled. Background left almost empty with soft ink wash so game text can sit beside. Plain, quiet, quietly formidable.",
    },
]

# Nhánh môn phái: mỗi đoạn một cảnh riêng (xem tools/xuong_monphai.py).
import importlib.util as _ilu
_mp_spec = _ilu.spec_from_file_location(
    "xuong_monphai", os.path.join(ROOT, "tools", "xuong_monphai.py"))
MP = _ilu.module_from_spec(_mp_spec)
_mp_spec.loader.exec_module(MP)
ASSETS.extend(MP.assets(STYLE_MAU))

# Ảnh GIAO DIỆN phải giữ cạnh sắc, tô phẳng, ruột trống cho chữ — không dùng khối hội họa
# viền mềm. Tách sang STYLE_UI ngay sau khi dựng danh sách.
UI_KEYS = ["bg-main", "panel-character", "panel-story", "avatar-ring", "btn-choice", "divider-ink"]
for _a in ASSETS:
    if _a["key"] in UI_KEYS and _a["prompt"].startswith(STYLE):
        _a["prompt"] = STYLE_UI + NET_UI + NO_TEXT + _a["prompt"][len(STYLE):]

# Ảnh truyện/nhân vật dùng bản tô màu điểm (彩墨) thay cho mực đen thuần.
for _a in ASSETS:
    if _a["key"] in MAU_KEYS and _a["prompt"].startswith(STYLE):
        _a["prompt"] = STYLE_MAU + _a["prompt"][len(STYLE):]

# Ảnh cảnh lẻ còn sót khối mực đen (lẫn trong bộ điểm màu) → đổi cho đồng bộ.
for _a in ASSETS:
    if _a["key"].startswith(("bc_", "nv_", "vt_")) and _a["prompt"].startswith(STYLE):
        _a["prompt"] = STYLE_MAU + _a["prompt"][len(STYLE):]

# Prompt có người (chân dung hoặc cảnh đông người) phải nhận thêm ràng buộc giải phẫu,
# vì nét gãy làm mặt méo và nếp áo nát — lỗi người dùng thấy rõ nhất. Chỉ áp cho ảnh
# truyện/nhân vật; ảnh giao diện (khung, nút, nền) không có người nên không cần.
# Số nhiều cũng phải khớp: cảnh đông người ghi "figures"/"disciples" mà regex cũ chỉ
# có dạng số ít, nên ba cảnh đông người bị bỏ sót khối giải phẫu.
_NGUOI = re.compile(r"\b(portrait of|character reference|young man|young woman|figures?|disciples?|"
                    r"cultivators?|men|women|youths?|beggars?|townsfolk|raiders?|faces?)\b", re.I)
for _a in ASSETS:
    if not _a["key"].startswith(("nv_", "bc_", "vt_")):
        continue
    if _NGUOI.search(_a["prompt"]) and NET_NGUOI not in _a["prompt"]:
        _a["prompt"] = _a["prompt"].replace(NO_TEXT, NET_NGUOI + NO_TEXT, 1)


def load_env():
    """Đọc khoá: ưu tiên biến môi trường (dùng trong GitHub Actions), rồi tới .env."""
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                env[k] = v
    for k in FIELDS:
        if os.environ.get(k):
            env[k] = os.environ[k]
    # Action đặt tên GEMINI_KEY → dùng như geminikey.
    if os.environ.get("GEMINI_KEY") and not env.get("geminikey"):
        env["geminikey"] = os.environ["GEMINI_KEY"]
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
    repo = "huuducbkb/game-hong-duc-lam"
    blocks = []
    for a in ASSETS:
        got = ""
        for fn, size in list_files(UI_DIR) + list_files(SCENE_DIR):
            if fn == a["file"]:
                got = f'<span class="got">✔ đã nhận ({size//1024} KB)</span>'
        thu_muc = f"https://github.com/{repo}/upload/main/xuong-inbox/{a['key']}"
        blocks.append(f"""
<div class="card">
  <div class="head"><b>{a['name']}</b> <span class="ratio">{a['ratio']}</span> {got}</div>
  <div class="use">{a['use']} &nbsp;·&nbsp; tên file khi lưu: <code>{a['file']}</code></div>
  <textarea readonly rows="6" onclick="this.select()">{a['prompt']}</textarea>
  <button class="cp" onclick="cp(this)">📋 Copy prompt</button>
  <label class="up-o">📤 Up ảnh cho đúng ô này (tự lưu + ghép vào game)
    <input type="file" accept="image/*" onchange="upMotO('{a['key']}', this)">
  </label>
  <a class="up-tm" href="{thu_muc}" target="_blank"
     title="Mở GitHub đã trỏ sẵn vào xuong-inbox/{a['key']}/ — kéo ảnh vào rồi bấm Commit changes">📁 Up thẳng vào thư mục <code>xuong-inbox/{a['key']}/</code></a>
  <div class="muted" id="o-{a['key']}"></div>
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


def khoi_style(p: str) -> str:
    """Khối phong cách nền của một prompt.

    Không so khớp cả `STYLE_MAU`: `NET_NGUOI` được chèn ngay trước `NO_TEXT`, nên
    prompt có người không còn khớp nguyên chuỗi và sẽ bị nhận nhầm là mực đen.
    """
    if p.startswith(STYLE_UI):
        return "ui"
    if p.startswith(MAU_GOC):
        return "mau"
    if p.startswith(STYLE_GOC):
        return "goc"
    return "khac"


def _prompt_than(a: dict) -> str:
    """Bỏ phần phong cách chung, chỉ giữ mô tả riêng của asset."""
    p = a.get("prompt", "")
    for phan in (STYLE_UI + NET_UI + NO_TEXT, MAU_GOC, STYLE_GOC, NET_MEM, NET_UI,
                 NET_NGUOI, NO_TEXT):
        if p.startswith(phan):
            p = p[len(phan):]
    return p.strip()


# 8 ảnh nhánh tán tu (Chương 1) — để tạo prompt gộp riêng
TAN_TU_KEYS = [
    "bc_duong_mon_nui", "bc_mieu_hoang", "vt_kiem_hap", "nv_kiem_linh",
    "bc_tran_lua", "bc_tan_hoang", "nv_han_lap", "bc_binh_minh",
]
# 4 ảnh truyện cũ (B.1–B.4) — đã có file, cần vẽ lại cho khớp phong cách điểm màu
CU_KEYS = ["bc_cho_01", "bc_tan_xa_dem", "vt_ngoc_cot", "nv_tuyet_co"]

# Tên tiếng Việt của ảnh mẫu — để ghi vào hướng dẫn "đính kèm ảnh mẫu nào".
ANH_MAU_TEN = {
    "nv_chinh_mau": "Nhân vật chính",
    "nv_do_tam_mau": "Đỗ Tam",
    "nv_hung_ba_mau": "Hùng Bá",
    "nv_mac_dai_phu_mau": "Mạc Đại Phu",
    "nv_tuyet_co": "Tuyết Cơ",
    "nv_han_lap": "Hàn Lập",
    "nv_kiem_linh": "Kiếm linh Hồng Trần",
    "vt_ngoc_cot": "Ngọc cốt",
    "vt_kiem_hap": "Hồng Trần Kiếm Hạp",
}

# 14 ảnh đợt 1 chia nhóm theo nhân vật/vật xuất hiện, để mỗi nhóm chỉ cần đính kèm
# đúng ảnh mẫu liên quan — nhờ vậy mặt/tóc/áo nhân vật giữ nguyên qua mọi cảnh.
NHOM_DOT1 = [
    {"ten": "Phong cảnh (không có người)",
     "keys": ["bc_cho_02", "bc_cho_03", "bc_mieu_trong"], "mau": []},
    {"ten": "Đồ vật — hộp kiếm",
     "keys": ["vt_kiem_hap_nhan"], "mau": ["vt_kiem_hap"]},
    {"ten": "Nhân vật chính",
     "keys": ["bc_dot_pha", "bc_tran_lua_2", "bc_tran_lua_3"], "mau": ["nv_chinh_mau"]},
    {"ten": "Kiếm linh Hồng Trần",
     "keys": ["nv_kiem_linh_thu", "nv_kiem_linh_than", "nv_kiem_linh_dieu"], "mau": ["nv_kiem_linh"]},
    {"ten": "Đỗ Tam (phản diện)",
     "keys": ["nv_do_tam_mieu", "bc_doat_hop"], "mau": ["nv_do_tam_mau", "nv_chinh_mau"]},
    {"ten": "Nhân vật chính + Kiếm linh",
     "keys": ["bc_tu_khiem"], "mau": ["nv_chinh_mau", "nv_kiem_linh"]},
    {"ten": "Hàn Lập",
     "keys": ["nv_han_lap_2"], "mau": ["nv_han_lap"]},
]


# Đoạn truyện mà mỗi ảnh cảnh nhắm tới. Nhận được ảnh → gán thẳng vào đoạn này.
# QUY TẮC: mỗi cảnh một ảnh riêng — không ảnh nào gánh hai đoạn.
DOAN_CUA_ANH = {
    # ─ Nhánh tán tu ─
    "bc_cho_01": ["c1_d01"],
    "bc_cho_02": ["c1_d02"],
    "bc_cho_03": ["c1_d02b"],
    "bc_duong_mon_nui": ["c1_d03"],
    "bc_mieu_hoang": ["c1_d04"],
    "bc_mieu_trong": ["c1_d04b"],
    "nv_do_tam_mieu": ["c1_d04c"],
    "bc_doat_hop": ["c1_d04d"],
    "vt_kiem_hap": ["c1_d05"],
    "nv_kiem_linh": ["c1_d06"],
    "nv_kiem_linh_thu": ["c1_d06b"],
    "nv_kiem_linh_than": ["c1_d07"],
    "nv_kiem_linh_dieu": ["c1_d07b"],
    "vt_kiem_hap_nhan": ["c1_d08"],
    "bc_tu_khiem": ["c1_d09"],
    "bc_dot_pha": ["c1_d10"],
    "bc_tran_lua": ["c1_d11"],
    "bc_tran_lua_2": ["c1_d12"],
    "bc_tran_lua_3": ["c1_d13"],
    "bc_tan_hoang": ["c1_d14"],
    "bc_mieu_hoang_nghi_dem": ["c1_d14b"],
    "nv_han_lap": ["c1_d15"],
    "nv_han_lap_2": ["c1_d16"],
    "bc_binh_minh": ["c1_d17"],
}
# ─ Nhánh môn phái: mỗi đoạn một cảnh riêng (35 cảnh mới + 6 cảnh đã có) ─
DOAN_CUA_ANH.update(MP.doan_cua_anh())

# Bố cục Xưởng: nhóm theo chương / công dụng để dễ nhìn.
NHOM_BO_CUC = [
    {"ma": "mau", "ten": "Ảnh mẫu tham chiếu", "mota": "Vẽ một lần, đính kèm khi vẽ ảnh cảnh."},
    {"ma": "giao-dien", "ten": "Giao diện", "mota": "Nền, khung, nút, ấn son."},
    {"ma": "c1-tan-tu", "ten": "Chương 1 — nhánh tán tu", "mota": "Chợ, miếu hoang, hộp kiếm, trấn cháy, Hàn Lập."},
    {"ma": "c1-mon-phai", "ten": "Chương 1 — nhánh môn phái", "mota": "Sân tập, vườn thuốc, tân xá, ngọc cốt."},
]

# key -> mã nhóm bố cục (mặc định suy theo `nhom`/tiền tố)
NHOM_CUA_ANH = {
    "bg-main": "giao-dien", "panel-character": "giao-dien", "panel-story": "giao-dien",
    "avatar-ring": "giao-dien", "btn-choice": "giao-dien", "seal": "giao-dien",
    "divider-ink": "giao-dien",
    "bc_cho_01": "c1-tan-tu", "bc_tan_xa_dem": "c1-mon-phai", "vt_ngoc_cot": "c1-mon-phai",
    "nv_tuyet_co": "c1-mon-phai", "bc_duong_mon_nui": "c1-tan-tu", "bc_mieu_hoang": "c1-tan-tu",
    "vt_kiem_hap": "c1-tan-tu", "nv_kiem_linh": "c1-tan-tu", "bc_tran_lua": "c1-tan-tu",
    "bc_tan_hoang": "c1-tan-tu", "bc_mieu_hoang_nghi_dem": "c1-tan-tu",
    "nv_han_lap": "c1-tan-tu", "bc_binh_minh": "c1-tan-tu",
    "bc_cho_02": "c1-tan-tu", "bc_cho_03": "c1-tan-tu", "bc_mieu_trong": "c1-tan-tu",
    "nv_do_tam_mieu": "c1-tan-tu", "bc_doat_hop": "c1-tan-tu", "bc_tu_khiem": "c1-tan-tu",
    "bc_dot_pha": "c1-tan-tu", "vt_kiem_hap_nhan": "c1-tan-tu",
    "nv_kiem_linh_thu": "c1-tan-tu", "nv_kiem_linh_than": "c1-tan-tu",
    "nv_kiem_linh_dieu": "c1-tan-tu", "bc_tran_lua_2": "c1-tan-tu",
    "bc_tran_lua_3": "c1-tan-tu", "nv_han_lap_2": "c1-tan-tu",
}


# ── Bố cục Xưởng ────────────────────────────────────────────────────────────
# Ba PHẦN lớn: dùng chung → nhánh tán tu → nhánh môn phái. Trong mỗi phần là
# các NHÓM CẢNH (cảnh liên tiếp trong truyện), mỗi nhóm có prompt gộp riêng.
XUONG_PHAN = [
    {"ma": "chung", "icon": "🧰", "ten": "Dùng chung",
     "mota": "Ảnh mẫu và giao diện — vẽ một lần, dùng cho cả hai nhánh."},
    {"ma": "c1-tan-tu", "icon": "🍂", "ten": "Chương 1 · Nhánh Tán tu",
     "mota": "Chợ sớm, miếu hoang, hộp kiếm, kiếm linh, trấn cháy, Hàn Lập."},
    {"ma": "c1-mon-phai", "icon": "⛩️", "ten": "Chương 1 · Nhánh Môn phái",
     "mota": "Tân xá đêm, ngọc cốt, Tuyết Cơ."},
]

# Nhóm cảnh theo thứ tự truyện. `keys` = ảnh của nhóm; `mau` = ảnh mẫu cần
# đính kèm khi vẽ (giữ mặt/tóc/áo nhân vật y hệt). Ảnh mẫu nằm riêng ở
# THU_VIEN_THU_TU (thư viện), không đánh số trùng ở đây.
NHOM_CANH = [
    # ─ Dùng chung ─
    {"ma": "giao-dien", "phan": "chung", "ten": "Giao diện game",
     "mota": "Nền, khung, nút, ấn son — khung chứa toàn bộ game.",
     "keys": ["bg-main", "panel-character", "panel-story", "avatar-ring",
              "btn-choice", "seal", "divider-ink"],
     "mau": []},
    # ─ Nhánh tán tu ─
    {"ma": "d-cho", "phan": "c1-tan-tu", "ten": "Chợ sớm Thất Huyền",
     "mota": "Chợ sớm, ngõ nhỏ sau chợ.", "keys": ["bc_cho_01", "bc_cho_02", "bc_cho_03"],
     "mau": []},
    {"ma": "d-duong", "phan": "c1-tan-tu", "ten": "Đường mòn lên núi",
     "mota": "Đường mòn lên núi — chạng vạng.", "keys": ["bc_duong_mon_nui"],
     "mau": []},
    {"ma": "d-mieu", "phan": "c1-tan-tu", "ten": "Miếu hoang — Đỗ Tam",
     "mota": "Miếu hoang sau núi, xác người, Đỗ Tam tranh giành.",
     "keys": ["bc_mieu_hoang", "bc_mieu_trong", "nv_do_tam_mieu", "bc_doat_hop"],
     "mau": ["nv_do_tam_mau", "nv_chinh_mau"]},
    {"ma": "d-hop", "phan": "c1-tan-tu", "ten": "Hồng Trần Kiếm Hạp",
     "mota": "Hộp kiếm — vật phẩm cơ duyên.", "keys": ["vt_kiem_hap"],
     "mau": []},
    {"ma": "d-kiemlinh-1", "phan": "c1-tan-tu", "ten": "Kiếm linh — thử thách",
     "mota": "Kiếm linh hiện ra, thử thách người chơi.",
     "keys": ["nv_kiem_linh", "nv_kiem_linh_thu"], "mau": ["nv_kiem_linh"]},
    {"ma": "d-kiemlinh-2", "phan": "c1-tan-tu", "ten": "Kiếm linh — thân phận & điều kiện",
     "mota": "Kiếm linh giới thiệu thân phận, nêu điều kiện nhận chủ.",
     "keys": ["nv_kiem_linh_than", "nv_kiem_linh_dieu"], "mau": ["nv_kiem_linh"]},
    {"ma": "d-nhan-chu", "phan": "c1-tan-tu", "ten": "Nhận chủ — máu nhỏ lên kiếm",
     "mota": "Máu nhỏ lên kiếm hạp, kiếm nhận chủ.",
     "keys": ["vt_kiem_hap_nhan"], "mau": ["vt_kiem_hap", "nv_chinh_mau"]},
    {"ma": "d-tu-khiem", "phan": "c1-tan-tu", "ten": "Tu luyện kiếm đạo",
     "mota": "Đêm đầu tu luyện kiếm đạo.",
     "keys": ["bc_tu_khiem"], "mau": ["nv_chinh_mau", "nv_kiem_linh"]},
    {"ma": "d-dot-pha", "phan": "c1-tan-tu", "ten": "Đột phá Luyện Khí",
     "mota": "Đột phá cảnh giới Luyện Khí.", "keys": ["bc_dot_pha"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "d-tran-lua", "phan": "c1-tan-tu", "ten": "Trấn cháy — cứu dân",
     "mota": "Thất Huyền trấn chìm trong lửa, cứu dân, cổng môn vỡ.",
     "keys": ["bc_tran_lua", "bc_tran_lua_2", "bc_tran_lua_3", "bc_tan_hoang",
               "bc_mieu_hoang_nghi_dem"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "d-han-lap", "phan": "c1-tan-tu", "ten": "Hàn Lập",
     "mota": "Chạm mặt Hàn Lập, đối thoại.",
     "keys": ["nv_han_lap", "nv_han_lap_2"], "mau": ["nv_han_lap"]},
    {"ma": "d-ket", "phan": "c1-tan-tu", "ten": "Kết chương — bình minh",
     "mota": "Bình minh đầu tiên rọi lên vai áo rách.",
     "keys": ["bc_binh_minh"], "mau": []},
] + MP.NHOM_CANH

# key -> mã nhóm cảnh (suy từ NHOM_CANH)
NHOM_CANH_CUA = {k: n["ma"] for n in NHOM_CANH for k in n["keys"]}
# key -> mã phần (suy từ NHOM_CANH)
PHAN_CUA = {k: n["phan"] for n in NHOM_CANH for k in n["keys"]}


def nhom_canh_cua(key: str) -> str:
    return NHOM_CANH_CUA.get(key, "")


def phan_cua(key: str) -> str:
    return PHAN_CUA.get(key, "")


def nhom_canh(ma: str) -> dict:
    return next((n for n in NHOM_CANH if n["ma"] == ma), {})


def so_hien_thi() -> dict:
    """key -> nhãn số hiển thị, đánh số tuần tự trong từng phần (C.x, D.x, P.x)."""
    tien_to = {"chung": "C", "c1-tan-tu": "D", "c1-mon-phai": "P"}
    dem, kq = {}, {}
    for n in NHOM_CANH:
        for k in n["keys"]:
            dem[n["phan"]] = dem.get(n["phan"], 0) + 1
            kq[k] = f"{tien_to.get(n['phan'], 'X')}.{dem[n['phan']]}"
    return kq


def build_gop_prompt_canh(nhom: dict) -> str:
    """Prompt gộp MỘT nhóm cảnh — dán 1 lần vào AI là nó vẽ lần lượt cả nhóm."""
    theo_key = {a["key"]: a for a in ASSETS}
    ds = [theo_key[k] for k in nhom["keys"] if k in theo_key]
    if not ds:
        return ""
    return _build_gop(ds, f'nhóm cảnh "{nhom["ten"]}"', mau=nhom.get("mau") or [])


def build_gop_prompt_phan(ma_phan: str) -> str:
    """Prompt gộp CẢ một phần (dùng chung / tán tu / môn phái)."""
    theo_key = {a["key"]: a for a in ASSETS}
    ds_nhom = [n for n in NHOM_CANH if n["phan"] == ma_phan]
    keys = [k for n in ds_nhom for k in n["keys"]]
    ds = [theo_key[k] for k in keys if k in theo_key]
    # Gom ảnh mẫu mà mọi nhóm trong phần cần đính kèm (giữ mặt/tóc/áo nhân vật).
    mau = []
    for n in ds_nhom:
        for k in n.get("mau") or []:
            if k not in mau:
                mau.append(k)
    ten = next((p["ten"] for p in XUONG_PHAN if p["ma"] == ma_phan), ma_phan)
    return _build_gop(ds, f"toàn bộ phần {ten}", mau=mau)


def nhom_dot1_cua(key: str) -> dict:
    """Nhóm đợt 1 (7 nhóm cũ) chứa ảnh này — giữ để tương thích."""
    return next((n for n in NHOM_DOT1 if key in n["keys"]), {})


def nhom_cua(key: str) -> str:
    """Mã nhóm bố cục của asset."""
    if key in NHOM_CUA_ANH:
        return NHOM_CUA_ANH[key]
    for a in ASSETS:
        if a["key"] == key and a.get("nhom") == "mau":
            return "mau"
    return "giao-dien"


def doan_cua(key: str) -> list:
    return DOAN_CUA_ANH.get(key, [])


def so_thu_tu() -> dict:
    """key -> số thứ tự (1..n) theo đúng thứ tự ASSETS, để người dùng dễ đối chiếu."""
    return {a["key"]: i for i, a in enumerate(ASSETS, 1)}


def ma_anh(a: dict) -> str:
    """Khối nhận diện của một ảnh: số thứ tự + mã + vị trí dùng.

    Khối này đi kèm prompt để người dùng biết ảnh nào dùng ở đâu. Phần mô tả
    tiếng Anh cho AI vẽ KHÔNG chứa khối này (xem `prompt_gui_ai`).
    """
    so = so_thu_tu().get(a["key"], 0)
    doan = doan_cua(a["key"])
    noi = ", ".join(doan) if doan else "—"
    return (f"ẢNH #{so} — mã `{a['key']}`\n"
            f"  · Dùng ở : {noi}\n"
            f"  · Loại   : {a.get('name', '')}\n"
            f"  · Tỷ lệ  : {a.get('ratio', '')}\n"
            f"  · Lưu là : {a['file']}")


def ten_sach(a: dict) -> str:
    """Tên asset đã bỏ mã đợt cũ (vd 'D.4c Đỗ Tam' → 'Đỗ Tam') để tránh trùng số hiển thị."""
    import re
    return re.sub(r"^[A-Z]\.\d+[a-z]?\s+", "", a.get("name", "")).strip()


def prompt_gui_ai(a: dict) -> str:
    """Chỉ phần prompt để dán vào AI vẽ ảnh — KHÔNG kèm khối nhận diện.

    Khối nhận diện (`ma_anh`) chỉ để người dùng đối chiếu, không đưa vào AI
    vì prompt đã cấm chữ trong ảnh.
    """
    return a.get("prompt", "")


def _build_gop(ds: list, tieu_de: str = "", dong_dau: str = "", mau: list = None) -> str:
    """Dựng prompt gộp cho một bộ ảnh: dán 1 lần vào AI chat là nó vẽ lần lượt.

    mau: danh sách key ảnh mẫu cần đính kèm (rỗng/None = không cần).
    """
    if not dong_dau:
        so = f"{len(ds)} image" + ("" if len(ds) == 1 else "s")
        dong_dau = (f'TASK: Create {so} for a Vietnamese cultivation game named '
                    f'"Hồng Đức Tu Tiên Lộ"')
        dong_dau += f" — {tieu_de}." if tieu_de else "."
    # Ghi phong cách chung của cả bộ: điểm màu (ảnh truyện) hay cạnh sắc (ảnh giao diện).
    khoi = {khoi_style(a["prompt"]) for a in ds}
    if khoi == {"ui"}:
        phong_cach = (STYLE_UI + NET_UI).strip()
    elif "ui" in khoi:
        phong_cach = (STYLE_GOC + NET_MEM).strip()
    else:
        phong_cach = (MAU_GOC + NET_MEM).strip()
    dong = [
        dong_dau,
        "Produce the images ONE BY ONE, in the order below, each as a SEPARATE image at its "
        "own aspect ratio.",
        "If you cannot finish them all in one reply, make as many as you can and then stop; "
        'I will reply "tiếp tục" to get the next batch.',
        "",
    ]
    # Nhóm có nhân vật → nhắc đính kèm ảnh mẫu để giữ mặt/tóc/áo y hệt.
    if mau:
        ten = ", ".join(ANH_MAU_TEN.get(k, k) for k in mau)
        ref = "reference image" + ("" if len(mau) == 1 else "s")
        dong += [
            f"ATTACHED REFERENCE IMAGE(S): I am attaching {len(mau)} {ref} — {ten}.",
            "Every figure in EVERY image below must keep the SAME face, hair, clothing and colours "
            "as the attached reference(s). Only the pose, expression, camera angle, lighting and "
            "background may change. Do not redesign the character.",
            "",
        ]
    dong += [
        "SHARED ART STYLE (apply to EVERY image): " + phong_cach,
        "",
    ]
    i_seal = next((i for i, a in enumerate(ds, 1) if a["key"] == "seal"), None)
    if i_seal:
        dong.append(
            "TEXT RULE: no text, no letters, no numbers, no calligraphy, no signature, no watermark, "
            f"no logo in ANY image. The ONLY exception is image {i_seal} (the seal): inside the seal it must show "
            "the words \"HỒNG\" and \"ĐỨC\" in Latin capitals, drawn in a Chinese ink-brush (Hán) "
            "calligraphy style and stacked vertically one above the other (HỒNG on top, ĐỨC below), "
            "and nothing else."
        )
    else:
        dong.append(
            "TEXT RULE: no text, no letters, no numbers, no calligraphy, no signature, no watermark, "
            "no logo in ANY image."
        )
    dong.append("")
    # Bộ trộn nhiều phong cách → ghi rõ từng ảnh dùng khối nào.
    hoa_tron = len(khoi) > 1
    for i, a in enumerate(ds, 1):
        nhan = ""
        if hoa_tron:
            ks = khoi_style(a["prompt"])
            if ks == "ui":
                nhan = " [interface element: sharp flat edges]"
            elif ks == "mau":
                nhan = " [colour-ink 彩墨, painterly]"
            elif a["key"] != "seal":
                nhan = " [black ink only, painterly]"
        doan = doan_cua(a["key"])
        vitri = ("  · dùng ở: " + ", ".join(doan)) if doan else ""
        dong.append(f"{i}. {a['file']} — {a['ratio']} — {ten_sach(a)}{nhan}{vitri}")
        dong.append(f"   {_prompt_than(a)}")
        dong.append("")
    return "\n".join(dong)


def build_gop_prompt() -> str:
    """Một prompt gộp: dán 1 lần vào AI chat là nó vẽ lần lượt cả bộ ảnh."""
    return _build_gop(ASSETS, dong_dau=(
        'TASK: Create the full image set for a Vietnamese cultivation game named '
        '"Hồng Đức Tu Tiên Lộ".'
    ))


def build_gop_prompt_tantu() -> str:
    """Prompt gộp riêng 8 ảnh nhánh tán tu (Chương 1)."""
    ds = [a for a in ASSETS if a["key"] in TAN_TU_KEYS]
    return _build_gop(ds, "nhánh tán tu, Chương 1")


def build_gop_prompt_cu() -> str:
    """Prompt gộp riêng 4 ảnh truyện cũ (B.1–B.4), vẽ lại theo phong cách điểm màu."""
    ds = [a for a in ASSETS if a["key"] in CU_KEYS]
    return _build_gop(ds, "4 ảnh truyện cũ (Chương 1), vẽ lại theo phong cách điểm màu")


def build_gop_prompt_mau() -> str:
    """Prompt gộp 4 ảnh MẪU tham chiếu — vẽ TRƯỚC khi vẽ ảnh cảnh."""
    ds = [a for a in ASSETS if a.get("nhom") == "mau"]
    return _build_gop(ds, "4 ảnh MẪU tham chiếu — vẽ TRƯỚC, dùng đính kèm khi vẽ ảnh cảnh")


def build_gop_prompt_dot1() -> str:
    """Prompt gộp 14 ảnh đợt 1 (nhánh tán tu, Chương 1)."""
    ds = [a for a in ASSETS if a.get("nhom") == "dot1"]
    return _build_gop(ds, "đợt 1 — nhánh tán tu, Chương 1")


def build_gop_prompt_nhom(nhom: dict) -> str:
    """Prompt gộp cho MỘT nhóm ảnh đợt 1 (kèm hướng dẫn đính kèm ảnh mẫu)."""
    ds = [a for a in ASSETS if a["key"] in nhom["keys"]]
    return _build_gop(ds, f'nhóm "{nhom["ten"]}" — đợt 1, Chương 1', mau=nhom["mau"])


def build_nhom_html() -> str:
    """Lưới 7 nhóm ảnh đợt 1 — mỗi nhóm 1 nút copy, ghi rõ đính kèm ảnh mẫu nào."""
    the = []
    for i, nhom in enumerate(NHOM_DOT1, 1):
        if nhom["mau"]:
            ds_mau = ", ".join(ANH_MAU_TEN.get(k, k) for k in nhom["mau"])
            nhac = f'<b>Đính kèm:</b> <span class="mau">{ds_mau}</span>'
        else:
            nhac = '<b>Đính kèm:</b> <span class="muted">không cần</span>'
        so_anh = len(nhom["keys"])
        the.append(f"""
<div class="card nhom">
  <div class="head"><b>{i}. {nhom['ten']}</b> <span class="ratio">{so_anh} ảnh</span></div>
  <div class="use">{nhac}</div>
  <textarea readonly rows="8" id="nhom{i}" onclick="this.select()">{html_lib.escape(build_gop_prompt_nhom(nhom))}</textarea>
  <button class="cp" onclick="cpText('nhom{i}', this)">📋 Copy prompt nhóm {i}</button>
  <button class="up" onclick="taiPromptGop('nhom{i}', 'hong-duc-nhom-{i}.txt')">⬇️ Tải .txt</button>
</div>""")
    return "\n".join(the)


# Thứ tự hiển thị thư viện ảnh mẫu: nhân vật trước, đồ vật sau.
THU_VIEN_THU_TU = [
    "nv_chinh_mau", "nv_mac_dai_phu_mau", "nv_do_tam_mau", "nv_hung_ba_mau",
    "nv_tuyet_co", "nv_han_lap", "nv_kiem_linh", "vt_ngoc_cot", "vt_kiem_hap",
]


def build_thu_vien_html() -> str:
    """Lưới 9 ảnh mẫu tham chiếu — xem + tải về để đính kèm khi vẽ cảnh."""
    theo_key = {a["key"]: a for a in ASSETS}
    the = []
    for k in THU_VIEN_THU_TU:
        a = theo_key.get(k)
        if not a:
            continue
        co = os.path.isfile(f'{SCENE_DIR}/{a["file"]}')
        nhan = ANH_MAU_TEN.get(k, k)
        nhan_file = ("<span class='badge chac'>đã có</span>" if co
                     else "<span class='badge'>chưa có</span>")
        the.append(f"""
<div class="item{' thieu' if not co else ''}">
  <img src="/assets/scene/{a['file']}" alt="{nhan}" loading="lazy">
  <div class="meta">
    <b>{nhan}</b><br>
    <span class="muted" style="font-size:11px">{a['file']}</span><br>
    {nhan_file}
    <a class="up" style="display:block;text-align:center;text-decoration:none;margin-top:8px"
       href="/assets/scene/{a['file']}" download="{a['file']}">⬇️ Tải ảnh</a>
  </div>
</div>""")
    return "\n".join(the)


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
    html = html.replace("__GOP_PROMPT_TANTU__", html_lib.escape(build_gop_prompt_tantu()))
    html = html.replace("__GOP_PROMPT_CU__", html_lib.escape(build_gop_prompt_cu()))
    html = html.replace("__GOP_PROMPT_MAU__", html_lib.escape(build_gop_prompt_mau()))
    html = html.replace("__GOP_PROMPT_DOT1__", html_lib.escape(build_gop_prompt_dot1()))
    html = html.replace("__NHOM_DOT1__", build_nhom_html())
    html = html.replace("__THU_VIEN_ANH_MAU__", build_thu_vien_html())
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
 .nhom{border-left:3px solid var(--jade)}
 .mau{color:#ffd166}
 details{margin:12px 0}
 summary{cursor:pointer;font-size:13px;color:var(--jade);padding:8px 0}
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
.up-o{display:block;margin-top:8px;font-size:12.5px;color:var(--muted)}
.up-o input{width:100%;margin-top:6px;padding:9px;font-size:12.5px;border-radius:9px;
  background:#1b2540;color:var(--fg);border:1px dashed #4a628c}
.up-tm{display:block;margin-top:8px;padding:9px 12px;font-size:12.5px;text-decoration:none;
  background:#2a2338;border:1px dashed #6b5a8c;border-radius:9px;color:#d9c7ff;font-weight:600}
.up-tm:hover{background:#352c48;border-color:#a68cf0;color:#efe6ff}
.up-tm code{font-size:11.5px;color:#c9b6ff}
.item.thieu{border-color:#a05a2a}
.item.thieu .meta{background:#2a150d}
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

<h2>1️⃣ Vẽ 4 ảnh MẪU tham chiếu (làm TRƯỚC)</h2>
<div class="card">
  <p class="muted">Đây là <b>bước nền</b>: vẽ 4 ảnh mẫu nhân vật <b>một lần</b>, rồi
  <b>đính kèm</b> chúng mỗi khi vẽ ảnh cảnh — nhờ vậy nhân vật giữ <b>cùng một gương mặt</b>
  qua mọi cảnh, mọi chương. Bấm <b>Copy</b> rồi dán vào Gemini chat.</p>
  <p class="muted"><b>Lưu ý:</b> 5 nhân vật/đồ vật khác <b>đã có sẵn</b> ảnh (Tuyết Cơ, Hàn Lập,
  Kiếm linh, Ngọc cốt, Hộp kiếm) — không cần vẽ lại, dùng luôn làm ảnh mẫu.</p>
  <textarea readonly rows="10" id="gopmau" onclick="this.select()">__GOP_PROMPT_MAU__</textarea>
  <button class="cp" onclick="cpText('gopmau', this)">📋 Copy prompt 4 ảnh mẫu</button>
  <button class="up" onclick="taiPromptGop('gopmau', 'hong-duc-prompt-4-anh-mau.txt')">⬇️ Tải về file .txt</button>
</div>

<h2>📚 Thư viện ảnh mẫu — tải về để đính kèm</h2>
<div class="card">
  <p class="muted">Đây là <b>9 ảnh mẫu</b> dùng để đính kèm khi vẽ ảnh cảnh. Khi vẽ nhóm nào,
  bấm <b>⬇️ Tải ảnh</b> của ảnh mẫu mà nhóm đó ghi, rồi đính kèm vào Gemini chat cùng prompt.
  Trên iPad: bấm giữ ảnh → <b>“Lưu vào Ảnh”</b>.</p>
  <div class="grid">__THU_VIEN_ANH_MAU__</div>
</div>

<h2>2️⃣ Vẽ 14 ảnh đợt 1 — chia 7 nhóm theo nhân vật</h2>
<div class="card">
  <p class="muted">Vẽ <b>từng nhóm một</b>: bấm <b>Copy</b> → dán vào Gemini chat → <b>đính kèm
  ảnh mẫu</b> đúng như nhóm ghi → lấy ảnh. Cách này giữ <b>mặt/tóc/áo nhân vật y hệt</b>
  giữa các cảnh. Vẽ xong nhóm nào, tải ảnh lên Xưởng ngay nhóm đó.</p>
  <p class="muted">Muốn vẽ nhanh cả 14 ảnh một lần? Dùng nút <b>“Copy prompt 14 ảnh đợt 1”</b>
  ở cuối trang (nhưng khi đó AI không thấy ảnh mẫu → mặt nhân vật có thể khác nhau).</p>
</div>
__NHOM_DOT1__

<details>
<summary>Hoặc vẽ cả 14 ảnh một lần (không đính kèm ảnh mẫu)</summary>
<div class="card">
  <textarea readonly rows="10" id="gopdot1" onclick="this.select()">__GOP_PROMPT_DOT1__</textarea>
  <button class="cp" onclick="cpText('gopdot1', this)">📋 Copy prompt 14 ảnh đợt 1</button>
  <button class="up" onclick="taiPromptGop('gopdot1', 'hong-duc-prompt-14-anh-dot1.txt')">⬇️ Tải về file .txt</button>
</div>
</details>

<h2>🎨 Vẽ cả bộ bằng 1 prompt (đỡ copy từng cái)</h2>
<div class="card">
  <p class="muted">Bấm <b>Copy</b> rồi dán <b>một lần</b> vào Gemini chat — nó sẽ vẽ lần lượt
  các ảnh theo đúng tỷ lệ. Hết lượt thì nhắn <b>“tiếp tục”</b> để lấy ảnh còn lại.</p>
  <p class="muted">Ảnh truyện &amp; nhân vật vẽ <b>thủy mặc điểm màu (彩墨)</b>; ảnh giao diện
  (nền, khung, nút) giữ <b>mực đen</b> để chữ trong game dễ đọc.</p>
  <textarea readonly rows="10" id="gop" onclick="this.select()">__GOP_PROMPT__</textarea>
  <button class="cp" onclick="cpText('gop', this)">📋 Copy prompt gộp</button>
  <button class="up" onclick="taiPromptGop()">⬇️ Tải về file .txt</button>
</div>

<h2>🎨 Vẽ riêng 8 ảnh nhánh tán tu bằng 1 prompt</h2>
<div class="card">
  <p class="muted">Chỉ gồm <b>8 ảnh nhánh tán tu</b> (Chương 1): đường mòn, miếu hoang, hộp kiếm,
  kiếm linh, trấn cháy, đống đổ nát, Hàn Lập, bình minh. Vẽ theo phong cách <b>thủy mặc điểm màu
  (彩墨)</b>. Bấm <b>Copy</b> rồi dán <b>một lần</b> vào Gemini chat — hết lượt thì nhắn
  <b>“tiếp tục”</b> để lấy ảnh còn lại.</p>
  <textarea readonly rows="10" id="goptantu" onclick="this.select()">__GOP_PROMPT_TANTU__</textarea>
  <button class="cp" onclick="cpText('goptantu', this)">📋 Copy prompt gộp 8 ảnh tán tu</button>
  <button class="up" onclick="taiPromptGop('goptantu', 'hong-duc-prompt-8-anh-tan-tu.txt')">⬇️ Tải về file .txt</button>
</div>

<h2>🎨 Vẽ lại 4 ảnh truyện cũ bằng 1 prompt</h2>
<div class="card">
  <p class="muted">Gồm <b>4 ảnh truyện đã có</b> (B.1 Chợ sớm, B.2 Tân xá đêm, B.3 Ngọc cốt,
  B.4 Tuyết Cơ) — vẽ lại theo phong cách <b>thủy mặc điểm màu (彩墨)</b> cho khớp các ảnh mới.
  Ảnh mới tải lên sẽ <b>đè</b> ảnh cũ cùng tên. Bấm <b>Copy</b> rồi dán <b>một lần</b> vào
  Gemini chat — hết lượt thì nhắn <b>“tiếp tục”</b> để lấy ảnh còn lại.</p>
  <textarea readonly rows="10" id="gopcu" onclick="this.select()">__GOP_PROMPT_CU__</textarea>
  <button class="cp" onclick="cpText('gopcu', this)">📋 Copy prompt gộp 4 ảnh cũ</button>
  <button class="up" onclick="taiPromptGop('gopcu', 'hong-duc-prompt-4-anh-cu.txt')">⬇️ Tải về file .txt</button>
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
  const nhan = btn.textContent;
  const done = () => { btn.classList.add('done'); btn.textContent='✅ Đã copy';
    setTimeout(()=>{btn.classList.remove('done');btn.textContent=nhan;},1600); };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(ta.value).then(done).catch(()=>{ try{document.execCommand('copy');done();}catch(e){} });
  } else { try{document.execCommand('copy');done();}catch(e){} }
}
function taiPromptGop(id, tenFile){
  const txt = document.getElementById(id || 'gop').value;
  const blob = new Blob([txt], {type:'text/plain;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = tenFile || 'hong-duc-prompt-ve-anh.txt';
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
    <div class="item ${k.key?'':'thieu'}" id="item${i}">
      <img src="data:image/jpeg;base64,${k.data||''}" alt="">
      <div class="meta">
        <div><span class="badge ${k.tu_dong?'chac':''}">${k.tu_dong?'AI chắc':'Cần duyệt'} · ${k.do_tin_cay||0}%</span></div>
        <div class="muted" style="font-size:11px;margin-top:4px">${k.kich_thuoc||''}</div>
        <select id="sel${i}" onchange="chonPrompt(${i}, this.value)">
          <option value="">— chọn prompt —</option>
          ${DANH_SACH.map(a=>`<option value="${a.key}" ${a.key===k.key?'selected':''}>${a.name}</option>`).join('')}
        </select>
        <div class="muted" id="trangThai${i}" style="font-size:11px">${k.key?'':'⚠️ chưa chọn prompt — sẽ KHÔNG được lưu'}</div>
        <div class="muted" style="font-size:11px">${k.mo_ta?k.mo_ta:''}</div>
      </div>
    </div>`).join('');
}

async function upMotO(key, input){
  const f = input.files && input.files[0];
  if(!f) return;
  const tt = document.getElementById('o-'+key);
  if(tt) tt.innerHTML = '<span class="muted">Đang lưu…</span>';
  const data = await docB64(f);
  try{
    const r = await fetch('/luu_loat',{method:'POST',headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ds:[{key, name:f.name, data}], day:true})});
    const j = await r.json();
    if(!j.ok){ if(tt) tt.innerHTML = `<span class="warn">⚠️ ${j.error||'lỗi'}</span>`; return; }
    let t = '✅ Đã lưu';
    if(j.ghep && Object.keys(j.ghep).length) t += ' + ghép vào truyện';
    if(j.day_len === 'ok') t += ' + đẩy lên GitHub (web cập nhật ~1 phút)';
    else if(j.day_len) t += ` (${j.day_len})`;
    if(tt) tt.innerHTML = `<span class="ok">${t}</span>`;
    input.value = '';
  }catch(e){ if(tt) tt.innerHTML = `<span class="warn">⚠️ Lỗi: ${e}</span>`; }
}

function chonPrompt(i, key){
  HANG_DOI[i].key = key;
  const item = document.getElementById('item'+i);
  const tt = document.getElementById('trangThai'+i);
  if(item) item.className = 'item' + (key ? '' : ' thieu');
  if(tt) tt.innerHTML = key ? '' : '⚠️ chưa chọn prompt — sẽ KHÔNG được lưu';
}

async function luuLoat(){
  const ds = HANG_DOI.filter(k=>k.key).map(k=>({key:k.key, data:k.data}));
  const thieu = HANG_DOI.length - ds.length;
  const saveMsg = document.getElementById('saveMsg');
  if(!ds.length){ saveMsg.innerHTML='<p class="warn">Chưa chọn prompt nào — chọn prompt cho ảnh rồi bấm Lưu lại.</p>'; return; }
  if(thieu > 0 && !confirm(
      `⚠️ Còn ${thieu} ảnh CHƯA chọn prompt, sẽ KHÔNG được lưu.\n\n` +
      `Vẫn lưu ${ds.length} ảnh đã chọn?\n\n` +
      `(Bấm Hủy để quay lại chọn prompt cho ${thieu} ảnh kia.)`)) {
    saveMsg.innerHTML=`<p class="warn">Đã dừng — hãy chọn prompt cho ${thieu} ảnh còn lại rồi bấm Lưu.</p>`;
    return;
  }
  saveMsg.innerHTML='<p class="muted">Đang lưu…</p>';
  try{
    const r = await fetch('/luu_loat',{method:'POST',headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ds, day:true})});
    const j = await r.json();
    if(!j.ok){ saveMsg.innerHTML=`<p class="warn">⚠️ ${j.error||'lỗi'}</p>`; return; }
    let html = `<p class="ok">✅ Đã lưu ${j.da_luu.length} ảnh: ${j.da_luu.map(x=>x.file).join(', ')}</p>`;
    const ghep = j.ghep || {};
    const soGhep = Object.keys(ghep).length;
    if(soGhep) html += `<p class="ok">🧩 Đã ghép vào truyện: ${soGhep} ảnh → ${Object.entries(ghep).map(([f,d])=>f+' → '+d.join(', ')).join(' · ')}</p>`;
    if(j.day_len === 'ok') html += `<p class="ok">🚀 Đã đẩy lên GitHub — bản chơi trên web sẽ cập nhật sau ~1 phút.</p>`;
    else if(j.day_len) html += `<p class="muted">Đẩy lên GitHub: ${j.day_len}</p>`;
    if(thieu > 0){
      html += `<p class="warn">⚠️ Bỏ qua ${thieu} ảnh chưa chọn prompt — chọn prompt rồi bấm Lưu lại.</p>`;
    } else {
      html += `<p class="muted">Xong hết. Tải lại trang để xem danh sách "Ảnh đã nhận".</p>`;
    }
    saveMsg.innerHTML = html;
    // Ảnh đã lưu xong thì bỏ khỏi hàng đợi, tránh lưu trùng khi bấm Lưu lần nữa.
    HANG_DOI = HANG_DOI.filter(k=>!k.key);
    if(!HANG_DOI.length){
      document.getElementById('review').style.display='none';
      document.getElementById('grid').innerHTML='';
    } else {
      hienDuyet(HANG_DOI.map(k=>k), HANG_DOI.map(k=>({data:k.data})));
    }
  }catch(e){ saveMsg.innerHTML=`<p class="warn">⚠️ Lỗi: ${e}</p>`; }
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


def luu_loat_va_ghep(ds: list, day: bool = False) -> dict:
    """Lưu ảnh đã xác nhận RỒI ghép vào truyện, cập nhật thư viện, dựng lại Xưởng.

    ds: [{key, data(base64)}]. `day=True` mới commit + push lên GitHub — mặc định
    KHÔNG đẩy, để chạy thử và bộ kiểm thử không bao giờ đẩy ảnh thử lên main.
    """
    ket_qua = []
    for item in ds or []:
        key = (item.get("key") or "").strip()
        if not key or not _asset_theo_key(key):
            continue
        ket_qua.append({"key": key, "data": item.get("data", ""),
                        "name": item.get("name") or key,
                        "cach": "nguoi-xac-nhan", "do_tin_cay": 100})

    if not ket_qua:
        return {"ok": False, "da_luu": [], "loi": "Chưa chọn prompt nào."}

    try:
        import xuong_tu_dong as X
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "da_luu": [], "loi": f"Thiếu mô-đun ghép ảnh: {e}"}

    bc = X.luu_va_ghep(ket_qua)
    bc["ok"] = not bc.get("loi")
    bc["ghep"] = bc.get("ghep", {})

    # Dựng lại Xưởng tĩnh + đẩy lên GitHub (nếu là kho git).
    bc["xuong"] = _dung_lai_xuong()
    bc["day_len"] = _day_len_github(bc.get("da_luu", [])) if day else "chưa đẩy (chưa bật)"
    return bc


def _dung_lai_xuong() -> str:
    """Dựng lại docs/xuong/index.html để trạng thái ảnh đúng ngay."""
    try:
        from tools import build_xuong as BX  # noqa: PLC0415
        with open(BX.OUT, "w", encoding="utf-8") as f:
            f.write(BX.build())
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"lỗi: {e}"


def _day_len_github(da_luu: list) -> str:
    """Commit + push ảnh mới để bản chơi trên web cập nhật.

    Chỉ chạy khi thư mục là kho git và có remote (bỏ qua khi chạy thử cục bộ).
    """
    import subprocess

    def _run(*args):
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)

    if os.environ.get("XUONG_KHONG_DAY"):
        return "bỏ qua (chế độ thử)"
    try:
        if _run("git", "rev-parse", "--is-inside-work-tree").returncode != 0:
            return "bỏ qua (không phải kho git)"
        if _run("git", "remote", "get-url", "origin").returncode != 0:
            return "bỏ qua (không có remote)"
        _run("git", "add", "-A")
        if _run("git", "diff", "--cached", "--quiet").returncode == 0:
            return "không có gì mới"
        ten = ", ".join(x.get("file", "") for x in da_luu[:5]) or "ảnh mới"
        msg = f"Xưởng: ghép {len(da_luu)} ảnh ({ten})"
        if _run("git", "commit", "-m", msg).returncode != 0:
            return "lỗi: không commit được"
        r = _run("git", "push", "origin", "HEAD:main")
        if r.returncode != 0:
            return f"lỗi đẩy: {(r.stderr or '').strip()[:160]}"
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"lỗi: {e}"


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
