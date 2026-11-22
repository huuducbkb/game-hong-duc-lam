"""Prompt tạo tiếng cho từng cảnh, viết theo góc người chơi.

Nguyên tắc, rút ra từ chính lời anh: người chơi phải nghe như đang ĐỨNG Ở ĐÓ,
chứ không phải nghe một bản nhạc. Nên mỗi prompt mở đầu bằng vị trí người chơi
và khoảng cách tới nguồn tiếng, rồi mới tới các lớp tiếng. Cùng là chợ mà chợ
sớm đông đặc khác chợ chiều vắng tanh — khác nhau ở chỗ người chơi ngồi đâu và
còn ai ở đó.

Bốn quy tắc lặp lại trong mọi prompt:

1. `no music` — không nhạc, không giai điệu, không tiếng đọc. Đây là tiếng của
   không gian, không phải nhạc nền game.
2. Tiếng người là TIẾNG VIỆT. Prompt ghi thẳng "Vietnamese" ở mọi chỗ có giọng
   nói, vì nếu không ghi thì công cụ sẽ mặc định ra tiếng Anh.
3. Mười giây, lặp được. Cảnh trong game chỉ 10 giây nên file phải quay vòng
   không nghe mối nối.
4. Dưới 450 ký tự. Đây là trần cứng của ô prompt trên ElevenLabs Sound
   Effects — dài hơn thì trang báo lỗi và không cho tạo. Trần này áp cho cả
   trang lẫn API.

Phần lớn cảnh có người nói thì cố ý KHÔNG rõ chữ — người chơi đứng xa, hoặc
đang nghe lén, hoặc giữa chợ ồn. Chữ nghĩa rõ ràng sẽ thành phim truyền thanh,
không còn là không gian. Không có lời thoại kèm theo: chỉ cần tiếng nền.

Tránh chữ dễ bị bộ lọc chặn: không tả thương tích, không tả xác, không lồng
tiếng trẻ con, không dùng chữ "violent". Tả ĐỘNG TÁC cụ thể (a blade turning
another aside, boots on stone) thay vì tả mức độ dữ dội — vừa dễ qua bộ lọc,
vừa ra tiếng đúng hơn.
"""

PROMPT = {

    # ------------------------------ CHỢ ------------------------------

    "cho_01": (
        "Vietnamese-language ambience, no music. The player lies on the "
        "ground in a corner of a crowded morning market, so every sound "
        "arrives low, at ear level. Close and loud: a porter shouting in "
        "Vietnamese as he shoves past, cart wheels creaking on packed earth, "
        "baskets and clay jars knocking, a vendor calling prices. Behind "
        "that: overlapping haggling in Vietnamese, a horse stamping, a dog "
        "barking. Dense, crowded. Loops seamlessly over ten seconds."
    ),

    "cho_02": (
        "Vietnamese-language ambience, no music. The player stands at the "
        "mouth of a narrow alley behind the market, ten metres from three men "
        "sitting around a small fire. Their voices reach him muffled by the "
        "walls: low Vietnamese speech, three voices taking turns, never clear "
        "enough for whole sentences, only the rhythm of men trading rumours "
        "and one clear phrase, 'Da Lang Bang'. Near him: fire crackling. "
        "Loops seamlessly over ten seconds."
    ),

    "cho_03": (
        "Vietnamese-language ambience, no music. The player sits at the edge "
        "of a market emptying at dusk. The crowd is gone: no calling out, no "
        "haggling. What is left is sparse and tired - a stall folded and "
        "stacked, crates dragged, a broom sweeping packed earth, slow "
        "footsteps walking away. Two or three Vietnamese voices talk quietly "
        "behind him, too far for words, with long pauses. Dry wind moves "
        "loose paper. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TRẬN LỬA ------------------------------

    "tran_lua": (
        "Vietnamese-language ambience, no music. The player stands high on a "
        "mountain path at night, looking down at a town below. Distance thins "
        "everything: a horn blowing from the valley, far-off shouting in "
        "Vietnamese, fire roaring, wooden structures collapsing, timber "
        "cracking. The closest sound is wind on the ridge, moving grass and "
        "the player's own clothing. Nothing is near him - he is only "
        "watching. Loops seamlessly over ten seconds."
    ),

    "tran_lua_2": (
        "Vietnamese-language ambience, no music. The player runs through a "
        "burning town street at night, inside the chaos. Close: fire roaring "
        "through a wooden house, roof beams cracking, a blade sweeping "
        "through air, steel ringing on steel, boots hammering stone, a man "
        "shouting in Vietnamese to keep moving. Mid-distance: more clashes, a "
        "wall coming down, horses. Everything near and moving. Loops "
        "seamlessly over ten seconds."
    ),

    "tran_lua_3": (
        "Vietnamese-language ambience, no music. The player is at the "
        "shattered gate of a martial sect during a night assault. Close: a "
        "heavy gate splintering and sagging, hinges tearing, boots stamping "
        "over broken planks and stone, hard breathing, one blade turning "
        "another aside. All around: many men moving at once, Vietnamese "
        "shouts of orders, a name called out. Under it, fire. Walled in. "
        "Loops seamlessly over ten seconds."
    ),

    # ------------------------------ CỔNG ĐÔNG ------------------------------

    "cong_dong_doi_mat": (
        "Vietnamese-language ambience, no music. The player stands at a "
        "broken gate facing several enemies only a few metres away, in the "
        "instant before blades meet. Almost silent, and the silence is the "
        "point: wind moving through the gate, cloth shifting as men adjust "
        "their stance, slow controlled breathing, one boot scuffing stone, a "
        "blade drawn an inch from its scabbard. No impact yet, no shouting. "
        "Loops seamlessly over ten seconds."
    ),

    "cong_dong_giau": (
        "Vietnamese-language ambience, no music. The player fights at a gate "
        "while deliberately holding his strength back. Close: fast shallow "
        "breathing, a blade parried and turned aside, boots sliding backwards "
        "on stone, cloth snapping, a grunt with effort. Mid-distance: other "
        "men fighting, Vietnamese voices calling to each other. Nothing "
        "explosive - every sound is controlled, suppressed, deliberately "
        "small. Loops seamlessly over ten seconds."
    ),

    "cong_dong_toan_luc": (
        "Vietnamese-language ambience, no music. The player stops holding "
        "back at a gate. Loud and sudden: one heavy impact, air torn, dust "
        "and gravel thrown, stone struck, breath bursting out. Around him the "
        "exchange continues - Vietnamese shouts, then a brief stunned quiet "
        "as onlookers react. The loudest of this group. Loops seamlessly over "
        "ten seconds."
    ),

    "cong_dong_quyen": (
        "Vietnamese-language ambience, no music. The player fights "
        "bare-handed at close range at a gate. Close and dry: a fist striking "
        "a chest, a forearm blocking, sleeves snapping, feet pivoting and "
        "stamping on stone, steady breathing through the nose, a short exhale "
        "on every strike. No metal anywhere. Around him other men move at the "
        "gate - Vietnamese shouts, boots on stone, blades further off. Loops "
        "seamlessly over ten seconds."
    ),

    "cong_dong_hung_ba": (
        "Vietnamese-language ambience, no music. The player shouts a "
        "challenge across a courtyard in the middle of a fight. One "
        "Vietnamese voice, loud and raw, calls out a name and it carries and "
        "echoes off the walls. Then everything stops: blades go quiet, "
        "footsteps halt, and there is only the echo dying away, wind, and the "
        "sound of many men holding still. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ HỎA TRƯỜNG CỨU NGƯỜI ------------------------------

    "hoa_truong_cuu": (
        "Vietnamese-language ambience, no music. The player is inside a "
        "burning building pulling someone out. Fire is the main sound and it "
        "is close: roaring, crackling, timber snapping, embers falling, smoke "
        "moving. Close to the player: heavy effort breathing, wood levered "
        "and thrown aside, a weak hoarse voice in Vietnamese saying thank "
        "you. Vietnamese shouting from outside, muffled by the fire. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ ĐƯỜNG MÒN NÚI ------------------------------

    "duong_mon_nui": (
        "Ambience, no music, no human voices. The player walks a narrow "
        "mountain trail at dusk. Close: boots on loose gravel, dry grass "
        "brushing against his legs, his own breathing. Around him: wind "
        "moving through tall grass, crickets starting up, a night bird "
        "flapping suddenly close and then gone. Wide, open, cold air. Loops "
        "seamlessly over ten seconds."
    ),

    "khe_nui_dem": (
        "Ambience, no music, no human voices. The player stands at the mouth "
        "of a narrow rock ravine at night. The ravine turns the wind into "
        "something like sighing: air forced through the gap, rising and "
        "falling, echoing back off wet stone. Close: a few drops of water "
        "falling into a pool, sparse insects, the player's own breathing. "
        "Narrow, cold, enclosed. Loops seamlessly over ten seconds."
    ),

    "khe_nui_chon": (
        "Ambience, no music, no human voices. The player digs in a mountain "
        "ravine at night. Close and physical: a shovel blade cutting wet "
        "soil, gravel and small stones sliding, earth landing on a pile, "
        "heavy breathing with effort, the shovel scraping rock. Behind it: "
        "wind through the ravine gap, distant insects. Quiet work done in a "
        "hurry. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ SÂN TẬP ------------------------------

    "san_tap_ngay": (
        "Vietnamese-language ambience, no music. The player stands in a large "
        "training yard at midday. Dozens of students train at once: wooden "
        "staffs striking each other, staffs hitting the ground in unison, "
        "bare feet stamping packed earth, breath forced out on each move, an "
        "instructor counting cadence in Vietnamese, someone shouting a "
        "correction. Banners flapping above. Dense, hot, rhythmic. Loops "
        "seamlessly over ten seconds."
    ),

    "san_tap_chen_ep": (
        "Vietnamese-language ambience, no music. The player stands in a "
        "training yard while a ring of students gathers around him. Nobody is "
        "loud, and that is what makes it hostile: low laughing, mocking "
        "comments in Vietnamese just loud enough to hear, feet shuffling as "
        "people circle him, a staff tapping the ground, someone spitting. The "
        "rest of the training carries on further away. Loops seamlessly over "
        "ten seconds."
    ),

    "san_tap_cai_lai": (
        "Vietnamese-language ambience, no music. The player has just talked "
        "back in a training yard. One Vietnamese voice rises sharply in "
        "anger, a flat slap lands, and then the whole yard goes completely "
        "quiet. After a beat, low murmuring in Vietnamese spreads through the "
        "crowd - not words, only reaction. A staff is picked up off the "
        "ground. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ SÂN SAU ------------------------------

    "san_sau_luyen_dem": (
        "Ambience, no music, no voices. The player practises alone in a back "
        "yard late at night and has to stay silent. Everything is "
        "deliberately small: bare feet on packed earth, cloth moving, breath "
        "held and released through the nose, a fist passing through air, a "
        "quiet landing after a step. Far off, insects and one dog. Loops "
        "seamlessly over ten seconds."
    ),

    "san_sau_anh_sang": (
        "Ambience, no music, no human voices. The player stands under a huge "
        "old tree in a back yard at night. Overhead: leaves moving in a light "
        "wind, a thick branch creaking slowly, leaves letting go and landing. "
        "Around: crickets, damp air, one insect very close to the ear. Very "
        "still, very quiet, faintly uneasy. Loops seamlessly over ten "
        "seconds."
    ),

    "san_sau_chon_lai": (
        "Ambience, no music, no human voices. The player digs in a back yard "
        "at night, in a hurry. Close: a small shovel biting into soft earth, "
        "soil poured out, roots snapping, leaves pushed aside, fast "
        "breathing, cloth rustling. Overhead, the old tree's leaves moving. "
        "Somewhere far, a dog. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ VƯỜN THUỐC ------------------------------

    "vuon_thuoc_gap": (
        "Ambience, no music. The player walks into a walled herb garden in "
        "the morning. Close: leaves brushing against each other and against "
        "his clothing, a bee passing close, dry stems snapping underfoot, a "
        "bird landing on the wall and calling twice. Beyond the wall, the "
        "muffled rhythm of a training yard - staffs and counting, softened by "
        "distance. No voices near the player. Loops seamlessly over ten "
        "seconds."
    ),

    "vuon_thuoc_hoi": (
        "Vietnamese-language ambience, no music. Two people talk in a walled "
        "herb garden: the player and an old man. Both speak Vietnamese, low "
        "and unhurried, with long pauses. The old man's voice is dry and "
        "slow; the player's is younger and tense. Words are mostly not clear "
        "- the tone is what matters, a question being pressed and not "
        "answered. Behind them, leaves moving, insects, a bundle of herbs "
        "being tied. Loops seamlessly over ten seconds."
    ),

    "vuon_thuoc_im": (
        "Ambience, no music, no human voices at all. The player sits in a "
        "walled herb garden and says nothing. Only: leaves moving in a light "
        "wind, a bundle of dried herbs being handled, insects, one bird far "
        "away. Long stretches where almost nothing happens. This emptiness is "
        "deliberate, not a broken file. Loops seamlessly over ten seconds."
    ),

    "vuon_thuoc_ngoc": (
        "Vietnamese-language ambience, no music. In a walled herb garden "
        "someone handles a heavy object. Close: a stone or jade object set "
        "down on wood with a solid knock, cloth unwrapped, fingers brushing "
        "stone, a bundle of herbs laid aside. Two Vietnamese voices talk "
        "quietly nearby, calm and unclear. Behind: leaves, insects. Low and "
        "secretive. Loops seamlessly over ten seconds."
    ),

    "vuon_thuoc_dem": (
        "Ambience, no music, no human voices. The player digs in a herb "
        "garden at night. The soil is soft and full of roots: a small tool "
        "cutting in, roots snapping, earth poured out, leaves swept aside, "
        "breath held. Wet garden air, insects, the stillness of a place where "
        "a flower has just opened. Quiet and careful. Loops seamlessly over "
        "ten seconds."
    ),

    # ------------------------------ MIẾU ------------------------------

    "mieu_hoang": (
        "Ambience, no music, no human voices. The player stands outside a "
        "ruined shrine at night, watching it. Wind pushes through broken "
        "walls and gaps, whistling low and then dropping away. Loose roof "
        "tiles shift. Crickets in the grass. A piece of wall crumbles "
        "somewhere. Vast, empty, cold - the player is still outside, not yet "
        "in. Loops seamlessly over ten seconds."
    ),

    "mieu_trong": (
        "Ambience, no music, no human voices. The player is inside a small "
        "stone shrine at night. The room itself is the sound: a long natural "
        "reverb, air moving through the doorway, a draft pushing dust across "
        "stone, a loose tile ticking, the player's own breath, and a single "
        "footstep echoing longer than it should. Very few events, but never "
        "silent. Cold stone. Loops seamlessly over ten seconds."
    ),

    "doat_hop": (
        "Ambience, no music. The player struggles for a box inside a stone "
        "shrine. Close: boots slipping on stone, bodies colliding, cloth "
        "tearing, a blade swung and missing, one heavy impact, then weight "
        "dropping onto the floor with the stone room carrying the sound. One "
        "hoarse voice in Vietnamese, cut short. Then nothing but echo. Loops "
        "seamlessly over ten seconds."
    ),

    "tu_khiem": (
        "Ambience, no music, no human voices. The player practises sword in a "
        "shrine at night. Close: a blade cutting air in a long clean arc, "
        "steel ringing faintly as it turns, the guard and pommel shifting in "
        "the hand, bare feet pivoting on stone, even breathing. Each swing "
        "ends in near-silence before the next. Cold, sharp, precise. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_dem": (
        "Ambience, no music, no human voices. The player sits awake in a "
        "cramped wooden dormitory at night. Close: a wooden bed frame "
        "creaking under small movement, cloth shifting, slow even breathing. "
        "Outside the paper window: crickets, a frog, a dog far away, a light "
        "wind. The room is small, so everything is close and dry. Loops "
        "seamlessly over ten seconds."
    ),

    "dem_tap_kich": (
        "Vietnamese-language ambience, no music. It begins as a quiet night "
        "inside a wooden dormitory - insects, wind, timber settling - then a "
        "horn cuts in from the forest and everything breaks at once: shouting "
        "in Vietnamese, fire catching, running feet, a gate slamming. Quiet "
        "first, then chaos. If the tool cannot produce a transition, generate "
        "only the chaos half. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TĨNH / SAU TRẬN ------------------------------

    "tan_hoang": (
        "Vietnamese-language ambience, no music. The player sits among ruins "
        "just before dawn after a battle. Fire is still smouldering: low "
        "crackling, a beam settling, ash shifting. Wind crosses collapsed "
        "walls. Close and quiet: slow footsteps of men carrying something "
        "heavy, setting it down, one or two Vietnamese words exchanged, a "
        "voice breaking far off and then stopping. No fighting anywhere. "
        "Heavy and empty. Loops seamlessly over ten seconds."
    ),

    "binh_minh": (
        "Ambience, no music. Dawn over a small town the morning after a night "
        "of trouble. Close: birds starting up one at a time, a rooster far "
        "off, a light wind moving dust and loose paper. Somewhere a shutter "
        "opens, a bucket of water is poured, a broom works. Almost nobody is "
        "awake, and there is no talking near the player. Clean and quiet, but "
        "not joyful. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_sang": (
        "Vietnamese-language ambience, no music. Morning in a martial sect "
        "dormitory. Close: a wooden door sliding open, sandals on stone, "
        "water poured from a bucket, a bed frame creaking, someone coughing, "
        "cloth pulled on. Outside: Vietnamese voices saying ordinary morning "
        "things, a staff tapped on the ground, a training yard counting "
        "cadence in the distance. Ordinary, unremarkable life. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ QUÁN NƯỚC ------------------------------

    "quan_nuoc": (
        "Vietnamese-language ambience, no music. The player sits in a dark "
        "corner of a roadside tea house. Close: a clay cup set on wood, tea "
        "poured, a kettle, coins counted, a stool scraping. Around him: many "
        "Vietnamese voices overlapping at different tables, laughter once, "
        "two men arguing over a price. Near the player, two men drop their "
        "voices and talk fast - still Vietnamese, still unclear. Warm and "
        "crowded. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_song_tu": (
        "Ambience, no music, no clear voices. The player lies still in a dark "
        "room at night. Extremely quiet and very close: slow breathing, a "
        "pulse, cloth shifting, a wooden bed taking weight, and a faint hum "
        "that seems to come from inside the room rather than outside it. Far "
        "off, crickets. Intimate and private, nothing loud. Loops seamlessly "
        "over ten seconds."
    ),

    "tan_xa_kho_tu": (
        "Ambience, no music, no voices. The player has just failed at "
        "cultivation and sits in the dark. Close: breathing that is too fast "
        "and too heavy, then a long shaky exhale, then nothing. A hand "
        "pressed against a chest, cloth twisted, a wooden floor creaking as "
        "weight shifts. Then silence, held. The weight is in the breathing, "
        "not in any loud event. Loops seamlessly over ten seconds."
    ),

    "tan_xa_suyt_lo": (
        "Ambience, no music, no voices. The player holds his breath in a dark "
        "dormitory. Close: breath held, then released very carefully, cloth "
        "pulled tight. Outside the door: footsteps on a wooden walkway, slow "
        "and deliberate, coming closer, pausing right outside, then moving "
        "away and fading. Then nothing but insects. Tight, tense, quiet. "
        "Loops seamlessly over ten seconds."
    ),

    "tan_xa_dot_pha": (
        "Ambience, no music, no voices. A deep low rumble rises out of "
        "silence, as if the air itself is under pressure, holds at its peak "
        "with a faint shimmer, then settles back into stillness. Nothing is "
        "struck or played - it is the room and the air vibrating. No melody, "
        "no rhythm, no beat. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TĨNH / SAU TRẬN ------------------------------

    "mon_phai_tan_hoang": (
        "Vietnamese-language ambience, no music. The player sits in the ruins "
        "of a martial sect just before dawn. Wider and emptier than a back "
        "yard: wind crossing open ground through broken walls, a wall section "
        "coming down somewhere, loose roof tiles sliding, timber still "
        "settling. Far off, men carrying something heavy - slow footsteps, "
        "one or two Vietnamese words, no talking. No fighting. Loops "
        "seamlessly over ten seconds."
    ),

    "binh_minh_ngoc_cot": (
        "Ambience, no music. Dawn at the mountain gate of a martial sect. "
        "High and open: mountain wind moving steadily, birds waking, a "
        "distant temple bell struck once and ringing away, cloth flapping on "
        "a pole. The courtyard is empty - no footsteps, no voices. Clean, "
        "cold, elevated. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "dot_pha": (
        "Ambience, no music, no voices. A closed room at night, intentionally "
        "silent. Close and small: wood creaking as it cools, a window shutter "
        "moving a fraction, the player's own breathing, and a faint low "
        "presence in the air like pressure. Nothing happens for long "
        "stretches. This silence is deliberate, not a broken file. Loops "
        "seamlessly over ten seconds."
    ),

}
