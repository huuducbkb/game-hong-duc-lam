# Hồng Đức Tu Tiên Lộ

Game AI text tu tiên chạy trên web. Đồng nhân xuyên không dựa trên *Phàm Nhân Tu Tiên* (Vong Ngữ).
Người chơi xuyên không vào thế giới đó, sống cùng thời Hàn Lập.

Người dùng chỉ có **Safari (iPad/iPhone), KHÔNG có terminal** → mọi thứ phải qua giao diện web.

## QUY TẮC BẮT BUỘC: dùng phương pháp PIC-IN-GAME

**Mọi việc đụng đến thiết kế giao diện, tạo hình ảnh, hoặc video ngắn → PHẢI dùng
quy trình PIC-IN-GAME.** Không tự nghĩ cách khác.

- Skill: `.agents/skills/pic-in-game/SKILL.md`
- Báo cáo đầy đủ: `docs/PIC-IN-GAME-report.md`

Tóm tắt 5 bước: **① PROMPT** (viết prompt gửi AI ngoài) → **② NHẬN ẢNH** (kiểm kê, giữ bản gốc)
→ **③ ĐO** (Pillow: độ dày viền, ruột sáng/tối, vị trí ấn son) → **④ GHÉP** (`border-image`
+ alpha key PNG) → **⑤ KIỂM CHỨNG** (chụp trình duyệt + bản đồ mật độ mực).

Ba điều không bao giờ quên:
1. **Không** kéo giãn ảnh khung bằng `background-size:100% 100%` → méo nét vẽ.
2. **Không** viết số CSS bằng cách đoán → đo bằng Pillow trước, đo lại sau khi resize.
3. **Luôn** kiểm chứng bằng ảnh chụp trình duyệt, không tin CSS "trông có vẻ đúng".

## Chạy máy chủ

```bash
# tĩnh (xem demo + ảnh) — port 12000
setsid nohup python3 -m http.server 12000 --bind 0.0.0.0 --directory /workspace/game-hong-duc-lam \
  > /tmp/static.log 2>&1 < /dev/null & disown

# Xưởng (prompt ảnh + upload) — port 12001
setsid nohup python3 tools_server.py > /tmp/studio.log 2>&1 < /dev/null & disown
```

Dùng `setsid nohup ... & disown` để máy chủ sống qua các lệnh shell.
URL cho người dùng: `https://work-1-...` (port 12000) và `https://work-2-...` (port 12001).

## Tài nguyên ảnh (QUAN TRỌNG)

Gemini free tier **chặn sinh ảnh** (quota 0), OpenRouter **hết credit**.
→ Quy trình: agent viết **prompt chi tiết** → người dùng gửi cho AI tạo ảnh bên ngoài
→ người dùng upload ảnh ngược lại qua Xưởng → agent ghép vào giao diện.

- `assets/ui/` — 7 ảnh đã tối ưu (1.4MB). Khung/nền là **JPEG**; `avatar-ring.png` và
  `seal.png` là **PNG alpha** (đã tách nền: giấy sáng → trong suốt, mực → đậm).
- `assets/ui-orig/` — ảnh gốc 18MB, **đã trong .gitignore**, chỉ dùng để xử lý lại.
- Ấn son đã tách khỏi `panel-character` thành `seal.png` để viền không méo khi co giãn.

### Kỹ thuật ghép khung: `border-image`

Ảnh khung không được kéo giãn trực tiếp (sẽ méo nét mực). Dùng `border-image` với
giá trị slice đo **trên ảnh đã resize**, không phải ảnh gốc:

```css
/* panel-character.jpg (800x1200) */ border-image:url(...) 71 67 64 68 fill / 9px 9px / 0 stretch;
/* panel-story.jpg     (800x1200) */ border-image:url(...) 39 38 32 37 fill / 9px 9px / 0 stretch;
/* btn-choice.jpg      (1100x473) */ border-image:url(...) 67 42 73 41 fill / 11px 11px / 0 stretch;
```

Đo lại slice bằng cách quét điểm tối (L<150) theo hàng/cột giữa ảnh.

## Giao diện đã chốt: **1 CỘT** (`demo/hybrid-1col.html`)

Thứ tự dọc: thanh trên (avatar + tiêu đề + nút Hệ Thống) → bảng truyện (cuộn bên trong)
→ 3 nút lựa chọn. `max-width:520px`, ưu tiên iPhone 11.
`demo/hybrid.html` là bản 2 cột cũ, giữ để tham khảo.

**Màn chính KHÔNG có khối thân phận** — chỉ số nhân vật nằm trong **tab "Nhân vật"**
của bảng Hệ Thống, để bảng truyện rộng tối đa.

Bảng Hệ Thống là **drawer trượt từ phải**, có 4 tab: Nhân vật · Kỹ năng · Túi · **NPC**.
Tab đầu gồm thẻ nhân vật (avatar + thanh Tu vi/Khí huyết/Thần thức) và bảng Thân phận.
Avatar đổi ở thanh trên thì **đồng bộ** sang thẻ nhân vật trong tab.

Tab **NPC** liệt kê NPC đã gặp + **thanh hảo cảm** (xanh ≥50, vàng −19…49, đỏ ≤−20)
và thái độ hiện tại. (Tên cũ: "Đã gặp".)

## Cơ chế HẢO CẢM (affinity)

Mỗi NPC có số hảo cảm **−100…+100**, 6 mức (`MUC_HAO_CAM` trong `engine.py`):

| Khoảng | Mức |
|---|---|
| −100…−60 | tử địch |
| −59…−20 | thù địch |
| −19…+19 | người dưng |
| +20…+49 | quen biết |
| +50…+79 | thân thiết |
| +80…+100 | tri kỷ |

- Trong JSON đoạn: `hieu_ung` hỗ trợ `gap_npc` (ghi nhận gặp, lưu chỉ số lần đầu) và
  `hao_cam: {tên: delta}` (tăng/giảm hảo cảm, kèm thông báo).
- `dieu_kien` hỗ trợ `hao_cam: {tên: ngưỡng}` → mở/khoá lựa chọn theo mức hảo cảm.
- Đoạn có NPC nên có **`bien_the`**: danh sách `{npc, muc, ke}` — engine tự chọn đoạn kể
  theo mức hảo cảm hiện tại (`_ke_theo_hao_cam`).
- **Lưu ý**: `_gap_npc` KHÔNG ghi đè hảo cảm đã tích; chỉ đặt `hao_cam` khi gặp lần đầu.

## Chế độ AI (Gemini) — QUAN TRỌNG

- `game/ai.py` bọc Gemini: `thu_ket_noi()` (nhớ kết quả trong RAM), `san_sang()`,
  `ke_lai(doan, hanh_dong)`.
- **Model cũ đã bị khai tử với tài khoản mới** (`gemini-2.5-flash` → HTTP 404). Dùng
  chuỗi dự phòng `MODEL_DU_PHONG` (`gemini-flash-lite-latest`, `gemini-3.5-flash`, …).
  Có thể ép model qua `GEMINI_TEXT_MODEL` trong `.env`.
- `GET /api/ai` → `{ai_san_sang, ly_do}`; `?thu_lai=1` để thử lại (bỏ cache).
- **Phương án D**: khi `ai_san_sang=false`, frontend **ẩn ô gõ tự do** và hiện ghi chú;
  gamebook vẫn chạy đủ bằng nút lựa chọn. Nút lựa chọn luôn hoạt động không cần AI.
- Gõ tự do khi CÓ AI → AI kể lại đoạn theo hành động (không đổi sự kiện/đoạn).

Quy ước: font `Noto Serif` + `Ma Shan Zheng`; màu mực `#1b1915`, ấn son `#a8352a`;
`panel-character.jpg` chỉ còn dùng cho khung (nếu cần), không còn khối thân phận ở màn chính.

## Cấu trúc

- `game/engine.py` — **engine game** (cơ chế chương + đoạn, chỉ số, lưu/nạp)
- `game/chapters/chuong1.json` — **Chương 1: Đại chiến Dã Lang Bang** (23 đoạn, đường chơi ~17–18 đoạn)
- `game/play.html` — **trang chơi** (giao diện 1 cột + 4 tab, nối API thật)
- `game_server.py` — **máy chủ game** (API + tệp tĩnh + Xưởng ảnh), cổng 12001
- `demo/` — 12 phương án giao diện + `hybrid-1col.html` (mẫu) + `hybrid.html` (2 cột)
- `assets/ui/` — ảnh UI đã tối ưu
- `tools_server.py` — Xưởng: prompt ảnh + upload
- `SPEC.md` — đặc tả game
- `.env` — key API (KHÔNG commit; đã trong .gitignore)

## Chạy game

```bash
# máy chủ game (API + giao diện chơi + Xưởng) — port 12001
setsid nohup python3 game_server.py > /tmp/game.log 2>&1 < /dev/null & disown
```

Người dùng mở `https://work-2-.../game` để chơi.

### API
| Đường dẫn | Việc |
|---|---|
| `POST /api/new` | Tạo nhân vật `{ten, xuat_than}` |
| `POST /api/chon` | Chọn `{chi_so}` |
| `POST /api/tu_do` | Hành động tự do `{van_ban}` (AI kể lại) |
| `GET /api/doan` | Nạp lại đoạn đang dừng |
| `GET /api/state` | Trạng thái gọn (có `co_phien`, `npc`) |
| `GET /api/ai` | Kiểm tra AI `{ai_san_sang, ly_do}` |
| `POST /api/luu` | Lưu `{slot}` |

Phiên giữ trong RAM + cookie `phien`; trạng thái đầy đủ lưu ở `data/saves/`.

## Bản thảo để duyệt

Xuất đoạn kể của mọi chương ra văn bản để người dùng đọc:

```bash
python3 tools/export_ban_thao.py        # mọi chương
python3 tools/export_ban_thao.py 1      # chỉ Chương 1
```

Kết quả ở `docs/ban-thao/`: `chuong1.md` (xem trên GitHub), `chuong1.html` (đọc trên Safari),
`index.html` (mục lục). Đọc trực tiếp tại `/docs/ban-thao/index.html`.

## Kế hoạch & đặc tả

- `SPEC.md` — đặc tả game (Chương 1–3)
- `docs/KE-HOACH-CHI-TIET.md` — **kế hoạch chi tiết đã chốt với người dùng**:
  cơ chế "chương + đoạn" chống lặp/quên, bảng chỉ số (10 chỉ số + tấn công/kháng phép
  9 hệ), thần niệm, thư viện ảnh/video, chi phí token, tab Hệ Thống, nghề phụ + kinh tế.

### Thuật ngữ quan trọng
- **"Đoạn"** = giai đoạn nhỏ trong chương (KHÔNG phải nút bấm). Chương = chuỗi đoạn.
- **"Lựa chọn"** = nút bấm người chơi chọn (gõ tự do vẫn giữ song song).
- **Thần niệm** = giác quan + tay nghề + vũ khí tinh thần (xem kế hoạch mục C).
- **Chủng loại** NPC: nhân loại · yêu thú · yêu thú hoá hình người · ma thú · quỷ ·
  khôi lỗi · cương thi… (dùng để AI tra đúng ảnh).
- **1 chương = 18 đoạn ≈ 45 phút** (2,5 phút/lượt). Cấu trúc 3 hồi: 5 mở · 8 thân · 5 kết.

## Cần làm tiếp

1. ~~Người dùng duyệt giao diện 1 cột~~ ✅
2. Backend game Python + tích hợp LLM (theo cơ chế chương + đoạn)
3. Nội dung Chương 1 (Dã Lang Bang), Chương 2 (Huyết Sát Thí Luyện), Chương 3
4. Thư viện ảnh/video + thẻ thuộc tính cho AI tra
5. *(giai đoạn sau)* Nghề phụ + thị trường kinh tế
