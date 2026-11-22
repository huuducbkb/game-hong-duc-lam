"""Dữ liệu tiếng cảnh — MỖI CẢNH MỘT FILE RIÊNG.

Trước đây gom 9 nhóm, nên một file phải gánh nhiều ngữ cảnh khác nhau: tiếng
"chợ sớm lúc sạp còn đang dựng" bị dùng luôn cho "góc chợ chiều mòn mỏi". Nghe
là thấy sai. Giờ mỗi ảnh trong game có file riêng, từ khoá riêng.

Mỗi cảnh có hai bộ từ khoá, phục vụ hai việc khác nhau:
  `tim`   — cụm tiếng Anh để tìm nguồn trên thư viện âm thanh (Freesound,
            Pixabay, YouTube). Đây là thứ người ta đặt tên cho file.
  `mo_ta` — cụm tiếng Anh mô tả chính âm thanh đó, để dán vào Google khi cần
            tìm hiểu hoặc tìm nguồn khác.

Không còn prompt: hiện chưa có công cụ nào tạo được âm thanh môi trường đúng
kiểu này từ prompt, nên giữ lại chỉ làm rối trang.

`nhom` là nhóm cũ, dùng làm đường lùi: cảnh chưa có file riêng thì game dùng
file nhóm nếu nhóm đó đã có.
"""

# moi: (ma, ten, nhom, anh, tim[3], mo_ta[3], mota)
MOI = [
    # ---------------- CHỢ ----------------
    ("cho_01", "Chợ sớm Thất Huyền trấn", "cho", "bc_cho_01.jpg",
     ["morning market ambience", "market opening early morning",
      "empty market stalls setting up"],
     ["sparse market early morning ambience", "wooden stalls being set up sound",
      "quiet market before crowds"],
     "Chợ lúc sạp còn đang dựng: gỗ kéo trên đất, sọt và hũ đặt xuống, bước chân "
     "thưa, bàn tán rất khẽ. Chưa đông, chưa có tiếng rao."),

    ("cho_02", "Ngõ nhỏ sau chợ — lời đồn", "cho", "bc_cho_02.jpg",
     ["narrow alley ambience", "market back alley sound",
      "close alleyway footsteps"],
     ["tight alley reverb ambience", "narrow lane background voices",
      "alley behind market ambience"],
     "Ngõ hẹp sau chợ: tiếng vọng sát vách, bước chân gần, giọng nói nhỏ ngay sau "
     "bức tường, đồ đạc khua trong sân. Chen chúc, kín, không thoáng."),

    ("cho_03", "Góc chợ — một ngày mòn mỏi", "cho", "bc_cho_03.jpg",
     ["late afternoon market ambience", "market winding down evening",
      "crowd thinning ambience"],
     ["tired market end of day ambience", "market packing up sound",
      "evening market sparse crowd"],
     "Chợ lúc chiều muộn, đã thưa: người dọn hàng, thùng gỗ đậy lại, bước chân "
     "mệt, tiếng nói rời rạc. Không còn huyên náo, chỉ còn mệt."),

    # ---------------- TRẬN CHIẾN ----------------
    ("tran_lua", "Dã Lang Bang tập kích", "tran", "bc_tran_lua.jpg",
     ["raid attack ambience", "burning village attack", "chaos attack night"],
     ["sudden attack chaos ambience", "fire and screaming distant",
      "raid panic soundscape"],
     "Tập kích bất ngờ: hỗn loạn bùng lên, lửa cháy, tiếng hét không rõ chữ, đồ "
     "vật vỡ, chạy loạn. Chưa thành trận đánh — còn là hoảng loạn."),

    ("tran_lua_2", "Xuống trấn — cứu dân", "tran", "bc_tran_lua_2.jpg",
     ["rescue amid fire ambience", "burning street ambience",
      "emergency crowd fire"],
     ["fire rescue background sound", "burning town street ambience",
      "people fleeing fire sound"],
     "Chạy xuống trấn giữa lửa: cháy gần, gỗ nổ, người gọi nhau, bước chân dồn "
     "trên đá. Chen giữa đám đông đang tháo chạy."),

    ("tran_lua_3", "Thất Huyền Môn — cổng vỡ", "tran", "bc_tran_lua_3.jpg",
     ["gate breaking battle ambience", "wooden gate smash sound",
      "siege breach ambience"],
     ["heavy gate crashing sound", "fortified gate breaking ambience",
      "battle at gate soundscape"],
     "Cổng gỗ vỡ: tiếng gỗ lớn gãy, bản lề bật, đám đông tràn qua. Nặng, chát, có "
     "lực va đập thật."),

    ("cong_dong_doi_mat", "Cổng đông — đối mặt địch", "tran",
     "bc_cong_dong_doi_mat.jpg",
     ["standoff tension ambience", "facing enemy silence",
      "western gate confrontation"],
     ["tense standoff quiet ambience", "before fight tension sound",
      "two sides facing ambience"],
     "Đối mặt trước khi đánh: căng, gần như im, chỉ có gió, thở, và tiếng vải áo "
     "khẽ động. Chưa có tiếng thép — chính cái im mới là căng."),

    ("cong_dong_giau", "Cổng đông — giấu thực lực", "tran",
     "bc_cong_dong_giau.jpg",
     ["held breath tension ambience", "restrained fight ambience",
      "quiet defensive stance"],
     ["suppressed tension ambience", "controlled breathing fight sound",
      "holding back ambience"],
     "Giấu lực: tiếng đánh bị nén lại, hơi thở giữ, bước chân chậm và chắc. Không "
     "bùng nổ, nhưng nặng."),

    ("cong_dong_toan_luc", "Cổng đông — dùng toàn lực", "tran",
     "bc_cong_dong_toan_luc.jpg",
     ["full power strike ambience", "explosive impact fight sound",
      "all out attack ambience"],
     ["powerful impact ambience", "full force martial exchange",
      "explosive clash soundscape"],
     "Toàn lực: va đập mạnh, gió bị xé, đất bật, hơi thở bung ra. To nhất trong "
     "nhóm cổng đông."),

    ("cong_dong_quyen", "Cổng đông — Thất Huyền quyền", "tran",
     "bc_cong_dong_quyen.jpg",
     ["martial arts fist exchange ambience", "punch impact ambience",
      "close combat sound"],
     ["fist strike impact sound", "close quarters combat ambience",
      "martial exchange soundscape"],
     "Đánh tay gần: quyền chạm quyền, tay áo phần phật, bước xoay trên đá, hơi thở "
     "đều. Gần và khô, không có nhạc."),

    ("cong_dong_hung_ba", "Cổng đông — gọi tên Hùng Bá", "tran",
     "bc_cong_dong_hung_ba.jpg",
     ["shout across courtyard ambience", "voice calling out echo",
      "sudden halt ambience"],
     ["single shout echo courtyard", "challenge shout ambience",
      "everything stops sound"],
     "Một tiếng gọi vang lên giữa sân: mọi thứ khựng lại, chỉ còn tiếng vọng và "
     "gió. Có giọng người nhưng không rõ chữ."),

    ("hoa_truong_cuu", "Hỏa trường — cứu người", "tran", "bc_hoa_truong_cuu.jpg",
     ["fire scene rescue ambience", "burning debris crackle",
      "smoke fire crackle sound"],
     ["fire crackling close ambience", "burning wood debris sound",
      "rescue in smoke ambience"],
     "Giữa đám cháy: lửa nổ lách tách, gỗ cháy sụp, khói, bước chân vội trên tro. "
     "Lửa là chính, người ở phía sau."),

    # ---------------- NÚI ----------------
    ("duong_mon_nui", "Đường mòn lên núi — chạng vạng", "nui",
     "bc_duong_mon_nui.jpg",
     ["mountain trail dusk ambience", "mountain path wind ambience",
      "hiking trail evening sound"],
     ["dusk mountain trail ambience", "wind on mountain path",
      "evening mountain walk soundscape"],
     "Đường mòn chạng vạng: gió qua đá và cỏ khô, bước chân trên sỏi, không gian "
     "rộng. Chưa tối hẳn, còn tiếng chim xa."),

    ("khe_nui_dem", "Hậu sơn — khe núi đêm", "nui", "bc_khe_nui_dem.jpg",
     ["mountain ravine night ambience", "narrow canyon wind night",
      "night mountain gorge sound"],
     ["night ravine wind ambience", "canyon echo night sound",
      "cold mountain night ambience"],
     "Khe núi ban đêm: gió dồn trong khe hẹp, vọng lại, côn trùng thưa, lạnh. Hẹp "
     "hơn đường mòn, có tiếng vọng."),

    ("khe_nui_chon", "Hậu sơn — chôn trả lại", "nui", "bc_khe_nui_chon.jpg",
     ["digging soil night ambience", "shovel dirt quiet night",
      "burying ground night sound"],
     ["digging in earth sound", "soil shovel night ambience",
      "quiet burial ground ambience"],
     "Đào đất ban đêm trong khe núi: xẻng lưỡi vào đất, sỏi rời, hơi thở nặng, gió "
     "khe núi phía sau. Việc nặng, làm lặng lẽ."),

    # ---------------- SÂN TẬP ----------------
    ("san_tap_ngay", "Sân tập Thất Huyền Môn — giữa ngày", "san",
     "bc_san_tap_ngay.jpg",
     ["training courtyard day ambience", "martial arts practice ambience",
      "many students training sound"],
     ["busy training yard ambience", "group martial practice sound",
      "daytime courtyard activity"],
     "Sân tập giữa ngày, đông: nhiều người cùng luyện, chân trên đất nện, vải áo "
     "phần phật, tiếng đếm nhịp xa. Đều và có nhịp của buổi tập."),

    ("san_tap_chen_ep", "Sân tập — bị chèn ép", "san", "bc_san_tap_chen_ep.jpg",
     ["tense courtyard ambience", "crowd mocking ambience",
      "hostile crowd murmur"],
     ["hostile crowd murmur ambience", "tense training yard sound",
      "uncomfortable crowd ambience"],
     "Bị vây giữa sân: tiếng cười khẽ, bàn tán chế giễu ở phía sau, bước chân vòng "
     "quanh. Không ai nói to, nhưng không thân thiện."),

    ("san_tap_cai_lai", "Sân tập — cãi lại", "san", "bc_san_tap_cai_lai.jpg",
     ["argument courtyard ambience", "raised voices argument sound",
      "confrontation crowd ambience"],
     ["angry voices argument ambience", "sudden silence after shout",
      "tense confrontation sound"],
     "Cãi lại: giọng bật lên giữa sân, rồi im phăng phắc, rồi xì xào. Có giọng "
     "người nhưng không rõ chữ."),

    ("san_sau_luyen_dem", "Tân xá — luyện lén trong đêm", "san",
     "bc_san_sau_luyen_dem.jpg",
     ["night training alone ambience", "quiet night practice sound",
      "solo martial practice night"],
     ["secret night training ambience", "quiet courtyard night sound",
      "lone practice at night"],
     "Luyện lén ban đêm: rất ít tiếng, chân trần trên đất, hơi thở nén, vải khẽ "
     "động. Phải giữ im nên mọi thứ đều nhỏ."),

    ("san_sau_anh_sang", "Sân sau — đêm, dưới gốc cổ thụ", "san",
     "bc_san_sau_anh_sang.jpg",
     ["night tree wind ambience", "old tree leaves night",
      "quiet garden night ambience"],
     ["large tree wind night ambience", "leaves overhead night sound",
      "still night garden ambience"],
     "Dưới gốc cổ thụ ban đêm: lá trên cao xào xạc, thân cây khẽ kêu, côn trùng "
     "thưa, không gian tĩnh."),

    ("san_sau_chon_lai", "Sân sau — chôn trả lại", "san",
     "bc_san_sau_chon_lai.jpg",
     ["digging soil night garden ambience", "shovel earth quiet sound",
      "burying backyard night"],
     ["digging garden soil sound", "quiet night digging ambience",
      "earth shovel night sound"],
     "Đào đất trong sân sau ban đêm: xẻng vào đất mềm, đất rơi, thở nặng, lá cây "
     "phía trên. Kín đáo, phải làm nhanh."),

    # ---------------- VƯỜN THUỐC ----------------
    ("vuon_thuoc_gap", "Vườn thuốc phía sau môn", "vuon", "bc_vuon_thuoc_gap.jpg",
     ["herb garden ambience", "medicinal garden morning sound",
      "garden leaves insects ambience"],
     ["herb garden morning ambience", "leaves rustle garden sound",
      "quiet walled garden ambience"],
     "Vườn thuốc buổi sáng: lá cọ nhau trong gió nhẹ, ong gần, côn trùng thưa, một "
     "con chim từ trên tường đáp lại. Ấm, kín, không người."),

    ("vuon_thuoc_hoi", "Vườn thuốc — hỏi thẳng", "vuon", "bc_vuon_thuoc_hoi.jpg",
     ["garden conversation ambience", "two people talking garden",
      "quiet garden voices"],
     ["low voices garden ambience", "tense conversation outdoor sound",
      "garden background voices"],
     "Hỏi thẳng trong vườn: hai giọng nói thấp, ngắt quãng, lá vẫn cọ phía sau. "
     "Không rõ chữ, nhưng nghe ra là đang gặng."),

    ("vuon_thuoc_im", "Vườn thuốc — im lặng", "vuon", "bc_vuon_thuoc_im.jpg",
     ["silent garden ambience", "still herb garden sound",
      "quiet garden no voices"],
     ["very quiet garden ambience", "still air garden sound",
      "silent outdoor ambience"],
     "Im lặng trong vườn: chỉ còn lá, gió, côn trùng rất xa. Không giọng người. "
     "Cái im này là cố ý, không phải file hỏng."),

    ("vuon_thuoc_ngoc", "Vườn thuốc — Mạc Đại Phu và khối ngọc", "vuon",
     "bc_vuon_thuoc_ngoc.jpg",
     ["garden with object handling ambience", "stone object set down sound",
      "quiet garden handling"],
     ["handling stone object ambience", "quiet garden with voices",
      "something placed on wood sound"],
     "Trong vườn, có người đang cầm một vật nặng: đá hoặc ngọc đặt xuống gỗ, vải "
     "bọc mở ra, lá vẫn động phía sau. Trầm và kín."),

    ("vuon_thuoc_dem", "Vườn thuốc — chôn trả lại", "vuon",
     "bc_vuon_thuoc_dem.jpg",
     ["night garden digging ambience", "soil digging night sound",
      "quiet garden night work"],
     ["night digging garden ambience", "dirt shovel quiet night",
      "garden at night ambience"],
     "Đào đất trong vườn thuốc ban đêm: đất mềm hơn sân sau, rễ cây đứt, lá bị gạt "
     "sang, thở nén. Làm lặng lẽ giữa luống thuốc."),

    # ---------------- MIẾU ----------------
    ("mieu_hoang", "Ngoài miếu — quan sát", "mieu", "bc_mieu_hoang.jpg",
     ["ruined shrine exterior ambience", "abandoned temple outside sound",
      "night shrine approach"],
     ["approaching ruined shrine ambience", "abandoned building exterior sound",
      "quiet night approach ambience"],
     "Ngoài miếu hoang: gió lùa qua tường vỡ, côn trùng đêm, không gian trống. "
     "Đứng ngoài quan sát, chưa vào trong."),

    ("mieu_trong", "Trong miếu — xác người còn ấm", "mieu", "bc_mieu_trong.jpg",
     ["empty stone shrine interior ambience", "temple room tone reverb",
      "cold stone hall sound"],
     ["stone room reverb ambience", "empty shrine interior room tone",
      "cold stone hall reverb"],
     "Trong miếu đá: vọng dài, lạnh, gió qua cửa, bụi rơi. Rất ít tiếng nhưng không "
     "im — chính căn phòng có tiếng của nó."),

    ("doat_hop", "Đoạt hộp — Đỗ Tam phản phệ", "mieu", "bc_doat_hop.jpg",
     ["struggle inside temple ambience", "scuffle stone floor sound",
      "sudden collapse ambience"],
     ["struggle and impact ambience", "stone floor scuffle sound",
      "sudden body fall ambience"],
     "Giằng co trong miếu: chân trượt trên đá, va đập, một tiếng sụp xuống, rồi "
     "vọng trong phòng đá. Ngắn và dữ."),

    ("tu_khiem", "Tu luyện kiếm đạo — đêm đầu", "mieu", "bc_tu_khiem.jpg",
     ["sword practice night ambience", "blade moving air sound",
      "quiet night sword training"],
     ["sword swishing air ambience", "metal blade night practice",
      "quiet sword handling sound"],
     "Luyện kiếm trong miếu đêm: lưỡi kiếm xé không khí, kim loại khẽ rít, bước "
     "chân xoay trên đá, hơi thở đều. Sắc và lạnh."),

    # ---------------- ĐÊM ----------------
    ("tan_xa_dem", "Tân xá — tu luyện đêm đầu", "dem", "bc_tan_xa_dem.jpg",
     ["night room cultivation ambience", "quiet night dormitory sound",
      "night insects interior"],
     ["quiet night interior ambience", "night dormitory room tone",
      "crickets outside window night"],
     "Đêm trong tân xá: côn trùng ngoài cửa sổ, giường gỗ khẽ kêu, hơi thở đều, "
     "không gian chật. Yên nhưng không im."),

    ("dem_tap_kich", "Đêm cuối — Dã Lang Bang tập kích", "dem",
     "bc_dem_tap_kich.jpg",
     ["night raid attack ambience", "night attack chaos sound",
      "sudden night assault"],
     ["night attack chaos ambience", "distant screams fire night",
      "sudden assault at night sound"],
     "Đêm bị tập kích: từ im lặng bùng thành hỗn loạn, lửa, hét xa, chạy. Nửa đầu "
     "là đêm, nửa sau là loạn."),

    # ---------------- LÀNG ----------------
    ("tan_hoang", "Sau trận — giữa đống đổ nát", "lang", "bc_tan_hoang.jpg",
     ["aftermath ruins ambience", "post battle destruction sound",
      "burned ruins quiet"],
     ["burnt ruins ambience", "aftermath destruction quiet sound",
      "smouldering debris ambience"],
     "Sau trận, giữa đống đổ nát: lửa còn âm ỉ, gỗ cháy khẽ nổ, gió qua tường sập, "
     "không còn ai. Trống và nặng."),

    ("binh_minh", "Kết chương — bình minh Thất Huyền trấn", "lang",
     "bc_binh_minh.jpg",
     ["dawn town ambience", "early morning village sunrise sound",
      "quiet dawn birds"],
     ["dawn ambience with birds", "sunrise quiet town sound",
      "early morning calm ambience"],
     "Bình minh trên trấn: chim sớm, gà xa, gió nhẹ, rất ít người đã dậy. Nhẹ và "
     "sạch, sau những gì vừa xảy ra."),

    ("tan_xa_sang", "Tân xá Thất Huyền Môn — sáng", "lang", "bc_tan_xa_sang.jpg",
     ["dormitory morning ambience", "morning courtyard activity sound",
      "students waking morning"],
     ["morning dormitory ambience", "people waking up sound",
      "morning activity courtyard"],
     "Tân xá buổi sáng: người dậy, cửa mở, nước đổ, bước chân ra sân, nói chuyện "
     "thường ngày. Đời thường, không có gì đặc biệt."),

    ("quan_nuoc", "Quán nước đầu trấn — dò tin", "lang", "bc_quan_nuoc.jpg",
     ["tea house ambience", "tavern chatter ambience", "busy tea stall sound"],
     ["tea house background chatter", "tavern murmur ambience",
      "cups and voices ambience"],
     "Quán nước: chén đặt xuống, nước rót, nhiều giọng nói chồng lên, tiếng cười "
     "thưa. Không rõ chữ — chỉ là chỗ đông người."),

    ("tan_xa_song_tu", "Tân xá — đêm, lần song tu đầu tiên", "lang",
     "bc_tan_xa_song_tu.jpg",
     ["quiet night room ambience", "night interior breathing sound",
      "still night dormitory"],
     ["quiet night room tone", "soft night interior ambience",
      "night stillness sound"],
     "Đêm trong phòng: rất tĩnh, hơi thở, vải khẽ động, côn trùng xa. Kín và riêng "
     "tư, không có gì ồn."),

    ("tan_xa_kho_tu", "Tân xá — khổ tu, lần thất bại", "lang",
     "bc_tan_xa_kho_tu.jpg",
     ["night exhausted breathing ambience", "quiet room tired sound",
      "frustrated night silence"],
     ["heavy breathing quiet room", "exhausted night ambience",
      "frustration silent room sound"],
     "Khổ tu thất bại: hơi thở mệt và gấp, rồi thở dài, im. Có cái nặng trong "
     "phòng, không phải tiếng động lớn."),

    ("tan_xa_suyt_lo", "Tân xá — suýt bị phát hiện", "lang",
     "bc_tan_xa_suyt_lo.jpg",
     ["held breath tension room ambience", "someone approaching quiet",
      "near discovery tension"],
     ["tense held breath ambience", "footsteps approaching quiet room",
      "near miss tension sound"],
     "Suýt bị phát hiện: nín thở, bước chân người khác tới gần rồi đi qua, im lại. "
     "Căng, không có tiếng lớn."),

    ("tan_xa_dot_pha", "Tân xá — đột phá Luyện Khí tầng hai", "lang",
     "bc_tan_xa_dot_pha.jpg",
     ["energy surge ambience", "breakthrough moment sound",
      "low rumble rising ambience"],
     ["rising energy rumble ambience", "breakthrough surge sound",
      "deep hum building ambience"],
     "Đột phá: một luồng trầm dâng lên rồi lắng xuống, không khí rung nhẹ, rồi trở "
     "lại tĩnh. Không phải nhạc — là rung của không gian."),

    ("mon_phai_tan_hoang", "Sau trận — giữa đống đổ nát", "lang",
     "bc_mon_phai_tan_hoang.jpg",
     ["sect ruins aftermath ambience", "destroyed courtyard quiet",
      "post battle rubble sound"],
     ["destroyed building ambience", "rubble and wind ambience",
      "quiet ruins aftermath sound"],
     "Đống đổ nát của môn phái: tường sập, gỗ gãy còn rơi lả tả, gió lùa qua khoảng "
     "trống, không người. Rộng và trống hơn sân sau."),

    ("binh_minh_ngoc_cot", "Kết chương — bình minh Thất Huyền Môn", "lang",
     "bc_binh_minh_ngoc_cot.jpg",
     ["dawn temple courtyard ambience", "sunrise mountain gate sound",
      "early morning quiet sect"],
     ["dawn courtyard ambience", "sunrise quiet mountain air",
      "early morning stillness sound"],
     "Bình minh ở cổng môn: gió núi nhẹ, chim sớm, chuông rất xa, sân còn vắng. "
     "Sạch và cao, khác bình minh dưới trấn."),

    # ---------------- TĨNH ----------------
    ("dot_pha", "Đột phá Luyện Khí", "tinh", "bc_dot_pha.jpg",
     ["quiet room tone ambience", "still interior room sound",
      "silent meditation ambience"],
     ["very quiet room tone", "silent interior ambience",
      "stillness with low presence"],
     "Yên ắng trong phòng kín: gỗ khẽ kêu, cửa sổ động rất nhẹ, không khí có trọng "
     "lượng. Không phải file hỏng — là phòng cố ý im."),
]


def _khoi(m):
    ma, ten, nhom, anh, tim, mo_ta, mota = m
    return {
        "ma": ma, "ten": ten, "nhom": nhom, "anh": anh, "file": ma + ".mp3",
        "tim": tim, "mo_ta": mo_ta, "mota": mota,
    }


CANH = [_khoi(m) for m in MOI]
THEO_MA = {c["ma"]: c for c in CANH}
THEO_ANH = {c["anh"]: c for c in CANH}

# Nhóm cũ -> tên hiển thị, dùng để chia đề mục trong trang xưởng.
NHOM = [
    ("cho", "Chợ"), ("tran", "Trận chiến"), ("nui", "Núi"),
    ("san", "Sân tập"), ("vuon", "Vườn thuốc"), ("mieu", "Miếu"),
    ("dem", "Đêm"), ("lang", "Làng"), ("tinh", "Tĩnh"),
]
TEN_NHOM = dict(NHOM)


def canh_theo_nhom(nhom):
    return [c for c in CANH if c["nhom"] == nhom]


def ma_theo_anh(ten_anh):
    """Mã cảnh của một ảnh. Nhận cả tên trần lẫn đường dẫn đầy đủ."""
    t = str(ten_anh).split("/").pop()
    c = THEO_ANH.get(t)
    return c["ma"] if c else None
