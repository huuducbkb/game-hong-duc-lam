# KẾ HOẠCH: Chuyển game sang JS chạy trên GitHub Pages (Hướng B)

> Trạng thái: **CHỜ NGƯỜI DÙNG DUYỆT** — chưa code dòng nào.
> Ngày lập: 2026-11-15
> Mục tiêu: game chơi được trên GitHub Pages (link vĩnh viễn), **giữ gõ tự do AI**
> bằng cách để **mỗi người chơi tự nhập key Gemini của họ**.

---

## 1. Vì sao làm được (đã kiểm chứng)

| Điều kiện | Kết quả kiểm tra |
|---|---|
| Gemini cho trình duyệt gọi thẳng (CORS) | ✅ `access-control-allow-origin` trả về đúng |
| Engine không dùng `random` | ✅ Chơi lại cho kết quả y hệt |
| Dữ liệu là JSON thuần | ✅ `chuong1.json` (111 KB) + `xuat_than.json` (2 KB) |
| Có Node.js để test | ✅ Node v24.22.1 |
| Có 139 test sẵn để đối chiếu | ✅ `game/_test_api.py` |

---

## 2. Nguyên tắc (chốt trước khi làm)

1. **Key của AI do NGƯỜI CHƠI tự nhập** — không nhúng key của bạn vào code.
2. **Key lưu trong máy người chơi** (localStorage), không gửi đi đâu ngoài Google.
3. **Không sửa dữ liệu truyện** — dùng chung `chuong1.json` + `xuat_than.json`.
4. **Bản Python giữ nguyên** — không xoá, để còn chơi bản đầy đủ (có server).
5. **Chưa gộp vào `main`** cho tới khi bạn chơi thử thấy ổn.

---

## 3. Cần làm gì (5 phần)

### Phần A — Dịch engine sang JavaScript

Dịch `game/engine.py` (590 dòng) → `docs/game/engine.js`.

| Hàm Python | Việc khi dịch |
|---|---|
| `load_xuat_than`, `ds_xuat_than` | Đọc JSON (thay `open()` bằng `fetch`) |
| `_khong_dau` | `normalize("NFD")` + bỏ dấu — JS làm được |
| `nhan_dien_xuat_than` | Dịch thẳng |
| `trang_thai_moi` | Dịch thẳng (giữ nguyên chỉ số) |
| `_dieu_kien_hop`, `_gap_npc`, `_doi_hao_cam` | Dịch thẳng |
| `_ap_hieu_ung`, `_thang_cap` | Dịch thẳng |
| `chon`, `hanh_dong_tu_do`, `_chuyen_doan` | Dịch thẳng |
| `luu`, `nap` | Đổi từ **file** sang **localStorage** |
| `_man_ket_chuong`, `_goi_y`, `_trang_thai_gon` | Dịch thẳng |

**Ước lượng:** ~400 dòng JS.

### Phần B — Dịch phần AI sang JavaScript

Dịch `game/ai.py` (276 dòng) → `docs/game/ai.js`.

| Hàm | Việc |
|---|---|
| `_goi_gemini` | `fetch()` tới Gemini, key lấy từ localStorage |
| `ke_lai_tien_hiep` | Dịch prompt (giữ nguyên câu chữ) |
| `nhan_dien` | Dịch prompt + lọc JSON |
| `_tach_json` | Dịch thẳng |

**Quan trọng:** giữ **nguyên văn** các prompt để AI trả lời giống bản Python.

### Phần C — Sửa giao diện `play.html`

| Việc | Chi tiết |
|---|---|
| Bỏ gọi `/api/*` | Đổi thành gọi thẳng `engine.js` |
| Thêm **ô nhập key Gemini** | Ở màn đầu hoặc nút "⚙️ Cài đặt" |
| Nút "AI kể" giữ nguyên | Nhưng nếu **chưa có key** → tự tắt + ghi chú |
| Ghi chú cho người chơi | "Cần key Gemini riêng để gõ tự do" + link hướng dẫn tạo key |

### Phần D — Test

1. Chạy **139 test cũ** trên bản JS (dùng Node) → phải **đạt hết**.
2. Test riêng: chưa có key → game vẫn chơi được (chỉ bấm lựa chọn).
3. Test: có key → gõ tự do hoạt động.
4. Test trên Safari (bạn tự thử).

### Phần E — Đưa lên Pages

1. Đặt file vào `docs/game/` (Pages tự phục vụ).
2. Thêm nút **"🎮 Chơi game"** vào `docs/index.html`.
3. Tạo nhánh mới + PR → bạn duyệt → gộp.

---

## 4. Cấu trúc file sau khi làm

```
docs/
├── index.html              ← thêm nút "Chơi game"
├── ban-thao/               ← giữ nguyên (đọc truyện)
└── game/                   ← MỚI
    ├── play.html           ← giao diện (sửa từ game/play.html)
    ├── engine.js           ← luật game (dịch từ engine.py)
    ├── ai.js               ← gọi Gemini (dịch từ ai.py)
    ├── du-lieu/
    │   ├── chuong1.json    ← copy (hoặc symlink) từ game/chapters/
    │   └── xuat_than.json  ← copy từ game/
    └── style.css           ← nếu cần
```

---

## 5. Điều sẽ MẤT khi dùng bản JS (bạn cần biết trước)

| Mất gì | Vì sao | Có bù được? |
|---|---|---|
| Lưu game trên server | Không có server | Lưu trong **localStorage** của Safari |
| Save dùng chung giữa máy | Mỗi máy lưu riêng | Không bù được (tính năng này) |
| Gõ tự do **không cần key** | Không có server giữ key | Người chơi **tự nhập key** |
| "Xưởng ảnh" (`/keys`, `/upload`) | Cần server | **Không có** trên bản Pages |

---

## 6. Điều được

| Được gì | Chi tiết |
|---|---|
| **Link vĩnh viễn** | `huuducbkb.github.io/game-hong-duc-lam/game/` |
| **Không cần server** | Không lo máy ảo tắt |
| **Chơi offline** | Sau khi tải, không cần mạng (trừ phần AI) |
| **Key an toàn** | Không có key của bạn trong code |
| **Nội dung luôn khớp** | Dùng chung file JSON với bản Python |

---

## 7. Thứ tự làm & cách bạn duyệt

```
Bước 1: Tôi dịch engine.js  ─┐
Bước 2: Tôi dịch ai.js       ├─ làm trên NHÁNH RIÊNG
Bước 3: Tôi sửa play.html    │  (chưa động vào main)
Bước 4: Chạy 139 test       ─┘
Bước 5: Tạo PR → bạn xem + chơi thử
Bước 6: Bạn OK → gộp vào main → Pages tự deploy
```

**Bạn sẽ được duyệt ở Bước 5** — trước khi lên `main`.

---

## 8. Câu hỏi cần bạn trả lời TRƯỚC khi tôi code

1. **Đặt game ở đâu trên Pages?** Tôi đề xuất `.../game-hong-duc-lam/game/`
   (hoặc bạn muốn đường khác?)

2. **Ô nhập key để ở đâu?**
   - (a) Ngay màn đầu (thấy liền)
   - (b) Trong nút "⚙️ Cài đặt" (gọn hơn)

3. **Chưa có key thì sao?** Tôi đề xuất: vẫn chơi được (bấm lựa chọn),
   chỉ **ẩn** ô gõ tự do + ghi chú "cần key Gemini để gõ tự do". Đúng ý bạn?

4. **Có cần giữ "Xưởng ảnh" trên bản Pages không?** (Tôi đề xuất: **không** —
   để bản server giữ.)

5. **Có giữ nguyên bản Python** để bạn vẫn chơi bản đầy đủ? (Tôi đề xuất: **có**.)

---

## 9. Rủi ro & cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Dịch sai logic | Chạy 139 test đối chiếu — sai là bắt được ngay |
| Safari cache bản cũ | Thêm ghi chú "tải lại trang" + đặt tên file có số phiên bản |
| Người chơi không biết lấy key | Thêm link hướng dẫn + ảnh minh hoạ trong màn cài đặt |
| Gemini đổi model | Giữ danh sách model dự phòng như bản Python |
