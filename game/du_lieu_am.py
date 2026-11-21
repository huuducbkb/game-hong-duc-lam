"""Dữ liệu 9 nhóm tiếng cảnh: mã, tên, prompt tạo, và bối cảnh dùng.

Một nguồn duy nhất: xưởng HTML sinh từ đây, workflow cũng đọc từ đây.
Sửa prompt thì sửa ở đây rồi chạy `python3 game/tao_xuong_am.py`.
"""
NHOM = [
    {
        "ma": "cho",
        "ten": "Chợ",
        "dung": "Cảnh chợ trong game (bc_cho_01…03)",
        "file": "cho.mp3",
        "mota": "Chợ đông người giữa ban ngày: người bán rao hàng, người mua trả giá, "
                "bước chân qua lại, mâm nồi kim loại chạm nhau. Không có nhạc.",
        "prompt": (
            "Field recording of a busy open-air street market in a small East Asian town "
            "at midday. Continuous ambient bed of many people moving and talking at "
            "medium distance: overlapping voices in an unintelligible tonal language, "
            "never a single clear speaker close to the microphone. A vendor calls out a "
            "long rising-then-falling sales chant every few seconds. Behind it: sandals "
            "and bare feet on packed earth and stone, wooden stalls creaking, metal "
            "pots and ladles knocking together, a knife on a cutting board, coins "
            "dropping, cloth bags rustling, occasional distant laughter and a child. "
            "Dense, lively, warm, human. Stereo, natural perspective, mid-side detail. "
            "No music, no instruments, no singing, no radio, no crowd cheering, no "
            "traffic, no engine, no birds dominating, no rain. Loopable: the level and "
            "character at the very start must match the very end so it can repeat "
            "seamlessly. Duration 30 seconds."
        ),
    },
    {
        "ma": "tran",
        "ten": "Trận chiến",
        "dung": "Cảnh giao chiến (bc_tran_lua…)",
        "file": "tran.mp3",
        "mota": "Trận đánh bằng vũ khí lạnh: thép chạm thép, tiếng hô, đấm, thở dốc. "
                "Không có nhạc.",
        "prompt": (
            "Close combat with cold weapons in an open courtyard: steel blade striking "
            "steel blade, dull wooden impacts of a body hitting the ground, leather and "
            "cloth shifting with fast movement, boots scuffing on stone, short sharp "
            "shouts and battle cries from men, heavy breathing and grunts of effort. "
            "Impacts are irregular and unpredictable, with short silences between them. "
            "Distant sounds of a larger skirmish in the background. No music, no "
            "orchestra, no drums, no gunshots, no explosions, no fire, no screaming in "
            "pain, no gore. Stereo, natural perspective, dry with a little stone "
            "courtyard reverb. Loopable: start and end level must match. Duration 30 "
            "seconds."
        ),
    },
    {
        "ma": "nui",
        "ten": "Núi",
        "dung": "Cảnh đường mòn, khe núi (bc_duong_mon_nui, bc_khe_nui…)",
        "file": "nui.mp3",
        "mota": "Gió núi cao thổi qua khe đá, chim rừng xa, thỉnh thoảng đá nhỏ lăn. "
                "Rộng và trống trải.",
        "prompt": (
            "High mountain pass at dawn, recorded from a narrow rocky trail. Wind moves "
            "through a stone gap with a low hollow whistle that swells and fades slowly "
            "in long irregular gusts. A few small forest birds call far away with long "
            "silences between calls. Very faint distant water in a ravine below. "
            "Occasional tiny pebbles shifting and rolling on rock. Vast, empty, cold, "
            "quiet. No music, no voices, no human activity, no traffic, no aircraft, no "
            "thunder, no rain. Stereo, wide natural perspective with long reverb tails. "
            "Loopable: start and end level must match. Duration 30 seconds."
        ),
    },
    {
        "ma": "san",
        "ten": "Sân tập",
        "dung": "Cảnh luyện võ (bc_san_tap, bc_san_sau…)",
        "file": "san.mp3",
        "mota": "Sân luyện võ: đấm vào bao cát theo nhịp, chân đạp đất, thở dốc, "
                "thầy đếm nhịp. Không có nhạc.",
        "prompt": (
            "A martial arts training yard in the early morning. Rhythmic heavy impacts of "
            "fists and shins striking a hanging sandbag, roughly one every one to two "
            "seconds, with the bag's rope creaking after each hit. Bare feet and cloth "
            "shoes pivoting and stamping on packed earth. A man breathing hard with each "
            "strike. Occasionally a teacher's voice counting cadence in a calm, "
            "unintelligible tonal language, at medium distance. A wooden dummy rattling. "
            "Disciplined, physical, repetitive but never mechanical. No music, no drums, "
            "no crowd, no cheering, no shouting in pain. Stereo, natural outdoor "
            "perspective. Loopable: start and end level must match. Duration 30 seconds."
        ),
    },
    {
        "ma": "vuon",
        "ten": "Vườn thuốc",
        "dung": "Cảnh vườn thảo dược (bc_vuon_thuoc…)",
        "file": "vuon.mp3",
        "mota": "Vườn cây thuốc buổi sáng: chim hót gần, lá xào xạc, ong bay, "
                "nước nhỏ giọt. Dịu và thưa.",
        "prompt": (
            "A herb garden in the early morning, recorded close to the plants. Several "
            "small birds singing nearby at different distances, with clear individual "
            "calls and long pauses between them. A light breeze moving through dense "
            "leaves with a soft dry rustle that rises and falls. A few bees passing close "
            "to the microphone with a brief doppler buzz. Water dripping slowly from a "
            "bamboo pipe into a clay jar. Calm, green, alive but sparse. No music, no "
            "voices, no traffic, no dogs, no insects swarming loudly, no rain. Stereo, "
            "intimate natural perspective. Loopable: start and end level must match. "
            "Duration 30 seconds."
        ),
    },
    {
        "ma": "mieu",
        "ten": "Miếu",
        "dung": "Cảnh miếu, chùa (bc_mieu…)",
        "file": "mieu.mp3",
        "mota": "Miếu cổ vắng: chuông chùa xa ngân dài, gió nhẹ, chim thưa, "
                "không gian rộng. Rất tĩnh.",
        "prompt": (
            "An old empty shrine in a mountain valley, recorded in the courtyard. A "
            "distant temple bronze bell is struck once every twenty to thirty seconds, "
            "its long inharmonic partials decaying for many seconds and beating slowly "
            "against each other. Very soft wind moving through old wooden eaves and "
            "stone. A few birds far away with long silences. Occasional creak of dry "
            "timber. Enormous quiet, wide reverberant space, deeply still and slightly "
            "sacred. No music, no chanting, no voices, no gongs in rhythm, no drums, no "
            "crowd, no traffic. Stereo, long natural reverb tail. Loopable: start and "
            "end level must match. Duration 30 seconds."
        ),
    },
    {
        "ma": "dem",
        "ten": "Đêm",
        "dung": "Cảnh ban đêm, tập kích (bc_dem_tap_kich, bc_khe_nui_dem…)",
        "file": "dem.mp3",
        "mota": "Đêm ngoài trời: dế kêu dày, thỉnh thoảng chó sủa xa, gió nhẹ. "
                "Tối và tĩnh.",
        "prompt": (
            "Night in open countryside, recorded from a quiet spot. A dense field of "
            "crickets and cicadas pulsing in slow overlapping rhythms, with individual "
            "insects distinguishable against the mass. A dog barks far away, once, then "
            "again after a long pause. Very light wind in dry grass. Now and then a "
            "single frog. No music, no voices, no owls screaming, no traffic, no "
            "aircraft, no rain, no thunder. Dark, wide, slightly lonely. Stereo, natural "
            "perspective. Loopable: start and end level must match. Duration 30 seconds."
        ),
    },
    {
        "ma": "lang",
        "ten": "Làng",
        "dung": "Cảnh làng, xóm, cổng cộng đồng (bc_tan_xa, bc_cong_dong…)",
        "file": "lang.mp3",
        "mota": "Làng quê ban ngày: gà, chó sủa xa, người nói chuyện trong nhà, "
                "chim, gió. Ấm và thưa.",
        "prompt": (
            "A small farming village in daytime, recorded from a lane between houses. "
            "Chickens scratching and clucking nearby. A dog barking in the middle "
            "distance, answered by another much further away. Two or three people "
            "talking unhurriedly inside a house, muffled and unintelligible, with long "
            "pauses. A few birds. Light wind in bamboo and thatch. Somewhere a wooden "
            "door and a bucket. Warm, ordinary, unhurried, sparse. No music, no radio, "
            "no television, no traffic, no engines, no crowd, no market bustle. Stereo, "
            "natural perspective. Loopable: start and end level must match. Duration 30 "
            "seconds."
        ),
    },
    {
        "ma": "tinh",
        "ten": "Tĩnh",
        "dung": "Cảnh yên ắng, trong nhà, lúc thiền (các cảnh còn lại)",
        "file": "tinh.mp3",
        "mota": "Yên tĩnh gần như tuyệt đối: phòng trống, hơi thở của không gian, "
                "thỉnh thoảng một tiếng rất xa.",
        "prompt": (
            "Almost silence inside an old empty room with stone walls and a wooden floor. "
            "A very faint low room tone, barely audible. Once or twice, the muffled sound "
            "of something happening far outside: a distant door, a single footstep, a "
            "bird. Nothing else. The impression of a large still space, not of a "
            "recording that failed. No music, no voices, no hum of electricity, no "
            "air-conditioning, no wind, no hiss, no tape noise. Stereo, natural "
            "perspective. Loopable: start and end level must match. Duration 30 seconds."
        ),
    },
]

# Quy ước chung dán vào cuối mọi prompt
CHUNG = (
    "Do not add any music, melody, chord, drum, singing or instrumental sound of any "
    "kind. Do not add narration or intelligible speech. Do not add sound effects that "
    "are not listed. Keep it a natural field recording, not a sound-design montage. "
    "No clipping, no distortion, no sudden loud peaks. Peak level below -3 dBFS."
)
