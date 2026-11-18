# 📥 Hộp nhận ảnh Xưởng

Bỏ ảnh đã vẽ vào đây (mọi tên file đều được), hệ thống sẽ tự xử lý.

## Hai cách đưa ảnh vào

### Cách 1 — Dán ảnh vào Issue (nhanh nhất)
1. Mở [trang tạo Issue](https://github.com/huuducbkb/game-hong-duc-lam/issues/new).
2. Tiêu đề bất kỳ, **kéo tất cả ảnh vào ô nội dung** rồi bấm **Submit new issue**.
3. Gắn nhãn `xuong-anh` cho Issue (nếu có).

Hệ thống tự nhận diện ảnh nào ở đâu rồi trả lời trong Issue.

### Cách 2 — Tải ảnh lên thư mục này
Bấm [mở trang tải lên](https://github.com/huuducbkb/game-hong-duc-lam/upload/main/xuong-inbox),
kéo ảnh vào rồi **Commit changes**.

> Mẹo: muốn chắc 100% thì đặt ảnh vào thư mục con mang mã ảnh, ví dụ
> `xuong-inbox/bc_dot_pha/bat-ky.png` — hoặc đặt tên file có chứa mã ảnh.

## Hệ thống làm gì sau đó
1. Nhận diện mỗi ảnh ứng với prompt nào (theo tên file → thư mục → AI).
2. Nén ảnh và lưu vào `assets/` + `docs/assets/`.
3. Ghép ảnh vào đúng đoạn trong Chương 1.
4. Cập nhật thư viện ảnh + dựng lại Xưởng + deploy web.

Ảnh nào AI không chắc sẽ **để lại** và báo trong Issue để bạn xác nhận.
