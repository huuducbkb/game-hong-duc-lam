"""Dữ liệu 9 nhóm tiếng cảnh — ÂM THANH MÔI TRƯỜNG, không phải nhạc.

Quyết định thể loại: đây là ambience / soundscape, KHÔNG phải nhạc. Không giai
điệu, không nhạc cụ, không nhịp trống, không hòa âm. Chỉ có tiếng của nơi chốn:
gió, nước, vật liệu, sinh hoạt, côn trùng, chim, người nói mờ.

Lý do: người chơi nghe nhạc nền giai điệu lặp 10 giây sẽ chán ngay và nhận ra
máy đang lặp. Tiếng môi trường thì lặp mà không lộ, vì tai người không bám vào
nhịp. Đây cũng đúng thể loại các thư viện âm thanh gọi là "ambience".

Mỗi cảnh có `tu_khoa`: cụm tiếng Anh để tìm nguồn trên thư viện âm thanh.
Cảnh chợ sớm ở Thất Huyền trấn -> "morning market ambience".
"""

# Một vòng 10 giây, nối khít, không mở đầu không kết thúc.
DUOI = (
    "Seamless ten-second loop that repeats without a seam: no fade in, no fade "
    "out, no intro, no ending, no build-up, no resolution. The texture must sit "
    "at a steady level for the whole ten seconds - it is a bed that keeps going, "
    "not a clip that starts and stops. Stereo. Duration exactly 10 seconds."
)

# Quy ước chung: khẳng định đây là âm thanh môi trường, cấm mọi thứ thuộc về nhạc.
CHUNG = (
    "This is an ambience soundscape, NOT music. No melody, no musical "
    "instruments, no chords, no harmony, no drum beat, no rhythmic pulse, no "
    "bassline, no singing, no humming, no soundtrack. Nothing in this file should "
    "have a tune. What fills the ten seconds is the sound of the place itself: "
    "air, materials, water, weather, small living things, distant indistinct "
    "activity. Naturalistic, believable, unremarkable - the sound of somewhere "
    "rather than the sound of a song. Recorded close and clean with real depth: "
    "full low end below 120 Hz where the scene has weight (wind, room, crowd), "
    "and air above 5 kHz so it does not sound band-limited or like a telephone "
    "or a radio. No intelligible speech, no narration, no voice-over, no radio "
    "host, no DJ. No lo-fi texture, no tape hiss, no vinyl crackle, no static, "
    "no radio tuning noise. No clipping, no distortion, no sudden loud peaks. "
    "Peak level below -3 dBFS."
)


NHOM = [
    {
        "ma": "cho",
        "ten": "Chợ sớm",
        "dung": "Chợ sớm Thất Huyền trấn (c1_y03, bc_cho_01…03)",
        "file": "cho.mp3",
        "tu_khoa": [
            "morning market ambience",
            "vietnamese market crowd",
            "small town market early morning",
            "market stall chatter",
        ],
        "mota": "Chợ sớm: người dựng sạp, hàng hóa đặt xuống, bàn tán xa, "
                "tiếng bước chân trên đất. Không nhạc.",
        "prompt": (
            "Ambience of a small market square in a Vietnamese town at first "
            "light, when the stalls are only just opening. The square is not full "
            "yet: a few vendors are setting up, so the sound is sparse and cool. "
            "Close and clear: wooden trestles being dragged and set down, baskets "
            "and clay jars knocking together, crates of produce thumping onto "
            "boards, footsteps on packed earth, cloth awnings being shaken out, "
            "and a soft morning breeze moving through the square. Somewhere "
            "further back, a low murmur of voices - no words you can make out, "
            "just the texture of people talking quietly while they work. A "
            "rooster far away. Everything is small, ordinary, unhurried."
        ),
    },
    {
        "ma": "tran",
        "ten": "Trận chiến",
        "dung": "Giao chiến, tập kích (bc_tran_lua, bc_dot_pha…)",
        "file": "tran.mp3",
        "tu_khoa": [
            "battlefield ambience",
            "medieval battle crowd distant",
            "sword clash ambience",
            "war chaos ambience",
        ],
        "mota": "Trận đánh: thép chạm thép, đất đá, gỗ vỡ, hơi thở nặng, tiếng "
                "hét xa không rõ chữ. Không nhạc.",
        "prompt": (
            "Ambience of a cold-weapon battle, heard from just behind the front "
            "line. No music and no rhythm - the sound is chaotic and uneven, the "
            "way a real fight sounds. Close: boots slipping on mud and gravel, "
            "breath coming hard, cloth and leather moving fast, steel meeting "
            "steel in irregular clangs, wooden shafts knocking, a shield taking a "
            "hit. Around it: bodies colliding, something wooden splintering, "
            "debris falling. Further off: a shapeless roar of many voices, "
            "distant shouting that never resolves into words, and the low rumble "
            "of a large crowd in motion. No single event is louder than the rest; "
            "it is a wall of confused, physical noise."
        ),
    },
    {
        "ma": "nui",
        "ten": "Núi",
        "dung": "Sườn núi, đường mòn, khe núi (bc_duong_mon_nui, bc_khe_nui…)",
        "file": "nui.mp3",
        "tu_khoa": [
            "mountain wind ambience",
            "high altitude wind",
            "mountain pass wind",
            "cold mountain ambience",
        ],
        "mota": "Núi cao: gió qua đá và cỏ, âm vực rộng, rất ít sinh vật. "
                "Không nhạc.",
        "prompt": (
            "Ambience high on a mountain pass. The dominant sound is wind: a wide, "
            "cold wind that moves across bare rock and dry grass, sometimes "
            "whistling thin through a gap in the stone, sometimes dropping to a low "
            "steady rush with real weight in the low end. It is not a gentle "
            "breeze - it has size. Beneath it, an enormous sense of open space and "
            "height, almost no reverb because there is nothing nearby to reflect "
            "from. A single distant bird call, twice, and then nothing. Very "
            "sparse. No other living thing, no water, no people."
        ),
    },
    {
        "ma": "san",
        "ten": "Sân tập",
        "dung": "Luyện võ (bc_san_tap, bc_san_sau…)",
        "file": "san.mp3",
        "tu_khoa": [
            "martial arts training ambience",
            "courtyard footsteps ambience",
            "wooden floor movement",
            "training hall ambience",
        ],
        "mota": "Sân tập: chân trần trên nền đất nện, quần áo vải, hơi thở, "
                "một tiếng đáp tay xa. Không nhạc.",
        "prompt": (
            "Ambience of an empty martial arts training courtyard in the cool of "
            "the morning. Close: bare feet and cloth shoes moving on packed earth, "
            "the soft scuff and pivot of someone shifting weight, loose cotton "
            "trousers snapping as they move, controlled breathing, an occasional "
            "sharp exhale. The courtyard has a little natural echo off a low "
            "wall. Somewhere behind, a broom sweeping stone, and once, faintly, "
            "the flat sound of a hand striking a padded surface. No voices, no "
            "counting, no shouting, no music."
        ),
    },
    {
        "ma": "vuon",
        "ten": "Vườn thuốc",
        "dung": "Vườn thảo dược, sườn núi hái thuốc (bc_vuon_thuoc…)",
        "file": "vuon.mp3",
        "tu_khoa": [
            "herb garden ambience",
            "garden birds insects ambience",
            "leaves rustling ambience",
            "quiet garden morning",
        ],
        "mota": "Vườn thuốc: lá cọ nhau, côn trùng nhỏ, chim xa, tay hái lá. "
                "Không nhạc.",
        "prompt": (
            "Ambience of a small walled herb garden in the morning. Close: leaves "
            "and stems brushing against each other in a light breeze, a hand "
            "parting foliage and snapping a stem, the soft rustle of a bundle of "
            "cut plants being laid down. Small life everywhere but never loud: a "
            "few bees working close by, a thin thread of insects in the "
            "background, one bird calling from a wall and answering from further "
            "off. Warm, enclosed, still air. No water, no voices, no music."
        ),
    },
    {
        "ma": "mieu",
        "ten": "Miếu",
        "dung": "Miếu, từ đường, nơi thờ (bc_mieu_hoang, bc_mieu_trong…)",
        "file": "mieu.mp3",
        "tu_khoa": [
            "temple ambience",
            "empty shrine room tone",
            "stone hall reverb ambience",
            "quiet temple interior",
        ],
        "mota": "Miếu cổ: phòng đá rỗng, tiếng vọng dài, gió lùa, một tiếng "
                "chuông đồng xa. Không nhạc, không tụng kinh.",
        "prompt": (
            "Room tone of an old stone shrine, empty and cold. The space is large "
            "and hard: a long natural reverb tail on everything, so even small "
            "sounds hang in the air. Close: a faint draught moving through the "
            "doorway, dust and grit shifting, a dry wooden beam creaking once as "
            "it settles. Somewhere far outside, a single small bronze bell is "
            "struck and allowed to die away completely. Nothing else happens. It "
            "is not silent - the room itself has a low, wide presence - but there "
            "is no activity in it. No chanting, no voices, no music."
        ),
    },
    {
        "ma": "dem",
        "ten": "Đêm",
        "dung": "Ban đêm, tập kích, chữa thương trong đêm (bc_dem_tap_kich, "
                "bc_khe_nui_dem…)",
        "file": "dem.mp3",
        "tu_khoa": [
            "night countryside ambience",
            "crickets night field",
            "night insects distant dog",
            "rural night ambience",
        ],
        "mota": "Đêm đồng quê: dế và côn trùng dày, gió nhẹ, chó sủa rất xa. "
                "Không nhạc.",
        "prompt": (
            "Ambience of open countryside at night. The air is full of insects - "
            "crickets and cicadas layering over each other in slow, uneven waves, "
            "close and then further away, never in time with anything. Underneath, "
            "a very low steady night air moving across fields. Once, a dog barks "
            "far off and stops. Once, dry grass shifts as something small moves "
            "through it. Dark, wide, empty. No voices, no music, no engine."
        ),
    },
    {
        "ma": "lang",
        "ten": "Làng",
        "dung": "Làng, xóm, cổng cộng đồng, quán trà, quán rượu (bc_tan_xa, "
                "bc_cong_dong, bc_quan_nuoc…)",
        "file": "lang.mp3",
        "tu_khoa": [
            "village ambience",
            "rural village daytime",
            "small village people distant",
            "countryside village life",
        ],
        "mota": "Làng quê: sinh hoạt thường ngày, gà, chó, tiếng người xa không "
                "rõ chữ, treo gió. Không nhạc.",
        "prompt": (
            "Ambience of a small farming village in the middle of an ordinary day. "
            "Layered and unremarkable: a few chickens scratching and clucking "
            "close by, a dog barking once somewhere down the lane, bamboo and "
            "thatch moving in a light wind, a wooden door opening, water being "
            "poured into a clay pot. Further back, a loose bed of village "
            "activity - indistinct voices talking at normal volume, a child, "
            "something being carried, a cart wheel on packed earth. Nothing is "
            "foreground, nothing is a story; it is simply a place where people "
            "live. No words you can make out, no music."
        ),
    },
    {
        "ma": "tinh",
        "ten": "Tĩnh",
        "dung": "Yên ắng: trong nhà, hiệu thuốc, lúc thiền (bc_hoi_uc, cảnh còn lại)",
        "file": "tinh.mp3",
        "tu_khoa": [
            "quiet room tone",
            "interior room ambience",
            "silent room atmosphere",
            "empty house room tone",
        ],
        "mota": "Yên ắng: phòng kín, tiếng vọng nhỏ, gỗ kêu, gió ngoài cửa sổ. "
                "Không nhạc. Không phải file hỏng.",
        "prompt": (
            "Room tone of a quiet interior - a small wooden room with a shuttered "
            "window. Almost nothing happens, and that is the point: this is the "
            "sound of a room that is deliberately still, not a recording that "
            "failed. Close: the very low presence of an enclosed space, a wooden "
            "floorboard settling, a shutter moving a fraction against its frame, "
            "a faint breeze passing outside the wall. One small object is set "
            "down on wood and the sound dies. No voices, no music, no electrical "
            "hum, no air conditioning, no clock."
        ),
    },
]


def prompt_day_du(n):
    """Prompt hoàn chỉnh: thân + đuôi loop 10 giây + quy ước chung."""
    return n["prompt"].strip() + " " + DUOI + "\n\n" + CHUNG
