# Chương 1 — Đại chiến Dã Lang Bang

> **Tóm tắt:** Người chơi xuyên không tới Thất Huyền trấn ngay trước khi Dã Lang Bang tập kích Thất Huyền Môn. Trong hỗn loạn, lần đầu chạm mặt Hàn Lập — khi đó còn là một tạp dịch đệ tử gầy gò, ít nói.

*Tổng 23 đoạn.*

---

## Hồi Mở

### Đoạn `c1_d01` — Chợ sớm Thất Huyền trấn

*Ảnh:* `chợ, thị trấn, buổi sáng`

Ngươi mở mắt giữa buổi chợ sớm của thị trấn Thất Huyền. Mùi thuốc bắc, tiếng người mặc cả, và đâu đó tiếng ngựa hí vang.

Ngươi chưa hiểu vì sao mình ở đây. Chỉ biết trên tay có một mảnh ngọc vụn còn ấm, và trong đầu vang lên một giọng nói lạnh lùng: “Nghịch chuyển càn khôn… đã bắt đầu.”

Phía xa, một thanh niên gầy gò, áo vải thô, lặng lẽ quan sát gánh hàng thuốc. Ánh mắt y sắc như dao — không giống kẻ tầm thường.

**Lựa chọn:**

- Lặng lẽ bám theo thanh niên áo vải  
  → `c1_d02`  
  ✦ mở cờ: nghi_ngo_han_lap
- Chen vào đám đông, dò hỏi chuyện Dã Lang Bang  
  → `c1_d03`
- Tìm quán trọ, ẩn mình chờ thời  
  → `c1_d04` *(điều kiện: {"linh_thach": 1})* — *khoá: Cần ít nhất 1 linh thạch để thuê phòng*  
  ✦ linh thạch -1; sinh lực +5

---

### Đoạn `c1_d02` — Ngõ nhỏ sau chợ

*Ảnh:* `ngõ nhỏ, thị trấn`

Ngươi theo y vào một ngõ nhỏ. Thanh niên ấy dừng lại trước sạp thuốc, cẩn thận chọn từng củ thảo dược, trả giá chặt chẽ đến mức lão chủ sạp phải nhăn mặt.

Y không hề quay đầu, nhưng giọng nói vang lên đúng lúc ngươi định bước tới: “Đi theo ta làm gì?”

Ngươi giật mình. Người này… không đơn giản.

**Lựa chọn:**

- Thú nhận mình là kẻ mới tới, xin hỏi đường  
  → `c1_d05`  
  ✦ thần niệm +1; NPC: Thanh niên áo vải (cảnh giác)
- Giả vờ hỏi mua thuốc để che mắt  
  → `c1_d05`  
  ✦ NPC: Thanh niên áo vải (dò xét)

---

### Đoạn `c1_d03` — Gánh hàng rong ven chợ

*Ảnh:* `chợ, đám đông`

Ngươi ghé vào một gánh hàng rong, giả vờ hỏi giá rồi khéo léo dẫn chuyện.

“Dã Lang Bang à?” — lão bán hàng hạ giọng — “Lũ đó hung hãn lắm. Nghe nói chúng đang dòm ngó Thất Huyền Môn. Mà môn phái ấy đâu có dễ chọc…”

Lão lắc đầu, rồi nhanh chóng quay đi như sợ bị nghe thấy.

**Lựa chọn:**

- Hỏi thêm về Thất Huyền Môn  
  → `c1_d05`  
  ✦ mở cờ: biet_tin_da_lang_bang
- Cảm ơn rồi rời đi  
  → `c1_d05`

---

### Đoạn `c1_d04` — Quán trọ Phúc Lai

*Ảnh:* `quán trọ, trong nhà, đèn dầu`

Ngươi thuê một gian phòng nhỏ trên gác. Vừa đặt lưng, ngươi đã nghe tiếng bước chân dồn dập ngoài hành lang và những giọng nói nén xuống.

“Chúng nó tập trung ở ngoại thành… đêm nay động thủ.”

Ngươi nắm chặt mảnh ngọc vụn trong tay. Nó ấm lên một cách kỳ lạ.

**Lựa chọn:**

- Lắng nghe kỹ câu chuyện ngoài hành lang  
  → `c1_d05`  
  ✦ thần niệm +1; mở cờ: biet_tin_da_lang_bang
- Nghỉ ngơi, giữ sức  
  → `c1_d05`  
  ✦ sinh lực +5

---

### Đoạn `c1_d05` — Trấn Thất Huyền, chạng vạng

*Ảnh:* `thị trấn, hoàng hôn, căng thẳng`

Trời sẩm tối. Thị trấn Thất Huyền bỗng trở nên vắng vẻ lạ thường — người bán hàng dọn sạp sớm, cửa nhà đóng im ỉm.

Trên tường thành, mấy đạo sĩ mặc đạo bào xám đang đứng gác, tay đặt sẵn lên chuôi kiếm. Một luồng khí lạnh chạy dọc sống lưng ngươi.

Rồi từ phía rừng tối ngoài trấn, một tiếng sói tru dài vang lên.

**Lựa chọn:**

- Lên tường thành, xem chuyện gì xảy ra  
  → `c1_d05b`
- Ở lại trong trấn, tìm nơi trú ẩn  
  → `c1_d05b`

---

### Đoạn `c1_d05b` — Đêm buông, chuẩn bị đối phó

*Ảnh:* `thị trấn, đêm, im lặng`

Đêm buông xuống thật nhanh. Ngươi kiểm lại trong người — không vũ khí, không pháp bảo, chỉ có mảnh ngọc vụn và chút linh thạch.

Một cảm giác lạnh chạy dọc gáy. Ngươi biết mình phải chọn chỗ đứng trước khi mọi chuyện vỡ ra.

**Lựa chọn:**

- Tiến lên phía cổng môn, nơi đông người  
  → `c1_d06`
- Nấp ở nơi khuất, quan sát trước  
  → `c1_d07`

---

## Hồi Thân

### Đoạn `c1_d06` — Tường thành phía bắc

*Ảnh:* `tường thành, đêm, canh gác`

Ngươi lách qua đám đông đang náo loạn, trèo lên bậc thang đá dẫn tới tường thành.

Một đệ tử trẻ tuổi chặn ngươi lại, nhưng trước ánh mắt bình tĩnh của ngươi, hắn ngập ngừng rồi cho qua.

“Dã Lang Bang đấy,” — hắn thì thào — “chúng kéo tới mấy trăm người. Không biết Thất Huyền Môn giữ nổi không.”

**Lựa chọn:**

- Quan sát đội hình Dã Lang Bang từ trên cao  
  → `c1_d08`  
  ✦ thần niệm +2; mở cờ: thay_da_lang_bang

---

### Đoạn `c1_d07` — Kho lương phía nam

*Ảnh:* `kho, tối, ẩn nấp`

Ngươi tìm được một góc khuất trong kho lương cũ. Từ đây, ngươi có thể nghe rõ mọi động tĩnh mà vẫn an toàn.

Qua khe cửa, ngươi thấy vài bóng người lén lút chuyển từng bao tải ra ngoài. Không phải đệ tử môn phái — áo chúng có thêu hình đầu sói.

Ngươi nín thở.

**Lựa chọn:**

- Bám theo bọn chúng, xem chúng làm gì  
  → `c1_d08`  
  ✦ thần niệm +1; mở cờ: thay_gian_te
- Quay lại báo cho đệ tử canh gác  
  → `c1_d08`  
  ✦ mở cờ: thay_gian_te; NPC: Đệ tử Thất Huyền Môn (biết ơn)

---

### Đoạn `c1_d08` — Trận địa trước cổng môn

*Ảnh:* `chiến trận, cổng môn phái, đêm`

Một tiếng nổ lớn rung chuyển trấn nhỏ. Cổng lớn Thất Huyền Môn bị đánh bật khỏi bản lề.

Hàng trăm bóng người áo da thú tràn vào, gầm gừ như dã thú. Trên tường thành, các đạo sĩ đồng loạt xuất thủ — linh quang xanh lục và vàng kim chém xuống như mưa.

Ngươi đứng giữa hai làn sóng, và không có đường lui.

**Lựa chọn:**

- Xông vào đám hỗn chiến, tìm cơ hội  
  → `c1_d08b`  
  ✦ mở cờ: tham_gia_dai_chien
- Vòng ra sườn, cứu người bị thương  
  → `c1_d08b`  
  ✦ sinh lực -3; mở cờ: cuu_nguoi

---

### Đoạn `c1_d08b` — Cổng môn vỡ — khoảnh khắc quyết định

*Ảnh:* `cổng vỡ, hỗn loạn, linh quang`

Cổng lớn đổ sập, bụi đá mù mịt. Tiếng gầm thét và tiếng kim loại chạm nhau trộn thành một mớ hỗn độn.

Ngươi chỉ có vài nhịp thở để quyết định: xông vào hay vòng ra.

**Lựa chọn:**

- Xông thẳng vào đám hỗn chiến  
  → `c1_d09`
- Vòng ra sườn, tìm chỗ ít người  
  → `c1_d10`

---

### Đoạn `c1_d09` — Giữa vòng hỗn chiến

*Ảnh:* `hỗn chiến, vũ khí, máu`

Ngươi bị cuốn vào dòng người. Một gã áo da sói vung đao chém tới — ngươi nghiêng người né, suýt nữa thì trúng.

Trong khoảnh khắc ấy, ngươi nhận ra: thân thể này tuy yếu, nhưng phản xạ nhanh hơn người thường. Mảnh ngọc trong tay ngươi nóng ran.

Phía trước, một thanh niên gầy gò đang bị ba gã bao vây. Y không hề lùi.

**Lựa chọn:**

- Xông tới hỗ trợ thanh niên áo vải  
  → `c1_d11`  
  ✦ tu vi +8; sinh lực -5; mở cờ: giup_han_lap
- Lùi lại, giữ mạng trước đã  
  → `c1_d11`  
  ✦ sinh lực -1

---

### Đoạn `c1_d10` — Sườn đông, nơi tạm trú thương binh

*Ảnh:* `thương binh, cứu người, lửa`

Ngươi kéo một đệ tử trúng đao vào chỗ khuất, băng vết thương bằng vải áo.

Hắn nhìn ngươi, thều thào: “Ngươi… không phải người của môn phái này. Sao lại giúp?”

Trước khi ngươi kịp trả lời, một bóng người gầy gò lướt qua — nhanh như mèo, hướng thẳng vào hậu trận Dã Lang Bang. Trên lưng y, một cái bình nhỏ lóe sáng.

**Lựa chọn:**

- Bám theo bóng người gầy gò  
  → `c1_d11`  
  ✦ thần niệm +1; mở cờ: theo_han_lap
- Ở lại chăm sóc thương binh  
  → `c1_d11`  
  ✦ thần niệm +1; NPC: Đệ tử Thất Huyền Môn (cảm kích)

---

### Đoạn `c1_d11` — Hậu trận Dã Lang Bang

*Ảnh:* `doanh trại, đêm, nguy hiểm`

Ngươi lần tới hậu trận địch. Ở đây, giữa những túp lều da thú, có một căn lều lớn hơn hẳn — nơi Bang chủ Dã Lang Bang đang ngồi.

Một lão nhân mặt sẹo, thân hình vạm vỡ, đang mân mê một chiếc hộp gỗ. Bên trong hộp, thứ gì đó tỏa ra linh quang mờ ảo.

Lão cười khàn khàn: “Thất Huyền Môn tưởng giữ được bí kíp này sao? Ngây thơ.”

**Lựa chọn:**

- Rón rén tới gần, tìm cách đoạt hộp gỗ  
  → `c1_d11b`  
  ✦ mở cờ: thay_hop_go
- Quan sát, ghi nhớ rồi rút lui an toàn  
  → `c1_d11b`  
  ✦ thần niệm +1; mở cờ: biet_bi_kip

---

### Đoạn `c1_d11b` — Rìa hậu trận địch

*Ảnh:* `doanh trại, lửa, bóng tối`

Ngươi tiến sát hậu trận địch. Mùi da thú, mồ hôi và máu nồng nặc. Những túp lều da thú xếp san sát, lính gác thưa thớt vì phần lớn đã ra trận.

Một căn lều lớn hơn hẳn nằm ở giữa — nơi phát ra luồng linh khí đen đặc quánh.

**Lựa chọn:**

- Lẻn tới gần căn lều lớn  
  → `c1_d12`
- Chỉ quan sát từ xa rồi rút  
  → `c1_d13`

---

### Đoạn `c1_d12` — Trong lều Bang chủ

*Ảnh:* `lều, hộp gỗ, căng thẳng`

Ngươi nép sát vách lều. Tim đập thình thịch. Chỉ cần thêm ba bước nữa là tới được chiếc hộp.

Nhưng đúng lúc ấy, Bang chủ ngẩng đầu. Ánh mắt lão quét thẳng về phía ngươi.

“Có chuột.” — lão đứng dậy, linh khí đen ngòm bùng lên quanh thân.

**Lựa chọn:**

- Liều mình lao tới đoạt hộp rồi chạy  
  → `c1_d14`  
  ✦ sinh lực -8; mở cờ: doat_hop_go; nhận: Hộp gỗ bí ẩn
- Tung một nắm bụi rồi tháo chạy  
  → `c1_d13`  
  ✦ sinh lực -3

---

### Đoạn `c1_d13` — Bìa rừng phía tây

*Ảnh:* `rừng, đêm, ẩn nấp`

Ngươi chạy mãi cho tới khi tiếng gầm thét xa dần, rồi gục xuống sau một gốc cổ thụ.

Trong đầu ngươi, giọng nói lạnh lùng lại vang lên: “Biết địch biết ta, trăm trận không nguy. Ngươi học nhanh đấy.”

Phía xa, lửa cháy rực trời Thất Huyền trấn. Cuộc chiến vẫn chưa kết thúc.

**Lựa chọn:**

- Quay lại chiến trường, tìm cơ hội cuối  
  → `c1_d14`  
  ✦ thần niệm +1
- Ngồi lại, điều tức hồi phục  
  → `c1_d14`  
  ✦ tu vi +5; sinh lực +6

---

## Hồi Kết

### Đoạn `c1_d14` — Đại chiến — cổng môn Thất Huyền Môn

*Ảnh:* `đại chiến, cổng môn, linh quang`

*Video:* `dai_chien`

Trận chiến bùng lên dữ dội. Bang chủ Dã Lang Bang tung một quyền, linh khí đen cuộn thành hình sói khổng lồ, đánh sập nửa bức tường thành.

Các trưởng lão Thất Huyền Môn đồng loạt xuất thủ. Ánh sáng xanh lục và vàng kim đan vào nhau như dệt lụa, chấn động cả bầu trời đêm.

Ngươi đứng cách đó vài chục trượng, lần đầu tiên trong đời cảm nhận được thế nào là uy lực của tu sĩ.

**Lựa chọn:**

- Nhân lúc hỗn loạn, lẻn vào trong môn phái  
  → `c1_d14b`  
  ✦ mở cờ: vao_mon_phai
- Ở ngoài quan sát trận chiến, học hỏi  
  → `c1_d14b`  
  ✦ thần niệm +3; mở cờ: hoc_chien_dau

---

### Đoạn `c1_d14b` — Đại chiến leo thang

*Ảnh:* `đại chiến, chấn động, linh quang`

Trận chiến leo thang dữ dội. Mỗi quyền của Bang chủ đánh ra đều để lại một hố sâu trên nền đá. Các trưởng lão Thất Huyền Môn phải liên thủ mới cầm cự nổi.

Ngươi ép sát người vào tường, linh khí dư chấn quét qua khiến da mặt rát bỏng. Đây là cơ hội — hoặc là mồ chôn.

**Lựa chọn:**

- Nhân lúc hỗn loạn, lẻn vào trong môn phái  
  → `c1_d15`
- Bám theo rìa trận địa, quan sát học hỏi  
  → `c1_d16`

---

### Đoạn `c1_d15` — Sân trong Thất Huyền Môn

*Ảnh:* `môn phái, sân trong, tàn phá`

Ngươi lẻn được vào sân trong. Nơi đây đã bị tàn phá — cột đá gãy, cỏ cháy đen.

Bỗng ngươi nghe tiếng bước chân. Một thanh niên gầy gò, áo vải thô đang lúi húi nhặt thứ gì đó dưới đất — một chiếc bình nhỏ bằng ngọc.

Y ngẩng lên nhìn ngươi. Ánh mắt bình thản đến lạnh người.

**Lựa chọn:**

- Lên tiếng chào, tỏ ý muốn kết giao  
  → `c1_d17`  
  ✦ mở cờ: gap_han_lap; NPC: Hàn Lập (quen biết)
- Im lặng, giả vờ không thấy rồi đi tiếp  
  → `c1_d17`  
  ✦ mở cờ: gap_han_lap; NPC: Hàn Lập (chưa rõ)

---

### Đoạn `c1_d16` — Mái nhà ven sườn núi

*Ảnh:* `mái nhà, quan sát, đêm`

Ngươi leo lên một mái nhà ven sườn núi, quan sát toàn cảnh trận chiến.

Ngươi thấy rõ cách các trưởng lão phối hợp, cách người yếu né đòn, cách kẻ mạnh truy sát. Từng chiêu thức, từng sơ hở — tất cả khắc sâu vào trí nhớ ngươi.

Khi trận chiến tạm lắng, ngươi nhảy xuống, hướng vào trong môn phái. Ở đó, một bóng người gầy gò vừa lướt qua cửa hông.

**Lựa chọn:**

- Đuổi theo bóng người gầy gò  
  → `c1_d17`  
  ✦ mở cờ: gap_han_lap; NPC: Hàn Lập (chưa rõ)

---

### Đoạn `c1_d17` — Gặp Hàn Lập — hậu sơn Thất Huyền Môn

*Ảnh:* `hậu sơn, gặp gỡ, trăng`

*Video:* `gap_han_lap`

Trăng lên. Ngươi và thanh niên ấy đứng cách nhau ba bước, giữa hậu sơn vắng lặng.

“Ngươi không phải đệ tử ở đây.” — y nói, giọng không cao không thấp — “Và ngươi biết ta là ai.”

Ngươi khựng lại. Y nhìn thẳng vào mắt ngươi, không chút sợ hãi.

Trong đầu ngươi, giọng nói lạnh lùng vang lên: “Hàn Lập. Tạp dịch đệ tử. Cũng là kẻ sẽ đứng trên đỉnh tu tiên giới… nếu ngươi không làm hỏng mọi thứ.”

**Lựa chọn:**

- Thành thật: “Ta biết tương lai của ngươi.”  
  → `c1_d17b`  
  ✦ mở cờ: tiet_lo_meta; NPC: Hàn Lập (nghi ngờ nhưng tò mò)
- Cười trừ: “Ta chỉ là kẻ đi đường, tình cờ ghé qua.”  
  → `c1_d17b`  
  ✦ NPC: Hàn Lập (cảnh giác)
- Hỏi ngược: “Vậy ngươi là ai?”  
  → `c1_d17b`  
  ✦ NPC: Hàn Lập (hứng thú)

---

### Đoạn `c1_d17b` — Đối thoại với Hàn Lập

*Ảnh:* `hậu sơn, trăng, đối thoại`

Hàn Lập im lặng một lúc lâu, rồi chậm rãi nói: “Ngươi là kẻ đầu tiên nói với ta như vậy. Đa số người ở đây chỉ nhìn thấy một tạp dịch.”

Y cúi xuống nhặt chiếc bình ngọc, cẩn thận lau sạch bùn đất.

“Ta không tin ngươi. Nhưng ta sẽ nhớ ngươi.”

**Lựa chọn:**

- “Vậy hẹn gặp lại khi ngươi mạnh hơn.”  
  → `c1_d18`  
  ✦ NPC: Hàn Lập (quen biết)
- Im lặng gật đầu rồi rời đi  
  → `c1_d18`

---

### Đoạn `c1_d18` — Kết chương — bình minh Thất Huyền Môn

*Ảnh:* `bình minh, kết chương, núi`

Trời sáng. Dã Lang Bang rút lui, để lại Thất Huyền Môn tan hoang nhưng chưa gục ngã.

Hàn Lập quay người, bước vào trong sương sớm. Trước khi khuất bóng, y nói một câu: “Gặp lại.”

Ngươi đứng lại, mảnh ngọc vụn trong tay đã nguội. Giọng nói lạnh lùng vang lên lần cuối: “Chương một, kết thúc. Con đường phía trước… ngươi tự chọn.”

**Lựa chọn:**

- Khép lại Chương 1  
  → `__ket_thuc__`

**— Hết chương —**

---
