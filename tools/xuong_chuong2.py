"""Cảnh riêng cho Chương 2 — Thái Nam Sơn Cốc (nhánh tán tu).

Quy tắc của dự án (tai-lieu/VIEC-CAN-LAM.md): "mỗi đoạn một cảnh riêng". Nhánh
tán tu của Chương 2 có 57 đoạn nhưng trước đây mượn ảnh Chương 1 ở nửa đầu và
KHÔNG có ảnh nào từ `c2_d11` trở đi — người chơi vào thung lũng là mất hình.

Module này khai đủ cảnh cho cả 57 đoạn. Mỗi cảnh gắn đúng MỘT đoạn bằng trường
`doan`; `doan_cua_anh()` suy ra ánh xạ từ chính danh sách này nên prompt và chỗ
dùng không thể lệch nhau.

tools_server.py nạp module này để mở rộng ASSETS / DOAN_CUA_ANH / NHOM_CANH.
"""

SCENES = [
    # ─ Đầu chương: Mạc phủ (dùng chung hai nhánh) ─
    {
        "key": "bc_mac_phu_tang",
        "name": "Mạc phủ — tang lễ trong sân",
        "doan": "c2_d06",
        "use": "Tang lễ Mạc Đại Phu: sân phủ treo vải trắng, khách khinh khỉnh (c2_d06).",
        "body": "The inner courtyard of a wealthy merchant manor in an ancient Chinese town, "
        "dressed for a funeral at grey morning light, seen at eye level. White hemp mourning "
        "cloth hangs in long strips from the eaves and across the gate, a plain coffin on trestles "
        "at the far side, a few mourners in coarse white standing with bowed heads. Near the gate "
        "a small cluster of well-dressed guests talk among themselves with cool indifferent faces. "
        "Wet flagstones, thin incense smoke, no bright colour anywhere. Composition keeps the upper "
        "third soft and empty for game text. Cold, formal, quietly contemptuous.",
    },
    # ─ Vào cốc: thung lũng hội và chợ linh thạch ─
    {
        "key": "bc_thai_nam_hoi",
        "name": "Thái Nam Sơn Cốc — thung lũng hội ban đêm",
        "doan": "c2_d11",
        "use": "Lần đầu tới Thái Nam Sơn Cốc: thung lũng đầy đèn lồng, người bay trên trời (c2_d11).",
        "body": "A wide mountain valley at dusk seen from a high ridge, an ancient Chinese cultivators' "
        "gathering filling the floor of the valley. Hundreds of small paper lanterns strung between "
        "tents and low halls glow warm orange in the blue dusk, cooking smoke and pale mist drift "
        "between them, and above the valley a handful of distant figures stand on flying swords, "
        "tiny and weightless against the sky. In the foreground a worn stone step and a thin pine. "
        "Composition keeps the upper sky calm and open for game text. Awe, hunger, a world far above.",
    },
    {
        "key": "bc_c2_cho_linh_thach",
        "name": "Chợ trong thung lũng — chiều",
        "doan": "c2_d12",
        "use": "Chợ tu sĩ trong thung lũng: hàng trăm lều, hàng bày trên vải, linh thạch (c2_d12).",
        "body": "Eye-level view down the floor of a vast mountain valley turned into a market of "
        "cultivators in an ancient Chinese fantasy world. Hundreds of low tents and cloth awnings in "
        "close rows, strings of small paper lanterns overhead, silent merchants sitting behind squares "
        "of cloth with their goods laid out: dull white spirit stones, jade scraps, stoppered clay "
        "bottles, rolled scrolls. A thin ragged youth in patched hemp walks between the rows, small in "
        "the frame. Warm lantern light against cold indigo dusk, low mist on the ground. Composition "
        "keeps the upper sky calm and empty for game text. Vast, hushed, quietly mercantile.",
    },
    {
        "key": "bc_c2_goc_hang_im",
        "name": "Chợ — hai người đổi linh thạch",
        "doan": "c2_d12b",
        "use": "Hai người nói khẽ, đổi linh thạch trên tấm vải — không ai rao giá (c2_d12b).",
        "body": "Close, low view inside a narrow aisle between market cloths in a mountain valley at "
        "dusk. Two merchants sit facing each other across a square of cloth laid on the ground, one "
        "pushing three small pale stones toward the other; only their hands and forearms are in frame, "
        "faces cropped above the mouth, robes plain and worn. A single lantern hangs at the edge of the "
        "frame, lighting the cloth and the stones. Composition keeps one side calm and empty for game "
        "text. Secretive, patient, businesslike.",
    },
    # ─ Gặp Hàn Lập bán di vật của Mạc Đại Phu ─
    {
        "key": "nv_c2_han_lap_ban_hang",
        "name": "Hàn Lập — ngồi bán di vật",
        "doan": "c2_d13",
        "use": "Hàn Lập ngồi sau tấm vải bán sách cũ, lọ thuốc, mảnh ngọc của Mạc Đại Phu (c2_d13).",
        "body": "Medium portrait of a thin young man of about seventeen in worn dark grey-blue robes, "
        "sitting cross-legged behind a small square of cloth on the ground, a shabby cloth bag beside "
        "him. On the cloth: a stained old book, five small clay medicine bottles, a chipped white jade "
        "shard. Lantern light from above, an evening market blurred behind him. His face is calm and "
        "closed, eyes lowered, giving nothing away. Background left soft and empty with pale ink wash "
        "for game text. Guarded, patient, unreadable.",
    },
    {
        "key": "vt_c2_manh_ngoc_to",
        "name": "Mảnh ngọc — soi lên nắng",
        "doan": "c2_d14a",
        "use": "Mảnh ngọc của Mạc Đại Phu soi lên nắng: một sợi chỉ sáng chạy trong lòng ngọc (c2_d14a).",
        "body": "Extreme close-up of a chipped white jade shard held between two fingers and lifted "
        "toward the low afternoon sun. The light passes through the stone and shows a single thread of "
        "pale light running end to end inside it, fine as silk. A blurred grey-blue sleeve at the edge "
        "of the frame, a dark market out of focus behind. Composition centred with generous bare paper "
        "around it. Precious, secret, quietly startling.",
    },
    {
        "key": "nv_c2_han_lap_goi_ngoc",
        "name": "Hàn Lập — gói ngọc rất nhanh",
        "doan": "c2_d14b",
        "use": "Hàn Lập nhận ba viên linh thạch, gói mảnh ngọc rất nhanh rồi cất sâu vào áo (c2_d14b).",
        "body": "Portrait of a thin young man in worn dark grey-blue robes, upper body, kneeling on the "
        "ground at an evening market, wrapping a small white jade shard in a scrap of old cloth with "
        "quick practised hands and tucking it deep inside his robe. Face lowered, jaw set, no "
        "expression. Lantern light from one side, blurred stalls behind him. Composition keeps one side "
        "calm and empty for game text. Fast, wary, self-protective.",
    },
    {
        "key": "bc_c2_lung_ao_vao_dam_dong",
        "name": "Hàn Lập — lưng áo khuất vào đám đông",
        "doan": "c2_d15_1",
        "use": "Hàn Lập đi vào đám đông, không quay lại; người chơi đứng nhìn (c2_d15_1).",
        "body": "Rear view of a thin young man in a worn robe with a faded cloth bag walking away "
        "between market rows into a loose crowd at dusk, his back small and straight, not looking back. "
        "Cloth awnings and lantern strings on both sides, packed stone ground, thin mist. In the "
        "foreground a ragged youth in patched hemp stands still, seen from behind. Composition keeps "
        "the upper part calm and open for game text. Lonely, unspoken, final.",
    },
    {
        "key": "bc_c2_di_qua_day_hang",
        "name": "Hai người — đi qua dãy hàng đang dọn",
        "doan": "c2_d15_0",
        "use": "Người chơi đi theo Hàn Lập qua dãy hàng đang dọn: nến, giấy bùa (c2_d15_0).",
        "body": "Eye-level view walking through rows of market stalls being packed up at evening: bolts "
        "of cloth folded, bundles of candles, stacks of yellow paper talismans, baskets of dried things "
        "that have no name. Two figures walk side by side, seen from behind and a step apart: one thin "
        "young man in worn grey-blue, one ragged youth in patched hemp. Warm lantern light, long "
        "shadows, dust in the air. Composition keeps the upper third calm and empty for game text. "
        "Companionable, quiet, watchful.",
    },
    # ─ Góc chợ tối: cuốn sách của Mạc Đại Phu ─
    {
        "key": "bc_c2_goc_cho_den_long",
        "name": "Góc chợ — đèn lồng thắp cùng lúc",
        "doan": "c2_d15",
        "use": "Đèn lồng thắp lên, hai người ngồi trên tảng đá; Hàn Lập mở cuốn sách ố (c2_d15).",
        "body": "A corner of a valley market at night, after the lanterns are lit all at once. Two "
        "figures sit on a flat stone between two rows of stalls already half packed, shoulder to "
        "shoulder, one of them holding an old stained book open on his knee. Hundreds of small lanterns "
        "recede into the dark behind them, warm ochre against deep indigo. Composition keeps the upper "
        "part calm and empty for game text. Intimate, still, suspended.",
    },
    {
        "key": "nv_c2_han_lap_ngang_dau",
        "name": "Hàn Lập — ngẩng đầu rất nhanh",
        "doan": "c2_d16a",
        "use": "Người chơi gọi đúng tên Trường Xuân Công; Hàn Lập ngẩng lên, mắt sắc lại (c2_d16a).",
        "body": "Close portrait of a thin young man in worn grey-blue robes, upper body, head lifted "
        "sharply from a book he has just shut, eyes narrow and bright, mouth still. Lantern light from "
        "one side carves his cheekbone; the night market is soft and dark behind him. Composition keeps "
        "one side calm and empty for game text. Alarmed, alert, reassessing.",
    },
    {
        "key": "bc_c2_goc_cho_trong",
        "name": "Góc chợ — hai người ngồi im",
        "doan": "c2_d17_1",
        "use": "Hai người ngồi im trong góc chợ; Hàn Lập đứng dậy nói 'đi thôi' (c2_d17_1).",
        "body": "Two figures sit in silence in the corner of a night market, both facing away from the "
        "viewer toward the dark, the last stalls closing down behind them. Most of the frame is empty "
        "dark valley and a few distant lanterns. Thin mist along the ground, a single low stone under "
        "them. Composition keeps the upper two thirds calm and empty for game text. Silent, heavy, held.",
    },
    {
        "key": "nv_c2_han_lap_noi_ve_mac",
        "name": "Hàn Lập — nói về Mạc Đại Phu",
        "doan": "c2_d17_0",
        "use": "Hàn Lập kể về Mạc Đại Phu: nuôi từ năm bảy tuổi, có một cái tên khác (c2_d17_0).",
        "body": "Portrait of a thin young man sitting on a stone at night, upper body, an old book "
        "closed in his lap, looking down and slightly aside, his face quiet and carefully flat. A "
        "flicker of something tired sits behind the eyes. Lantern light low from one side; behind him "
        "the dark of the valley and one distant lantern. Composition keeps one side calm and empty for "
        "game text. Confiding, reluctant, afraid.",
    },
    {
        "key": "nv_c2_han_lap_doc_sach",
        "name": "Hàn Lập — đọc sách bên đèn",
        "doan": "c2_d16b",
        "use": "Hàn Lập đọc thêm mấy dòng rồi gấp sách; nhận xét người chơi im quá lâu (c2_d16b).",
        "body": "Portrait of a thin young man reading by lantern light, upper body, the book held open "
        "and tilted toward the flame, brow slightly drawn, lips still. Half his face is in shadow. "
        "Behind him a dark market row and one hanging lantern. Composition keeps the dark side calm and "
        "empty for game text. Absorbed, guarded, alone.",
    },
    # ─ Đêm đầu: kiếm linh dạy hít hồng trần ─
    {
        "key": "bc_c2_go_da_dem",
        "name": "Gờ đá — đêm, kiếm linh dạy bài đầu",
        "doan": "c2_d17",
        "use": "Đêm đầu ngoài gờ đá: kiếm linh dạy hít hồng trần, hai kiếm ngang đùi (c2_d17).",
        "body": "Night at the rim of a mountain valley. A ragged youth sits cross-legged under a low "
        "ledge of rock, two long swords laid across his thighs, faint pale mist gathering at his open "
        "palms; a translucent white-robed sword spirit stands a few steps away, half dissolved into the "
        "dark, one hand raised. Far behind them, sparse lanterns of the market and cold stars. "
        "Composition keeps the upper area dark and calm for game text. Cold, intent, austere.",
    },
    {
        "key": "nv_c2_dung_som",
        "name": "Người chơi — dừng sớm, tay run",
        "doan": "c2_d18_1",
        "use": "Dẫn hồng trần tới đau thì thả ra; ngồi thở, tay run, chọn không chết đêm nay (c2_d18_1).",
        "body": "Close view of a ragged young man sitting under a rock ledge at night, one hand lifted "
        "away from his own chest, fingers trembling, face pale with sweat, eyes open and breathing "
        "hard. Two swords lie across his knees. Cold blue night light, a band of pale mist braided "
        "across the ground. Composition keeps one side calm and empty for game text. Shaken, careful, "
        "alive.",
    },
    {
        "key": "nv_c2_di_qua_gioi_han",
        "name": "Người chơi — đi quá giới hạn một nhịp",
        "doan": "c2_d18_0",
        "use": "Vẫn dẫn thêm một nhịp, đau tới mức mắt tối lại, rồi dịu xuống (c2_d18_0).",
        "body": "Close view of a ragged young man under a rock ledge at night, jaw clenched, eyes shut "
        "and dark-rimmed, a thin line of pale mist drawn from his palms down into his lower belly, the "
        "mist bright and edged like a blade. The swords rest at his knees. Cold night, deep shadow. "
        "Composition keeps the upper part dark and calm for game text. Driven, pained, past the limit.",
    },
    # ─ Vạn Tiểu Sơn: một câu hỏi đổi một viên linh thạch ─
    {
        "key": "nv_c2_van_tieu_son",
        "name": "Vạn Tiểu Sơn — bục đá, cây gậy",
        "doan": "c2_d18",
        "use": "Vạn Tiểu Sơn đứng trên bục đá: 'hạ phẩm đổi một câu hỏi' (c2_d18).",
        "body": "Medium portrait of an old wandering cultivator of an ancient Chinese fantasy world, "
        "standing on a low stone platform in a crowded valley at early morning. Very old, white hair "
        "bound tight, long grey robe, a smooth worn wooden staff in one hand. Thin mouth, narrow bright "
        "eyes, entirely unimpressed, chin slightly raised. Behind him a loose crowd of ragged youths, "
        "out of focus. Composition keeps one side calm and empty for game text. Arrogant, lucid, "
        "amused.",
    },
    {
        "key": "bc_c2_buc_da_dat_thach",
        "name": "Bục đá — đặt viên linh thạch cuối",
        "doan": "c2_d19",
        "use": "Người chơi đặt viên linh thạch cuối lên bục; đám đông im bặt (c2_d19).",
        "body": "A low stone platform in a mountain valley at morning. A single small dull-white spirit "
        "stone lies on the stone with a ragged youth's hand just withdrawing from it; the old man with "
        "the wooden staff stands above, looking down. A dense ring of ragged listeners surrounds the "
        "platform, seen from behind at a distance. Hard clear morning light, dust in the air, mist on "
        "the far ridge. Composition keeps the upper part calm and empty for game text. Public, quiet, "
        "decisive.",
    },
    {
        "key": "bc_c2_lui_khoi_dam_dong",
        "name": "Lùi khỏi đám đông — không hỏi thêm",
        "doan": "c2_d20_1",
        "use": "Người chơi cúi đầu, lùi lại; đám đông khép lại như nước khép trên đá (c2_d20_1).",
        "body": "A ragged youth with his head bowed steps back from a stone platform as the crowd of "
        "ragged cultivators closes in front of him like water closing over a stone: many backs and "
        "shoulders fill the middle of the frame, the platform and the old man barely visible beyond. "
        "Morning light, dust hanging in the air. Composition keeps the upper part calm and empty for "
        "game text. Small, swallowed, prudent.",
    },
    {
        "key": "bc_c2_bong_ao_xam_quay_di",
        "name": "Rìa đám đông — bóng áo xám quay đi",
        "doan": "c2_d20_0",
        "use": "Vạn Tiểu Sơn nói kẻ giữ tấm lệnh thứ hai đang đứng đây; một bóng áo xám quay đi (c2_d20_0).",
        "body": "View across a crowd in a mountain valley at morning: hundreds of ragged figures "
        "standing shoulder to shoulder, and at the far edge of the crowd a single figure in a faded "
        "grey robe turning away, face hidden, already half lost between two tents. Several heads in the "
        "crowd turn slightly toward him. Composition keeps the sky calm and empty for game text. "
        "Suspicious, unseen, dangerous.",
    },
    {
        "key": "bc_c2_nghe_ben_le",
        "name": "Nghe lén — mười bảy câu hỏi",
        "doan": "c2_d19b",
        "use": "Người chơi đứng ngoài nghe Vạn Tiểu Sơn trả lời mười bảy câu, học về phẩm linh thạch (c2_d19b).",
        "body": "A ragged young man stands at the edge of a listening crowd in a mountain valley, arms "
        "folded, half hidden behind the shoulders of others, eyes fixed on a low stone platform beyond. "
        "Morning light, thin mist, tents and banners around, dust underfoot. Composition keeps the upper "
        "part calm and empty for game text. Attentive, patient, hungry.",
    },
    # ─ Trả giá thuốc ở dãy hàng phía bắc ─
    {
        "key": "nv_c2_ba_can_thuoc",
        "name": "Bà bán đan — cái cân nhỏ",
        "doan": "c2_d20",
        "use": "Bà bán đan trả ba viên cho thuốc của Mạc Đại Phu; biết Hàn Lập đang cần tiền (c2_d20).",
        "body": "Portrait of a middle-aged woman with a cold flat face standing behind a cloth counter "
        "at a day market, upper body. Dark hair pulled back, plain brown robe, a small brass balance "
        "scale held in one hand, rows of small clay medicine bottles in front of her. Her expression is "
        "bored and knowing. Behind her a wall of cloth awnings. Composition keeps one side calm and "
        "empty for game text. Hard, dismissive, shrewd.",
    },
    {
        "key": "nv_c2_han_lap_vai_ha",
        "name": "Hàn Lập — vai hạ xuống",
        "doan": "c2_d21_3",
        "use": "Người chơi nói thật lý do đi theo; vai Hàn Lập hạ xuống một chút (c2_d21_3).",
        "body": "Portrait of a thin young man in worn grey-blue robes at a market counter at midday, "
        "upper body, half turned away from the viewer, one hand paused above a row of clay medicine "
        "bottles, his shoulder just lowering as tension leaves it. Only jaw and cheek are visible. Hard "
        "flat midday light, cloth awnings behind. Composition keeps one side calm and empty for game "
        "text. Relenting, tired, honest.",
    },
    {
        "key": "bc_c2_quay_thuoc",
        "name": "Đứng nhìn — ba bước sau lưng",
        "doan": "c2_d21_2",
        "use": "Người chơi đứng ba bước, không nói; Hàn Lập nhận ba viên rồi đi (c2_d21_2).",
        "body": "A ragged youth stands three steps back from a cloth counter, arms at his sides, "
        "watching without speaking; beyond him a thin young man in grey-blue ties three clay bottles "
        "into a cloth and turns to go. Midday market, hard light, dust, other stalls receding into the "
        "frame. Composition keeps the upper part calm and empty for game text. Distant, patient, a "
        "little hurt.",
    },
    {
        "key": "nv_c2_han_lap_cuoi_kho",
        "name": "Hàn Lập — tiếng cười khô đầu tiên",
        "doan": "c2_d21_1",
        "use": "Người chơi nói 'ta ghét bị trả giá'; Hàn Lập cười một tiếng khô (c2_d21_1).",
        "body": "Close portrait of a thin young man in worn grey-blue robes at a market counter, upper "
        "body, caught in a short dry laugh: the corner of the mouth pulled, eyes narrowed, no warmth in "
        "it but no cruelty either — the first time his face has moved. Midday light from one side, "
        "blurred awnings behind. Composition keeps one side calm and empty for game text. Dry, "
        "surprised, human.",
    },
    {
        "key": "nv_c2_han_lap_quay_lai",
        "name": "Hàn Lập — quay hẳn lại nhìn",
        "doan": "c2_d21_0",
        "use": "Người chơi nói 'ta cũng cần một người hiểu ta'; Hàn Lập quay hẳn lại (c2_d21_0).",
        "body": "Portrait of a thin young man turned fully toward the viewer, upper body, looking "
        "straight out with an unreadable steady gaze, a packet of medicine held in one hand. Midday "
        "market light, cloth awnings soft behind him. Composition keeps one side calm and empty for "
        "game text. Seen, weighing, quiet.",
    },
    # ─ Ba kẻ áo xám theo dõi ─
    {
        "key": "bc_c2_ba_bong_ao_xam",
        "name": "Ba bóng áo xám — rải giữa chợ",
        "doan": "c2_d21",
        "use": "Hàn Lập cảnh báo ba kẻ áo xám theo người chơi từ dãy đông (c2_d21).",
        "body": "Wide afternoon view across a mountain valley market: three figures in faded grey robes "
        "stand far apart between the stalls, each turned slightly toward the same direction, waiting. In "
        "the foreground a ragged youth and a thin young man in grey-blue stand close together and talk, "
        "unaware in the frame. Long afternoon shadows, dust, thinning crowds. Composition keeps the "
        "upper part calm and empty for game text. Watched, tense, patient.",
    },
    # ─ Khe đá: một canh giờ bàn tay trên vai ─
    {
        "key": "bc_c2_khe_da_sat_vach",
        "name": "Khe đá — hai người ép sát vách",
        "doan": "c2_d22",
        "use": "Hai người ép sát vách khe đá; tiếng chân chạy qua ngoài khe (c2_d22).",
        "body": "Interior of a narrow rock crevice at night: two figures pressed close against the "
        "stone wall, only their shoulders and one hand laid on a shoulder visible in the dark, a thin "
        "blade of moonlight entering through the crack. Outside the crevice, a dark slope and cold mist. "
        "Composition keeps the upper part dark and calm for game text. Cramped, hushed, held breath.",
    },
    {
        "key": "nv_c2_nua_mat_trong_toi",
        "name": "Hàn Lập — nửa mặt trong bóng tối",
        "doan": "c2_d23_2",
        "use": "'Ta sẽ không để ngươi chết một mình' — nửa mặt Hàn Lập trong tối (c2_d23_2).",
        "body": "Close view in near darkness: half of a thin young man's face lit by a thin line of "
        "moonlight, one eye and the line of the jaw visible, his expression set and strange. The rest of "
        "the frame is black rock. Composition keeps one side deep dark and calm for game text. "
        "Unreadable, close, painful.",
    },
    {
        "key": "bc_c2_khe_da_lanh",
        "name": "Khe đá — hai người ngồi cách một gang tay",
        "doan": "c2_d23_1",
        "use": "'Ta không cần ngươi hiểu ta' — hai người ngồi im, cách nhau một gang tay (c2_d23_1).",
        "body": "Two figures sit apart inside a rock crevice at night, both facing forward, a hand's "
        "width of stone between them, cold blue moonlight falling between the walls. Neither looks at "
        "the other. Composition keeps the upper part dark and calm for game text. Cold, proud, wounded.",
    },
    {
        "key": "bc_c2_khe_da_tho_ra",
        "name": "Khe đá — một hơi thở dài",
        "doan": "c2_d23_0",
        "use": "'Cùng nhau ra khỏi đây' — Hàn Lập thở ra một hơi dài rồi đáp 'được' (c2_d23_0).",
        "body": "The same rock crevice at night, seen from the mouth: one figure leaning back against "
        "the stone with his head tipped back, chest fallen in a long exhale, the other sitting forward. "
        "Thin moonlight, deep shadow, a sliver of the valley beyond. Composition keeps the upper part "
        "dark and calm for game text. Released, decided, quiet.",
    },
    {
        "key": "bc_c2_khe_da_gan_sang",
        "name": "Khe đá — gần sáng, trời xám",
        "doan": "c2_d23",
        "use": "'Vì ngươi không giống những kẻ khác' — trời bắt đầu xám (c2_d23).",
        "body": "The mouth of a rock crevice before dawn: grey light on the stone, mist on the ground, "
        "two figures sitting side by side, one looking toward the grey sky. A faint translucent "
        "white-robed sword spirit is implied only as a wisp of pale mist at the edge of the frame. "
        "Composition keeps the upper part calm and empty for game text. Ending, still, a beginning.",
    },
    # ─ Nhánh tự lo: một mình dưới gờ đá ─
    {
        "key": "bc_c2_go_da_mot_minh",
        "name": "Gờ đá — một mình, ba kẻ tới gần sáng",
        "doan": "c2_d22b",
        "use": "Người chơi tự lo: ngồi một mình dưới gờ đá, ba kẻ áo xám tới gần sáng (c2_d22b).",
        "body": "Night at the rim of a mountain valley: a single ragged youth sits alone under a low "
        "ledge of rock with two long swords across his knees, another person's sleeping place a few "
        "steps away, cold and unused. Three dim figures in grey approach far off between the tents. "
        "Composition keeps the upper part dark and calm for game text. Alone, braced, resigned.",
    },
    # ─ Giao dịch với kẻ áo xám thêu chỉ bạc ─
    {
        "key": "bc_c2_giao_dich_ao_xam",
        "name": "Giao dịch — áo xám thêu chỉ bạc",
        "doan": "c2_d23b",
        "use": "Hàn Lập đưa cho kẻ áo xám thêu chỉ bạc một thứ, người chơi đứng từ xa nhìn (c2_d23b).",
        "body": "Daylight in a mountain valley market: two figures stand face to face between closed "
        "stalls, one a thin young man in worn grey-blue, the other a grey-robed man with silver thread "
        "stitched at his cuffs, standing very straight as if holding office. Something small passes "
        "between their hands. Both faces are turned away from the viewer. Pale morning light, dust, "
        "hanging cloth. Composition keeps one side calm and empty for game text. Furtive, official, "
        "dangerous.",
    },
    {
        "key": "nv_c2_han_lap_giac_minh",
        "name": "Hàn Lập — giật mình quay lại",
        "doan": "c2_d24b_1",
        "use": "Người chơi bước tới hỏi 'ngươi đưa hắn cái gì'; Hàn Lập giật mình (c2_d24b_1).",
        "body": "Close portrait of a thin young man spun half around, upper body, caught off guard: "
        "eyes wide for one instant, mouth slightly open, the calm broken. A daylight market behind him, "
        "out of focus. Composition keeps one side calm and empty for game text. Startled, exposed, "
        "swift to recover.",
    },
    {
        "key": "bc_c2_quay_lung_muoi_buoc",
        "name": "Bỏ đi — mười bước, không quay lại",
        "doan": "c2_d24b_0",
        "use": "Người chơi bỏ đi mười bước, không quay lại nhìn (c2_d24b_0).",
        "body": "Rear view of a ragged youth walking away alone down a market row, ten paces off, "
        "shoulders square, not looking back; the thin young man in grey-blue stands behind him, small in "
        "the distance, watching. Daylight, dust, rows of stalls on both sides. Composition keeps the "
        "upper part calm and empty for game text. Deliberate, sore, chosen.",
    },
    # ─ Bà lão đo linh căn ─
    {
        "key": "nv_do_linh_can",
        "name": "Bà lão đo linh căn",
        "doan": "c2_d23c",
        "use": "Bà lão cầm viên đá đo linh căn, viên đá sáng trắng: thiên linh căn (c2_d23c).",
        "body": "Close portrait of an old woman of an ancient Chinese fantasy world, upper body only, "
        "facing the viewer at a slight angle. A dried, weathered face with deep lines and narrow "
        "unimpressed eyes, grey hair pulled back in a plain bun with a wooden pin, a dull grey robe "
        "with a worn collar. In her raised hand she holds a smooth egg-shaped stone that glows a soft "
        "cold white, its light falling on her fingers and cheek. Behind her a blurred crowd of ragged "
        "youths in the dusk. Background left almost empty with soft ink wash so game text can sit "
        "beside. Weary, indifferent, faintly surprised.",
    },
    # ─ Tà tu phong toả cốc ─
    {
        "key": "bc_c2_cho_don_hang",
        "name": "Chợ dọn hàng — tà tu phong toả",
        "doan": "c2_d24b",
        "use": "Sáng ngày cuối: chợ dọn gấp, khói bốc phía đông, tà tu phong toả cốc (c2_d24b).",
        "body": "A mountain valley market on its last morning, being taken down fast: cloths folded, "
        "tents dropped, carts loaded, everyone moving in tight groups of three or four. Smoke rises "
        "from the eastern edge of the valley in a low column. Cold flat light, dust, a sense of hurry in "
        "every figure. Composition keeps the upper part calm and empty for game text. Uneasy, hurried, "
        "closed.",
    },
    # ─ Bình men xanh ─
    {
        "key": "vt_c2_binh_men_xanh",
        "name": "Bình men xanh — sứt một miếng",
        "doan": "c2_d25",
        "use": "Hàn Lập đặt cái bình men xanh nhặt ở Thất Huyền Môn lên tảng đá (c2_d25).",
        "body": "Close still-life on a flat rock inside a rock crevice at dusk: a small ceramic bottle "
        "the height of two finger joints, glazed deep green-blue, one chip missing from the rim, "
        "standing beside a worn wooden chest. Faint cool light on the glaze, dust, a fold of grey cloth. "
        "Composition centred with bare paper around it. Ordinary, old, and not ordinary at all.",
    },
    {
        "key": "nv_c2_han_lap_goi_binh",
        "name": "Hàn Lập — gói bình rất chậm",
        "doan": "c2_d26_2",
        "use": "'Giấu nó đi' — Hàn Lập gói cái bình vào vải, rất chậm, cất sâu vào áo (c2_d26_2).",
        "body": "The thin young man in grey-blue sits in a rock crevice at dusk, wrapping a small "
        "green-blue bottle in a scrap of cloth very slowly, both hands in frame, face lowered and "
        "intent. Stone walls, cold half-light, dust on the rock. Composition keeps one side calm and "
        "empty for game text. Careful, secretive, decided.",
    },
    {
        "key": "nv_c2_han_lap_cam_binh",
        "name": "Hàn Lập — cầm bình, xoay một vòng",
        "doan": "c2_d26_1",
        "use": "'Ta không đọc được vật' — Hàn Lập cầm bình xoay một vòng, nói 'sợ' (c2_d26_1).",
        "body": "Portrait of a thin young man holding a small chipped green-blue bottle up between his "
        "fingers, upper body, turning it slowly, his face flat and steady. Dusk light in a rock "
        "crevice, deep shadow behind him. Composition keeps one side calm and empty for game text. "
        "Afraid and unafraid at the same time.",
    },
    {
        "key": "vt_c2_binh_tren_da",
        "name": "Bình trên tảng đá — tay vừa rút lại",
        "doan": "c2_d26_0",
        "use": "Kiếm linh bảo cất bình đi; cái bình vẫn nằm trên tảng đá, men xanh, sứt miếng (c2_d26_0).",
        "body": "Close view of a small chipped green-blue ceramic bottle standing alone on a flat "
        "stone, a hand just withdrawn from it at the edge of the frame; deep shadow around, a thin band "
        "of last daylight across the stone. Composition centred with generous empty paper around it. "
        "Waiting, sealed, wrong.",
    },
    # ─ Nấp trong hốc đá ─
    {
        "key": "bc_c2_hoc_da_phia_tay",
        "name": "Hốc đá phía tây — nằm im nghe",
        "doan": "c2_d25b",
        "use": "Nấp trong hốc đá phía tây, khe hở nhìn ra thung lũng, nghe một người chết (c2_d25b).",
        "body": "Inside a narrow hollow under a western rock shelf at dusk, seen from within: a ragged "
        "youth lies flat with two swords crossed over his chest, a slit of open sky and the far valley "
        "visible through a crack, smoke drifting past. Composition keeps the upper part dark and calm "
        "for game text. Hidden, listening, afraid.",
    },
    {
        "key": "vt_c2_binh_khong_phang",
        "name": "Bình men xanh — không phản chiếu lửa",
        "doan": "c2_d26",
        "use": "Đêm trong khe đá: cái bình không phản chiếu ánh lửa như mọi thứ khác (c2_d26).",
        "body": "Night in a rock crevice: a small chipped green-blue bottle stands on a stone in front "
        "of a low fire, and though everything around it is warm-lit, the glaze of the bottle reflects "
        "nothing at all — a flat dead green. Two figures sit in shadow behind, out of focus. Composition "
        "centred with dark calm space around it. Still, cold, unnatural.",
    },
    # ─ Xác người trong khói ─
    {
        "key": "bc_c2_nam_trong_khe",
        "name": "Nằm trong khe — đếm từng nhịp thở",
        "doan": "c2_d27_1",
        "use": "Nằm im trong khe, nghe tiếng chân, tiếng rên; Hàn Lập đứng dậy trước (c2_d27_1).",
        "body": "Inside a rock crevice at night: a ragged youth lies on his side, eyes open, counting "
        "breaths, one hand flat on the stone; beyond the crevice mouth a dark slope with a fallen shape "
        "dimly visible and dust hanging in the air. Composition keeps the upper part dark and calm for "
        "game text. Frozen, counting, waiting.",
    },
    {
        "key": "bc_c2_xac_trong_khoi",
        "name": "Bò ra khỏi khe — xác cách mười bước",
        "doan": "c2_d27_0",
        "use": "Người chơi bò ra trước, thấy xác người cách mười bước; Hàn Lập quỳ xuống (c2_d27_0).",
        "body": "Thick smoke at the mouth of a rock crevice at dusk: a ragged youth crawls out low on "
        "hands and knees, and ten paces away on the rock lies a body in a faded grey robe. Another "
        "figure kneels beside the body. Smoke curls through the whole frame, dim orange light from a "
        "distant fire. Composition keeps the upper part hazy and calm for game text. Choking, grim, "
        "quiet.",
    },
    {
        "key": "bc_c2_xac_ao_xam",
        "name": "Xác áo xám — Hàn Lập lục túi",
        "doan": "c2_d27",
        "use": "Xác Kim Quang Thượng Nhân, áo xám bạc màu; Hàn Lập quỳ lục túi trữ vật (c2_d27).",
        "body": "A body lies face down on flat rock at dusk, in a faded grey robe gone pale, a dark "
        "stain spreading from shoulder to hip, one hand still half curled. A thin young man kneels "
        "beside it, one arm thrust beneath the body, his face unreadable. Cold dusk light, smoke, bare "
        "rock. Composition keeps the upper part calm and empty for game text. Clinical, terrible, "
        "practised.",
    },
    # ─ Sau khi Hàn Lập lục túi xác ─
    {
        "key": "bc_c2_han_lap_di_ve_ria",
        "name": "'Ngươi là kẻ giết người' — hắn đi về rìa",
        "doan": "c2_d28_3",
        "use": "Người chơi buộc tội; Hàn Lập đáp 'ừ' rồi đi về phía rìa thung lũng (c2_d28_3).",
        "body": "Dusk on a rock shelf: a thin young man in a faded grey-blue robe walks away toward the "
        "dark rim of a valley, a small grey cloth bag in his hand, his back to the viewer. A ragged "
        "youth stands still in the foreground, watching him go. Smoke and low fire glow at the valley "
        "edge. Composition keeps the upper part calm and empty for game text. Accusing, unapologetic, "
        "alone.",
    },
    {
        "key": "bc_c2_di_ben_nhau",
        "name": "Đi bên nhau — không đi sau",
        "doan": "c2_d28_2",
        "use": "'Vậy thì ta đi cùng ngươi' — hai người đi ngang nhau, không ai đi sau (c2_d28_2).",
        "body": "Two figures walk side by side across a dark valley floor at dusk, shoulder to "
        "shoulder, not one behind the other: a thin young man in faded grey-blue and a ragged youth in "
        "patched hemp. Low fires burn at the edges of the market behind them, mist on the ground. "
        "Composition keeps the upper part calm and empty for game text. Equal, quiet, chosen.",
    },
    {
        "key": "bc_c2_vai_cham_vai",
        "name": "Vai chạm vai — rất nhẹ",
        "doan": "c2_d28_1",
        "use": "Hàn Lập đi ngang, vai khẽ chạm vai người chơi — có thể là vô tình (c2_d28_1).",
        "body": "Close view at dusk on bare rock: the shoulder of one figure just touching the shoulder "
        "of another as he passes, a small grey cloth bag held in one hand. Faces above the shoulder line "
        "are out of frame or in shadow. Cold light, thin smoke. Composition keeps one side calm and "
        "empty for game text. Accidental, or not, and unspoken.",
    },
    {
        "key": "bc_c2_ban_tay_nam_ho",
        "name": "Bàn tay người chết — còn nắm hờ",
        "doan": "c2_d28_0",
        "use": "Bàn tay người chết còn nắm hờ như vừa định rút kiếm; Hàn Lập nhét túi vải vào áo (c2_d28_0).",
        "body": "Close view low to the ground at dusk: the hand of a dead man in a faded grey sleeve, "
        "fingers still half curled as if reaching for a sword hilt, a dark stain on the stone beside it. "
        "A thin young man's hand withdraws a small grey cloth bag from beneath the body. Composition "
        "keeps the upper part calm and empty for game text. Cold, exact, merciless.",
    },
    # ─ Rời cốc: tấm Thăng Tiên Lệnh ─
    {
        "key": "bc_c2_ra_coc_dem",
        "name": "Ra khỏi cốc — đêm, lửa còn ở rìa",
        "doan": "c2_d28",
        "use": "Hai người ra khỏi cốc lúc trời tối hẳn; Hàn Lập đưa một tấm lệnh (c2_d28).",
        "body": "Two figures leave a mountain valley at full night: small fires still burning in "
        "scattered patches behind them at the edges of the abandoned market, a dark ridge ahead, stars "
        "above. One figure has stopped at the mouth of a gorge and looks back, a thin token held out in "
        "his hand toward the other. Composition keeps the sky calm and open for game text. Ending, "
        "offer, ash.",
    },
    {
        "key": "vt_c2_thang_tien_lenh",
        "name": "Thăng Tiên Lệnh — trong lòng bàn tay",
        "doan": "c2_d29_0",
        "use": "Người chơi cầm tấm lệnh: miếng kim loại mỏng, lạnh, khắc hình một cánh cổng (c2_d29_0).",
        "body": "Extreme close-up of a thin metal token lying in an open palm: a flat slip of dark "
        "metal, cold, engraved with the shape of a gate or archway, its edge worn smooth. The fingers "
        "curl around it, a fold of patched hemp sleeve at the wrist. Faint dawn light. Composition "
        "centred with bare paper around it. Light, heavy, a door.",
    },
    {
        "key": "bc_c2_day_lenh_lai",
        "name": "Đẩy tấm lệnh lại — hai ngón tay",
        "doan": "c2_d29_1",
        "use": "Người chơi đẩy tấm lệnh lại: 'giữ đủ ba tấm, ngươi cần cả ba hơn ta' (c2_d29_1).",
        "body": "Two figures stand face to face at night at the mouth of a mountain gorge: one thin "
        "young man in faded grey-blue holds out a metal token; the other, a ragged youth, pushes it back "
        "with two fingers. Behind them the last small fires of the valley. Composition keeps the upper "
        "part calm and empty for game text. Refusal, respect, no debt.",
    },
    # ─ Chia tay ở chân núi ─
    {
        "key": "bc_c2_chan_nui_chia_tay",
        "name": "Chân núi — gần sáng, chia tay",
        "doan": "c2_d29",
        "use": "Chia tay ở chân núi: Thái Nam Cốc sau lưng im, hai thanh kiếm ấm trong tay (c2_d29).",
        "body": "Before dawn at the foot of a mountain: two figures stand apart on a stony path, one "
        "facing south, one facing north, the empty valley behind them silent with no fires left, only "
        "mist. The ragged youth holds two long swords, their blades catching a faint warmth. "
        "Composition keeps the upper part calm and open for game text. Parted, resolved, brief.",
    },
    {
        "key": "bc_c2_khong_ngoai_lai",
        "name": "'Mỗi người đi đường mình' — không ngoái lại",
        "doan": "c2_d29x",
        "use": "Người chơi cắt dây: 'ta không cần ngươi'; Hàn Lập quay đi, không ngoái lại (c2_d29x).",
        "body": "A thin young man walks away down a stony path at first light, his back to the viewer, "
        "no greeting and no glance, one hand loose at his side. A ragged youth stands still behind him "
        "in the foreground. Barren slope, low mist. Composition keeps the upper part calm and empty for "
        "game text. Final, cold, a cut thread.",
    },
    {
        "key": "bc_c2_duong_mon_phia_bac",
        "name": "Đường mòn phía bắc — một mình",
        "doan": "c2_d27b",
        "use": "Người chơi ra khỏi cốc bằng đường mòn phía bắc, một mình; cốc cháy tới sáng (c2_d27b).",
        "body": "A single ragged youth climbs a narrow north mountain path before dawn, two long swords "
        "in his hands, the burning valley far below and behind him, small fires still visible through "
        "smoke. Cold grey sky, bare rock, mist in the folds of the ground. Composition keeps the upper "
        "part calm and open for game text. Alone, upward, unrepentant.",
    },
    # ─ Ba kẻ áo xám đêm: ba cách đánh (tán tu) ─
    {
        "key": "bc_c2_ba_ke_ao_xam_dem",
        "name": "Ba kẻ áo xám — chặn giữa đường đêm",
        "doan": "c2_d22c_0",
        "use": "Ba kẻ áo xám chặn người chơi giữa đường đêm, chưa rút vũ khí (c2_d22c_0).",
        "body": "Night on a narrow mountain path: three men in coarse grey robes stand across the way, "
        "spaced apart, faces half in shadow, hands empty and loose at their sides. Behind them a dark "
        "slope and low mist; a thin cold moonlight from one side. A ragged youth stands facing them, "
        "small and tense. Composition keeps the upper part dark and calm for game text. Outnumbered, "
        "quiet, about to turn violent.",
    },
    {
        "key": "bc_c2_da_lenh_dem",
        "name": "Đá lệch hướng — né rồi chạy",
        "doan": "c2_d22c_1",
        "use": "Người chơi ném đá lệch hướng rồi chạy; ba kẻ áo xám quay đầu theo tiếng (c2_d22c_1).",
        "body": "Night on a rocky slope, seen low and wide: a small stone still in the air above the "
        "rocks, three grey-robed figures turning their heads toward the sound, one already stepping "
        "that way. In the near foreground the back of a ragged youth slipping between two boulders. "
        "Cold moonlight, long shadows, dust in the air. Composition keeps the upper part calm and dark "
        "for game text. Quick, clever, barely breathing.",
    },
    {
        "key": "bc_c2_khe_da_danh_vo",
        "name": "Khe đá hẹp — đánh vào chỗ hở rồi lách",
        "doan": "c2_d22c_2",
        "use": "Người chơi lách vào khe hẹp, đánh vào đầu gối kẻ thứ nhất rồi chen qua (c2_d22c_2).",
        "body": "Inside a narrow rock crevice at night: one grey-robed man bent forward, clutching a "
        "knee, his face twisted; a ragged youth squeezing past him through a gap too narrow for two. "
        "Two more grey figures behind, blocked by the first. Thin silver light from the crack above, "
        "grey stone close on both sides. Composition keeps the upper part dark and calm for game text. "
        "Cramped, violent, escaping.",
    },
    {
        "key": "bc_c2_ba_ke_bo_di",
        "name": "Ba kẻ áo xám bỏ đi — không ai đuổi",
        "doan": "c2_d22c_3",
        "use": "Người chơi chỉ tay về phía bắc nói hắn đi lối đó; ba kẻ áo xám bỏ đi (c2_d22c_3).",
        "body": "Night on a mountain path: three grey-robed men walking away down a slope, seen from "
        "behind, one glancing back over his shoulder. In the foreground a ragged youth stands still, "
        "one arm half raised as if he has just pointed. Cold moonlight, mist between rocks. Composition "
        "keeps the upper part calm and empty for game text. A lie told well, and the cost of it still to come.",
    },
    # ─ Tà tu bị thương ở miệng khe (tán tu) ─
    {
        "key": "bc_c2_ta_tu_bi_thuong",
        "name": "Tà tu bị thương — ngồi dựa vách khe",
        "doan": "c2_d25c_0",
        "use": "Tà tu bị thương nặng ngồi dựa vách khe, thở dốc, kiếm gãy bên cạnh (c2_d25c_0).",
        "body": "Inside a rock crevice at dusk: a man in a torn dark robe sits slumped against the stone "
        "wall, one hand pressed to a wound at his side, breath shallow, a broken sword on the ground "
        "beside him. His robe has a faded sect mark. Dust, cold grey light from the crevice mouth. "
        "Composition keeps the upper part dark and calm for game text. Dangerous even now, and dying.",
    },
    {
        "key": "bc_c2_ta_tu_cheo_mieng_khe",
        "name": "Tà tu lết tới miệng khe",
        "doan": "c2_d25c_1",
        "use": "Tà tu lết tới miệng khe, để lại vệt máu trên đá (c2_d25c_1).",
        "body": "A rock crevice at dusk seen from inside: a dark-robed man dragging himself toward the "
        "bright mouth of the crevice, one hand over his side, a wet smear of blood left along the grey "
        "stone behind him. A ragged youth stands further back in shadow, watching him go. Cold light, "
        "dust. Composition keeps the upper part calm and empty for game text. Pity and caution at once.",
    },
    {
        "key": "bc_c2_lay_kiem_ta_tu",
        "name": "Lấy kiếm của tà tu — tra vào vỏ",
        "doan": "c2_d25c_2",
        "use": "Người chơi lấy thanh kiếm gãy của tà tu, tra vào vỏ bên hông (c2_d25c_2).",
        "body": "Close view at dusk: a hand lifting a broken sword from grey stone, the snapped edge "
        "catching a thin line of light, an empty scabbard held open by another hand. Behind, blurred, "
        "the dark wall of a crevice and the hem of a dark robe. Dust in the air. Composition centred "
        "with calm dark space above for game text. Practical, cold, not quite theft.",
    },
    # ─ Bị chặn đường ở sườn đông (tán tu) ─
    {
        "key": "bc_c2_suon_dong_chan_duong",
        "name": "Sườn đông — bị chặn đường lúc rời cốc",
        "doan": "c2_d27c_0",
        "use": "Người chơi bị chặn ở sườn đông khi rời cốc; phía sau là lửa, phía trước là người (c2_d27c_0).",
        "body": "A rocky eastern slope above a valley at night: fires glow far below and behind, while "
        "two grey-robed figures stand ahead on the narrow path, blocking it, faces unreadable in the "
        "dark. A ragged youth stands between fire and men, a thin sword just drawn, moonlight on the "
        "blade. Smoke drifting. Composition keeps the upper part dark and calm for game text. Cornered, "
        "adrenaline, no way but through.",
    },
    {
        "key": "bc_c2_lui_lai_suon_dong",
        "name": "Lùi lại sườn đông — nhường đường",
        "doan": "c2_d27c_1",
        "use": "Người chơi lùi lại nhường đường, hai kẻ áo xám đi qua rồi khuất (c2_d27c_1).",
        "body": "Night on a narrow rock path: two grey-robed men walking past, close, one turning his "
        "head slightly toward the viewer; a ragged youth pressed back against the rock wall to let them "
        "pass, sword lowered. Fires far below, mist. Composition keeps the upper part dark and calm for "
        "game text. Held breath, humiliated, alive.",
    },
    {
        "key": "bc_c2_menh_lenh_bai_doi_duong",
        "name": "Đưa lệnh bài đổi đường đi",
        "doan": "c2_d27c_2",
        "use": "Người chơi đưa tấm lệnh bài để đổi lấy đường đi; một kẻ áo xám cầm lấy (c2_d27c_2).",
        "body": "Night on rock: a small dark token held out on an open palm, a grey-robed man's hand "
        "closing over it, both hands lit by thin moonlight. Behind, a second grey figure waits, and a "
        "ragged youth watches his own hand give the thing away. Fires below, mist. Composition keeps the "
        "upper part dark and calm for game text. A trade that costs more than it looks.",
    },
    {
        "key": "bc_c2_rut_kiem_danh_toi_cung",
        "name": "Rút kiếm — đánh tới cùng",
        "doan": "c2_d27c_3",
        "use": "Người chơi rút kiếm đánh tới cùng trên sườn đông; kiếm linh hét lên (c2_d27c_3).",
        "body": "Night on a rocky slope, close and violent: a thin sword swung hard, its edge catching "
        "firelight from below, a grey-robed figure recoiling with an arm up. A ragged youth behind the "
        "blade, mouth open, eyes wide. Smoke, sparks, cold mist. Composition keeps the upper part dark "
        "and crowded only at the bottom for game text. Desperate, too committed, no plan left.",
    },
    {
        "key": "bc_c2_nga_xuong_suon_dong",
        "name": "Ngã xuống sườn đông — đêm khép lại",
        "doan": "c2_d27c_thua",
        "use": "Kết thua: người chơi ngã xuống sườn đông, kiếm rời tay, lửa xa dần (c2_d27c_thua).",
        "body": "A rocky slope at night seen from very low, almost at ground level: a thin sword lying "
        "loose on the stones out of reach, a dark shape of a body fallen on its side, dust settling. Far "
        "below, the valley fires burn small and distant. Grey moonlight, mist creeping along the ground. "
        "Composition leaves the upper part vast, dark and calm for game text. Stillness, finality, quiet.",
    },
]

# Nhóm cảnh theo nhịp truyện. `keys` = ảnh của nhóm; `mau` = ảnh mẫu cần đính
# kèm khi vẽ (giữ mặt/tóc/áo nhân vật y hệt).
NHOM_CANH = [
    {"ma": "c2-dau-chuong", "phan": "c2", "ten": "Đầu chương — tang lễ Mạc phủ",
     "mota": "Sân Mạc phủ treo vải trắng; khách khinh khỉnh; di vật của Mạc Đại Phu.",
     "keys": ["bc_mac_phu_tang"], "mau": ["nv_chinh_mau"]},
    {"ma": "c2-vao-coc", "phan": "c2", "ten": "Vào Thái Nam Sơn Cốc",
     "mota": "Thung lũng hội ban đêm; chợ tu sĩ; hai người đổi linh thạch.",
     "keys": ["bc_thai_nam_hoi", "bc_c2_cho_linh_thach", "bc_c2_goc_hang_im"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "c2-gap-han-lap", "phan": "c2", "ten": "Gặp Hàn Lập bán ngọc",
     "mota": "Hàn Lập ngồi bán di vật; mảnh ngọc soi nắng; hắn gói ngọc rất nhanh.",
     "keys": ["nv_c2_han_lap_ban_hang", "vt_c2_manh_ngoc_to", "nv_c2_han_lap_goi_ngoc",
              "bc_c2_lung_ao_vao_dam_dong", "bc_c2_di_qua_day_hang"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-goc-cho", "phan": "c2", "ten": "Góc chợ — cuốn sách của Mạc Đại Phu",
     "mota": "Đèn lồng thắp cùng lúc; Trường Xuân Công tầng bốn tới sáu; Hàn Lập kể về sư phụ.",
     "keys": ["bc_c2_goc_cho_den_long", "nv_c2_han_lap_ngang_dau", "bc_c2_goc_cho_trong",
              "nv_c2_han_lap_noi_ve_mac", "nv_c2_han_lap_doc_sach"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-dem-dau", "phan": "c2", "ten": "Đêm đầu — kiếm linh dạy hít hồng trần",
     "mota": "Gờ đá ban đêm; dẫn hồng trần tới đau; dừng sớm hay đi quá một nhịp.",
     "keys": ["bc_c2_go_da_dem", "nv_c2_dung_som", "nv_c2_di_qua_gioi_han"],
     "mau": ["nv_chinh_mau", "nv_kiem_linh"]},
    {"ma": "c2-van-tieu-son", "phan": "c2", "ten": "Vạn Tiểu Sơn — một câu hỏi đổi một linh thạch",
     "mota": "Bục đá; viên linh thạch cuối; Thăng Tiên Lệnh; kẻ giữ tấm thứ hai.",
     "keys": ["nv_c2_van_tieu_son", "bc_c2_buc_da_dat_thach", "bc_c2_lui_khoi_dam_dong",
              "bc_c2_bong_ao_xam_quay_di", "bc_c2_nghe_ben_le"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "c2-tra-gia", "phan": "c2", "ten": "Trả giá thuốc — dãy hàng phía bắc",
     "mota": "Bà bán đan và cái cân nhỏ; ba hay năm viên; tiếng cười khô đầu tiên.",
     "keys": ["nv_c2_ba_can_thuoc", "nv_c2_han_lap_vai_ha", "bc_c2_quay_thuoc",
              "nv_c2_han_lap_cuoi_kho", "nv_c2_han_lap_quay_lai"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-bi-theo-doi", "phan": "c2", "ten": "Ba kẻ áo xám",
     "mota": "Ba bóng áo xám rải giữa chợ, theo người chơi từ dãy đông.",
     "keys": ["bc_c2_ba_bong_ao_xam"], "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-khe-da", "phan": "c2", "ten": "Khe đá — một canh giờ bàn tay trên vai",
     "mota": "Ép sát vách; nửa mặt trong tối; 'cùng nhau ra khỏi đây'; gần sáng.",
     "keys": ["bc_c2_khe_da_sat_vach", "nv_c2_nua_mat_trong_toi", "bc_c2_khe_da_lanh",
              "bc_c2_khe_da_tho_ra", "bc_c2_khe_da_gan_sang"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-tu-lo", "phan": "c2", "ten": "Nhánh tự lo — một mình dưới gờ đá",
     "mota": "Người chơi tự lo; ba kẻ áo xám tới gần sáng; Hàn Lập đã đi.",
     "keys": ["bc_c2_go_da_mot_minh"], "mau": ["nv_chinh_mau"]},
    {"ma": "c2-giao-dich", "phan": "c2", "ten": "Giao dịch với kẻ áo xám thêu chỉ bạc",
     "mota": "Hàn Lập đổi một tấm lệnh lấy một con đường; người chơi bước tới hay bỏ đi.",
     "keys": ["bc_c2_giao_dich_ao_xam", "nv_c2_han_lap_giac_minh", "bc_c2_quay_lung_muoi_buoc"],
     "mau": ["nv_han_lap", "nv_chinh_mau"]},
    {"ma": "c2-linh-can", "phan": "c2", "ten": "Bà lão đo linh căn",
     "mota": "Viên đá sáng trắng: thiên linh căn, 'đừng để ai biết'.",
     "keys": ["nv_do_linh_can"], "mau": ["nv_chinh_mau"]},
    {"ma": "c2-ta-tu", "phan": "c2", "ten": "Tà tu phong toả cốc",
     "mota": "Sáng ngày cuối: chợ dọn gấp, khói bốc phía đông, không ai được ra.",
     "keys": ["bc_c2_cho_don_hang"], "mau": []},
    {"ma": "c2-binh-men", "phan": "c2", "ten": "Bình men xanh",
     "mota": "Cái bình nhặt ở Thất Huyền Môn; gói rất chậm; 'nó đang chờ một người'.",
     "keys": ["vt_c2_binh_men_xanh", "nv_c2_han_lap_goi_binh", "nv_c2_han_lap_cam_binh",
              "vt_c2_binh_tren_da"],
     "mau": ["nv_han_lap"]},
    {"ma": "c2-nap-minh", "phan": "c2", "ten": "Nấp trong hốc đá — nghe một người chết",
     "mota": "Hốc đá phía tây; khe hở nhìn ra thung lũng; cái bình không phản chiếu lửa.",
     "keys": ["bc_c2_hoc_da_phia_tay", "vt_c2_binh_khong_phang"], "mau": ["nv_chinh_mau"]},
    {"ma": "c2-xac-nguoi", "phan": "c2", "ten": "Xác người trong khói",
     "mota": "Nằm trong khe đếm nhịp thở; bò ra thấy xác; Hàn Lập quỳ lục túi trữ vật.",
     "keys": ["bc_c2_nam_trong_khe", "bc_c2_xac_trong_khoi", "bc_c2_xac_ao_xam"],
     "mau": ["nv_chinh_mau", "nv_han_lap"]},
    {"ma": "c2-giet-nguoi", "phan": "c2", "ten": "Hàn Lập — kẻ giết người",
     "mota": "'Ngươi là kẻ giết người' — 'ừ'; đi bên nhau; vai chạm vai; bàn tay còn nắm hờ.",
     "keys": ["bc_c2_han_lap_di_ve_ria", "bc_c2_di_ben_nhau", "bc_c2_vai_cham_vai",
              "bc_c2_ban_tay_nam_ho"],
     "mau": ["nv_chinh_mau", "nv_han_lap"]},
    {"ma": "c2-roi-coc", "phan": "c2", "ten": "Rời cốc — tấm Thăng Tiên Lệnh",
     "mota": "Lửa còn ở rìa cốc; tấm lệnh trong lòng bàn tay; người chơi đẩy lại.",
     "keys": ["bc_c2_ra_coc_dem", "vt_c2_thang_tien_lenh", "bc_c2_day_lenh_lai"],
     "mau": ["nv_chinh_mau", "nv_han_lap"]},
    {"ma": "c2-chia-tay", "phan": "c2", "ten": "Chia tay ở chân núi",
     "mota": "Cốc sau lưng im; hai thanh kiếm ấm; mỗi người đi đường mình.",
     "keys": ["bc_c2_chan_nui_chia_tay", "bc_c2_khong_ngoai_lai", "bc_c2_duong_mon_phia_bac"],
     "mau": ["nv_chinh_mau", "nv_han_lap"]},
    # ─ Ba cảnh chiến đấu + kết thua (thêm cùng nhánh kết thua) ─
    {"ma": "c2-ba-ke-ao-xam", "phan": "c2", "ten": "Ba kẻ áo xám đêm — ba cách đánh",
     "mota": "Chặn giữa đường đêm: ném đá lệch hướng, lách khe hẹp đánh đầu gối, hoặc chỉ tay nói dối.",
     "keys": ["bc_c2_ba_ke_ao_xam_dem", "bc_c2_da_lenh_dem", "bc_c2_khe_da_danh_vo",
              "bc_c2_ba_ke_bo_di"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "c2-ta-tu-bi-thuong", "phan": "c2", "ten": "Tà tu bị thương ở miệng khe",
     "mota": "Kẻ tà tu thở dốc dựa vách; lết ra miệng khe; thanh kiếm gãy còn đó.",
     "keys": ["bc_c2_ta_tu_bi_thuong", "bc_c2_ta_tu_cheo_mieng_khe", "bc_c2_lay_kiem_ta_tu"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "c2-chan-duong", "phan": "c2", "ten": "Sườn đông — bị chặn đường lúc rời cốc",
     "mota": "Lửa phía sau, người phía trước: lùi lại, đưa lệnh bài, hay rút kiếm đánh tới cùng.",
     "keys": ["bc_c2_suon_dong_chan_duong", "bc_c2_lui_lai_suon_dong",
              "bc_c2_menh_lenh_bai_doi_duong", "bc_c2_rut_kiem_danh_toi_cung"],
     "mau": ["nv_chinh_mau"]},
    {"ma": "c2-ket-thua", "phan": "c2", "ten": "Kết thua — ngã xuống sườn đông",
     "mota": "Kiếm rời tay, đêm khép lại; lửa dưới thung lũng xa dần.",
     "keys": ["bc_c2_nga_xuong_suon_dong"], "mau": []},
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
    """key -> [đoạn], suy thẳng từ trường `doan` của từng cảnh."""
    ra = {}
    for s in SCENES:
        if any(s["doan"] in ds for ds in ra.values()):
            raise ValueError(f"hai cảnh cùng trỏ một đoạn: {s['doan']}")
        ra[s["key"]] = [s["doan"]]
    return ra
