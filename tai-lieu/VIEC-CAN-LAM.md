# Việc cần làm — Hồng Đức Tu Tiên Lộ

> **Sổ việc sống.** Cập nhật mỗi khi có việc mới hoặc xong việc.
> Quy ước: `[ ]` chưa làm · `[~]` đang làm · `[x]` xong.
> Cập nhật lần cuối: **2026-11-17**

---

## 🔴 ĐANG LÀM

- [~] **Phần ảnh — bước 2: 14 ảnh cảnh đợt 1 (nhánh tán tu)**
  - [x] **4 ảnh mẫu đã xong** ✓ (đã kiểm tra: đúng tên, tỷ lệ 3:4, đúng canon)
  - [x] **Chia 7 nhóm + nút copy riêng** ✓ (PR #29 merged, commit `4b9ae0a`)
        mỗi nhóm ghi rõ đính kèm ảnh mẫu nào → giữ mặt nhân vật đều
  - [x] **Thư viện ảnh mẫu** ✓ (PR #30 merged, commit `19923e0`)
        lưới 9 ảnh mẫu, xem + tải về để đính kèm
  - [~] **→ Người dùng: mở Xưởng, vẽ từng nhóm, upload lại** (xem hướng dẫn bên dưới)
        Nhóm 1 đã upload xong và **đã ghép vào game**; còn 6 nhóm (11 ảnh) chờ vẽ.
  - [~] Agent: ghép 14 ảnh vào game khi đủ — đã ghép nhóm 1 (3 ảnh)
  - **Tiến độ 14 ảnh: 3/14 (3 ảnh đã ghép vào game)**
    - [x] **Nhóm 1 — Phong cảnh (3/3)** ✓ (PR #31 merged, commit `79b30ed`)
          bc_cho_02 · bc_cho_03 · bc_mieu_trong — khớp cảnh 95/100, phong cách 90/100, không chữ
          **Đã ghép (commit `<GHÉP>`):** `bc_cho_02`→`c1_d02` · `bc_cho_03`→`c1_d02b` ·
          `bc_mieu_trong`→`c1_d04b`; cập nhật `docs/assets/library/index.json`
    - [ ] Nhóm 2 — Đồ vật hộp kiếm (0/1): vt_kiem_hap_nhan
    - [ ] Nhóm 3 — Nhân vật chính (0/3): bc_dot_pha · bc_tran_lua_2 · bc_tran_lua_3
    - [ ] Nhóm 4 — Kiếm linh (0/3): nv_kiem_linh_thu · nv_kiem_linh_than · nv_kiem_linh_dieu
    - [ ] Nhóm 5 — Đỗ Tam (0/2): nv_do_tam_mieu · bc_doat_hop
    - [ ] Nhóm 6 — NV chính + Kiếm linh (0/1): bc_tu_khiem
    - [ ] Nhóm 7 — Hàn Lập (0/1): nv_han_lap_2

---

## ✅ VỪA XONG — Ghép 3 ảnh nhóm 1 vào game

- [x] Ghép 3 ảnh phong cảnh vào đúng đoạn theo `use` trong Xưởng:
      `bc_cho_02`→`c1_d02` · `bc_cho_03`→`c1_d02b` · `bc_mieu_trong`→`c1_d04b`
- [x] Cập nhật `docs/assets/library/index.json`: thêm 3 mục mới, sửa `dung_o`
      (`bc_cho_01` bỏ `c1_d02`/`c1_d02b`; `bc_mieu_hoang` bỏ `c1_d04b`)
- [x] Sửa ảnh gán sai `c1_p19` (kết chương) → `bc_binh_minh` (thay `vt_ngoc_cot`)
- [x] Đồng bộ `game/chapters/chuong1.json` **và** `docs/game/du-lieu/chuong1.json`
- [x] Engine test **105/105** · API test **161/161**

---

## ✅ VỪA XONG — Nhóm 1 phong cảnh (PR #31)

- [x] Nhận 3 ảnh: `bc_cho_02` · `bc_cho_03` · `bc_mieu_trong` (900×1200, 3:4 ✓)
- [x] AI vision: khớp cảnh 95/100, phong cách 90/100, không chữ
- [x] Lưu cả `assets/` và `docs/assets/`

---

## ✅ VỪA XONG — Thư viện ảnh mẫu (PR #30)

- [x] Mục **📚 Thư viện ảnh mẫu**: lưới 9 ảnh, mỗi ảnh có xem trước + tên + badge + nút tải
- [x] Đường dẫn tuyệt đối `/assets/scene/...` (không hỏng khi URL có `/` cuối)
- [x] Engine test **105/105** · API test **161/161**

---

## ✅ VỪA XONG — Chia nhóm ảnh đợt 1 (PR #29)

- [x] 14 ảnh đợt 1 chia **7 nhóm theo nhân vật**, mỗi nhóm 1 nút Copy + tải .txt
  - Prompt nhóm có khối `ATTACHED REFERENCE IMAGE(S)` nhắc AI giữ mặt/tóc/áo
- [x] Engine test **105/105** · API test **161/161**
- [x] Xưởng: 7 thẻ nhóm hiển thị, 0 placeholder sót, ngữ pháp đúng

---

## ✅ VỪA XONG — Nhận 4 ảnh mẫu tham chiếu

- [x] 4 ảnh mẫu vào `assets/scene/` + `docs/assets/scene/` (commit `0ceacd7`)
  - `nv_chinh_mau` · `nv_mac_dai_phu_mau` · `nv_do_tam_mau` · `nv_hung_ba_mau`
  - Kiểm tra: 900×1200 (3:4 ✓) · AI xác nhận đúng canon + đúng dạng ảnh mẫu (1 nhân vật, nền trống)
- [x] **9 ảnh mẫu sẵn sàng** = 4 mới + 5 cũ (Tuyết Cơ, Hàn Lập, Kiếm linh, Ngọc cốt, Hộp kiếm)
- [x] Phân tích: 14 ảnh đợt 1 chia **6 nhóm theo nhân vật** (để đính kèm đúng ảnh mẫu)

---

## ✅ VỪA XONG — Thêm prompt ảnh vào Xưởng

- [x] Xưởng (`tools_server.py`): thêm **18 asset mới** (4 ảnh mẫu + 14 ảnh đợt 1)
  - Tổng ASSETS: 19 → **37**
  - 2 khối mới **lên đầu trang** + 2 nút copy + 2 nút tải .txt
- [x] Engine test **105/105** · API test **161/161** (test nén ảnh nay cũng đạt)
- [x] Đã khôi phục 2 ảnh thật bị API test ghi đè (`bc_cho_01`, `divider-ink`)

---

## ✅ VỪA XONG — Đẩy văn lên web

- [x] PR **#27** merged (commit `e530a3a`): sửa văn trùng Chương 1 + bảng canon + sổ việc
  - Đã kiểm chứng web thật: `p05c`/`p19` là bản mới, **0 đoạn** còn câu mơ cũ
  - GitHub Pages deploy: **success**
  - URL game: https://huuducbkb.github.io/game-hong-duc-lam/game/play.html

---

## 🟡 CHỜ LÀM — ẢNH (mỗi cảnh 1 ảnh riêng)

- [x] **Bảng canon nhân vật & đồ vật** — `tai-lieu/CANON-NHAN-VAT-DO-VAT.md`
- [~] **Ảnh mẫu tham chiếu** (vẽ 1 lần, dùng lại cho mọi chương sau)
  - [ ] 4 ảnh mẫu cần vẽ: nhân vật chính · Mạc Đại Phu · Đỗ Tam · Hùng Bá
- [ ] **51 ảnh cảnh Chương 1** (63 cảnh − 12 ảnh đã có), chia 6 đợt
  - [~] **Đợt 1 — nhánh tán tu: 14 ảnh** (prompt đã sẵn trong Xưởng)
  - [ ] Đợt 2 — nhánh tán tu còn lại
  - [ ] Đợt 3 — môn phái: sân tập, vườn thuốc
  - [ ] Đợt 4 — môn phái: hậu sơn, ngọc cốt (Tuyết Cơ)
  - [ ] Đợt 5 — môn phái: tân xá, khổ tu
  - [ ] Đợt 6 — môn phái: cổng đông, Hàn Lập
- [ ] Sửa ảnh gán sai: `c1_p19` (kết chương) → `bc_binh_minh` (thay `vt_ngoc_cot`)
      → [x] **ĐÃ SỬA** (xem "VỪA XONG — Ghép 3 ảnh nhóm 1 vào game")

---

## 🟢 ĐÃ XONG

- [x] **Sửa văn trùng Chương 1** — 8 đoạn viết lại (`c1_p03e`, `c1_p05c`, `c1_p06b`,
      `c1_p03d`, `c1_p05b`, `c1_p06`, `c1_p17`, `c1_p19`). Quét trùng: **5 cặp → 0 cặp**.
      Engine test 105/105 · API test 160/161 (1 test nén ảnh hỏng sẵn, không liên quan).
- [x] **Bảng canon nhân vật & đồ vật** — `tai-lieu/CANON-NHAN-VAT-DO-VAT.md`
      (7 nhân vật + 5 đồ vật + bối cảnh + quy tắc bất di bất dịch)
- [x] **Xoá kế hoạch viết lại** (`KE-HOACH-SUA-CHUONG-1.md`) — người dùng chốt
      **giữ hướng hiện tại**, không viết lại. Đã bảo tồn: khung 7 giai đoạn + chi tiết
      3 nhánh chưa xây → chuyển vào `Y-TUONG-3-NHANH-CHUA-XAY.md`
- [x] **Sổ việc** — `tai-lieu/VIEC-CAN-LAM.md` (file này)
- [x] Ghép 8 ảnh nhánh tán tu vào game — PR #24
- [x] Sửa Xưởng cảnh báo ảnh chưa gán prompt — PR #25
- [x] Ghép 4 ảnh tán tu cuối — đủ 12/12 ảnh truyện — PR #26

---

## ⏸️ ĐÃ QUYẾT — không còn là "chưa quyết"

- [x] ~~Kế hoạch viết lại Chương 1~~ → **HUỶ** (người dùng chốt 2026-11-17).
      Hướng hiện tại (2 nhánh: tán tu + môn phái) là **đúng**, tiếp tục phát triển.
- [ ] 3 nhánh dược đồng / gia tộc / hắc đạo — đã gỡ, xây lại sau
      (`tai-lieu/Y-TUONG-3-NHANH-CHUA-XAY.md` — đã bổ sung khung 7 giai đoạn + chi tiết cơ duyên)

---

## 📌 QUYẾT ĐỊNH ĐÃ CHỐT (không hỏi lại)

| Ngày | Quyết định |
|---|---|
| 2026-11-17 | **Mỗi cảnh = 1 ảnh riêng** — không dùng lại ảnh giữa các cảnh |
| 2026-11-17 | Cùng nhân vật nhưng **khác tư thế / biểu cảm** ở mỗi cảnh |
| 2026-11-17 | Nhân vật & đồ vật phải **nhất quán qua các chương** → dùng bảng canon + ảnh mẫu tham chiếu |
| 2026-11-17 | **Sửa văn trước**, ảnh sau |
| 2026-11-17 | Ảnh phải **thay được từng tấm** khi cần (tên file tách rời code) |
| — | Repo `huuducbkb/game-hong-duc-lam` public, deploy GitHub Pages |
| — | Người chơi dùng Safari (iPad/iPhone), **không có terminal** → mọi thao tác qua web |
| — | **Không tự thêm tính năng** — bàn trước khi làm |

---

## 📋 QUY TRÌNH THÊM ẢNH (đã chốt, dùng lại mỗi lần)

1. AI soạn **prompt gộp** (kèm ảnh mẫu tham chiếu nếu có)
2. Người dùng dán vào Gemini → vẽ ra
3. Người dùng tải lên **Xưởng** (`/upload`)
4. AI ghép vào game → đồng bộ `assets/scene/` **và** `docs/assets/scene/`
5. Cập nhật `docs/assets/library/index.json` (ghi `dung_o`)
6. Commit → PR → merge → deploy GitHub Pages → kiểm tra HTTP 200
