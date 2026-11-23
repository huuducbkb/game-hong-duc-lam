"""Prompt tạo tiếng cho từng cảnh, viết như prompt tả âm thanh.

Bài học từ một prompt khác tốt hơn: prompt cũ của tôi kể chuyện ("the player
walks into..."), mở bằng ba lần phủ định ("Ambience, no music, no speech"), và
chỉ 2/43 cảnh nói chất âm muốn thế nào. Máy tạo tiếng không tạo được hành động
của người chơi — nó chỉ tạo được tiếng. Nên bản này:

1. Mở bằng câu khai báo đầy đủ: dài bao lâu, không khí gì, ở đâu. Không mở
   bằng phủ định.
2. Không có "the player". Chỉ tả cái tai nghe thấy. Người chơi vẫn là gốc của
   mọi khoảng cách ("at the ear", "a few metres off", "far behind") nhưng không
   được kể là đang làm gì.
3. Có từ chỉ chất âm: warm, cold, intimate, field recording, natural reverb,
   enclosed, open air. Không có mấy chữ này thì máy tự đoán chất, mỗi lần ra
   một kiểu.
4. Phủ định trừu tượng đổi thành tả cụ thể. "Nothing comes back" thành "open
   air, no reflection, each sound lands and dies". Máy không tạo được cái
   không-có-gì; nó chỉ tạo được cái đang có.
5. Ba lớp khoảng cách, và nói rõ tiếng đổi chất ở đâu: tường đá dội lại, ngõ
   hẹp dội nhanh, phòng kín đè tiếng xuống, ngoài trời tiếng rơi là mất.
6. Không lời nói. Chỉ thở, hừ, rên, huýt gió, la, khóc. "Shouted count" là đếm
   thành tiếng, tức là có chữ — đã bỏ, thay bằng "a sharp whistle".
7. Dưới 450 ký tự: trần cứng của ô prompt ElevenLabs Sound Effects.
"""

PROMPT = {

    # ------------------------------ CHỢ ------------------------------

    "cho_01": (
        "10-second dense, close morning market ambience heard from ground "
        "level in a crowded corner. Cart wheels creaking on packed earth, "
        "clay jars knocking, coins dropped into a palm, cloth brushing past "
        "the ear. A few metres off: crossing footsteps, a stool dragged, "
        "laughter once. Far behind: a dog. Crowd-damped, echo swallowed. No "
        "music, no speech, seamless loop."
    ),

    "cho_02": (
        "10-second hushed night ambience at the mouth of a narrow alley "
        "behind a market. Ten metres off, men sit around a small fire: "
        "crackling, a stick poking embers, spit hissing, a cough, a low sigh. "
        "Their sound comes back off the close walls, softened. Near the ear: "
        "quiet breathing, a boot scuffing grit. Intimate, walled-in field "
        "recording. No music, no speech, seamless loop."
    ),

    "cho_03": (
        "10-second sparse, tired dusk ambience at the edge of an emptying "
        "market. Close at the ear: a broom sweeping packed earth, cloth "
        "moving. Further off: a wooden stall folded and stacked, crates "
        "dragged. Behind and right: slow footsteps walking away, a cough, a "
        "long sigh. Dry wind moving loose paper. Open ground, no reflection, "
        "far sounds thin out. No music, no speech, seamless loop."
    ),

    # ------------------------------ TRẬN LỬA ------------------------------

    "tran_lua": (
        "10-second distant night ambience from a high mountain path above a "
        "burning town. Everything from the valley is thin and wide: fire "
        "roaring, timber cracking, structures falling, one far shout, a horn. "
        "Close at the ear: wind on the ridge, grass moving, cloth. The valley "
        "is too wide to answer. Cold, open, cinematic. No music, no speech, "
        "seamless loop."
    ),

    "tran_lua_2": (
        "10-second chaotic night ambience inside a burning town street. Close "
        "around the head: fire roaring through a wooden house, roof beams "
        "cracking, a blade sweeping through air, steel ringing on steel, "
        "boots hammering stone, hard breathing. Ahead: a wall coming down, "
        "horses. Behind: a shout. House fronts throw every sound back fast "
        "and hard. Immersive. No music, no speech, seamless loop."
    ),

    "tran_lua_3": (
        "10-second violent night ambience at the shattered gate of a martial "
        "sect under assault. Close: a heavy gate splintering, hinges tearing, "
        "boots stamping broken planks, hard breathing, one blade turning "
        "another aside. Further back, bouncing off stone: many men moving at "
        "once, grunts, one hoarse shout. Beyond the gate: fire. Walled in, "
        "hard reflections. No music, no speech, seamless loop."
    ),

    # ------------------------------ CỔNG ĐÔNG ------------------------------

    "cong_dong_doi_mat": (
        "10-second tense near-silent ambience at a broken gate, the instant "
        "before blades meet. Close at the ear: slow breath, cloth shifting as "
        "weight settles. A few metres ahead: their breathing, a boot scuffing "
        "stone, a blade drawn an inch. Behind: wind through the gate. Sparse, "
        "with long gaps, and the stone carries every small sound. No music, "
        "no speech, seamless loop."
    ),

    "cong_dong_giau": (
        "10-second controlled, suppressed ambience at a gate. Close: fast "
        "shallow breathing, a blade turned aside, boots sliding backwards on "
        "stone, cloth snapping, a short grunt. Mid-distance, off to the side: "
        "other men moving, breath, a wordless shout. Stone walls close on "
        "both sides, so small sounds come back doubled. Restrained and dry. "
        "No music, no speech, seamless loop."
    ),

    "cong_dong_toan_luc": (
        "10-second sudden loud ambience at a gate. Close: one heavy impact, "
        "air torn, dust and gravel thrown, stone struck, breath bursting out, "
        "a loud grunt. Around, further off: the exchange carries on, then a "
        "brief stunned quiet, one shout from onlookers. The gate walls catch "
        "it and send it back a beat later. Punchy, physical. No music, no "
        "speech, seamless loop."
    ),

    "cong_dong_quyen": (
        "10-second dry close-combat ambience at a gate, bare-handed. Right at "
        "the ear: a fist striking a chest, a forearm blocking, sleeves "
        "snapping, feet pivoting and stamping stone, steady breathing through "
        "the nose, a short exhale on each strike. Further off: boots on "
        "stone, a grunt. Stone under and behind returns every hit a little "
        "late. No music, no speech, seamless loop."
    ),

    # ------------------------------ 10-second courtyard ambience built on one shout and its echo. Close at the ear: one breath held. One raw wordless shout goes out and comes back off the far wall, then everything stops: blades quiet, footsteps halt, wind, many men holding still. The wall is the depth, a long hard reflection. Tense, wide, open. No music, no speech, seamless loop. ------------------------------

    "cong_dong_hung_ba": (
        "10-second courtyard ambience built on one shout and its echo. Close "
        "at the ear: one breath held. One raw wordless shout goes out and "
        "comes back off the far wall, then everything stops: blades quiet, "
        "footsteps halt, wind, many men holding still. The wall is the depth, "
        "a long hard reflection. Tense, wide, open. No music, no speech, "
        "seamless loop."
    ),

    # ------------------------------ 10-second urgent ambience inside a burning building. Fire close and filling the space: roaring, crackling, timber snapping, embers falling. At the ear: heavy effort breathing, wood levered and thrown aside, a weak hoarse moan. Outside, further off and muffled through the fire: a shout. Thick, smoke-damped, claustrophobic. No music, no speech, seamless loop. ------------------------------

    "hoa_truong_cuu": (
        "10-second urgent ambience inside a burning building. Fire close and "
        "filling the space: roaring, crackling, timber snapping, embers "
        "falling. At the ear: heavy effort breathing, wood levered and thrown "
        "aside, a weak hoarse moan. Outside, further off and muffled through "
        "the fire: a shout. Thick, smoke-damped, claustrophobic. No music, no "
        "speech, seamless loop."
    ),

    # ------------------------------ ĐƯỜNG MÒN NÚI ------------------------------

    "duong_mon_nui": (
        "10-second cold open ambience on a narrow mountain trail at dusk. At "
        "the ear: boots on loose gravel, dry grass brushing legs, quiet "
        "breathing. Further out, wide and open: wind through tall grass, "
        "crickets starting up. Far below: wind moving in the valley. Open "
        "air, no reflection, each sound lands and dies. No music, no speech, "
        "seamless loop."
    ),

    "khe_nui_dem": (
        "10-second cold, narrow ambience in a rock ravine at night. Close at "
        "the ear: a few drops falling into a pool, sparse insects, quiet "
        "breathing. The ravine makes the wind sigh, forced through the gap "
        "and coming back off wet stone on both sides. Far above: wind "
        "crossing the open ridge. Tight, echoing, enclosed. No music, no "
        "speech, seamless loop."
    ),

    "khe_nui_chon": (
        "10-second physical ambience of hurried digging in a mountain ravine "
        "at night. Close: a shovel blade cutting wet soil, gravel sliding, "
        "earth landing on a pile, heavy breathing with effort, the shovel "
        "scraping rock. Further out: wind through the ravine gap, distant "
        "insects. Rock walls close in, so the digging comes back off both "
        "sides. No music, no speech, seamless loop."
    ),

    # ------------------------------ SÂN TẬP ------------------------------

    "san_tap_ngay": (
        "10-second dense, hot midday ambience in a large training yard. At "
        "the ear: bare feet stamping packed earth, breath forced out on each "
        "move. A few metres off, left and right: wooden staffs striking each "
        "other, staffs hitting the ground in unison, a sharp whistle blast. "
        "Further off: banners flapping overhead. Open yard, far sounds thin "
        "out. Rhythmic, busy. No music, no speech, seamless loop."
    ),

    "san_tap_chen_ep": (
        "10-second hostile quiet ambience in a training yard, a ring of "
        "students closing in. Low laughter, a mocking hum, feet shuffling as "
        "they circle, a staff tapping ground, someone spitting. Close, all "
        "around the head. The ring of bodies soaks the sound up instead of "
        "bouncing it. The rest of the training carries on further off. Tight, "
        "unpleasant. No music, no speech, seamless loop."
    ),

    "san_tap_cai_lai": (
        "10-second ambience of a training yard going silent after one slap. "
        "One sharp angry shout, wordless, then a flat slap lands close, and "
        "the whole yard goes completely quiet. After a beat a low hum of "
        "reaction spreads through the crowd, only sound. Far off: the rest of "
        "the training has stopped too. The quiet leans in. No music, no "
        "speech, seamless loop."
    ),

    # ------------------------------ SÂN SAU ------------------------------

    "san_sau_luyen_dem": (
        "10-second deliberately small ambience of solitary late-night "
        "practice in a back yard. Everything at the ear: bare feet on packed "
        "earth, cloth moving, breath held and released through the nose, a "
        "fist passing through air, a quiet landing after a step. Far off: "
        "insects, one dog. Open night air, no reflection, sound dies fast. No "
        "music, no speech, seamless loop."
    ),

    "san_sau_anh_sang": (
        "10-second still ambience under a huge old tree in a back yard at "
        "night. Close at the ear: quiet breathing, one insect very close. "
        "Overhead: leaves moving in a light wind, a thick branch creaking "
        "slowly, leaves letting go and landing. Far off: crickets, a dog. The "
        "canopy deadens everything above. Damp, faintly uneasy. No music, no "
        "speech, seamless loop."
    ),

    "san_sau_chon_lai": (
        "10-second hurried ambience of digging in a back yard at night. "
        "Close: a small shovel biting soft earth, soil poured out, roots "
        "snapping, leaves pushed aside, fast breathing, cloth rustling. "
        "Overhead: the old tree's leaves moving. Far off: a dog. Soft earth "
        "swallows the digging, the leaves overhead catch the rest. Muffled, "
        "secretive. No music, no speech, seamless loop."
    ),

    # ------------------------------ VƯỜN THUỐC ------------------------------

    "vuon_thuoc_gap": (
        "10-second warm, secluded morning ambience in a walled herb garden. "
        "Gentle breeze rustling dense herbal leaves, brushing softly against "
        "each other and against cloth. A bee buzzes close by, sparse delicate "
        "insects behind it. Dry stems snap underfoot. Beyond the wall, "
        "softened by distance: wooden staffs striking, a sharp whistle. "
        "Intimate field recording, natural reverb off the wall. No music, no "
        "speech, seamless loop."
    ),

    "vuon_thuoc_hoi": (
        "10-second tense, quiet ambience in a walled herb garden, two people "
        "standing close and wordless. What carries is the shape of it: slow "
        "dry breathing close on the left, a younger breath held tight, a foot "
        "shifting, cloth. Behind them, further off: leaves moving, insects, a "
        "bundle of herbs being tied. The wall holds it all in, low. No music, "
        "no speech, seamless loop."
    ),

    "vuon_thuoc_im": (
        "10-second deliberate stillness in a walled herb garden, wordless. "
        "Close at the ear: a bundle of dried herbs being handled, quiet "
        "breathing. Further off: leaves moving in a light wind, insects, one "
        "bird far away. Long quiet stretches between each small sound. The "
        "wall holds everything in, so the quiet has an edge. No music, no "
        "speech, seamless loop."
    ),

    "vuon_thuoc_ngoc": (
        "10-second secretive ambience in a walled herb garden, a heavy object "
        "handled. Close: a jade object set down on wood with a solid knock, "
        "cloth unwrapped, fingers brushing stone, a bundle of herbs laid "
        "aside. Near the ear: two low unhurried breaths. Behind: leaves, "
        "insects. The wall keeps it in and small. No music, no speech, "
        "seamless loop."
    ),

    "vuon_thuoc_dem": (
        "10-second careful night ambience of digging in a herb garden. Close "
        "at the ear: a small tool cutting soft soil, roots snapping, earth "
        "poured out, breath held. Further out: leaves swept aside, insects in "
        "wet garden air. The wall keeps it close, damp air deadens whatever "
        "tries to travel. Still, cool, patient. No music, no speech, seamless "
        "loop."
    ),

    # ------------------------------ MIẾU ------------------------------

    "mieu_hoang": (
        "10-second vast, cold ambience outside a ruined shrine at night. "
        "Close at the ear: quiet breathing, grass moving at the feet. Ahead, "
        "inside the ruin: wind pushing through broken walls and gaps, "
        "whistling low then dropping away, loose roof tiles shifting. Further "
        "off: crickets, a piece of wall crumbling. Broken walls break the "
        "wind into pieces. No music, no speech, seamless loop."
    ),

    # Cảnh "quay phắt lại": chỉ cần tiếng cửa và bước chân, 2 giây. Không phải
    # 10 giây — người chơi bấm xong là sang cảnh khác ngay.
    "mieu_trong": (
        "2-second scene, dry stone shrine interior at night. An old wooden "
        "door drags open, hinge creaking, then two slow heavy footsteps on "
        "gritted stone coming from behind, closer on the second. Short dry "
        "stone reverb. No music, no voice, no wind."
    ),

    "doat_hop": (
        "10-second violent ambience of a struggle for a box inside a stone "
        "shrine. Close: boots slipping on stone, bodies colliding, cloth "
        "tearing, a blade swung and missing, one heavy impact, then weight "
        "dropping onto the floor. One hoarse shout, cut short. Further off, "
        "outside: a door, running feet. Then only echo. Hard, resonant stone. "
        "No music, no speech, seamless loop."
    ),

    "tu_khiem": (
        "10-second precise ambience of sword practice in a shrine at night. "
        "Close at the ear: a blade cutting air in a long clean arc, steel "
        "ringing faintly as it turns, the guard shifting in the hand, bare "
        "feet pivoting on stone, even breathing. Further off: the room "
        "answers each swing with its own reverb, then near-silence. Cold, "
        "sharp, clean. No music, no speech, seamless loop."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_dem": (
        "10-second small, dry ambience of a cramped wooden dormitory at "
        "night, someone lying awake. Close at the ear: a bed frame creaking "
        "under small movement, cloth shifting, slow even breathing. Outside "
        "the paper window, muffled and further: crickets, a frog, a dog far "
        "away, light wind. The small room keeps everything close. No music, "
        "no speech, seamless loop."
    ),

    "dem_tap_kich": (
        "10-second ambience that turns from quiet night to chaos. Inside a "
        "wooden dormitory, close at the ear: insects, a bed frame, quiet "
        "breathing; further off: wind, timber settling. Then a horn cuts in "
        "from the forest and everything breaks at once: fire igniting, "
        "blades, running feet, a gate slamming, one shout. Sharp contrast, "
        "wide to close. No music, no speech, seamless loop."
    ),

    "tan_xa_sang": (
        "10-second ordinary morning ambience in a martial sect dormitory. "
        "Close: a wooden door sliding open, sandals on stone, water poured "
        "from a bucket, a bed frame creaking, someone coughing, cloth pulled "
        "on. Outside, further and softened: a staff tapped on the ground, "
        "footsteps, a sharp whistle from the yard. Unremarkable, easy, "
        "lived-in. No music, no speech, seamless loop."
    ),

    "tan_xa_song_tu": (
        "10-second extremely quiet, intimate ambience of lying still in a "
        "dark room at night. At the ear: slow breathing, a pulse, cloth "
        "shifting, a wooden bed taking weight, and a faint hum that seems to "
        "come from inside the room rather than outside it. Far off: crickets. "
        "The small room holds the sound against you. Private, close, still. "
        "No music, no speech, seamless loop."
    ),

    "tan_xa_kho_tu": (
        "10-second raw, quiet ambience of sitting in the dark after failure. "
        "Close: breathing too fast and too heavy, then a long shaky exhale, "
        "then silence. A hand pressed against a chest, cloth twisted. Further "
        "off, outside the room: a wooden floor creaking as someone else "
        "shifts weight. The room is small enough to send the breathing back. "
        "No music, no speech, seamless loop."
    ),

    "tan_xa_suyt_lo": (
        "10-second tight, tense ambience of held breath in a dark dormitory. "
        "Close: breath held, then released very carefully, cloth pulled "
        "tight. Further off, outside the door on the wooden walkway, coming "
        "closer: slow deliberate footsteps, pausing right outside, then "
        "moving away and fading. Then only insects. The thin wall carries it "
        "through too clearly. No music, no speech, seamless loop."
    ),

    "tan_xa_dot_pha": (
        "10-second deep, sub-heavy ambience of a closed room under pressure. "
        "A low rumble rises out of silence, holds at its peak with a faint "
        "shimmer, then settles back into stillness. Close at the ear: one "
        "held breath, then a slow release. The walls take the rumble and give "
        "it back. Far off, the building settles around it. Pure air and "
        "stone. No music, no speech, seamless loop."
    ),

    "dot_pha": (
        "10-second heavy silence in a closed room at night. Close at the ear: "
        "wood creaking as it cools, quiet breathing, a window shutter moving "
        "a fraction. Further off, through the wall: a faint low presence in "
        "the air like pressure. Long stretches pass with only the room's own "
        "settling. The closed room presses back, so the silence has weight. "
        "No music, no speech, seamless loop."
    ),

    # ------------------------------ TĨNH / SAU TRẬN ------------------------------

    "tan_hoang": (
        "10-second heavy, empty ambience among ruins just before dawn after a "
        "battle. Fire still smouldering: low crackling, a beam settling, ash "
        "shifting. Wind crosses collapsed walls. Close and quiet: slow "
        "footsteps of men carrying something heavy, setting it down, one long "
        "breath let go, a broken sob far off then stopping. Collapsed walls "
        "scatter the sound, so it thins and dies. No music, no speech, "
        "seamless loop."
    ),

    "binh_minh": (
        "10-second clean dawn ambience over a small town the morning after "
        "trouble. Close: birds starting up one at a time, a rooster far off, "
        "light wind moving dust and loose paper. Somewhere a shutter opens, a "
        "bucket of water poured, a broom working. Almost nobody awake, the "
        "town still asleep. Open morning air, each sound lands clean and "
        "stops. No music, no speech, seamless loop."
    ),

    "mon_phai_tan_hoang": (
        "10-second wide, empty ambience in the ruins of a martial sect just "
        "before dawn. Close at the ear: quiet breathing, ash shifting. "
        "Further out, crossing open ground through broken walls: wind, a wall "
        "section coming down somewhere, loose roof tiles sliding. Far off: "
        "slow footsteps of men carrying something heavy, one long breath. "
        "Open ruins, sound spreads and thins. No music, no speech, seamless "
        "loop."
    ),

    "binh_minh_ngoc_cot": (
        "10-second high, clean dawn ambience at the mountain gate of a "
        "martial sect. Close at the ear: cloth flapping on a pole, quiet "
        "breathing. Further out: mountain wind moving steadily, birds waking. "
        "Far down the valley: a temple bell struck once and ringing away. The "
        "courtyard is empty. High open air, so the bell runs away down the "
        "valley. No music, no speech, seamless loop."
    ),

    # ------------------------------ QUÁN NƯỚC ------------------------------

    "quan_nuoc": (
        "10-second warm, crowded ambience in a dark corner of a roadside tea "
        "house. Close at the ear: a clay cup set on wood, tea poured, a "
        "kettle, coins counted, a stool scraping. Around, at other tables: a "
        "low hum too far to be anything, laughter once, a hand slapped on a "
        "table. Low ceiling and close walls press the hum down around the "
        "head. No music, no speech, seamless loop."
    ),

    # ------------------- GẶP GỠ — CẢNH CÓ MỘT CÂU THOẠI -------------------
    # Mỗi cảnh chỉ MỘT câu thoại, đúng câu đầu tiên trong cốt truyện. Người
    # chơi đọc chữ; tiếng chỉ để nghe ra ai nói, giọng thế nào, và không gian
    # quanh đó. Không lồng cả đoạn hội thoại — sẽ dài, và lệch với chữ trên
    # màn hình khi người chơi bấm sang đoạn khác.
    #
    # Câu tiếng Hoa viết theo lối cổ trang, khớp với bản dịch tiếng Việt trong
    # chuong1.json. Giọng ghi rõ tuổi và chất giọng để máy không tự đoán.

    # Đỗ Tam: đàn ông vạm vỡ, sẹo dài, giọng khàn. Câu đầu: "Lại thêm một con
    # chuột". Nói sát, lớn, có hơi đe.
    "do_tam_mieu": (
        "4-second scene, dry stone shrine interior. A heavy man's voice, "
        "rough and hoarse, low-pitched, speaking close and unhurried with a "
        "threat under it, in Mandarin: 「又来一只老鼠。」 Behind him: faint "
        "wind through a broken doorway, stone reverb short and dry. No music."
    ),

    # Hộp kiếm bật mở, giọng nam lạnh không rõ nguồn. Câu: "Ngươi… khác bọn
    # chúng."
    "kiem_hap": (
        "4-second scene in a cold stone shrine. First a wooden box lid "
        "snapping open, dry and sharp. Then a cold male voice, young, quiet, "
        "disembodied, close to the ear with long stone reverb, in Mandarin: "
        "「你……和他们不一样。」 No music, no other voices."
    ),

    # Kiếm linh hiện hình: nam trẻ, lạnh, ngắn. Câu: "Ta là kiếm linh Hồng Trần."
    "kiem_linh": (
        "5-second scene, cold stone shrine, air still. A young man's voice, "
        "flat and icy, quiet but clear, speaking close with a slight spectral "
        "edge, in Mandarin: 「我是红尘剑灵。」 Long, cold stone reverb behind "
        "the voice. No music, nothing else moves."
    ),

    # Nhân vật chính cười gằn, cảnh giác. Câu: "Tin ngươi?"
    "kiem_linh_thu": (
        "3-second scene in a still stone shrine. A young man's voice, wary "
        "and dry, a short humourless laugh inside the words, close to the "
        "ear, in Mandarin: 「信你？」 Faint metal ring far off, once. Short "
        "stone reverb. No music."
    ),

    # Kiếm linh nói đều đều, không cảm xúc. Câu: "Ta là kiếm linh của Hồng
    # Trần Kiếm."
    "kiem_linh_than": (
        "6-second scene, cold stone hall, dead quiet. A young man's voice, "
        "even and emotionless, measured pace, close and clear, in Mandarin: "
        "「我是红尘剑的剑灵。」 Stone hall reverb stretching behind each "
        "phrase. No music, no breath, no movement."
    ),

    # Nhân vật chính hỏi lại, dè dặt. Câu: "Ta cần biết rõ."
    "kiem_linh_dieu": (
        "4-second scene, still stone shrine. A young man's voice, cautious "
        "and low, choosing words carefully, close to the ear, in Mandarin: "
        "「我要问清楚。」 Very short stone reverb, nothing else in the room. "
        "No music."
    ),

    # Nhận chủ: kim loại rạch mảnh, rồi kiếm linh nói ngắn. Câu: "Xong rồi."
    "kiem_hap_nhan": (
        "4-second scene, cold stone shrine. A thin blade cuts skin, one "
        "small sharp metallic whisper. Then a young man's low voice, "
        "satisfied and final, close, in Mandarin: 「成了。」 Quiet stone "
        "around it. No music."
    ),

    # Hàn Lập quay lưng, giọng trầm đều. Câu: "Theo ta lâu vậy, không mệt sao?"
    "han_lap": (
        "4-second scene on a quiet mountain path, late afternoon. A man's "
        "voice, low and flat, unhurried, speaking without turning around, "
        "close to the ear, in Mandarin: 「跟了我这么久，不累吗？」 Behind "
        "him: light wind on ridge grass, gravel underfoot, cloth shifting. "
        "No music."
    ),

    # Hàn Lập nói chậm, cân nhắc. Câu: "Người ở đây chỉ nhìn thấy một kẻ lang
    # thang nơi ta."
    "han_lap_2": (
        "5-second scene, still mountain night. A man's voice, low and even, "
        "slow, weighing each phrase, close, in Mandarin: 「这里的人只看见一个"
        "流浪汉。」 Very quiet night air, one distant insect. No music, no "
        "echo."
    ),

    # Tân xá đêm: đèn dầu tí tách + câu thoại của nhân vật chính. Ngọc phát
    # sáng KHÔNG có âm thanh — anh dặn rõ: chỉ lửa đèn dầu, không tiếng cho ngọc.
    "ngoc_cot": (
        "6-second scene, small wooden room at night, very still. Close at the "
        "ear: a tiny oil-lamp flame ticking and crackling, slow quiet "
        "breathing, straw mat shifting once. Then a young man's voice, barely "
        "above a whisper, half to himself, in Mandarin: 「你……是什么？」 The "
        "glowing jade itself makes no sound at all. No music, no hum, no "
        "shimmer."
    ),

    # Nhân vật chính giật mình. Câu: "Ngươi… ngươi là ai? Sao lại ở trong khối
    # ngọc này?"
    "tuyet_co": (
        "5-second scene, wooden room at night, lamp lit. A young man's voice, "
        "startled and unsteady, breath catching first, close to the ear, in "
        "Mandarin: 「你……你是谁？怎么会在玉里？」 Tiny lamp flame ticking "
        "under it. No music."
    ),

    # Nhân vật chính cười gằn, gượng. Câu: "Cần ta?"
    "tuyet_co_canh_giac": (
        "3-second scene, still night room. A young man's voice, guarded, "
        "with a dry forced laugh at the front, close, in Mandarin: "
        "「需要我？」 Soft room tone, one unsteady breath. No music."
    ),

    # Tuyết Cơ: nữ, mềm như tơ nhưng lạnh, chậm. Câu: "Ta là Tuyết Cơ."
    "tuyet_co_than_phan": (
        "6-second scene, quiet wooden room at night. A woman's voice, soft "
        "and silky but cold underneath, slow as if telling an old story, "
        "close to the ear, in Mandarin: 「我是雪姬。」 Lamp flame ticking "
        "faintly, still air. No music."
    ),

    # Nhân vật chính hỏi, giọng đã run. Câu: "Ta cần biết rõ."
    "tuyet_co_dieu_kien": (
        "4-second scene, silent night room. A young man's voice, trembling "
        "slightly, trying to hold steady, close, in Mandarin: 「我要问清楚。」 "
        "Only quiet room tone and one breath. No music."
    ),

    # Do dự, KHÔNG có thoại. Chỉ nín thở, đèn dầu, gỗ khẽ kêu.
    "tuyet_co_do_du": (
        "5-second scene, night room, held breath. Close at the ear: breath "
        "stopped then released slowly, a tiny oil-lamp flame ticking, one "
        "dry wooden joint creaking. Tense but nothing loud. No voice, no "
        "music."
    ),

    # Nhân vật chính nói ngắn, đã quyết. Câu: "Ta ký."
    "tuyet_co_khe_uoc": (
        "4-second scene, quiet night room. A young man's voice, low and "
        "firm, decision already made, close, in Mandarin: 「我签。」 A soft "
        "female breath answers, barely audible. Lamp ticking. No music."
    ),

    # Hàn Lập nói mà không quay đầu. Câu: "Theo ta suốt đoạn đường vậy, không
    # mệt sao?"
    "han_lap_gap": (
        "4-second scene on a rocky path behind a mountain, night. A man's "
        "voice, low and even, calm, speaking with his back turned, close, in "
        "Mandarin: 「跟了我一路，不累吗？」 Light night wind over rock, "
        "gravel. No music, nobody else."
    ),

    # Nhân vật chính nói ra, giọng khàn. Câu: "Ta biết tương lai của ngươi."
    "han_lap_that": (
        "6-second scene, very still mountain night. A young man's voice, "
        "gone hoarse with tension, quiet but deliberate, close, in Mandarin: "
        "「我知道你的未来。」 Dead air around it, no wind, no insect. No "
        "music."
    ),

    # Nhân vật chính cười gượng, lảng tránh. Câu: "Ta chỉ là kẻ tình cờ ở đây
    # thôi."
    "han_lap_cuoi_tru": (
        "4-second scene, quiet night air. A young man's voice, an awkward "
        "laugh first, then evasive and light, close, in Mandarin: 「我只是碰巧"
        "路过罢了。」 Still night behind it. No music."
    ),

    # Nhân vật chính hỏi ngược, có gai. Câu: "Vậy ngươi là ai?"
    "han_lap_hoi_nguoc": (
        "6-second scene, still mountain night. A young man's voice, sharp "
        "and probing, an edge in it, close to the ear, in Mandarin: 「那你又是"
        "谁？」 Faint wind far off. No music."
    ),

    # Hàn Lập nhận bầu nước, uống, rồi nói khẽ. Câu: "Ngươi không giống người
    # ở đây."
    "han_lap_bau_nuoc": (
        "5-second scene, night mountain, very quiet. A water flask cap "
        "opening, one swallow, then a man's voice, low and quiet, almost "
        "warm, close, in Mandarin: 「你和这里的人不一样。」 Light wind. No "
        "music."
    ),

}
