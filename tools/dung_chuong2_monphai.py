"""Dựng nhánh MÔN PHÁI của Chương 2 — đi riêng, không gặp nhánh tán tu.

Bạn đồng hành: Tuyết Cơ, hảo cảm 100 từ đầu chương.
Hai hướng với Hàn Lập: hảo cảm đủ thì thành bạn, hảo cảm thấp thì thành kẻ thù.
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


def dung():
    d = []

    d.append(doan(
        "c2_p07", "Thái Nam Sơn Cốc — mép thung lũng",
        "Ta đứng ở mép thung lũng, và lần đầu tiên trong đời, ta thấy người ta bay.\n\n"
        "Không phải nhảy cao. Không phải đu dây. Bay. Một người áo trắng đứng trên một thanh kiếm mảnh, "
        "lơ lửng cách mặt đất chừng ba trượng, rồi hạ xuống nhẹ như lá rụng.\n\n"
        "Trong vạt áo ta, khối ngọc cốt nóng ran.\n\n"
        "“Đứng yên,” — Tuyết Cơ nói, giọng căng như dây đàn. — “Đừng để linh khí trong người ngươi động. "
        "Kẻ kia là Trúc Cơ. Hắn cảm được ngươi từ trên cao.”\n\n"
        "“Trúc Cơ?”\n\n"
        "“Trên Luyện Khí một bậc. Một bậc thôi, nhưng khoảng cách giữa hai bậc ấy là khoảng cách giữa người biết bơi "
        "và người biết đi trên nước.” — Nàng ngừng. — “Ta từng ở bậc đó. Rất lâu rồi.”\n\n"
        "Ta nín thở. Người áo trắng đứng trên kiếm nhìn về phía thung lũng, không nhìn xuống ta.\n\n"
        "Rồi hắn bay đi.\n\n"
        "“Xuống dưới kia,” — Tuyết Cơ nói, giọng đã dịu lại. — “Đây là lần đầu ngươi được thấy giới tu hành thật. "
        "Nhìn cho kỹ, nhưng đừng tỏ ra ngươi hiểu gì. Người hiểu nhiều ở đây thường chết sớm.”\n\n"
        "Phía dưới, thung lũng trải ra như một cái chợ khổng lồ: hàng trăm lều trại dựng san sát, "
        "đèn lồng treo thành dãy, và ở giữa là một khoảng trống lớn nơi người ta bày hàng trên những tấm vải trải đất.",
        [chon("Xuống chợ", "c2_p08")],
        hoi="Mở"))

    d.append(doan(
        "c2_p08", "Chợ trong thung lũng — chiều",
        "Cái chợ này không giống bất kỳ cái chợ nào ta từng biết.\n\n"
        "Không ai rao. Không ai mặc cả to tiếng. Người ta ngồi sau tấm vải, hàng hoá bày trước mặt, "
        "và khi có khách thì nói rất khẽ.\n\n"
        "“Đừng nhìn hàng,” — Tuyết Cơ nói. — “Nhìn tay người bán.”\n\n"
        "“Vì sao?”\n\n"
        "“Vì hàng thì ai cũng bày được. Tay mới nói thật.” — Nàng chậm lại. — “Kẻ bán đan dược thật thì ngón tay "
        "có vết chai ở đầu ngón giữa, vì phải nghiền thuốc. Kẻ bán pháp khí thật thì tay áo bên phải sờn hơn bên trái, "
        "vì phải lau khí mỗi ngày. Kẻ không có gì trong tay thì nói to nhất.”\n\n"
        "Ta nhìn lại cái chợ bằng con mắt khác.\n\n"
        "Và ta thấy nàng nói đúng. Người đàn bà bán đan ở dãy thứ hai có vết chai ở ngón giữa. "
        "Gã bán pháp khí ở dãy thứ tư có tay áo phải sờn. Còn gã đứng giữa chợ, nói to nhất, "
        "tay áo phẳng lì, thì trước mặt chỉ có một tấm vải trống.\n\n"
        "“Nàng dạy ta những thứ này từ bao giờ?” — ta hỏi khẽ.\n\n"
        "“Từ lúc ngươi ký khế ước.” — Giọng nàng có gì đó gần như cười. — “Ta là tớ của ngươi. "
        "Tớ không được để chủ chết ở một cái chợ.”",
        [chon("Hỏi nàng về linh thạch", "c2_p09"),
         chon("Đi thẳng vào dãy hàng phía đông", "c2_p10")]))

    d.append(doan(
        "c2_p09", "Chợ trong thung lũng — chiều",
        "“Linh thạch là gì?”\n\n"
        "“Là máu của đất.” — Nàng nói ngay, không cần nghĩ. — “Linh khí tụ lại trong đá, nén lại qua trăm năm, "
        "thành thứ cầm được. Người tu hành không ăn cơm, họ ăn cái này. Hoặc họ dùng nó để mua thứ khác ăn được.”\n\n"
        "“Bốn phẩm?”\n\n"
        "Nàng im một nhịp, như đang cân nhắc nên nói bao nhiêu.\n\n"
        "“Bốn. Hạ, trung, thượng, cực phẩm. Một viên trung phẩm bằng mười hạ phẩm. Một viên thượng phẩm bằng mười trung. "
        "Cực phẩm thì không ai đổi — người có nó không cần đổi.” — Nàng ngừng. — “Và ngươi đang nghèo.”\n\n"
        "“Ta biết.”\n\n"
        "“Ngươi chưa biết.” — Giọng nàng nghiêm lại. — “Ngươi có một khối ngọc cốt trong ngực. Khối ấy, "
        "nếu ai biết, đáng giá hơn cả cái chợ này. Đó là lý do ngươi phải học giá trước khi học võ. "
        "Kẻ không biết giá sẽ bán mình mà tưởng mình đang mua.”",
        [chon("Ghi nhớ từng lời", "c2_p10", {"tu_vi": 10}),
         chon("Hỏi thêm về khối ngọc", "c2_p09b")]))

    d.append(doan(
        "c2_p09b", "Chợ trong thung lũng — chiều",
        "“Khối ngọc này là gì?” — ta hỏi. — “Nàng chưa từng nói hết.”\n\n"
        "Tuyết Cơ im rất lâu. Lâu đến mức ta tưởng nàng đã ngủ.\n\n"
        "“Là chỗ ta bị nhốt.” — Cuối cùng nàng nói, giọng nhẹ như không. — “Và cũng là chỗ ngươi hấp thu linh khí. "
        "Hai chuyện đó là một. Ngươi càng dùng nó, ta càng tỉnh. Ngươi càng mạnh, ta càng gần được ra.”\n\n"
        "“Vậy là ta đang giúp nàng.”\n\n"
        "“Ngươi đang giúp chính ngươi.” — Nàng sửa lại, và giọng nàng lạnh đi một chút. — “Đừng nhầm. "
        "Ta không phải người tốt. Ta bị nhốt ở đây vì có lý do. Khi ta ra được, ngươi sẽ biết lý do đó.”\n\n"
        "“Vậy sao ta phải tin nàng?”\n\n"
        "“Vì ta chưa từng nói dối ngươi.” — Nàng ngừng. — “Và vì ngươi không còn lựa chọn nào khác. "
        "Đó là hai lý do khác nhau. Ngươi tự chọn lấy một.”",
        [chon("Đi vào dãy hàng phía đông", "c2_p10")]))

    d.append(doan(
        "c2_p10", "Dãy hàng phía đông — chạng vạng",
        "Ta thấy Hàn Lập trước khi hắn thấy ta.\n\n"
        "Hắn ngồi sau một tấm vải nhỏ, trước mặt bày mấy thứ: một cuốn sách ố, mấy lọ thuốc, và một mảnh ngọc trắng đục. "
        "Di vật của Mạc Đại Phu.\n\n"
        "Một gã áo gấm đứng trước tấm vải, cầm mảnh ngọc lên, xoay dưới đèn, rồi đặt xuống với vẻ chán chường.\n\n"
        "“Ngọc vụn,” — gã nói. — “Ba viên hạ phẩm, ta lấy cả.”\n\n"
        "Ta biết giá. Tuyết Cơ vừa dạy ta cách nhìn tay người bán — và cách nhìn tay kẻ mua. "
        "Gã áo gấm này có tay áo phẳng, không chai, không sờn. Gã không phải người làm nghề này. "
        "Gã là kẻ đi săn đồ rẻ ở chợ người mới.\n\n"
        "“Đừng xen vào,” — Tuyết Cơ nói, rất khẽ. — “Đây không phải chuyện của ngươi.”\n\n"
        "“Hắn là người ta quen.”\n\n"
        "“Ngươi quen hắn ở đâu?”\n\n"
        "Ta không trả lời. Hàn Lập không nói gì. Hắn chỉ nhìn mảnh ngọc trong tay gã áo gấm, mặt không đổi sắc.",
        [chon("Bước vào, phá ngang", "c2_p11a",
              {"hao_cam": {"Hàn Lập": 12}}),
         chon("Đứng nhìn, để hắn tự quyết", "c2_p11b",
              {"hao_cam": {"Hàn Lập": -6}}),
         chon("Nghe lời Tuyết Cơ, quay đi", "c2_p11c",
              {"hao_cam": {"Hàn Lập": -18}})]))

    d.append(doan(
        "c2_p11a", "Dãy hàng phía đông",
        "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
        "“Mảnh ngọc ấy không phải ngọc thường,” — ta nói. — “Ngươi thử cầm nó dưới nắng xem.”\n\n"
        "Gã áo gấm nhíu mày, nhưng vẫn xoay mảnh ngọc. Ánh chiều xuyên qua, và trong lòng ngọc hiện lên "
        "một sợi chỉ sáng mảnh như tơ.\n\n"
        "Mặt gã đổi hẳn.\n\n"
        "“Ngươi là ai?” — gã hỏi, giọng đã khác.\n\n"
        "“Kẻ vừa nói cho ngươi biết ngươi đang định mua hớ.” — Ta nghiêng đầu. — “Hoặc ngươi trả đúng giá, "
        "hoặc ngươi trả bằng danh dự.”\n\n"
        "Gã áo gấm nhìn ta một lúc, rồi cười — không vui — đặt mảnh ngọc xuống, rút ra một túi nhỏ, "
        "đếm ra mười viên linh thạch, rồi bỏ đi.\n\n"
        "Hàn Lập nhìn túi linh thạch, rồi nhìn ta.\n\n"
        "“Ngươi mặc áo đệ tử Thất Huyền Môn.” — Hắn nói, không phải hỏi. — “Sao ngươi biết giá ở chợ tu hành?”\n\n"
        "“Ta có một người dạy.”\n\n"
        "“Ai?”\n\n"
        "Ta không trả lời. Trong vạt áo, khối ngọc cốt khẽ ấm.\n\n"
        "Hàn Lập nhìn ta lâu hơn mọi lần trước. Rồi hắn gật đầu, rất nhẹ, và không hỏi nữa.",
        [chon("Ngồi xuống cạnh hắn", "c2_p12",
              {"hao_cam": {"Hàn Lập": 6}})]))

    d.append(doan(
        "c2_p11b", "Dãy hàng phía đông",
        "Ta đứng nhìn.\n\n"
        "Gã áo gấm trả ba viên linh thạch. Hàn Lập nhận, không nói một lời, gói mảnh ngọc lại bằng vải cũ "
        "rồi cất vào trong áo — cất rất nhanh, rất kín.\n\n"
        "Gã áo gấm đi. Ta bước tới.\n\n"
        "“Mảnh ngọc ấy đáng giá hơn ba viên.”\n\n"
        "Hàn Lập ngẩng lên. Trong mắt hắn không có gì — không giận, không tiếc, không cả trách ta đã đứng nhìn.\n\n"
        "“Ta biết,” — hắn nói.\n\n"
        "“Vậy sao ngươi bán?”\n\n"
        "“Vì ta cần tiền hôm nay.” — Hắn đứng dậy, phủi vải. — “Ngươi mặc áo Thất Huyền Môn. Ngươi tới đây "
        "bằng đường khác ta. Vậy mà ngươi vẫn tới.”\n\n"
        "Hắn không nói thêm. Nhưng câu đó ở lại với ta lâu hơn ta muốn.",
        [chon("Đi theo hắn", "c2_p12",
              {"hao_cam": {"Hàn Lập": 4}}),
         chon("Đứng lại, để hắn đi", "c2_p12",
              {"hao_cam": {"Hàn Lập": -8}})]))

    d.append(doan(
        "c2_p11c", "Dãy hàng phía đông — chạng vạng",
        "Ta quay đi.\n\n"
        "Tuyết Cơ nói đúng — đây không phải chuyện của ta. Ta tới đây để học, không để xen vào việc của người khác.\n\n"
        "Nhưng khi ta đi được mười bước, ta nghe phía sau có tiếng gã áo gấm cười, và tiếng Hàn Lập nói rất khẽ: "
        "“Được. Ba viên.”\n\n"
        "Ta không quay lại.\n\n"
        "“Ngươi vừa làm đúng,” — Tuyết Cơ nói. — “Và ngươi vừa mất một thứ.”\n\n"
        "“Thứ gì?”\n\n"
        "“Một người.” — Nàng ngừng. — “Nhưng ngươi mới tới đây một ngày. Ngươi không thể cứu tất cả những kẻ "
        "mà ngươi sẽ gặp. Nếu ngươi thử, ngươi sẽ chết trước khi học được cách cứu ai.”",
        [chon("Đi tiếp vào chợ", "c2_p12")]))

    d.append(doan(
        "c2_p12", "Góc chợ — tối",
        "Đèn lồng trong thung lũng thắp lên cùng một lúc, và cái chợ đổi hẳn màu.\n\n"
        "Ta ngồi trên một tảng đá, giữa hai dãy hàng đã bắt đầu dọn. Không xa, Hàn Lập ngồi một mình, "
        "trong tay là cuốn sách ố mua được ở quầy bên kia.\n\n"
        "“Ta đọc được chữ này,” — hắn nói, và giọng hắn có gì đó ta chưa từng nghe — như thể hắn đang tự nói với mình.\n\n"
        "Tuyết Cơ trong vạt áo ta khẽ nói:\n\n"
        "“Trường Xuân Công. Tầng bốn tới tầng sáu. Thứ này ở chợ phàm không có.”\n\n"
        "Ta biết một thứ mà Hàn Lập không biết ta biết.",
        [chon("Nói cho hắn biết sách viết gì", "c2_p13a",
              {"hao_cam": {"Hàn Lập": 15}, "co_su_kien": ["noi_sach_cho_han_lap"]}),
         chon("Giấu, chưa nói", "c2_p13b",
              {"hao_cam": {"Hàn Lập": -10}, "co_su_kien": ["giu_kin_chuyen_sach"]})]))

    d.append(doan(
        "c2_p13a", "Góc chợ — tối",
        "“Trường Xuân Công,” — ta nói. — “Tầng bốn tới tầng sáu.”\n\n"
        "Hàn Lập ngẩng lên rất nhanh. Mắt hắn sắc lại, và lần đầu tiên ta thấy hắn nhìn ta như nhìn một người "
        "chứ không phải một cái bóng.\n\n"
        "“Ngươi đọc được chữ này?”\n\n"
        "“Không phải ta.” — Ta ngừng một nhịp, chọn lời. — “Ta có một thứ giúp ta đọc. Ta chưa thể nói là gì. "
        "Nhưng ta không muốn ngươi bán rẻ thứ này cho gã áo gấm nào nữa.”\n\n"
        "Hắn im lâu. Rồi hắn gật đầu, chậm.\n\n"
        "“Vậy thì ta nợ ngươi một lần.”\n\n"
        "“Ngươi nợ ta hai lần.” — Ta cười. — “Lần trước là mảnh ngọc.”\n\n"
        "“Ta nhớ.” — Hắn cất sách vào áo. — “Ta nhớ hết.”\n\n"
        "*Hắn nhớ hết.* Ta tin câu đó. Ta không biết vì sao, nhưng ta tin.",
        [chon("Hỏi hắn về Mạc Đại Phu", "c2_p14",
              {"hao_cam": {"Hàn Lập": 8}}),
         chon("Không hỏi gì, ngồi im", "c2_p14")]))

    d.append(doan(
        "c2_p13b", "Góc chợ — tối",
        "Ta im.\n\n"
        "Hàn Lập đọc thêm mấy dòng, rồi gấp sách lại. Hắn không hỏi ta có đọc được không. Hắn không hỏi gì cả.\n\n"
        "Nhưng khi hắn đứng dậy, hắn nói một câu, không quay đầu:\n\n"
        "“Ngươi im lâu quá.”\n\n"
        "“Sao?”\n\n"
        "“Không sao.” — Hắn bước đi. — “Chỉ là ta để ý.”\n\n"
        "Tuyết Cơ trong vạt áo khẽ nói, giọng khô:\n\n"
        "“Ngươi vừa giữ được một bí mật nhỏ và mất một thứ lớn hơn. Cân đi. Nhưng đừng cân lâu quá — "
        "ở cái chợ này, người ta không cho ngươi cân lại lần hai.”",
        [chon("Đi theo hắn", "c2_p14",
              {"hao_cam": {"Hàn Lập": -4}})]))

    d.append(doan(
        "c2_p14", "Rìa thung lũng — đêm",
        "Đêm ấy ta ngủ ngoài trời, dưới một gờ đá.\n\n"
        "Thung lũng ban đêm khác hẳn ban ngày. Đèn lồng tắt dần, và những vệt linh khí trở nên rõ hơn — "
        "chúng bay chậm, như đom đóm mệt.\n\n"
        "“Ngồi dậy,” — Tuyết Cơ nói. — “Ta dạy ngươi thứ đầu tiên.”\n\n"
        "Ta ngồi. Khối ngọc cốt trong ngực ấm ran.\n\n"
        "“Người khác phải mất ba năm mới cảm nhận được linh khí. Ngươi có ngọc cốt — linh khí sẽ tự tìm tới ngươi. "
        "Nhưng đó là lý do ngươi phải cẩn thận hơn người khác, không phải ít hơn.”\n\n"
        "“Vì sao?”\n\n"
        "“Vì ở đây có kẻ cảm được linh khí của người khác.” — Giọng nàng nghiêm lại. — “Nếu ngươi hấp thu quá nhanh, "
        "ngươi sẽ sáng như đèn trong đêm. Và kẻ mạnh nhất trong cái cốc này sẽ tới hỏi ngươi đang giấu gì.”\n\n"
        "Nàng ngừng.\n\n"
        "“Cho nên đêm nay ngươi không học cách hấp thu. Ngươi học cách giấu.”",
        [chon("Học cách nén khí tức", "c2_p15",
              {"tu_vi": 25, "co_su_kien": ["hoc_nen_khi_tuc"]}),
         chon("Học cách hấp thu nhanh", "c2_p15",
              {"tu_vi": 45, "co_su_kien": ["hoc_hap_thu_nhanh"]})]))

    d.append(doan(
        "c2_p15", "Giữa thung lũng — sáng sớm",
        "Sáng hôm sau, giữa thung lũng có một đám đông tụ lại.\n\n"
        "Ta tới gần. Ở giữa đám đông là một cái bục đá thấp, và trên bục là một ông lão mặc áo xám dài, "
        "tóc bạc buộc gọn, tay chống một cây gậy gỗ trơn nhẵn.\n\n"
        "“Linh thạch hạ phẩm đổi một câu hỏi,” — ông nói, giọng không to nhưng ai cũng nghe. — "
        "“Trung phẩm đổi một lần chỉ. Thượng phẩm thì ta không dám nhận.”\n\n"
        "“Vạn Tiểu Sơn,” — Tuyết Cơ nói. — “Tán tu. Luyện Khí tầng tám. Lão kiêu ngạo tới mức cả cái cốc này "
        "phải nể, vì lão là người duy nhất ở đây dám nói thẳng giá của từng thứ.”\n\n"
        "“Lão nói thật?”\n\n"
        "“Lão nói giá. Giá và thật là hai chuyện khác nhau. Nhưng ở đây, biết giá đã là sống.”",
        [chon("Bước lên, đặt một viên linh thạch", "c2_p16"),
         chon("Đứng ngoài nghe", "c2_p16b")]))

    d.append(doan(
        "c2_p16", "Bục đá — sáng",
        "Ta đặt viên linh thạch cuối cùng của mình xuống.\n\n"
        "Vạn Tiểu Sơn nhìn viên thạch, rồi nhìn ta — nhìn rất lâu, từ đầu tới chân, không vội. "
        "Rồi lão nhìn xuống vạt áo ta, chỗ khối ngọc cốt.\n\n"
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
        [chon("Hỏi: kẻ nào đang giữ?", "c2_p17",
              {"co_su_kien": ["biet_ba_tam_lenh"]}),
         chon("Cúi đầu, rời đi", "c2_p17")]))

    d.append(doan(
        "c2_p16b", "Rìa đám đông — sáng",
        "Ta đứng ngoài nghe, và học được nhiều hơn một viên linh thạch đáng giá.\n\n"
        "Vạn Tiểu Sơn trả lời mười bảy câu hỏi trong buổi sáng ấy. Ta nhớ cả mười bảy.\n\n"
        "Linh thạch có bốn phẩm. Pháp khí chia theo cấp. Đan dược hỗ trợ tu luyện thì chia theo công dụng, "
        "không chia theo giá. Và thứ đắt nhất ở cái chợ này không phải pháp khí — mà là tin tức.\n\n"
        "“Ngươi nghe giỏi hơn ngươi nói,” — Tuyết Cơ nhận xét. — “Đó là một đức tính. Đừng bỏ.”",
        [chon("Đi tìm Hàn Lập", "c2_p17")]))

    d.append(doan(
        "c2_p17", "Dãy hàng phía bắc — trưa",
        "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
        "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân nhỏ. "
        "Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
        "“Ba viên,” — bà ta nói. — “Không hơn.”\n\n"
        "“Năm.” — Hàn Lập không nhấc mắt. — “Thuốc này ta tự tay pha. Bà biết nó đáng bao nhiêu.”\n\n"
        "“Ta biết ngươi đang cần tiền.” — Bà ta cười. — “Đó là lý do ngươi chỉ được ba.”\n\n"
        "Hàn Lập im. Ta thấy vai hắn hơi siết.\n\n"
        "“Vì sao ngươi đi theo ta?” — hắn hỏi bất ngờ, không quay lại.\n\n"
        "Câu hỏi ấy không dành cho bà bán đan.",
        [chon("“Vì ta cũng cần một người hiểu ta.”", "c2_p18",
              {"hao_cam": {"Hàn Lập": 10}}),
         chon("“Vì ta ghét bị trả giá.”", "c2_p18",
              {"hao_cam": {"Hàn Lập": 6}}),
         chon("Đứng nhìn, để hắn tự trả giá", "c2_p18",
              {"hao_cam": {"Hàn Lập": -10}}),
         chon("“Vì ngươi có thứ ta cần.”", "c2_p18",
              {"hao_cam": {"Hàn Lập": -15}})]))

    d.append(doan(
        "c2_p18", "Rìa thung lũng — chiều ngày thứ ba",
        "Ba ngày trôi qua.\n\n"
        "Ta học được nhiều thứ đến mức đầu ta đau. Rằng linh thạch có bốn phẩm. Rằng pháp khí chia theo cấp. "
        "Rằng có những kẻ ở đây đã tu hành cả trăm năm mà trông vẫn như thanh niên hai mươi.\n\n"
        "Và ta học được một thứ nữa, không ai dạy: rằng Hàn Lập không bao giờ hỏi thẳng một câu hai lần. "
        "Nếu hắn đã hỏi, hắn đã ghi câu trả lời vào đâu đó trong đầu.\n\n"
        "“Đêm nay ngươi ngủ đâu?” — hắn hỏi.\n\n"
        "“Ngoài gờ đá.”\n\n"
        "“Có người để ý ngươi rồi.” — Hắn nói, giọng đều. — “Ba kẻ. Áo xám, không có pháp khí, "
        "nhưng đi theo ngươi từ dãy đông tới giờ.”\n\n"
        "Ta không quay lại. Tuyết Cơ trong vạt áo khẽ nói: “Hắn nói đúng. Ta thấy chúng từ trưa.”\n\n"
        "“Vậy làm gì?” — ta hỏi.\n\n"
        "Hàn Lập nhìn ta. Lần này hắn nhìn lâu hơn mọi lần trước.",
        [chon("“Đêm nay ta ngủ chỗ ngươi.”", "c2_p19",
              {"hao_cam": {"Hàn Lập": 8}, "co_su_kien": ["ngu_cung_han_lap"]}),
         chon("“Ta tự lo được.”", "c2_p19b",
              {"hao_cam": {"Hàn Lập": -12}, "co_su_kien": ["tu_lo_mot_minh"]})]))

    d.append(doan(
        "c2_p19", "Khe đá — đêm",
        "Khe đá đủ cho hai người, không hơn.\n\n"
        "Chúng ta ép sát vào vách. Bên ngoài, cách chỗ ta chừng mười bước, có tiếng chân người chạy qua — "
        "rồi tiếng một vật nặng đổ, rồi im.\n\n"
        "Hàn Lập đặt tay lên vai ta. Hắn không nói. Nhưng bàn tay ấy nặng và ấm, và nó ở đó suốt một canh giờ.\n\n"
        "Khi tiếng chân đã xa hẳn, hắn mới rút tay về.\n\n"
        "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta mấy ngày.”\n\n"
        "Hắn im lâu đến mức ta tưởng hắn không trả lời.",
        [chon("“Vậy thì cùng nhau ra khỏi đây.”", "c2_p20"),
         chon("“Ta không cần ngươi hiểu ta.”", "c2_p20"),
         chon("“Ta sẽ không để ngươi chết một mình.”", "c2_p20")]))

    d.append(doan(
        "c2_p20", "Khe đá — gần sáng",
        "“Vì ngươi không giống những kẻ khác ở đây.” — Cuối cùng hắn nói. — “Những kẻ khác tới cái chợ này "
        "để lấy thứ gì đó. Ngươi tới để hiểu. Ta thấy được điều đó từ hôm đầu, khi ngươi đứng chắn trước tấm vải của ta.”\n\n"
        "“Ta tưởng ngươi không để ý.”\n\n"
        "“Ta để ý mọi thứ.” — Hắn nói, giọng đều. — “Đó là cách ta sống được tới giờ.”\n\n"
        "Bên ngoài, trời bắt đầu xám. Khối ngọc cốt trong ngực ta khẽ ấm, và Tuyết Cơ nói, chỉ cho ta nghe:\n\n"
        "“Ngươi vừa có một thứ mà ta không dạy được. Giữ nó.”\n\n"
        "“Thứ gì?”\n\n"
        "“Một người.” — Nàng ngừng. — “Ta đã sống ngàn năm và ta chưa từng thấy ai giữ được thứ đó lâu. "
        "Nhưng ngươi thử đi.”\n\n"
        "Trời sáng. Ngày cuối của hội bắt đầu.",
        [chon("Ra khỏi khe đá", "c2_p21b",
              {"hao_cam": {"Hàn Lập": 5}})]))

    d.append(doan(
        "c2_p19b", "Gờ đá — đêm",
        "“Ta tự lo được,” — ta nói.\n\n"
        "Hàn Lập nhìn ta một lúc. Rồi hắn gật đầu, rất nhẹ, và quay đi.\n\n"
        "“Vậy thì tự lo.”\n\n"
        "Đêm ấy ta ngồi một mình dưới gờ đá, khối ngọc cốt trong ngực ấm ran. Ba kẻ áo xám tới lúc gần sáng.\n\n"
        "Ta không gọi ai. Tuyết Cơ nói một câu duy nhất trước khi chúng tới:\n\n"
        "“Đánh thì đánh, nhưng đừng đánh như kẻ muốn thắng. Đánh như kẻ muốn sống. "
        "Và nhớ: ngươi mới tầng hai. Ngươi không thắng được ba kẻ tầng bốn. Ngươi chỉ cần chạy nhanh hơn chúng.”\n\n"
        "Ta sống. Nhưng khi trời sáng, chỗ Hàn Lập nghỉ đã trống. Hắn đi lúc nào ta không biết. "
        "Hắn không để lại gì — không một lời, không một dấu.\n\n"
        "*Hắn không đợi ta.*",
        [chon("Đi tìm hắn", "c2_p20b"),
         chon("Không tìm. Đi đường của mình.", "c2_p20c")]))

    d.append(doan(
        "c2_p20b", "Thung lũng — sáng ngày thứ tư",
        "Ta tìm hắn suốt buổi sáng. Ta tìm thấy hắn ở dãy hàng phía bắc, và ta thấy hắn trước khi hắn thấy ta.\n\n"
        "Hắn đang nói chuyện với một kẻ áo xám. Không phải ba kẻ đêm qua. Kẻ này khác — áo xám nhưng có thêu chỉ bạc ở cổ tay, "
        "và đứng thẳng như người có chức phận.\n\n"
        "Hàn Lập đưa cho hắn một thứ. Ta không thấy rõ. Nhưng kẻ áo xám nhận, gật đầu, rồi đi về phía đông.\n\n"
        "Tuyết Cơ nói, rất khẽ: “Ngươi vừa thấy một cuộc giao dịch. Đừng hỏi hắn về nó. Hỏi là mất.”\n\n"
        "Ta đứng lại. Ta không bước tới.",
        [chon("Bỏ đi, không hỏi", "c2_p21b",
              {"co_su_kien": ["thay_han_lap_giao_dich"]}),
         chon("Bước tới, hỏi thẳng", "c2_p21b",
              {"hao_cam": {"Hàn Lập": -10}, "co_su_kien": ["hoi_thang_han_lap"]})]))

    d.append(doan(
        "c2_p20c", "Rìa thung lũng — chiều ngày thứ tư",
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
        "“Và là thứ mà cả cái cốc này sẽ giết để có.”\n\n"
        "Tuyết Cơ trong vạt áo nói, rất khẽ: “Nàng ta nói đúng. Và ta sẽ nói thêm một điều nàng ta không dám nói: "
        "ngươi không cần Thăng Tiên Lệnh. Ngươi có thứ quý hơn.”",
        [chon("Cúi đầu cảm ơn, đi", "c2_p21b",
              {"co_su_kien": ["biet_thien_linh_can"]})]))

    d.append(doan(
        "c2_p21b", "Giữa thung lũng — sáng ngày cuối",
        "Sáng ngày cuối, cái chợ đổi tính.\n\n"
        "Người ta dọn hàng nhanh hơn. Những tấm vải cuốn lại, lều hạ xuống, và ai cũng đi thành nhóm ba bốn người, "
        "không đi một mình.\n\n"
        "“Sao vậy?” — ta hỏi gã bán bánh khô.\n\n"
        "“Tà tu,” — gã nói, không ngẩng lên. — “Chúng phong toả cốc từ đêm qua. Không cho ai ra. "
        "Bắt người làm lô đỉnh. Ngươi muốn sống thì tìm chỗ nấp, đừng tìm đường ra.”\n\n"
        "Khối ngọc cốt trong ngực ta khẽ rung.\n\n"
        "“Đây là lúc ta nói thật với ngươi,” — Tuyết Cơ nói, giọng lạnh hơn mọi khi. — “Ngươi mới Luyện Khí tầng hai. "
        "Một tên tà tu thấp nhất ở đây cũng tầng năm. Ngươi không thắng được. Ngươi chỉ có thể chọn cách sống sót.”\n\n"
        "“Còn nàng?”\n\n"
        "“Ta đang ngủ dở.” — Nàng ngừng. — “Ta chỉ tỉnh được nửa canh giờ nữa. Sau đó ngọc cốt sẽ tối. "
        "Ngươi phải chọn trước khi ta ngủ lại.”\n\n"
        "Phía đông, khói bắt đầu bốc lên.",
        [chon("Đi tìm Hàn Lập", "c2_p22",
              {"co_su_kien": ["di_tim_han_lap"]}),
         chon("Tự tìm chỗ nấp", "c2_p22b")]))

    d.append(doan(
        "c2_p22", "Khe đá — chạng vạng",
        "Ta tìm thấy Hàn Lập trước khi chúng tìm thấy.\n\n"
        "Hắn ngồi trong khe đá, cái hòm gỗ dựng bên cạnh, và trước mặt hắn là một cái bình nhỏ màu xanh — "
        "cao chừng hai đốt ngón tay, men đã sứt một miếng.\n\n"
        "“Cái này,” — hắn nói, đặt nó xuống tảng đá — “ta nhặt được ở Thất Huyền Môn. Trong đám đổ nát, sau trận.”\n\n"
        "“Là gì?”\n\n"
        "“Ta không biết.” — Hắn xoay cái bình. — “Ta đã thử đựng nước. Nước không đổi. Ta đã thử chôn nó. "
        "Nó lại nằm trên mặt đất sáng hôm sau. Ta đã thử bỏ nó. Nó quay lại trong túi ta.”\n\n"
        "Tuyết Cơ trong ngực ta bỗng nói, giọng đổi hẳn — không lạnh, mà như có gì bị nén lại:\n\n"
        "“Cất nó đi. Đừng cho ai thấy. Đừng nói với ai — kể cả ta, sau này.”\n\n"
        "“Nó là gì?” — ta hỏi khẽ.\n\n"
        "“Là thứ mà nếu người ta biết hắn có, thì cái cốc này sẽ không còn đủ chỗ cho xác hắn.” — "
        "Nàng ngừng. — “Ta không đọc được hết. Nhưng ta biết một điều: nó không thuộc về hắn. Nó đang chờ một người.”\n\n"
        "Hàn Lập nhìn ta. Hắn không biết ta vừa nghe gì.",
        [chon("“Giấu nó đi. Đừng cho ai thấy.”", "c2_p23",
              {"hao_cam": {"Hàn Lập": 15}, "co_su_kien": ["khuyen_giau_binh", "thay_chuong_thien_binh"]}),
         chon("“Ta không đọc được vật.”", "c2_p23",
              {"hao_cam": {"Hàn Lập": -5}}),
         chon("“Đưa nó cho ta giữ.”", "c2_p23",
              {"hao_cam": {"Hàn Lập": -20}})]))

    d.append(doan(
        "c2_p22b", "Hốc đá phía tây — chạng vạng",
        "Ta tự tìm chỗ nấp.\n\n"
        "Hốc đá phía tây hẹp, tối, và có một khe hở nhìn ra thung lũng. Ta nằm im, khối ngọc cốt tối dần trên ngực.\n\n"
        "“Ta ngủ đây,” — Tuyết Cơ nói, giọng đã yếu. — “Nửa canh giờ nữa ngọc cốt sẽ tối hẳn. Từ đó tới sáng, "
        "ngươi chỉ có chính mình.”\n\n"
        "“Nàng ngủ đi.”\n\n"
        "“Ngươi không sợ?”\n\n"
        "“Sợ.” — Ta nói thật. — “Nhưng nàng đã dạy ta cách giấu khí tức. Ta sẽ dùng nó.”\n\n"
        "Nàng im một lúc. Rồi nàng nói câu cuối, rất khẽ:\n\n"
        "“Ngươi khác ta hồi đó. Ta hồi đó sẽ không nói thật là mình sợ.”\n\n"
        "Rồi khối ngọc tối hẳn.\n\n"
        "Bên ngoài, tiếng đánh nhau tới gần rồi xa. Có tiếng ai đó hét lên một tiếng, rồi im hẳn. "
        "Rồi ta nghe một giọng người trẻ, lạnh, nói rất nhanh: “Lệnh bài đâu?” — và một giọng khác, khàn hơn, đáp: "
        "“Ngươi… ngươi là ai…” Rồi im.\n\n"
        "Ta nằm im rất lâu. Đến khi trời tối hẳn, ta mới bò ra.",
        [chon("Bò ra, đi về phía bắc", "c2_p24b")]))

    d.append(doan(
        "c2_p23", "Khe đá — đêm ngày cuối",
        "Hàn Lập cất cái bình vào áo, rất chậm, rồi gật đầu.\n\n"
        "“Vậy thì ta giữ.”\n\n"
        "Bên ngoài, khói đã dày đặc. Tiếng chân người chạy qua khe đá, rồi tiếng một vật nặng đổ.\n\n"
        "“Ra ngoài xem,” — Hàn Lập nói, đứng dậy.\n\n"
        "Ta theo hắn ra.\n\n"
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
        [chon("“Ngươi vừa giết người.”", "c2_p24",
              {"hao_cam": {"Hàn Lập": 5}}),
         chon("Đứng nhìn, không nói gì", "c2_p24"),
         chon("“Vậy thì ta đi cùng ngươi.”", "c2_p24",
              {"hao_cam": {"Hàn Lập": 12}}),
         chon("“Ngươi là kẻ giết người.”", "c2_p24",
              {"hao_cam": {"Hàn Lập": -20}})]))

    d.append(doan(
        "c2_p24", "Rìa thung lũng — đêm ngày cuối",
        "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
        "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở rìa, chỗ những lều bị đốt. "
        "Đủ để thấy đường mà đi.\n\n"
        "Hàn Lập dừng lại ở miệng một khe núi, quay đầu nhìn lần cuối.\n\n"
        "“Ba tấm lệnh,” — hắn nói. — “Ta có ba tấm. Cả cái cốc này có ba tấm.”\n\n"
        "“Vậy ngươi sẽ đi đâu?”\n\n"
        "“Hoàng Phong Cốc.” — Hắn nói, không do dự. — “Một trong Thất Đại Môn Phái. Ở đó có người dạy ta cách dùng thứ này.”\n\n"
        "Hắn nhìn ta. Rồi hắn rút ra một tấm lệnh, đưa về phía ta.\n\n"
        "“Cầm.”\n\n"
        "“Ta không cần.” — Ta nói, và ta thấy mặt hắn đổi.\n\n"
        "“Không cần?”\n\n"
        "“Ta có thứ khác.” — Ta đặt tay lên ngực, chỗ khối ngọc cốt. — “Ta có thiên linh căn. Ta không cần lệnh bài "
        "để được nhận. Ta chỉ cần tới đúng cửa.”\n\n"
        "Hàn Lập nhìn ta rất lâu.\n\n"
        "“Thiên linh căn.” — Hắn lặp lại, và trong giọng hắn có gì đó ta không đọc được. — “Vậy thì ngươi là thứ "
        "mà cả cái cốc này giết nhau để có.”\n\n"
        "“Ta biết.”\n\n"
        "“Và ngươi vẫn nói cho ta biết.”\n\n"
        "“Vì ngươi đã nói cho ta biết ngươi có Trường Xuân Công.” — Ta nhún vai. — “Ta nợ ngươi một lần. Giờ trả xong.”",
        [chon("“Vậy thì đừng chết.”", "c2_p25",
              {"hao_cam": {"Hàn Lập": 20}},
              {"hao_cam": {"Hàn Lập": 50}}),
         chon("“Đi đi. Đừng quay lại.”", "c2_p25x",
              {"hao_cam": {"Hàn Lập": -15}},
              {"hao_cam_max": {"Hàn Lập": 49}})]))

    d.append(doan(
        "c2_p25", "Chân núi — gần sáng",
        "Trời sáng khi chúng ta ra tới chân núi.\n\n"
        "Thái Nam Cốc ở phía sau, im. Không còn tiếng, không còn lửa, không còn ai. "
        "Một cái chợ của mấy trăm người, và trong một đêm nó thành một cái thung lũng trống.\n\n"
        "Hàn Lập đứng bên ta, nhìn về phía nam.\n\n"
        "“Ta đi Hoàng Phong Cốc,” — hắn nói. — “Ngươi đi đâu?”\n\n"
        "Ta nhìn khối ngọc cốt trong tay. Nó tối — Tuyết Cơ vẫn đang ngủ. Nhưng ta biết nàng sẽ tỉnh.\n\n"
        "“Ta đi tìm một tông môn,” — ta nói. — “Không phải để được nhận. Để xem họ có dám nhận không.”\n\n"
        "Hàn Lập gật đầu. Hắn không giận.\n\n"
        "“Vậy thì đừng chết.”\n\n"
        "“Ngươi cũng vậy.”\n\n"
        "Chúng ta chia tay ở chân núi, mỗi người một hướng. Ta không biết có gặp lại không.\n\n"
        "Nhưng ta biết một điều: hắn sẽ là người quan trọng nhất trong đời ta. Tuyết Cơ đã nói thế từ đêm đầu. "
        "Và nàng chưa bao giờ nói sai.\n\n"
        "Khi mặt trời lên khỏi núi, khối ngọc trong tay ta khẽ ấm.\n\n"
        "“Tỉnh rồi,” — giọng nàng yếu, nhưng có ý cười. — “Ngươi vẫn còn sống.”\n\n"
        "“Vẫn còn.”\n\n"
        "“Tốt.” — Nàng ngừng. — “Vậy thì đi tiếp.”",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    # --- kết thù địch (môn phái) ---
    d.append(doan(
        "c2_p25x", "Chân núi — gần sáng",
        "“Đi đi,” — ta nói. — “Đừng quay lại.”\n\n"
        "Hàn Lập đứng im. Trong tay hắn vẫn là tấm lệnh chưa kịp đưa.\n\n"
        "“Vì sao?”\n\n"
        "“Vì ngươi là thứ ta không muốn trở thành.” — Ta nói, và ta nghe giọng mình lạnh hơn ta tưởng. — "
        "“Ngươi giết người rồi lấy túi của họ. Ngươi gọi đó là sống. Ta gọi đó là chết dần.”\n\n"
        "Hàn Lập cất tấm lệnh vào áo. Rất chậm.\n\n"
        "“Ngươi có thiên linh căn,” — hắn nói. — “Ngươi sẽ vào được cửa. Rồi ngươi sẽ học được rằng "
        "cái cửa đó không mở cho người sạch.”\n\n"
        "“Vậy thì ta sẽ đứng ngoài.”\n\n"
        "“Ngươi sẽ đổi ý.” — Hắn quay đi. — “Và lúc đó, đừng tìm ta.”\n\n"
        "Hắn đi về phía nam. Ta đứng lại.\n\n"
        "Khối ngọc cốt trong ngực ta khẽ ấm. Tuyết Cơ nói, giọng yếu nhưng rõ:\n\n"
        "“Ta không nói ngươi sai. Nhưng ta nói cho ngươi biết: ta đã thấy ngàn năm người ta tự tay đốt "
        "những cây cầu họ sẽ cần. Ngươi vừa làm thế.”\n\n"
        "“Ta biết.”\n\n"
        "“Ngươi có hối không?”\n\n"
        "Ta nghĩ rất lâu.\n\n"
        "“Không.”\n\n"
        "“Vậy thì giữ câu đó.” — Nàng ngừng. — “Ngươi sẽ cần nó.”",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    # --- kết thù địch ---
    d.append(doan(
        "c2_p24b", "Chân núi phía bắc — gần sáng",
        "Ta ra khỏi thung lũng bằng con đường mòn phía bắc, một mình.\n\n"
        "Khối ngọc cốt trong ngực đã tối từ đêm qua. Tuyết Cơ vẫn ngủ.\n\n"
        "Phía sau, Thái Nam Cốc cháy tới sáng.\n\n"
        "Ta không biết Hàn Lập có ra được không. Ta không hỏi. Ta cũng không quay lại.\n\n"
        "Khi trời sáng hẳn, khối ngọc khẽ ấm. Giọng nàng yếu ớt:\n\n"
        "“Ngươi ra được.”\n\n"
        "“Ừ.”\n\n"
        "“Còn kẻ kia?”\n\n"
        "“Ta không biết.”\n\n"
        "Nàng im rất lâu. Rồi nàng nói, và lần này giọng nàng không lạnh:\n\n"
        "“Ta đã sống ngàn năm và ta học được một điều: người ta không tiếc thứ mình bỏ đi. "
        "Họ chỉ tiếc thứ họ bỏ đi mà không biết mình đã bỏ.”\n\n"
        "Ta đi về phía bắc. Trời sáng dần. Và trong lòng ta có một chỗ trống mà ta biết sẽ không lấp được "
        "bằng tu vi hay linh thạch.",
        [chon("Khép lại Chương 2", "__ket_thuc__")]))

    return d


def ket():
    return {
        "boi_canh": "Chương 2 — hết (môn phái)",
        "ke": "Thái Nam Cốc khép lại. Thung lũng trống, lều đã dỡ, đèn lồng tắt hết.\n\n"
              "Ta ra khỏi cốc với một khối ngọc trong ngực, một sợi linh căn không ai được biết, "
              "và một cái tên phải nhớ: Hàn Lập.\n\n"
              "*Chương sau: kẻ mang thiên linh căn đi tìm cửa.*",
    }
