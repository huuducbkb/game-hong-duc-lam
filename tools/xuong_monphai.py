"""Cảnh riêng cho nhánh Môn phái — MỖI ĐOẠN MỘT CẢNH RIÊNG.

Quy tắc của dự án (tai-lieu/VIEC-CAN-LAM.md): "mỗi cảnh 1 ảnh riêng", hai nhánh
không dùng chung ảnh. Nhánh môn phái có 41 đoạn nhưng trước đây chỉ 6 ảnh, trong
đó 3 ảnh gánh 15 đoạn — sai quy tắc.

Module này liệt kê 35 cảnh còn thiếu để mỗi đoạn có đúng một cảnh của nó. Sáu
đoạn đã có ảnh riêng (p05, p07, p08, p11, p16, p19) giữ ảnh cũ, mỗi ảnh đúng
một đoạn. tools_server.py nạp module này để mở rộng ASSETS / DOAN_CUA_ANH /
NHOM_CANH.
"""

# key, tên, mô tả dùng ở đâu, mô tả tiếng Anh cho AI vẽ (nối sau STYLE_MAU).
SCENES = [
    {
        "key": "bc_tan_xa_sang",
        "name": "Tân xá — sáng, thức giấc",
        "use": "Tân xá buổi sáng, tân đệ tử choàng tỉnh (p01).",
        "body": "A simple communal sleeping quarters in an ancient Chinese martial sect at early morning, seen from inside. A low wooden sleeping platform with thin rolled bedding just vacated, a small paper window letting in pale dawn light, a plain low table with a bowl, bare timber walls, dust motes floating in the light shaft. Beyond the door a courtyard and distant training sounds implied by a few dry ink strokes. Composition keeps the center low and calm for game text. Waking, disoriented, a new day.",
    },
    {
        "key": "bc_san_tap_ngay",
        "name": "Sân tập — giữa ngày",
        "use": "Sân tập rộng, hàng trăm đệ tử luyện võ (p02).",
        "body": "A wide earthen training ground of an ancient Chinese martial sect at midday, seen at eye level. Flat packed earth, blue sect banners on poles at both sides, rows of disciples practising staff and fist forms suggested loosely by ink strokes, faces not detailed, dust and heat haze in the air. In one corner a thin plain-robed youth practises alone, small in the frame. Composition keeps the upper third calm for game text. Hot, crowded, disciplined.",
    },
    {
        "key": "bc_san_tap_chen_ep",
        "name": "Sân tập — bị chèn ép",
        "use": "Tân đệ tử bị gã to con chèn ép trước đám đông (p03).",
        "body": "The same earthen training ground, close view: a thin young disciple in coarse patched robes has stumbled and fallen back onto the ground, a wooden staff thrown aside, while a burly sneering senior disciple stands over him and jeers, a few other disciples laughing behind. Faces suggested, not detailed. Harsh midday light, dust kicked up. Composition keeps one side calm for game text. Humiliating, tense.",
    },
    {
        "key": "bc_san_sau_luyen_dem",
        "name": "Sân sau — luyện lén trong đêm",
        "use": "Lén ra sân sau luyện lại bài quyền nhập môn (p03b).",
        "body": "A hidden back courtyard of an ancient Chinese martial sect at night, seen at eye level. An old gnarled tree, a low stone wall, frost on the ground, a thin sickle moon. In the middle a lone young disciple in patched robes practises a fist form alone by moonlight, sleeves rolled, breath visible in the cold. Deep quiet, long shadows. Composition keeps the upper part dark and calm for game text. Solitary, stubborn.",
    },
    {
        "key": "bc_san_tap_cai_lai",
        "name": "Sân tập — cãi lại",
        "use": "Tân đệ tử cãi lại, bị tát ngã, không cúi đầu (p03c).",
        "body": "The training ground seen close and low: a thin young disciple sits fallen on the packed earth, blood at the corner of his mouth, head raised defiantly, while a burly senior disciple turns away in anger, a crowd of silent disciples watching. Faces loosely suggested. Harsh light, dust. Composition keeps one side calm for game text. Defiant, painful, a flicker of respect.",
    },
    {
        "key": "bc_san_sau_anh_sang",
        "name": "Sân sau — ánh sáng lạ dưới gốc cổ thụ",
        "use": "Đào thấy khối ngọc phát sáng dưới rễ cổ thụ (p03d).",
        "body": "A moonlit back courtyard of an ancient martial sect, close on the base of an old tree. A thin young disciple kneels in the dirt, hands just parted the leaf mould, and from the exposed roots a faint cold blue-white glow seeps up between his fingers. Night mist, deep shadow all around. Composition keeps the upper part dark for game text. Secret, uncanny, a fateful discovery.",
    },
    {
        "key": "bc_san_sau_chon_lai",
        "name": "Sân sau — chôn trả lại",
        "use": "Vội vàng lấp đất chôn lại khối ngọc (p03e).",
        "body": "The same moonlit back courtyard: the thin young disciple kneels pressing earth back over the roots with trembling hands, the faint blue glow already gone, only loose leaf mould scattered around. He looks back over his shoulder towards the dark quarters. Deep night, cold mist. Composition keeps the upper part dark and calm for game text. Uneasy, torn.",
    },
    {
        "key": "bc_vuon_thuoc_gap",
        "name": "Vườn thuốc — gặp Mạc Đại Phu",
        "use": "Lần đầu tới vườn thuốc, gặp Mạc Đại Phu (p04).",
        "body": "A quiet herb garden behind an ancient Chinese martial sect in soft daylight, seen at eye level. Neat beds of medicinal plants, a low wooden fence, drying bundles of herbs hung on a rack, mist over the far hill. At one corner an old grey-robed physician sits sorting herbs with slow sure hands, looking up at a thin young disciple who stands before him. Faces suggested. Composition keeps the upper third calm for game text. Calm, watchful.",
    },
    {
        "key": "bc_vuon_thuoc_hoi",
        "name": "Vườn thuốc — hỏi thẳng",
        "use": "Hỏi thẳng Mạc Đại Phu thấy gì khác thường (p04a).",
        "body": "Close view in a herb garden: the old grey-robed physician pauses in his work, a bundle of herbs in his hands, and studies the thin young disciple standing before him with a long, deep, unreadable gaze; the youth waits, tense. Herb bundles and low beds around them, soft daylight. Composition keeps one side calm for game text. Probing, quiet tension.",
    },
    {
        "key": "bc_vuon_thuoc_im",
        "name": "Vườn thuốc — im lặng",
        "use": "Không hỏi thêm, lặng lẽ phụ ông nhặt lá (p04b).",
        "body": "Herb garden, closer: the thin young disciple bows his head and says nothing, while the old physician gives a small satisfied nod and bends back to binding his herbs; the youth then crouches to help pick leaves. Soft daylight, bundles of drying herbs. Composition keeps one side calm for game text. Reserved, discreet, a silent understanding.",
    },
    {
        "key": "bc_khe_nui_dem",
        "name": "Hậu sơn — khe núi đêm",
        "use": "Theo lời đồn, lẻn ra khe núi sau hậu sơn (p05b).",
        "body": "A narrow wet ravine behind an ancient Chinese mountain sect at night, seen at eye level. Grey boulders, moss-covered walls close on both sides, a low sickle moon above, thin mist. In the middle the thin young disciple crouches over a patch of freshly disturbed moss, a faint cold blue glimmer just fading in the earth. Composition keeps the upper part dark for game text. Cold, secret, tense.",
    },
    {
        "key": "bc_khe_nui_chon",
        "name": "Hậu sơn — chôn trả lại",
        "use": "Lấp rêu chôn lại khối ngọc nơi khe núi (p05c).",
        "body": "The same narrow ravine at deep night: the thin young disciple kneels pressing moss and earth back into place, the glow gone, wind moving through the cleft. He looks small against the wet stone walls. Long shadows, thin mist. Composition keeps the upper part dark and calm for game text. Restless, drawn back against his will.",
    },
    {
        "key": "bc_vuon_thuoc_ngoc",
        "name": "Vườn thuốc — khối ngọc dưới luống cỏ",
        "use": "Nhổ cỏ vườn thuốc, chạm phải khối ngọc trước mặt Mạc Đại Phu (p06).",
        "body": "Herb garden in early morning: the thin young disciple kneels among weeds, one hand frozen just above the moss where a small pale jade piece lies half-revealed, a faint cold inner glow in it; behind him the old physician bends over his herbs, apparently paying no attention. Soft mist, drying herb racks. Composition keeps one side calm for game text. Secret, uneasy.",
    },
    {
        "key": "bc_vuon_thuoc_dem",
        "name": "Vườn thuốc — chôn trả lại, đêm",
        "use": "Trằn trọc rồi lén quay lại vườn thuốc đào lên (p06b).",
        "body": "The herb garden at dusk, then night: the thin young disciple crouches pressing earth back over a weed bed, herb bundles still hanging above, the garden empty of the old physician. Deep shadow under the racks, drifting mist. Composition keeps the upper part dark and calm for game text. Guilty, haunted.",
    },
    {
        "key": "nv_tuyet_co_canh_giac",
        "name": "Ngọc cốt — cảnh giác",
        "use": "Cảnh giác trước lời đề nghị của Tuyết Cơ (p08b).",
        "body": "Interior of a dim communal quarters at night: the thin young disciple holds a small glowing pale jade piece before him, his face wary and disbelieving, while a faint translucent female figure of pale blue mist hovers just above the jade, one slender hand raised towards him. Warm lamp glow, deep shadow. Composition keeps one side calm for game text. Wary, uncanny.",
    },
    {
        "key": "nv_tuyet_co_than_phan",
        "name": "Ngọc cốt — Tuyết Cơ giới thiệu thân phận",
        "use": "Tuyết Cơ nói rõ mình là nội môn đệ tử Hợp Hoan Tông (p09).",
        "body": "Close night interior: a beautiful pale misty female cultivator, upper body only, half-lidded sultry eyes and a faint knowing smile, long black hair loose, pale blue-and-white gauze robes slipping off one shoulder, hovering above a small glowing jade piece held in the young disciple's hands. Cold mist, warm lamp glow. Composition keeps one side calm for game text. Alluring, mysterious.",
    },
    {
        "key": "nv_tuyet_co_dieu_kien",
        "name": "Ngọc cốt — điều kiện khế ước",
        "use": "Tuyết Cơ nêu điều kiện: cần một phần dương khí (p09b).",
        "body": "Night interior, close on two: the pale misty female cultivator leans slightly forward with an amused, appraising look, one translucent hand raised as if stating terms, while the thin young disciple watches her with a hard, guarded face, the glowing jade between them. Cold mist, dim lamp. Composition keeps one side calm for game text. Bargaining, dangerous.",
    },
    {
        "key": "nv_tuyet_co_do_du",
        "name": "Ngọc cốt — khoảnh khắc do dự",
        "use": "Do dự cân nhắc cái giá trước khi ký (p09c).",
        "body": "Night interior: the thin young disciple stares down at the small jade piece cupped in his palm, its inner light pulsing slowly like a breath, his expression troubled and undecided; the female figure is only a faint suggestion of pale mist at the edge of the frame. Deep shadow, dim lamp. Composition keeps one side calm for game text. Hesitant, heavy with consequence.",
    },
    {
        "key": "nv_tuyet_co_khe_uoc",
        "name": "Ngọc cốt — ký khế ước",
        "use": "Đưa tay ra, ký khế ước với Tuyết Cơ (p10).",
        "body": "Night interior, close on hands: the thin young disciple extends his hand, and a slender translucent female hand of pale mist rests lightly over it above the glowing jade piece; faint hair-thin light threads pass between them. A warm, quiet glow, deep shadow around. Composition keeps one side calm for game text. Solemn, binding, a pact sealed.",
    },
    {
        "key": "bc_tan_xa_song_tu",
        "name": "Tân xá — đêm, lần song tu đầu tiên",
        "use": "Thổi tắt đèn, lần song tu đầu tiên (p10b).",
        "body": "A dark communal quarters at night, the oil lamp just blown out. The thin young disciple sits cross-legged on the low sleeping platform, eyes closed, hands cupped over a small jade piece on his chest that glows faintly in slow even pulses, like a second heartbeat; a soft pale mist coils around his shoulders. Deep dark, one dim glow. Composition keeps the upper part dark and calm for game text. Intimate, quiet, secret.",
    },
    {
        "key": "bc_tan_xa_kho_tu",
        "name": "Tân xá — khổ tu, lần thất bại",
        "use": "Đêm thứ hai, dẫn khí tán loạn, đau đớn (p11b).",
        "body": "A dark corner of communal quarters at night: the thin young disciple doubles over clutching his chest, sweat on his brow, face contorted, a small jade piece lying dim and cold beside him; the air around him faintly distorted as if stray energy scattered. Deep shadow, one dim lamp. Composition keeps the upper part dark for game text. Painful, stubborn.",
    },
    {
        "key": "bc_tan_xa_suyt_lo",
        "name": "Tân xá — suýt bị phát hiện",
        "use": "Sư huynh kiểm tra ban đêm, suýt lộ tu vi (p11c).",
        "body": "Night interior, tense: the thin young disciple lies still on the low sleeping platform pretending to sleep, a faint cold frost-like veil just fading from his skin, while a senior disciple's silhouette pauses at the open doorway with a lantern. Deep shadow, one lantern glow. Composition keeps one side dark for game text. Near-discovery, held breath.",
    },
    {
        "key": "bc_tan_xa_dot_pha",
        "name": "Tân xá — đột phá Luyện Khí tầng hai",
        "use": "Nửa tháng khổ tu, đột phá Luyện Khí tầng hai (p12).",
        "body": "Communal quarters just before dawn: the thin young disciple sits straight-backed on the sleeping platform, a faint warm aura of light rising around him, the small jade piece glowing steadily at his chest; a thin sliver of pale dawn light comes through the paper window. Calm, quiet power. Composition keeps the upper part calm for game text. Breakthrough, restrained triumph.",
    },
    {
        "key": "bc_dem_tap_kich",
        "name": "Đêm cuối — Dã Lang Bang tập kích",
        "use": "Tù và vang, cổng đông bùng lửa, Dã Lang Bang tập kích (p13).",
        "body": "An ancient Chinese martial sect at night under sudden attack, seen from within the quarters: through the open door, the eastern gate is ablaze with fire, dark figures running in chaos, disciples falling, thick smoke rolling across the courtyard. The thin young disciple stands in the doorway, short blade in hand, backlit by the fire. Ember-orange accent, deep shadow. Composition keeps the upper part smoky for game text. Alarm, chaos.",
    },
    {
        "key": "bc_cong_dong_doi_mat",
        "name": "Cổng đông — đối mặt địch",
        "use": "Chạy ngược dòng người, đối mặt địch nơi cổng vỡ (p14).",
        "body": "The shattered eastern gate of an ancient Chinese martial sect at night, seen at eye level from inside. The gate broken open, fallen disciples in blue robes on the blood-stained stone, raiders pouring through smoke, flames at the edges. In the foreground the thin young disciple faces a raised blade, body turned to evade. Ember-orange accent, deep shadow. Composition keeps the upper part smoky for game text. Desperate, defiant.",
    },
    {
        "key": "bc_cong_dong_giau",
        "name": "Cổng đông — giấu thực lực",
        "use": "Chỉ dùng võ công phàm nhân, giấu tu vi (p14b).",
        "body": "The broken gate courtyard at night, close on the thin young disciple mid-fight: he looks like an ordinary clumsy martial disciple, plain stance, no glow, no aura, simply enduring and striking back against two raiders pressing in on him; bodies of raiders at his feet. Ember-orange firelight, smoke. Composition keeps the upper part smoky for game text. Hard, restrained, hiding his strength.",
    },
    {
        "key": "bc_cong_dong_toan_luc",
        "name": "Cổng đông — dùng toàn lực ngọc cốt",
        "use": "Vận toàn lực ngọc cốt, tốc độ tăng vọt, bị nghi ngờ (p14c).",
        "body": "The broken gate courtyard at night: the thin young disciple moves with unnatural speed, a faint warm aura just visible around him, his blade a clean arc, three raiders already down; nearby disciples turn to stare at him with suspicion. Ember-orange firelight, thick smoke. Composition keeps the upper part smoky for game text. Fast, dangerous, exposed.",
    },
    {
        "key": "bc_cong_dong_quyen",
        "name": "Cổng đông — Thất Huyền quyền",
        "use": "Dùng Thất Huyền quyền đỡ đòn, phản kích (p14d).",
        "body": "Close night action at the broken gate: the thin young disciple in a low rooted stance of a plain martial fist form, one hand deflecting a descending blade, the other driving a straight punch into a raider's chest; precise and economical, no glow. Ember-orange firelight, dust and smoke. Composition keeps the upper part smoky for game text. Grounded, disciplined.",
    },
    {
        "key": "bc_cong_dong_hung_ba",
        "name": "Cổng đông — gọi tên Hùng Bá",
        "use": "Quát lớn gọi tên Hùng Bá, khiến địch khựng lại (p14e).",
        "body": "The broken gate courtyard at night: the thin young disciple stands with head raised, shouting into the dark, while raiders before him hesitate and glance back at each other; far off in the darkness a tall broad-shouldered silhouette with a heavy blade is only a suggestion of ink. Ember-orange firelight, smoke. Composition keeps the upper part smoky for game text. Bold, a name that carries weight.",
    },
    {
        "key": "bc_hoa_truong_cuu",
        "name": "Hỏa trường — cứu người",
        "use": "Lao vào lửa bẩy cột gỗ cứu đệ tử nhỏ (p15).",
        "body": "A burning storage yard spreading to the communal quarters at night: thick black smoke, orange flame licking the wooden buildings, embers in the air. In the middle the thin young disciple heaves a heavy fallen beam off the leg of a small crying young disciple, robes singed. Ember-orange accent, deep smoke. Composition keeps the upper part smoky for game text. Urgent, selfless.",
    },
    {
        "key": "nv_han_lap_gap",
        "name": "Gặp Hàn Lập — sau trận",
        "use": "Bám theo bóng người, chạm mặt Hàn Lập sau hậu sơn (p17).",
        "body": "A hidden hollow among boulders behind a mountain at grey dawn, close on two figures: a lean ordinary-featured young man in coarse undyed robes stands with his back half-turned, calm and unreadable, while the thin young disciple behind him watches tensely, one hand pressed to his chest. Cold mist, low pale light. Composition keeps one side calm for game text. Quiet, wary, fateful.",
    },
    {
        "key": "nv_han_lap_that",
        "name": "Hàn Lập — lời thành thật",
        "use": "Nói thật biết tương lai hắn; hắn cân nhắc giết ta (p18a).",
        "body": "Dawn among the boulders, close on two faces: the lean plain-robed young man looks straight at the thin disciple with cold, piercing eyes, his expression flat and dangerous, while the disciple's face is pale and strained. Cold mist, low grey light. Composition keeps one side calm for game text. Chilling, a knife's edge.",
    },
    {
        "key": "nv_han_lap_cuoi_tru",
        "name": "Hàn Lập — lời cười trừ",
        "use": "Cười trừ chối quanh; hắn không tin một chữ (p18b).",
        "body": "Dawn among the boulders: the thin disciple smiles awkwardly and looks away, while the lean plain-robed young man watches him with flat disbelief, quietly wiping blood from his sleeve. Cold mist, low grey light. Composition keeps one side calm for game text. A lie that fails.",
    },
    {
        "key": "nv_han_lap_hoi_nguoc",
        "name": "Hàn Lập — hỏi ngược",
        "use": "Hỏi ngược hắn giấu thứ gì; hắn khựng rồi cười lạnh (p18c).",
        "body": "Dawn among the boulders, close on two: the thin disciple has just spoken and the lean plain-robed young man pauses for a moment, then gives a thin cold smile that is neither glad nor angry. Pale moonlight thinning into dawn, cold mist. Composition keeps one side calm for game text. Two guarded people, mirrored.",
    },
    {
        "key": "nv_han_lap_bau_nuoc",
        "name": "Hàn Lập — bầu nước",
        "use": "Đưa bầu nước cho hắn; hắn nhớ mặt ta (p18d).",
        "body": "Dawn among the boulders: the thin disciple silently holds out a plain water gourd to the lean plain-robed young man, who looks at it with a flicker of surprise, one hand reaching to take it. Cold mist, low pale light. Composition keeps one side calm for game text. A small, unexpected kindness.",
    },
]

# Đoạn truyện → ảnh. MỘT đoạn một ảnh, không ảnh nào gánh hai đoạn.
# Sáu ảnh đầu đã có file (giữ nguyên); 35 ảnh sau là cảnh mới cần vẽ.
DOAN_CUA_ANH = {
    "c1_p01": "bc_tan_xa_sang",
    "c1_p02": "bc_san_tap_ngay",
    "c1_p03": "bc_san_tap_chen_ep",
    "c1_p03b": "bc_san_sau_luyen_dem",
    "c1_p03c": "bc_san_tap_cai_lai",
    "c1_p03d": "bc_san_sau_anh_sang",
    "c1_p03e": "bc_san_sau_chon_lai",
    "c1_p04": "bc_vuon_thuoc_gap",
    "c1_p04a": "bc_vuon_thuoc_hoi",
    "c1_p04b": "bc_vuon_thuoc_im",
    "c1_p05": "bc_quan_nuoc",
    "c1_p05b": "bc_khe_nui_dem",
    "c1_p05c": "bc_khe_nui_chon",
    "c1_p06": "bc_vuon_thuoc_ngoc",
    "c1_p06b": "bc_vuon_thuoc_dem",
    "c1_p07": "vt_ngoc_cot",
    "c1_p08": "nv_tuyet_co",
    "c1_p08b": "nv_tuyet_co_canh_giac",
    "c1_p09": "nv_tuyet_co_than_phan",
    "c1_p09b": "nv_tuyet_co_dieu_kien",
    "c1_p09c": "nv_tuyet_co_do_du",
    "c1_p10": "nv_tuyet_co_khe_uoc",
    "c1_p10b": "bc_tan_xa_song_tu",
    "c1_p11": "bc_tan_xa_dem",
    "c1_p11b": "bc_tan_xa_kho_tu",
    "c1_p11c": "bc_tan_xa_suyt_lo",
    "c1_p12": "bc_tan_xa_dot_pha",
    "c1_p13": "bc_dem_tap_kich",
    "c1_p14": "bc_cong_dong_doi_mat",
    "c1_p14b": "bc_cong_dong_giau",
    "c1_p14c": "bc_cong_dong_toan_luc",
    "c1_p14d": "bc_cong_dong_quyen",
    "c1_p14e": "bc_cong_dong_hung_ba",
    "c1_p15": "bc_hoa_truong_cuu",
    "c1_p16": "bc_mon_phai_tan_hoang",
    "c1_p17": "nv_han_lap_gap",
    "c1_p18a": "nv_han_lap_that",
    "c1_p18b": "nv_han_lap_cuoi_tru",
    "c1_p18c": "nv_han_lap_hoi_nguoc",
    "c1_p18d": "nv_han_lap_bau_nuoc",
    "c1_p19": "bc_binh_minh_ngoc_cot",
}

# Nhóm cảnh để duyệt trong Xưởng — theo mạch truyện, mỗi ảnh thuộc đúng một đoạn.
NHOM_CANH = [
    {"ma": "p-mo-dau", "phan": "c1-mon-phai", "ten": "Tân xá — thức giấc & ngày đầu",
     "mota": "Tân đệ tử choàng tỉnh; sân tập đông người; bị chèn ép.",
     "keys": ["bc_tan_xa_sang", "bc_san_tap_ngay", "bc_san_tap_chen_ep"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "p-san-sau", "phan": "c1-mon-phai", "ten": "Sân tập & sân sau — nhục nhã, luyện lén",
     "mota": "Cãi lại; luyện lén ban đêm; thấy ánh sáng lạ; chôn trả lại.",
     "keys": ["bc_san_sau_luyen_dem", "bc_san_tap_cai_lai",
              "bc_san_sau_anh_sang", "bc_san_sau_chon_lai"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "p-vuon-thuoc", "phan": "c1-mon-phai", "ten": "Vườn thuốc — Mạc Đại Phu",
     "mota": "Gặp Mạc Đại Phu; hỏi thẳng; im lặng; khối ngọc dưới luống cỏ.",
     "keys": ["bc_vuon_thuoc_gap", "bc_vuon_thuoc_hoi", "bc_vuon_thuoc_im",
              "bc_vuon_thuoc_ngoc", "bc_vuon_thuoc_dem"],
     "mau": ["nv_mac_dai_phu_mau", "nv_chinh_mau"]},
    {"ma": "p-quan-khe", "phan": "c1-mon-phai", "ten": "Quán nước & khe núi",
     "mota": "Dò tin nơi quán nước; lẻn ra khe núi; chôn trả lại.",
     "keys": ["bc_quan_nuoc", "bc_khe_nui_dem", "bc_khe_nui_chon"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "p-ngoc-hien", "phan": "c1-mon-phai", "ten": "Ngọc cốt — người trong ngọc",
     "mota": "Ngọc phát sáng trong đêm; người trong ngọc hiện ra; cảnh giác.",
     "keys": ["vt_ngoc_cot", "nv_tuyet_co", "nv_tuyet_co_canh_giac"],
     "mau": ["nv_tuyet_co", "nv_chinh_mau"]},
    {"ma": "p-tuyet-co", "phan": "c1-mon-phai", "ten": "Tuyết Cơ — thân phận & khế ước",
     "mota": "Nói thân phận; điều kiện; do dự; rồi ký khế ước.",
     "keys": ["nv_tuyet_co_than_phan", "nv_tuyet_co_dieu_kien",
              "nv_tuyet_co_do_du", "nv_tuyet_co_khe_uoc"],
     "mau": ["nv_tuyet_co", "nv_chinh_mau"]},
    {"ma": "p-tan-xa-tu", "phan": "c1-mon-phai", "ten": "Tân xá — song tu & khổ tu",
     "mota": "Song tu đêm đầu; tu luyện đêm đầu; khổ tu thất bại; suýt lộ; đột phá.",
     "keys": ["bc_tan_xa_song_tu", "bc_tan_xa_dem", "bc_tan_xa_kho_tu",
              "bc_tan_xa_suyt_lo", "bc_tan_xa_dot_pha"],
     "mau": ["nv_tuyet_co", "nv_chinh_mau"]},
    {"ma": "p-tap-kich", "phan": "c1-mon-phai", "ten": "Đêm tập kích",
     "mota": "Tù và vang, cổng đông bùng lửa.",
     "keys": ["bc_dem_tap_kich"], "mau": ["nv_chinh_mau"]},
    {"ma": "p-cong-dong", "phan": "c1-mon-phai", "ten": "Cổng đông — giao chiến",
     "mota": "Đối mặt địch; giấu thực lực; toàn lực; Thất Huyền quyền; gọi tên Hùng Bá.",
     "keys": ["bc_cong_dong_doi_mat", "bc_cong_dong_giau", "bc_cong_dong_toan_luc",
              "bc_cong_dong_quyen", "bc_cong_dong_hung_ba"],
     "mau": ["nv_chinh_mau", "nv_hung_ba_mau"]},
    {"ma": "p-hoa-truong", "phan": "c1-mon-phai", "ten": "Hỏa trường — cứu người",
     "mota": "Lao vào lửa cứu đệ tử nhỏ.",
     "keys": ["bc_hoa_truong_cuu"], "mau": ["nv_chinh_mau"]},
    {"ma": "p-sau-tran", "phan": "c1-mon-phai", "ten": "Sau trận — Mạc Đại Phu",
     "mota": "Thất Huyền Môn tổn thất; Mạc Đại Phu xách hòm thuốc cứu chữa.",
     "keys": ["bc_mon_phai_tan_hoang"], "mau": ["nv_mac_dai_phu_mau"]},
    {"ma": "p-han-lap", "phan": "c1-mon-phai", "ten": "Hàn Lập — sau hậu sơn",
     "mota": "Chạm mặt Hàn Lập: thành thật; cười trừ; hỏi ngược; bầu nước.",
     "keys": ["nv_han_lap_gap", "nv_han_lap_that", "nv_han_lap_cuoi_tru",
              "nv_han_lap_hoi_nguoc", "nv_han_lap_bau_nuoc"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "p-ket", "phan": "c1-mon-phai", "ten": "Kết chương — bình minh",
     "mota": "Bình minh đầu tiên; ngọc cốt khẽ ấm trong vạt áo.",
     "keys": ["bc_binh_minh_ngoc_cot"], "mau": []},
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


def doan_cua_anh() -> dict:
    """key -> [đoạn] (mỗi ảnh đúng một đoạn)."""
    return {k: [d] for d, k in DOAN_CUA_ANH.items()}
