# Kế hoạch sửa Chương 1 — mạch lạc + 5 cơ duyên

> Trạng thái: **ĐỀ XUẤT — chờ người dùng duyệt**. Chưa sửa code.
> Ngày: 2026-11-14. Ghi lại các quyết định của người dùng ở mục 6.

---

## 0. VẤN ĐỀ ĐANG CÓ

### 0.1. Truyện rời rạc, nhảy cảnh
Người chơi phát hiện: nhánh đệ tử môn phái — vừa đào được **ngọc cốt** (vật lạ có bóng
người bên trong) — thì bị **nhảy thẳng** sang cảnh "đêm buông, ngoại môn im lặng"
rồi tới trận đánh. Không có câu bắc cầu, không có đoạn tìm hiểu ngọc cốt.

### 0.2. Nguyên nhân (đã tra bằng chứng)
1. **Bản thảo gốc = nhánh tán tu** (`docs/ban-thao/chuong1.md`, 23 đoạn, id `c1_d01`…`c1_d18`).
2. **4 nhánh kia viết sau**, sao chép **khung nhịp** của bản thảo gốc (01→02→…→17→18)
   rồi thay bối cảnh. Bằng chứng: các nhánh dùng **cùng số nhịp** (`p01`, `y01`, `g01`…).
3. **Ép hội tụ**: mọi nhánh phải đổ về `c1_d18` → nhánh ngắn (12–16 đoạn) phải **nhảy**
   cho kịp đích.
4. **Chương bị trói vào mục tiêu "tới trận đánh + gặp Hàn Lập"** → mạch phụ bị cắt phăng.

### 0.3. Cơ duyên bị bỏ đói
Tra toàn chương: **5/5 vật phẩm gieo ra đều 0 lần nhắc lại**:

| Đoạn | Vật phẩm (cũ) | Nhắc lại |
|---|---|---|
| `c1_p02b` | Ngọc cốt bí ẩn | 0 |
| `c1_d12` | Hộp gỗ bí ẩn | 0 |
| `c1_y02` | Thanh linh thảo trăm năm | 0 |
| `c1_y03` | Kim sang dược | 0 |
| `c1_h03` | Mảnh tin của Tần Báo | 0 |

Mọi cờ sự kiện (`biet_tin_da_lang_bang`, `thay_gian_te`, `giup_han_lap`…) cũng **không dùng lại**.

### 0.4. Lỗi "lựa chọn giả"
- **25 chỗ** nhiều lựa chọn cùng dẫn 1 đích.
- **1 chỗ vô nghĩa thật**: `c1_d05` — hai lựa chọn đều không có hiệu ứng.
- **1 chỗ lời mơ hồ**: `c1_p02b` — "giấu kỹ, coi như chưa từng thấy" vs "siết chặt, giữ cho mình"
  (thật ra khác cơ chế: một bên nhận ngọc, một bên không — nhưng chữ không thể hiện).

---

## 1. GỠ 4 RÀNG BUỘC TỰ ĐẶT (người dùng đã duyệt)

| # | Ràng buộc cũ | Thay bằng |
|---|---|---|
| 1 | Mọi nhánh hội tụ về `c1_d18` | **Mỗi nhánh có kết riêng, không trùng nhau** |
| 2 | Đúng 18 đoạn/chương | **Không ép số** — đoạn nào cần thì viết |
| 3 | Ép tới trận đánh ở nhịp 17 | **Biến cố ập tới tự nhiên** (trận là sự kiện thế giới, nhân vật tự bị cuốn vào) |
| 4 | Mọi nhánh dùng chung khung nhịp | **Mỗi nhánh có nhịp riêng** hợp cốt truyện nó |

**Ghi chú:** ràng buộc **canon** vẫn giữ (theo `SPEC.md`): chương 1 = Đại chiến Dã Lang Bang,
lần đầu gặp Hàn Lập. Chỉ bỏ ràng buộc **tự đặt**.

---

## 2. CHỮA MẠCH TRUYỆN

### Việc A — Sửa 2 chỗ lỗi rõ
| Đoạn | Sửa |
|---|---|
| `c1_d05` | Hai lựa chọn phải **khác hiệu ứng** (hoặc gộp còn 1 lựa chọn) |
| `c1_p02b` | Sửa **lời** cho rõ: một bên *"bỏ lại chỗ cũ"* (không nhận), một bên *"siết chặt giữ riêng"* (nhận ngọc) |

### Việc B — Câu bắc cầu ở mọi mối nối lệch cảnh
Thêm **1–2 câu chuyển** ở cuối đoạn nguồn cho mọi mối nối bị nhảy (thời gian/địa điểm).
Không đổi cốt truyện. Danh sách mối nối: xem khi thực hiện (khoảng 25 chỗ).

Ví dụ điển hình — nhánh p:
```
TRƯỚC:  p02b (vườn dược, ban ngày)  →  p05b ("Đêm buông xuống…")   ← nhảy
SAU:    p02b + "…Trời còn sớm. Ta cất ngọc vào vạt áo, lòng nặng trĩu.
                Còn một ngày nữa để xoay xở."  →  p05b
```

### Việc C — Tách nhánh thật cho 23 chỗ hội tụ
Mỗi lựa chọn dẫn tới **một đoạn riêng** thay vì cùng đích. Làm hết một lượt.

---

## 3. NĂM CƠ DUYÊN (người dùng chốt)

> Nguyên tắc: **bảo vật bị phong ấn / dùng một phần** — không phá tiến trình game.

### 3.1. Nhánh **p (môn phái)** — NGỌC CỐT
- **Bản chất:** trong ngọc cốt có **một phân thân là người thật** (da thịt, không phải tàn hồn) —
  **nữ tu Hợp Hoan Tông**. Nàng cần **khế ước nô lệ** để song tu khôi phục sức mạnh.
- **Vai trò game:** **người dẫn dắt tu hành** cho người chơi.
- **Thời điểm (người dùng chốt):** **ký khế ước ngay trong chương 1**.
- **Mức nội dung:** giữ ở mức **gợi ý** (theo ghi chú cũ trong `game/xuat_than.json`).
  Không viết cảnh thân mật trực tiếp. Phần cốt lõi (khế ước, hướng dẫn tu hành, khôi phục
  sức mạnh) viết đầy đủ.
- **Gắn xuất thân ẩn:** `tuyet_co` (đã có trong `xuat_than.json`, đang khoá).

### 3.2. Nhánh **d (tán tu)** — HỒNG TRẦN KIẾM HẠP
- **Bản chất:** chí bảo — **phóng vạn kiếm, phá vạn pháp trong thiên địa**.
- **Chính là "hộp gỗ"** ở `c1_d12` (đổi tên + mô tả).
- **Cơ chế:** **bị phong ấn**, chỉ dùng được một phần:

| Cảnh giới người chơi | Số kiếm dùng được |
|---|---|
| Luyện Khí | 2 |
| Trúc Cơ | 4 |
| Kim Đan | 16 |
| (tiếp) | **nhân đôi mỗi cấp** |

→ Giúp người chơi dễ hơn, nhưng không vượt cảnh giới.

### 3.3. Nhánh **y (dược đồng)** — VÔ VẠN THỌ NGUYÊN
- **Bản chất:** **viên đan dược duy nhất**. Nuốt vào → **thọ nguyên vô tận, trẻ mãi không già**.
- Thay cho "Thanh linh thảo trăm năm" + "Kim sang dược" (2 món cũ).
- **Thời điểm (người dùng chốt):** **nuốt ngay trong chương 1**.
- **Cân bằng:** chỉ ảnh hưởng **thọ nguyên** — không tăng tu vi, không tăng chiến lực.
  Người chơi vẫn phải tu luyện bình thường.

### 3.4. Nhánh **g (gia tộc)** — NHẪN NGỌC GIA TỘC
- **Bản chất:** chí bảo — **bên trong có gia tốc thời gian**: 1 ngày ngoài = **30 ngày** trong.
- **Nhận chủ:** gia tộc coi nó là **chiếc nhẫn bình thường, không ai để ý**. Chỉ khi gặp
  **đúng người có đại cơ duyên** (người chơi) thì nhẫn **mới nhận chủ** và lộ bản chất.
- **KHÔNG liên quan Hàn Lập.** Cảnh `c1_g08`/`c1_g09`/`c1_g10` (nhẫn rơi → Hàn Lập nhặt trả)
  **phải sửa**. **Người dùng chốt: Cách (a) — bỏ hẳn cảnh nhặt nhẫn**, và
  **viết lại cốt truyện nhánh g cho hợp lý**:
  - Nhẫn **không rơi**. Nhẫn **thức tỉnh / nhận chủ** ở đoạn riêng, không dính Hàn Lập.
  - Hàn Lập gặp người chơi trong tình huống khác (viết mới, hợp mạch).
- **Cân bằng:** tu luyện nhanh gấp 30, nhưng **tốn linh thạch / nguyên liệu** tương ứng.

### 3.5. Nhánh **h (hắc đạo)** — THÔN THIÊN MA CÔNG
- **Bản chất:** **hỗn độn công pháp đỉnh nóc ma đạo thời hồng hoang**.
- **Cơ chế:** **thôn phệ đối phương** để gia tăng cảnh giới; tu luyện công pháp này
  có **thực lực mạnh gấp 10 lần đồng cấp**.
- **Cái giá (người dùng chốt):** thôn phệ nhiều → **sát nghiệp quấn thân** → dần **đánh mất chính mình**.
  Muốn thanh trừ sát nghiệp **phải dùng sấm sét** → **rủi ro bị sét đánh chết nếu không chuẩn bị**.
- **Cân bằng:** mạnh gấp 10 nhưng **nghiệp nặng dần**; thanh trừ phải trả giá (sấm sét, rủi ro chết).

---

## 4. NĂM KẾT RIÊNG (việc E)

Bỏ `c1_d18` dùng chung. Mỗi nhánh có đoạn kết **riêng, không trùng nhau**, gắn với cơ duyên:

| Nhánh | Kết gắn với |
|---|---|
| p | Ngọc cốt — khế ước / hướng tu hành mở ra |
| d | Hồng Trần Kiếm Hạp — nhận chủ, kiếm đầu tiên xuất hiện |
| y | Vô Vạn Thọ Nguyên — nuốt hay giữ? |
| g | Nhẫn ngọc — bước vào dòng thời gian gia tốc lần đầu |
| h | Thôn Thiên Ma Công — bước đầu nhập ma đạo |

---

## 5. THỨ TỰ THỰC HIỆN & KIỂM THỬ

```
Bước 1: Gỡ 4 ràng buộc (chỉ đổi tài liệu, chưa đụng truyện)
Bước 2: Việc A (sửa 2 chỗ lỗi)
Bước 3: Việc B (câu bắc cầu)
Bước 4: Việc C (tách 23 chỗ hội tụ)
Bước 5: Xây 5 cơ duyên — TỪNG NHÁNH MỘT, mỗi nhánh xong thì test
        5a. d (Hồng Trần Kiếm Hạp)
        5b. p (Ngọc cốt)
        5c. y (Vô Vạn Thọ Nguyên)
        5d. g (Nhẫn gia tốc)
        5e. h (Thôn Thiên Ma Công)
Bước 6: Việc E (5 kết riêng)
Bước 7: Chạy 40 test cũ + test mới cho từng cơ duyên
```

**Sau mỗi bước:** chạy `python3 game/_test_api.py` (40 test) để chắc không làm hỏng gì.
**Cách kiểm thử cơ duyên:** kiểm tra (1) nhặt được vật, (2) vật nhắc lại trong truyện,
(3) lựa chọn dùng vật hiện đúng điều kiện, (4) kết gắn với cơ duyên.

---

## 6. QUYẾT ĐỊNH NGƯỜI DÙNG (đã chốt)

| # | Vấn đề | Quyết định |
|---|---|---|
| 1 | Gỡ ràng buộc | **Gỡ cả 4** + mỗi nhánh 1 kết riêng không trùng |
| 2 | Gặp Hàn Lập chương 1 | **Giữ**, nhưng cách gặp **tự nhiên theo từng nhánh** |
| 3 | Mạch cơ duyên | **Xây dựng, không bỏ** — cơ duyên là linh hồn truyện |
| 4 | Mức nội dung ngọc cốt | **Xây rõ hơn** (nhưng vẫn ở mức gợi ý khi viết cảnh thân mật) |
| 5 | Số nhánh xây cơ duyên | **Cả 5 nhánh** |
| 6 | Cơ duyên 3 nhánh | d → **Hồng Trần Kiếm Hạp**; y → **Vô Vạn Thọ Nguyên**; h → **Thôn Thiên Ma Công** |
| 7 | Cách dùng bảo vật | **Bị phong ấn, dùng một phần** (không phá tiến trình) |
| 8 | Cách làm | Từng nhánh một, mỗi nhánh xong thì test |
| 9 | Nhẫn gia tộc | **Không liên quan Hàn Lập**; nhẫn **nhận chủ** khi gặp đúng người có đại cơ duyên. **Chốt: Cách (a)** — bỏ cảnh nhặt nhẫn, **viết lại cốt truyện nhánh g** |
| 10 | Thôn Thiên Ma Công — cái giá | Thôn phệ nhiều → **sát nghiệp quấn thân** → đánh mất mình; thanh trừ **phải dùng sấm sét**, **rủi ro bị sét đánh chết** |
| 11 | Vô Vạn Thọ Nguyên | **Nuốt ngay chương 1** |
| 12 | Ngọc cốt — khế ước | **Ký ngay chương 1** |
| 13 | Hiện cơ duyên | **Để lẫn trong túi**, nhưng **luôn ở vị trí đầu** + **viền đánh bóng nhiều màu** cho nổi bật; **nhấn vào → hiện bảng thông tin cơ duyên** |

---

## 7. GIAO DIỆN CƠ DUYÊN (theo người dùng chốt)

Trong tab **Túi trữ vật** của bảng Hệ Thống:

| Yêu cầu | Chi tiết |
|---|---|
| Vị trí | **Luôn nằm ở đầu danh sách** (trên ngọc vụn, linh thạch…) |
| Nổi bật | **Viền đánh bóng nhiều màu** (gradient/viền phát sáng) |
| Nhấn vào | **Hiện bảng thông tin cơ duyên** — mô tả bảo vật, cơ chế, trạng thái |

**Trạng thái hiển thị** (ví dụ):
- Ngọc cốt — *[phong ấn · chưa khế ước]* → sau khi ký: *[đã khế ước · đang hồi phục]*
- Hồng Trần Kiếm Hạp — *[phong ấn · Luyện Khí: 2 kiếm]*
- Vô Vạn Thọ Nguyên — *[chưa nuốt]* → sau khi nuốt: *[đã dùng · thọ nguyên vô tận]*
- Nhẫn ngọc — *[chưa nhận chủ]* → sau: *[đã nhận chủ · gia tốc 1:30]*
- Thôn Thiên Ma Công — *[chưa tu luyện]* → sau: *[tầng 1 · sát nghiệp 0]*

**Cần làm:** thêm trường `co_duyen` (đánh dấu bảo vật) trong dữ liệu vật phẩm +
CSS viền nhiều màu + JS hiện bảng thông tin khi nhấn.

---

## 8. CÒN CẦN CHỐT

*(Không còn — các quyết định chính đã chốt. Chi tiết nhỏ sẽ hỏi khi thực hiện từng bước.)*
