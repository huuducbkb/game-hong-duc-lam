# Hồng Đức Tu Tiên Lộ

Game AI text tu tiên chạy trên web. Đồng nhân xuyên không dựa trên *Phàm Nhân Tu Tiên* (Vong Ngữ).
Người chơi xuyên không vào thế giới đó, sống cùng thời Hàn Lập.

Người dùng chỉ có **Safari (iPad/iPhone), KHÔNG có terminal** → mọi thứ phải qua giao diện web.

## 📓 ĐỌC TRƯỚC KHI LÀM GÌ: `tai-lieu/NHAT-KY.md`

**Mở khung chat mới thì đọc `tai-lieu/NHAT-KY.md` trước tiên.** Đó là nhật ký công việc:
đã làm gì, đổi file nào, kiểm chứng bằng số đo nào, còn gì chưa xong. Người dùng làm việc
qua nhiều phiên chat và chat cũ có thể lỗi — nhật ký là thứ giữ mạch công việc.

**Sau mỗi việc xong, ghi thêm một mục vào đầu file đó** (mới nhất trên cùng), theo mẫu:
ngày · người dùng yêu cầu gì · đã sửa file nào · **số đo kiểm chứng** · chưa làm gì.
Đừng ghi "đã làm đẹp hơn" — ghi cái đo được.

Ghi nhật ký **trước khi** báo xong cho người dùng, để lần sau không phải dựng lại từ chat.

## QUY TẮC BẮT BUỘC: dùng phương pháp PIC-IN-GAME

**Mọi việc đụng đến thiết kế giao diện, tạo hình ảnh, hoặc video ngắn → PHẢI dùng
quy trình PIC-IN-GAME.** Không tự nghĩ cách khác.

- Skill: `.agents/skills/pic-in-game/SKILL.md`
- Báo cáo đầy đủ: `tai-lieu/PIC-IN-GAME-report.md`

Tóm tắt 5 bước: **① PROMPT** (viết prompt gửi AI ngoài) → **② NHẬN ẢNH** (kiểm kê, giữ bản gốc)
→ **③ ĐO** (Pillow: độ dày viền, ruột sáng/tối, vị trí ấn son) → **④ GHÉP** (`border-image`
+ alpha key PNG) → **⑤ KIỂM CHỨNG** (chụp trình duyệt + bản đồ mật độ mực).

Bốn điều không bao giờ quên:
1. **Không** kéo giãn ảnh khung bằng `background-size:100% 100%` → méo nét vẽ.
2. **Không** viết số CSS bằng cách đoán → đo bằng Pillow trước, đo lại sau khi resize.
3. **Luôn** kiểm chứng bằng ảnh chụp trình duyệt, không tin CSS "trông có vẻ đúng".
4. **PNG đè lên ảnh khác phải kiểm alpha thật**, đừng tin đuôi `.png`.
   File có kênh alpha vẫn có thể **đục 100%** (alpha = 255 khắp nơi) và sẽ che kín
   thứ nằm dưới. Đo trước khi dùng: `sum(1 for v in im.getchannel("A").get_flattened_data() if v < 30)`
   — nếu ra 0 thì ảnh đang đục, phải tách nền. Đây đúng là lỗi từng làm người dùng
   tưởng "up ảnh đại diện không được" (2026-11-21): vòng `avatar-ring.png` đục che mất ảnh.

   Nền giấy trong bộ ảnh này là **kem ~232**, không phải trắng 255 — nên đừng dùng
   ngưỡng trắng cứng. Công thức đúng: `alpha = (225 - do_sang) / (225 - 60)`, kẹp 0..255.

   **Ảnh mực ĐỎ (son, ấn, triện) thì tách theo độ đỏ, đừng tách theo độ sáng.**
   Vân giấy có chỗ tối ngang mực nhạt nên tách theo độ sáng sẽ lọt lại ~30% nền.
   Đo `do_do = r - max(g,b)`: giấy ~14–18, mực son ~65–149, hai nhóm tách rời hẳn.
   Công thức: `alpha = (do_do - 25) / (70 - 25)`, kẹp 0..255.
   Đã dùng cho `seal.png` (2026-11-21): 0% → 86,5% trong suốt, và so với ảnh gốc
   chỉ lệch 0,04% pixel — tức tách nền không làm hỏng nét vẽ.

   Cách kiểm sau khi tách: đặt bản tách lên đúng màu nền giấy rồi so với ảnh gốc
   (`ImageChops.difference`). Lệch trung bình phải nhỏ (cỡ chục/255). Nếu lệch nhiều
   là đã ăn mất nét hoặc còn sót nền.

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

### Dán ảnh ngay trong thẻ Xưởng tĩnh (GitHub Pages)

Trang tĩnh `docs/xuong/index.html` **không có backend**, nên thay vì mở Issue nhiều bước,
mỗi thẻ có **ô dán ảnh** gọi thẳng GitHub Contents API từ trình duyệt:

- Người dùng **dán token 1 lần** ở mục "🔑 Kết nối GitHub" (fine-grained PAT, quyền
  **Contents: Read and write**). Token lưu ở `localStorage` khoá `xuong_gh_token`,
  chỉ gửi tới `api.github.com` — không qua server nào của mình.
- Mỗi thẻ: **chạm vào ô 📷** → mở **thư viện ảnh** (điện thoại) hoặc hộp chọn file (máy tính);
  trên máy tính còn **dán Ctrl+V** / **kéo thả** được. Ô là `<label>` bọc `<input type=file>`
  phủ toàn ô (opacity 0) — **KHÔNG dùng `input.click()` bằng JS**, vì iOS/Safari chặn
  hộp chọn file mở từ JS khi không nằm trong luồng chạm thật. Sau khi chọn, ảnh
  **nén trên máy** (canvas, cạnh dài ≤1600px; PNG giữ PNG, còn lại JPEG q0.9) →
  `PUT /contents/xuong-inbox/<mã>/<mã>.<ext>` (kèm `sha` khi ghi đè) → bot GitHub Actions
  nhận, nhận diện theo **tên thư mục = mã ảnh**, nén lại theo quy tắc game, ghép vào đoạn,
  deploy Pages. Ô và nút Gửi phải **to** (padding ≥14px) cho ngón tay.
- Chỉ một ô là đích cho Ctrl+V tại một thời điểm (`O_DANG_CHON`, cập nhật khi chạm ô).
- Hàm JS: `ghLuuToken` / `ghQuenToken` / `ghLaySha` / `ghPutAnh` / `ghNenAnh` / `guiMotAnh`.
- Nút **🔄 Kiểm tra** mỗi thẻ: `GET /repos/.../commits?path=docs/assets/<scene|ui>/<file>&per_page=1`
  → nếu có commit thì ảnh **đã vào game**. Hiện ảnh qua `raw.githubusercontent.com/<repo>/<sha>/<path>`
  — ghim theo **sha** nên không bị cache, luôn thấy bản mới nhất. Đổi nhãn thẻ sang "đã có".
  Sau khi gửi ảnh, `theoDoiAnh()` tự dò mỗi **15 giây**, tối đa **10 lần**, rồi báo.
  Thư mục suy theo tên file: `bc_`/`vt_`/`nv_` → `docs/assets/scene/`, còn lại → `docs/assets/ui/`.
- Lưu ý khi viết JS trong chuỗi Python: `\n` trong template Python thành **xuống dòng thật**,
  làm hỏng JS. Dùng chuỗi thô (`r"""`) hoặc tránh escape trong JS.
- CORS: `api.github.com` trả `access-control-allow-origin: *` cho PUT/POST — nên gọi
  thẳng từ trang Pages được, **không cần proxy**.
- Vẫn giữ đường lui: nút mở Issue trống và mục "Up thẳng vào thư mục" (không cần token).

### Up ảnh là tự vào game (Xưởng studio, cổng 12001)

Người dùng **chỉ cần up ảnh** — không cần đặt tên, không cần chọn đúng prompt:

- **Mỗi thẻ prompt** trong Xưởng có ô **📤 Up ảnh cho đúng ô này** → up vào là ảnh
  gán thẳng theo `key` của thẻ đó (không AI đoán, không lộn giữa các cảnh).
- **Kéo thả nhiều ảnh** ở cuối trang → AI nhận diện theo tỷ lệ + nội dung, ảnh nào
  chắc (≥80%) thì tự gán, còn lại hiện lưới để người dùng xác nhận.
- Endpoint `POST /luu_loat` (`{ds:[{key,data}], day:true}`) chạy trọn:
  lưu ảnh (nén) → **ghép vào đoạn truyện** (`xuong_tu_dong.luu_va_ghep`) →
  cập nhật `docs/assets/library/index.json` → dựng lại `docs/xuong/index.html` →
  commit + push (Pages tự cập nhật).
- **`day=true` mới commit/push.** Mặc định `day=false` (không đẩy) — để chạy thử và
  **bộ kiểm thử không bao giờ đẩy ảnh thử lên `main`**. Nút up trên Xưởng gửi `day:true`.
  (Sự cố đã gặp: `/luu_loat` từng tự push, mà `_test_api.py` gọi endpoint này → đẩy ảnh
  thử lên main, ghi đè ảnh thật. Vì vậy `/luu_loat` phải opt-in và test phải sao lưu
  cả `docs/assets/library/index.json` + dữ liệu chương.)

- **KHÔNG gửi `Authorization` khi tải ảnh từ CDN GitHub.** Ảnh đính kèm trong Issue nằm
  trên `github.com/user-attachments/...` và `*.githubusercontent.com` — URL đã ký sẵn;
  gửi kèm `Bearer <token>` sẽ bị trả **400 Bad Request**. Chỉ gửi token cho
  `api.github.com`. (Sự cố đã gặp: `_tai` trong `tools/xu_ly_inbox.py` gửi token cho
  MỌI link chứa chữ "github" → ảnh Issue tải thất bại, bot im lặng bỏ qua, báo
  "Không tìm thấy ảnh nào" dù Issue có ảnh và workflow vẫn "success". Đã sửa: chỉ gửi
  token cho `api.github.com`, và ghi log ra stderr khi tải thất bại thay vì nuốt lỗi.)

- `assets/ui/` — 7 ảnh đã tối ưu (1.4MB). Khung/nền là **JPEG**; `avatar-ring.png` và
  `seal.png` là **PNG alpha** (đã tách nền: giấy sáng → trong suốt, mực → đậm).
- `assets/ui-orig/` — ảnh gốc 18MB, **đã trong .gitignore**, chỉ dùng để xử lý lại.
- Ấn son đã tách khỏi `panel-character` thành `seal.png` để viền không méo khi co giãn.

### Nén ảnh tự động khi lưu (Xưởng)

`luu_anh` (trong `tools_server.py`) tự nén mọi ảnh upload qua `game/nen_anh.py`
(mức "vừa": JPEG q80). Quy tắc trong `QUY_TAC`:

- **Bề rộng đích PHẢI khớp cỡ ảnh game đang dùng** (`panel-story` 800, `btn-choice` 1100…)
  vì `border-image` cắt viền theo pixel cố định → đổi cỡ là lệch viền.
- `seal`, `avatar-ring` giữ **PNG alpha**; còn lại lưu **JPEG**.
- Bản gốc (chưa nén) lưu vào `assets/ui-orig/` hoặc `assets/scene-orig/` (đã gitignore).
- Ảnh lưu vào **cả** `assets/…` **lẫn** `docs/assets/…` (Pages chạy từ `docs/`).
- Thiếu Pillow → lưu nguyên gốc (không vỡ luồng). `pip install Pillow` nếu cần.

Kết quả thực đo (ảnh AI 2.3MB → bản game): giảm **6–37×** (vd `bg-main` 2341→144 KB).

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
  `ke_lai(doan, hanh_dong, thay_doi)`, `nhan_dien(van_ban, boi_canh) -> dict`.
- **Model cũ đã bị khai tử với tài khoản mới** (`gemini-2.5-flash` → HTTP 404). Dùng
  chuỗi dự phòng `MODEL_DU_PHONG` (`gemini-flash-lite-latest`, `gemini-3.5-flash`, …).
  Có thể ép model qua `GEMINI_TEXT_MODEL` trong `.env`.
- `GET /api/ai` → `{ai_san_sang, ly_do}`; `?thu_lai=1` để thử lại (bỏ cache).
- **Phương án D**: khi `ai_san_sang=false`, frontend **ẩn ô gõ tự do** và hiện ghi chú;
  gamebook vẫn chạy đủ bằng nút lựa chọn. Nút lựa chọn luôn hoạt động không cần AI.
- Gõ tự do khi CÓ AI: hai bước — (1) `nhan_dien()` đọc hành động → JSON ý định
  (hành động + thay đổi chỉ số NHỎ), engine lọc qua `_loc_y_dinh()` (chỉ khoá/NPC hợp lệ,
  cắt trong giới hạn) rồi áp bằng `_ap_hieu_ung()`; (2) `ke_lai()` viết lại đoạn cho khớp.
  **Đoạn truyện không đổi** — chỉ chỉ số/hảo cảm đổi. Ý định lọc ở 2 lớp: ai.py và engine.
  Giới hạn: `sinh_luc −15..10`, `tu_vi 0..8`, `linh_thach −10..10`, `than_niem 0..2`,
  `hao_cam −10..10` (chỉ NPC đã gặp).

### Chặn "AI kể" viết hỏng — BẮT BUỘC giữ

Prompt kiểu "đổi sang giọng **cổ phong**" từng sinh chữ rác thật (người chơi báo):
`mộtỗ`, `dị hương`, `khứu đại`, `triệt ngộ`, `u lan chi khí ấy lại tùng hình nàng mà chí`,
và `mai táng` dùng sai (chôn khối ngọc, không phải chôn người). Truyện gốc **sạch 100%**,
nên AI chỉ làm hỏng thêm.

- Prompt hiện tại yêu cầu **tiếng Việt hiện đại, trong sáng**, cấm từ Hán-Việt cổ, giữ
  ngôi "ta", giữ tên riêng, giữ dòng trống giữa các đoạn, viết trọn câu.
- Hàm chặn `van_ban_dung(ban_ai, ban_goc) -> (dùng_được, lý_do)` có ở **cả hai bản**:
  `game/ai.py` và `docs/game/ai.js`. Bản AI không đạt → trả `""` → nơi gọi dùng văn gốc.
  Kiểm tra: ký tự rác, danh sách `TU_RAC`, chữ dính (`mộtỗ`), câu bị cắt, tỉ lệ từ lạ
  >12%, mất tên riêng, gộp mất dòng trống, độ dài ngoài 70–140% bản gốc.
- Kho từ chuẩn lấy từ chính truyện: Python đọc `game/chapters/*.json`; JS lấy qua
  `Engine.load_chuong(1)` (truyện nạp bất đồng bộ, không có global sẵn).
- Số đo hiệu chỉnh: bản gốc **0.0%** từ lạ · bản AI hỏng **12–45%**. Sau khi sửa prompt:
  **0.0–0.8%**, 8/8 đoạn thử đạt, độ dài 100%, không mất tên riêng.
- Sửa prompt/hàm chặn phải sửa **cả hai file** — `ai.js` là bản chạy thật trên GitHub Pages.


Quy ước: font `Noto Serif` + `Ma Shan Zheng`; màu mực `#1b1915`, ấn son `#a8352a`;
`panel-character.jpg` chỉ còn dùng cho khung (nếu cần), không còn khối thân phận ở màn chính.

## Cấu trúc

- `game/engine.py` — **engine game** (cơ chế chương + đoạn, chỉ số, lưu/nạp)
- `game/chapters/chuong1.json` — **Chương 1: Đại chiến Dã Lang Bang** (23 đoạn, đường chơi ~17–18 đoạn)
- `game/play.html` — **trang chơi bản Python** (giao diện 1 cột + 4 tab, nối API thật)
- `game/_test_engine.js` — test engine JS (đặt ở đây, KHÔNG trong `docs/`)
- `game_server.py` — **máy chủ game** (API + tệp tĩnh + Xưởng ảnh), cổng 12001
- `demo/` — 12 phương án giao diện + `hybrid-1col.html` (mẫu) + `hybrid.html` (2 cột)
- `assets/ui/` — ảnh UI đã tối ưu
- `tools_server.py` — Xưởng: prompt ảnh + upload
- `SPEC.md` — đặc tả game
- `tai-lieu/` — **tài liệu nội bộ** (kế hoạch, góp ý bản thảo, báo cáo). Nằm NGOÀI `docs/` nên không bị Pages phục vụ.
- `.env` — key API (KHÔNG commit; đã trong .gitignore)

### ⚠ `docs/` = thư mục deploy, MỌI thứ trong đó đều PUBLIC

Workflow Pages upload **cả** `docs/`. Nên:
- Chỉ để trong `docs/` những gì người chơi được thấy (game, ảnh, trang chủ, bản thảo để đọc).
- Tài liệu nội bộ, kế hoạch, báo cáo → để ở `tai-lieu/` (ngoài `docs/`).
- File test (`_test_engine.js`) → để ở `game/`, không để trong `docs/game/`.
- Kiểm tra nhanh: `curl -o /dev/null -w '%{http_code}' https://huuducbkb.github.io/game-hong-duc-lam/<đường-dẫn>` — 200 nghĩa là đang public.
- Lưu ý: repo là **public**, nên file ở `tai-lieu/` vẫn xem được trên GitHub; chỉ là hết public trên *web Pages*.

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

Xuất đoạn kể ra văn bản để người dùng đọc. **Mỗi xuất thân là một nhánh riêng →
xuất thành FILE RIÊNG** (không nối các nhánh vào một file):

```bash
python3 tools/export_ban_thao.py                      # mọi chương, mọi nhánh
python3 tools/export_ban_thao.py 1                    # Chương 1, mọi nhánh
python3 tools/export_ban_thao.py 1 --nhanh mon_phai   # CHỈ nhánh môn phái
```

Mã nhánh: `tan_tu`, `mon_phai`. **(Chỉ còn 2 nhánh — xem mục "Phạm vi xây dựng".)**

Kết quả ở `docs/luu-tru/ban-thao/`: `index.html` (mục lục: chương + từng nhánh),
`chuong1-<nhánh>.html` (đọc trên Safari), `chuong1-<nhánh>.md` (xem trên GitHub).
Đọc trực tiếp tại `/docs/luu-tru/ban-thao/index.html`.

> **Khi đang viết 1 nhánh:** dùng `--nhanh <mã>` để chỉ xuất nhánh đó — đúng
> nhánh đang duyệt, không lẫn các nhánh khác.

**Sơ đồ nhánh tự động.** Nhiều nhánh rẽ thành nhiều đường song song (người chơi
chọn 1) rồi hội tụ lại. Nếu chỉ xếp đoạn theo thứ tự JSON, người đọc tưởng nhân
vật đi HẾT các đường liên tiếp (đã từng bị báo lỗi này). Vì vậy export tự:
- phát hiện điểm rẽ (đoạn có ≥2 lựa chọn) và lan truyền để biết đoạn nào thuộc
  đường nào;
- đoạn đi được từ ≥2 đường = **hội tụ** (dùng chung, không gắn nhãn);
- in **sơ đồ nhánh** ở đầu file (①②③ + tên lựa chọn + danh sách đoạn + điểm hội tụ);
- gắn nhãn `· **[ĐƯỜNG ①]**` vào tiêu đề mỗi đoạn riêng của đường.

Không hard-code — hàm `phan_tich_nhanh()` trong `tools/export_ban_thao.py` tự suy
ra từ liên kết, nên tự đúng cho mọi nhánh.

## Kế hoạch & đặc tả

- `SPEC.md` — đặc tả game (Chương 1–3)
- `tai-lieu/KE-HOACH-CHI-TIET.md` — **kế hoạch chi tiết đã chốt với người dùng**:
  cơ chế "chương + đoạn" chống lặp/quên, bảng chỉ số (10 chỉ số + tấn công/kháng phép
  9 hệ), thần niệm, thư viện ảnh/video, chi phí token, tab Hệ Thống, nghề phụ + kinh tế.

### Thuật ngữ quan trọng
- **"Đoạn"** = giai đoạn nhỏ trong chương (KHÔNG phải nút bấm). Chương = chuỗi đoạn.
- **"Lựa chọn"** = nút bấm người chơi chọn (gõ tự do vẫn giữ song song).
- **Thần niệm** = giác quan + tay nghề + vũ khí tinh thần (xem kế hoạch mục C).
- **Chủng loại** NPC: nhân loại · yêu thú · yêu thú hoá hình người · ma thú · quỷ ·
  khôi lỗi · cương thi… (dùng để AI tra đúng ảnh).
- **Số đoạn/chương: KHÔNG ép cứng** — viết bao nhiêu tuỳ cốt truyện cần (trước đây từng
  đặt mục tiêu 18 đoạn ≈ 45 phút, nay **bỏ ràng buộc này** để truyện khỏi bị gò).

## CANON — BẮT BUỘC ĐÚNG (đọc trước khi viết truyện)

> Đã từng viết sai nặng vì coi Thất Huyền Môn là tông môn tu tiên. Ghi lại để không tái phạm.

| Điều | Canon ĐÚNG |
|---|---|
| **Thất Huyền Môn (七玄门)** | **Môn phái GIANG HỒ (võ lâm)** — KHÔNG phải tông môn tu tiên. Đệ tử phần lớn là **phàm nhân luyện võ**. |
| **Tu luyện ở Thất Huyền Môn** | **Không có** (không truyền thụ tu tiên cho đệ tử). Tu luyện ở đây là **bí mật, hiếm** — ai lộ ra là chết. |
| **Hàn Lập vào môn** | Do **chú của y dẫn tới dự tuyển** đệ tử — không tự tới. |
| **Mạc Đại Phu (墨大夫)** | Thầy thuốc trong môn, **sư phụ của Hàn Lập**, người **bí mật truyền Trường Xuân Công** → đây là **bước đầu tu luyện** của Hàn Lập. |
| **Trường Xuân Công** | Công pháp Hàn Lập lén học từ Mạc Đại Phu — **giữ kín**, không ai biết. |
| **Dã Lang Bang (野狼帮)** | Bang hội giang hồ — trận đánh là **chiến tranh võ lâm**, đa số là võ giả phàm nhân. |
| **Tiền tệ (chương giang hồ)** | **Bạc / vàng** (lượng, quan). **KHÔNG dùng "linh thạch"** — linh thạch chỉ thuộc giới tu tiên, chưa xuất hiện ở tầng phàm nhân. |
| **Thời điểm Chương 1** | **Sau khi Hàn Lập đã vào Thất Huyền Môn** (khớp trận Dã Lang Bang). |
| **Nhánh "môn phái" của người chơi** | **Đệ tử võ lâm phàm nhân** của Thất Huyền Môn, **tự tới dự tuyển** (không có người thân dẫn). Lén nhận **con đường tu luyện từ ngọc cốt** — song hành với Hàn Lập lén học Trường Xuân Công. |
| **Mạc Đại Phu trong chương 1** | **Có xuất hiện** — người chơi cũng gặp ông, tạo móc nối với Hàn Lập. |

**Sai thường gặp cần tránh:** gọi đệ tử Thất Huyền Môn là "tu sĩ"; dùng "linh thạch",
"linh dược viên", "cống phẩm linh thạch"; cho người chơi lộ tu vi công khai.


## Xuất thân = nhánh truyện (đã làm)

Mỗi xuất thân KHÔNG chỉ là nhãn — nó quyết định **hành trình riêng** tới lúc gặp Hàn Lập.

- Bảng nhóm ở `game/xuat_than.json`: **2 nhóm chơi được** + 1 nhóm ẩn (`an: true`, khoá).
  Nhóm ẩn = "Ngọc cốt Tuyết Cơ" — **chưa mở**, không hiện menu, **không tự nhận diện**.
- Mã nhóm → đoạn mở đầu:
  `tan_tu`→`c1_d01`, `mon_phai`→`c1_p01`. **Mỗi nhánh có kết riêng** (không hội tụ về
  một đoạn chung — ràng buộc cũ "mọi nhánh về `c1_d18`" đã **bỏ**, `c1_d18` đã xoá).
- Nhận diện: `engine.nhan_dien_xuat_than()` dò từ khoá (bỏ dấu tiếng Việt). Không khớp → `tan_tu`.
- Người chơi có 2 cách chọn: bấm 1 trong 2 nút (gửi `nhom`) HOẶC gõ tự do (server tự nhận diện).
- Lựa chọn riêng theo nhóm: dùng `dieu_kien: {"nhom": ["mon_phai", ...]}`.
- API: `POST /api/new` nhận `{ten, xuat_than, nhom}`; `GET /api/xuat_than` trả danh sách nhóm.
- **Quy ước gọi tên nhánh:** luôn gọi **tên đầy đủ** (tán tu · môn phái) khi trao đổi
  với người dùng — **không dùng ký hiệu** (d/p).

## PHẠM VI XÂY DỰNG — CHỈ 2 NHÁNH (chốt 2026-11-12)

**Chỉ xây 2 nhánh: tán tu + môn phái.** Người dùng làm một mình, không test hết được.

**3 nhánh dược đồng / gia tộc / hắc đạo đã GỠ** khỏi game (chưa xong: thiếu cơ duyên
riêng, lỗi canon `linh thảo`/`Trúc Cơ`, từng dùng chung đoạn kết `c1_d18`). Gỡ để
người chơi không gặp truyện lỗi.

- **Ý tưởng + bản thảo cũ giữ ở** `tai-lieu/Y-TUONG-3-NHANH-CHUA-XAY.md`
  và `tai-lieu/chuong1-3-nhanh-chua-xay.json` — để **xây lại sau**.
- **Bật lại:** thêm nhóm vào `game/xuat_than.json` + thêm đoạn vào `chuong1.json`
  (theo đúng 4 bước cơ duyên + quy tắc hệ thống ở dưới) + thêm test.

## 2 CƠ DUYÊN — mỗi nhánh một cơ duyên (BẮT BUỘC)

Mỗi nhánh phải có **cơ duyên riêng** — thứ đưa người chơi từ phàm nhân lên con đường
tu luyện. Cơ duyên KHÔNG được rơi vào tay người chơi một cách vô cớ.

**Quy tắc vàng — "làm sao CÓ cơ duyên" (4 bước, mọi nhánh phải theo):**
1. **Nghe đồn / manh mối** — nhân vật biết tới cơ duyên qua lời đồn, người kể, hoặc
   vật lạ (không tự nhiên xuất hiện).
2. **Đi tìm** — nhân vật phải CHỦ ĐỘNG tới nơi (có lựa chọn đi / không đi).
3. **Thử thách** — cơ duyên thử lòng (xương khô kẻ tới trước, câu hỏi, đánh đổi).
   Cho thấy nguy hiểm là THẬT, người khác đã chết vì nó.
4. **Nhận** — cơ duyên chọn chủ (có lý do). **Lý do tùy nhánh:**
   - **Nhánh xuyên không** (tán tu, môn phái): linh hồn "sạch/lạ" vì không thuộc
     thế giới này.
   - **Nhánh bản địa** (dược đồng, gia tộc, hắc đạo): lý do **trong thế giới** —
     tay nghề, huyết mạch tổ tiên, sát khí/kinh nghiệm giang hồ. KHÔNG dùng lý do
     "linh hồn xuyên không".
   → sau đó mới **tu luyện** và **kết chương**.

## HỆ THỐNG & BÍ MẬT XUYÊN KHÔNG (BẮT BUỘC)

- **Cả 2 nhánh** (tán tu, môn phái) đều **xuyên không** → có **HỆ THỐNG** + biết mình
  xuyên không. (Nhánh **bản địa** — dược đồng, gia tộc, hắc đạo — nếu xây lại thì
  **KHÔNG có hệ thống**, KHÔNG biết gì về xuyên không.)
- **Giọng hệ thống** luôn viết đúng định dạng: `👁️‍🗨️ 【Hệ thống】“…”`
  Lần đầu xuất hiện (`c1_d01`, `c1_p01`) phải **giới thiệu rõ**: dòng chữ lơ lửng
  `👁️‍🗨️ 【 Hệ Thống · Nghịch Chuyển Càn Khôn 】 đã kích hoạt.` + giọng máy móc
  "Từ nay ta là hệ thống của ngươi" + người chơi liên tưởng tới trò chơi ở thế giới cũ.
  KHÔNG viết kiểu mơ hồ ("giọng nói lạnh lùng vang lên") khiến người đọc tưởng độc thoại.
- **Xuyên không là BÍ MẬT.** Người chơi **không tự khai** với người bản địa.
  Người bản địa có thể **cảm nhận hồn phách khác thường** (Tuyết Cơ, kiếm linh) —
  nhưng **không biết** "xuyên không" là gì. Người chơi né tránh ("không nhớ rõ").
- Từ **"xuyên không"** chỉ xuất hiện trong **suy nghĩ nội tâm** người chơi, KHÔNG
  trong lời thoại với người bản địa.
- Nhân vật bản địa **không có kiến thức meta** (không biết tương lai Hàn Lập).
  Chỉ biết Hàn Lập qua **quan sát/lời đồn** trong thế giới.

## VĂN PHONG (BẮT BUỘC)

Người chơi kêu câu *"Thứ này… không phải **đồ bỏ**"* nghe **"lúa" (dân dã)** quá —
không hợp giọng tu tiên. Đã đổi thành **"phàm vật"**.

- **Tránh từ ngữ đời thường** trong nội tâm người chơi và lời kể: "đồ bỏ",
  "đồ nhặt", "chờ chết"… → dùng từ Hán-Việt/văn vẻ hợp bối cảnh
  ("phàm vật", "tầm thường", "vô danh"…).
- **Ngoại lệ:** nhánh **tán tu** (ăn mày) — giọng dân dã ở đây là **dụng ý**
  (thân phận thấp), giữ nguyên.
- Câu nội tâm *…* phải gãy gọn, sắc — không giải thích dài dòng.

| Nhánh | Cơ duyên | Cơ chế | Kết chương 1 |
|---|---|---|---|
| **Tán tu** | Hồng Trần Kiếm Hạp (cặp kiếm dài-ngắn + kiếm linh) | Hấp thu **hồng trần** để mạnh; phải đi giữa đời, không ẩn tu | ✅ `c1_d17` |
| **Môn phái** | Ngọc cốt bí ẩn (đào ở vườn thuốc, Mạc Đại Phu để ý) | Hấp thu **linh khí** nhanh gấp mấy lần; giấu kín vì môn võ lâm | ✅ `c1_p19` |

**2 nhánh đã xong (chuẩn mẫu).** 3 nhánh dược đồng / gia tộc / hắc đạo đã gỡ —
xem `tai-lieu/Y-TUONG-3-NHANH-CHUA-XAY.md`.

## Cần làm tiếp

1. ~~Người dùng duyệt giao diện 1 cột~~ ✅
1b. ~~Giao diện cơ duyên trong túi (viền nhiều màu + bấm xem thông tin)~~ ✅
1c. ~~Thư viện ảnh cảnh truyện + giao diện hiển thị theo đoạn (Chương 1, 4 ảnh thử)~~ ✅
2. Backend game Python + tích hợp LLM (theo cơ chế chương + đoạn)
3. Nội dung Chương 1 (Dã Lang Bang), Chương 2 (Huyết Sát Thí Luyện), Chương 3
4. Thư viện ảnh/video: mở rộng đủ Chương 1 (~19 ảnh) + video ngắn (chuỗi ảnh + hiệu ứng)
5. *(giai đoạn sau)* Nghề phụ + thị trường kinh tế

## Xưởng ảnh tự động (GitHub)

Xưởng ảnh giờ chạy **trên GitHub**, không cần agent:

- **Xưởng tĩnh** (prompt + nút copy + trạng thái ảnh): `docs/xuong/index.html`,
  dựng bằng `python3 tools/build_xuong.py`. Bố cục **3 tầng**: PHẦN (dùng chung giao diện /
  nhánh tán tu / nhánh môn phái) → NHÓM CẢNH (cảnh liên tiếp trong truyện) → TỪNG ẢNH.
  Dữ liệu bố cục: `XUONG_PHAN` + `NHOM_CANH` trong `tools_server.py`. Ảnh mẫu để riêng
  ở thư viện (`THU_VIEN_THU_TU`), không đánh số trùng.
  - Prompt 3 mức: `build_gop_prompt_phan()` (toàn phần), `build_gop_prompt_canh()`
    (cả nhóm cảnh, kèm nhắc đính kèm ảnh mẫu), và prompt từng ảnh (`prompt_gui_ai`).
  - Số hiển thị C.x/D.x/P.x do `so_hien_thi()`; `ten_sach()` bỏ mã đợt cũ (B.x/C.x/D.x)
    khỏi tên để không trùng số mới.
  - **Hai nhánh KHÔNG dùng chung ảnh**: mỗi nhánh có ảnh riêng (nhánh tán tu: `bc_cho_01`,
    `bc_tan_hoang`, `bc_binh_minh`; nhánh môn phái: `bc_quan_nuoc`, `bc_mon_phai_tan_hoang`,
    `bc_binh_minh_ngoc_cot`). Muốn thêm ảnh thì thêm vào `ASSETS` + `DOAN_CUA_ANH` +
    `NHOM_CANH`, rồi gửi ảnh để bot tự gán.
  - **Bẫy ID trùng**: thẻ chứa và ô `<textarea>` phải khác `id` (ô chữ dùng `<id>-t`),
    nếu không `getElementById` trả về thẻ và nút copy hỏng.
- **Người dùng làm**: copy prompt → vẽ → **bấm nút 📤 ngay trên thẻ** (ảnh) hoặc **📤 cả nhóm**.
  Nút mở Issue **điền sẵn dòng `mã-ảnh: <key>`** (một dòng mỗi ảnh, đúng thứ tự) nên bot gán
  thẳng theo mã, **không cần AI đoán**. Hoặc bỏ ảnh vào `xuong-inbox/<mã>/`.
  - `ma_anh_trong()` trong `tools/xu_ly_inbox.py` đọc các dòng `mã-ảnh:`; `tai_tu_urls()`
    gán mã theo thứ tự URL. Thừa URL thì bot tự đoán như cũ.
- **GitHub Action** `.github/workflows/xuong-anh.yml` tự: nhận diện → nén → lưu
  (`assets/` + `docs/assets/`) → ghép vào đúng đoạn `chuong1.json` → cập nhật thư viện →
  dựng lại Xưởng → commit → deploy Pages → trả lời trong Issue.

Các mô-đun:
- `xuong_tu_dong.py` — luồng xử lý: `nhan_dien()` → `luu_va_ghep()`.
- `tools/xu_ly_inbox.py` — CLI: `--inbox xuong-inbox` hoặc `--urls-file <issue.md>`.
- `tools/bao_cao_issue.py` — sinh bình luận báo cáo trong Issue.
- `tools/build_xuong.py` — dựng Xưởng tĩnh.
- `tools_server.py` — thêm `DOAN_CUA_ANH` (ảnh → đoạn), `XUONG_PHAN` + `NHOM_CANH`
  (bố cục Xưởng), `ma_anh()`; `ROOT` động; `load_env()` đọc cả biến môi trường.

**Bản đồ ảnh → đoạn** nằm ở `DOAN_CUA_ANH` trong `tools_server.py`. Ảnh mới (D.x) thay
ảnh dùng chung ở đúng đoạn của nó (mỗi cảnh một ảnh riêng). Thêm ảnh mới thì thêm key vào
`DOAN_CUA_ANH` + `NHOM_CANH` (thêm nhóm cảnh hoặc bỏ vào nhóm có sẵn).

## Xưởng video (trailer intro)

Trang `docs/xuong-video/index.html`, dựng bằng `python3 tools/build_xuong_video.py`
(gọi được bằng hàm `build_va_ghi()`).

- Dữ liệu: `CANH_VIDEO` trong `tools/xuong_video.py` — 14 cảnh `v01`…`v14`, tổng **72 giây**.
  Timecode **tự tính** từ `giay` của từng cảnh (`moc_thoi_gian()`, `tong_giay()`, `mmss()`),
  không hardcode — sửa độ dài một cảnh là cả bảng và prompt tổng tự cập nhật.
- Ảnh trailer là khung **9:16 (1080×1920)**, KHÁC ảnh game (thẻ 3:4 chừa chỗ chữ).
  Không dùng lại ảnh game làm trailer.
- Prompt: từng cảnh (tiếng Anh + tiếng Việt), từng phần, **prompt tổng** (14 ảnh một lần),
  prompt chuyển động cho công cụ image-to-video, và prompt nhạc 72 giây.
  - Prompt tiếng Anh phải **thuần Anh**: dùng `CAMERA_EN` để dịch trường chuyển động và
    `ten_en` cho tên cảnh. Chỉ tên riêng (Hồng Đức Tu Tiên Lộ, Phàm Nhân Tu Tiên) là tiếng Việt.
  - `GOI_Y_NHAC` là bộ ba `(mốc, ghi chú Việt cho người dùng, chỉ dẫn Anh cho AI tạo nhạc)`.

**Gửi ảnh từ web (không cần terminal)** — giống Xưởng ảnh:
- Mỗi thẻ cảnh có ô `📷 Bấm vào đây để chọn ảnh` + nút `📤 Gửi ảnh này` + `🔄 Kiểm tra`.
  Ảnh nén ngay trên máy (canvas, cạnh dài ≤1920) rồi PUT thẳng lên GitHub qua API.
- Mục **📤 Gửi cả loạt ảnh** cho chọn nhiều ảnh; khớp cảnh theo **tên file**
  (`canhTheoTen()` so `CANH[i].f` trước, rồi `includes(mã)`). Ảnh không khớp bị bỏ qua kèm gợi ý.
- Token GitHub lưu ở `localStorage` khoá `xuong_video_gh_token` (tách khỏi `xuong_gh_token`
  của Xưởng ảnh để hai trang không giẫm chân nhau).
- **Đích PUT là `xuong-inbox/<mã>/<mã>.jpg`, KHÔNG phải `docs/assets/video/`** — cố ý:
  chỉ push vào `xuong-inbox/**` mới kích hoạt `xuong-anh.yml`, mà workflow đó mới là thứ
  chạy `xuong_tu_dong.py` (resize + đệm khung) rồi dựng lại trang. Đẩy thẳng vào
  `docs/assets/video/` thì file lên nhưng thẻ cảnh **không** đổi trạng thái.
- `CANH` trong JS sinh từ `_canh_json()` (`key`/`file`/`ten_en`); chuỗi `</` được thoát
  thành `<\/` để không cắt sớm khối `<script>`.

**Chủ đề trailer — ĐỌC KỸ, dễ hiểu sai**: game là **đồng nhân Phàm Nhân Tu Tiên**, nhưng
nhân vật chính là **người chơi (NV-1)**, KHÔNG phải Hàn Lập. Hàn Lập (NV-4) là **nhân vật
thứ hai**, ngang tầm, và quan hệ của họ là **đối đầu / hảo hữu tuỳ lựa chọn của người chơi**
(trong `chuong1.json`, người chơi bám theo Hàn Lập lên hậu sơn, và Hàn Lập nói *"Ta không
giết ngươi, không phải đêm nay. Nhưng từ giờ, ta sẽ để mắt tới ngươi"*). Vì vậy:
- Cảnh 1–4 dùng canon **NV-1** (người chơi), không phải Hàn Lập.
- Cảnh 13 là **đối đầu hai người**, khai `"canon": ["NV-1", "NV-4"]` và dùng `{canon0}`,
  `{canon1}` trong prompt — `prompt_canh()` thay từng cái một.
- KHÔNG bao giờ để trailer chỉ có Hàn Lập: người xem sẽ tưởng game kể chuyện Hàn Lập.

**Chữ trên hình là lớp ghép riêng, không nằm trong ảnh.** Mọi prompt đều cấm chữ
(`no text, no letters`) vì AI vẽ chữ tiếng Việt sai dấu. Chữ lưu ở `CANH_VIDEO[i]["chu"]`,
ghép ở CapCut, và `tools/dung_video_xem_truoc.py` vẽ bằng DejaVuSerif-Bold (đủ glyph tiếng Việt;
`fc-list :lang=vi` để kiểm tra font khác).

**Sinh ảnh bằng Gemini: model ảnh bị chặn ở free tier.** `gemini-3-pro-image`,
`gemini-3.1-flash-image`, `gemini-2.5-flash-image` đều trả **429 với `limit: 0`** (không phải
quota tạm thời — free tier không cấp quyền sinh ảnh), `gemini-3.8-flash` trả 503. Cả 4 khoá
`geminikey`…`geminikey3` đều vậy. Muốn tự động sinh ảnh phải bật billing. Vì thế ảnh hiện do
người dùng tạo bằng công cụ ngoài rồi úp qua Xưởng.

**Úp video intro vào game** — một đường duy nhất, làm được trên điện thoại:
thả file vào ô **🎬 Video intro** ở trang Xưởng. Trang cắt thành mảnh 8 MB, đẩy vào
`xuong-video-inbox/`, rồi `ghep-video.yml` ghép → nén → đưa vào game → dọn inbox.

Vì sao phải chia mảnh (đo thật, không suy đoán):
- `api.github.com` **có** CORS (`allow-origin: *`), `uploads.github.com` (Release
  asset) **không có** → trình duyệt không đẩy asset Release được.
- `POST` asset qua `api.github.com` → 404, không có endpoint đó.
- Mỗi `PUT` ở `api.github.com` bị trần ~30 MB: 29.1 MB ✅, 42.5 MB → 422 "too large",
  61.6 MB → 504. Mảnh 8 MB (base64 ~11 MB) nằm dưới trần rất xa.

`ghep-video.yml` chỉ chạy khi thấy `<lô>.json`, mà trang đẩy nó **sau** khi hết mảnh —
nên không bao giờ ghép file còn thiếu phần. Nó kiểm tra kích thước ghép khớp khai báo,
kiểm tra ffmpeg đọc được, và **dọn inbox cả khi nén lỗi** (không thì mẩu tin nằm lại,
mỗi push sau lại fail lại).

Đo thật end-to-end: 61.6 MB → 8 mảnh đẩy 25s → nén 13.8 MB trong 1m54s → HTTP 200.


**Ba màn vào game** — `play.html` đi theo thứ tự: `.bia` (z-index 14) → `.phim-intro` (11)
→ `.setup` chọn nhánh chơi (9). Không còn màn chữ bản thảo riêng: bấm "Vào game" là phim
intro chạy toàn màn hình, hết phim tự sang màn chọn nhánh.

- Phim dùng `object-fit:cover` để **phủ kín** màn hình. Phim gốc 1080x1920 (dọc), nên
  trên màn ngang nó bị cắt trên/dưới — cố ý, để không có dải đen hai bên. Đừng đổi lại
  thành `contain`: người dùng đã yêu cầu rõ phim phải tràn viền.
- `.bia` là `div` nền ảnh (không phải `<img>`) nên file thiếu không hiện icon ảnh hỏng.
  CSS khai 2 lớp: `docs/assets/bia.jpg` (người dùng tự úp ở Xưởng ảnh) rồi lùi về
  `assets/video/v14_nen_tieu_de.jpg`.
- Video **chỉ tải sau khi bấm nút** (`src` gán lúc đó), người ghé xem không phải tải 14 MB.
- Toàn bộ đường đi bìa → phim → chọn nhánh nằm trong **một script riêng đặt ngay sau màn
  bìa**, không nằm trong script chính. `engine.js`/`ai.js` lỗi là script chính chết; nếu
  nút nối ở đó thì người chơi kẹt vĩnh viễn ở màn bìa. Đã test bằng cách cho cả hai file ném lỗi.
- Script riêng tự đọc `localStorage["hdttl_phien"]`: đang chơi dở thì bỏ qua cả bìa lẫn
  phim, vào thẳng truyện. Việc này **phải** kiểm tra trong script riêng, không đợi script
  chính, cùng lý do trên.
- Phim có 3 đường thoát để không bao giờ kẹt: hết phim (`ended`), nút "Bỏ qua ▸", và
  `error`/quá 12 giây chưa phát được. Safari iPhone chặn tự phát có tiếng → tự tắt tiếng
  để phim vẫn chạy.

**Màn chọn xuất thân (`.setup`)** — giao diện đã chốt theo "hướng C" (2026-11-20):
thẻ ngang một cột, mỗi thẻ có **ảnh nền lấy từ chính đoạn mở đầu** của xuất thân đó
(`bc_cho_01` cho tán tu, `bc_tan_xa_sang` cho môn phái), tên lớn font `--brush`, dấu ✓ đỏ
khi chọn. Chọn thẻ thì **cả nền màn hình đổi ảnh** (`.nen-chon`, `opacity:.42`) và hiện
**trích đoạn mở đầu thật** ở `#xtTrich` (câu đầu của `doan_dau`, cắt ~120 ký tự).
Ô "xuất thân tự do" thu sau một link `#xtTuDo`, mở ra `#xtO`.

- Mỗi xuất thân **có chỉ số khởi đầu riêng** (từ 2026-11-20, người dùng đã cho phép sửa
  dữ liệu + engine). Khai ở **`chi_so_dau`** trong `xuat_than.json`; engine đọc qua
  `chi_so_dau_cua(nhom)`, thiếu thì rơi về `CHI_SO_DAU_MAC_DINH` (nhóm ẩn không khai).
  `game_server.py` trả `chi_so_dau` trong `/api/xuat_than`; thẻ vẽ dải số bằng `daiChiSo()`.
  Xem bảng số + lý do dẫn nguyên văn ở `tai-lieu/NHAT-KY.md`.
- **Đổi số khởi đầu thì PHẢI mô phỏng lại cả 2 nhánh tới hết chương.** Tu vi khởi đầu
  quyết định mốc lên tầng, mà nguyên văn đã chốt cảnh giới cuối chương: `c1_d17` nói tán tu
  *"Luyện Khí tầng ba"*, `c1_p12` nói môn phái *"Luyện Khí tầng hai"* và `c1_p19` vẫn tầng
  hai. Đặt sai (vd môn phái tu vi 8) là môn phái kết ở tầng 1 — truyện nói một đằng, bảng
  chỉ số nói một nẻo. Test trong `game/_test_engine.js` khoá 5 mốc này.
- Bản `game/` lấy ảnh/trích đoạn qua `fetch("/game/chapters/chuong1.json")` +
  `fetch("/game/xuat_than.json")` — **đường dẫn phải có tiền tố `/game/`** vì
  `game_server.py` phục vụ từ gốc repo, và `/api/xuat_than` **không** trả `doan_dau`.

**Trang gốc `docs/index.html` KHÔNG còn là portal.** Người dùng đã yêu cầu bỏ hẳn giao
diện portal (tiêu đề + mô tả game + thẻ "Xưởng video"), nên trang gốc giờ chỉ là một
redirect `<meta refresh>` sang `game/play.html`. Không thêm lại menu, không thêm thẻ giới
thiệu. Mở link gốc là vào thẳng game.

Các thư mục `docs/xuong/`, `docs/xuong-video/`, `docs/luu-tru/ban-thao/` **vẫn còn** trong
repo và vẫn truy cập được bằng URL trực tiếp, chỉ không còn liên kết từ đâu tới. Đừng xoá
trừ khi người dùng nói rõ — họ còn dùng Xưởng video để dựng trailer.

### HAI bản `play.html` phải đồng bộ giao diện

- `game/play.html` — bản Python (chạy `game_server.py`, KHÔNG deploy)
- `docs/game/play.html` — bản JS (deploy lên Pages, người dùng chơi)

Hai file khác nhau phần nối backend (`/api/*` vs `Engine.*`) nhưng **giao diện + CSS
phải giống nhau**. Khi sửa giao diện một bản, sửa luôn bản kia. Bản Python không có
nút Cài đặt key (key nằm ở `.env`), nên đừng bê nguyên nút đó sang.

Lưu ý harness: iframe **phải cùng origin** với trang cần đo, nếu không sẽ dính
`contentDocument = null`. Cách gọn: đặt file harness vào chính thư mục server phục vụ
(ví dụ để tạm ở gốc dự án rồi mở qua `game_server.py`), dùng đường dẫn tương đối
(`/game`). Nhớ xoá file harness sau khi đo.

### Prompt tiếng cảnh: phải là ÂM THANH GAME, không phải bản ghi thực địa

Prompt cũ mở đầu bằng "Field recording of…" và cấm nhạc/nhạc cụ. Kết quả: file
nghe như radio hoặc như micro đặt giữa chợ thật — người chơi chê đúng. Âm thanh
game là **thiết kế có lớp**: nhạc cụ (đàn tranh, sáo, trống, chiêng, đàn bầu),
thang ngũ cung, nền đệm, sạch và cách điệu. Không phải bản ghi hiện trường.

Quy tắc khi viết prompt trong `game/du_lieu_am.py`:

- mở đầu bằng "Game ambience loop for …", nói rõ **NOT a field recording**
- liệt kê từng **lớp** (layer): nhạc cụ nào, làm gì, nền đệm là gì
- **10 giây**, không phải 30 — đúng bằng `GIAY_CANH` trong game
- cấm: lời nói hiểu được, giọng đọc, giọng radio, lo-fi, hiss băng, static
- `DUOI` giữ phần 10 giây/loop; `CHUNG` giữ quy ước chung. Đừng lặp lại
  hai lần trong cùng một prompt.

### Prompt phải nói RÕ nhạc lặp lại, không chỉ ghi chữ "loop"

Ghi "seamless 10-second loop" là **chưa đủ**: công cụ sinh âm thanh vẫn trả về
một bản 10 giây **có mở đầu và có kết thúc** — hết là hết, không lặp. Phải nói
cả ba điều:

1. **Nhịp và số ô nhịp** sao cho chia chẵn 10 giây. Một ô 4/4 dài `4*60/nhịp`
   giây, nên số ô = `nhịp/24`. Chỉ nhịp bội của 24 mới chẵn:
   48 BPM → 2 ô, 72 BPM → 3 ô, 96 BPM → 4 ô, 120 BPM → 5 ô.
2. **"The musical pattern must repeat at least twice inside these ten seconds"**
   — nói thẳng là nền chạy tiếp, không phải bản nhạc có đầu có cuối.
3. **"No intro, no outro, no build-up, no final chord, no resolution"** — cấm
   mọi dấu hiệu kết thúc. Câu chốt: "the first beat and the last beat are the
   same point in the cycle".

Cảnh thưa (núi, miếu, tĩnh) dùng 48 BPM × 2 ô; cảnh vừa (vườn, đêm) 72 × 3;
cảnh đông (chợ, sân, làng) 96 × 4. `duoi(nhịp, ô)` trong `game/du_lieu_am.py`
có `assert` chặn mọi tổ hợp không ra đúng 10,00 giây — đừng bỏ assert đó.

### File tiếng tải lên phải được nối vòng, không phát thẳng

`cho.mp3` có **0,3 giây lặng câm ở đầu** và kết thúc giữa tiếng. Code cũ đặt
`nguon.loop = true` nên mỗi vòng nghe một khoảng câm rồi tiếng cụt. Đã sửa bằng
`lamVongKhit()` trong `play.html` (cả hai bản): cắt lặng hai đầu, rồi crossfade
80ms chồng đuôi lên đầu.

Đo được: bước nhảy tại chỗ nối từ **giật** thành **0,6 lần mức trung bình**
(mượt hơn cả tiếng bình thường trong file); chênh âm lượng hai đầu 2,2 dB; file
6,06s → 5,7s. Không có hàm này thì **mọi file anh tải lên đều bị lỗi này**, vì
công cụ sinh âm thanh luôn thêm lặng ở đầu.

### Sửa mã sinh trang thì phải sửa ở NGUỒN, không chỉ file sinh ra

`docs/xuong-am/index.html` là **file sinh ra** từ `game/tao_xuong_am.py` +
`game/xuong_am.js`. Sửa thẳng file sinh ra rồi chạy lại script là **mất sạch**.
Đã từng mất bản sửa token vì lý do này. Sửa JS ở `game/xuong_am.js`, sửa HTML ở
`game/tao_xuong_am.py`, rồi chạy `python3 game/tao_xuong_am.py`.

### Trạng thái lưu trong localStorage phải KHÔI PHỤC lên giao diện

Token Xưởng âm thanh lưu đúng vào `localStorage` và việc gửi file vẫn chạy, nhưng
**giao diện không khôi phục khi tải lại**: ô `<input type="password">` luôn trống
(trình duyệt không điền lại), không có dòng nào báo "đã kết nối". Người dùng tưởng
mất token và dán lại mỗi lần — mất công mà không cần thiết.

Quy tắc: **mọi thứ lưu vào `localStorage` phải có hàm khôi phục chạy lúc tải trang**,
và phải hiện trạng thái cho người dùng thấy. Đừng chỉ đọc nó lúc dùng.

Đã sửa bằng `ghKhoiPhuc()` (gọi ở cuối `<script>`):

- kiểm tra lại token với GitHub rồi hiện "✅ Đã kết nối … — không cần dán lại"
- đổi `placeholder` thành "Đã lưu token — để trống nếu không đổi"
- **không xoá token khi mất mạng** — chỉ báo chưa kiểm tra được
- token hết hạn (401) thì báo rõ và hướng dẫn dán token mới
- `ghLuuToken()` dùng `|| ghToken()`: bấm Lưu khi ô trống thì kiểm tra lại token cũ,
  không báo oan "chưa dán token"

Đã đo 7 tình huống bằng trình duyệt thật (có chặn `api.github.com` để giả lập):
chưa có token, vừa lưu, tải lại trang, bấm Lưu khi ô trống, token hết hạn, mất mạng,
bấm Quên token. Cả 7 đúng.

### Âm thanh cảnh: PHẢI có cao độ, không được là nhiễu lọc

**Bài học đắt nhất về âm thanh.** Ba vòng sửa liên tiếp tôi đo crest, LUFS, cắt đỉnh,
limiter — đều đạt, mà người dùng vẫn bảo "đây là âm thanh game à?". Đo đúng nhưng
**sai hướng thiết kế**: tôi tối ưu chất lượng của một thứ vốn không phải nhạc.

Tiếng cảnh cũ là **nhiễu hồng lọc bandpass + vài tiếng ngẫu nhiên**. Đo được:

- độ phẳng phổ **0,738** (1,0 = nhiễu trắng) — không có cao độ
- nền nhiễu chiếm **70–88%** năng lượng ở cả 9 cảnh; sự kiện chỉ 12–30%
- các hàm "tiếng người" (`raoHang`, `noiChuyen`, `damDong`) dùng 5–7 lần
  `Math.random`, **0 dao động** — tức là nhiễu, không phải âm có cao độ

Tai nghe ra "radio không bắt được đài", và người dùng nói đúng.

**Cách kiểm trước khi tin là xong:** đo độ tuần hoàn (autocorrelation) và độ phẳng
phổ. Nhạc thật cho R ≈ 1,0; nhiễu trắng cho R ≈ 0,02. Đừng chỉ đo to/nhỏ.

**Bản đúng hiện tại** (`BAN_NHAC` + `bufDay/bufSao/bufTrong/bufChieng/bufBau`):

- thang **ngũ cung** `[0,2,4,7,9]`, mỗi cảnh một nốt gốc riêng (D3…E4)
- **đàn tranh = Karplus-Strong**: nhiễu chỉ để kích dây, cao độ do vòng lặp trễ tạo ra
- dựng sẵn buffer một lần cho mỗi cao độ rồi `start()` đúng lúc — tổng hợp bằng
  oscillator cả chuỗi dài thì nặng và lệch nhịp
- kết quả đo: 45/45 nốt đúng, lệch tối đa **16 cent**; R = 1,000 (đàn tranh), 0,968 (sáo)

**Hiệu chuẩn âm lượng phải lặp, không được tính một lần.** Bù tuyến tính một lượt
cho ra chênh 9,3 dB và 14 mẫu chạm limiter, vì đỉnh và RMS không tỉ lệ với nhau khi
đổi gain có limiter phía sau. Dùng vòng lặp 6 lần (`g = g * DICH/rms`, chặn đỉnh)
→ hội tụ chênh **1,4–1,6 dB**, 0 mẫu cắt, 0 lần limiter can thiệp.

### Âm thanh: tổng hợp trong máy, có thể thay bằng bản ghi thật

Game dùng bốn tiếng ngắn (`bam`, `lat`, `lui`, `mo`) dựng bằng Web Audio ngay trong máy.
**Đừng thêm file mp3/wav vào repo** trừ khi người dùng yêu cầu. Repo vẫn không chứa file
âm thanh nào — xem mục dưới.

**Ngoại lệ có kiểm soát: Xưởng âm thanh.** Người dùng tự tạo bản ghi rồi tải lên qua
`docs/xuong-am/` hoặc kéo file vào một Issue có nhãn `xuong-am`. Workflow `xuong-am.yml`
nén về mp3 96 kbps, cân âm lượng −18 LUFS, đặt vào `docs/assets/am/<mã>.mp3`. Game đọc
`docs/assets/am/danh-sach.json`: nhóm nào có trong đó thì phát file, không có thì dùng
tiếng tổng hợp. **Không bao giờ im.** Đừng tự tay commit mp3 vào `assets/am/` — hãy đi
qua xưởng, để còn cân âm lượng.

Chín nhóm tiếng và prompt tạo nằm ở `game/du_lieu_am.py`; sửa prompt thì sửa ở đó rồi
chạy `python3 game/tao_xuong_am.py`. Nhóm tiếng suy ra từ tên file ảnh cảnh
(`nhomCanh`), nên 68 ảnh chỉ cần 9 file tiếng.

Bốn điều đã trả giá để biết, đừng làm lại:

1. **Đường chính phải là Issue, không phải token.** Người dùng chỉ có điện thoại; bắt
   tạo personal access token rồi dán vào trang là quá khó. Kéo file vào Issue GitHub
   thì không cần token và làm được trên iPhone. Trang xưởng có nút gửi trực tiếp,
   nhưng đó là đường phụ.
2. **`loudnorm` một lượt đo sai trên file ngắn.** Đặt `I=-23` mà đo lại ra −24.3 dBTP
   (nhỏ hơn cả đỉnh mục tiêu). Phải đo trước bằng `print_format=json` rồi áp
   `measured_I/measured_TP/measured_LRA/measured_thresh`. Đã sửa trong `tools/xu_ly_am.py`.
3. **Mục tiêu −18 LUFS, không phải −23.** −23 là chuẩn phát thanh cho nghe bằng tai
   nghe; tiếng nền phát qua loa điện thoại ở mức đó nghe như không có.
4. **Sinh trang HTML thì phải kiểm thẻ `<script>` còn hay không.** Đã từng ghép JS vào
   template mà quên bọc `<script>`: hàm `ghLuuToken` có trong file nhưng trình duyệt coi
   là văn bản, bấm nút không làm gì và chỉ báo `Can't find variable`. Kiểm bằng
   `grep -c "<script"` và thử bấm nút thật, đừng chỉ `node --check`.

Ba điều dễ làm sai khi sửa `keTieng`:

1. **Mọi thành phần phải đi qua bộ điều âm lượng.** Nếu nối tắt một nguồn vào bộ lọc thì
   tín hiệu đi hai đường: bị nhân đôi (đỉnh > 1.0, nghe "bụp") và thành phần đó to hơn
   mức đặt ra. Đã từng đo được 0.544 trong khi đặt `vol: 0.075`.
2. **Nhiều tiếng chồng nhau sẽ vượt 1.0.** Bấm 10 lần sát nhau từng cho đỉnh 1.485. Phải
   giữ `DynamicsCompressor` trước loa (`loaTieng`), đừng nối thẳng vào `destination`.
3. **Đo bằng `OfflineAudioContext`, đừng đo qua `requestAnimationFrame`.** rAF trong
   headless chỉ lấy được 5–6 mẫu, không đủ kết luận.

Nút tắt tiếng có **hai chỗ**: `#nutTieng` trên thanh trên và `#setupTieng` trong thẻ tạo
nhân vật (ở màn tạo nhân vật thanh trên bị lớp phủ che nên phải có nút riêng trong thẻ).
Trạng thái nhớ ở `localStorage` khoá `hdttl_tieng`.

**Mọi đường vào game đều phải đánh thức tiếng, không chỉ nút "Vào game".** Đây là gốc của
lỗi "bấm lần đầu kêu, lần sau không". Có hai đường vào và chúng khác nhau:

- Bấm "Vào game" ở bìa → có cú chạm → `moKhoaTieng()` chạy → tiếng sống.
- Đang chơi dở mà tải lại trang → `docPhien()` → `vaoThangNhanh()`, **không có cú chạm nào**
  → tiếng ngủ im. Đo được: `state = "suspended"`, bấm → tín hiệu 0.

Nên `thucDayTieng()` được gắn vào `touchstart`/`click`/`visibilitychange` ở cấp `document`,
gọi lại 60ms sau khi phim intro nhả phiên âm thanh, và đánh thức ngay ở cú chạm đầu khi khôi
phục phiên.

**iOS có ba trạng thái, không phải một.** `suspended` (bị ẩn), `interrupted` (cuộc gọi tới,
app khác chiếm phiên âm thanh), `closed` (bị thu hồi khi chạy nền lâu). Chỉ `resume()` khi
`suspended` thì hai trạng thái sau là **im vĩnh viễn**. Nay: `closed` thì dựng lại context
(`taoCtxTieng`), còn mọi trạng thái khác `"running"` thì `resume()`.

**Đang ngủ thì đừng bỏ tiếng, hãy phát sau khi tỉnh.** `resume().then(() => keTieng(loai))`.
Bỏ tiếng thì cú chạm đầu sau khi mở lại trang mất âm — người chơi nghe ra là "bấm không kêu".

**Cờ chặn bấm phải nhả trong `finally`.** `chon`, `tuDo`, `lui` bật `dangCho = true` rồi tắt ở
cuối hàm; nếu `hienThi` ném lỗi thì cờ kẹt và **mọi lần bấm sau bị chặn từ đầu** — không kêu,
không chuyển trang. Đã bọc `try/finally` cả ba.

### Tiếng theo cảnh: nhiễu nâu lặp vòng, mặc định tắt

68 ảnh chia chín nhóm trong `nhomCanh()`; mỗi nhóm một lớp nhiễu nâu lặp (buffer 2 giây,
`loop = true`) lọc bandpass, thêm lớp "thưa" hẹn giờ ngẫu nhiên (chuông, dế, gió).

Bốn điều dễ làm sai:

1. **`src` của ảnh là đường dẫn đầy đủ, không phải tên file.** Phải `split("/").pop()` trước khi
   so tiền tố `bc_`, nếu không `nhomCanh` trả `""` và cảnh im hoàn toàn.
2. **Ảnh nhân vật/vật (`nv_*`, `vt_*`) không được cắt tiếng nền.** Chúng là cận cảnh giữa
   chừng, không phải nơi chốn mới. Cắt nền ở đó nghe như tiếng hỏng đúng lúc đang đọc.
3. **Đừng đặt nút mới lên thanh trên.** Đo trên màn 320px: thêm một nút làm thanh cao thêm
   52px, khung truyện còn 238px. Game đọc chữ nên đây là hồi quy thật. Nút phụ để trong bảng
   Hệ Thống.
4. **Tiếng nền phải nhỏ hơn tiếng thao tác khoảng 10 lần.** Đo được: nền 0.023–0.043, tiếng bấm
   0.333. Nếu để nền to hơn thì người chơi tắt tiếng và mất luôn tiếng bấm.

### Kiểm hành vi, không chỉ kiểm "có tín hiệu"

Bốn lỗi dưới đây đều lọt qua lần kiểm đầu vì phép thử quá yếu. Ghi lại để không lặp:

- **"Có tiếng" không bằng "tiếng đổi đúng".** Bản `game/play.html` từng thiếu `doiCanhTieng(ten)`
  trong `hienThiAnh`; tiếng nền vẫn kêu vì đó là tiếng của cảnh đầu, nhưng không bao giờ đổi.
  Phép thử đúng: **đi qua ≥6 cảnh và đếm số nhóm khác nhau** — phải > 1. Một lần đo tín hiệu
  duy nhất không phân biệt được "đang chạy" với "đang đứng yên".
- **`catch Exception` nuốt lỗi thành lỗi im lặng.** Nhánh dự phòng của khâu nén ảnh ghi nguyên
  bản khi Pillow lỗi, không để lại dấu vết — nên PNG đội lốt `.jpg` mà không ai biết. Khi một
  phép thử về "kích thước/kết quả phải khác đi" hỏng, **kiểm byte đầu file và kích thước thật**,
  đừng suy đoán nguyên nhân.
- **Khởi động lại tiến trình server sau khi cài thư viện Python.** Tiến trình cũ giữ
  `sys.modules` cũ, nên `import PIL` vẫn thất bại dù `pip install` đã xong. Triệu chứng dễ nhầm:
  gọi hàm trực tiếp thì đúng, gọi qua server thì sai.
- **Playwright tự huỷ `confirm()`/`alert()`.** Nút có `confirm()` sẽ không chạy; đăng ký
  `page.on("dialog", d => d.accept())` trước. Nếu không, tiếng đo được là tiếng của chính cú bấm.
- **Đo âm thanh phải đo bằng RMS qua bộ lọc của loa đích, không đo đỉnh tín hiệu trong máy.**
  Bản tiếng phông cảnh đầu tiên đo đỉnh 0.023–0.043 và tôi báo "có nền" — người dùng báo
  **không nghe thấy gì**, và đúng là không nghe được: đo RMS sau khi lọc như loa điện thoại
  (highpass 700 Hz) ra −39…−50 dBFS, gần như im lặng. Hai lỗi cộng lại:
  - **Quá nhỏ.** Đặt mức để "có số trong máy" chứ không phải để nghe trên loa.
  - **Sai dải tần.** Nhiễu nâu (1/f²) dồn ~70% năng lượng dưới 300 Hz; loa điện thoại cắt
    dưới ~700 Hz, nên phần lớn tiếng **không ra khỏi loa**. Dùng **nhiễu hồng (1/f)**, đặt
    tâm dải trong 800–1500 Hz, và highpass 400 Hz để bỏ phần không phát được.
  Phép thử đúng: đo RMS từng khung (không cộng dồn), bỏ qua giai đoạn vào dần, và **đo cả
  trước lẫn sau một highpass 700 Hz** để biết bao nhiêu năng lượng thực sự ra loa. Đích:
  −30 dBFS sau lọc, ≥40% năng lượng trong dải 700–2000 Hz.
- **"Rè" gần như luôn là bộ hạn chế/nén đang phải ghì, không phải lỗi dải tần.** Đo cảnh
  chợ: trọng tâm phổ 2683 Hz, 25% năng lượng ở 2–6 kHz — tôi sửa dải tần (thêm trầm, hạ
  formant) nhưng người dùng vẫn báo rè. Nguyên nhân thật: **crest 15–25 dB** (RMS −34 dBFS
  mà đỉnh 0.115) nên muốn nghe được phải nâng 13–22×, đẩy đỉnh lên **1.9**, và bộ hạn chế
  phải ghì **5,7 dB**. Ghì 5,7 dB là biến dạng phi tuyến — tai nghe thành rè. Cách chữa
  đúng là **hạ crest tại nguồn** (nâng lớp nền, hạ tiếng nhói) chứ không phải nới ngưỡng
  hạn chế. Sau khi sửa: crest 5,8–11,9 dB, và **kiểm bằng phép thử "bộ hạn chế có can thiệp
  không"** — render với `g.gain = muc` nối thẳng vào destination, đo đỉnh; nếu đỉnh < 0.841
  (−1.5 dBFS) thì hạn chế không chạm. Đích: **0/9 cảnh**. Con số này quan trọng hơn mọi
  phép đo phổ, vì nó chứng minh tín hiệu đi qua hoàn toàn tuyến tính.
- **Đo crest phải dùng NHIỀU lần render và lấy đỉnh lớn nhất.** Sự kiện cảnh đặt ngẫu nhiên
  nên một lần render 20 giây có thể bỏ sót đỉnh. Đo 5 lần rồi lấy max: cảnh sân ra 0.132
  một lần nhưng đỉnh thật khi nhân mức là 1.92. Đo một lần sẽ kết luận sai là "không bị ghì".
- **Script đo phải ĐỌC hằng số từ file, không hardcode.** Tôi sửa `0.055 → 0.135` trong
  `play.html` rồi chạy lại test thấy số y nguyên — vì test ghi cứng `0.055`. Mất một vòng
  lặp. Đọc bằng regex từ chính file đang test, hoặc truyền vào qua `page.evaluate`.
- **Âm lượng do người dùng quyết, không do agent đoán.** Mỗi loa một khác và agent không
  nghe được. Khi không thể tự kiểm bằng tai, **thêm thanh chỉnh âm lượng** thay vì đoán
  một con số rồi tuyên bố "đã đủ to".
- **Web Audio: `resume()` là bất đồng bộ — không được `return` sau khi gọi nó.** Đây là
  nguồn của hai lỗi "bật lên thì câm" trong game:
  - `doiCanhTieng` kiểm `state !== "running"` rồi `return`, trong khi `resume()` vẫn đang
    chạy. `resume()` xong thì không ai gọi lại → im vĩnh viễn. Phải `.then(() => gọi lại)`.
  - `thucDayTieng` chỉ dựng lại lớp nền **bên trong** nhánh `state !== "running"`. Nếu lớp
    nền chết trong lúc context vẫn `"running"`, không có gì chữa. Phải kiểm tra "đáng lẽ
    phải đang chạy mà không chạy" ở **mọi** cú chạm.
  - Đừng chặn bằng `if (nhom === canhLoai) return;` khi `canhLoai` được gán **trước** khi
    biết chắc đã phát được. Chỉ bỏ qua khi **đang thực sự có lớp chạy**.
  Cách chứng minh: chạy **cùng một phép thử** trên bản cũ và bản mới. Nếu bản cũ không
  hỏng thì phép thử chưa chạm tới lỗi. Cả hai lỗi trên đều được chứng minh đúng cách đó
  (0 → 0.107 và 0 → 0.10).

**WebKit báo `interrupted` cả khi CHƯA mở khóa.** Đừng đọc đó là "bị ngắt phiên âm thanh":
đó chỉ là "chưa có cú chạm nào". Muốn biết có bị ngắt thật hay không thì phải biết context
**đã từng chạy** chưa (theo dõi qua `statechange` khi thấy `running`). Trang `docs/phong-do/tieng.html`
có cờ `daTungChay` để phân biệt; bản đầu không có cờ này nên báo cáo báo động sai.

**Máy giả lập Linux không mô phỏng `interrupted`.** Đo được `suspended` và `closed`, còn
`interrupted` phải xử lý theo tài liệu WebKit. Đừng kết luận "đã đúng trên iPhone" từ máy
giả lập. Người dùng đã xác nhận bản sửa chạy đúng trên iPhone thật (2026-11-21).

**Đừng đặt nút loa lên phim mở đầu.** Đã thử và người dùng báo nó che chữ trong phim; đã bỏ.

### Chiều cao khung: dùng `svh`, đừng dùng `vh`

Trên iPhone, `vh` và khung `position:fixed; inset:0` được tính theo **màn hình đầy đủ** (kể cả
phần thanh công cụ Safari che), nên nội dung ở đáy bị đẩy ra ngoài tầm nhìn. Đây chính là
nguyên nhân nút "Bắt đầu" ở màn tạo nhân vật không bấm được — đã sửa hai lần mới đúng gốc.

Dùng `height:100svh` cho khung và `max-height:calc(100svh - 40px)` cho thẻ, luôn kèm dòng
`vh` phía trước làm dự phòng cho máy cũ.

**Máy giả lập Linux không có thanh công cụ Safari nên KHÔNG tái hiện được lỗi này.**
Muốn tái hiện phải ép khung cao hơn vùng nhìn thấy (ví dụ `#setup{height:844px}` với viewport
390×664), rồi đo bằng `elementFromPoint` dọc theo nút xem bao nhiêu điểm bấm được.
