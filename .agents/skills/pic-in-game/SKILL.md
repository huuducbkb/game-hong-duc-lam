---
name: pic-in-game
description: Quy trình PIC-IN-GAME — đưa ảnh và video do AI bên ngoài tạo vào game/giao diện web. Ghép ảnh khung bằng kỹ thuật border-image (không méo nét vẽ), tách nền alpha, dựng video ngắn bằng cách ghép nhiều ảnh + hiệu ứng CSS (kiểu intro CapCut). Kèm đo đạc bằng Pillow và kiểm chứng bằng ảnh chụp trình duyệt. Dùng khi cần thiết kế giao diện, tạo hình ảnh, dựng video ngắn, xây thư viện ảnh/video cho game, hoặc khi API sinh ảnh bị chặn/hết credit. Kích hoạt khi người dùng nói "làm giao diện", "ghép ảnh", "thiết kế UI", "ảnh nền", "video ngắn", "cinematic", "thư viện ảnh", "pic-in-game".
triggers:
- giao diện
- ghép ảnh
- thiết kế UI
- thiết kế giao diện
- ảnh nền
- video ngắn
- cinematic
- thư viện ảnh
- pic-in-game
---

# Quy trình PIC-IN-GAME

**Tên:** PIC-IN-GAME — *Pic-in-Game Method*
**Tên tiếng Việt:** Phương pháp đưa ảnh vào game
**Một câu:** Biến ảnh do AI bên ngoài vẽ thành giao diện web thật, **không méo nét vẽ**, có đo đạc và kiểm chứng — thay vì đoán mò CSS.

## Khi nào dùng

- Cần giao diện / hình ảnh / video ngắn nhưng **API sinh ảnh không dùng được**
  (free tier chặn, hết credit, không có key).
- Người dùng có **một công cụ AI tạo ảnh riêng** và sẵn sàng tự vẽ rồi gửi ảnh lại.
- Ảnh tài nguyên là **tranh vẽ tay / thủy mặc / khung viền có nét mực** — thứ mà
  kéo giãn CSS thông thường sẽ làm méo.
- Dựng **video ngắn kiểu cinematic** bằng CSS animation (không cần file video).

## Vì sao cần quy trình này

Hai cái bẫy thường gặp:

1. **Kéo giãn ảnh khung làm méo nét mực.** `background-size:100% 100%` bóp méo viền vẽ tay.
   → Cách đúng: `border-image`, cắt 4 góc + 4 cạnh, chỉ giãn phần giữa.
2. **Đoán số liệu CSS bằng mắt.** Không biết viền dày bao nhiêu, ruột sáng hay tối,
   slice bằng bao nhiêu → ghép sai, chữ đè lên nét mực.
   → Cách đúng: **đo bằng Pillow** (mật độ mực, độ sáng), rồi mới viết CSS.

## 5 bước

### 1. PROMPT — viết prompt gửi công cụ AI ngoài
- Viết prompt **chi tiết, tách từng tài nguyên một**: nền, khung bảng, nút, viền avatar, ấn son.
- Ghi rõ: tỷ lệ khung, "nền giấy sáng, ruột khung để trống để đặt chữ", "viền mực đều 4 cạnh".
- Cho người dùng một trang web (Xưởng) có sẵn prompt để **copy** + ô **upload** ảnh trả về.
- Nếu chưa có Xưởng: dựng bằng `http.server` + một trang HTML nhỏ, hoặc dùng lại
  `tools_server.py` của dự án này làm mẫu.

### 2. NHẬN ẢNH — nhận và kiểm kê
- Nhận ảnh người dùng upload, lưu vào `assets/ui/` (giữ bản gốc ở `assets/ui-orig/`).
- Kiểm kê: đủ tài nguyên chưa, kích thước bao nhiêu, tài nguyên nào còn thiếu.

### 3. ĐO — đo bằng Pillow trước khi viết CSS
- **Viền khung dày bao nhiêu:** quét hàng/cột giữa ảnh, tìm dải điểm tối (L<150).
- **Ruột khung sáng hay tối:** lấy trung bình độ sáng vùng giữa → quyết định màu chữ.
- **Vị trí chi tiết có sẵn** (ấn son, hoạ tiết): tìm theo màu (điểm đỏ cho ấn son).
- **Tỷ lệ ảnh:** so với khung chứa trong CSS để chọn `border-image` hay `background`.

### 4. GHÉP — CSS bằng `border-image` + alpha key
- Khung/nền/nút → `border-image` với slice **đo trên ảnh ĐÃ resize** (không phải ảnh gốc):

```css
.frame{
  border-style:solid;border-color:transparent;
  border-width:9px 9px;
  border-image:url("../assets/ui/panel.jpg") 71 67 64 68 fill / 9px 9px / 0 stretch;
}
```
  - Bốn số slice = **trên phải dưới trái**, cộng biên an toàn ~8px.
  - Từ khoá `fill` giữ phần ruột; `stretch` giãn phần giữa, không méo viền.
- Tài nguyên đè lên nền (viền avatar, ấn son) → **tách nền thành PNG alpha**:
  giấy sáng → trong suốt, mực → đậm. Công thức: `alpha = ((255-L)/255)**(1/gamma)*255`.
- Tài nguyên nặng → thu nhỏ + chuyển **JPEG** (khung/nền/nút) hoặc PNG alpha (đè).

### 5. KIỂM CHỨNG — chụp trình duyệt rồi đo lại
- Mở trang bằng trình duyệt headless, **chụp ảnh màn hình**.
- Phân tích ảnh chụp bằng Pillow: **bản đồ mật độ mực** (lưới ô) để xem viền có hiện đúng
  vị trí, chữ có nằm trong ruột khung không.
- Đối chiếu **URL công khai** mà người dùng thật sự dùng (không chỉ localhost).

## Video ngắn: ghép nhiều ảnh + hiệu ứng (kiểu intro CapCut)

Video **không phải** file phim. Video = **một chuỗi ảnh tĩnh** chạy qua hiệu ứng,
giống các đoạn intro trong CapCut. Vì vậy cùng một thư viện ảnh phục vụ cả ảnh lẫn video.

Cách dựng:
- Một **timeline** gồm nhiều **khung** (`frame`), mỗi khung giữ 0.6–1.2 giây.
- Mỗi khung: một ảnh từ thư viện + hiệu ứng vào/ra.
- Nối khung bằng **chuyển cảnh** (crossfade, trượt, mực loang).

Hiệu ứng từng khung:

| Hiệu ứng | Kỹ thuật CSS |
|---|---|
| Máy quay chậm (Ken Burns) | `@keyframes` đổi `transform: scale()` + `translate()` |
| Mực loang | ảnh PNG alpha + `animation` đổi `opacity` / `filter: blur()` |
| Mây trôi, lá rơi | nhiều lớp ảnh, mỗi lớp một tốc độ `animation-duration` |
| Chuyển cảnh | `mask-image` + `linear-gradient` chạy ngang |
| Khói / sương | `radial-gradient` mờ + `animation` dịch chuyển |

Dựng timeline bằng **một biến JS** liệt kê khung, rồi sinh `@keyframes` từ đó:

```js
const timeline = [
  {img:"library/dong-phu-01.jpg", fx:"kenburns", sec:1.0},
  {img:"library/linh-khi-02.jpg", fx:"ink-spread", sec:0.8},
  {img:"library/dot-pha-03.jpg",  fx:"flash",     sec:1.2},
];
```

**Kiểm chứng:** chụp ảnh ở **nhiều mốc thời gian** (ví dụ 0s, 0.8s, 1.6s), không chỉ 1 khung.

### Thư viện ảnh/video dùng chung

- Thư viện là **cây thư mục + tệp mô tả** (`library/index.json`), mỗi mục có **thuộc tính**
  để AI tra đúng ảnh: `loai` (nhân vật / bối cảnh / vật phẩm), `gioi_tinh`, `tuoi`,
  `ngoai_hinh`, `mau_da`, `chung_toc`, `tinh_cach`, `tags`.
- AI **tra theo thuộc tính**, không đoán mò → tránh lấy ảnh nữ cho Hàn Lập hay ảnh ông già.
- Cùng bộ ảnh phục vụ cả hiển thị tĩnh lẫn dựng video.

## Mẫu lệnh Pillow dùng lại

Skill này có **3 script sẵn dùng** trong `scripts/` (thay cho việc viết lại code mỗi lần):

```bash
# ③ ĐO — độ dày viền, ruột sáng/tối, và dòng CSS border-image sẵn dùng
python3 scripts/measure_frame.py assets/ui/panel-character.jpg

# ④ GHÉP — tách nền PNG alpha (tài nguyên đè) hoặc nén JPEG (khung/nền/nút)
python3 scripts/prep_assets.py alpha assets/ui-orig/avatar-ring.png assets/ui/avatar-ring.png --width 512
python3 scripts/prep_assets.py jpeg  assets/ui-orig/bg-main.png     assets/ui/bg-main.jpg     --width 820

# ⑤ KIỂM CHỨNG — bản đồ mật độ mực từ ảnh chụp trình duyệt
python3 scripts/verify_shot.py screenshot.png --region 700 0 1220 1080
```

Cần Pillow: `pip install Pillow`.

Nếu phải viết tay, dùng mẫu sau:

```python
from PIL import Image
# Đo độ dày viền
im = Image.open(path).convert('L'); w,h = im.size; px = im.load()
xs = [x for x in range(int(w*.35)) if px[x,h//2] < 150]     # viền trái
print("viền:", min(xs), max(xs), "-> slice", max(xs)+8)

# Tách nền PNG alpha cho tài nguyên đè
for y in range(h):
    for x in range(w):
        r,g,b = im_rgb.getpixel((x,y)); L = (r*299+g*587+b*114)//1000
        a = int(min(255, ((max(0,255-L-8))/255)**0.5*255))
        out.putpixel((x,y), (r,g,b,a))
```

## Ghi nhớ

- **Không bao giờ** kéo giãn ảnh khung bằng `background-size:100% 100%` → méo nét vẽ.
- **Không bao giờ** viết số CSS bằng cách đoán → luôn đo bằng Pillow trước.
- **Luôn** kiểm chứng bằng ảnh chụp trình duyệt + bản đồ mực, không tin vào CSS "trông có vẻ đúng".
- Giữ **bản gốc ảnh** ở thư mục riêng, chỉ tối ưu bản dùng cho web.
