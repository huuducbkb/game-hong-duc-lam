# Góp ý bản thảo Chương 1 + kế hoạch sửa (BẢN ĐỀ XUẤT)

> Trạng thái: **đề xuất, chờ người dùng duyệt**. Chưa sửa code.
> Ngày: 2026-11-12. Ghi lại 5 góp ý của người dùng về bản thảo Chương 1.

---

## 1. NĂM GÓP Ý

| # | Góp ý | Việc phải làm |
|---|---|---|
| 1 | Văn phong đúng tiên hiệp nhưng **hơi khô**, **thiếu nội tâm NVC**, **đối thoại NPC quá ít**, **nội dung hơi ngắn** | Thêm nội tâm + đối thoại + kéo dài đoạn. **Thêm cơ chế "độ hảo cảm"** |
| 2 | Đoạn kể nên **5–8 câu** | Kéo dài mỗi đoạn kể |
| 3 | **Ngôi kể**: muốn **nhập vai nhân vật**, không phải "kẻ quan sát" | Đổi sang **ngôi thứ nhất "ta"** + nội tâm |
| 4 | Hàn Lập đúng chất | Giữ nguyên |
| 5 | **Nếu chọn lựa chọn khác thì sao? Không có AI key thì ai dẫn truyện, ai viết tiếp?** | Xem mục 4 |

---

## 2. CƠ CHẾ "ĐỘ HẢO CẢM" (đề xuất)

### Khái niệm
Mỗi NPC có một con số **hảo cảm** với người chơi, từ **−100 đến +100**.
Con số này quyết định:
- NPC **nói chuyện với ngươi kiểu gì** (giọng điệu, thái độ)
- **Lựa chọn nào mở ra / khoá lại**
- NPC có **giúp** (đồng minh chiến đấu, bán rẻ, cho đồ) hay **hại** (tấn công, phản bội)
- Kết cục về sau (bạn hay thù)

### 6 mức hảo cảm

| Khoảng | Mức | Thái độ NPC |
|---|---|---|
| −100 … −60 | **Tử địch** | Tấn công ngay khi gặp |
| −59 … −20 | **Thù địch** | Không nói chuyện, đe doạ |
| −19 … +19 | **Người dưng** | Nói chuyện hạn chế, lạnh nhạt |
| +20 … +49 | **Quen biết** | Đối thoại bình thường |
| +50 … +79 | **Thân thiết** | Chia sẻ bí mật, giúp đỡ |
| +80 … +100 | **Tri kỷ / sinh tử chi giao** | Kết nghĩa, hi sinh vì nhau |

### Đối thoại dựa vào hảo cảm (trả lời góp ý 1)
- Mỗi lựa chọn có thể **yêu cầu hảo cảm tối thiểu**:
  `dieu_kien: {hao_cam: {"Hàn Lập": 50}}` → chỉ hiện khi đã thân thiết.
- Mỗi lựa chọn **thay đổi hảo cảm**:
  `hieu_ung: {hao_cam: {"Hàn Lập": +10}}`.
- **Cùng một đoạn, NPC trả lời khác nhau theo mức hảo cảm** — viết sẵn 2–3 biến thể
  (người dưng / quen biết / thân thiết). Không có AI vẫn chạy được.

### Ví dụ (đoạn gặp Hàn Lập `c1_d17`)

| Hảo cảm | Hàn Lập phản ứng |
|---|---|
| Người dưng (0) | “Ngươi không phải đệ tử ở đây. Đi đi.” |
| Quen biết (+30) | “...Ngươi biết ta. Tại sao?” |
| Thân thiết (+60) | “Ngươi đã giúp ta ở cổng môn. Ta nhớ.” |

---

## 3. NGÔI KỂ + VĂN PHONG (trả lời góp ý 1, 2, 3)

### Hiện tại (ngôi thứ hai — như người kể chuyện nói với bạn)
> **Ngươi** mở mắt giữa buổi chợ sớm... Chỉ biết trên tay **ngươi** có một mảnh ngọc vụn...

→ Người chơi bị đẩy ra ngoài: giống **kẻ quan sát** bị kể lại.

### Đề xuất (ngôi thứ nhất "ta" + nội tâm)
> **Ta** mở mắt giữa buổi chợ sớm của thị trấn Thất Huyền. Mùi thuốc bắc xộc vào mũi,
> tiếng mặc cả ồn ào, và đâu đó tiếng ngựa hí vang.
>
> *Đây… là đâu?* Ta nhớ mình đã… không, ký ức hỗn độn quá. Chỉ biết trên tay có một
> mảnh ngọc vụn còn ấm, và trong đầu vang lên một giọng nói lạnh lùng:
> “Nghịch chuyển càn khôn… đã bắt đầu.”
>
> Ta nghiến răng. **Thân thể này không phải của ta** — nhưng ta đang sống trong nó.
>
> Phía xa, một thanh niên gầy gò, áo vải thô, lặng lẽ quan sát gánh hàng thuốc.
> Ánh mắt y sắc như dao. Tim ta khẽ đập nhanh — ta linh cảm kẻ này không tầm thường.

→ **Nội tâm** in nghiêng (`*…*`), lời NPC trong ngoặc kép. Người chơi **nhập vai**.

### Quy ước mới
| Thành phần | Cách viết |
|---|---|
| Tự sự | Ngôi thứ nhất **"ta"** |
| Nội tâm / suy nghĩ | *in nghiêng* |
| Lời thoại NPC | “trong ngoặc kép” |
| Giọng "Hệ Thống" | giữ lạnh lùng, khác giọng thường |
| Độ dài mỗi đoạn | **5–8 câu** (hiện 3–5) |

---

## 4. AI DẪN TRUYỆN? CHỌN NHÁNH KHÁC THÌ SAO? (trả lời góp ý 5)

### Sự thật về cách game đang chạy
**Toàn bộ đoạn kể là do TÔI viết sẵn**, lưu trong `game/chapters/chuong1.json`.
Engine **không sinh chữ** — nó chỉ **đi theo đồ thị** đoạn đã viết.

### Chọn lựa chọn khác thì sao?
Mỗi lựa chọn trỏ tới **một đoạn đã viết sẵn riêng**. Ví dụ:

```
c1_d01 (chợ sớm)
 ├─ "bám theo thanh niên"     → c1_d02 (ngõ nhỏ — Hàn Lập phát hiện)
 ├─ "dò hỏi Dã Lang Bang"     → c1_d03 (gánh hàng rong — nghe tin)
 └─ "tìm quán trọ"            → c1_d04 (quán trọ — nghe lén)
```

→ Chọn khác → **đoạn khác** (đã viết sẵn). Chương 1 hiện có **103.680 đường đi khác nhau**
đã tính ra. Đây là kiểu **"sách phiêu lưu" (gamebook)**: tác giả viết hết, người chơi chọn đường.

### Vậy ai dẫn truyện khi KHÔNG có AI key?
**Người dẫn truyện = văn bản tôi viết sẵn.** Không cần AI, truyện vẫn chạy đủ 18 đoạn,
vẫn rẽ nhánh, vẫn có kết. **Chế độ KHÔNG AI chơi được 100% miễn phí.**

### Còn ô "gõ hành động tự do"?
Đây là chỗ **duy nhất** cần AI. Đề xuất xử lý:

| Phương án | Mô tả | Nhược điểm |
|---|---|---|
| **A. Ẩn ô gõ tự do** ở chế độ không AI | Chỉ bấm lựa chọn | Mất phần sáng tạo |
| **B. Trả lời theo từ khoá** | Nhận vài chục từ khoá, trả câu viết sẵn | Cứng, dễ hụt |
| **C. Giữ câu trả lời chung chung** (như hiện tại) | Không tốn gì | Nhạt |
| **D. Bật ô gõ tự do khi CÓ AI key** | Có AI → gõ tự do thật; không AI → ẩn | Cần cả 2 chế độ |

→ **Đề xuất chọn D**: chế độ không AI chỉ bấm lựa chọn (đủ hay), chế độ có AI mở ô gõ tự do.

### Hai chế độ chạy song song
| | Không AI (mặc định) | Có AI (Gemini/OpenRouter) |
|---|---|---|
| Người kể | Văn bản viết sẵn | AI **kể lại** đoạn đã viết, sinh động hơn |
| Gõ tự do | Ẩn (hoặc câu chung) | AI **viết tiếp** theo ngữ cảnh |
| Đổi hướng truyện? | Không (cố định) | **Không** (AI vẫn bị nhốt trong đoạn) |
| Chi phí | **0 token** | Tốn token |

**Điểm mấu chốt:** dù có AI hay không, **khung truyện do ta viết** → không bao giờ lạc hướng.

---

## 5. VIỆC SẼ LÀM (sau khi bạn duyệt)

1. Viết lại **23 đoạn** theo: ngôi thứ nhất "ta" + nội tâm + 5–8 câu + thêm đối thoại.
2. Thêm **cơ chế hảo cảm**: mỗi NPC một con số, 6 mức, mở/khoá lựa chọn.
3. Viết **biến thể đối thoại** theo mức hảo cảm cho các đoạn có NPC.
4. Xuất lại bản thảo để bạn đọc.

---

## 6. CẦN BẠN CHỐT

1. **Ngôi kể**: "ta" (ngôi 1) đúng ý bạn chưa? Hay muốn kiểu khác?
2. **Hảo cảm**: thang −100…+100 với 6 mức — ổn chưa? Có muốn hiện **thanh hảo cảm**
   trong bảng Hệ Thống (tab "Đã gặp") không?
3. **Gõ tự do khi không có AI**: chọn phương án **D** (ẩn khi không AI) hay phương án khác?
4. **Đối thoại NPC**: mỗi đoạn có NPC nên có mấy câu thoại? (đề xuất 2–4 câu)
