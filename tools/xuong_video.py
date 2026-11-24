"""Dữ liệu Xưởng VIDEO: 14 cảnh dựng trailer intro.

Khác Xưởng ảnh ở chỗ ảnh game là thẻ cảnh 3:4 (chừa chỗ cho chữ, dùng khi chơi),
còn ảnh trailer là khung 9:16 điện ảnh (chủ thể chiếm khung, có chiều sâu).
Đây là hai bộ ảnh độc lập — không cắt ảnh game ra làm trailer.

Mô tả nhân vật / đồ vật lấy TRỰC TIẾP từ `tai-lieu/CANON-NHAN-VAT-DO-VAT.md`
lúc chạy, để không bao giờ lệch canon. Canon quy định: chép nguyên văn.
"""

from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON_FILE = os.path.join(ROOT, "tai-lieu", "CANON-NHAN-VAT-DO-VAT.md")
VIDEO_DIR = os.path.join(ROOT, "docs", "assets", "video")
TI_LE = "9:16 dọc (1080×1920)"
TI_LE_EN = "9:16 vertical (1080×1920)"
KHUNG = (1080, 1920)

# ── Khối phong cách dùng chung (khớp MAU_GOC + NO_TEXT của Xưởng ảnh) ──
STYLE_VIDEO = (
    "Traditional East Asian colour-ink painting (cǎi-mò / 彩墨) on smooth handmade mulberry (dó) paper: "
    "an ink-wash picture still dominated by black ink and bare pale dó paper, with only a few restrained, "
    "muted washes of soft colour laid over the ink. Keep the brushwork clean and controlled with crisp, "
    "well-defined edges, and the generous empty negative space (liubai) of an ancient "
    "hanging scroll. Use a small desaturated palette — soft indigo and slate blue for sky and water, jade "
    "and olive green for foliage, warm ochre and sepia for earth and wood, off-white and pale blue for "
    "cloth, and a single restrained accent of vermilion or ember orange for fire and lamps. Never bright, "
    "never saturated, never a full-colour painting: most of the image must remain black ink and bare paper. "
    "Draw every outline as one continuous unbroken brush stroke with a smooth steady curve: "
    "no jagged zigzag edges, no sketchy broken lines, no short choppy overlapping strokes, "
    "no abstract or scribbled shapes. Contours of faces, hands and clothing folds must be crisp, "
    "clean and clearly readable, with solid filled shapes rather than scattered fragments of ink. "
    "Flat, even ink coverage inside each shape, with no speckle, no splatter and no bleeding halo. "
    "IMPORTANT: absolutely no text, no letters, no numbers, no calligraphy, no signature, "
    "no watermark, no logo, no UI labels."
)

NEGATIVE = (
    "text, letters, watermark, signature, logo, photorealistic, 3d render, cgi, anime, cartoon, "
    "oversaturated, neon, plastic skin, modern objects, cars, buildings, blurry, low detail, "
    "jagged zigzag lines, broken sketchy strokes, abstract scribbles, ink splatter, "
    "muddy bleeding ink, fragmented shapes, "
    "extra limbs, deformed hands, cluttered composition"
)

CANON_LUU_Y = (
    "Khung hình ĐIỆN ẢNH dọc 9:16. Chủ thể chiếm khung, có tiền cảnh – trung cảnh – hậu cảnh "
    "rõ ràng, tương phản mạnh, ánh sáng có hướng. Không phải thẻ cảnh tĩnh kiểu ảnh trong game."
)

# Bản dịch chuyển động camera sang tiếng Anh — prompt gửi AI phải thuần Anh,
# trộn tiếng Việt vào giữa câu lệnh sẽ làm AI hiểu sai.
CAMERA_EN = {
    "Zoom out rất chậm": "very slow zoom out",
    "Pan lên": "slow tilt up",
    "Zoom in mạnh": "strong zoom in",
    "Cắt thẳng": "static camera, no movement",
    "Pan ngang phải, rất chậm (100% → 112%)": "very slow pan right, zooming from 100% to 112%",
    "Zoom in chậm": "slow zoom in",
    "Zoom in nhanh (100% → 118%) + shake nhẹ": "fast zoom in from 100% to 118%, with a subtle shake",
    "Zoom in rất chậm": "very slow zoom in",
    "Pan ngang trái": "slow pan left",
    "Pan ngang phải": "slow pan right",
    "Rung nhẹ": "subtle shake, no zoom",
    "Tĩnh": "completely static, no movement",
}


def _canon(ma: str) -> str:
    """Chép nguyên văn khối 'Mô tả cố định' của một mục canon (NV-4, DV-1…)."""
    if not os.path.isfile(CANON_FILE):
        raise FileNotFoundError(f"Thiếu file canon: {CANON_FILE}")
    noi_dung = open(CANON_FILE, encoding="utf-8").read()
    mau = re.search(rf"^### {re.escape(ma)} ·.*?```\n(.*?)```", noi_dung, re.S | re.M)
    if not mau:
        raise ValueError(f"Không tìm thấy mục canon {ma} trong {CANON_FILE}")
    return " ".join(mau.group(1).split())


# ── Phần: nhóm cảnh theo mạch trailer ──
PHAN_VIDEO = [
    {"ma": "pham-nhan", "icon": "🌾", "ten": "Mở — Phàm nhân",
     "mota": "Cái nghèo, cái nhỏ bé, rồi cú giật xuyên không. Nhịp chậm, gần như không nhạc."},
    {"ma": "tien-gioi", "icon": "⛰️", "ten": "Tiên giới",
     "mota": "Thế giới tu tiên mở ra — cảnh lớn nhất của trailer, nhạc vào mạnh."},
    {"ma": "suc-manh", "icon": "⚔️", "ten": "Sức mạnh",
     "mota": "Đột phá, ngọc cốt, yêu thú, vạn kiếm — nhịp dồn dần."},
    {"ma": "mat-mat", "icon": "🔥", "ten": "Mất mát",
     "mota": "Điểm tối nhất. Cắt sạch nhạc, chỉ còn tiếng lửa."},
    {"ma": "ket", "icon": "🌅", "ten": "Kết",
     "mota": "Khoảng lặng trước tiêu đề, rồi tên game."},
]

# ── 14 cảnh. `giay` là thời lượng; mốc thời gian tính tự động để không lệch. ──
CANH_VIDEO = [
    {
        "key": "v01", "phan": "pham-nhan",
        "ten": "Phàm nhân — ruộng bậc thang",
        "ten_en": "Mortal — terraced fields",
        "file": "v01_pham_nhan.jpg",
        "giay": 5,
        "chuyen_dong": "Zoom out rất chậm",
        "chuyen_canh": "Dissolve 0.6s",
        "chu": "Phàm nhân sinh ra đã là phàm nhân.",
        "prompt": (
            "Cinematic wide establishing shot, vertical composition. Vast terraced rice paddies climbing "
            "the lower slopes of enormous mountains at first grey light. Thin water lies in the flooded "
            "terraces, catching pale cold sky in long silver bands that step up the hillside. In the lower "
            "third, tiny and insignificant, a single barefoot peasant child in coarse patched hemp carries "
            "two wooden water buckets on a shoulder pole along a narrow earth ridge, walking away from the "
            "viewer. Behind and above everything, the mountain slopes rise out of frame into pale mist and "
            "empty paper — the peaks are not visible, only the sense that they are impossibly high. A few "
            "thin strokes of bare winter trees at the field edges. Cold, quiet, poor, ordinary. The whole "
            "world is grey and small. Foreground: dark wet earth ridge, strong and detailed. Middle ground: "
            "the terraces stepping upward. Background: mist and empty paper. Deep atmospheric perspective."
        ),
    },
    {
        "key": "v02", "phan": "pham-nhan",
        "ten": "Ngước nhìn đỉnh núi tiên",
        "ten_en": "Looking up at the immortal peak",
        "file": "v02_nguoc_nhin.jpg",
        "giay": 4,
        "chuyen_dong": "Pan lên",
        "chuyen_canh": "Dissolve 0.6s",
        "chu": "Kẻ không chịu như vậy… sẽ phải trả giá.",
        "prompt": (
            "Dramatic low-angle vertical shot, looking steeply upward. In the very bottom of the frame, seen "
            "from behind and slightly to one side, the small dark silhouette of a barefoot peasant boy in "
            "patched hemp clothing, head tilted back, gazing up. Above him the frame is almost entirely "
            "consumed by colossal mountain cliffs rising vertically out of sight, their bases dark and "
            "detailed with a few twisted pines clinging to the rock, their upper reaches dissolving into "
            "pale mist and bare paper so the peaks are never seen. Far up in the empty pale sky, tiny and "
            "faint, a few cranes fly in a loose line — the only hint that something lives above. The scale "
            "is overwhelming: the boy is less than a tenth of the frame height. Cold pale light from above, "
            "deep shadow at the cliff bases. Foreground: the boy's shoulders and the back of his head, dark. "
            "Middle ground: sheer rock. Background: mist and emptiness. Small, awed, yearning — the moment "
            "a mortal first looks at the world of immortals."
        ),
    },
    {
        "key": "v03", "phan": "pham-nhan",
        "ten": "Đô thị tan thành mực",
        "ten_en": "The city dissolving into ink",
        "file": "v03_do_thi_tan.jpg",
        "giay": 3,
        "chuyen_dong": "Zoom in mạnh",
        "chuyen_canh": "Cắt thẳng",
        "chu": "Một đêm, cả thế giới cũ tan thành mực.",
        "prompt": (
            "A surreal transitional image, vertical composition. A dense modern city skyline of glass towers "
            "is dissolving downward into wet black ink: the upper towers are still faintly legible as pale "
            "grey geometric shapes, but from the middle of the frame down they melt and run, bleeding into "
            "soft black wash and feathered ink edges that spread across the paper like water soaking upward. "
            "Street lights and window grids survive only as a few tiny cold blue-white points of light "
            "trapped in the dissolving ink. At the very bottom, the ink has pooled into a still dark surface. "
            "No people, no vehicles, no readable signs. The whole image reads as a world being erased and "
            "rewritten. Vertical motion: solid at top, liquid at bottom. High contrast, unsettling, quiet "
            "catastrophe."
        ),
    },
    {
        "key": "v04", "phan": "pham-nhan",
        "ten": "Thức tỉnh — bàn tay lạ",
        "ten_en": "Awakening — a stranger's hand",
        "file": "v04_thuc_tinh.jpg",
        "giay": 3,
        "chuyen_dong": "Zoom in rất chậm",
        "chuyen_canh": "Cắt thẳng",
        "chu": "Ta tỉnh dậy trong thân xác kẻ thấp nhất trấn này.",
        "prompt": (
            "Extreme close-up, vertical composition, seen from directly above. A single open hand lies "
            "palm-up on cold wet grey stone, fingers slightly curled and trembling. The hand is thin and "
            "underfed: sun-tanned skin, hard callouses across the palm and finger bases, cracked knuckles, "
            "dark-rimmed nails with dirt worked into the edges, a faint old scar across the back. A coarse "
            "frayed grey-brown hemp sleeve, far too large for the arm, bunches at the wrist. Beside the hand "
            "on the wet stone: a few grains of straw, a smear of mud, and a thin film of water reflecting "
            "pale cold light. Shallow depth of field — the fingertips are sharp, the edges of the frame fall "
            "away into soft dark ink shadow. No face, no body. Intimate, disorienting — a body recognised as "
            "not one's own."
        ),
    },
    {
        "key": "v05", "phan": "tien-gioi",
        "ten": "Tiên giới — toàn cảnh",
        "ten_en": "Immortal realm — wide panorama",
        "file": "v05_tien_gioi.jpg",
        "giay": 8,
        "chuyen_dong": "Pan ngang phải, rất chậm (100% → 112%)",
        "chuyen_canh": "Cắt thẳng / Fade to White 0.2s",
        "chu": "TU TIÊN",
        "prompt": (
            "Epic cinematic vertical panorama of an immortal mountain realm. Colossal stone peaks rise in "
            "layered ranks, the nearest dark and detailed, the furthest reduced to pale grey silhouettes "
            "that dissolve into empty paper at the top of the frame. A vast sea of cloud fills the valleys "
            "between the peaks, its surface catching pale cold light in long soft bands. On the shoulders of "
            "two or three of the great peaks perch ancient Chinese sect buildings — slender pagodas with "
            "upswept eaves, long covered galleries, stone platforms cut into the cliff face — all tiny "
            "against the mountains, connected by impossibly thin stone bridges spanning the cloud sea. Long "
            "white waterfalls plunge from the cliff edges and disappear into the mist below. A flock of "
            "cranes wheels slowly across the middle distance. A few twisted pines cling to the rock in the "
            "foreground, dark and sharp. Deep layered atmospheric perspective: near is black and detailed, "
            "far is pale and empty. Foreground: dark cliff edge and pine. Middle ground: cloud sea, bridges, "
            "sect buildings, waterfalls. Background: fading peaks and bare paper sky. Majestic, vast, "
            "silent, ancient. The world the mortal boy was looking at."
        ),
    },
    {
        "key": "v06", "phan": "tien-gioi",
        "ten": "Tông môn — bậc đá lên trời",
        "ten_en": "The sect — stairway to heaven",
        "file": "v06_tong_mon.jpg",
        "giay": 5,
        "chuyen_dong": "Pan lên",
        "chuyen_canh": "Dissolve 0.5s",
        "chu": "Nơi này, mạng người rẻ hơn một viên đan.",
        "prompt": (
            "Vertical low-angle shot of the entrance to an ancient Chinese martial sect. A monumental stone "
            "stairway climbs steeply away from the viewer and out of the top of the frame, its steps worn "
            "concave by centuries of feet. At the base, two massive stone pillars flank the first step, "
            "weathered and carved with faint cloud patterns, a great horizontal stone lintel resting across "
            "them. Long blue-grey banners hang from the pillars, their fabric hanging heavy and still. On "
            "both sides of the stairway, tall dark pines. Halfway up, small figures in pale robes climb the "
            "steps in a loose file, tiny and distant — disciples going up. High above, the top of the "
            "stairway is lost in pale mist, so the sect itself is never shown, only implied. Cold morning "
            "light slanting across the steps, long shadows between them. Foreground: worn stone steps, sharp "
            "and detailed. Middle ground: pillars, banners, pines, climbing figures. Background: mist and "
            "empty paper. Formal, imposing, a threshold that cannot be uncrossed."
        ),
    },
    {
        "key": "v07", "phan": "tien-gioi",
        "ten": "Tu luyện bên vực",
        "ten_en": "Cultivating at the precipice",
        "file": "v07_tu_luyen.jpg",
        "giay": 5,
        "chuyen_dong": "Zoom in chậm",
        "chuyen_canh": "Dissolve 0.5s",
        "chu": "Ta không có linh căn. Nhưng ta có thứ đáng sợ hơn.",
        "prompt": (
            "Vertical composition, seen from slightly behind and to one side. A single figure in coarse grey "
            "robes sits cross-legged in meditation on a narrow rock ledge at the very edge of a precipice, "
            "facing away from the viewer toward the void. His back is straight, hands resting on his knees, "
            "posture absolute stillness. Beyond the ledge, the world falls away into a vast sea of pale mist "
            "— no bottom visible, only empty paper fading downward. Around his shoulders and above his head, "
            "a slow spiral of pale blue-white mist and faint light motes turns in the air, the only motion in "
            "an otherwise still image, suggesting qi gathering. A thin cold dawn light from the left "
            "rim-lights his shoulders and the edge of the rock. A few dry grass blades at the ledge edge bend "
            "in a wind. Foreground: the seated figure and rock ledge, dark and sharp. Middle ground: the void "
            "of mist. Background: empty pale paper. Disciplined, solitary, patient. A mortal forcing himself "
            "to become something else."
        ),
    },
    {
        "key": "v08", "phan": "suc-manh",
        "ten": "Đột phá",
        "ten_en": "Breakthrough",
        "file": "v08_dot_pha.jpg",
        "giay": 4,
        "chuyen_dong": "Zoom in nhanh (100% → 118%) + shake nhẹ",
        "chuyen_canh": "Dissolve 0.4s",
        "chu": "Luyện Khí · Trúc Cơ · Kim Đan · Nguyên Anh",
        "prompt": (
            "A violent burst of released energy, vertical composition, centred. At the centre of the frame a "
            "seated meditating figure in coarse grey robes, seen from the front, is silhouetted inside an "
            "expanding sphere of pale jade-green and white light — his robe and hair blown outward by the "
            "force. The expanding wave of the breakthrough radiates outward as concentric rings of ink: sharp "
            "dark brush strokes near the centre, breaking into dry bristle fragments and spray at the edges, "
            "scattering across the paper like an explosion drawn in calligraphy. Loose gravel, leaves and "
            "dust are lifted off the ground and thrown outward in streaks. The ground beneath him is cracked "
            "in a radial pattern. Above, the sky is torn open with pale light. The jade-green glow is the "
            "only colour in an otherwise black and cream image. Foreground: cracked ground and flying debris. "
            "Middle ground: the figure in the light sphere. Background: radiating ink shockwave and pale sky. "
            "Explosive, triumphant, the instant a mortal ceases to be merely mortal."
        ),
    },
    {
        "key": "v09", "phan": "suc-manh",
        "ten": "Ngọc cốt phát sáng",
        "ten_en": "The jade bone glowing",
        "file": "v09_ngoc_cot.jpg",
        "giay": 5,
        "chuyen_dong": "Zoom in rất chậm",
        "chuyen_canh": "Dissolve 0.5s",
        "chu": "Trong khối ngọc này, có thứ đã ngủ ngàn năm.",
        "canon": "DV-1",
        "prompt": (
            "Vertical cinematic close shot, dramatic low light. {canon} "
            "The soil around it is wet and black, clods of earth casting long soft shadows in the cold halo "
            "of the stone. A few thin wisps of pale mist curl up from the soil around the stone and drift "
            "into the darkness. Tiny floating light motes hang in the air. Everything beyond the halo falls "
            "away into deep black ink shadow. Nothing else in the frame. Foreground: the jade and wet soil, "
            "sharply detailed. Background: pure dark ink. Ancient, sealed, waiting. Something alive inside "
            "something dead."
        ),
    },
    {
        "key": "v10", "phan": "suc-manh",
        "ten": "Yêu thú trong sương",
        "ten_en": "Demon beast in the mist",
        "file": "v10_yeu_thu.jpg",
        "giay": 4,
        "chuyen_dong": "Pan ngang trái",
        "chuyen_canh": "Dissolve 0.5s",
        "chu": "Thế giới này không dành cho kẻ yếu.",
        "prompt": (
            "Vertical composition, seen from the ground looking up into dense mist. A colossal demon beast "
            "emerges from the fog, only partly visible: an enormous horned head lowered toward the viewer, "
            "filling the upper half of the frame, its body lost entirely in mist so the scale is impossible "
            "to judge. The creature is rendered as heavy black ink masses with smooth fur texture, its "
            "hide suggesting thick coarse scales. Two huge eyes glow with a single cold amber-orange light — "
            "the only warm colour in the image — and a long slow breath of white vapour curls from its "
            "nostrils. Its horns are massive, ridged and dark. In the extreme lower foreground, tiny and "
            "insignificant, the dark silhouettes of two or three human figures in robes stand frozen, weapons "
            "half-raised, less than a twentieth of the frame height. Sparse twisted branches cross the "
            "corners of the frame. Foreground: tiny human figures, sharp black silhouettes. Middle ground: "
            "the vast head and glowing eyes. Background: solid pale mist and empty paper. Overwhelming, "
            "predatory, ancient. The world does not care that you are the protagonist."
        ),
    },
    {
        "key": "v11", "phan": "suc-manh",
        "ten": "Vạn kiếm xuất không",
        "ten_en": "Ten thousand swords",
        "file": "v11_van_kiem.jpg",
        "giay": 5,
        "chuyen_dong": "Pan ngang phải",
        "chuyen_canh": "Dissolve 0.5s",
        "chu": "Cũng không dành cho kẻ mạnh.",
        "prompt": (
            "Dynamic vertical composition, sky filled with flying swords. Dozens of slender Chinese straight "
            "swords streak diagonally upward and across the frame in a loose swarm, each trailing a long thin "
            "line of pale cold light like a comet's tail — the trails are drawn as clean smooth tapering strokes, "
            "tapering and breaking into bristle fragments at their ends. The blades themselves are dark "
            "silhouettes with a thin bright edge catching light. They rise from a dark mountain ridge at the "
            "bottom of the frame and converge toward the upper right, where the light trails knot together "
            "into a bright pale knot before dispersing. In the lower foreground, the small dark figure of a "
            "swordsman in flowing robes stands on the ridge, one arm raised, commanding them. Thin cloud "
            "wisps torn apart by the passage of the blades. The sky is pale and open; the ridge and figure "
            "are deep black. Foreground: the summoning figure on the ridge, sharp black. Middle ground: the "
            "swarm of blades and their light trails. Background: pale open sky. Swift, overwhelming, "
            "beautiful and lethal."
        ),
    },
    {
        "key": "v12", "phan": "mat-mat",
        "ten": "Tông môn chìm trong lửa",
        "ten_en": "The sect burning",
        "file": "v12_chay.jpg",
        "giay": 5,
        "chuyen_dong": "Rung nhẹ",
        "chuyen_canh": "Cắt thẳng",
        "chu": "Chỉ dành cho kẻ dám phản bội chính mình.",
        "prompt": (
            "Vertical composition, a sect destroyed at night. The great pagoda and long galleries of an "
            "ancient Chinese immortal sect burn fiercely — tall vermilion and ember-orange flames leap from "
            "the tiered roofs, the only strong colour in the image, everything else black ink and smoke. "
            "Thick black smoke boils upward and swallows the top of the frame. Burning debris and sparks "
            "drift across the middle distance. The stone stairway in the foreground is strewn with broken "
            "weapons, torn blue-grey banners and fallen bodies rendered only as dark shapes, no faces. A few "
            "small figures flee down the steps toward the viewer, each drawn with clean continuous outlines. A great "
            "bronze bell has fallen from its frame and lies cracked on the ground. Cold moonlight cuts "
            "through the smoke in one pale shaft. Foreground: wreckage, fallen bell, fleeing figures. Middle "
            "ground: the burning sect. Background: smoke and dark. Catastrophic, tragic, total. The end of "
            "everything that was built."
        ),
    },
    {
        "key": "v13", "phan": "ket",
        "ten": "Đối đầu — người chơi và Hàn Lập",
        "ten_en": "Standoff — the player and Han Li",
        "file": "v13_han_lap.jpg",
        "giay": 7,
        "chuyen_dong": "Zoom in rất chậm",
        "chuyen_canh": "Dissolve 0.6s",
        "chu": "Ta biết tương lai của ngươi. Và ta sẽ đổi nó.",
        "canon": ["NV-1", "NV-4"],
        "prompt": (
            "Cinematic vertical two-shot, a standoff between two young men on a dark hillside path at "
            "dusk. They stand facing each other at a slight angle, roughly equal in the frame, a narrow "
            "gap of empty dark paper between them — neither is dominant, and neither has drawn a weapon. "
            "LEFT, seen in three-quarter profile turned toward the right: {canon0} "
            "RIGHT, seen in three-quarter profile turned toward the left: {canon1} "
            "Both are the same height and the same age, both thin, both plainly dressed and poor — the "
            "mirror of each other. The left one's eyes are alert and calculating, the eyes of a man doing "
            "arithmetic he does not intend to share. The right one's eyes are cold and unreadable, the eyes "
            "of a man who has already decided something. Between them, at chest height, a faint pale mist "
            "drifts and curls, the only bright thing in the frame. A cold pale rim light from above catches "
            "one edge of each face and leaves the rest in deep shadow, so they are lit identically — two "
            "men under the same sky, on opposite sides of a line neither has drawn yet. Behind them, "
            "hillside rock and pine dissolve into black ink and empty paper. The lower third of the frame "
            "is empty dark ink so a line of text can be placed beneath. Foreground: dark wet stone. Middle "
            "ground: the two figures, sharp. Background: black ink and void. Quiet, tense, dangerous — the "
            "moment two people recognise each other as the only real threat in the room."
        ),
    },
    {
        "key": "v14", "phan": "ket",
        "ten": "Nền tiêu đề",
        "ten_en": "Title background",
        "file": "v14_nen_tieu_de.jpg",
        "giay": 9,
        "chuyen_dong": "Tĩnh",
        "chuyen_canh": "Dissolve 0.8s",
        "chu": "HỒNG ĐỨC TU TIÊN LỘ / Nghịch chuyển càn khôn",
        "prompt": (
            "A nearly empty vertical sheet of smooth handmade mulberry paper filling the frame, pale warm "
            "cream with visible fibre texture and faint uneven washes of pale sepia near the edges. A single "
            "long vertical brush stroke of black ink descends through the upper middle of the paper — thick "
            "and dark where the brush first touched down, thinning and breaking into dry bristle marks as it "
            "trails downward. Along the very bottom edge, a faint suggestion of mist-wrapped mountain ridges, "
            "no more than two or three soft grey strokes, almost invisible. The whole centre of the frame is "
            "bare, open, untouched paper — empty and light so a title can be placed on top. Low contrast, "
            "calm, quiet, generous negative space."
        ),
    },
]

# ── Nhạc nền & hướng dẫn dựng ──
# (mốc, ghi chú tiếng Việt cho người dùng, chỉ dẫn tiếng Anh cho AI tạo nhạc)
GOI_Y_NHAC = [
    ("0:00–0:15", "Gần như im. Chỉ một nốt trầm rất khẽ, để người xem chìm vào cái nghèo.",
     "near-silence, one very faint low drone"),
    ("0:15", "Nhạc vào mạnh đột ngột — trống da + dây trầm. Đây là cú nổ của cảnh tiên giới.",
     "sudden loud entry: frame drums and low strings"),
    ("0:33", "Nhịp dồn dần, thêm lớp dây cao.",
     "building pulse, add a high string layer"),
    ("0:44", "Tiếng gầm trầm của yêu thú, rất xa, dưới nền nhạc.",
     "a deep distant beast growl buried under the music"),
    ("0:51", "Cắt sạch nhạc 0.5s — chỉ còn tiếng lửa cháy, gỗ nổ, chuông đồng rơi.",
     "hard cut of all music for half a second — only fire, cracking wood, a falling bronze bell"),
    ("0:56", "Gần như im hoàn toàn. Một nốt trầm giữ suốt cảnh Hàn Lập.",
     "almost total silence, one sustained low note held through the portrait"),
    ("1:03", "Chuông xa, nhạc dâng lên rồi tắt dần dưới tiêu đề.",
     "a distant bell, the score rises then fades under the title"),
]


def _thoi_luong() -> list:
    """Tính mốc bắt đầu/kết thúc từ thời lượng từng cảnh (không hardcode để khỏi lệch)."""
    moc, t = [], 0.0
    for c in CANH_VIDEO:
        moc.append((t, t + c["giay"]))
        t += c["giay"]
    return moc


def mmss(giay: float) -> str:
    giay = int(round(giay))
    return f"{giay // 60}:{giay % 60:02d}"


def moc_thoi_gian() -> dict:
    """key -> {bat_dau, ket_thuc, bat_dau_s, ket_thuc_s}."""
    return {
        c["key"]: {"bat_dau": mmss(a), "ket_thuc": mmss(b), "bat_dau_s": a, "ket_thuc_s": b}
        for c, (a, b) in zip(CANH_VIDEO, _thoi_luong())
    }


def tong_giay() -> int:
    return sum(c["giay"] for c in CANH_VIDEO)


def prompt_canh(c: dict) -> str:
    """Prompt đầy đủ của một cảnh: khối phong cách + phần mô tả riêng.

    Cảnh có hai nhân vật thì khai `canon` thành list và dùng `{canon0}`, `{canon1}`
    trong `prompt` — mỗi người vẫn chép nguyên văn mô tả cố định của mình.
    """
    than = c["prompt"]
    ma = c.get("canon")
    if isinstance(ma, str):
        than = than.replace("{canon}", _canon(ma))
    elif isinstance(ma, list):
        for i, m in enumerate(ma):
            than = than.replace("{canon%d}" % i, _canon(m))
    return f"{STYLE_VIDEO}\n\n{than}"


def prompt_am_thanh(c: dict) -> str:
    """Prompt riêng cho công cụ tạo video từ ảnh (image-to-video), nếu muốn dùng."""
    cam = CAMERA_EN.get(c["chuyen_dong"], c["chuyen_dong"])
    giay = c["giay"]
    manh = "an" if giay in (8, 11, 18) else "a"
    if cam.startswith("completely static"):
        return (
            f"Hold this still image for exactly {giay} seconds with no camera movement at all. "
            "The frame stays locked. Only the faintest life is allowed: one slow curl of mist, "
            "a few drifting light motes. Nothing else moves. "
            "Preserve the ink-wash painting style exactly: do not add detail, do not change colours, "
            "do not redraw anything. Keep the paper texture and the empty negative space. "
            "No text, no letters, no watermark, no logo."
        )
    return (
        f"Animate this still image into {manh} {giay}-second cinematic shot. "
        f"Camera movement: {cam}. "
        "Very slow, smooth, constant motion — no cuts, no sudden changes. "
        "Preserve the ink-wash painting style exactly: do not add detail, do not change colours, "
        "do not redraw faces or clothing. Keep the paper texture and the empty negative space. "
        "Subtle life only: drifting mist, faint light motes, slow swaying branches, gentle ember flicker. "
        "No text, no letters, no watermark, no logo."
    )


def canh_cua_phan(ma_phan: str) -> list:
    return [c for c in CANH_VIDEO if c["phan"] == ma_phan]


def da_co(c: dict) -> bool:
    return os.path.isfile(os.path.join(VIDEO_DIR, c["file"]))


def so_da_co() -> int:
    return sum(1 for c in CANH_VIDEO if da_co(c))


def _build_gop(ds: list, tieu_de: str) -> str:
    """Prompt gộp: dán 1 lần, AI vẽ lần lượt từng ảnh."""
    so = f"{len(ds)} image" + ("" if len(ds) == 1 else "s")
    dong = [
        f'TASK: Create {so} for the INTRO TRAILER of a Vietnamese cultivation game named '
        f'"Hồng Đức Tu Tiên Lộ" — {tieu_de}.',
        "Produce the images ONE BY ONE, in the order below, each as a SEPARATE image. "
        f"ALL images must be {TI_LE_EN} — vertical, cinematic, full-frame.",
        'If you cannot finish them all in one reply, make as many as you can and then stop; '
        'I will reply "tiếp tục" to get the next batch.',
        "",
        "SHARED ART STYLE (apply to EVERY image): " + STYLE_VIDEO,
        "",
        "LAYOUT RULE: these are cinematic trailer frames, NOT game scene cards. The subject must fill "
        "the frame with clear foreground, middle ground and background layers, strong contrast and "
        "directional light. Do not leave a large flat empty area for text — text is added later in "
        "the video editor.",
        "",
        "TEXT RULE: no text, no letters, no numbers, no calligraphy, no signature, no watermark, "
        "no logo in ANY image.",
        "",
    ]
    for i, c in enumerate(ds, 1):
        moc = moc_thoi_gian()[c["key"]]
        cam = CAMERA_EN.get(c["chuyen_dong"], c["chuyen_dong"])
        dong.append(f"{i}. {c['file']} — {TI_LE_EN} — {c.get('ten_en', c['ten'])} "
                    f"(video {moc['bat_dau']}–{moc['ket_thuc']}, {c['giay']}s, "
                    f"camera: {cam})")
        dong.append(f"   {prompt_canh(c).split(chr(10) + chr(10), 1)[1]}")
        dong.append("")
    return "\n".join(dong)


def build_gop_prompt_tat_ca() -> str:
    """Prompt TỔNG: một lần dán, vẽ cả 14 ảnh của trailer."""
    return _build_gop(CANH_VIDEO, "full 14-shot intro trailer")


def build_gop_prompt_phan(ma_phan: str) -> str:
    p = next((x for x in PHAN_VIDEO if x["ma"] == ma_phan), {"ten": ma_phan})
    return _build_gop(canh_cua_phan(ma_phan), f"part: {p['ten']}")


def prompt_nhac() -> str:
    """Prompt mô tả nhạc nền, để người dùng tìm/tạo nhạc khớp."""
    dong = [
        f"TASK: Create a {tong_giay()}-second instrumental score for the intro trailer of "
        '"Hồng Đức Tu Tiên Lộ", a Vietnamese cultivation (tu tiên) game set in the world of '
        "Phàm Nhân Tu Tiên.",
        "",
        "STYLE: traditional East Asian strings (guzheng, erhu, pipa) blended with dark ambient. "
        "No vocals, no lyrics. Restrained and ancient, never bombastic or modern.",
        "",
        "STRUCTURE — follow these timings exactly:",
    ]
    for moc, _vi, en in GOI_Y_NHAC:
        dong.append(f"  {moc} — {en}")
    dong += [
        "",
        "Dynamic shape: near-silence, then a sudden swell at 0:15, steady build to 0:51, "
        "a hard drop to almost nothing at 0:56, then a slow rise and fade under the title at 1:03.",
        f"Total length: exactly {tong_giay()} seconds.",
    ]
    return "\n".join(dong)
