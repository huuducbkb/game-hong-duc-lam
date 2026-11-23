"""Prompt tạo tiếng cho từng cảnh, viết theo kiểu câu chảy.

Mỗi prompt làm đúng bốn việc:

1. Mở bằng một câu khai báo đầy đủ: dài bao lâu, chất âm gì, không khí gì, ở đâu.
2. Tả tiếng trong câu liền mạch. Khoảng cách gắn tự nhiên vào câu ("close at the
   ear", "a few paces off", "far behind") chứ không chia thành ba mục có dấu hai
   chấm như bản cũ.
3. Chốt bằng một thẻ chất âm ngắn, kiểu "Warm, tranquil, intimate field
   recording." Đây là chỗ máy lấy không khí chung cho cả file.
4. Dưới 450 ký tự — trần cứng của ô prompt ElevenLabs Sound Effects.

Đã bỏ lối cũ "No music, no speech, seamless loop." lặp ở cuối mọi prompt. Câu đó
vừa rập khuôn vừa sai: game phát mỗi file một lần rồi thôi, không lặp. Ghi
"seamless loop" là bảo máy làm bản nền lặp, ngược với cách game dùng.

Cảnh có thoại (nhóm "gap") giữ đúng MỘT câu tiếng Hoa trong ngoặc 「」, lấy câu
đầu tiên của đoạn truyện, kèm tuổi và chất giọng để máy không tự đoán.
"""

PROMPT = {

    # ------------------------------ CHỢ ------------------------------

    "cho_01": (
        "10-second dense, lively early-morning ambience in a crowded corner of "
        "a small town market. Cart wheels creak over packed earth, clay jars "
        "knock together, coins drop into a palm, cloth brushes past the ear. A "
        "few paces off, feet cross and a stool is dragged; laughter rises once "
        "and settles. Far behind, a dog answers. Warm, human, close-recorded "
        "market field recording with soft crowd damping."
    ),

    "cho_02": (
        "10-second hushed, secretive night ambience at the mouth of a narrow "
        "alley behind a market. Ten paces in, men sit around a small fire: wood "
        "crackles, a stick pokes the embers, spit hisses, someone coughs and "
        "sighs low. Their voices reach the ear softened, coming back off the "
        "close walls. Near at hand, quiet breathing and a boot scuffing grit. "
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
        "stretched: fire roaring, timber cracking, structures folding, one far "
        "shout, a horn. Close at the ear, wind combs the ridge grass and cloth "
        "lifts. The valley is too wide to answer back. Cold, open, cinematic "
        "mountain field recording."
    ),

    "tran_lua_2": (
        "10-second chaotic, close night ambience inside a burning town street. "
        "Fire roars through a wooden house beside the ear, roof beams crack, a "
        "blade sweeps through air, steel rings on steel, boots hammer stone, "
        "breath comes hard. Ahead, a wall comes down and horses pass. Behind, a "
        "shout. House fronts throw every sound back fast and hard. Immersive, "
        "hot, urgent field recording."
    ),

    "tran_lua_3": (
        "10-second frantic, enclosed night ambience at the shattered gate of a "
        "martial sect under assault. Close by, a heavy gate splinters, hinges "
        "tear, boots stamp broken planks, breath rasps, one blade turns another "
        "aside. Further back, bouncing off stone, many men move at once, "
        "grunts, a hoarse shout. Beyond the gate, fire. Walled in, hard "
        "reflections. Brutal, enclosed stone courtyard field recording."
    ),

    "cong_dong_doi_mat": (
        "10-second tense, near-silent ambience at a broken gate in the instant "
        "before blades meet. Close at the ear, slow breath and cloth shifting "
        "as weight settles. A few paces ahead, their breathing, a boot scuffing "
        "stone, a blade drawn an inch. Behind, wind through the gate. Long gaps "
        "between sounds, and the stone carries every small one. Cold, coiled, "
        "intimate stone field recording."
    ),

    "cong_dong_giau": (
        "10-second controlled, suppressed ambience at a gate. Close in, fast "
        "shallow breathing, a blade turned aside, boots sliding backwards on "
        "stone, cloth snapping, a short grunt. Off to the side, other men move "
        "and breathe, one wordless shout. Stone walls close on both sides, so "
        "small sounds come back doubled. Restrained, dry, enclosed stone field "
        "recording."
    ),

    "cong_dong_toan_luc": (
        "10-second sudden, loud ambience at a gate. Close in, one heavy impact, "
        "air torn, dust and gravel thrown, stone struck, breath bursting out, a "
        "loud grunt. Around and further off, the exchange carries on, then a "
        "brief stunned quiet, one shout from onlookers. The gate walls catch it "
        "all and send it back a beat later. Punchy, physical, enclosed stone "
        "field recording."
    ),

    "cong_dong_quyen": (
        "10-second dry, close bare-handed combat ambience at a gate. Right at "
        "the ear, a fist strikes a chest, a forearm blocks, sleeves snap, feet "
        "pivot and stamp stone, steady breathing through the nose, a short "
        "exhale on each strike. Further off, boots on stone, a grunt. The stone "
        "under and behind returns every hit a little late. Tight, dry, enclosed "
        "stone field recording."
    ),

    "cong_dong_hung_ba": (
        "10-second courtyard ambience built on one shout and its echo. Close at "
        "the ear, one breath held. A single raw wordless shout goes out, comes "
        "back off the far wall, and everything stops: blades quiet, footsteps "
        "halt, wind, many men holding still. The wall supplies the depth, a "
        "long hard reflection. Tense, wide, open stone courtyard field "
        "recording."
    ),

    "hoa_truong_cuu": (
        "10-second urgent ambience inside a burning building. Fire close and "
        "filling the space: roaring, crackling, timber snapping, embers "
        "falling. At the ear, heavy effort breathing, wood levered and thrown "
        "aside, a weak hoarse moan. Outside, muffled through the fire, a shout. "
        "Thick, smoke-damped, claustrophobic field recording."
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
        "move. A few paces left and right, wooden staffs strike each other, "
        "staffs hit the ground in unison, a sharp whistle cuts across. "
        "Overhead, banners flap. Open yard, where far sounds thin out. Rhythmic, "
        "busy, hot open-air field recording."
    ),

    "san_tap_chen_ep": (
        "10-second hostile, quiet ambience in a training yard as a ring of "
        "students closes in. Low laughter, a mocking hum, feet shuffling as "
        "they circle, a staff tapping ground, someone spitting. Close, all "
        "around the head. The ring of bodies soaks the sound up instead of "
        "bouncing it. The rest of the training carries on further off. Tight, "
        "unpleasant, close-recorded yard ambience."
    ),

    "san_tap_cai_lai": (
        "10-second ambience of a training yard going silent after one slap. A "
        "sharp wordless angry shout, then a flat slap lands close, and the "
        "whole yard goes completely quiet. After a beat, a low hum of reaction "
        "spreads through the crowd, sound only. Far off, the rest of the "
        "training has stopped too. The quiet leans in. Sharp, still, open-yard "
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
        "in, a small shovel bites soft earth, soil pours out, roots snap, "
        "leaves are pushed aside, breathing quickens, cloth rustles. Overhead, "
        "the old tree's leaves move. Far off, a dog. Soft earth swallows the "
        "digging, the leaves overhead catch the rest. Muffled, secretive, close "
        "night field recording."
    ),

    # --------------------------- VƯỜN THUỐC ---------------------------

    "vuon_thuoc_gap": (
        "10-second warm, secluded morning ambience in a walled herb garden. A "
        "gentle breeze rustles dense herbal leaves, brushing softly against each "
        "other and against cloth. A bee buzzes close by, weaving past the "
        "plants, sparse delicate insects behind it. Dry stems snap underfoot. "
        "Beyond the wall, softened by distance, wooden staffs strike and a "
        "sharp whistle sounds. Warm, tranquil, intimate walled-garden field "
        "recording."
    ),

    "vuon_thuoc_hoi": (
        "10-second tense, quiet ambience in a walled herb garden, two people "
        "standing close and wordless. What carries is the shape of it: slow dry "
        "breathing close on the left, a younger breath held tight, a foot "
        "shifting, cloth. Behind them, further off, leaves move, insects, a "
        "bundle of herbs being tied. The wall holds it all in, low. Warm, "
        "hushed, walled-in garden field recording."
    ),

    "vuon_thuoc_im": (
        "10-second deliberate stillness in a walled herb garden, wordless. "
        "Close at the ear, a bundle of dried herbs is handled and quiet "
        "breathing. Further off, leaves move in a light wind, insects, one bird "
        "far away. Long quiet stretches open between each small sound. The wall "
        "holds everything in, so the quiet has an edge. Warm, still, walled-in "
        "garden field recording."
    ),

    "vuon_thuoc_ngoc": (
        "10-second secretive ambience in a walled herb garden where a heavy "
        "object is handled. Close in, a jade object is set down on wood with a "
        "solid knock, cloth is unwrapped, fingers brush stone, a bundle of "
        "herbs is laid aside. Near the ear, two low unhurried breaths. Behind, "
        "leaves and insects. The wall keeps it in and small. Warm, hushed, "
        "close-recorded garden ambience."
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
        "shrine. Close in, boots slip on stone, bodies collide, cloth tears, a "
        "blade swings and misses, one heavy impact, then weight drops to the "
        "floor. One hoarse shout, cut short. Further off, outside, a door and "
        "running feet. Then only echo. Hard, resonant, enclosed stone field "
        "recording."
    ),

    "tu_khiem": (
        "10-second precise ambience of sword practice in a shrine at night. "
        "Close at the ear, a blade cuts air in a long clean arc, steel rings "
        "faintly as it turns, the guard shifts in the hand, bare feet pivot on "
        "stone, breathing stays even. Further off, the room answers each swing "
        "with its own reverb, then near-silence. Cold, sharp, clean stone field "
        "recording."
    ),

    # ---------------------------- TÂN XÁ ----------------------------

    "tan_xa_dem": (
        "10-second small, dry ambience of a cramped wooden dormitory at night, "
        "someone lying awake. Close at the ear, a bed frame creaks under small "
        "movement, cloth shifts, breathing stays slow and even. Outside the "
        "paper window, muffled and further, crickets, a frog, a dog far away, "
        "light wind. The small room keeps everything close. Dry, hushed, "
        "intimate room field recording."
    ),

    "dem_tap_kich": (
        "10-second ambience that turns from quiet night into chaos. Inside a "
        "wooden dormitory, close at the ear, insects, a bed frame, quiet "
        "breathing; further off, wind and timber settling. Then a horn cuts in "
        "from the forest and everything breaks at once: fire igniting, blades, "
        "running feet, a gate slamming, one shout. Sharp contrast, wide to "
        "close. Tense, cinematic night field recording."
    ),

    "tan_hoang": (
        "10-second heavy, empty ambience among ruins just before dawn after a "
        "battle. Fire still smoulders: low crackling, a beam settling, ash "
        "shifting. Wind crosses collapsed walls. Close and quiet, slow footsteps "
        "of men carrying something heavy, setting it down, one long breath let "
        "go, a broken sob far off that stops. Collapsed walls scatter the "
        "sound, so it thins and dies. Cold, exhausted, ruined open-air field "
        "recording."
    ),

    "binh_minh": (
        "10-second clean dawn ambience over a small town the morning after "
        "trouble. Close in, birds start up one at a time, a rooster far off, "
        "light wind moves dust and loose paper. Somewhere a shutter opens, a "
        "bucket of water is poured, a broom works. Almost nobody awake, the town "
        "still asleep. Open morning air, each sound landing clean and stopping. "
        "Clean, calm, open-air dawn field recording."
    ),

    "tan_xa_sang": (
        "10-second ordinary morning ambience in a martial sect dormitory. Close "
        "in, a wooden door slides open, sandals on stone, water poured from a "
        "bucket, a bed frame creaks, someone coughs, cloth pulled on. Outside, "
        "further and softened, a staff tapped on the ground, footsteps, a sharp "
        "whistle from the yard. Unremarkable, easy, lived-in room field "
        "recording."
    ),

    "quan_nuoc": (
        "10-second warm, crowded ambience in a dark corner of a roadside tea "
        "house. Close at the ear, a clay cup is set on wood, tea poured, a "
        "kettle, coins counted, a stool scraping. Around, at other tables, a low "
        "hum too far to be anything, laughter once, a hand slapped on a table. A "
        "low ceiling and close walls press the hum down around the head. Warm, "
        "crowded, close-recorded tea house ambience."
    ),

    "tan_xa_song_tu": (
        "10-second extremely quiet, intimate ambience of lying still in a dark "
        "room at night. At the ear, slow breathing, a pulse, cloth shifting, a "
        "wooden bed taking weight, and a faint hum that seems to come from "
        "inside the room rather than outside it. Far off, crickets. The small "
        "room holds the sound against you. Private, close, still, intimate room "
        "field recording."
    ),

    "tan_xa_kho_tu": (
        "10-second raw, quiet ambience of sitting in the dark after failure. "
        "Close in, breathing too fast and too heavy, then a long shaky exhale, "
        "then silence. A hand pressed against a chest, cloth twisted. Further "
        "off, outside the room, a wooden floor creaks as someone else shifts "
        "weight. The room is small enough to send the breathing back. Dry, bare, "
        "intimate room field recording."
    ),

    "tan_xa_suyt_lo": (
        "10-second tight, tense ambience of held breath in a dark dormitory. "
        "Close in, breath held, then released very carefully, cloth pulled "
        "tight. Further off, outside the door on the wooden walkway, coming "
        "closer, slow deliberate footsteps that pause right outside, then move "
        "away and fade. Then only insects. The thin wall carries it through too "
        "clearly. Tight, hushed, intimate room field recording."
    ),

    "tan_xa_dot_pha": (
        "10-second deep, sub-heavy ambience of a closed room under pressure. A "
        "low rumble rises out of silence, holds at its peak with a faint "
        "shimmer, then settles back into stillness. Close at the ear, one held "
        "breath, then a slow release. The walls take the rumble and give it "
        "back. Far off, the building settles around it. Deep, enclosed, "
        "low-frequency room ambience."
    ),

    "mon_phai_tan_hoang": (
        "10-second wide, empty ambience in the ruins of a martial sect just "
        "before dawn. Close at the ear, quiet breathing and ash shifting. "
        "Further out, crossing open ground through broken walls, wind, a wall "
        "section coming down somewhere, loose roof tiles sliding. Far off, slow "
        "footsteps of men carrying something heavy, one long breath. Open "
        "ruins, sound spreading and thinning. Cold, empty, wide ruined field "
        "recording."
    ),

    "binh_minh_ngoc_cot": (
        "10-second high, clean dawn ambience at the mountain gate of a martial "
        "sect. Close at the ear, cloth flaps on a pole and breathing stays "
        "quiet. Further out, mountain wind moves steadily and birds wake. Far "
        "down the valley, a temple bell is struck once and rings away. The "
        "courtyard is empty. High open air, so the bell runs away down the "
        "valley. Clean, high, open mountain field recording."
    ),

    "dot_pha": (
        "10-second heavy silence in a closed room at night. Close at the ear, "
        "wood creaks as it cools, quiet breathing, a window shutter moves a "
        "fraction. Further off, through the wall, a faint low presence in the "
        "air like pressure. Long stretches pass with only the room's own "
        "settling. The closed room presses back, so the silence has weight. "
        "Deep, still, enclosed room ambience."
    ),

    # ---------------------- CẢNH CÓ MỘT CÂU THOẠI ----------------------

    "do_tam_mieu": (
        "4-second scene inside a dry stone shrine at night. A heavy man's "
        "voice, rough and hoarse, pitched low, speaks close and unhurried with "
        "a threat resting under it, in Mandarin: 「又来一只老鼠。」 Behind him, "
        "faint wind moves through a broken doorway. Short, dry stone reverb. "
        "Dark, close, intimate field recording."
    ),

    "kiem_hap": (
        "4-second scene in a cold stone shrine. A wooden box lid snaps open, "
        "dry and sharp, then a cold young male voice speaks close to the ear, "
        "quiet and disembodied, in Mandarin: 「你……和他们不一样。」 Long stone "
        "reverb trails behind it. Cold, still, intimate field recording."
    ),

    "kiem_linh": (
        "5-second scene in a cold stone shrine, air completely still. A young "
        "man's voice, flat and icy, quiet but clear, with a faint spectral "
        "edge, speaks close in Mandarin: 「我是红尘剑灵。」 Long cold stone reverb "
        "opens out behind the voice. Still, spectral, intimate field recording."
    ),

    "kiem_linh_thu": (
        "3-second scene in a still stone shrine. A young man's voice, wary and "
        "dry, carrying a short humourless laugh inside the words, speaks close "
        "to the ear in Mandarin: 「信你？」 Far off, metal rings once. Short stone "
        "reverb. Dry, guarded, intimate field recording."
    ),

    "kiem_linh_than": (
        "6-second scene in a cold stone hall, dead quiet. A young man's voice, "
        "even and emotionless, measured, speaks close and clear in Mandarin: "
        "「我是红尘剑的剑灵。」 Stone hall reverb stretches behind each phrase. "
        "Cold, hollow, intimate field recording."
    ),

    "kiem_linh_dieu": (
        "4-second scene in a still stone shrine. A young man's voice, cautious "
        "and low, choosing each word carefully, speaks close to the ear in "
        "Mandarin: 「我要问清楚。」 Very short stone reverb, nothing else in the "
        "room. Careful, quiet, intimate field recording."
    ),

    "kiem_hap_nhan": (
        "4-second scene in a cold stone shrine. A thin blade whispers across "
        "skin, one small sharp metallic sound, then a young man's low voice, "
        "satisfied and final, speaks close in Mandarin: 「成了。」 Quiet stone "
        "sits around it. Cold, final, intimate field recording."
    ),

    "han_lap": (
        "4-second scene on a quiet mountain path in late afternoon. A man's "
        "voice, low and flat, unhurried, speaks without turning around, close "
        "to the ear, in Mandarin: 「跟了我这么久，不累吗？」 Behind him, light wind "
        "moves ridge grass, gravel shifts underfoot, cloth stirs. Cool, still, "
        "intimate mountain field recording."
    ),

    "han_lap_2": (
        "5-second scene on a still mountain night. A man's voice, low and "
        "even, slow, weighing each phrase, speaks close in Mandarin: "
        "「这里的人只看见一个流浪汉。」 Very quiet night air behind it, one "
        "distant insect. Cool, bare, intimate night field recording."
    ),

    "ngoc_cot": (
        "6-second scene in a small wooden room at night, very still. Close at "
        "the ear, a tiny oil-lamp flame ticks and crackles, breathing stays slow "
        "and quiet, a straw mat shifts once. Then a young man's voice, barely "
        "above a whisper, half to himself, in Mandarin: 「你……是什么？」 The "
        "glowing jade itself makes no sound at all. Warm, hushed, intimate room "
        "field recording."
    ),

    "tuyet_co": (
        "5-second scene in a wooden room at night with the lamp lit. A young "
        "man's voice, startled and unsteady, breath catching first, speaks "
        "close to the ear in Mandarin: 「你……你是谁？怎么会在玉里？」 Under it, a "
        "tiny lamp flame ticks. Warm, hushed, tense intimate field recording."
    ),

    "tuyet_co_canh_giac": (
        "3-second scene in a still night room. A young man's voice, guarded, a "
        "dry forced laugh at the front of it, speaks close in Mandarin: "
        "「需要我？」 Soft room tone and one unsteady breath behind. Quiet, wary, "
        "intimate room field recording."
    ),

    "tuyet_co_than_phan": (
        "6-second scene in a quiet wooden room at night. A woman's voice, soft "
        "and silky with cold underneath, slow as if telling an old story, "
        "speaks close to the ear in Mandarin: 「我是雪姬。」 A lamp flame ticks "
        "faintly in still air. Warm, silk-smooth, faintly cold intimate field "
        "recording."
    ),

    "tuyet_co_dieu_kien": (
        "4-second scene in a silent night room. A young man's voice, trembling "
        "slightly, trying to hold steady, speaks close in Mandarin: "
        "「我要问清楚。」 Only quiet room tone and one breath behind it. Hushed, "
        "tense, intimate room field recording."
    ),

    "tuyet_co_do_du": (
        "5-second scene in a night room, a breath held. Close at the ear, breath "
        "stops and releases slowly, a tiny oil-lamp flame ticks, one dry wooden "
        "joint creaks. Tense but nothing loud. Warm, hushed, suspended intimate "
        "room field recording."
    ),

    "tuyet_co_khe_uoc": (
        "4-second scene in a quiet night room. A young man's voice, low and "
        "firm, decision already made, speaks close in Mandarin: 「我签。」 A soft "
        "female breath answers, barely audible, and the lamp ticks. Warm, "
        "hushed, resolved intimate field recording."
    ),

    "han_lap_gap": (
        "4-second scene on a rocky path behind a mountain at night. A man's "
        "voice, low and even, calm, speaks with his back turned, close in "
        "Mandarin: 「跟了我一路，不累吗？」 Light night wind crosses rock, gravel "
        "shifts. Cool, open, intimate night field recording."
    ),

    "han_lap_that": (
        "6-second scene on a very still mountain night. A young man's voice, "
        "gone hoarse with tension, quiet but deliberate, speaks close in "
        "Mandarin: 「我知道你的未来。」 Dead air around it, no wind, no insect. "
        "Bare, exposed, intimate night field recording."
    ),

    "han_lap_cuoi_tru": (
        "4-second scene in quiet night air. A young man's voice, an awkward "
        "laugh first, then light and evasive, speaks close in Mandarin: "
        "「我只是碰巧路过罢了。」 Still night behind it. Cool, thin, intimate "
        "night field recording."
    ),

    "han_lap_hoi_nguoc": (
        "6-second scene on a still mountain night. A young man's voice, sharp "
        "and probing, an edge under it, speaks close to the ear in Mandarin: "
        "「那你又是谁？」 Faint wind far off. Cool, sharp, intimate night field "
        "recording."
    ),

    "han_lap_bau_nuoc": (
        "5-second scene on a night mountain, very quiet. A water flask cap "
        "opens, one swallow, then a man's voice, low and quiet, almost warm, "
        "speaks close in Mandarin: 「你和这里的人不一样。」 Light wind behind. "
        "Cool, quiet, almost warm intimate field recording."
    ),
}
