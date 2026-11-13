# HỒNG ĐỨC TU TIÊN LỘ — Bản đặc tả (SPEC)

> Game AI text tu tiên, thể loại **đồng nhân xuyên không** dựa trên tác phẩm
> **"Phàm Nhân Tu Tiên" của Vong Ngữ**. Phi thương mại, mục đích học tập/cá nhân.

---

## 1. Tổng quan

| Hạng mục | Nội dung |
|---|---|
| Tên game | **Hồng Đức Tu Tiên Lộ** |
| Thể loại | Đồng nhân xuyên không (fan-fiction isekai) |
| Nền tảng | Web (chạy trên trình duyệt) |
| Ngôn ngữ | Tiếng Việt, phong cách tiên hiệp |
| Đối tượng | Người đã biết/đang đọc Phàm Nhân Tu Tiên |
| Người dẫn truyện | AI (Gemini / OpenRouter) đóng vai "Hệ Thống" + dẫn truyện |

---

## 2. Định vị & điểm độc đáo

- Người chơi là **một người xuyên không** vào thế giới Phàm Nhân Tu Tiên,
  **sống cùng thời với Hàn Lập**.
- Người chơi **biết trước cốt truyện gốc** (meta-knowledge) → có thể tận dụng
  để né hiểm, giành cơ duyên, kết giao đúng người.
- **Bám sát nguyên tác (canon)**: các sự kiện lớn của truyện **không thể bị thay đổi**.
  Người chơi chen vào **khoảng trống** giữa các sự kiện đó.
- Có **"Hệ Thống"** hỗ trợ: hiển thị chỉ số, gợi ý nhiệm vụ, nhắc mốc thời gian.

---

## 3. Bối cảnh & mốc thời gian

**Thời điểm bắt đầu: TỰ DO — trước khi Hàn Lập gia nhập Thất Huyền Môn.**

Lý do: người chơi có thể chọn **xuất thân khác nhau** (tán tu, tạp dịch đệ tử
môn phái khác, con nhà nông, đệ tử bang hội…). Vì thế không thể cố định người
chơi "cùng lứa Hàn Lập". Thay vào đó, người chơi **gặp Hàn Lập tại các sự kiện
của thế giới** khi thời cơ đến.

**Cơ chế gặp nhân vật chính:** không gặp ở đầu game. Hàn Lập xuất hiện khi
người chơi chạm tới đúng sự kiện canon (xem "Dòng thời gian sự kiện").

### Dòng thời gian sự kiện (mỗi sự kiện = 1 chương)

> **Phạm vi hiện tại: chỉ làm Chương 1 → 3.** Từ Chương 4 trở đi sẽ **bàn lại**
> để chọn sự kiện bám sát nguyên tác (chưa chốt).

| Chương | Sự kiện canon | Hàn Lập ở đâu | Người chơi có thể |
|---|---|---|---|
| 1 | Đại chiến **Dã Lang Bang** tấn công Thất Huyền Môn | Tạp dịch đệ tử Thất Huyền Môn | Lần đầu chạm mặt Hàn Lập (tùy xuất thân) |
| 2 | **Huyết Sát Thí Luyện** | Trong môn phái | Chen vào thí luyện, tranh cơ duyên |
| 3 | **Đêm đại chiến trong Hoàng Cung** — diệt **Hắc Sát Giáo** | Tham gia | Chọn phe, cứu/giết, đoạt bảo |
| 4+ | *(chưa chốt — sẽ trao đổi với người dùng)* | — | — |

**Thế lực & nhân vật chính thống:** Hàn Lập, Lệ Phi Vũ, Nam Cung Uyển,
Mặc Đại Phu, Trương Thiết, Đổng Huyên Nhi, Nguyên Dao, Hải Đại Thiếu, Khúc Hồn…

---

## 4. Nhân vật người chơi

- Là người hiện đại **xuyên không** vào thân xác một người trong thế giới Phàm Nhân.
- **Có "Hệ Thống"** (bàn tay vàng) — khác với Hàn Lập (chỉ có Tiểu Bình).
- **Quan hệ với Hàn Lập: do người chơi chọn** — đồng minh / đối thủ / người dưng.
- Người chơi đặt tên nhân vật khi bắt đầu.

### Xuất thân (người chơi TỰ QUYẾT ĐỊNH — hoàn toàn tự do)

Người chơi **tự nhập xuất thân** bằng chữ, không bị giới hạn trong danh sách cứng.
Ví dụ (chỉ để gợi ý, không bắt buộc): tán tu, tạp dịch đệ tử môn phái khác,
con nhà nông, đệ tử bang hội, thương nhân, thợ săn, dược đồng…

Hệ thống sẽ **tự suy luận** từ mô tả xuất thân để quyết định:
- Điểm khởi đầu (nơi ở, tài nguyên ban đầu)
- Cách người chơi gặp Hàn Lập về sau
- Ưu/nhược riêng

> Ghi chú kỹ thuật: ô nhập xuất thân là **văn bản tự do**; AI + Hệ thống diễn giải.
> Nếu bỏ trống, mặc định là "tán tu vô danh".

---

## 5. Hệ thống (bàn tay vàng)

- Hiển thị **bảng chỉ số** (cảnh giới, tu vi, HP, linh thạch, túi đồ).
- **Nhiệm vụ / gợi ý** theo mốc canon (ví dụ: "3 ngày nữa Hoàng Phong Cốc khai mở…").
- **Cảnh báo nguy hiểm** dựa trên meta-knowledge.
- Không cho phép phá vỡ canon (xem mục 7).

---

## 6. Cơ chế chơi (game loop)

```
[Hệ thống gợi ý tình huống]
        ↓
Người chơi chọn:  (a) gõ hành động tự do   (b) bấm lựa chọn A/B/C
        ↓
AI (Hệ thống) kể diễn biến + quyết định kết quả
        ↓
Cập nhật chỉ số (tu vi, HP, linh thạch, vật phẩm)
        ↓
Hiển thị ảnh minh họa  (+ video ngắn nếu là khoảnh khắc lớn)
        ↓
[Chuyển sang tình huống tiếp theo]
```

- **Hai cách nhập**: gõ tự do **và** nút lựa chọn A/B/C (kết hợp cả hai).
- **Mục tiêu dài hạn: do người chơi chọn** (tu thành Chân Tiên / sống sót /
  xây thế lực / thay đổi số phận nhân vật phụ…).

---

## 7. Luật canon & meta-knowledge

| Luật | Nội dung |
|---|---|
| Bám canon | Sự kiện lớn **không đổi**: Hàn Lập vẫn nhận Tiểu Bình, vẫn tiến cảnh giới theo nguyên tác… |
| Vùng tự do | Người chơi tự do hành động **giữa** các sự kiện canon |
| Meta-knowledge | Người chơi **được dùng** hiểu biết nguyên tác để làm lợi thế |
| Hệ quả | Nếu người chơi cố phá canon → AI kể thất bại hợp lý (thiên đạo cản trở) |

---

## 8. Cảnh giới & chỉ số (theo nguyên tác)

**Cảnh giới:** Luyện Khí (13 tầng) → Trúc Cơ → Kết Đan → Nguyên Anh → Hóa Thần
→ Luyện Hư → Hợp Thể → Đại Thừa → Độ Kiếp → Chân Tiên.

**Chỉ số:** tu vi, khí huyết (HP), công kích, linh thạch, pháp lực,
túi đồ (đan dược, pháp bảo, bùa, bí kíp).

---

## 9. Nghề phụ (sẽ phát triển ở giai đoạn sau)

- **Luyện đan** — thành công → video ngắn
- **Luyện khí (rèn vũ khí/pháp bảo)** — thành công → video ngắn
- **Vẽ bùa** — thành công → video ngắn

---

## 10. Ảnh & video (phương án C)

| Loại | Cách làm | Chi phí |
|---|---|---|
| **Ảnh minh họa** | Python vẽ **SVG** theo bối cảnh (núi, biển, động phủ, tuyết sơn, chiến trường…) | 🆓 Miễn phí |
| **Video ngắn** | Hiệu ứng **cinematic CSS** (ken-burns, rung lắc khi giao chiến, hào quang khi đột phá…) | 🆓 Miễn phí |

**Video ngắn xuất hiện ở các khoảnh khắc:**
1. Đột phá cảnh giới
2. Luyện đan thành công
3. Luyện vũ khí/pháp bảo thành công
4. Vẽ bùa thành công
5. Đại chiến
6. Lần đầu gặp Hàn Lập
7. Độ kiếp

**Ảnh minh họa:** hiển thị **mỗi lượt** (miễn phí, không tốn token).

---

## 11. Chi phí token (quan trọng)

| Thành phần | Gọi API? | Tốn token? |
|---|---|---|
| Ảnh SVG | Không | 🆓 Không |
| Video cinematic | Không | 🆓 Không |
| AI kể chuyện (mỗi hành động) | Có | 💰 Có (1 lần/lượt) |

→ Ảnh mỗi lượt **không tốn gì**. Chỉ AI kể chuyện tốn token.
Có sẵn **chế độ không AI** để chơi thử miễn phí.

---

## 12. Giao diện (3 cột)

```
┌──────────────┬───────────────────────────┬──────────────────┐
│  NHÂN VẬT    │        CÂU CHUYỆN          │   HÌNH ẢNH       │
│  Tên, danh   │  Khung truyện cuộn        │  Ảnh bối cảnh    │
│  hiệu        │  (Hệ thống kể lại)        │  (SVG)           │
│  Cảnh giới   │                           │                  │
│  Tu vi bar   │  ─ Ô nhập hành động ─     │  Video ngắn      │
│  HP bar      │  ─ Nút chọn A/B/C ─       │  (cinematic)     │
│  Túi đồ      │                           │  Tên bối cảnh    │
└──────────────┴───────────────────────────┴──────────────────┘
```

Phong cách: nền tối (mực đen), điểm nhấn **vàng kim + xanh ngọc**, chữ thư pháp,
hiệu ứng sương mù trôi.

---

## 13. Kiến trúc kỹ thuật

```
FRONTEND (HTML/CSS/JS)  ←→  BACKEND (Python FastAPI)  ←→  LLM (Gemini/OpenRouter)
                                     │
                                     ├── SQLite (lưu nhân vật + lịch sử)
                                     ├── SVG generator (ảnh, offline)
                                     └── Cinematic CSS (video, offline)
```

**API:** `/api/new` (tạo nhân vật) · `/api/action` (hành động) ·
`/api/state` (trạng thái) · `/api/image` (ảnh SVG) · `/api/status` (cấu hình).

---

## 14. Lộ trình — chia theo CHƯƠNG

Nguyên tắc: làm từng chương một, chơi thử xong mới sang chương kế.
**Phạm vi hiện tại: Chương 1 → 3.** Chương 4+ sẽ bàn lại.

**Chương 1 — Khởi nguyên & gặp Hàn Lập** *(MVP)*
- Tạo nhân vật: đặt tên + **nhập xuất thân tự do**
- Bảng chỉ số + Hệ Thống + cảnh giới chuẩn nguyên tác (Luyện Khí 13 tầng…)
- Cơ chế chơi: gõ tự do **+** chọn A/B/C
- AI dẫn truyện + ảnh SVG mỗi lượt
- **Sự kiện: Đại chiến Dã Lang Bang** → lần đầu chạm mặt Hàn Lập
- Video cinematic: đột phá cảnh giới · đại chiến · gặp Hàn Lập

**Chương 2 — Huyết Sát Thí Luyện**
- Bối cảnh thí luyện trong môn phái, tranh cơ duyên
- NPC đồng môn, đối thủ, nguy hiểm chết người

**Chương 3 — Đêm đại chiến Hoàng Cung (diệt Hắc Sát Giáo)**
- Chọn phe, cứu/giết, đoạt bảo
- Nhân vật canon: Hàn Lập, Mặc Đại Phu…

**Chương 4+** — *(chưa chốt, sẽ trao đổi)*

**Song song / sau này — Nghề phụ**
- Luyện đan · luyện khí · vẽ bùa (thành công → video ngắn)
- Nhiệm vụ, quan hệ nhân vật, thế lực, lưu nhiều nhân vật

---

## 15. Bản quyền

Đây là sản phẩm **đồng nhân (fan-fiction) phi thương mại** dựa trên
**"Phàm Nhân Tu Tiên" của tác giả Vong Ngữ**. Ghi rõ nguồn gốc, không dùng
cho mục đích thương mại.
