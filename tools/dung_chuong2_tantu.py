"""Dựng nhánh TÁN TU của Chương 2 — đi riêng, không gặp nhánh môn phái.

Bạn đồng hành: kiếm linh Hồng Trần, hảo cảm 100 từ đầu chương.
Hai hướng với Hàn Lập: hảo cảm đủ thì thành bạn (mở khoá hành động),
hảo cảm thấp thì thành kẻ thù (bán đứng hắn cho tà tu).
"""


def doan(did, boi_canh, ke, lua_chon, hoi="Thân"):
    return {"id": did, "hoi": hoi, "boi_canh": boi_canh, "ke": ke, "lua_chon": lua_chon}


def chon(chu, den, hieu_ung=None, dieu_kien=None):
    o = {"chu": chu, "den": den}
    if hieu_ung:
        o["hieu_ung"] = hieu_ung
    if dieu_kien:
        o["dieu_kien"] = dieu_kien
    return o


GAP_KIEM_LINH = {"gap_npc": {"Hồng Trần": {"hao_cam": 100}}}
NPC = ["Hồng Trần"]


def dung():
    d = []

    d.append(doan(
        "c2_d11", "Thái Nam Sơn Cốc — mép thung lũng",
        "Ta đứng ở mép thung lũng, và lần đầu tiên trong đời, ta thấy người ta bay.\n\n"
        "Không phải nhảy cao. Không phải đu dây. Bay. Một người áo trắng đứng trên một thanh kiếm mảnh, "
        "lơ lửng cách mặt đất chừng ba trượng, rồi hạ xuống nhẹ như lá rụng.\n\n"
        "Ta đứng im rất lâu.\n\n"
        "“Đừng nhìn lâu,” — kiếm linh nói sau lưng ta. Giọng nó đã đỡ yếu hơn đêm qua, nhưng vẫn khô như đá. "
        "“Ngươi nhìn họ, rồi ngươi sẽ tưởng mình thiếu thứ gì. Ngươi không thiếu. Ngươi chỉ chưa trả giá.”\n\n"
        "“Trả giá bằng gì?”\n\n"
        "“Bằng chính cái ngươi đang có.” — Nó ngừng một nhịp. — “Xuống dưới kia đi. Cái chợ đó là hồng trần đậm nhất "
        "ngươi từng gặp. Kiếm này tu giữa đời, không tu trong hang. Ngươi xuống đó mà học.”\n\n"
        "Phía dưới, thung lũng trải ra như một cái chợ khổng lồ: hàng trăm lều trại dựng san sát, "
        "đèn lồng treo thành dãy, và ở giữa là một khoảng trống lớn nơi người ta bày hàng trên những tấm vải trải đất.",
        [chon("Xuống chợ", "c2_d12")],
        hoi="Mở"))

    d.append(doan(
        "c2_d12", "Chợ trong thung lũng — chiều",
        "Cái chợ này không giống bất kỳ cái chợ nào ta từng biết.\n\n"
        "Không ai rao. Không ai mặc cả to tiếng. Người ta ngồi sau tấm vải, hàng hoá bày trước mặt, "
        "và khi có khách thì nói rất khẽ — khẽ đến mức ta phải nín thở mới nghe được.\n\n"
        "Ta đi qua mấy dãy hàng. Không ai nhìn ta quá một nhịp. Đó là điều lạ nhất. Ở chợ phàm, "
        "một kẻ áo rách đi vào là bị nhìn từ cổng tới cuối dãy.\n\n"
        "“Họ không thấy ngươi,” — kiếm linh nói — “vì ngươi chưa đáng để thấy. Đừng lấy làm may.”\n\n"
        "Trước mặt ta, một người đàn ông đặt lên vải một viên đá trắng đục, nhỏ bằng đầu ngón tay. "
        "Người mua trả bằng ba viên khác, cũng trắng đục, nhưng sáng hơn.\n\n"
        "“Linh thạch,” — ta nói khẽ.\n\n"
        "“Linh thạch.” — Kiếm linh lặp lại, và lần này trong giọng nó có gì đó gần như dịu lại. — "
        "“Thứ tiền của người tu hành. Một viên hạ phẩm bằng cả căn nhà ở Gia Nguyên. Ngươi ôm hai thanh kiếm "
        "trong vạt áo mà chưa biết mình đang nghèo đến mức nào. Cũng chưa biết mình đang giàu đến mức nào.”",
        [chon("Hỏi kiếm linh: ta giàu ở đâu?", "c2_d12b"),
         chon("Đi thẳng vào dãy hàng phía đông", "c2_d13")]))

    d.append(doan(
        "c2_d12b", "Chợ trong thung lũng — chiều",
        "“Giàu ở đâu?” — ta hỏi.\n\n"
        "Kiếm linh im một lúc lâu, đủ để ta tưởng nó không buồn trả lời.\n\n"
        "“Ngươi có thứ mà cả cái chợ này đổi không được.” — Nó nói chậm. — “Hai thanh kiếm này không ăn linh thạch. "
        "Chúng ăn hồng trần — cái thứ người ta sống qua mỗi ngày mà không biết mình đang có. Một kẻ tu trong hang "
        "một trăm năm cũng không bằng một kẻ đi qua chợ này ba ngày, nếu kẻ đó biết nhìn.”\n\n"
        "“Biết nhìn là nhìn gì?”\n\n"
        "“Nhìn cái giá.” — Giọng nó lạnh trở lại. — “Ai trả gì cho ai. Ai cười, ai cúi, ai quay mặt. "
        "Ngươi nhìn được ba ngày, ta dạy ngươi thứ mà môn phái kia phải mất ba năm mới dạy xong.”\n\n"
        "Ta gật đầu, dù nó không nhìn thấy.",
        [chon("Đi vào dãy hàng phía đông", "c2_d13")]))

    d.append(doan(
        "c2_d13", "Dãy hàng phía đông — chạng vạng",
        "Ta thấy Hàn Lập trước khi hắn thấy ta.\n\n"
        "Hắn ngồi sau một tấm vải nhỏ, trước mặt bày mấy thứ: một cuốn sách ố, mấy lọ thuốc, và một mảnh ngọc trắng đục. "
        "Di vật của Mạc Đại Phu.\n\n"
        "Một gã áo gấm đứng trước tấm vải, cầm mảnh ngọc lên, xoay dưới đèn, rồi đặt xuống với vẻ chán chường.\n\n"
        "“Ngọc vụn,” — gã nói. — “Ba viên hạ phẩm, ta lấy cả.”\n\n"
        "Ta biết giá. Ta vừa học giá ở dãy bên kia. Mảnh ngọc ấy, nếu đúng như ta nghĩ, đáng giá gấp mười lần.\n\n"
        "“Đừng xen vào,” — kiếm linh nói, rất khẽ. — “Đây là chợ của người tu. Một kẻ ăn mày mở miệng ở đây "
        "thì mất mạng, không mất tiền.”\n\n"
        "Hàn Lập không nói gì. Hắn chỉ nhìn mảnh ngọc trong tay gã áo gấm, mặt không đổi sắc.",
        [chon("Bước vào, phá ngang", "c2_d14a",
              {"hao_cam": {"Hàn Lập": 12}}),
         chon("Đứng nhìn, để hắn tự quyết", "c2_d14b",
              {"hao_cam": {"Hàn Lập": -6}})]))

    d.append(doan(
        "c2_d14a", "Dãy hàng phía đông",
        "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
        "“Mảnh ngọc ấy,” — ta nói, giọng bình thản đến mức chính ta cũng ngạc nhiên — “không phải ngọc thường. "
        "Ngươi thử cầm nó dưới nắng xem.”\n\n"
        "Gã áo gấm nhíu mày, nhưng vẫn xoay mảnh ngọc. Ánh chiều xuyên qua, và trong lòng ngọc hiện lên một sợi chỉ sáng "
        "mảnh như tơ, chạy dọc từ đầu tới cuối.\n\n"
        "Mặt gã đổi hẳn.\n\n"
        "“Ngươi là ai?” — gã hỏi, giọng đã khác.\n\n"
        "“Kẻ vừa nói cho ngươi biết ngươi đang định mua hớ.” — Ta nghiêng đầu. — “Hoặc ngươi trả đúng giá, "
        "hoặc ngươi trả bằng danh dự. Ta không quan tâm cái nào. Nhưng ta đứng đây tới khi ngươi chọn.”\n\n"
        "Gã áo gấm nhìn ta một lúc. Rồi gã cười — không vui — đặt mảnh ngọc xuống, rút ra một túi nhỏ, "
        "đếm ra mười viên linh thạch, rồi bỏ đi.\n\n"
        "Hàn Lập nhìn túi linh thạch, rồi nhìn ta. Hắn không cảm ơn. Hắn chỉ nói một câu:\n\n"
        "“Ngươi biết giá.”\n\n"
        "“Ta mới học.”\n\n"
        "“Học ở đâu?”\n\n"
        "Ta không trả lời. Kiếm linh trong vạt áo khẽ rung, như cười.",
        [chon("Ngồi xuống cạnh hắn", "c2_d15",
              {"hao_cam": {"Hàn Lập": 6}})]))

    d.append(doan(
        "c2_d14b", "Dãy hàng phía đông",
        "Ta đứng nhìn.\n\n"
        "Gã áo gấm trả ba viên linh thạch. Hàn Lập nhận, không nói một lời, gói mảnh ngọc lại bằng vải cũ "
        "rồi cất vào trong áo — cất rất nhanh, rất kín, như thể hắn đã quen với việc bị lấy mất thứ gì đó.\n\n"
        "Gã áo gấm đi. Ta bước tới.\n\n"
        "“Mảnh ngọc ấy đáng giá hơn ba viên.”\n\n"
        "Hàn Lập ngẩng lên. Hắn nhìn ta một lúc, và trong mắt hắn không có gì — không giận, không tiếc, "
        "không cả trách ta đã đứng nhìn.\n\n"
        "“Ta biết,” — hắn nói.\n\n"
        "“Vậy sao ngươi bán?”\n\n"
        "“Vì ta cần tiền hôm nay, không cần giá đúng vào tháng sau.” — Hắn đứng dậy, phủi vải. — "
        "“Ngươi đứng đó từ đầu. Ta thấy ngươi.”\n\n"
        "Hắn không nói thêm. Nhưng câu đó ở lại với ta lâu hơn ta muốn.",
        [chon("Đi theo hắn", "c2_d15",
              {"hao_cam": {"Hàn Lập": 4}}),
         chon("Đứng lại, để hắn đi", "c2_d15",
              {"hao_cam": {"Hàn Lập": -8}})]))

    d.append(doan(
        "c2_d15", "Góc chợ — tối",
        "Đèn lồng trong thung lũng thắp lên cùng một lúc, và cái chợ đổi hẳn màu.\n\n"
        "Ta ngồi cạnh Hàn Lập trên một tảng đá, giữa hai dãy hàng đã bắt đầu dọn. Trong tay hắn là cuốn sách ố "
        "mua được ở quầy bên kia.\n\n"
        "“Ta đọc được chữ này,” — hắn nói, và giọng hắn có gì đó ta chưa từng nghe — như thể hắn đang tự nói với mình.\n\n"
        "Ta liếc. Những nét chữ ấy ta không đọc được. Nhưng kiếm linh trong vạt áo ta khẽ nói:\n\n"
        "“Trường Xuân Công. Tầng bốn tới tầng sáu. Thứ này ở chợ phàm không có.”\n\n"
        "Ta biết một thứ mà Hàn Lập không biết ta biết.",
        [chon("Nói cho hắn biết sách viết gì", "c2_d16a",
              {"hao_cam": {"Hàn Lập": 15}, "co_su_kien": ["noi_sach_cho_han_lap"]}),
         chon("Giấu, chưa nói", "c2_d16b",
              {"hao_cam": {"Hàn Lập": -10}, "co_su_kien": ["giu_kin_chuyen_sach"]})]))

    d.append(doan(
        "c2_d16a", "Góc chợ — tối",
        "“Trường Xuân Công,” — ta nói. — “Tầng bốn tới tầng sáu.”\n\n"
        "Hàn Lập ngẩng lên rất nhanh. Mắt hắn sắc lại, và lần đầu tiên ta thấy hắn nhìn ta như nhìn một người "
        "chứ không phải một cái bóng đi bên cạnh.\n\n"
        "“Ngươi đọc được chữ này?”\n\n"
        "“Không phải ta.” — Ta ngừng một nhịp, chọn lời. — “Ta có một thứ giúp ta đọc. Ta chưa thể nói là gì. "
        "Nhưng ta không muốn ngươi bán rẻ thứ này cho gã áo gấm nào nữa.”\n\n"
        "Hắn im lâu. Rồi hắn gật đầu, chậm.\n\n"
        "“Vậy thì ta nợ ngươi một lần.”\n\n"
        "“Ngươi nợ ta hai lần.” — Ta cười. — “Lần trước là mảnh ngọc.”\n\n"
        "“Ta nhớ.” — Hắn cất sách vào áo. — “Ta nhớ hết.”\n\n"
        "*Hắn nhớ hết.* Ta tin câu đó. Ta không biết vì sao, nhưng ta tin.",
        [chon("Hỏi hắn về Mạc Đại Phu", "c2_d17",
              {"hao_cam": {"Hàn Lập": 8}}),
         chon("Không hỏi gì, ngồi im", "c2_d17")]))

    d.append(doan(
        "c2_d16b", "Góc chợ — tối",
        "Ta im.\n\n"
        "Hàn Lập đọc thêm mấy dòng, rồi gấp sách lại. Hắn không hỏi ta có đọc được không. Hắn không hỏi gì cả.\n\n"
        "Nhưng khi hắn đứng dậy, hắn nói một câu, không quay đầu:\n\n"
        "“Ngươi im lâu quá.”\n\n"
        "“Sao?”\n\n"
        "“Không sao.” — Hắn bước đi. — “Chỉ là ta để ý.”\n\n"
        "Kiếm linh trong vạt áo khẽ nói, giọng khô:\n\n"
        "“Ngươi vừa giữ được một bí mật nhỏ và mất một thứ lớn hơn. Cân đi. Nhưng đừng cân lâu quá — "
        "ở cái chợ này, người ta không cho ngươi cân lại lần hai.”",
        [chon("Đi theo hắn", "c2_d17",
              {"hao_cam": {"Hàn Lập": -4}})]))

    d.append(doan(
        "c2_d17", "Rìa thung lũng — đêm",
        "Đêm ấy ta ngủ ngoài trời, dưới một gờ đá, cách chỗ Hàn Lập nghỉ chừng hai mươi bước.\n\n"
        "Thung lũng ban đêm khác hẳn ban ngày. Đèn lồng tắt dần, và những vệt linh khí trở nên rõ hơn — "
        "chúng bay chậm, như đom đóm mệt.\n\n"
        "“Ngồi dậy,” — kiếm linh nói. — “Ta dạy ngươi thứ đầu tiên.”\n\n"
        "Ta ngồi. Hai thanh kiếm nằm ngang đùi, lạnh như đá sông.\n\n"
        "“Đừng hít linh khí. Linh khí là của người khác. Ngươi hít hồng trần.”\n\n"
        "“Hồng trần là gì?”\n\n"
        "“Là cái ngươi vừa làm hôm nay.” — Giọng nó chậm lại. — “Ngươi bước vào một cuộc mặc cả không phải của ngươi, "
        "và ngươi đổi một chút an toàn lấy một chút giá trị. Đó là hồng trần. Ngươi nhớ cái cảm giác ấy không?”\n\n"
        "Ta nhớ. Cảm giác khi gã áo gấm quay lại nhìn ta, và ta biết mình có thể bị giết.\n\n"
        "“Giữ nó,” — kiếm linh nói. — “Đừng để nó tan. Dẫn nó xuống đan điền như dẫn một dòng nước đục. "
        "Kiếm này mạnh lên bằng những gì ngươi đã sống qua, không bằng những gì ngươi ngồi yên.”\n\n"
        "Ta nhắm mắt. Trong người ta, một luồng ấm nóng dần tụ lại dưới rốn — không mát như linh khí, "
        "mà nóng, hơi rát, như uống rượu mạnh.",
        [chon("Dẫn tới cùng, chịu đau", "c2_d18",
              {"tu_vi": 40, "sinh_luc": -6}),
         chon("Dừng lại khi thấy rát", "c2_d18",
              {"tu_vi": 15})]))

    d.append(doan(
        "c2_d18", "Giữa thung lũng — sáng sớm",
        "Sáng hôm sau, giữa thung lũng có một đám đông tụ lại.\n\n"
        "Ta tới gần. Ở giữa đám đông là một cái bục đá thấp, và trên bục là một ông lão mặc áo xám dài, "
        "tóc bạc buộc gọn, tay chống một cây gậy gỗ trơn nhẵn.\n\n"
        "“Linh thạch hạ phẩm đổi một câu hỏi,” — ông nói, giọng không to nhưng ai cũng nghe. — "
        "“Trung phẩm đổi một lần chỉ. Thượng phẩm thì ta không dám nhận.”\n\n"
        "Đám đông cười. Nhưng không ai bước lên.\n\n"
        "“Gã này là ai?” — ta hỏi.\n\n"
        "“Vạn Tiểu Sơn,” — kiếm linh đáp. — “Tán tu. Luyện Khí tầng tám. Lão kiêu ngạo tới mức cả cái cốc này "
        "phải nể, vì lão là người duy nhất ở đây dám nói thẳng giá của từng thứ.”\n\n"
        "“Lão nói thật?”\n\n"
        "“Lão nói giá. Giá và thật là hai chuyện khác nhau. Nhưng ở đây, biết giá đã là sống.”",
        [chon("Bước lên, đặt một viên linh thạch", "c2_d19"),
         chon("Đứng ngoài nghe", "c2_d19b")]))

    d.append(doan(
        "c2_d19", "Bục đá — sáng",
        "Ta đặt viên linh thạch cuối cùng của mình xuống.\n\n"
        "Vạn Tiểu Sơn nhìn viên thạch, rồi nhìn ta — nhìn rất lâu, từ đầu tới chân, không vội.\n\n"
        "“Hỏi đi.”\n\n"
        "“Thăng Tiên Lệnh là gì?”\n\n"
        "Đám đông im bặt. Vạn Tiểu Sơn chậm rãi nhấc cây gậy lên, gõ xuống bục một tiếng.\n\n"
        "“Câu hỏi của kẻ không biết mình đang hỏi gì.” — Lão cười, không có vẻ gì là chế giễu. — "
        "“Thăng Tiên Lệnh là tấm lệnh cho phép ngươi bái nhập trực tiếp một trong Thất Đại Môn Phái. "
        "Không khảo hạch. Không xét linh căn. Kèm một viên Trúc Cơ Đan.”\n\n"
        "Lão cúi xuống, gần ta hơn.\n\n"
        "“Và cả cái Thái Nam Cốc này, mấy trăm con người, chỉ có ba tấm. Ba. Ngươi hiểu chưa?”\n\n"
        "Ta hiểu. Ta hiểu vì sao đám đông im.\n\n"
        "“Còn ai có?” — ta hỏi.\n\n"
        "“Một kẻ đã có.” — Lão đứng thẳng. — “Một kẻ đang giữ. Và một kẻ sẽ chết vì nó trong mấy ngày tới.”",
        [chon("Hỏi: kẻ nào đang giữ?", "c2_d20",
              {"co_su_kien": ["biet_ba_tam_lenh"]}),
         chon("Cúi đầu, rời đi", "c2_d20")]))

    d.append(doan(
        "c2_d19b", "Rìa đám đông — sáng",
        "Ta đứng ngoài nghe, và học được nhiều hơn một viên linh thạch đáng giá.\n\n"
        "Vạn Tiểu Sơn trả lời mười bảy câu hỏi trong buổi sáng ấy. Ta nhớ cả mười bảy.\n\n"
        "Linh thạch có bốn phẩm. Pháp khí chia theo cấp. Đan dược hỗ trợ tu luyện thì chia theo công dụng, "
        "không chia theo giá. Và thứ đắt nhất ở cái chợ này không phải pháp khí — mà là tin tức.\n\n"
        "“Ngươi nghe giỏi hơn ngươi nói,” — kiếm linh nhận xét. — “Đó là một đức tính. Đừng bỏ.”",
        [chon("Đi tìm Hàn Lập", "c2_d20")]))

    d.append(doan(
        "c2_d20", "Dãy hàng phía bắc — trưa",
        "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
        "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân nhỏ. "
        "Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
        "“Ba viên,” — bà ta nói. — “Không hơn.”\n\n"
        "“Năm.” — Hàn Lập không nhấc mắt. — “Thuốc này ta tự tay pha. Bà biết nó đáng bao nhiêu.”\n\n"
        "“Ta biết ngươi đang cần tiền.” — Bà ta cười. — “Đó là lý do ngươi chỉ được ba.”\n\n"
        "Hàn Lập im. Ta thấy vai hắn hơi siết.\n\n"
        "“Vì sao ngươi đi với ta?” — hắn hỏi bất ngờ, không quay lại.\n\n"
        "Câu hỏi ấy không dành cho bà bán đan.",
        [chon("“Vì ta cũng cần một người hiểu ta.”", "c2_d21",
              {"hao_cam": {"Hàn Lập": 10}}),
         chon("“Vì ta ghét bị trả giá.”", "c2_d21",
              {"hao_cam": {"Hàn Lập": 6}}),
         chon("Đứng nhìn, để hắn tự trả giá", "c2_d21",
              {"hao_cam": {"Hàn Lập": -10}}),
         chon("“Vì ngươi có thứ ta cần.”", "c2_d21",
              {"hao_cam": {"Hàn Lập": -15}})]))

    d.append(doan(
        "c2_d21", "Rìa thung lũng — chiều ngày thứ ba",
        "Ba ngày trôi qua.\n\n"
        "Ta học được nhiều thứ đến mức đầu ta đau. Rằng linh thạch có bốn phẩm. Rằng pháp khí chia theo cấp. "
        "Rằng có những kẻ ở đây đã tu hành cả trăm năm mà trông vẫn như thanh niên hai mươi.\n\n"
        "Và ta học được một thứ nữa, không ai dạy: rằng Hàn Lập không bao giờ hỏi thẳng một câu hai lần. "
        "Nếu hắn đã hỏi, hắn đã ghi câu trả lời vào đâu đó trong đầu.\n\n"
        "“Đêm nay ngươi ngủ đâu?” — hắn hỏi.\n\n"
        "“Ngoài gờ đá.”\n\n"
        "“Có người để ý ngươi rồi.” — Hắn nói, giọng đều. — “Ba kẻ. Áo xám, không có pháp khí, "
        "nhưng đi theo ngươi từ dãy đông tới giờ.”\n\n"
        "Ta không quay lại. Kiếm linh trong vạt áo khẽ nói: “Hắn nói đúng. Ta thấy chúng từ trưa.”\n\n"
        "“Vậy làm gì?” — ta hỏi.\n\n"
        "Hàn Lập nhìn ta. Lần này hắn nhìn lâu hơn mọi lần trước.",
        [chon("“Đêm nay ta ngủ chỗ ngươi.”", "c2_d22",
              {"hao_cam": {"Hàn Lập": 8}, "co_su_kien": ["ngu_cung_han_lap"]}),
         chon("“Ta tự lo được.”", "c2_d22b",
              {"hao_cam": {"Hàn Lập": -12}, "co_su_kien": ["tu_lo_mot_minh"]})]))

    d.append(doan(
        "c2_d22", "Khe đá — đêm",
        "Khe đá đủ cho hai người, không hơn.\n\n"
        "Chúng ta ép sát vào vách. Bên ngoài, cách chỗ ta chừng mười bước, có tiếng chân người chạy qua — "
        "rồi tiếng một vật nặng đổ, rồi im.\n\n"
        "Hàn Lập đặt tay lên vai ta. Hắn không nói. Nhưng bàn tay ấy nặng và ấm, và nó ở đó suốt một canh giờ.\n\n"
        "Khi tiếng chân đã xa hẳn, hắn mới rút tay về.\n\n"
        "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta mấy ngày.”\n\n"
        "Hắn im lâu đến mức ta tưởng hắn không trả lời.",
        [chon("“Vậy thì cùng nhau ra khỏi đây.”", "c2_d23"),
         chon("“Ta không cần ngươi hiểu ta.”", "c2_d23"),
         chon("“Ta sẽ không để ngươi chết một mình.”", "c2_d23")]))

    d.append(doan(
        "c2_d23", "Khe đá — gần sáng",
        "“Vì ngươi không giống những kẻ khác ở đây.” — Cuối cùng hắn nói. — “Những kẻ khác tới cái chợ này "
        "để lấy thứ gì đó. Ngươi tới để hiểu. Ta thấy được điều đó từ hôm đầu, khi ngươi đứng chắn trước tấm vải của ta.”\n\n"
        "“Ta tưởng ngươi không để ý.”\n\n"
        "“Ta để ý mọi thứ.” — Hắn nói, giọng đều. — “Đó là cách ta sống được tới giờ.”\n\n"
        "Bên ngoài, trời bắt đầu xám. Kiếm linh trong vạt áo khẽ nói, chỉ cho ta nghe:\n\n"
        "“Ngươi vừa có một thứ mà ta không dạy được. Giữ nó.”\n\n"
        "“Thứ gì?”\n\n"
        "“Một người.” — Nó ngừng. — “Ta đã sống lâu hơn ngươi tưởng, và ta chưa từng thấy ai giữ được thứ đó lâu. "
        "Nhưng ngươi thử đi.”\n\n"
        "Trời sáng. Ngày cuối của hội bắt đầu.",
        [chon("Ra khỏi khe đá", "c2_d24b",
              {"hao_cam": {"Hàn Lập": 5}})]))
    # --- nhánh hảo cảm thấp: Hàn Lập bỏ đi, người chơi tự lo ---
    d.append(doan(
        "c2_d22b", "Gờ đá — đêm",
        "“Ta tự lo được,” — ta nói.\n\n"
        "Hàn Lập nhìn ta một lúc. Rồi hắn gật đầu, rất nhẹ, và quay đi.\n\n"
        "“Vậy thì tự lo.”\n\n"
        "Đêm ấy ta ngồi một mình dưới gờ đá, hai thanh kiếm đặt ngang đùi. Ba kẻ áo xám tới lúc gần sáng.\n\n"
        "Ta không gọi ai. Ta cũng không cần gọi. Kiếm linh nói một câu duy nhất trước khi chúng tới:\n\n"
        "“Đánh thì đánh, nhưng đừng đánh như kẻ muốn thắng. Đánh như kẻ muốn sống.”\n\n"
        "Ta sống. Nhưng khi trời sáng, chỗ Hàn Lập nghỉ đã trống. Hắn đi lúc nào ta không biết. "
        "Hắn không để lại gì — không một lời, không một dấu.\n\n"
        "*Hắn không đợi ta.*",
        [chon("Đi tìm hắn", "c2_d23b"),
         chon("Không tìm. Đi đường của mình.", "c2_d23c")]))

    d.append(doan(
        "c2_d23b", "Thung lũng — sáng ngày thứ tư",
        "Ta tìm hắn suốt buổi sáng. Ta tìm thấy hắn ở dãy hàng phía bắc, và ta thấy hắn trước khi hắn thấy ta.\n\n"
        "Hắn đang nói chuyện với một kẻ áo xám. Không phải ba kẻ đêm qua. Kẻ này khác — áo xám nhưng có thêu chỉ bạc ở cổ tay, "
        "và đứng thẳng như người có chức phận.\n\n"
        "Hàn Lập đưa cho hắn một thứ. Ta không thấy rõ. Nhưng kẻ áo xám nhận, gật đầu, rồi đi về phía đông.\n\n"
        "Kiếm linh nói, rất khẽ: “Ngươi vừa thấy một cuộc giao dịch. Đừng hỏi hắn về nó. Hỏi là mất.”\n\n"
        "Ta đứng lại. Ta không bước tới.",
        [chon("Bỏ đi, không hỏi", "c2_d24b",
              {"co_su_kien": ["thay_han_lap_giao_dich"]}),
         chon("Bước tới, hỏi thẳng", "c2_d24b",
              {"hao_cam": {"Hàn Lập": -10}, "co_su_kien": ["hoi_thang_han_lap"]})]))

    d.append(doan(
        "c2_d23c", "Rìa thung lũng — chiều ngày thứ tư",
        "Ta không tìm.\n\n"
        "Ta đi về phía đông, tới chỗ bà lão đo linh căn, và ta trả một viên linh thạch cuối cùng để biết mình là thứ gì.\n\n"
        "Viên đá sáng lên — một sợi chỉ sáng mảnh như tơ, chạy dọc từ trong ra ngoài, không chen với màu nào khác.\n\n"
        "Bà lão nhìn rất lâu. Rồi bà cất viên đá đi, rất nhanh.\n\n"
        "“Thiên linh căn,” — bà nói, và giọng bà đổi hẳn. — “Một loại. Cả năm ta chưa thấy lần thứ hai.”\n\n"
        "“Nghĩa là tốt?”\n\n"
        "“Nghĩa là ngươi không được để ai biết.” — Bà nhìn quanh. — “Nghe cho kỹ. Ta đo linh căn bốn mươi năm. "
        "Tứ linh căn, ngũ hành linh căn — đám ấy vứt đi. Tam linh căn, song linh căn — còn dùng được. "
        "Còn một loại thì cả năm ta chưa thấy một lần. Thiên linh căn. Chân truyền đệ tử. Thiên tài của một tông môn.”\n\n"
        "Bà ngừng.\n\n"
        "“Và là thứ mà cả cái cốc này sẽ giết để có.”",
        [chon("Cúi đầu cảm ơn, đi", "c2_d24b",
              {"co_su_kien": ["biet_thien_linh_can"]})]))

    # --- cao trào: tà tu phong toả ---
    d.append(doan(
        "c2_d24b", "Giữa thung lũng — sáng ngày cuối",
        "Sáng ngày cuối, cái chợ đổi tính.\n\n"
        "Người ta dọn hàng nhanh hơn. Những tấm vải cuốn lại, lều hạ xuống, và ai cũng đi thành nhóm ba bốn người, "
        "không đi một mình.\n\n"
        "“Sao vậy?” — ta hỏi gã bán bánh khô.\n\n"
        "“Tà tu,” — gã nói, không ngẩng lên. — “Chúng phong toả cốc từ đêm qua. Không cho ai ra. "
        "Bắt người làm lô đỉnh. Ngươi muốn sống thì tìm chỗ nấp, đừng tìm đường ra.”\n\n"
        "Kiếm linh trong vạt áo khẽ rung.\n\n"
        "“Đây là lúc ta nói thật với ngươi,” — nó nói, giọng lạnh hơn mọi khi. — “Ngươi mới Luyện Khí tầng hai. "
        "Một tên tà tu thấp nhất ở đây cũng tầng năm. Ngươi không thắng được. Ngươi chỉ có thể chọn cách sống sót.”\n\n"
        "Phía đông, khói bắt đầu bốc lên.",
        [chon("Đi tìm Hàn Lập", "c2_d25",
              {"co_su_kien": ["di_tim_han_lap"]}),
         chon("Tự tìm chỗ nấp", "c2_d25b")]))

    d.append(doan(
        "c2_d25", "Khe đá — chạng vạng",
        "Ta tìm thấy Hàn Lập trước khi chúng tìm thấy.\n\n"
        "Hắn ngồi trong khe đá, cái hòm gỗ dựng bên cạnh, và trước mặt hắn là một cái bình nhỏ màu xanh — "
        "cao chừng hai đốt ngón tay, men đã sứt một miếng.\n\n"
        "“Cái này,” — hắn nói, đặt nó xuống tảng đá — “ta nhặt được ở Thất Huyền Môn. Trong đám đổ nát, sau trận.”\n\n"
        "“Là gì?”\n\n"
        "“Ta không biết.” — Hắn xoay cái bình. — “Ta đã thử đựng nước. Nước không đổi. Ta đã thử chôn nó. "
        "Nó lại nằm trên mặt đất sáng hôm sau. Ta đã thử bỏ nó. Nó quay lại trong túi ta.”\n\n"
        "Hắn nhìn ta.\n\n"
        "“Ngươi có thứ giúp ngươi đọc sách. Thứ đó có đọc được cái này không?”",
        [chon("Nhờ kiếm linh xem giúp", "c2_d26",
              {"co_su_kien": ["thay_chuong_thien_binh"], "hao_cam": {"Hàn Lập": 10}}),
         chon("“Ta không đọc được vật.”", "c2_d26",
              {"hao_cam": {"Hàn Lập": -5}}),
         chon("“Giấu nó đi. Đừng cho ai thấy.”", "c2_d26",
              {"hao_cam": {"Hàn Lập": 15}, "co_su_kien": ["khuyen_giau_binh"]})]))

    d.append(doan(
        "c2_d25b", "Hốc đá phía tây — chạng vạng",
        "Ta tự tìm chỗ nấp.\n\n"
        "Hốc đá phía tây hẹp, tối, và có một khe hở nhìn ra thung lũng. Ta nằm im, hai thanh kiếm đặt ngang ngực.\n\n"
        "Bên ngoài, tiếng đánh nhau tới gần rồi xa. Có tiếng ai đó hét lên một tiếng, rồi im hẳn.\n\n"
        "Rồi ta nghe một giọng khác — giọng người trẻ, lạnh, nói rất nhanh:\n\n"
        "“Lệnh bài đâu?”\n\n"
        "Và một giọng nữa, khàn hơn, đáp:\n\n"
        "“Ngươi… ngươi là ai…”\n\n"
        "Rồi im.\n\n"
        "Ta nằm im rất lâu. Kiếm linh không nói gì. Đến khi trời tối hẳn, nó mới nói một câu:\n\n"
        "“Ngươi vừa nghe thấy một người chết. Đừng quên tiếng đó. Nó sẽ dạy ngươi nhiều hơn ba ngày chợ.”",
        [chon("Bò ra, đi về phía bắc", "c2_d27b")]))

    d.append(doan(
        "c2_d26", "Khe đá — đêm ngày cuối",
        "Kiếm linh im rất lâu khi nhìn cái bình.\n\n"
        "Rồi nó nói, và giọng nó khác hẳn mọi khi — không lạnh, không khô, mà như có gì đó bị nén lại:\n\n"
        "“Cất nó đi. Đừng cho ai thấy. Đừng nói với ai — kể cả ta, sau này.”\n\n"
        "“Nó là gì?”\n\n"
        "“Là thứ mà nếu người ta biết ngươi có, thì cái cốc này sẽ không còn đủ chỗ cho xác ngươi.” — "
        "Nó ngừng. — “Ta không đọc được hết. Nhưng ta biết một điều: nó không thuộc về ngươi, và nó cũng không thuộc về hắn. "
        "Nó đang chờ một người.”\n\n"
        "Hàn Lập nhìn ta. Hắn không hỏi thêm. Hắn chỉ cất cái bình vào áo, rất chậm, rồi gật đầu.\n\n"
        "“Vậy thì ta giữ.”\n\n"
        "Bên ngoài, khói đã dày đặc. Tiếng chân người chạy qua khe đá, rồi tiếng một vật nặng đổ.",
        [chon("Ra ngoài xem", "c2_d27"),
         chon("Nằm im, chờ", "c2_d27")]))

    d.append(doan(
        "c2_d27", "Ngoài khe đá — chạng vạng",
        "Xác người nằm sấp trên đá. Áo trắng — không, áo xám đã bạc màu, và một vùng sẫm loang từ vai xuống hông.\n\n"
        "Hàn Lập quỳ xuống. Hắn không run. Đó là điều làm ta sợ nhất.\n\n"
        "Hắn luồn tay dưới người chết, luồn rất nhanh, rất thành thạo như một kẻ đã làm quen với việc này từ nhỏ. "
        "Khi hắn rút tay ra, trong tay hắn là một cái túi vải nhỏ màu xám — một túi trữ vật.\n\n"
        "“Đi,” — hắn nói, đứng dậy.\n\n"
        "“Khoan.” — Ta nắm vai hắn. — “Hắn là ai?”\n\n"
        "“Kim Quang Thượng Nhân.” — Hàn Lập nhìn xuống. — “Luyện Khí tầng chín. Hắn có một tấm Thăng Tiên Lệnh. "
        "Và hắn vừa định giết ta để lấy tấm thứ hai.”\n\n"
        "Hắn mở túi. Bên trong: một tấm lệnh bài, một mảnh kim quang lấp lánh, và vài viên linh thạch.\n\n"
        "“Hắn chết vì hắn chậm hơn ta một nhịp,” — Hàn Lập nói, giọng không có gì. — “Không có gì khác.”",
        [chon("“Ngươi vừa giết người.”", "c2_d28",
              {"hao_cam": {"Hàn Lập": 5}}),
         chon("Đứng nhìn, không nói gì", "c2_d28"),
         chon("“Vậy thì ta đi cùng ngươi.”", "c2_d28",
              {"hao_cam": {"Hàn Lập": 12}}),
         chon("“Ngươi là kẻ giết người.”", "c2_d28",
              {"hao_cam": {"Hàn Lập": -20}})]))

    d.append(doan(
        "c2_d28", "Rìa thung lũng — đêm ngày cuối",
        "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
        "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở rìa, chỗ những lều bị đốt. "
        "Đủ để thấy đường mà đi.\n\n"
        "Hàn Lập dừng lại ở miệng một khe núi, quay đầu nhìn lần cuối.\n\n"
        "“Ba tấm lệnh,” — hắn nói. — “Ta có ba tấm. Cả cái cốc này có ba tấm.”\n\n"
        "“Vậy ngươi sẽ đi đâu?”\n\n"
        "“Hoàng Phong Cốc.” — Hắn nói, không do dự. — “Một trong Thất Đại Môn Phái. Ở đó có người dạy ta cách dùng thứ này.”\n\n"
        "Hắn nhìn ta. Rồi hắn làm một việc ta không ngờ: hắn rút ra một tấm lệnh, đưa về phía ta.\n\n"
        "“Cầm.”\n\n"
        "“Ta không có gì đổi lại.”\n\n"
        "“Ta không đổi.” — Hắn vẫn cầm tấm lệnh. — “Ngươi đã đứng chắn trước tấm vải của ta hôm đầu. "
        "Ngươi đã nói cho ta biết cuốn sách viết gì. Ta không quên.”",
        [chon("Nhận tấm lệnh", "c2_d29",
              {"them_vat": [{"ten": "Thăng Tiên Lệnh", "so": 1,
                             "mo_ta": "Lệnh bài Hàn Lập đưa. Bái nhập trực tiếp một trong Thất Đại Môn Phái."}],
               "hao_cam": {"Hàn Lập": 20}},
              {"hao_cam": {"Hàn Lập": 50}}),
         chon("Không nhận, bảo hắn giữ đủ ba tấm", "c2_d29",
              {"hao_cam": {"Hàn Lập": 25}},
              {"hao_cam": {"Hàn Lập": 50}}),
         chon("“Ngươi giữ đi. Ta tự có đường.”", "c2_d29x",
              {"hao_cam": {"Hàn Lập": -15}},
              {"hao_cam_max": {"Hàn Lập": 49}})]))

    d.append(doan(
        "c2_d29", "Chân núi — gần sáng",
        "Trời sáng khi chúng ta ra tới chân núi.\n\n"
        "Thái Nam Cốc ở phía sau, im. Không còn tiếng, không còn lửa, không còn ai. "
        "Một cái chợ của mấy trăm người, và trong một đêm nó thành một cái thung lũng trống.\n\n"
        "Hàn Lập đứng bên ta, nhìn về phía nam.\n\n"
        "“Ta đi Hoàng Phong Cốc,” — hắn nói. — “Ngươi đi đâu?”\n\n"
        "Ta nhìn hai thanh kiếm trong tay. Chúng ấm — không phải vì nắng, mà vì thứ gì đó bên trong chúng vừa thức dậy.\n\n"
        "“Ta chưa biết,” — ta nói. — “Nhưng ta sẽ không đi đường của ngươi. Đường ngươi đi là đường của kẻ giấu mình. "
        "Ta phải đi giữa đời.”\n\n"
        "Hàn Lập gật đầu. Hắn không giận.\n\n"
        "“Vậy thì đừng chết.”\n\n"
        "“Ngươi cũng vậy.”\n\n"
        "Chúng ta chia tay ở chân núi, mỗi người một hướng. Ta không biết có gặp lại không.\n\n"
        "Nhưng ta biết một điều: hắn sẽ là người quan trọng nhất trong đời ta. Kiếm linh đã nói thế từ đêm đầu. "
        "Và kiếm linh chưa bao giờ nói sai.",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    # --- kết thù địch (tán tu) ---
    d.append(doan(
        "c2_d29x", "Chân núi — gần sáng",
        "“Ngươi giữ đi,” — ta nói. — “Ta tự có đường.”\n\n"
        "Hàn Lập nhìn tấm lệnh trong tay, rồi nhìn ta. Hắn cất nó đi, chậm.\n\n"
        "“Ngươi nghĩ ta đang thương hại ngươi.”\n\n"
        "“Ta nghĩ ngươi đang trả nợ.” — Ta nhún vai. — “Ta không cần nợ. Ta cũng không cần ngươi.”\n\n"
        "Câu đó ra khỏi miệng ta trước khi ta kịp nghĩ. Và ta thấy nó trúng — trúng chỗ ta không định bắn.\n\n"
        "Hàn Lập không đổi mặt. Hắn chỉ gật đầu, một lần.\n\n"
        "“Vậy thì từ đây,” — hắn nói — “mỗi người đi đường mình. Và nếu đường ta gặp đường ngươi lần nữa, "
        "ta sẽ nhớ câu này.”\n\n"
        "Hắn quay đi. Không chào. Không ngoái lại.\n\n"
        "Kiếm linh trong vạt áo khẽ nói, giọng khô:\n\n"
        "“Ngươi vừa tự tay cắt một sợi dây. Ta không nói ngươi sai. Nhưng ta nói cho ngươi biết: "
        "sợi dây đó, người ta thường phải mất mạng mới có lại được.”\n\n"
        "Ta đứng ở chân núi rất lâu. Trời sáng hẳn.\n\n"
        "Ta ra khỏi Thái Nam Cốc với hai thanh kiếm, một bài học, và một kẻ thù mà ta biết sẽ không quên ta.",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    # --- kết thù địch ---
    d.append(doan(
        "c2_d27b", "Chân núi phía bắc — gần sáng",
        "Ta ra khỏi thung lũng bằng con đường mòn phía bắc, một mình.\n\n"
        "Trong vạt áo ta không có lệnh bài. Trong tay ta chỉ có hai thanh kiếm và một thứ kiếm linh vừa dạy.\n\n"
        "Phía sau, Thái Nam Cốc cháy tới sáng.\n\n"
        "Ta không biết Hàn Lập có ra được không. Ta không hỏi. Ta cũng không quay lại.\n\n"
        "“Ngươi có hối không?” — kiếm linh hỏi.\n\n"
        "“Không.”\n\n"
        "“Ngươi nói dối.” — Giọng nó khô, nhưng không lạnh. — “Nhưng nói dối cũng là một cách sống. "
        "Nhớ lấy cái giá của nó.”\n\n"
        "Ta đi về phía bắc. Trời sáng dần. Và trong lòng ta có một chỗ trống mà ta biết sẽ không lấp được "
        "bằng tu vi hay linh thạch.",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    return d


def ket():
    return {
        "boi_canh": "Chương 2 — hết (tán tu)",
        "ke": "Thái Nam Cốc khép lại. Thung lũng trống, lều đã dỡ, đèn lồng tắt hết.\n\n"
              "Ta ra khỏi cốc với hai thanh kiếm và một bài học: ở chốn này, người ta không cho ai vay. "
              "Mỗi thứ đều có giá, và giá luôn trả trước.\n\n"
              "*Chương sau: con đường của kẻ đi giữa hồng trần.*",
    }
