"""Dữ liệu 9 nhóm tiếng cảnh: mã, tên, prompt tạo, và bối cảnh dùng.

Một nguồn duy nhất: xưởng HTML sinh từ đây, workflow cũng đọc từ đây.
Sửa prompt thì sửa ở đây rồi chạy `python3 game/tao_xuong_am.py`.

Prompt viết cho âm thanh game: 10 giây, có nhạc và nhạc cụ, KHÔNG phải bản ghi
thực địa. Bản ghi thực địa nghe như radio hoặc như micro đặt giữa chợ thật —
người chơi đã chê đúng như vậy.
"""

# Đuôi chung cho mọi prompt: 10 giây, loop khít, không fade.
DUOI = ("Seamless 10-second loop, no fade in and no fade out. Stereo. "
        "Duration exactly 10 seconds.")

NHOM = [
    {
        "ma": "cho",
        "ten": "Chợ",
        "dung": "Cảnh chợ trong game (bc_cho_01…03)",
        "file": "cho.mp3",
        "mota": "Chợ đông: nền đàn tranh ngũ cung, nhịp gỗ nhẹ, tiếng đám đông mờ. "
                "Dạng nhạc nền game, không phải bản ghi thực địa.",
        "prompt": (
            "Game ambience loop for a busy market scene in a Vietnamese historical "
            "RPG. This is designed game audio, layered and stylized — NOT a field "
            "recording and NOT a radio broadcast. Layers: a soft bed of indistinct "
            "crowd murmur with no clear words, a light wooden percussion pulse at a "
            "walking tempo, a repeating plucked dan tranh figure in a Vietnamese "
            "pentatonic mode, and a small metal bowl accent every few beats. Warm, "
            "lively, mid-forward, slightly stylized. Clean and close, no room "
            "recording feel. No intelligible speech, no narration, no radio voice, no "
            "lo-fi texture, no tape hiss, no vinyl crackle, no static."
        ),
    },
    {
        "ma": "tran",
        "ten": "Trận chiến",
        "dung": "Cảnh giao chiến (bc_tran_lua…)",
        "file": "tran.mp3",
        "mota": "Trận đánh: trống trận dồn, chiêng trầm, đàn tranh dứt khoát, tiếng "
                "thép chạm thép làm nhịp. Dạng nhạc nền game.",
        "prompt": (
            "Game combat ambience loop for a cold-weapon battle in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — NOT a "
            "field recording. Layers: war drums (trong tran) in a driving repeating "
            "pattern, a low chieng gong swell that rises and falls, short staccato dan "
            "tranh plucks on the off-beats, and steel-on-steel hits used as rhythmic "
            "accents rather than realistic events. Tense, martial, driving, cinematic "
            "but restrained. Clean studio sound, not a live recording. No gunshots, no "
            "explosions, no screaming in pain, no gore, no intelligible speech, no "
            "narration, no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "nui",
        "ten": "Núi",
        "dung": "Cảnh đường mòn, khe núi (bc_duong_mon_nui, bc_khe_nui…)",
        "file": "nui.mp3",
        "mota": "Núi cao: sáo trúc lơ lửng trên nền trầm giữ, gió làm lớp đệm. "
                "Rộng và trống trải.",
        "prompt": (
            "Game ambience loop for a high mountain pass in a Vietnamese historical "
            "RPG. This is designed game audio, layered and stylized — NOT a field "
            "recording. Layers: a sustained low drone pad as the floor of the mix, a "
            "sparse bamboo flute (sao) melody in a Vietnamese pentatonic mode floating "
            "above it with long rests, and a filtered wind layer used as a soft pad "
            "rather than a realistic gust. Vast, cold, open, contemplative. Clean and "
            "wide, with a long synthetic reverb tail. No voices, no narration, no "
            "birdsong detail, no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "san",
        "ten": "Sân tập",
        "dung": "Cảnh luyện võ (bc_san_tap, bc_san_sau…)",
        "file": "san.mp3",
        "mota": "Sân luyện võ: trống giữ nhịp đều, đàn tranh gọn, hơi thở làm lớp nền. "
                "Dạng nhạc nền game.",
        "prompt": (
            "Game ambience loop for a martial arts training yard in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — NOT a "
            "field recording. Layers: a steady drum (trong) keeping tempo like a "
            "metronome for practice, tight dan tranh plucks landing on the beat, a "
            "soft breath-like noise layer used as texture, and a wooden clapper "
            "accent. Disciplined, physical, repetitive, hypnotic. Clean studio sound, "
            "not a live recording. No crowd, no cheering, no shouting in pain, no "
            "intelligible speech, no narration, no lo-fi texture, no tape hiss, no "
            "static."
        ),
    },
    {
        "ma": "vuon",
        "ten": "Vườn thuốc",
        "dung": "Cảnh vườn thảo dược (bc_vuon_thuoc…)",
        "file": "vuon.mp3",
        "mota": "Vườn thuốc: sáo cao, đàn tranh thưa, lớp đệm lá nhẹ. Dịu và thưa.",
        "prompt": (
            "Game ambience loop for a herb garden in a Vietnamese historical RPG. "
            "This is designed game audio, layered and stylized — NOT a field recording. "
            "Layers: a high bamboo flute (sao) playing a short gentle pentatonic "
            "phrase, sparse plucked dan tranh notes with long gaps, and a soft "
            "filtered leaf-rustle pad underneath. A single water-drop accent as a "
            "texture. Calm, green, airy, unhurried. Clean and intimate, with a light "
            "synthetic reverb. No voices, no narration, no bees or insects detail, no "
            "lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "mieu",
        "ten": "Miếu",
        "dung": "Cảnh miếu, chùa (bc_mieu…)",
        "file": "mieu.mp3",
        "mota": "Miếu cổ: chiêng ngân dài, nền trầm giữ, đàn bầu thỉnh thoảng. "
                "Rất tĩnh và thiêng.",
        "prompt": (
            "Game ambience loop for an old mountain shrine in a Vietnamese historical "
            "RPG. This is designed game audio, layered and stylized — NOT a field "
            "recording. Layers: a bronze chieng gong struck once, its long inharmonic "
            "partials decaying and beating slowly, a sustained low drone underneath, "
            "and a single dan bau note bending gently. Enormous quiet, wide "
            "reverberant space, sacred and still. Clean and deep, with a long "
            "synthetic reverb tail. No chanting, no voices, no narration, no lo-fi "
            "texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "dem",
        "ten": "Đêm",
        "dung": "Cảnh ban đêm, tập kích (bc_dem_tap_kich, bc_khe_nui_dem…)",
        "file": "dem.mp3",
        "mota": "Đêm: đàn bầu ngân là chính, nền trầm, tiếng côn trùng cách điệu. "
                "Tối và tĩnh.",
        "prompt": (
            "Game ambience loop for a night scene in open countryside in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — NOT a "
            "field recording. Layers: a slow dan bau melody with its characteristic "
            "pitch bend as the leading voice, a deep sustained drone beneath it, and a "
            "stylized high shimmer suggesting distant insects — synthesized, not "
            "sampled. Dark, wide, lonely, suspended. Clean and spacious, with a long "
            "synthetic reverb. No dogs, no voices, no narration, no lo-fi texture, no "
            "tape hiss, no static."
        ),
    },
    {
        "ma": "lang",
        "ten": "Làng",
        "dung": "Cảnh làng, xóm, cổng cộng đồng (bc_tan_xa, bc_cong_dong…)",
        "file": "lang.mp3",
        "mota": "Làng quê: đàn tranh ấm, sáo nhẹ, trống thưa, tiếng người mờ. "
                "Ấm và thưa.",
        "prompt": (
            "Game ambience loop for a small farming village in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — NOT a "
            "field recording. Layers: a warm dan tranh figure in a pentatonic mode as "
            "the main voice, a soft bamboo flute answering it, a sparse drum (trong) "
            "marking the phrase, and a very low bed of indistinct murmuring voices "
            "with no clear words. Warm, ordinary, unhurried, homely. Clean and close, "
            "with a light synthetic reverb. No intelligible speech, no narration, no "
            "radio voice, no television, no traffic, no lo-fi texture, no tape hiss, "
            "no static."
        ),
    },
    {
        "ma": "tinh",
        "ten": "Tĩnh",
        "dung": "Cảnh yên ắng, trong nhà, lúc thiền (các cảnh còn lại)",
        "file": "tinh.mp3",
        "mota": "Yên ắng: nền trầm rất nhẹ, thỉnh thoảng một tiếng chuông xa. "
                "Không phải im lặng hỏng file.",
        "prompt": (
            "Game ambience loop for a quiet interior in a Vietnamese historical RPG. "
            "This is designed game audio, layered and stylized — NOT a field recording. "
            "Layers: a very soft low drone as a bed, barely audible, and one distant "
            "bell tone decaying across the loop. The impression of a large still space "
            "that is deliberately quiet — not a recording that failed. Clean, "
            "intentional, minimal. No voices, no narration, no electrical hum, no "
            "air-conditioning, no wind, no lo-fi texture, no tape hiss, no static."
        ),
    },
]

# Quy ước chung dán vào cuối mọi prompt
CHUNG = (
    "Style: this is game audio, not a field recording and not a radio broadcast. "
    "Designed, layered, clean and stylized, the way a game soundtrack or ambience "
    "bed sounds — not a microphone in a real place. Use Vietnamese instruments "
    "(dan tranh, sao, trong, chieng, dan bau) and a pentatonic mode where the prompt "
    "asks for them. No intelligible speech, no narration, no radio voice, no DJ. "
    "No lo-fi texture, no tape hiss, no vinyl crackle, no static, no radio tuning "
    "noise. No clipping, no distortion, no sudden loud peaks. Peak level below "
    "-3 dBFS."
)


def prompt_day_du(n):
    """Prompt hoàn chỉnh: thân + đuôi 10 giây + quy ước chung."""
    return n["prompt"].strip() + " " + DUOI + "\n\n" + CHUNG
