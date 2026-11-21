"""Dữ liệu 9 nhóm tiếng cảnh, viết lại từ phân tích bản ghi chợ anh tải lên.

Bản ghi gốc (assets/am/cho.mp3, 6,06 giây) đã được đo trước khi viết prompt:
năng lượng dồn 300–2000 Hz (90%), gần như không có gì dưới 120 Hz và trên 5 kHz,
âm sắc đổi liên tục 78–501 Hz, 92% năng lượng nằm trong dải tiếng nói, có nền ồn
liên tục, và có 0,4 giây lặng câm ở đầu. Đó là dấu hiệu của bản ghi thực địa đã
bị lọc bớt hai đầu tần — nghe như radio, không như nhạc game.

Vì vậy prompt dưới đây không chép lại bản ghi đó. Chúng giữ đúng *nội dung cảnh*
(chợ sớm, đông người, bàn tán tin Dã Lang Bang) nhưng viết theo hướng âm thanh
game: có lớp, có nhạc cụ, có nhịp, không có nền ồn thực địa.

Mỗi cảnh khai báo `nhip` = (BPM, số ô 4/4). Một ô dài 4*60/BPM giây nên
số ô = BPM/24, chỉ nhịp bội của 24 mới chia chẵn 10,00 giây.
"""

# 10 giây chia chẵn, tất cả đều đúng 10,00 giây:
#   48 BPM -> 2 ô (5,00 s/ô)   cảnh thưa: núi, miếu, tĩnh
#   72 BPM -> 3 ô (3,33 s/ô)   cảnh vừa: vườn, đêm
#   96 BPM -> 4 ô (2,50 s/ô)   cảnh đông: chợ, sân, làng
#  120 BPM -> 5 ô (2,00 s/ô)   cảnh gấp: trận
NHIP_MAC_DINH = (96, 4)


def duoi(nhip=96, o_nhip=4):
    giay = o_nhip * 4 * 60 / nhip
    assert abs(giay - 10) < 0.01, f"{nhip} BPM x {o_nhip} ô = {giay:.2f}s, không phải 10s"
    return (
        f"Structure: steady {nhip} BPM in 4/4, {o_nhip} bars long, so the ten "
        "seconds land exactly on the bar line. The musical pattern must repeat at "
        "least twice inside these ten seconds - this is a bed that keeps going, not "
        "a piece that starts and ends. No intro, no outro, no build-up, no final "
        "chord, no resolution, no fade in, no fade out: the first beat and the last "
        "beat are the same point in the cycle, so the file repeats forever without "
        "a seam. If the scene has no drums, keep the same grid internally so the "
        "phrase still repeats on the bar. Stereo. Duration exactly 10 seconds."
    )


NHOM = [
    {
        "ma": "cho",
        "nhip": (96, 4),
        "ten": "Chợ sớm",
        "dung": "Chợ sớm Thất Huyền trấn (c1_y03, bc_cho_01…03)",
        "file": "cho.mp3",
        "mota": "Chợ sớm: tiếng rao thưa, nhịp gỗ đều, đàn tranh ngũ cung, "
                "tiếng bàn tán mờ. Dạng nhạc nền game.",
        "prompt": (
            "Game ambience loop for an early morning market in Thất Huyền trấn, a "
            "walled town in a Vietnamese historical RPG. This is designed game "
            "audio, layered and stylized — NOT a field recording and NOT a radio "
            "broadcast. It is dawn: the market is just opening, so the scene is "
            "sparse and cool, not crowded. Layers: a low dan tranh drone on the "
            "tonic as the floor, a steady wooden clapper (phách) marking every "
            "beat like a stallholder setting up, a repeating four-note dan tranh "
            "figure in a Vietnamese pentatonic mode, and a very quiet bed of "
            "indistinct murmuring voices far back in the mix with no clear words. "
            "One small brass bowl ring at the top of each bar, as a market bell. "
            "Cool, unhurried, slightly mysterious — there is gossip in the air. "
            "Clean and close, mid-forward, no room recording feel, no reverb "
            "wash. No intelligible speech, no narration, no radio voice, no "
            "lo-fi texture, no tape hiss, no vinyl crackle, no static."
        ),
    },
    {
        "ma": "tran",
        "nhip": (120, 5),
        "ten": "Trận chiến",
        "dung": "Giao chiến, tập kích (bc_tran_lua, bc_dot_pha…)",
        "file": "tran.mp3",
        "mota": "Trận đánh: trống trận dồn 120 nhịp, chiêng trầm, đàn tranh dứt "
                "khoát, thép chạm thép làm nhịp. Dạng nhạc nền game.",
        "prompt": (
            "Game combat ambience loop for a cold-weapon battle in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — "
            "NOT a field recording. Layers: war drums (trống trận) in a driving "
            "repeating pattern at a fast tempo, a low chiêng gong swell that rises "
            "and falls across the bar, short staccato dan tranh plucks on the "
            "off-beats, and steel-on-steel hits used as rhythmic accents rather "
            "than realistic events. Tense, martial, driving, cinematic but "
            "restrained — the energy comes from the pattern, not from volume. "
            "Clean studio sound, not a live recording. No gunshots, no explosions, "
            "no screaming in pain, no gore, no intelligible speech, no narration, "
            "no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "nui",
        "nhip": (48, 2),
        "ten": "Núi",
        "dung": "Sườn núi, đường mòn, khe núi (bc_duong_mon_nui, bc_khe_nui…)",
        "file": "nui.mp3",
        "mota": "Núi cao: sáo trúc lơ lửng trên nền trầm giữ, gió làm lớp đệm. "
                "Rộng và trống trải.",
        "prompt": (
            "Game ambience loop for a high mountain pass in a Vietnamese historical "
            "RPG. This is designed game audio, layered and stylized — NOT a field "
            "recording. Layers: a sustained low drone pad as the floor of the mix, "
            "a sparse bamboo flute (sáo) melody in a Vietnamese pentatonic mode "
            "floating above it with long rests, and a filtered wind layer used as a "
            "soft pad rather than a realistic gust. Vast, cold, open, "
            "contemplative. Clean and wide, with a long synthetic reverb tail. No "
            "voices, no narration, no birdsong detail, no lo-fi texture, no tape "
            "hiss, no static."
        ),
    },
    {
        "ma": "san",
        "nhip": (96, 4),
        "ten": "Sân tập",
        "dung": "Luyện võ (bc_san_tap, bc_san_sau…)",
        "file": "san.mp3",
        "mota": "Sân luyện võ: trống giữ nhịp đều, đàn tranh gọn, hơi thở làm lớp "
                "nền. Dạng nhạc nền game.",
        "prompt": (
            "Game ambience loop for a martial arts training yard in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — "
            "NOT a field recording. Layers: a steady drum (trống) keeping tempo "
            "like a metronome for practice, tight dan tranh plucks landing on the "
            "beat, a soft breath-like noise layer used as texture, and a wooden "
            "clapper accent on the bar line. Disciplined, physical, repetitive, "
            "hypnotic. Clean studio sound, not a live recording. No crowd, no "
            "cheering, no shouting in pain, no intelligible speech, no narration, "
            "no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "vuon",
        "nhip": (72, 3),
        "ten": "Vườn thuốc",
        "dung": "Vườn thảo dược, sườn núi hái thuốc (bc_vuon_thuoc…)",
        "file": "vuon.mp3",
        "mota": "Vườn thuốc: sáo cao, đàn tranh thưa, lớp đệm lá nhẹ. Dịu và thưa.",
        "prompt": (
            "Game ambience loop for a herb garden in a Vietnamese historical RPG. "
            "This is designed game audio, layered and stylized — NOT a field "
            "recording. Layers: a high bamboo flute (sáo) playing a short gentle "
            "pentatonic phrase, sparse plucked dan tranh notes with long gaps, and "
            "a soft filtered leaf-rustle pad underneath. A single water-drop accent "
            "as a texture on the bar line. Calm, green, airy, unhurried. Clean and "
            "intimate, with a light synthetic reverb. No voices, no narration, no "
            "bees or insects detail, no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "mieu",
        "nhip": (48, 2),
        "ten": "Miếu",
        "dung": "Miếu, từ đường, nơi thờ (bc_mieu_hoang, bc_mieu_trong…)",
        "file": "mieu.mp3",
        "mota": "Miếu cổ: chiêng ngân dài, nền trầm giữ, đàn bầu thỉnh thoảng. "
                "Rất tĩnh và thiêng.",
        "prompt": (
            "Game ambience loop for an old mountain shrine in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — "
            "NOT a field recording. Layers: a bronze chiêng gong struck once, its "
            "long inharmonic partials decaying and beating slowly, a sustained low "
            "drone underneath, and a single đàn bầu note bending gently. Enormous "
            "quiet, wide reverberant space, sacred and still. Clean and deep, with "
            "a long synthetic reverb tail. No chanting, no voices, no narration, no "
            "lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "dem",
        "nhip": (72, 3),
        "ten": "Đêm",
        "dung": "Ban đêm, tập kích, chữa thương trong đêm (bc_dem_tap_kich, "
                "bc_khe_nui_dem…)",
        "file": "dem.mp3",
        "mota": "Đêm: đàn bầu ngân là chính, nền trầm, tiếng côn trùng cách điệu. "
                "Tối và tĩnh.",
        "prompt": (
            "Game ambience loop for a night scene in open countryside in a "
            "Vietnamese historical RPG. This is designed game audio, layered and "
            "stylized — NOT a field recording. Layers: a slow đàn bầu melody with "
            "its characteristic pitch bend as the leading voice, a deep sustained "
            "drone beneath it, and a stylized high shimmer suggesting distant "
            "insects — synthesized, not sampled. Dark, wide, lonely, suspended. "
            "Clean and spacious, with a long synthetic reverb. No dogs, no voices, "
            "no narration, no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "lang",
        "nhip": (96, 4),
        "ten": "Làng",
        "dung": "Làng, xóm, cổng cộng đồng, quán trà, quán rượu (bc_tan_xa, "
                "bc_cong_dong, bc_quan_nuoc…)",
        "file": "lang.mp3",
        "mota": "Làng quê: đàn tranh ấm, sáo nhẹ, trống thưa, tiếng người mờ. "
                "Ấm và thưa.",
        "prompt": (
            "Game ambience loop for a small farming village in a Vietnamese "
            "historical RPG. This is designed game audio, layered and stylized — "
            "NOT a field recording. Layers: a warm dan tranh figure in a pentatonic "
            "mode as the main voice, a soft bamboo flute answering it, a sparse "
            "drum (trống) marking the phrase, and a very low bed of indistinct "
            "murmuring voices with no clear words. Warm, ordinary, unhurried, "
            "homely. Clean and close, with a light synthetic reverb. No "
            "intelligible speech, no narration, no radio voice, no television, no "
            "traffic, no lo-fi texture, no tape hiss, no static."
        ),
    },
    {
        "ma": "tinh",
        "nhip": (48, 2),
        "ten": "Tĩnh",
        "dung": "Yên ắng: trong nhà, hiệu thuốc, lúc thiền (bc_hoi_uc, cảnh còn lại)",
        "file": "tinh.mp3",
        "mota": "Yên ắng: nền trầm rất nhẹ, thỉnh thoảng một tiếng chuông xa. "
                "Không phải im lặng hỏng file.",
        "prompt": (
            "Game ambience loop for a quiet interior in a Vietnamese historical "
            "RPG. This is designed game audio, layered and stylized — NOT a field "
            "recording. Layers: a very soft low drone as a bed, barely audible, and "
            "one distant bell tone decaying across the loop. The impression of a "
            "large still space that is deliberately quiet — not a recording that "
            "failed. Clean, intentional, minimal. No voices, no narration, no "
            "electrical hum, no air-conditioning, no wind, no lo-fi texture, no "
            "tape hiss, no static."
        ),
    },
]

CHUNG = (
    "Style: this is game audio, not a field recording and not a radio broadcast. "
    "Designed, layered, clean and stylized, the way a game soundtrack or ambience "
    "bed sounds — not a microphone in a real place. Use Vietnamese instruments "
    "(dan tranh, sáo, trống, chiêng, đàn bầu) and a pentatonic mode where the "
    "prompt asks for them. Full-range mix with real low end (the music must have "
    "weight below 120 Hz) and air above 5 kHz — do not band-limit it to the "
    "telephone band. No intelligible speech, no narration, no radio voice, no DJ. "
    "No lo-fi texture, no tape hiss, no vinyl crackle, no static, no radio tuning "
    "noise. No clipping, no distortion, no sudden loud peaks. Peak level below "
    "-3 dBFS. Loopable bed, not a finished track: no intro, no ending, no fade."
)


def prompt_day_du(n):
    """Prompt hoàn chỉnh: thân + đuôi 10 giây + quy ước chung."""
    nhip, o_nhip = n.get("nhip", NHIP_MAC_DINH)
    return n["prompt"].strip() + " " + duoi(nhip, o_nhip) + "\n\n" + CHUNG
