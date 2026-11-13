# Kế hoạch chi tiết (BẢN ĐỀ XUẤT) — Hồng Đức Tu Tiên Lộ

> Trạng thái: **đề xuất, chờ người dùng duyệt**. Chưa code.
> Cập nhật: 2026-11-12. Ghi lại các ý tưởng trao đổi ở mục 5–12.

---

## A. CƠ CHẾ GAME LOOP — "Chương + Nút" (chống lặp & chống quên)

### ĐỊNH NGHĨA "NÚT" (sửa lại cho đúng)
**"Nút" = một ĐOẠN / GIAI ĐOẠN NHỎ trong chương** — không phải nút bấm.
Một chương chia thành nhiều đoạn kế tiếp nhau. Mỗi đoạn có:
- một đoạn kể (bối cảnh + diễn biến),
- (tuỳ chọn) vài **lựa chọn** để người chơi bấm — *lựa chọn* mới là nút bấm.

Ví dụ Chương 1 = các đoạn: `chợ sớm → chạm mặt thanh niên áo vải → biến cố Dã Lang Bang → …`

### Vấn đề người dùng gặp
AI dẫn truyện hay bị: (1) **lặp vòng** khi bí ý tưởng, (2) **quên** nhân vật / đồ đạc /
sự kiện, (3) **lạc hướng** truyện.

### Giải pháp: 4 lớp bảo vệ

**Lớp 1 — Chương là một CHUỖI ĐOẠN do ta viết sẵn bằng dữ liệu.**
AI không tự bịa ra diễn biến kế tiếp; nó chỉ kể trong đoạn đã định.

```json
{
  "chuong": 1,
  "ten": "Đại chiến Dã Lang Bang",
  "doan": [
    {
      "id": "c1_d01",
      "boi_canh": "chợ sớm Thất Huyền trấn",
      "ke": "Ngươi mở mắt giữa buổi chợ sớm...",
      "lua_chon": [
        { "chu": "Lặng lẽ bám theo thanh niên áo vải", "den": "c1_d02",
          "hieu_ung": { "co": ["nghi_ngo_han_lap"] } },
        { "chu": "Chen vào đám đông dò hỏi Dã Lang Bang", "den": "c1_d03" },
        { "chu": "Tìm quán trọ ẩn mình", "den": "c1_d04",
          "dieu_kien": { "linh_thach": 1 } }
      ]
    }
  ]
}
```

**Lớp 2 — AI chỉ kể TRONG đoạn hiện tại.**
Mỗi lượt gửi cho AI một **thẻ ngữ cảnh** gồm: tóm tắt chương, đoạn hiện tại,
chỉ số hiện tại, túi đồ, nhân vật đã gặp, danh sách lựa chọn hợp lệ.
AI **không được** tự thêm đoạn mới hay đổi hướng truyện.

**Lớp 3 — Bộ nhớ CÓ CẤU TRÚC (lưu ra file, không dựa vào trí nhớ AI).**

| Nhớ cái gì | Lưu ở đâu | Nạp lại mỗi lượt? |
|---|---|---|
| Chỉ số (máu, mana, thần niệm…) | `state.json` | ✅ |
| Túi đồ (đan, phù, vũ khí) | `state.json` | ✅ |
| Cờ sự kiện (đã gặp Hàn Lập chưa…) | `flags` | ✅ |
| Nhân vật đã gặp + thái độ | `npc.json` | ✅ |
| Nhật ký tóm tắt | `summary` | ✅ |

→ AI "quên" cũng không sao, vì mỗi lượt ta **nạp lại** từ file.

**Lớp 4 — Chống lặp + tóm tắt luỹ tiến.**
- So sánh câu AI mới với các câu gần đây; giống quá → buộc viết lại.
- Mỗi đoạn chỉ chạy **1 lần** (đánh dấu `visited`).
- Mỗi 3–5 lượt, nén lịch sử thành 3–5 câu "đã xảy ra gì" → thay cho việc dump toàn bộ
  lịch sử (tiết kiệm token).

### Đoạn tự do (vùng sáng tạo)
Giữa các đoạn chính có **đoạn tự do**: cho phép người chơi **gõ hành động tự do**.
Kết quả do AI kể, nhưng sau đó vẫn **quay về đoạn chính kế tiếp** → không lạc truyện.
(Hai cách nhập vẫn giữ: **gõ tự do** *và* **bấm lựa chọn**.)

### Vì sao "đoạn trong chương" giải quyết được bệnh cũ

| Bệnh | Cách chặn |
|---|---|
| Lặp vòng | Đoạn đi 1 chiều, đánh dấu `visited`, phát hiện câu lặp |
| Quên nhân vật/đồ | Nạp lại `state.json` mỗi lượt |
| Lạc hướng | AI bị giới hạn trong đoạn; hướng truyện do ta viết |

### Số đoạn mỗi chương — tính toán

**Mục tiêu: 1 chương ≈ 45 phút chơi.** Người chơi vừa chơi vừa đọc → **2–3 phút mỗi lượt**
(đọc đoạn kể + suy nghĩ + chọn).

| Giả định | Số đoạn |
|---|---|
| 2 phút/lượt | 22,5 |
| **2,5 phút/lượt (trung bình)** | **18** |
| 3 phút/lượt | 15 |

Trừ ~5 phút tạo nhân vật (đầu game) → phần chơi còn ~40 phút.

**→ Chốt: 18 đoạn/chương.** Cấu trúc 3 hồi:

| Hồi | Số đoạn | Nội dung | Thời lượng |
|---|---|---|---|
| **Mở** | 5 | Tạo nhân vật + nhập môn + gặp gỡ đầu | ~12 phút |
| **Thân** | 8 | Diễn biến chính, leo thang, gặp NPC | ~20 phút |
| **Kết** | 5 | Cao trào + lựa chọn lớn + kết chương | ~13 phút |

Trong 18 đoạn:
- **14 đoạn có lựa chọn** (14 × 2,5 ≈ 35 phút)
- **4 đoạn đặc biệt** (không chọn hoặc lâu hơn): mở đầu, 2 khoảnh khắc lớn (đại chiến /
  gặp Hàn Lập — có video, ~3–4 phút mỗi đoạn), kết chương.

**Lưu ý:** con số này là **mục tiêu**, sẽ **tinh chỉnh sau khi chơi thử**. Đoạn ngắn thì
nhiều hơn, đoạn dài (đại chiến) thì ít hơn nhưng mỗi đoạn lâu hơn.

### Chi phí token mỗi chương (ước tính)

| Khoản | Mỗi lượt | 18 lượt/chương |
|---|---|---|
| Vào (thẻ ngữ cảnh + tóm tắt) | ~1.500 token | ~27.000 |
| Ra (AI kể + JSON cập nhật) | ~400 token | ~7.200 |
| **Tổng** | ~1.900 | **~34.000 token/chương** |

→ Với Gemini free tier (hạn mức lớn), **một chương chỉ tốn ~34k token** — thoải mái.
Chế độ KHÔNG AI thì **0 token**.

---

## B. BẢNG CHỈ SỐ (dùng chung cho cả NVC và NPC)

### Chỉ số cơ bản

| Chỉ số | Viết tắt | Ý nghĩa |
|---|---|---|
| Sinh lực | SL / HP | Máu. Về 0 → trọng thương/chết |
| Linh lực | LL / MP | Năng lượng thi triển pháp thuật, pháp bảo |
| Thần niệm | TN | Nhận thức linh hồn (xem mục C) |
| Tấn công | TC | Sát thương vật lý cơ bản |
| Phòng thủ | PT | Giảm sát thương vật lý |
| Chí mạng | CM | Tỉ lệ đánh trúng yếu huyệt |
| Bạo kích | BK | Hệ số sát thương khi chí mạng |
| Xuyên giáp | XG | Bỏ qua một phần Phòng thủ địch |
| Tốc độ | TD | Ai cao hơn **đánh trước** (tiên cơ) |

### Tấn công phép — 9 hệ
Mỗi hệ có **một con số tấn công riêng**: **Kim · Mộc · Thủy · Hỏa · Thổ · Lôi · Phong · Băng · Độc**.

Ví dụ: tu Hỏa hệ → tấn công Hỏa cao, các hệ khác thấp.
Pháp thuật/pháp bảo gây sát thương theo hệ tương ứng.

### Kháng phép — 9 hệ (đối xứng với tấn công phép)
Mỗi hệ có **một con số kháng riêng**: Kim · Mộc · Thủy · Hỏa · Thổ · Lôi · Phong · Băng · Độc.

**Công thức gợi ý:** sát thương phép hệ X = (Tấn công phép hệ X) − (Kháng phép hệ X của địch).
Ví dụ: địch tấn công Hỏa 200, ta kháng Hỏa 50 → nhận 150.

→ Tu sĩ tu một hệ thường **kháng mạnh hệ đó** và **yếu hệ khắc** (Hỏa khắc Kim, Thủy khắc Hỏa…).

### Trang bị cộng chỉ số
Trang bị = **đan dược · phù lục · vũ khí/pháp bảo**. Mỗi món cộng một số chỉ số
(có thể cộng cả tấn công phép và kháng phép theo hệ).
→ Ai trang bị tốt hơn thì mạnh hơn.

### Chiến đấu (giai đoạn sau)
Khi A đánh B → mở **bảng giao diện chiến đấu**, AI căn cứ chỉ số 2 bên để phán thắng thua.
Tốc độ quyết định ai ra đòn trước.

---

## C. THẦN NIỆM (THẦN THỨC) — giải thích

**Là gì:** "thần thức" (神识) là **nhận thức / linh hồn** của tu sĩ, tách khỏi thể xác.
Nó mạnh dần theo cảnh giới: Luyện Khí ~ vài **sợi**; Trúc Cơ ~ vài chục sợi;
Kết Đan ~ hàng trăm sợi; Nguyên Anh ~ hàng ngàn sợi; Hóa Thần ~ hàng vạn sợi.

**Công dụng (theo nguyên tác):**

| # | Công dụng | Trong game |
|---|---|---|
| 1 | **Dò xét** — quét cảnh giới, phát hiện ẩn thân, cạm bẫy, pháp bảo | TN cao hơn → biết chỉ số địch trước (tiên cơ) |
| 2 | **Điều khiển pháp bảo** — ngự kiếm, ngự phù, thuyền bay | TN cao → điều khiển nhiều pháp bảo, xa hơn |
| 3 | **Luyện đan / luyện khí / vẽ bùa** — khống hỏa, khắc trận văn | TN thấp → dễ nổ lò, thất bại |
| 4 | **Cảm ứng nguy hiểm** — cảm nhận sát ý, độc khí | Cảnh báo cạm bẫy trước khi bước vào |
| 5 | **Tấn công thần thức** — đánh trực tiếp linh hồn địch | Đòn mạnh ở cảnh giới cao |
| 6 | **Chống thần thức công kích** | Phòng thủ linh hồn, chống mê hoặc |
| 7 | **Lưu trữ** — ghi nhớ ngọc giản | Mở khoá thông tin, bản đồ |

→ **Tóm lại trong game:** thần niệm = vừa là **"giác quan"** (dò địch, cảnh báo),
vừa là **"tay nghề"** (luyện đan/khí/bùa), vừa là **"vũ khí tinh thần"**.
Thần niệm thấp hơn địch nhiều → có thể bị **áp chế** (choáng, mất kiểm soát).

---

## D. THƯ VIỆN ẢNH & VIDEO (theo PIC-IN-GAME)

### Vấn đề: AI lấy SAI ảnh nếu thuộc tính quá sơ sài

Ví dụ: NPC **Độc Nhĩ Đạt** — *một kẻ lùn, da đen, nham hiểm*.
Nếu thư viện chỉ ghi `gioi_tinh: nam` → AI có thể lấy **một kẻ lùn da trắng, mặt chính khí**.
→ Sai hoàn toàn. Vì vậy **thuộc tính phải chi tiết và bắt buộc khớp**.

### Bộ thuộc tính nhân vật (chi tiết)

| Nhóm | Thuộc tính | Ví dụ (Độc Nhĩ Đạt) |
|---|---|---|
| **Chủng loại** | `chung_loai` | nhân loại / **yêu thú** / **yêu thú hoá hình người** / **ma thú** / **quỷ** / **khôi lỗi** / **cương thi** / linh thể / bán yêu… |
| Giới tính | `gioi_tinh` | nam / nữ / vô tính |
| Tuổi tác | `tuoi_tac` | thiếu niên / trẻ / trung niên / già / cổ xưa |
| **Vóc dáng** | `voc_dang` | **lùn**, thấp, trung bình, cao, khổng lồ, gầy, béo, cường tráng |
| **Màu da** | `mau_da` | **đen**, trắng, vàng nhạt, xanh lục, xám, tái nhợt… |
| **Ngoại hình** | `ngoai_hinh` | "mặt nhọn, mắt ti hí, răng nanh" |
| **Thần thái** | `than_thai` | **nham hiểm**, chính khí, lạnh lùng, hung tợn, hiền lành, điên cuồng |
| Tóc / đặc điểm | `dac_diem` | hói, sẹo mắt, râu dài, sừng, đuôi, cánh |
| Trang phục | `trang_phuc` | áo vải thô, đạo bào, giáp da, hắc bào |
| Tộc | `chung_toc` | nhân loại, yêu tộc, ma tộc, quỷ tộc |
| Cảnh giới | `canh_gioi` | Luyện Khí / Trúc Cơ / Kết Đan… |
| Tính cách | `tinh_cach` | đa nghi, tàn nhẫn, trầm tĩnh |
| Cảm xúc | `cam_xuc` | bình thản, giận dữ, sợ hãi |

**Quy tắc khớp:** thuộc tính **bắt buộc** (chủng loại, giới tính, tên nhân vật) phải
**khớp tuyệt đối**; thuộc tính còn lại (vóc dáng, màu da, thần thái) **ưu tiên khớp** —
nếu không có ảnh khớp hết thì chọn ảnh khớp nhiều nhất và **báo rõ là ảnh gần đúng**.

### Ví dụ ghi mục lục

```json
{
  "id": "nv_doc_nhi_dat_01",
  "loai": "nhan_vat",
  "ten_nhan_vat": "Độc Nhĩ Đạt",
  "chung_loai": "yêu thú hoá hình người",
  "gioi_tinh": "nam",
  "tuoi_tac": "trung niên",
  "voc_dang": "lùn",
  "mau_da": "đen",
  "ngoai_hinh": "mặt nhọn, mắt ti hí, tai nhọn",
  "than_thai": "nham hiểm",
  "dac_diem": ["tai nhọn", "răng nanh"],
  "trang_phuc": "hắc bào rách",
  "chung_toc": "yêu tộc",
  "tinh_cach": ["nham hiểm", "tham lam"],
  "tags": ["phản diện", "yêu thú"]
}
```

Ví dụ bối cảnh:
```json
{ "id": "bc_dong_phu_03", "loai": "boi_canh", "tags": ["động phủ", "hang động", "tối"] }
```

**AI tra theo thuộc tính, không đoán mò** → không thể lấy ảnh nữ/ông già/chính khí
cho một kẻ lùn da đen nham hiểm.

### Thư viện video
Video = **chuỗi ảnh + hiệu ứng** (kiểu intro CapCut), không phải file phim.
Cùng bộ ảnh phục vụ cả hai. AI chọn chuỗi ảnh + hiệu ứng → sinh timeline:

```js
const timeline = [
  { img: "library/bc_dong_phu_03.jpg", fx: "kenburns",   sec: 1.0 },
  { img: "library/vk_kiem_01.jpg",     fx: "ink-spread", sec: 0.8 },
  { img: "library/hq_dot_pha_02.jpg",  fx: "flash",      sec: 1.2 }
];
```

Có thể có `index_video.json` mô tả **mẫu video** (ví dụ "intro động phủ" = 4 ảnh + fx).

---

## E. CHI PHÍ TOKEN (hướng miễn phí, chủ đạo Gemini)

**Chỉ tốn token khi AI kể chuyện / phán định.** Ảnh và video **không tốn token**.

Cách tiết kiệm:
1. **Thẻ ngữ cảnh ngắn gọn, có cấu trúc** — không dump toàn bộ lịch sử.
2. **Tóm tắt luỹ tiến** — nén lịch sử thành vài câu.
3. **Giới hạn độ dài phản hồi** AI (khoảng 300–500 token/lượt).
4. **Gộp 1 lượt = 1 lần gọi** — vừa kể vừa trả JSON cập nhật chỉ số.
5. **Cache** kết quả cho cùng đoạn + cùng hành động (chơi lại không tốn).
6. **Chế độ KHÔNG AI** — đoạn + kết quả viết sẵn → chơi miễn phí 100%.
7. **Đếm token** mỗi lượt, hiển thị nếu muốn.

Ngân sách dự kiến (chốt sau khi đo thực tế): 1 lượt ≈ 800–1.500 token vào + 300–500 ra.

---

## F. BẢNG HỆ THỐNG — nhiều tab, độ trễ thấp

Hiện tại: tất cả tab render sẵn, ẩn bằng `display:none` → **chuyển tab tức thì, không độ trễ mạng**.

Khi có nhiều tab + nội dung nặng:
1. **Giữ pane đã render**, chỉ ẩn/hiện — không render lại.
2. **Lazy-load** nội dung nặng (ảnh, danh sách dài) ở lần mở tab đầu.
3. `content-visibility:auto` cho pane dài → bỏ qua vẽ phần ngoài màn hình.
4. Tránh reflow: đặt `min-height` cho pane.
5. Nhiều tab → **thanh tab cuộn ngang** thay vì thu nhỏ chữ.
6. **Vuốt ngang để đổi tab** trên mobile.
7. Đo độ trễ thật bằng Performance API + kiểm chứng bằng ảnh chụp.

---

## G. NGHỀ PHỤ + KINH TẾ — giai đoạn sau

**Quyết định:** để **giai đoạn sau** (không làm trong Chương 1–3).

**Hiện tại:** SPEC mục 9 mới nêu **ý tưởng** (luyện đan · luyện khí · vẽ bùa, thành công → video),
**chưa có thiết kế chi tiết hệ thống**.

**Khi làm, sẽ dựng 1 hệ thống chung cho cả 3 nghề:**

| Thành phần | Nội dung |
|---|---|
| Nguyên liệu | Thảo dược, khoáng thạch, da/xương yêu thú |
| Công thức | Nguyên liệu + cấp + **thần niệm yêu cầu** |
| Quá trình | Thần niệm khống hỏa → tỉ lệ thành công theo kỹ năng + thần niệm + nguyên liệu + đan lô/đỉnh |
| Kết quả | Thành phẩm + cấp phẩm (hạ → cực phẩm) |
| Thất bại | Mất nguyên liệu / nổ lò |
| Thành công | → video ngắn (PIC-IN-GAME) |

### Thị trường & kinh tế (kèm theo nghề)
**Có nghề → có thị trường kinh tế.** Khi làm nghề phụ, làm luôn:

| Thành phần | Nội dung |
|---|---|
| Tiền tệ | Linh thạch (hạ / trung / thượng phẩm) |
| Mua | Nguyên liệu, đan dược, phù lục, vũ khí, bí kíp |
| Bán | Thành phẩm do mình luyện, chiến lợi phẩm |
| Giá | Theo cấp phẩm + độ hiếm + thời điểm (chiến tranh → giá thuốc tăng) |
| NPC buôn | Thương nhân, tán tu bán rong, hội đấu giá |
| Đấu giá | Tranh giá với NPC cho bảo vật hiếm |

→ Ghi nhận là **hạng mục giai đoạn sau**, chưa làm ngay.

---

## H. CÔNG CỤ ĐÃ ĐỔI TÊN

`INKFRAME` → **`PIC-IN-GAME`** (Pic-in-Game Method).
Đã cập nhật: skill, báo cáo, `AGENTS.md`, `README.md`, tên thư mục, trigger.

---

## I. TÓM TẮT QUYẾT ĐỊNH NGƯỜI DÙNG (2026-11-12)

| # | Vấn đề | Quyết định |
|---|---|---|
| 1 | "Nút" là gì | = **đoạn/giai đoạn nhỏ** trong chương, **không phải nút bấm**. Vẫn giữ **gõ tự do + bấm lựa chọn** |
| 2 | Bảng chỉ số | Thêm **tấn công phép 9 hệ** (Kim Mộc Thủy Hỏa Thổ Lôi Phong Băng Độc), đối xứng với kháng phép 9 hệ |
| 3 | Thư viện ảnh | Thuộc tính phải **chi tiết**: chủng loại (yêu thú, yêu thú hoá hình người, ma thú, quỷ, khôi lỗi, cương thi…), vóc dáng, màu da, thần thái… |
| 4 | Nghề phụ | **Giai đoạn sau**; kèm theo sẽ có **thị trường kinh tế** |
| 5 | Mục 10 | Đã hiểu |
| 6 | Tên công cụ | Đổi `INKFRAME` → **`PIC-IN-GAME`** ✅ đã làm |
| 7 | Số đoạn/chương | **18 đoạn** (45 phút chơi, 2,5 phút/lượt). Cấu trúc 3 hồi: 5 mở · 8 thân · 5 kết |
| 8 | Bảng chỉ số | **Đã đủ** (10 cơ bản + 9 tấn công phép + 9 kháng phép) |
