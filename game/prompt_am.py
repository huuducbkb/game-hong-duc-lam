"""Prompt tạo tiếng cho từng cảnh.

Mỗi prompt làm bốn việc:

1. Mở bằng một câu khai báo đầy đủ: dài bao lâu, chất âm gì, không khí gì, ở đâu.
2. Tả tiếng trong câu liền mạch, khoảng cách gắn tự nhiên vào câu.
3. Chốt bằng một thẻ chất âm ngắn, riêng cho cảnh đó.
4. Dưới 450 ký tự — trần cứng của ô prompt ElevenLabs Sound Effects.

CẢNH CÓ THOẠI: mọi cảnh mà đoạn truyện có lời ai đó nói đều phải có 1–2 câu tiếng
Hoa trong ngoặc 「」, kèm tuổi, giới và chất giọng. Không chỉ 21 cảnh nhóm "gap" —
cả cảnh nền cũng có NPC nói (Tuyết Cơ nhắc trong đầu, kiếm linh nhắc, sư huynh
quát, ăn mày lẩm bẩm…). Bảng giọng ở `game/GIONG_NPC.md`.

Sáu cảnh chỉ có giọng Hệ thống (máy, vô cảm, không phải NPC) thì để nguyên không
thoại: cho_03, duong_mon_nui, khe_nui_dem, mieu_hoang, san_sau_anh_sang, mieu_trong.

CẢNH CHỈ CÓ NHÂN VẬT CHÍNH NÓI: vẫn phải có câu của nhân vật chính, đọc bằng giọng
nam 16 tuổi trầm ấm — xem `nvc` trong `game/GIONG_NPC.md`. Trước đây bỏ thoại ở
những cảnh này, nên `vuon_thuoc_im` mất hẳn câu 「多谢前辈。」 dù truyện có lời thoại.

Đã bỏ lối cũ "No music, no speech, seamless loop." lặp ở cuối mọi prompt: game phát
mỗi file một lần rồi thôi, không lặp.
"""

PROMPT = {

    # ------------------------------ CHỢ ------------------------------

    "cho_01": (
        "10-second dense, lively early-morning ambience in a crowded corner of a "
        "small town market. Cart wheels creak over packed earth, clay jars knock "
        "together, coins drop into a palm, cloth brushes past the ear. A rough "
        "male porter's voice, around thirty-five, hoarse and impatient, barks close by in Mandarin: "
        "「让开！让开！」 Then a flat machine-even voice inside the head, in "
        "Mandarin: 「你已穿越。从今往后，我就是你的系统。」 Warm, human, "
        "close-recorded market field recording."
    ),

    "cho_02": (
        "10-second hushed, secretive night ambience at the mouth of a narrow "
        "alley behind a market. Ten paces in, men sit around a small fire: wood "
        "crackles, a stick pokes the embers, spit hisses. A lame old beggar, "
        "a man around sixty, mutters low and hoarse in Mandarin: 「再过几天，野狼帮就要打过来了。」 "
        "Their voices reach the ear softened, coming back off the close walls. "
        "Intimate, walled-in night field recording."
    ),

    "cho_03": (
        "10-second sparse, tired dusk ambience at the edge of a market that is "
        "emptying. Close at the ear, a broom sweeps packed earth and cloth "
        "shifts. Further off, a wooden stall is folded and stacked, crates "
        "dragged a short way. Behind and to the right, slow footsteps walk "
        "away, a cough, a long sigh. Dry wind moves loose paper over open "
        "ground, where distant sounds thin out and die. Weary, open-air field "
        "recording."
    ),

    # --------------------------- CHÁY / TRẬN ---------------------------

    "tran_lua": (
        "10-second distant, wide night ambience from a high mountain path above "
        "a burning town. Everything rising from the valley arrives thin and "
        "stretched: fire roaring, timber cracking, one far shout, a horn. Close "
        "at the ear, wind combs ridge grass. A man's voice, thirty, deep and grave, flat and icy, "
        "speaks close in Mandarin: 「野狼帮来得比我预想的早。」 Cold, open, "
        "cinematic mountain field recording."
    ),

    "tran_lua_2": (
        "10-second chaotic, close night ambience inside a burning town street. "
        "Fire roars through a wooden house beside the ear, roof beams crack, a "
        "blade sweeps through air, steel rings on steel, boots hammer stone, "
        "breath comes hard. A man's voice, thirty, deep and clipped, cold, cuts in "
        "close in Mandarin: 「很好。双手配合，别停下。」 Immersive, hot, "
        "urgent field recording."
    ),

    "tran_lua_3": (
        "10-second frantic, enclosed night ambience at the shattered gate of a "
        "martial sect under assault. Close by, a heavy gate splinters, hinges "
        "tear, boots stamp broken planks, breath rasps. A man's voice, thirty, deep and icy "
        "and level, speaks in Mandarin: 「别贪战。你撑不了多久，保命要紧。」 "
        "Further back, bouncing off stone, many men move at once, grunts, a "
        "hoarse shout. Brutal, enclosed stone courtyard field recording."
    ),

    "cong_dong_doi_mat": (
        "10-second tense, near-silent ambience at a broken gate in the instant "
        "before blades meet. Close at the ear, slow breath and cloth shifting as "
        "weight settles. A few paces ahead, their breathing, a boot scuffing "
        "stone, a blade drawn an inch. A girl's voice, eighteen, sweet and sultry, breathy, teasing, a little flirtatious, speaks in the head in Mandarin: 「选吧。但记住我的规矩。」 "
        "Cold, coiled, intimate stone field recording."
    ),

    "cong_dong_giau": (
        "10-second controlled, suppressed ambience at a gate. Close in, fast "
        "shallow breathing, a blade turned aside, boots sliding backwards on "
        "stone, cloth snapping, a short grunt. A girl's voice, eighteen, sweet and sultry, breathy, teasing, a little flirtatious, speaks low in the head in Mandarin: 「这就对了。」 then 「藏好。活过今晚比赢更重要。」 Stone walls "
        "close on both sides, so small sounds come back doubled. "
        "Restrained, dry, enclosed stone field recording."
    ),

    "cong_dong_toan_luc": (
        "10-second sudden, loud ambience at a gate. Close in, one heavy impact, "
        "air torn, gravel thrown, stone struck, breath bursting out. A young "
        "man's hushed voice, around twenty-five, startled, in Mandarin: 「你……"
        "用的是什么？」 Then a girl's voice, eighteen, sweet but cool and "
        "displeased, the teasing gone, in the head: 「快是快，可你露了。记住：有人开始注意你"
        "了。」 Punchy, physical, enclosed stone field recording."
    ),

    "cong_dong_quyen": (
        "10-second dry, close bare-handed combat ambience at a gate. Right at "
        "the ear, a fist strikes a chest, a forearm blocks, sleeves snap, feet "
        "pivot and stamp stone, steady breathing through the nose. A girl's voice, eighteen, sweet and sultry, pleased, teasing, speaks in the head in Mandarin: "
        "「不错。凡人的武功用对地方，就是最好的盾。」 Tight, dry, enclosed "
        "stone field recording."
    ),

    "cong_dong_hung_ba": (
        "10-second courtyard ambience built on one shout and its echo. Close at "
        "the ear, one breath held. A wordless shout goes out and comes back off "
        "the far wall, then everything stops. From deep in the dark, a hoarse "
        "heavy male voice, a man around forty-five, answers, far off, in Mandarin: 「谁敢直呼我的名字？」 "
        "A girl's voice, eighteen, sweet and amused, teasing, in Mandarin: 「胆子不小。不过好。」 "
        "Tense, wide, open stone courtyard field recording."
    ),

    "hoa_truong_cuu": (
        "10-second urgent ambience inside a burning building. Fire close and "
        "filling the space: roaring, crackling, timber snapping, embers falling. "
        "At the ear, heavy effort breathing, wood levered and thrown aside. A "
        "boy's voice, around fourteen, thin and broken, gasps close in Mandarin: "
        "「师兄……谢谢你……」 then a girl's voice, eighteen, sweet but firm, in the head: 「够了。你已经救到人了。现在顾自己的命。」 Thick, "
        "smoke-damped, claustrophobic field recording."
    ),

    # ------------------------ NÚI / KHE NÚI ------------------------

    "duong_mon_nui": (
        "10-second cold, open ambience on a narrow mountain trail at dusk. At "
        "the ear, boots on loose gravel, dry grass brushing legs, quiet "
        "breathing. Further out and wide, wind moves through tall grass and "
        "crickets start up. Far below, wind turns over in the valley. Open air, "
        "no reflection, each sound lands and dies. Cold, open, wide mountain "
        "field recording."
    ),

    "khe_nui_dem": (
        "10-second cold, narrow ambience in a rock ravine at night. Close at the "
        "ear, a few drops fall into a pool, sparse insects, quiet breathing. "
        "The ravine makes the wind sigh, forced through the gap and coming back "
        "off wet stone on both sides. Far above, wind crosses the open ridge. "
        "Tight, echoing, enclosed rock field recording."
    ),

    "khe_nui_chon": (
        "10-second physical ambience of hurried digging in a mountain ravine at "
        "night. Close in, a shovel blade cuts wet soil, gravel slides, earth "
        "lands on a pile, heavy breathing with effort, the shovel scrapes rock. "
        "Further out, wind through the ravine gap and distant insects. Rock "
        "walls close in, so the digging comes back off both sides. Cold, "
        "physical, enclosed rock field recording."
    ),

    # ---------------------------- SÂN TẬP ----------------------------

    "san_tap_ngay": (
        "10-second dense, hot midday ambience in a large training yard. At the "
        "ear, bare feet stamp packed earth and breath is forced out on each "
        "move. A few paces off, wooden staffs strike each other, a sharp whistle "
        "cuts across. Two young male disciples, both around twenty, mutter close; the first hushed "
        "and eager in Mandarin: 「听见没？野狼帮快打过来了。」 then a second, "
        "sharp and scared: 「嘘！想死啊？」 Rhythmic, busy, hot open-air field "
        "recording."
    ),

    "san_tap_chen_ep": (
        "10-second hostile, quiet ambience in a training yard as a ring of "
        "students closes in. Low laughter, a mocking hum, feet shuffling as they "
        "circle. A big young man's voice, loud and sneering, close in Mandarin: "
        "「瞧啊，新来的！棍子打得跟拍苍蝇一样。」 Then low and threatening: "
        "「过几天跟野狼帮动手，你就躲我后头。」 Tight, unpleasant, "
        "close-recorded yard ambience."
    ),

    "san_tap_cai_lai": (
        "10-second ambience of a training yard going silent after one slap. A "
        "big young man's voice, furious, close in Mandarin: 「放肆！」 Then a "
        "flat slap lands, and the whole yard goes completely quiet. After a "
        "beat, a low hum of reaction spreads through the crowd, sound only. Far "
        "off, the rest of the training has stopped too. Sharp, still, open-yard "
        "field recording."
    ),

    # ---------------------------- SÂN SAU ----------------------------

    "san_sau_luyen_dem": (
        "10-second deliberately small ambience of solitary late-night practice "
        "in a back yard. Everything at the ear: bare feet on packed earth, "
        "cloth moving, breath held and released through the nose, a fist "
        "passing through air, a quiet landing after a step. Far off, insects "
        "and one dog. Open night air, no reflection, sound dying fast. Small, "
        "secretive, open-night field recording."
    ),

    "san_sau_anh_sang": (
        "10-second still ambience under a huge old tree in a back yard at "
        "night. Close at the ear, quiet breathing and one insect very near. "
        "Overhead, leaves move in a light wind, a thick branch creaks slowly, "
        "leaves let go and land. Far off, crickets and a dog. The canopy "
        "deadens everything above. Damp, faintly uneasy, close-recorded night "
        "field recording."
    ),

    "san_sau_chon_lai": (
        "10-second hurried ambience of digging in a back yard at night. Close "
        "in, a small shovel bites soft earth, soil pours out, roots snap, leaves "
        "pushed aside, breathing quickens. A girl's voice, eighteen, sweet and dreamy, coaxing and faint, drifts in close in Mandarin: 「你……已经碰过我了。"
        "别把我丢下。」 Soft earth swallows the digging. Muffled, secretive, "
        "close night field recording."
    ),

    # --------------------------- VƯỜN THUỐC ---------------------------

    "vuon_thuoc_gap": (
        "10-second warm, secluded morning ambience in a walled herb garden. A "
        "gentle breeze rustles dense herbal leaves. A bee buzzes close by, "
        "sparse delicate insects behind it. Dry stems snap underfoot. An old "
        "man's voice, dry and unhurried, close in Mandarin: 「新来的弟子？」 then "
        "「老夫莫大夫，照看这片药园。」 Warm, tranquil, intimate walled-garden "
        "field recording."
    ),

    "vuon_thuoc_hoi": (
        "10-second tense, quiet ambience in a walled herb garden, two people "
        "standing close and wordless. What carries is the shape of it: slow dry "
        "breathing close on the left, a younger breath held tight, a foot "
        "shifting. An old man's voice, quiet and steady, close in Mandarin: "
        "「我行医几十年，受伤的人我一眼就看得出。可你……不像受伤的人。」 Warm, "
        "hushed, walled-in garden field recording."
    ),

    "vuon_thuoc_im": (
        "10-second deliberate stillness in a walled herb garden. Close at the "
        "ear, a bundle of dried herbs is handled and quiet breathing. Then a "
        "boy's voice, sixteen, low and warm, pleasant, speaks quietly in "
        "Mandarin: 「多谢前辈。」 Leaves move in a light wind, insects, one bird "
        "far away, then long quiet stretches open between each small sound. The "
        "wall holds everything in, so the quiet has an edge. Warm, still, "
        "walled-in garden field recording."
    ),

    "vuon_thuoc_ngoc": (
        "10-second secretive ambience in a walled herb garden where a heavy "
        "object is handled. Close in, a jade object is set down on wood with a "
        "solid knock, cloth unwrapped, fingers brush stone. An old man's voice, "
        "casual but probing, close in Mandarin: 「你是自己来的？没人带你来？」 "
        "Near the ear, two low unhurried breaths. Warm, hushed, close-recorded "
        "garden ambience."
    ),

    "vuon_thuoc_dem": (
        "10-second careful night ambience of digging in a herb garden. Close at "
        "the ear, a small tool cuts soft soil, roots snap, earth pours out, "
        "breath held. Further out, leaves swept aside and insects in wet garden "
        "air. The wall keeps it close, and damp air deadens whatever tries to "
        "travel. Still, cool, patient, close-recorded night garden ambience."
    ),

    # ----------------------------- MIẾU -----------------------------

    "mieu_hoang": (
        "10-second vast, cold ambience outside a ruined shrine at night. Close "
        "at the ear, quiet breathing and grass moving at the feet. Ahead, "
        "inside the ruin, wind pushes through broken walls and gaps, whistling "
        "low then dropping away, loose roof tiles shift. Further off, crickets "
        "and a piece of wall crumbling. Broken walls break the wind into "
        "pieces. Cold, vast, ruined-stone field recording."
    ),

    "mieu_trong": (
        "2-second scene inside a dry stone shrine at night. An old wooden door "
        "drags open with a creak of hinges, then two slow heavy footsteps land "
        "on gritted stone, the second closer than the first. Short dry stone "
        "reverb. Cold, close, enclosed stone ambience."
    ),

    "doat_hop": (
        "10-second frantic ambience of a struggle for a box inside a stone "
        "shrine. Close in, boots slip on stone, bodies collide, cloth tears, one "
        "heavy impact, then weight drops to the floor. A heavy man's voice, "
        "around forty, hoarse and gloating, in Mandarin: 「蠢货。我让你看看，有"
        "缘人长什么样。」 Then a man's voice, thirty, deep and cold, from the "
        "blades: 「不……配……」 Hard, resonant, enclosed stone field recording."
    ),

    "tu_khiem": (
        "10-second precise ambience of sword practice in a shrine at night. "
        "Close at the ear, a blade cuts air in a long clean arc, steel rings "
        "faintly, bare feet pivot on stone. A man's voice, thirty, deep and grave, flat and icy, "
        "instructing close in Mandarin: 「吸气。把气送到手，送到柄，送到剑尖。」 "
        "The room answers each swing with its own reverb. Cold, sharp, clean "
        "stone field recording."
    ),

    # ---------------------------- TÂN XÁ ----------------------------

    "tan_xa_dem": (
        "10-second small, dry ambience of a cramped wooden dormitory at night, "
        "someone lying awake. Close at the ear, a bed frame creaks under small "
        "movement, cloth shifts, breathing stays slow. A girl's voice, eighteen, sweet and lazy, teasing, faint as if from far inside, in Mandarin: 「坐好。我教你合欢宗的"
        "呼吸法。」 Dry, hushed, intimate room field recording."
    ),

    "dem_tap_kich": (
        "10-second ambience that turns from quiet night into chaos. Inside a "
        "wooden dormitory, close at the ear, insects, a bed frame, quiet "
        "breathing. Then a horn cuts in from the forest and everything breaks at "
        "once: fire igniting, blades, running feet, a gate slamming. A girl's voice, eighteen, sweet but sharp with alarm, in Mandarin: 「野狼帮来得比我预想的早。」 "
        "Tense, cinematic night field recording."
    ),

    "tan_hoang": (
        "10-second heavy, empty ambience among ruins just before dawn after a "
        "battle. Fire still smoulders: low crackling, a beam settling, ash "
        "shifting. Wind crosses collapsed walls. Slow footsteps of men carrying "
        "something heavy, setting it down, one long breath let go. A young man's "
        "voice, quiet and unusually gentle, in Mandarin: 「你做得不错。但这只是"
        "开始。」 Cold, exhausted, ruined open-air field recording."
    ),

    "binh_minh": (
        "10-second clean dawn ambience over a small town the morning after "
        "trouble. Close in, birds start up one at a time, a rooster far off, "
        "light wind moves dust and loose paper. A man's voice, thirty, deep and grave, tired but "
        "almost smiling, in Mandarin: 「你活过了第一夜。而且已经到炼气三层。」 "
        "Open morning air, each sound landing clean and stopping. Clean, calm, "
        "open-air dawn field recording."
    ),

    "tan_xa_sang": (
        "10-second ordinary morning ambience in a martial sect dormitory. Close "
        "in, a wooden door bangs open, sandals on stone, water poured from a "
        "bucket, a bed frame creaks. A big man's voice, around thirty, loud and blustering, in "
        "Mandarin: 「新来的！还躺着？」 then 「七玄门不养懒人。马上去练武场！」 "
        "Unremarkable, easy, lived-in room field recording."
    ),

    "quan_nuoc": (
        "10-second warm, crowded ambience in a dark corner of a roadside tea "
        "house. Close at the ear, a clay cup is set on wood, tea poured, coins "
        "counted, a stool scraping. A bearded man's voice, around forty, dropped low and "
        "secretive, close in Mandarin: 「野狼帮最近动静很怪。」 Then sharp and "
        "scared: 「嘘！乱说会丢命的。」 Warm, crowded, close-recorded tea house "
        "ambience."
    ),

    "tan_xa_song_tu": (
        "10-second extremely quiet, intimate ambience of lying still in a dark "
        "room at night. At the ear, slow breathing, a pulse, cloth shifting, and "
        "a faint hum that seems to come from inside the room. A girl's voice, eighteen, sweet and breathy, trembling, teasing, close to the ear in Mandarin: 「别怕。只是"
        "借一点。」 Private, close, still, intimate room field recording."
    ),

    "tan_xa_kho_tu": (
        "10-second raw, quiet ambience of sitting in the dark after failure. "
        "Close in, breathing too fast and too heavy, then a long shaky exhale, "
        "then silence. A hand pressed against a chest, cloth twisted. A girl's voice, eighteen, sweet but scolding, a teasing edge under it, in Mandarin: 「错了。你太急。引气是十年的"
        "事，不是一夜。」 Dry, bare, intimate room field recording."
    ),

    "tan_xa_suyt_lo": (
        "10-second tight, tense ambience of held breath in a dark dormitory. "
        "Close in, breath held, then released very carefully. Outside the door "
        "on the wooden walkway, slow footsteps come closer, pause, then fade. A girl's voice, eighteen, sweet but urgent, then fading, in Mandarin: 「让我来。」 then "
        "「不妙。我得睡一阵子。别叫我。」 Tight, hushed, intimate room field "
        "recording."
    ),

    "tan_xa_dot_pha": (
        "10-second deep, sub-heavy ambience of a closed room under pressure. A "
        "low rumble rises out of silence, holds at its peak with a faint "
        "shimmer, then settles. Close at the ear, one held breath, then a slow "
        "release. A girl's voice, eighteen, sweet and delighted, teasing, in Mandarin: "
        "「你上了一个台阶。炼气二层。半个月。比我预想的快。」 Deep, enclosed, "
        "low-frequency room ambience."
    ),

    "mon_phai_tan_hoang": (
        "10-second wide, empty ambience in the ruins of a martial sect just "
        "before dawn. Close at the ear, quiet breathing and ash shifting. "
        "Further out, wind through broken walls, loose roof tiles sliding. An "
        "old man's voice, around sixty, quiet and kind, close in Mandarin: "
        "「你活下来……就好。」 then 「拿着。护身的药，需要就用。」 Cold, empty, "
        "wide ruined field recording."
    ),

    "binh_minh_ngoc_cot": (
        "10-second high, clean dawn ambience at the mountain gate of a martial "
        "sect. Close at the ear, cloth flaps on a pole and breathing stays "
        "quiet. Far down the valley, a temple bell is struck once and rings "
        "away. A girl's voice, eighteen, sweet and lazy, almost fond, in Mandarin: "
        "「你活过了第一夜。」 then 「在这武林里，你的修为是死罪。藏深一点。」 "
        "Clean, high, open mountain field recording."
    ),

    "dot_pha": (
        "10-second heavy silence in a closed room at night. Close at the ear, "
        "wood creaks as it cools, quiet breathing, a window shutter moves a "
        "fraction. A man's voice, thirty, deep and measured, in Mandarin: 「你上了"
        "台阶。」 then 「但听清楚：这是凡尘。别在人前露剑气。」 Deep, still, "
        "enclosed room ambience."
    ),

    # ---------------------- CẢNH NHÓM "GAP" ----------------------

    "do_tam_mieu": (
        "4-second scene inside a dry stone shrine at night. A heavy man's voice, "
        "around forty, rough and hoarse, pitched low, speaks close and unhurried with a threat "
        "resting under it, in Mandarin: 「又来一只老鼠。」 Behind him, faint wind "
        "moves through a broken doorway. Short, dry stone reverb. Dark, close, "
        "intimate field recording."
    ),

    "kiem_hap": (
        "4-second scene in a cold stone shrine. A wooden box lid snaps open, dry "
        "and sharp, then a cold young male voice speaks close to the ear, quiet "
        "and disembodied, in Mandarin: 「你……和他们不一样。」 Long stone reverb "
        "trails behind it. Cold, still, intimate field recording."
    ),

    "kiem_linh": (
        "5-second scene in a cold stone shrine, air completely still. A man's "
        "voice, thirty, deep and grave, flat and icy, quiet but clear, with a faint spectral edge, "
        "speaks close in Mandarin: 「我是红尘剑灵。」 Long cold stone reverb opens "
        "out behind the voice. Still, spectral, intimate field recording."
    ),

    "kiem_linh_thu": (
        "3-second scene in a still stone shrine. A man's voice, thirty, deep and "
        "grave, flat and icy, speaks close to the ear in Mandarin: 「若我想杀你，"
        "你碰到盒子的那一刻就已经死了。」 Far off, metal rings once. Short stone "
        "reverb. Cold, final, intimate field recording."
    ),

    "kiem_linh_than": (
        "6-second scene in a cold stone hall, dead quiet. A man's voice, thirty, "
        "deep and grave, even and emotionless, speaks close and clear in Mandarin: "
        "「我是红尘剑的剑灵。」 Stone hall reverb stretches behind each phrase. "
        "Cold, hollow, intimate field recording."
    ),

    "kiem_linh_dieu": (
        "4-second scene in a still stone shrine. A man's voice, thirty, deep and "
        "grave, flat and icy, speaks close to the ear in Mandarin: 「我要你走在"
        "红尘之中。」 Very short stone reverb, nothing else in the room. Cold, "
        "quiet, intimate field recording."
    ),

    "kiem_hap_nhan": (
        "4-second scene in a cold stone shrine. A thin blade whispers across "
        "skin, one small sharp metallic sound, then a young man's low voice, "
        "satisfied and final, speaks close in Mandarin: 「成了。」 Quiet stone "
        "sits around it. Cold, final, intimate field recording."
    ),

    "han_lap": (
        "4-second scene on a quiet mountain path in late afternoon. A young man's "
        "voice, eighteen, low and cold, unhurried, speaks without turning around, close to "
        "the ear, in Mandarin: 「跟了我这么久，不累吗？」 Behind him, light wind "
        "moves ridge grass, gravel shifts underfoot. Cool, still, intimate "
        "mountain field recording."
    ),

    "han_lap_2": (
        "5-second scene on a still mountain night. A young man's voice, eighteen, low and "
        "cold, slow, weighing each phrase, speaks close in Mandarin: 「这里的人只看见"
        "一个流浪汉。」 Very quiet night air behind it, one distant insect. Cool, "
        "bare, intimate night field recording."
    ),

    "ngoc_cot": (
        "6-second scene in a small wooden room at night, very still. Close at "
        "the ear, a tiny oil-lamp flame ticks, breathing stays slow, a straw mat "
        "shifts once. Then a girl's voice, eighteen, sweet as honey and just as teasing, close in Mandarin: 「你……终于来了。」 The glowing jade "
        "itself makes no sound at all. Warm, hushed, intimate room field "
        "recording."
    ),

    "tuyet_co": (
        "5-second scene in a wooden room at night with the lamp lit. A girl's voice, eighteen, sweet and sultry, breathy, teasing, speaks close to the ear in Mandarin: 「我先问你——你是谁？」 Under it, a "
        "tiny lamp flame ticks. Warm, hushed, tense intimate field recording."
    ),

    "tuyet_co_canh_giac": (
        "3-second scene in a still night room. A girl's voice, eighteen, sweet and unhurried, teasing, speaks close in Mandarin: 「若我想害你，你"
        "碰到玉的那一刻就已经死了。」 Soft room tone and one unsteady breath "
        "behind. Quiet, cool, intimate room field recording."
    ),

    "tuyet_co_than_phan": (
        "6-second scene in a quiet wooden room at night. A girl's voice, eighteen, sweet and breathy, slow and teasing, as if telling a secret, speaks close to the ear in Mandarin: 「我是雪姬。」 A lamp flame ticks faintly "
        "in still air. Warm, silk-smooth, faintly cold intimate field recording."
    ),

    "tuyet_co_dieu_kien": (
        "4-second scene in a silent night room. A girl's voice, eighteen, sweet and businesslike, teasing under it, speaks close in Mandarin: 「签，"
        "还是不签？」 Only quiet room tone and one breath behind it. Hushed, "
        "tense, intimate room field recording."
    ),

    "tuyet_co_do_du": (
        "5-second scene in a night room, a breath held. Close at the ear, breath "
        "stops and releases slowly, a tiny oil-lamp flame ticks, one dry wooden "
        "joint creaks. A girl's voice, eighteen, sweet and light, as if it "
        "hardly matters, speaks close in Mandarin: 「一部分阳气。」 Tense but "
        "nothing loud. Warm, hushed, suspended intimate room field recording."
    ),

    "tuyet_co_khe_uoc": (
        "4-second scene in a quiet night room. A girl's voice, eighteen, sweet and pleased now, teasing, speaks close in Mandarin: 「好。把手给我。」 "
        "Then a softer breath: 「从今往后，你是主，我是仆。」 The lamp ticks. "
        "Warm, hushed, resolved intimate field recording."
    ),

    "han_lap_gap": (
        "4-second scene on a rocky path behind a mountain at night. A young man's "
        "voice, eighteen, low and cold, level, speaks with his back turned, close in "
        "Mandarin: 「跟了我一路，不累吗？」 Light night wind crosses rock, gravel "
        "shifts. Cool, open, intimate night field recording."
    ),

    "han_lap_that": (
        "6-second scene on a very still mountain night. A young man's voice, "
        "eighteen, low and cold, slow, speaks close in Mandarin: 「你可知道，我会"
        "怎么对待知道太多的人？」 Dead air around it, no wind, no insect. Bare, "
        "exposed, intimate night field recording."
    ),

    "han_lap_cuoi_tru": (
        "4-second scene in quiet night air. A young man's voice, eighteen, low "
        "and cold, unimpressed, speaks close in Mandarin: 「碰巧的人，不会天没亮"
        "就跟着别人上后山。」 Still night behind it. Cool, thin, intimate night "
        "field recording."
    ),

    "han_lap_hoi_nguoc": (
        "6-second scene on a still mountain night. A young man's voice, "
        "eighteen, low and cold, an edge under it, speaks close to the ear in "
        "Mandarin: 「今晚谁都有秘密。我不问你，你也别问我。」 Faint wind far "
        "off. Cool, sharp, intimate night field recording."
    ),

    "han_lap_bau_nuoc": (
        "5-second scene on a night mountain, very quiet. A water flask cap "
        "opens, one swallow, then a young man's voice, eighteen, low and cool, almost warm, "
        "speaks close in Mandarin: 「你和这里的人不一样。」 Light wind behind. "
        "Cool, quiet, almost warm intimate field recording."
    ),
}
