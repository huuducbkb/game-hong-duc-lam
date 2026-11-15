# Ý tưởng 3 nhánh chưa xây (dược đồng · gia tộc · hắc đạo)

Ngày 2026-11-12: gỡ 3 nhánh này khỏi game để **chỉ còn 2 nhánh hoàn chỉnh**
(tán tu, môn phái). Người dùng một mình không test hết 5 nhánh; 3 nhánh kia
chưa xong (còn lỗi canon + chưa có cơ duyên riêng + dùng chung đoạn kết cũ).

Giữ lại ý tưởng ở đây để **xây lại sau** khi rảnh.

## Bản lưu dữ liệu cũ

- `docs/luu-tru/chuong1-3-nhanh-chua-xay.json` — 41 đoạn + 3 nhóm xuất thân
  (bản thảo cũ, để tham khảo khi viết lại — KHÔNG dùng trực tiếp vì còn lỗi).

## 3 nhánh — ý tưởng đã chốt

| Nhánh | Cơ duyên | Cơ chế | Trạng thái |
|---|---|---|---|
| **Dược đồng** | Vô Vạn Thọ Nguyên (1 viên đan) | **Vô hạn thọ nguyên** → đốt thọ nguyên tăng tu vi (nhánh khác đốt là chết) | ⏳ chưa xây |
| **Gia tộc** | Nhẫn ngọc (thức tỉnh nhận chủ) | Tu luyện nhanh **30×**, tốn **bạc**; **không** rơi gần Hàn Lập | ⏳ chưa xây |
| **Hắc đạo** | Thôn Thiên Ma Công (nuốt để mạnh) | Mạnh **10×** nhưng tích **sát nghiệp** → mất bản ngã; cứu bằng **lôi kiếp** | ⏳ chưa xây |

Chi tiết đầy đủ (bảng chỉ số, mức nội dung, lỗi canon cần sửa) ở
`docs/KE-HOACH-SUA-CHUONG-1.md`.

## Còn nợ khi xây lại (4 bước mỗi nhánh)

1. **Cơ duyên riêng** trong truyện (chưa có cảnh nhận).
2. **Sửa lỗi canon**: `linh thảo`, `Trúc Cơ`… (xem `KE-HOACH-SUA-CHUONG-1.md`).
3. **Đoạn kết riêng** cho từng nhánh (không dùng chung `c1_d18` — đã xoá).
4. **Không có HỆ THỐNG** + không biết xuyên không (3 nhánh này là **bản địa**).

> Nhánh **tán tu** và **môn phái** đã xong, dùng làm **chuẩn mẫu** khi viết lại.

## Cách bật lại (khi xây xong)

1. Thêm lại nhóm vào `game/xuat_than.json` (bỏ cờ ẩn nếu có).
2. Thêm lại các đoạn vào `game/chapters/chuong1.json`.
3. Chạy `python3 game/_test_api.py` — bổ sung test cho nhánh mới.
