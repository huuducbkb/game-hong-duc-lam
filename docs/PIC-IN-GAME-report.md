# Báo cáo công cụ: PIC-IN-GAME

**Tên:** PIC-IN-GAME — *Pic-in-Game Method*
**Tên tiếng Việt:** Phương pháp đưa ảnh vào game
**Phiên bản:** 1.0
**Ngày lập:** 2026-11-12
**Nguồn gốc:** đúc kết từ việc ghép 7 ảnh thủy mặc do AI bên ngoài vẽ vào giao diện
game *Hồng Đức Tu Tiên Lộ*.
**Nơi lưu skill:** `.agents/skills/pic-in-game/SKILL.md`
**Script kèm theo:**
- `.agents/skills/pic-in-game/scripts/measure_frame.py` — bước ③ ĐO
- `.agents/skills/pic-in-game/scripts/prep_assets.py` — bước ④ GHÉP
- `.agents/skills/pic-in-game/scripts/verify_shot.py` — bước ⑤ KIỂM CHỨNG

---

## 1. Công cụ này là gì

PIC-IN-GAME là **quy trình 5 bước** để biến ảnh do một công cụ AI **bên ngoài** vẽ
(tranh vẽ tay, thủy mặc, khung viền có nét mực) thành **giao diện web thật**, sao cho:

- **không méo nét vẽ** khi co giãn,
- **có đo đạc** thay vì đoán mò số liệu CSS,
- **có kiểm chứng** bằng ảnh chụp trình duyệt thật.

Nó cũng mở rộng sang **video ngắn kiểu cinematic** dựng bằng CSS animation trên ảnh tĩnh.

> **Câu chốt:** *Đo trước, ghép sau, chụp lại mà kiểm.*

## 2. Vấn đề nó giải quyết

| Vấn đề thực tế | Hậu quả nếu không có PIC-IN-GAME |
|---|---|
| API sinh ảnh không dùng được (Gemini free tier chặn, OpenRouter hết credit) | Tắc hẳn, không có tài nguyên để làm giao diện |
| Ảnh khung vẽ tay bị kéo giãn bằng `background-size:100% 100%` | Viền mực **bị bóp méo**, nét vẽ biến dạng |
| Viết số CSS bằng cách ước lượng bằng mắt | Chữ **đè lên nét mực**, khung lệch, phải sửa nhiều lần |
| Không kiểm chứng, chỉ tin CSS "trông có vẻ đúng" | Lỗi chỉ lộ ra khi người dùng mở trên máy thật |
| Ảnh gốc nặng (7 ảnh ≈ 18MB) | Tải chậm trên Safari iPhone/iPad |

## 3. Quy trình 5 bước

```
 ① PROMPT  →  ② NHẬN ẢNH  →  ③ ĐO (Pillow)  →  ④ GHÉP (border-image)  →  ⑤ KIỂM CHỨNG (chụp trình duyệt)
     ▲                                                                              │
     └──────────────────────  thiếu/sửa tài nguyên thì lặp lại  ◄────────────────────┘
```

**① PROMPT** — viết prompt chi tiết, tách từng tài nguyên; cho người dùng trang web
(Xưởng) để copy prompt và upload ảnh trả về.

**② NHẬN ẢNH** — nhận, kiểm kê, giữ bản gốc riêng, tối ưu bản dùng cho web.

**③ ĐO** — dùng Pillow đo: độ dày viền, ruột sáng/tối, vị trí chi tiết (ấn son),
tỷ lệ ảnh so với khung chứa.

**④ GHÉP** — CSS `border-image` với slice đo **trên ảnh đã resize**; tách nền PNG alpha
cho tài nguyên đè lên nền; nén JPEG cho khung/nền/nút.

**⑤ KIỂM CHỨNG** — chụp ảnh trình duyệt, dựng **bản đồ mật độ mực** bằng Pillow,
đối chiếu với URL công khai mà người dùng thật sự dùng.

## 4. Hai kỹ thuật cốt lõi

### 4.1 `border-image` — giữ nét viền không méo

Ảnh khung được cắt thành 9 phần: 4 góc (giữ nguyên), 4 cạnh (giãn 1 chiều),
1 ruột (giãn 2 chiều). Góc không bao giờ bị bóp méo.

```css
.frame{
  border-style:solid; border-color:transparent;
  border-width:9px 9px;                                  /* độ dày hiển thị */
  border-image:url("../assets/ui/panel.jpg")
               71 67 64 68                              /* slice: trên phải dưới trái */
               fill / 9px 9px / 0 stretch;               /* fill=giữ ruột, stretch=giãn */
}
```

**Quan trọng:** slice phải đo trên ảnh **đã resize**, không phải ảnh gốc. Đo lại sau mỗi lần thu nhỏ.

### 4.2 Alpha key — tách nền cho tài nguyên đè

Viền avatar và ấn son cần **nhìn xuyên qua** nền. Tách bằng cách biến độ sáng thành độ mờ:

```
alpha = ((255 − L) / 255) ^ (1/gamma) × 255      # L = độ sáng, gamma ≈ 2.0
```

Giấy sáng → alpha thấp (trong suốt); mực đậm → alpha cao (rõ). Kết quả: PNG alpha
dùng được trên cả nền sáng lẫn nền tối.

## 5. Ca thực tế đã áp dụng (bằng chứng)

**Dự án:** *Hồng Đức Tu Tiên Lộ* — 7 ảnh thủy mặc do AI bên ngoài vẽ.

### Số liệu đo được (bước ③)

| Tài nguyên | Kích thước gốc | Viền (gốc) | Sau resize | Slice dùng | Kích thước web |
|---|---|---|---|---|---|
| `panel-character` | 1024×1536 | 3.4% | 800×1200 | `71 67 64 68` | 121 KB (JPEG) |
| `panel-story` | 1024×1536 | 1.4% | 800×1200 | `39 38 32 37` | 153 KB (JPEG) |
| `btn-choice` | 1913×822 | 1.4% | 1100×473 | `67 42 73 41` | 81 KB (JPEG) |
| `bg-main` | 864×1821 | — | 820×1728 | (background) | 144 KB (JPEG) |
| `avatar-ring` | 1254×1254 | — | 512×512 | (alpha key) | 548 KB (PNG) |
| `seal` | 1254×1254 | — | 300×300 | (alpha key) | 186 KB (PNG) |

**Kết quả tối ưu:** 18 MB → **1.4 MB** (giảm ~87%).

### Kiểm chứng (bước ⑤)

Phân tích ảnh chụp trình duyệt bằng bản đồ mật độ mực xác nhận: viền khung hiện đúng
vị trí, ruột khung sáng (L ≈ 224–240) nên **chữ mực đọc tốt**, nút lựa chọn khớp khung.

### Chi tiết đáng nhớ

- **Ấn son có sẵn trong ảnh khung** (ở 85%–91% ngang, 90%–94% dọc) làm viền bị lệch khi
  dùng `border-image` → phải **tách ấn son ra** thành `seal.png` riêng, rồi lấp vùng đó
  bằng vân giấy bên cạnh.
- Ảnh 1024×1536 (tỷ lệ 3:4) nhét vào cột cao hẹp (≈1:4) sẽ méo nặng nếu dùng `background`
  → `border-image` là bắt buộc.

## 6. Checklist dùng nhanh

```
[ ] 1. Đã viết prompt tách từng tài nguyên, có nói rõ ruột khung để trống?
[ ] 2. Đã giữ bản gốc ở thư mục riêng (assets/*-orig)?
[ ] 3. Đã đo độ dày viền + ruột sáng/tối bằng Pillow TRƯỚC khi viết CSS?
[ ] 4. Đã resize rồi ĐO LẠI slice trên ảnh đã resize?
[ ] 5. Tài nguyên đè lên nền đã tách alpha PNG chưa?
[ ] 6. Đã chuyển khung/nền/nút sang JPEG để nhẹ chưa?
[ ] 7. Đã chụp trình duyệt và dựng bản đồ mật độ mực để kiểm chứng chưa?
[ ] 8. Đã thử trên URL công khai (không chỉ localhost) chưa?
```

## 7. Video ngắn: ghép nhiều ảnh + hiệu ứng (kiểu intro CapCut)

Video **không phải** file phim. Video = **một chuỗi ảnh tĩnh** chạy qua hiệu ứng,
giống các đoạn intro trong CapCut. Vì vậy cùng một thư viện ảnh phục vụ cả ảnh lẫn video.

Cách dựng: một **timeline** gồm nhiều khung, mỗi khung giữ 0.6–1.2 giây,
mỗi khung là một ảnh + hiệu ứng vào/ra, nối nhau bằng chuyển cảnh.

| Hiệu ứng | Kỹ thuật CSS |
|---|---|
| Máy quay chậm (Ken Burns) | `@keyframes` đổi `transform: scale()` + `translate()` |
| Mực loang | ảnh PNG alpha + `animation` đổi `opacity` / `filter: blur()` |
| Mây trôi, lá rơi | nhiều lớp ảnh, mỗi lớp một tốc độ `animation-duration` khác nhau |
| Chuyển cảnh | `mask-image` + `linear-gradient` chạy ngang |
| Khói / sương | `radial-gradient` mờ + `animation` dịch chuyển |

Timeline khai báo bằng biến JS, rồi sinh `@keyframes` từ đó:

```js
const timeline = [
  { img: "library/bc_dong_phu_03.jpg", fx: "kenburns",   sec: 1.0 },
  { img: "library/vk_kiem_01.jpg",     fx: "ink-spread", sec: 0.8 },
  { img: "library/hq_dot_pha_02.jpg",  fx: "flash",      sec: 1.2 }
];
```

**Kiểm chứng:** chụp ảnh ở **nhiều mốc thời gian** (ví dụ 0s, 0.8s, 1.6s), không chỉ một khung.

### Thư viện ảnh/video dùng chung

Thư viện là cây thư mục + tệp mô tả `index.json`. Mỗi mục có **thuộc tính** để AI tra đúng:
`loai` (nhân vật / bối cảnh / vật phẩm), `gioi_tinh`, `tuoi`, `ngoai_hinh`, `mau_da`,
`chung_toc`, `tinh_cach`, `tags`. AI tra theo thuộc tính, không đoán mò.

## 8. Ghi nhớ cốt lõi

1. **Không** kéo giãn ảnh khung bằng `background-size:100% 100%` → méo nét vẽ.
2. **Không** viết số CSS bằng cách đoán → luôn đo bằng Pillow trước.
3. **Luôn** kiểm chứng bằng ảnh chụp trình duyệt + bản đồ mực.
4. **Luôn** giữ bản gốc ảnh riêng, chỉ tối ưu bản dùng cho web.
5. Tài nguyên đè lên nền → **tách alpha PNG**; khung/nền/nút → **JPEG**.
6. Chi tiết có sẵn trong ảnh khung (ấn son, hoạ tiết) làm viền lệch → **tách ra riêng**.
