"""Prompt tạo tiếng cho từng cảnh, viết theo tai người chơi.

Người chơi phải nghe như đang ĐỨNG Ở ĐÓ, không phải nghe một bản nhạc. Nên mỗi
prompt mở đầu bằng chỗ người chơi đứng, rồi tả tiếng theo lớp: sát tai, vài mét,
xa. Có lớp gần có lớp xa thì tai mới nghe ra chiều sâu của không gian — đó là
thứ khiến tiếng thành "trong game" chứ không phải một file phát đều.

Năm quy tắc lặp lại trong mọi prompt:

1. `no music` — không nhạc, không giai điệu. Đây là tiếng của không gian, không
   phải nhạc nền game.
2. `no speech` — KHÔNG có lời nói, không tiếng đọc, không ai nói câu nào. Tiếng
   người chỉ được là âm không lời: thở, thở dốc, hừ, rên, huýt gió, la, khóc.
   Lời nói biến cảnh thành phim truyền thanh và kéo theo chuyện phải chọn đúng
   tiếng Việt cho từng câu.
3. Chiều sâu: mỗi prompt phải có ít nhất hai lớp khoảng cách và nói rõ hướng
   (trước mặt, bên trái, sau lưng, trên đầu). Ghi cả thứ làm tiếng đổi chất:
   tường dội lại, cửa che bớt, không gian hẹp hay trống.
4. Mười giây, lặp được. Cảnh trong game chỉ 10 giây nên file phải quay vòng
   không nghe mối nối.
5. Dưới 450 ký tự. Đây là trần cứng của ô prompt trên ElevenLabs Sound
   Effects — dài hơn thì trang báo lỗi và không cho tạo. Trần này áp cho cả
   trang lẫn API.

Tránh chữ dễ bị bộ lọc chặn: không tả thương tích, không tả xác, không dùng
chữ "violent". Tả ĐỘNG TÁC cụ thể (a blade turning another aside, boots on
stone) thay vì tả mức độ dữ dội — vừa dễ qua bộ lọc, vừa ra tiếng đúng hơn.
"""

PROMPT = {

    # ------------------------------ CHỢ ------------------------------

    "cho_01": (
        "Ambience, no music, no speech. The player lies on the ground in a "
        "corner of a crowded morning market, so every sound arrives at ear "
        "level. Close: cart wheels creaking on packed earth, clay jars "
        "knocking, coins dropped into a palm, cloth brushing past the ear. A "
        "few metres off: footsteps crossing, a stool dragged, one short "
        "shout, laughter once. Far behind: a dog. The crowd swallows its own "
        "echoes. Loops seamlessly over ten seconds."
    ),

    "cho_02": (
        "Ambience, no music, no speech. The player stands at the mouth of a "
        "narrow alley behind the market, ten metres from three men sitting "
        "around a small fire. Their sounds reach him softened and thrown back "
        "by the close walls: fire crackling, a stick poking embers, spit "
        "hissing, a cough, a low sigh, a hand slapped on a knee. At his own "
        "ear: his breathing, a boot scuffing grit. Loops seamlessly over ten "
        "seconds."
    ),

    "cho_03": (
        "Ambience, no music, no speech. The player sits at the edge of a "
        "market emptying at dusk, in open space. Close: a wooden stall folded "
        "and stacked, crates dragged, a broom sweeping packed earth. Further "
        "off, behind and right: slow footsteps walking away, a cough, a long "
        "tired sigh. Far: dry wind moving loose paper. Open ground, so the "
        "far sounds thin out instead of bouncing back. Loops seamlessly over "
        "ten seconds."
    ),

    # ------------------------------ TRẬN LỬA ------------------------------

    "tran_lua": (
        "Ambience, no music, no speech. The player stands high on a mountain "
        "path at night, looking down at a town below. Everything from the "
        "valley is thin and far, spread wide and low: fire roaring, timber "
        "cracking, structures falling, one distant shout, a horn. Close, at "
        "the ear: wind on the ridge, grass moving, his own clothing. Nothing "
        "is near him. The valley is too wide to answer, so each sound lands "
        "and stops. Loops seamlessly over ten seconds."
    ),

    "tran_lua_2": (
        "Ambience, no music, no speech. The player runs through a burning "
        "town street at night, inside it. Close, all around the head: fire "
        "roaring through a wooden house, roof beams cracking, a blade "
        "sweeping through air, steel ringing on steel, boots hammering stone, "
        "hard breathing. Mid-distance ahead: a wall coming down, horses. Far "
        "behind: a shout. House fronts throw every sound back fast. Loops "
        "seamlessly over ten seconds."
    ),

    "tran_lua_3": (
        "Ambience, no music, no speech. The player is at the shattered gate "
        "of a martial sect during a night assault. Close: a heavy gate "
        "splintering, hinges tearing, boots stamping broken planks, hard "
        "breathing, one blade turning another aside. Further back, bouncing "
        "off stone: many men moving at once, grunts, one hoarse shout. Far "
        "beyond the gate: fire. Walled in. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ CỔNG ĐÔNG ------------------------------

    "cong_dong_doi_mat": (
        "Ambience, no music, no speech. The player stands at a broken gate "
        "facing several men a few metres off, in the instant before blades "
        "meet. Almost silent, and the silence is the depth. Close at the ear: "
        "his own slow breath, cloth shifting as he sets his stance. Ahead of "
        "him: their breathing, a boot scuffing stone, a blade drawn an inch. "
        "Behind: wind through the gate. Loops seamlessly over ten seconds."
    ),

    "cong_dong_giau": (
        "Ambience, no music, no speech. The player holds his strength back at "
        "a gate. Close: fast shallow breathing, a blade turned aside, boots "
        "sliding backwards on stone, cloth snapping, a short grunt. "
        "Mid-distance, off to the side: other men moving, breath, a wordless "
        "shout. Everything controlled and deliberately small. Stone walls "
        "close on both sides, so the small sounds come back doubled. Loops "
        "seamlessly over ten seconds."
    ),

    "cong_dong_toan_luc": (
        "Ambience, no music, no speech. The player stops holding back at a "
        "gate. Close and sudden: one heavy impact, air torn, dust and gravel "
        "thrown, stone struck, breath bursting out, a loud grunt. Around him, "
        "further off: the exchange carries on, then a brief stunned quiet, "
        "one shout from the onlookers. The gate walls catch it and send it "
        "back a beat later. Loops seamlessly over ten seconds."
    ),

    "cong_dong_quyen": (
        "Ambience, no music, no speech. The player fights bare-handed at "
        "close range at a gate. Close and dry, right at the ear: a fist "
        "striking a chest, a forearm blocking, sleeves snapping, feet "
        "pivoting and stamping stone, steady breathing through the nose, a "
        "short exhale on each strike. Further off: boots on stone, blades, a "
        "grunt. Stone under and stone behind, so every hit returns a little "
        "late. Loops seamlessly over ten seconds."
    ),

    "cong_dong_hung_ba": (
        "Ambience, no music, no speech. The player shouts a challenge across "
        "a courtyard in the middle of a fight. One raw wordless shout goes "
        "out, and comes back off the far wall as echo - the wall is the "
        "depth. Close at the ear: his own breath. Further off: blades going "
        "quiet, footsteps halting, many men holding still. Loops seamlessly "
        "over ten seconds."
    ),

    # ------------------------------ HỎA TRƯỜNG CỨU NGƯỜI ------------------------------

    "hoa_truong_cuu": (
        "Ambience, no music, no speech. The player is inside a burning "
        "building pulling someone out. Fire is close and it fills the space: "
        "roaring, crackling, timber snapping, embers falling. At the ear: "
        "heavy effort breathing, wood levered and thrown aside, a weak hoarse "
        "moan. Outside, far through the fire: a shout, muffled. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ ĐƯỜNG MÒN NÚI ------------------------------

    "duong_mon_nui": (
        "Ambience, no music, no speech. The player walks a narrow mountain "
        "trail at dusk. Close at the ear: boots on loose gravel, dry grass "
        "brushing his legs, his own breathing. Further out, wide and open: "
        "wind through tall grass, crickets starting up. Far below: wind "
        "moving in the valley. No walls, so nothing comes back. Loops "
        "seamlessly over ten seconds."
    ),

    "khe_nui_dem": (
        "Ambience, no music, no speech. The player stands at the mouth of a "
        "narrow rock ravine at night. Close at the ear: a few drops falling "
        "into a pool, sparse insects, his own breathing. The ravine makes the "
        "wind sigh - air forced through the gap, coming back off wet stone on "
        "both sides. Far above: wind crossing the open ridge. Loops "
        "seamlessly over ten seconds."
    ),

    "khe_nui_chon": (
        "Ambience, no music, no speech. The player digs in a mountain ravine "
        "at night. Close and physical: a shovel blade cutting wet soil, "
        "gravel sliding, earth landing on a pile, heavy breathing with "
        "effort, the shovel scraping rock. Further out: wind through the "
        "ravine gap, distant insects. Quiet work done in a hurry. Rock walls "
        "close in, so the digging comes back at him off both sides. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ SÂN TẬP ------------------------------

    "san_tap_ngay": (
        "Ambience, no music, no speech. The player stands in a large training "
        "yard at midday. Close at the ear: bare feet stamping packed earth, "
        "breath forced out on each move. A few metres off, left and right: "
        "wooden staffs striking each other, staffs hitting the ground in "
        "unison, one shouted count. Further off: banners flapping overhead, "
        "the yard edge. Open yard, so the far sounds thin out instead of "
        "bouncing back. Loops seamlessly over ten seconds."
    ),

    "san_tap_chen_ep": (
        "Ambience, no music, no speech. The player stands in a training yard "
        "while a ring of students gathers around him. Nobody is loud, and "
        "that is the threat: low laughter, a mocking hum, feet shuffling as "
        "they circle, a staff tapping ground, someone spitting. Close, all "
        "around the head. The rest of the training carries on further off. "
        "The ring of bodies soaks up the sound instead of bouncing it. Loops "
        "seamlessly over ten seconds."
    ),

    "san_tap_cai_lai": (
        "Ambience, no music, no speech. The player has just answered back in "
        "a training yard. One sharp angry shout, no words, then a flat slap "
        "lands close, and the whole yard goes completely quiet. After a beat "
        "a low hum of reaction spreads through the crowd - only sound, "
        "nothing formed. Far off: the rest of the training has stopped too. "
        "Loops seamlessly over ten seconds."
    ),

    # ------------------------------ SÂN SAU ------------------------------

    "san_sau_luyen_dem": (
        "Ambience, no music, no speech. The player practises alone in a back "
        "yard late at night and has to stay silent. Everything is "
        "deliberately small and at the ear: bare feet on packed earth, cloth "
        "moving, breath held and released through the nose, a fist passing "
        "through air, a quiet landing. Far off: insects, one dog. Open night "
        "air, so nothing comes back and each sound dies where it lands. Loops "
        "seamlessly over ten seconds."
    ),

    "san_sau_anh_sang": (
        "Ambience, no music, no speech. The player stands under a huge old "
        "tree in a back yard at night. Close at the ear: his own quiet "
        "breathing, one insect very close. Overhead: leaves moving in a light "
        "wind, a thick branch creaking slowly, leaves letting go and landing. "
        "Far off: crickets, a dog. The tree takes the sound and gives nothing "
        "back. Loops seamlessly over ten seconds."
    ),

    "san_sau_chon_lai": (
        "Ambience, no music, no speech. The player digs in a back yard at "
        "night, in a hurry. Close: a small shovel biting soft earth, soil "
        "poured out, roots snapping, leaves pushed aside, fast breathing, "
        "cloth rustling. Overhead: the old tree's leaves moving. Far off: a "
        "dog. Soft earth swallows the digging; the leaves overhead catch the "
        "rest. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ VƯỜN THUỐC ------------------------------

    "vuon_thuoc_gap": (
        "Ambience, no music, no speech. The player walks into a walled herb "
        "garden in the morning. Close, at the ear: leaves brushing each other "
        "and his clothing, a bee passing, dry stems snapping underfoot, a "
        "bird landing on the wall and calling twice. Beyond the wall, "
        "softened by distance: staffs, a shouted count. Loops seamlessly over "
        "ten seconds."
    ),

    "vuon_thuoc_hoi": (
        "Ambience, no music, no speech. Two people stand in a walled herb "
        "garden: the player and an old man. Nothing is spoken. What carries "
        "is the shape of it: slow dry breathing close on the left, a younger "
        "breath held tense, a foot shifting, cloth. Behind them, further off: "
        "leaves moving, insects, a bundle of herbs being tied. The wall holds "
        "the sound in, close and low, so it never leaves the garden. Loops "
        "seamlessly over ten seconds."
    ),

    "vuon_thuoc_im": (
        "Ambience, no music, no speech at all. The player sits in a walled "
        "herb garden and stays silent. Close at the ear: a bundle of dried "
        "herbs being handled, his own breath. Further off: leaves moving in a "
        "light wind, insects, one bird far away. Long stretches where almost "
        "nothing happens. This emptiness is deliberate. The wall holds "
        "everything in, so the quiet has an edge to it. Loops seamlessly over "
        "ten seconds."
    ),

    "vuon_thuoc_ngoc": (
        "Ambience, no music, no speech. In a walled herb garden someone "
        "handles a heavy object. Close: a stone or jade object set down on "
        "wood with a solid knock, cloth unwrapped, fingers brushing stone, a "
        "bundle of herbs laid aside. Near the ear: two low unhurried breaths. "
        "Behind: leaves, insects. The wall keeps it in and small, nothing "
        "escaping. Loops seamlessly over ten seconds."
    ),

    "vuon_thuoc_dem": (
        "Ambience, no music, no speech. The player digs in a herb garden at "
        "night. Close at the ear: a small tool cutting soft soil, roots "
        "snapping, earth poured out, breath held. Further out: leaves swept "
        "aside, insects in the wet garden air. Beyond the wall: the stillness "
        "of a place where a flower has just opened. The wall keeps it close; "
        "damp air deadens whatever tries to travel. Loops seamlessly over ten "
        "seconds."
    ),

    # ------------------------------ MIẾU ------------------------------

    "mieu_hoang": (
        "Ambience, no music, no speech. The player stands outside a ruined "
        "shrine at night, watching it. Close at the ear: his own breathing, "
        "grass moving at his feet. Ahead, inside the ruin: wind pushing "
        "through broken walls and gaps, whistling low then dropping away, "
        "loose roof tiles shifting. Further off: crickets, a piece of wall "
        "crumbling. Broken walls break up the wind, so it arrives in pieces. "
        "Loops seamlessly over ten seconds."
    ),

    "mieu_trong": (
        "Ambience, no music, no speech. The player is inside a small stone "
        "shrine at night. The room is the sound, and the room is the depth: "
        "close at the ear his own breath, then a long natural reverb carrying "
        "it away. Air moving through the doorway, a draft pushing dust across "
        "stone, a loose tile ticking. One footstep echoing longer than it "
        "should. Loops seamlessly over ten seconds."
    ),

    "doat_hop": (
        "Ambience, no music, no speech. The player struggles for a box inside "
        "a stone shrine. Close: boots slipping on stone, bodies colliding, "
        "cloth tearing, a blade swung and missing, one heavy impact, then "
        "weight dropping onto the floor. One hoarse shout, cut short. Further "
        "off, outside the shrine: a door, running feet, then nothing but "
        "echo. Loops seamlessly over ten seconds."
    ),

    "tu_khiem": (
        "Ambience, no music, no speech. The player practises sword in a "
        "shrine at night. Close at the ear: a blade cutting air in a long "
        "clean arc, steel ringing faintly as it turns, the guard shifting in "
        "the hand, bare feet pivoting on stone, even breathing. Further off: "
        "the room answers each swing with its own reverb, then near-silence. "
        "Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_dem": (
        "Ambience, no music, no speech. The player sits awake in a cramped "
        "wooden dormitory at night. Close, at the ear: a bed frame creaking "
        "under small movement, cloth shifting, slow even breathing. Outside "
        "the paper window, muffled and further: crickets, a frog, a dog far "
        "away, a light wind. Loops seamlessly over ten seconds."
    ),

    "dem_tap_kich": (
        "Ambience, no music, no speech. It begins as a quiet night inside a "
        "wooden dormitory - close at the ear: insects, a bed frame, his own "
        "breath; further off: wind, timber settling. Then a horn cuts in from "
        "the forest and everything breaks at once: fire igniting, blades, "
        "running feet, a gate slamming, one shout. Quiet first, then chaos. "
        "The wooden room holds the quiet tight, then lets the chaos in all at "
        "once. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TĨNH / SAU TRẬN ------------------------------

    "tan_hoang": (
        "Ambience, no music, no speech. The player sits among ruins just "
        "before dawn after a battle. Fire is still smouldering: low "
        "crackling, a beam settling, ash shifting. Wind crosses collapsed "
        "walls. Close and quiet: slow footsteps of men carrying something "
        "heavy, setting it down, one long breath let go, a broken sob far off "
        "and then stopping. Collapsed walls give the sound nowhere to bounce, "
        "so it dies in the open. Loops seamlessly over ten seconds."
    ),

    "binh_minh": (
        "Ambience, no music, no speech. Dawn over a small town the morning "
        "after. Close: birds starting up one at a time, a rooster far off, a "
        "light wind moving dust and loose paper. Somewhere a shutter opens, a "
        "bucket of water is poured, a broom works. Almost nobody is awake, "
        "and nothing human is near the player. Open morning air, so each "
        "sound lands clean and stops. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_sang": (
        "Ambience, no music, no speech. Morning in a martial sect dormitory. "
        "Close: a wooden door sliding open, sandals on stone, water poured "
        "from a bucket, a bed frame creaking, someone coughing, cloth pulled "
        "on. Outside, further and softened: a staff tapped on the ground, a "
        "shouted count from the yard, footsteps. Loops seamlessly over ten "
        "seconds."
    ),

    # ------------------------------ QUÁN NƯỚC ------------------------------

    "quan_nuoc": (
        "Ambience, no music, no speech. The player sits in a dark corner of a "
        "roadside tea house. Close, at the ear: a clay cup set on wood, tea "
        "poured, a kettle, coins counted, a stool scraping. Around, at other "
        "tables: a low hum too far to be anything, laughter once, a hand "
        "slapped on a table. Warm and crowded. Low ceiling and close walls "
        "press the hum down around his head. Loops seamlessly over ten "
        "seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "tan_xa_song_tu": (
        "Ambience, no music, no speech. The player lies still in a dark room "
        "at night. Extremely quiet and at the ear: slow breathing, a pulse, "
        "cloth shifting, a wooden bed taking weight, and a faint hum that "
        "seems to come from inside the room rather than outside it. Far off: "
        "crickets. The small room holds his own sound against him. Loops "
        "seamlessly over ten seconds."
    ),

    "tan_xa_kho_tu": (
        "Ambience, no music, no speech. The player has just failed at "
        "cultivation and sits in the dark. Close at the ear: breathing too "
        "fast and too heavy, then a long shaky exhale, then nothing. A hand "
        "pressed against a chest, cloth twisted. Further off, outside the "
        "room: a wooden floor creaking as someone else shifts weight. The "
        "room is small enough to send his breathing back at him. Loops "
        "seamlessly over ten seconds."
    ),

    "tan_xa_suyt_lo": (
        "Ambience, no music, no speech. The player holds his breath in a dark "
        "dormitory. Close: breath held, then released very carefully, cloth "
        "pulled tight. Outside the door, on the wooden walkway, coming "
        "closer: slow deliberate footsteps, pausing right outside, then "
        "moving away and fading. Then nothing but insects. The thin wall "
        "carries the footsteps through too clearly. Loops seamlessly over ten "
        "seconds."
    ),

    "tan_xa_dot_pha": (
        "Ambience, no music, no speech. A deep low rumble rises out of "
        "silence, as if the air itself is under pressure, holds at its peak "
        "with a faint shimmer, then settles back into stillness. Close at the "
        "ear: one held breath, then a slow release. Far off, the walls of the "
        "room take the rumble and give it back. No melody, no rhythm. Loops "
        "seamlessly over ten seconds."
    ),

    # ------------------------------ TĨNH / SAU TRẬN ------------------------------

    "mon_phai_tan_hoang": (
        "Ambience, no music, no speech. The player sits in the ruins of a "
        "martial sect just before dawn. Close at the ear: his own breath, ash "
        "shifting. Further out, crossing open ground through broken walls: "
        "wind, a wall section coming down somewhere, loose roof tiles "
        "sliding. Far off: slow footsteps of men carrying something heavy, "
        "one long breath. Open ruins, so the sound spreads out and thins. "
        "Loops seamlessly over ten seconds."
    ),

    "binh_minh_ngoc_cot": (
        "Ambience, no music, no speech. Dawn at the mountain gate of a "
        "martial sect. Close at the ear: cloth flapping on a pole, his own "
        "breathing. Further out: mountain wind moving steadily, birds waking. "
        "Far down the valley: a temple bell struck once and ringing away. The "
        "courtyard is empty - no footsteps. High open air, so the bell runs "
        "away down the valley. Loops seamlessly over ten seconds."
    ),

    # ------------------------------ TÂN XÁ ------------------------------

    "dot_pha": (
        "Ambience, no music, no speech. A closed room at night, intentionally "
        "silent. Close at the ear: wood creaking as it cools, his own "
        "breathing, a window shutter moving a fraction. Further off, through "
        "the wall: a faint low presence in the air like pressure, the room "
        "itself pressing back. Nothing happens for long stretches. The closed "
        "room presses back, so the silence has weight. Loops seamlessly over "
        "ten seconds."
    ),

}
