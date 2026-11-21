# 🎧 Hộp nhận tiếng Xưởng âm thanh

Bỏ file tiếng vào đây, hệ thống tự nén và ghép vào game.

## Cách đúng: dùng trang Xưởng

Mở **https://huuducbkb.github.io/game-hong-duc-lam/xuong-am/** — ở đó có prompt cho
từng cảnh, ô nghe thử, và nút gửi. Trang tự đặt file vào đúng thư mục, anh không phải
đổi tên gì.

## Cách thủ công

Đặt file vào thư mục con mang **mã nhóm tiếng**:

```
xuong-am-inbox/
  cho/    ← file gì cũng được, tên gì cũng được
  tran/
  nui/
  san/
  vuon/
  mieu/
  dem/
  lang/
  tinh/
```

Chỉ cần thư mục đúng mã. Tên file không quan trọng — hệ thống đổi thành `<mã>.mp3`.

## Chín mã nhóm

| mã | cảnh |
|---|---|
| `cho` | chợ |
| `tran` | trận chiến |
| `nui` | núi, đường mòn |
| `san` | sân tập |
| `vuon` | vườn thuốc |
| `mieu` | miếu, chùa |
| `dem` | đêm |
| `lang` | làng, xóm |
| `tinh` | tĩnh, trong nhà |

## Hệ thống làm gì

1. Chuyển mọi định dạng về **mp3 96 kbps**, 44.1 kHz, stereo.
2. Cân âm lượng về **−23 LUFS** (chuẩn phát thanh), đỉnh dưới −2 dB.
3. Lưu vào `docs/assets/am/<mã>.mp3` và `assets/am/<mã>.mp3`.
4. Ghi lại `danh-sach.json` để game biết nhóm nào đã có bản thật.
5. Dọn hộp nhận, commit, deploy.

Nhóm nào chưa có file thì game dùng tiếng tổng hợp sẵn trong máy — **không bao giờ im**.

## Lưu ý

- **Đừng** tự đặt file vào `assets/am/`. Đi qua hộp nhận để còn cân âm lượng.
- File nên dài **30 giây** và **lặp được** (đầu khớp cuối). Nếu không lặp được, chỗ nối
  sẽ nghe thấy một cái "cụp".
- Không có nhạc, không có lời nói rõ nghĩa — xem prompt ở trang Xưởng.
