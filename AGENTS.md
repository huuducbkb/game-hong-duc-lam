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

## 🔁 BÀN GIAO — kết thúc MỌI phiên làm việc, không chờ ai nhắc

Người dùng chỉ có điện thoại, không có terminal, và đã nhiều lần phải mở khung chat mới
giữa việc. Chat mới **không nhớ hội thoại cũ**, chỉ nhớ repo. Vì vậy kết thúc phiên là
phải đóng gói đủ để một AI khác (hoặc chính mình ở chat mới) làm tiếp được ngay.

### Ba bước, làm đủ, không bỏ bước nào

**1. Ghi việc vào `tai-lieu/NHAT-KY.md`** — mục mới nhất trên cùng. Phải có:
ngày · người dùng yêu cầu gì · đã sửa file nào · **số đo kiểm chứng** · còn treo gì.
Ghi cái đo được, không ghi "đã làm đẹp hơn".

**2. Cập nhật `tai-lieu/VIEC-CAN-LAM.md`** — việc mới vào mục 🔴 ĐANG LÀM,
kèm **lệnh đo được** để phiên sau biết khi nào xong.

**3. Chạy `python3 tools/ban_giao.py --tu HEAD~N`** rồi **gửi nguyên danh sách link
cho người dùng trong câu trả lời cuối**. Đây là bước hay bị quên nhất.

Danh sách là **năm link cố định**, đúng thứ tự này, không phải "mọi trang vừa đổi":

| # | Tên | Đường dẫn |
|---|---|---|
| 1 | Xưởng âm thanh | `xuong-am/` |
| 2 | Xưởng ảnh | `xuong/` |
| 3 | Xưởng video | `xuong-video/` |
| 4 | Game để chơi | `game/` |
| 5 | Sơ đồ cốt truyện | `nhap/so-do-cot-truyen.html` |

Người dùng đã nói rõ: họ mở đúng năm chỗ đó để làm việc, nên gửi link trang khác
là trả lời sai câu hỏi. Script đã in sẵn năm link kèm mã HTTP.

```bash
python3 tools/ban_giao.py --tu HEAD~3   # N = số commit của phiên này
```

Script in ra: **năm link cố định** (gọi thử từng cái), link commit trên GitHub, và
cảnh báo nếu nhật ký / sổ việc chưa được commit. Script thoát mã 1 khi còn cảnh báo
— nghĩa là **bàn giao chưa xong**. Link nào trả mã khác 200 thì in kèm ⚠, đừng gửi
link đó như thể nó sống.

### Gửi link là bắt buộc, không phải tuỳ chọn

Người dùng không mở được terminal để tự tìm trang. Không gửi link nghĩa là họ không
kiểm chứng được gì. Cuối mỗi phiên, câu trả lời **phải** có đủ năm link, dạng:

```
**Xưởng âm thanh** — https://huuducbkb.github.io/game-hong-duc-lam/xuong-am/
**Xưởng ảnh** — https://huuducbkb.github.io/game-hong-duc-lam/xuong/
**Xưởng video** — https://huuducbkb.github.io/game-hong-duc-lam/xuong-video/
**Game để chơi** — https://huuducbkb.github.io/game-hong-duc-lam/game/
**Sơ đồ cốt truyện** — https://huuducbkb.github.io/game-hong-duc-lam/nhap/so-do-cot-truyen.html
```

Đừng gửi link chưa gọi thử. Gửi đủ năm, kể cả phiên chỉ sửa một chỗ — người dùng
dùng danh sách này như bảng điều khiển, không phải như báo cáo thay đổi.

### Đừng dựa vào ngày để kiểm bàn giao

Đồng hồ máy chạy và ngày trong phiên chat **lệch nhau** (đã gặp: máy ghi `2026-11-27`,
phiên ghi `2026-11-17`). Nên `ban_giao.py` kiểm theo **tệp có trong commit hay không**,
không so ngày. Đừng "sửa" nó về cách so ngày.

### Câu người dùng sẽ dán vào chat mới

> Đọc `tai-lieu/NHAT-KY.md` và `tai-lieu/VIEC-CAN-LAM.md` trước, rồi tiếp tục.

`AGENTS.md` tự nạp ở mọi chat, nên chỉ cần câu đó là đủ mạch. Việc của phiên trước là
làm cho câu đó **đúng** — nhật ký không có mục mới nhất thì câu đó vô dụng.


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
- Kiểm tra nhanh: `curl -o /dev/null -w '%{http_code}' https://huuducbkb.github.io/game-hong-duc-lam/<đường-dẫn>` — 200 nghĩa là đang public. **`docs/` là gốc web**, nên `docs/nhap/a.html` → `/nhap/a.html` (bỏ tiền tố `docs/`).
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


### Canon Thái Nam Tiểu Hội — ĐỌC `tai-lieu/CANON-THAI-NAM.md` TRƯỚC KHI VIẾT

Đã từng viết sai **11/55 đoạn Chương 2** vì dựng Thái Nam thành "ba tông môn dựng đài
tuyển đệ tử". **Sai hoàn toàn.**

| Điều | Canon ĐÚNG |
|---|---|
| Thái Nam Tiểu Hội | **Hội chợ giao dịch tự phát** của **tán tu** + đệ tử cấp thấp của **gia tộc nhỏ**. **KHÔNG phải môn phái, KHÔNG tuyển đệ tử.** |
| Nhịp tổ chức | **Vài năm một lần** (không phải mỗi năm, không phải "bảy ngày hội") |
| Mục đích tới đây | Trao đổi tài nguyên, mua bán đan dược/pháp khí/phù lục, **nghe ngóng tin tức** |
| Vạn Tiểu Sơn | Tán tu **lớn tuổi**, **Luyện Khí tầng 8**, tính **kiêu ngạo** — KHÔNG phải "gã thanh niên cười tươi" |
| Thăng Tiên Lệnh | Lệnh bài **bái nhập trực tiếp** một trong Thất Đại Môn Phái của Việt Quốc, không qua khảo hạch, kèm **Trúc Cơ Đan**. Là động cơ chính của Hàn Lập |
| Chưởng Thiên Bình | Bình nhỏ màu xanh, **thúc chín linh thảo**. Hàn Lập mua **hạt giống rẻ** → bán **một lượng nhỏ** thảo dược lâu năm. Tuyệt đối giữ bí mật |
| Cao trào | **Tà tu phong toả Thái Nam Cốc** cướp tài vật, bắt tu sĩ làm **lô đỉnh**. Hàn Lập hạ sát **Kim Quang Thượng Nhân**, đoạt túi trữ vật (thêm một Thăng Tiên Lệnh + Kim Quang Chuyên) |
| Sau hội | Vào **Hoàng Phong Cốc** nhờ Thăng Tiên Lệnh |
| Tu vi Hàn Lập lúc này | **Luyện Khí kỳ trung kỳ**, Trường Xuân Công **tầng 6–7** |

**Ngoại lệ đã chốt cho game này:** canon gốc Hàn Lập **giết** Mạc Đại Phu. Game giữ
**Mạc Đại Phu chết vì trận Dã Lang Bang**, là người tốt, Hàn Lập không giết. Động cơ tới
Thái Nam là **di nguyện** của ông. Đừng viết lại thành Hàn Lập giết thầy.

**Quy tắc rút ra:** trước khi viết bất kỳ sự kiện nào có thật trong nguyên tác, phải tra
`tai-lieu/CANON-*.md` trước. Không có file thì **hỏi người dùng**, đừng tự suy ra từ
"nghe hợp lý". Văn hay mà sai canon là vô giá trị.

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
1c. ~~Thư viện ảnh cảnh truyện + giao diện hiển thị theo đoạn~~ ✅
2. ~~Backend game Python + tích hợp LLM (theo cơ chế chương + đoạn)~~ ✅
3. ~~**Chương 1** (Dã Lang Bang)~~ ✅ **XONG 2026-11-17** — 66 đoạn, 2 nhánh
   (tán tu 24 · môn phái 42), 95 lựa chọn, 66 ảnh riêng, test 166 đạt.
   Bàn giao chi tiết: `tai-lieu/NHAT-KY.md` mục *"CHỐT CHƯƠNG 1"*.
4. ~~**Chương 2** (Huyết Sát Thí Luyện)~~ ✅ **XONG nội dung** — **164 đoạn**, 2 nhánh
   (tán tu 86 · môn phái 78 — đo bằng `x['id'].startswith('c2_d')` / `'c2_p'`),
   cơ chế chuyển chương đã có.
   Mỗi nhánh có **3 cảnh đánh + 1 nhánh thua** (2026-11-27): `c2_d22c_*` · `c2_d25c_*` ·
   `c2_d27c_*` + `c2_d27c_thua`, và `c2_p19c_*` · `c2_p22c_*` · `c2_p23c_*` + `c2_p23c_thua`.
   **Còn thiếu ảnh**: Xưởng đã khai **70 cảnh** nhánh tán tu (prompt + ánh xạ), gồm 12 cảnh
   chiến đấu mới, nhưng **chưa vẽ tấm nào**. Nhánh môn phái **56 đoạn chưa có cảnh** —
   xem `tai-lieu/VIEC-CAN-LAM.md`.
5. Chương 3 (đêm đại chiến Hoàng Cung — diệt Hắc Sát Giáo)
6. **Vẽ lại ảnh chương 1** bằng prompt thủy mặc mới. Đo 2026-11-17: **60/66 ảnh loang**,
   trung vị 0.279, tệ nhất `nv_han_lap` 0.477; chỉ 6 ảnh đạt (ngưỡng ≤ 0.15)
7. Video ngắn (chuỗi ảnh + hiệu ứng) — chương 1 hiện **0 đoạn có video**
8. *(giai đoạn sau)* Nghề phụ + thị trường kinh tế

## NÉT VẼ: thủy mặc, sạch loang và đốm (bắt buộc)

> **Mục này từng SAI.** Suốt một thời gian dài nó đòi "line-art nét liền" với các hằng số
> `NET_LIEN` / `NET_NGUOI` / `STYLE_UI`. Ba hằng số đó **đã xoá khỏi mã** ở commit `14a108a`.
> Đọc lại mục này là thấy hướng đúng, đừng dựng lại hướng cũ.

Người dùng phản ánh ảnh ra "nét như răng cưa, quần áo và mặt như tranh trừu tượng".

**Hướng đang dùng: thủy mặc shui-mo (水墨) / điểm màu cǎi-mò (彩墨).** Không phải line-art,
không phải hội họa có khối. Đây là bản gốc trước cả hai hướng kia, và là hướng người dùng
chốt lại (2026-11-17).

**Bốn cụm từ là nguồn gốc của mực loang lỗ và đốm sáng — TUYỆT ĐỐI không dùng lại:**

| Cụm cấm | Vì sao |
|---|---|
| `wet ink bleeding edges` | đòi mực chảy loang ra mép → mảng mực không kín |
| `dry brush strokes` | nét khô gãy vụn, vá víu sáng tối |
| `visible paper fiber texture` | AI vẽ vân giấy thành đốm li ti trong thân mực |
| `rough handmade` | giấy nhám → nền lốm đốm, đọc như tranh trừu tượng |

Cách thay đúng (đang dùng trong mã):

- `rough handmade` → **`smooth handmade`**
- ba cụm còn lại → bỏ hẳn, thay bằng **`clean controlled brushwork`** và
  **`solid flat ink`** / `crisp, well-defined edges`.

Ba hướng đã đi và đã bỏ, ghi lại để không đi lại:

1. **Đòi viền sắc mà không đòi nét liền** → răng cưa.
2. **Hội họa có khối** (`soft blended edges`, `volumetric shading`, bỏ viền) → **loang lỗ
   nặng nhất**. Đòi "layered washes turning gradually" thì AI tô nhiều lớp chồng nhau.
3. **Line-art nét liền** (`baimiao`) → chữa được răng cưa nhưng **người dùng không chọn**.
   Đã gỡ toàn bộ (`NET_LIEN`, `NET_NGUOI`, `NET_UI`, `STYLE_UI`, vòng `UI_KEYS`, regex
   `_NGUOI` tiêm câu vào prompt).

Các khối hiện tại trong `tools_server.py`:

- `STYLE_GOC` / `MAU_GOC`: thủy mặc trên giấy dó **trơn** (`smooth handmade`), mực đen chủ
  đạo + vài mảng màu trầm, `clean controlled brushwork`, `liubai`. `MAU_GOC` thêm
  `Keep the brushwork clean and controlled with crisp, well-defined edges`.
- `STYLE_CHU` = `STYLE_GOC + NO_TEXT`; `STYLE_MAU` = `MAU_GOC + NO_TEXT`.
- `khoi_style(p)` trả `"mau" | "goc" | "khac"`. **Không còn nhánh `"ui"`.**
- Bộ trộn nhiều phong cách dựa trên `a["prompt"].startswith(STYLE_MAU)` — không dùng
  `STYLE_UI`.

**Chặn tái phạm:** `python3 tools/kiem_prompt_anh.py` phải in `SACH`. Test trong
`game/_test_api.py` cũng chặn: *"không prompt ảnh nào chứa từ gây loang"* — danh sách
`_LOANG` gồm cả `wet ink bleeding`, `dry brush`, `paper fiber`, `rough handmade`,
`suggested loosely`, `ink splash`, `blotchy`, `wobbly edges`.

**Cụm "vẽ rời rạc" cũng gây loang, không chỉ bốn cụm trên.** `suggested loosely by a few
ink strokes` / `faces not detailed` từng nằm trong 5 cảnh + 2 prompt môn phái; đã đổi thành
`drawn with solid readable shapes`.

### Đo chất lượng mực

`python3 tools/do_net_anh.py` — ba đại lượng, ngưỡng lấy từ ảnh tổng hợp chứ không đoán:

| Đại lượng | Đo gì | Ngưỡng |
|---|---|---|
| `LOANG` | tỉ lệ điểm còn sáng nằm **bên trong thân mực**. Mực đặc = 0.00; loang lỗ = 0.15–0.48 | trên 0.15 là loang lỗ |
| `ĐỐM` | điểm sáng trong **lỗ nhỏ** giữa thân mực. Lỗ lớn = giấy trắng trong nét bao, hợp lệ | trên 0.03 |
| `NÉT` | nhất quán hướng nét dọc biên; nét chắp vụn thì hướng đảo | chỉ để soi bất thường |

`--tu-kiem` chạy trên 3 ảnh biết trước đáp án; **phải đúng 3/3 mới được dùng**. Thứ tự xét
quan trọng: xét `LOANG` trước `ĐỐM`, vì mực loang tự sinh lỗ nhỏ nên nếu xét đốm trước sẽ
chấm nhầm.

Số đo bộ 70 ảnh cũ: **63 loang lỗ, 1 có đốm, 6 đạt**, trung vị 0.272. Ảnh tệ nhất là chân
dung (`nv_han_lap` 0.477). Sửa prompt **không chữa được ảnh cũ** — phải vẽ lại.

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

### (Đã bỏ) Quy tắc "âm thanh game có nhạc cụ"

Từng có một giai đoạn prompt đòi mở bằng `Game ambience loop for …`, liệt kê nhạc cụ
(đàn tranh, sáo, trống, chiêng), thang ngũ cung, và ghi rõ "NOT a field recording".
**Toàn bộ giai đoạn đó đã bị bỏ.** Người dùng chốt: tiếng cảnh là tiếng không gian
người chơi nghe thấy, không phải nhạc nền — nên prompt giờ tả âm thanh hiện trường
(`field recording` là chữ ĐƯỢC dùng, trong thẻ chất âm ở cuối prompt).

`DUOI`, `CHUNG`, `duoi(nhịp, ô)` và mọi assert nhịp BPM **không còn trong mã**. Nếu
thấy tài liệu nào còn nhắc, tài liệu đó cũ.

### (Đã bỏ) Quy tắc "phải nói rõ nhạc lặp lại"

Cũng bỏ theo. Game phát mỗi file **một lần** rồi thôi, không lặp — xem mục
"Đừng lặp một câu khuôn ở cuối mọi prompt" bên dưới. Đừng viết `seamless loop`,
đừng tính BPM, đừng bắt máy lặp mẫu.

### Độ dài cảnh KHÔNG còn cố định 10 giây

Mỗi cảnh khai `giay` riêng (phần tử thứ 8 của tuple trong `MOI`; thiếu thì lấy
`GIAY_MAC_DINH`). Người dùng yêu cầu cảnh mở cửa chỉ **2 giây**; cảnh có lời thoại
**3–6 giây**; cảnh bối cảnh vẫn **10 giây**. Con số này chảy qua ba chỗ, sửa một
chỗ là lệch:

1. `game/du_lieu_am.py` — nguồn duy nhất.
2. `game/ghi_danh_sach_am.py` — ghi `giay` vào `danh-sach.json`; game đọc từ đó.
3. `tools/xu_ly_am.py` — `giay_canh(ma)` cắt file tải lên đúng độ dài cảnh.

Trong `play.html`, việc vào dần / tắt dần do chính lớp file lo (`datAmLuong` +
`hen()`), tính theo **độ dài thật** của buffer. Đừng đặt lại mốc cứng: bản cũ
fade-in 1,2 giây và tắt ở 10 giây, nên âm mở cửa 2 giây bị nuốt gần hết, chỉ còn
một tiếng "phụt".

### Ảnh `nv_` / `vt_` cũng là cảnh có tiếng — bốn lỗi từng làm chúng câm

Cảnh có lời thoại dùng ảnh nhân vật/vật (`nv_han_lap.jpg`), không phải `bc_`.
Bốn lỗi chồng nhau khiến 21 cảnh này **không bao giờ** phát được tiếng dù đã có file:

1. `maCanhTuAnh()` trả `""` cho mọi ảnh không bắt đầu bằng `bc_`.
2. Nhánh `"diem"` trong `doiCanhTieng()` kêu một nốt rồi `return` — bỏ qua file.
3. Điều kiện bỏ qua so **nhóm** (`canhLoai`) chứ không so **mã cảnh**; mọi cảnh
   nhân vật đều nhóm `diem`, nên cảnh thứ hai trở đi bị coi là "đang phát rồi".
   Đã thêm biến `canhMa` để so theo mã.
4. `datAmLuongCanh()` gọi thẳng `cancelScheduledValues` → xoá luôn hẹn tắt, tiếng
   chạy mãi sau khi người chơi kéo thanh âm lượng. Phải đi qua `datAmLuong`.

**Phép thử bắt buộc:** phát **sáu cảnh nhân vật liên tiếp**, đo biên độ từng cảnh.
Cả 6 phải kêu. Chỉ thử một cảnh sẽ không bắt được lỗi số 3.

### Tiếng cảnh phát MỘT lần rồi thôi — không lặp

Người dùng chốt: "âm thanh ở các cảnh chạy 10s là thôi không lặp lại". Ba đường
làm tiếng quay lại, cả ba đều phải bịt:

1. **`nguon.loop`** — không được đặt `true`. File ngắn hơn 10 giây (có hai file:
   `cong_dong_quyen` ~4s, `san_tap_cai_lai` ~5s) sẽ lặp 2–3 lần trong một cảnh.
   Phát một lần; hết file thì im, phần còn lại của cảnh không có tiếng.

2. **Nối vòng bằng crossfade** — hàm cũ `lamVongKhit` cắt đuôi rồi chồng lên đầu.
   Chỉ có nghĩa khi lặp; bỏ lặp thì nó **cắt mất đuôi tiếng**. Giờ là
   `catLangHaiDau`: vẫn cắt lặng hai đầu (công cụ sinh âm thanh luôn thêm 0,3–2
   giây lặng ở đầu, để nguyên thì phải đợi mới nghe thấy), nhưng không nối vòng.

3. **`thucDayTieng` dựng lại nền** — đây là lỗi người dùng nghe thấy thật, và nó
   không nằm ở chỗ phát file. Hàm này chạy ở **mọi cú chạm** và mọi lần tab hiện
   lại. Sau 10 giây tiếng đã tắt nên `canhDangChay === null`; hàm tưởng nền chết
   và dựng lại từ đầu. Người chơi bấm mở bảng Hệ Thống sau giây thứ 10 là nghe
   lại tiếng cảnh — lặp vô hạn theo số lần chạm.

   Cờ `canhDaHet` chặn việc này: đặt khi hết 10 giây hoặc khi cảnh không có file;
   xoá khi sang cảnh mới hoặc khi người chơi chủ động bật lại tiếng.

**Phép thử đúng** phải đo biên độ theo thời gian, không chỉ đếm số nguồn: đếm
"đợt tiếng" (RMS > 0,001 liên tục ≥ 0,3s). Đúng là **1 đợt** và đợt đó **không
kéo quá 10,6 giây**. Đếm nguồn không bắt được lỗi số 1 nếu file dài hơn 10s, và
không bắt được lỗi số 3 nếu không chạm màn hình sau giây thứ 10.

### Trạng thái "đã có tiếng" phải sinh từ dữ liệu, không viết cứng

`da_co()` trong `game/tao_xuong_am.py` đọc `danh-sach.json` và biết chính xác cảnh
nào có file. Nhưng badge trong thẻ từng bị viết cứng `<span class="badge thieu">⬜
chưa có</span>`, nên **40 cảnh có tiếng vẫn hiện như chưa có** — người dùng chỉ thấy
đúng sau khi bấm "Kiểm tra lại" từng thẻ. Nhãn và class `done` giờ lấy từ `da_co()`
lúc dựng trang.

Bài học chung: nếu trang đã biết một sự thật lúc dựng, đừng bắt người dùng bấm nút
để hỏi lại sự thật đó.

### Không gọi GitHub API theo số lượng cảnh

Trang xưởng từng gọi `api.github.com/.../commits?path=...` **một lần cho mỗi cảnh**,
tức 64 lượt mỗi lần mở trang. GitHub cho 60 lượt/giờ cho mỗi IP, nên mở trang một
lần là vượt hạn mức, và từ đó **mọi cảnh hiện như chưa có tiếng** — dù file vẫn tải
được bình thường. Triệu chứng đánh lừa: file trả 200 nhưng giao diện báo thiếu.

Nay: cảnh có file thì trỏ thẳng vào file trong repo (`data-co="1"` sinh sẵn lúc dựng
trang), nút "Kiểm tra" hỏi thẳng file bằng `HEAD` + query đổi theo thời gian để không
dính bộ nhớ đệm. Không cần token, không hạn mức.

Quy tắc: nếu trang đã biết dữ liệu lúc dựng, đừng hỏi lại API lúc chạy.

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
`docs/assets/am/danh-sach.json`: cảnh nào có mã trong đó thì phát đúng file của cảnh
đó. **Cảnh chưa có file thì IM.** Không lùi về file nhóm, không rơi về nhạc tổng hợp —
người dùng yêu cầu rõ: cảnh nào chưa có tiếng thì để nguyên, không chèn âm thanh khác.
Đừng tự tay commit mp3 vào `assets/am/` — hãy đi qua xưởng, để còn cân âm lượng.

Prompt tạo tiếng nằm ở `game/prompt_am.py`, danh sách cảnh ở `game/du_lieu_am.py`; sửa
prompt thì sửa ở đó rồi chạy `python3 game/tao_xuong_am.py`. Mã cảnh suy ra từ tên file
ảnh (`maCanhTuAnh`), nên mỗi cảnh cần đúng một file `<mã>.mp3`.

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

### Tiếng theo cảnh: chỉ file thật, mặc định tắt

Không còn tiếng tổng hợp. Cảnh nào có file trong `docs/assets/am/` thì phát file
đó một lần 10 giây; cảnh nào chưa có thì **im hẳn** — không lấy file của cảnh
khác, không chèn nhạc dựng bằng Web Audio. `nhomCanh()` vẫn còn nhưng chỉ dùng để
biết cảnh có đổi không, không dùng để chọn file.

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

### Xưởng âm thanh: nhận video, chỉ lấy tiếng

Ô chọn file nhận cả video. Trình duyệt giải mã video bằng `decodeAudioData`, lấy 12 giây
đầu, nén mp3 rồi mới gửi — **video không bao giờ được tải lên**. Đây là yêu cầu của người
dùng: video ~10 MB nằm vĩnh viễn trong lịch sử git, kể cả khi bot xoá file ở commit sau.

**Đừng gửi WAV.** WAV 12 giây là 2 MB, base64 thành 2,7 MB, nhân 43 cảnh là 29 MB lịch sử
git. `lamejs` (nhúng ở `docs/xuong-am/lamejs.js`, 168 KB, LGPL-3.0) nén ngay trong trình
duyệt còn 95–141 KB mỗi đoạn. Đổi 168 KB lấy 21 MB. Xem `docs/xuong-am/lamejs.NOTICE.txt`
— LGPL bắt buộc ghi công và nạp thư viện thành tệp riêng, đừng trộn vào mã trang.

**Không dùng `MediaRecorder`.** WebKit — Safari trên iPhone/iPad — không có API đó. Đã đo.

Nhận diện video theo **đuôi file**, không theo MIME: iPhone hay để `type` trống.

Đo trên WebKit với iPad (2026-11-22): mp4 H.264, mov HEVC (`hvc1`, định dạng iPhone quay
mặc định) và video 20 giây đều ra đúng số giây — 8,07 / 10,06 / 12,07. Qua bot: 12,00 s,
−18,45 LUFS. Video 5,4 MB bị chặn đúng trần; video không tiếng báo lỗi, không gửi file rỗng.

**Cẩn thận khi test trên trang live:** file test đặt trong `docs/` phải push và deploy xong
mới tải được. Lần đầu tôi trỏ vào file chưa deploy, nhận 404, rồi kết luận sai là HEVC
không đọc được. Muốn thử nhanh thì chạy `python3 -m http.server --directory docs`.

**`npm install` trong repo này rất nguy hiểm.** Không có `package.json` được theo dõi, nên
npm tạo file mới và **xoá sạch `node_modules`** — mất Playwright. Dùng
`npm install --no-save <gói>` hoặc `npm pack` ra `/tmp` rồi chép tay.

### Prompt tiếng theo cảnh: tả không gian, không tả nhạc

Mỗi cảnh trong `game/prompt_am.py` có một prompt. Nguyên tắc: mở đầu bằng **một câu khai
báo đầy đủ** — dài bao lâu, không khí gì, ở đâu — rồi mới tới các lớp tiếng theo khoảng
cách tính từ tai người chơi. Đây là khác biệt cốt lõi: cùng là chợ mà chợ sớm thì đứng
giữa đám đông, chợ chiều thì ngồi một mình ở rìa — hai prompt khác hẳn, không dùng chung
một file ambience.

**Đừng lặp một câu khuôn ở cuối mọi prompt.** Bản cũ có `No music, no speech,
seamless loop.` ở cuối cả 42 prompt nền. Ba lỗi trong một câu:

- `seamless loop` **sai sự thật**: game phát mỗi file một lần rồi thôi
  (`<audio>` không đặt `loop`). Ghi vậy là bảo máy làm bản nền lặp.
- `no speech` **thừa**: prompt không hề có ai nói, phủ định một cái không tồn tại.
- Câu khuôn lặp 42 lần thì máy coi đó là phần quan trọng nhất của prompt.

Thay bằng một **thẻ chất âm** riêng cho từng cảnh ở cuối, kiểu
`Warm, tranquil, intimate walled-garden field recording.` — ngắn, cụ thể, đổi theo cảnh.

**Prompt tả âm thanh, không kể chuyện.** Máy tạo tiếng không tạo được hành động của
nhân vật. "The player walks into a walled herb garden" không cho nó biết phải phát ra
tiếng gì — nó chỉ tạo được tiếng. Nên KHÔNG viết "the player", "his own". Chỉ tả cái
tai nghe thấy. Người chơi vẫn là gốc của mọi khoảng cách (`at the ear`, `a few metres
off`, `far behind`), nhưng không bị kể là đang làm gì.

**Mở bằng câu khai báo, không mở bằng phủ định.** Sai: `"Ambience, no music, no
speech."` — ba lần phủ định, không nói gì về chất âm. Đúng: `"10-second warm, secluded
morning ambience in a walled herb garden."` — dài bao lâu, không khí gì, ở đâu.

**Phải có từ chỉ chất âm.** `warm`, `cold`, `intimate`, `tense`, `sparse`, `dense`,
`field recording`, `natural reverb`, `open air`, `enclosed`, `muffled`. Không có mấy
chữ này thì máy tự đoán chất, mỗi lần ra một kiểu. Bản cũ chỉ 2/43 cảnh có.

**Phủ định trừu tượng phải đổi thành tả cụ thể.** Máy không tạo được cái không-có-gì.
`"nothing comes back"` → `"open air, no reflection, each sound lands and dies"`.
`"gives nothing back"` → `"the canopy deadens everything above"`.

**Lời nói chỉ đưa vào khi truyện có lời thoại thật.** Cảnh không có ai nói câu nào
thì không thêm tiếng đọc, không "shouting in Vietnamese", không "voices talking".
Tiếng người lúc đó chỉ là âm không lời: thở, thở dốc, hừ, rên, huýt gió, la, khóc.
Lý do: lời nói thêm vào chỗ không có sẽ biến cảnh thành phim truyền thanh. Chú ý:
"shouted count" là đếm thành tiếng, tức là có chữ — vi phạm; dùng "a sharp whistle".

Ngoại lệ: **cảnh nào có người nói thì prompt phải có 1–2 câu tiếng Hoa trong ngoặc
`「」`** — NPC nói thì lấy lời NPC, nhân vật chính nói thì lấy lời nhân vật chính với
giọng `nvc`, suy nghĩ trong đầu `*...*` thì bỏ. Hiện là 55/64 cảnh, không phải chỉ 21
cảnh nhóm `gap`. Đây là yêu cầu người dùng nêu nhiều lần, gần nhất là cảnh nền cũng có
NPC nói (`cong_dong_giau`, Tuyết Cơ nhắc) và cảnh chỉ có nhân vật chính nói
(`vuon_thuoc_im`) — cả hai đều phải lên tiếng.

Hai lỗi đã mắc, đừng mắc lại:

1. **Suy thoại từ nhóm thay vì từ đoạn truyện.** Lần đầu chỉ gắn cho nhóm `gap` →
   bỏ sót 32 cảnh. Phải quét từng đoạn truyện trong `game/chapters/chuong1.json`,
   tìm câu trong ngoặc kép.
2. **Đưa nhầm lời nhân vật chính vào chỗ của NPC.** 10 cảnh lấy câu của nhân vật
   chính (người chơi) thay vì NPC — ví dụ `kiem_linh_thu` lấy `「信你？」` trong khi
   đó là câu nhân vật chính hỏi kiếm linh. Lỗi ở đây là **gán sai người nói**, không
   phải "cấm lời nhân vật chính". Lời nhân vật chính vẫn lấy, nhưng phải đọc bằng
   giọng `nvc` — xem mục dưới. Dấu hiệu nhận biết:

   - Câu NPC: đứng sau `— Tuyết Cơ nói`, `— kiếm linh nói`, `— ông khẽ nói`,
     `— hắn gầm lên` (có tên/chức danh).
   - Câu nhân vật chính: đứng sau `— ta nói`, `— ta đáp`, `— ta quát`, `— ta hỏi`.
   - Suy nghĩ trong đầu: đứng một mình sau `*...*`. Bỏ — không ai nói ra.

**Lời nhân vật chính có giọng riêng, không bỏ.** Người dùng chốt: nhân vật chính là
**nam 16 tuổi, giọng trầm ấm nghe dễ chịu**. Cảnh chỉ có nhân vật chính nói thì vẫn
phải có câu của nhân vật chính — từng bỏ sót nên `vuon_thuoc_im` mất hẳn câu
`「多谢前辈。」` dù truyện có thoại, người chơi nghe im lặng ở đúng chỗ đang nói:

```
A boy's voice, sixteen, low and warm, pleasant
```

**Mỗi câu thoại phải ghi tuổi và giới của người nói.** Không ghi thì máy tự đoán,
mỗi cảnh ra một người khác nhau. Bảng giọng (13 NPC + nhân vật chính `nvc`) ở
`game/GIONG_NPC.md`; câu thoại dài thì tách thành hai đoạn `「…」 then 「…」` để máy
ngắt đúng chỗ.

**Tuyết Cơ là ngoại lệ quan trọng — giọng riêng, không dùng khuôn chung.** Người
dùng đã sửa hai lần, chốt: **nữ 18 tuổi, ngọt ngào, gợi cảm, lẳng lơ, thích trêu
đùa**. Câu chuẩn, áp cho cả 20 cảnh có nàng nói:

```
A girl's voice, eighteen, sweet and sultry, breathy, teasing, a little flirtatious
```

Bốn chữ không được bỏ: `sweet` (ngọt), `sultry` (gợi cảm), `breathy` (giọng hơi,
thở nhẹ), `teasing` (trêu). Thiếu `teasing` là ra cô gái nghiêm túc; thiếu `breathy`
là ra giọng trẻ con trong trẻo. Đổi phần đuôi theo tình huống (`pleased, teasing` /
`sweet but urgent` / `sweet and delighted` / `sweet and lazy, almost fond` /
`sweet and breathy, trembling`).

**Đừng viết `cold` cho Tuyết Cơ.** Bản đầu em ghi `soft and silky with cold
underneath` và `cold as ice` — người dùng chê vì ra giọng bà cô lạnh lùng, mất hết
tính trêu đùa. Cái lạnh chỉ hiện khi nàng nổi giận: viết `sweet but cool and
displeased, the teasing gone`.

**Đừng dùng `woman's voice` hay `around twenty`** cho nàng — đã bị sửa hai lần, chốt
là `girl's voice, eighteen`.

Cảnh chỉ có giọng Hệ thống (máy, vô cảm) thì **không** thêm thoại: `cho_03`,
`duong_mon_nui`, `khe_nui_dem`, `mieu_hoang`, `san_sau_anh_sang`, `mieu_trong`.

**Sửa prompt xong thì phải rà lại TOÀN BỘ, không chỉ cảnh vừa sửa.** Lần chốt ba
giọng, em sửa 20 cảnh nhưng bỏ sót 3 cảnh vẫn tả giọng kiểu cũ (`kiem_hap`
"a cold young male voice", `kiem_hap_nhan` "a young man's low voice", `tan_hoang`
"A young man's voice, quiet and unusually gentle") — cả ba đều là Kiếm Linh. Cách
rà: gom mọi mẫu `(?:A|a|Then a) … voice` trong `PROMPT` rồi so với danh sách khuôn
giọng đã chốt; mẫu nào không khớp khuôn nào là mẫu sai.

**Kiểm tiếng đã úp thì so prompt tại ĐÚNG LÚC úp, không so với prompt hiện tại.**
Một file tiếng có thể đúng giọng mà vẫn thiếu thoại, vì nó được tạo trước khi thoại
được thêm vào prompt. Cách kiểm đúng:

```python
r = git log -1 --format=%H -- docs/assets/am/<canh>.mp3   # commit úp file
old = PROMPT tại f'{r}^'                                   # prompt lúc đó
# nếu ('「' in old) != ('「' in PROMPT[canh]) -> file thiếu/thừa thoại, phải tạo lại
```

Lần kiểm 66 file, cách này lôi ra 10 cảnh có tiếng nhưng tạo từ prompt chưa có
thoại (`tran_lua`, `tran_lua_2`, `tran_lua_3`, `binh_minh`, `san_tap_ngay`,
`cong_dong_hung_ba`, `cong_dong_quyen`, `quan_nuoc`, `san_sau_chon_lai`,
`tan_hoang`). So với prompt hiện tại thì không thấy, vì prompt hiện tại khác cả
những cảnh chỉ đổi câu chữ.

**Đừng đoán thoại bằng phân tích tín hiệu.** Em thử đo nhịp điệu âm (2–8 Hz) và độ
có cao độ để tìm câu nói trong file — cả hai đều sai: `san_sau_luyen_dem` (không
thoại) cho chỉ số cao hơn `vuon_thuoc_im` (có thoại). Muốn biết file có thoại hay
không thì đọc prompt đã dùng để tạo nó, đừng suy từ sóng âm.

**Ba lớp khoảng cách, gắn vào câu chứ không chia mục.** Prompt cần (1) sát tai,
(2) vài mét, (3) xa — và nói rõ tiếng ĐỔI thế nào khi đi qua không gian đó: tường đá
dội lại, ngõ hẹp dội nhanh và cứng, phòng kín đè tiếng xuống quanh đầu, ngoài trời
tiếng rơi xuống là mất. Nhưng viết thành câu liền mạch (`Close at the ear, … A few
paces off, … Far behind, …`), KHÔNG viết thành danh sách có dấu hai chấm như bản cũ
— danh sách làm máy đọc từng mục rời rạc, ra tiếng chắp vá.

Bài học từ bản Gemini mà người dùng khen: câu chảy, mỗi câu một tầng, kết bằng một
thẻ chất âm. Đó là khuôn mẫu, không phải danh sách gạch đầu dòng.

**Trần 450 ký tự.** Ô prompt của ElevenLabs Sound Effects chỉ nhận 450 ký tự —
dài hơn thì trang báo lỗi và không cho tạo, không phải lỗi nội dung. Prompt cũ dài
508 ký tự nên bị chặn. Mọi prompt phải dưới 450; trang Xưởng có bộ đếm để thấy ngay.

Đã tái phạm: hai prompt cảnh nghỉ đêm thêm sau đó dài 602 và 582 ký tự, vượt trần
mà không ai thấy, vì bộ đếm trên trang chỉ **tô đỏ con số** — vẫn phải tự nhìn vào
mới biết. Giờ `game/_test_api.py` có phép kiểm canh trần, chạy là báo ngay.

Rút prompt mà không mất tầng âm: bỏ chữ trùng nghĩa trước ("at night, just before
dawn" khi đã có "before dawn"), bỏ tính từ chồng ("pleasant, quiet", "cramped,
exhausted", "hollow with a faint eerie ring"), gộp "Further out" thành "A few paces
off". Đừng cắt câu thoại hay cắt tầng khoảng cách — đó là phần tai nghe ra khác biệt.

**Tránh chữ dễ bị bộ lọc chặn:** không tả thương tích, không tả xác, không lồng
tiếng trẻ con, không dùng "violent", "dead", "weeping". Tả ĐỘNG TÁC cụ thể (a blade
sweeping through air, boots hammering stone) thay vì tả mức độ dữ dội — vừa dễ qua
bộ lọc, vừa ra tiếng đúng hơn.

**Đừng thêm lời thoại vào cảnh không có ai nói.** Người dùng đã bỏ kiểu nhét câu tiếng
Việt cụ thể trong ngoặc kép vào prompt. Chỉ lấy câu thoại có thật trong truyện, và câu
tiếng Hoa trong `「」` — không phải tiếng Việt. Xem quy tắc "Lời nói chỉ đưa vào khi
truyện có lời thoại thật" ở trên.

Trước đây tôi đã bỏ prompt vì lý do sai: tôi cho là không công cụ nào tạo được ambience từ
prompt. Thực ra vấn đề là prompt cũ tả nhạc, không tả không gian.

**Playwright có thể mất trình duyệt** (cache trống). Cài lại bằng
`npx playwright install-deps webkit` rồi `npx playwright install webkit`. Bước `-deps` cần
quyền root và chạy lâu, nên đặt chạy nền.

## Tiếng cảnh: bộ nhớ đệm và push đụng độ

Người dùng báo "tải tiếng mới lên mà vẫn nghe bản cũ, mà tiếng mới không thấy
đâu". Hai lỗi riêng biệt, cùng lúc:

**1. GitHub Pages giữ file 10 phút.** `cache-control: max-age=600`. Thay tiếng
của một cảnh mà giữ nguyên tên file thì trình duyệt vẫn phát bản cũ. Sửa: mỗi mục
trong `docs/assets/am/danh-sach.json` có thêm `v` = 8 ký tự đầu mã băm nội dung
(`game/ghi_danh_sach_am.py`), và nơi phát tiếng gắn `?v=<mã>` vào địa chỉ. Đã sửa
ở cả `game/play.html`, `docs/game/play.html` (hàm `phatFileThat`) và
`game/xuong_am.js` (dùng `Date.now()`).

**2. Workflow `xuong-am.yml` push thẳng vào main.** Người dùng và agent cũng push
vào main, nên khi trùng lúc thì bot bị từ chối (`! [rejected] main -> main (fetch
first)`), job chết ở bước Commit, và file nằm kẹt trong `xuong-am-inbox/` — không
vào `docs/assets/am/`, nên game không thấy. Đã xảy ra thật với
`cong_dong_doi_mat` (run 45197036729). Sửa: vòng thử 5 lượt, mỗi lượt
`git pull --rebase --autostash` rồi push lại; hết lượt thì `::error::` và exit 1.

**Cách kiểm khi người dùng báo lỗi này** — đừng đoán, chạy đúng ba bước:

```bash
find xuong-am-inbox -type f ! -name 'README.md' ! -name '.gitkeep'   # file ket?
curl -s <api>/actions/workflows/xuong-am.yml/runs?per_page=15          # run that bai?
md5sum docs/assets/am/<ma>.mp3; curl -s <live-url> | md5sum            # live khop local?
```

Nếu live khớp local mà vẫn nghe cũ thì là bộ nhớ đệm, không phải file sai.

### Lần 2: vẫn "ở âm thanh cũ" — hai lỗi khác, không phải lỗi cũ

Sau khi đã sửa bộ nhớ đệm và push đụng độ, người dùng báo lại y hệt. Lần này
nguyên nhân KHÁC, nên đừng vội kết luận "đã sửa rồi mà vẫn lỗi":

**a. `deploy-pages` chết vì lỗi tạm thời của GitHub.** Hai run liền
(`45203424457`, `45204652597`) báo `Fetching artifact metadata failed` và
`No artifacts named "github-pages" were found`. Bước xử lý tiếng thành công,
file đã nằm trong repo, nhưng **chưa lên trang** — live vẫn là bản cũ. Cách
nhận biết nhanh: so `md5sum` file local với file live; lệch nhau mà
`git log` đã có commit mới nghĩa là chưa deploy, không phải file sai.
Đã thêm 3 lượt thử, chờ 30s rồi 60s giữa các lượt.

**b. Xưởng ghi cứng trạng thái lúc sinh trang.** `tao_xuong_am.py` đọc
`danh-sach.json` rồi nhúng `data-co="0/1"` vào HTML. Workflow chỉ ghi lại
danh sách mà **không sinh lại xưởng**, nên thẻ vẫn báo "chưa có" và nút nghe
vẫn ẩn dù tiếng đã vào. Nay workflow chạy `game/tao_xuong_am.py` ngay sau
`ghi_danh_sach_am.py`.

**Điều dễ bỏ sót:** bot push bằng `GITHUB_TOKEN` nên **không** kích hoạt
`pages.yml` (GitHub chặn vòng lặp). Deploy trong `xuong-am.yml` là đường
**duy nhất** đưa tiếng lên trang. Nó chết là tiếng không lên, dù repo đúng.

**c. Deploy dồn dập thì Pages chặn, không phải lỗi code.** Một phiên sửa
prompt đã deploy 12 lần trong 1 giờ; 4 lượt liền báo `Deployment failed, try
again later` dù artifact upload thành công (75 MB, có trong run) và
githubstatus.com ghi "All Systems Operational". `workflow_dispatch` và
`rerun` đều hỏng. Chờ ~15 phút rồi dispatch lại → **thành công ngay**.

Nên: sau 2 lượt hỏng liên tiếp cùng thông báo đó, **đừng thử tiếp** — chờ
10–15 phút. Phân biệt hai lỗi rất giống nhau:

| Thông báo | Nghĩa | Xử lý |
|---|---|---|
| `No artifacts named "github-pages"` / `Fetching artifact metadata failed` | artifact không tới được bước deploy | thử lại 1–2 lần, cách 30–60s |
| `Deployment failed, try again later` (sau khi đã `Created deployment`) | Pages từ chối build, thường do dồn dập | chờ 15 phút, đừng retry liền |

Cách kiểm artifact có thật trong run hay không:

```bash
gh api repos/<owner>/<repo>/actions/runs/<run_id>/artifacts \
  --jq '.artifacts[] | "\(.name) \(.size_in_bytes) expired=\(.expired)"'
```

**Thứ tự kiểm khi người dùng báo "vẫn âm thanh cũ":**

```bash
find xuong-am-inbox -type f ! -name 'README.md' ! -name '.gitkeep'  # 1. kẹt?
curl -s <api>/actions/workflows/xuong-am.yml/runs?per_page=5         # 2. run lỗi?
git log --oneline -3 -- docs/assets/am/<ma>.mp3                      # 3. có commit?
md5sum docs/assets/am/<ma>.mp3                                       # 4. local
curl -s <live>/assets/am/<ma>.mp3 | md5sum                           # 5. live khop?
curl -s <live>/assets/am/danh-sach.json | grep <ma>                  # 6. v khop?
```

## Cảnh dùng lại ảnh nền sẽ phát nhầm tiếng

`doiCanhTieng()` trong `docs/game/play.html` suy mã tiếng từ **tên file ảnh**
(`maCanhTuAnh`). Hai cảnh khác nhau dùng chung một ảnh nền thì chúng dùng chung
một mã tiếng: cảnh sau nghe lại đúng đoạn tiếng của cảnh trước, và mục tiếng
riêng của cảnh sau không bao giờ được phát dù file đã có.

Vì vậy **mỗi cảnh cần một ảnh nền riêng** nếu muốn có tiếng riêng. Khi thêm
cảnh mới:

1. Thêm mục vào `ASSETS` (`tools_server.py`) với `key` = tên file không đuôi.
2. Thêm key đó vào một nhóm trong `NHOM_CANH` — ảnh không thuộc nhóm nào thì
   **không hiện** trên trang Xưởng.
3. Thêm dòng trong `DOAN_CUA_ANH` để biết ảnh thuộc đoạn nào.
4. Thêm mục trong `game/du_lieu_am.py` (mã tiếng = key bỏ tiền tố `bc_`).
5. Thêm prompt trong `game/prompt_am.py` — **đúng số câu thoại** trong cảnh và
   **đúng tuổi + giới** theo `game/GIONG_NPC.md`.
6. `python3 tools/build_xuong.py` rồi `python3 game/ghi_danh_sach_am.py`.

Kiểm nhanh lỗi lệch thoại (số câu tiếng phải bằng số câu thoại trong cảnh):

```bash
python3 -c "
import json,io,re,sys; sys.path.insert(0,'game')
import prompt_am as PA
d=json.load(io.open('game/chapters/chuong1.json',encoding='utf-8'))
D={x['id']:x for x in d['doan']}
for sid,key in (('c1_p16b','tan_xa_nghi_dem'),('c1_d14b','mieu_hoang_nghi_dem')):
    th=re.findall(r'“([^”]+)”',D[sid]['ke']); cn=re.findall(r'「([^」]+)」',PA.PROMPT[key])
    print(sid,len(th),len(cn),'KHOP' if len(th)==len(cn) else 'LECH')
"
```

Khoá rẽ nhánh trong `chuong1.json` là **`den`**, không phải `toi`.
`__ket_thuc__` là mốc kết thúc hợp lệ, không phải đích hỏng.

## Ảnh vào repo là chưa đủ — cần bản nhỏ 300px

Xưởng âm thanh (`game/tao_xuong_am.py`) trỏ ảnh vào `assets/scene/nho/`, bản
thu nhỏ 300px, để trang nhẹ trên điện thoại. Không có script tự sinh bản nhỏ:
workflow xưởng ảnh chỉ ghi bản gốc. Ảnh mới lên mà thiếu bản nhỏ thì thẻ cảnh
trong xưởng âm thanh hiện **ô ảnh trống**, không báo lỗi gì.

Kiểm nhanh (phải in `khong`):

```bash
python3 -c "
import os,glob
goc={os.path.basename(p) for p in glob.glob('docs/assets/scene/*.jpg')}
nho={os.path.basename(p) for p in glob.glob('docs/assets/scene/nho/*.jpg')}
print('thieu ban nho:',sorted(goc-nho) or 'khong')
"
```

Tạo bản nhỏ, **giữ đúng tỉ lệ ảnh gốc** (đừng ép 3:4 — ảnh 759x1600 mà ép
3:4 sẽ cắt mất đầu/chân nhân vật; CSS `object-fit:cover` đã tự lo khung):

```bash
python3 -c "
from PIL import Image
k='bc_ten_anh'
im=Image.open(f'docs/assets/scene/{k}.jpg').convert('RGB')
im=im.resize((300, round(im.height*300/im.width)), Image.LANCZOS)
im.save(f'docs/assets/scene/nho/{k}.jpg','JPEG',quality=82,optimize=True)
"
```

## Trang xưởng là HTML sinh sẵn, sửa dữ liệu phải sinh lại

`docs/xuong/index.html` (xưởng ảnh) và `docs/xuong-am/index.html` (xưởng âm
thanh) đều là file tĩnh sinh ra, **không đọc dữ liệu lúc chạy**. Thêm mục vào
`ASSETS` / `du_lieu_am.py` mà quên sinh lại thì trang vẫn là bản cũ, không báo
lỗi. Phải chạy:

```bash
python3 tools/build_xuong.py        # xưởng ảnh
python3 game/tao_xuong_am.py        # xưởng âm thanh
python3 game/ghi_danh_sach_am.py    # danh sách tiếng
```

## Xưởng âm thanh gắn cốt truyện theo TÊN ẢNH

`doc_truyen()` trong `tao_xuong_am.py` gom đoạn truyện theo
`hinh_anh.anh` của từng đoạn. Mục tiếng trỏ **nhầm ảnh** thì khối "Cốt truyện
cảnh này" hiện đoạn của cảnh khác — nhìn qua tưởng đúng vì vẫn có chữ. Khi
thêm mục tiếng, kiểm `anh` trỏ đúng file của chính cảnh đó.

## Hai nhánh chương 1 tách theo xuất thân, không gặp nhau

`c1_d01` (tán tu) và `c1_p01` (môn phái) là hai cây riêng: từ `c1_d01` chỉ tới
được 24/66 đoạn. Muốn kiểm nhánh môn phái phải chọn xuất thân `mon_phai` ở
màn tạo nhân vật (`.xt-the[data-ma=mon_phai]`), không thì không bao giờ tới
`c1_p16b`. Đừng kết luận "nút hỏng" khi thực ra đi sai cây.

### Deploy Pages hỏng: đừng "chạy lại job", phải dispatch lượt mới

Đã gặp nhiều lần. Triệu chứng: `actions/deploy-pages@v4` báo
`Fetching artifact metadata failed` rồi
`No artifacts named "github-pages" were found` — dù bước upload ngay trước đó
**thành công** và đã đẩy cả trăm MB.

**Nguyên nhân thật (tìm ra 2026-11-27 bằng log của run 45867201111):** không phải
quyền, không phải code. Đây là lỗi hạ tầng của API GitHub. Log ghi rõ
`error_count: 10`, `timeout: 600000`, kèm câu
`Is githubstatus.com reporting issues with API requests, Pages, or Actions?` —
tức `deploy-pages` gọi API để lấy metadata artifact, bị lỗi mạng/API phía GitHub,
nên **không thấy** artifact dù artifact có thật. Upload và deploy là hai lời gọi
API khác nhau; cái sau hỏng không nói gì về cái trước.

Dữ liệu thật, cùng một commit `54c0fe1`:

| Run | Kiểu | Kết quả |
|---|---|---|
| 45864987603 | `push` | hỏng |
| 45866224033 | `workflow_dispatch` | hỏng |
| 45866497562 | `push` | hỏng |
| 45866802692 | `workflow_dispatch` | **thành công** |
| 45867201111 | `push` | hỏng |
| 45867328706 | `workflow_dispatch` (cùng commit) | **thành công** |

Hai kết luận rút ra:

- **`actions: read` không phải nguyên nhân.** Em đã thêm quyền đó vào `permissions`,
  và lượt `push` sau đó **vẫn hỏng y hệt**. Giữ quyền đó cũng vô hại (deploy-pages có
  đọc artifact), nhưng đừng tin nó là cách sửa.
- **`workflow_dispatch` là đường thoát.** Cùng commit, `push` hỏng mà `dispatch`
  thành công. Có lần dispatch đầu cũng hỏng — **dispatch lại lần nữa là được**.

Nên khi gặp lỗi này: **dispatch, hỏng thì dispatch lại**. Đừng chạy lại job
(xem lý do bên dưới), đừng mất thời gian mò quyền.

Nếu chạy lại job (`rerun-failed-jobs`) thì **hỏng kiểu khác**:
`Multiple artifacts named "github-pages" were unexpectedly found. Artifact count is 2`
— vì lượt chạy lại sinh thêm artifact thứ hai cùng tên trong cùng một run, và
`deploy-pages` không biết chọn cái nào. Chạy lại lần nữa cũng không cứu được run đó.

**Đừng kết luận "push không kích hoạt deploy" chỉ vì thấy 404.** Ngày 2026-11-27 em
poll 20 lần × 15 giây thấy 404 và tưởng push không chạy; thật ra run `push` đã chạy và
**thành công** (`45958939342`), chỉ là em đang thử **sai đường dẫn**. Trước khi
dispatch, hãy xem danh sách run:

```bash
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/huuducbkb/game-hong-duc-lam/actions/runs?per_page=6" \
  | python3 -c "import json,sys; [print(r['id'],r['event'],r['head_sha'][:7],r['status'],r['conclusion']) for r in json.load(sys.stdin)['workflow_runs']]"
```

**Và nhớ: `docs/` là GỐC của web Pages, không phải thư mục con.** Workflow upload
`path: docs`, nên `docs/nhap/a.html` chạy ở `/nhap/a.html`, **không** phải
`/docs/nhap/a.html`. Thử sai tiền tố sẽ ra 404 y như file không tồn tại. Đây chính là
cái bẫy đã làm em mất 5 phút ngày 2026-11-27.

Cách sửa đúng — tạo **lượt chạy mới hoàn toàn**, không dính artifact cũ:

```bash
curl -s -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/huuducbkb/game-hong-duc-lam/actions/workflows/pages.yml/dispatches \
  -d '{"ref":"main"}'
```

Rồi kiểm bằng dữ liệu thật, đừng tin "push xong là xong":

```bash
curl -s "https://huuducbkb.github.io/game-hong-duc-lam/game/du-lieu/chuong2.json?v=$(date +%s)" | ...
```

Bài học: **push thành công ≠ web đã cập nhật.** Pages có CDN `max-age=600`, nên bản
cũ vẫn trả về bình thường trong 10 phút. Luôn kiểm `workflow_runs` xem lượt deploy
của đúng commit đó có `conclusion: success` không, trước khi kết luận là đã lên mạng.

### Ảnh chụp màn hình cho báo cáo: PNG chụp 2x là quá nặng, dùng JPEG

Ảnh chụp 390×844 ở `deviceScaleFactor: 2` lưu PNG nặng **1,1–1,7 MB mỗi ảnh**.
Bốn ảnh thành 4,2 MB — trên điện thoại 3G là mấy chục giây, và mỗi lần deploy
Pages phải đẩy thêm chừng ấy.

Đổi sang JPEG `quality=82`, **giữ nguyên 780 px** (2x cho màn retina): còn
117–240 KB, giảm 7 lần, chữ vẫn đọc rõ. Đừng hạ xuống 390 px — chữ mờ trên
điện thoại thật.

```python
from PIL import Image
im = Image.open(p).convert('RGB')          # giu 780px = 2x
im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
```

Nhớ `convert('RGB')` — PNG có alpha mà lưu thẳng sang JPEG sẽ lỗi.

### Test ghi đè ảnh thật: phải sao lưu ĐỦ mọi đường, và máy chủ đang chạy giữ cache

Hai lỗi liên tiếp trong `_test_api.py`, cả hai đều ngốn thời gian:

**1. Sao lưu thiếu đường.** Phép kiểm nén ảnh ghi đè `bc_cho_01` rồi phục hồi,
nhưng chỉ sao lưu `assets/scene/`, quên `docs/assets/scene/` — nơi máy chủ cũng
ghi. Kết quả: `docs/assets/scene/bc_cho_01.jpg` bị thay bằng ảnh nhiễu của test
(3,2 MB thay vì 190 KB). Ảnh hỏng vẫn "chạy" nên rất dễ lọt. Khi test cần ghi đè
file thật, phải sao lưu **mọi** đường mà code ghi tới, và `git status` phải sạch
sau khi chạy test — đó là cách phát hiện.

**2. Máy chủ giữ trạng thái lúc khởi động.** Cài Pillow xong nhưng `game_server.py`
đang chạy từ trước vẫn tưởng không có Pillow, nên bỏ qua đường nén: ảnh lưu ra
đúng bằng kích thước gốc và phép kiểm "nhẹ hơn ảnh gốc" hỏng. Không phải lỗi
code. Sửa: khởi động lại máy chủ sau khi cài thư viện.

Ngoài ra `_test_api.py` cần server ở cổng 12001:

```bash
python3 game_server.py &        # rồi mới chạy python3 game/_test_api.py
node game/_test_engine.js       # bộ JS không cần server
```

Bỏ Pillow thì bộ Python chỉ còn 178 phép kiểm (hai phép ảnh bị bỏ qua) — **con số
180 chỉ đúng khi đã cài Pillow**.

### Trang đọc truyện: hai lối vào in riêng, mạch chung in MỘT lần

`docs/nhap/cot-truyen-chuong2.html` sinh từ `tools/tao_trang_cot_truyen.py`.
Lần đầu viết, trang in trọn mạch chung cho cả hai nhánh: 105 đoạn, cao 76.000 px,
dài gấp đôi cần thiết. Nguyên nhân: đoạn rẽ cuối mỗi lối vào ("Xuống thung lũng")
dẫn thẳng vào mạch chung, nên hàm in chuỗi rẽ chạy tuốt qua cả chương còn lại.

Cách đúng: chia trang làm ba phần — lối vào tán tu, lối vào môn phái, rồi **mạch
chung in một lần**. Hàm in chuỗi rẽ phải nhận danh sách đoạn "đã in ở nơi khác"
để dừng lại.

**Nhưng dừng lại thôi chưa đủ — nhánh lồng trong nhánh còn bị bỏ sót.** Ngày
2026-11-27 kiểm lại trang này mới thấy nó in 60 bài mà **thiếu hai kết xấu**
(`c2_c24c_xau`, `c2_c26_xau`) và **trùng ba đoạn**. Lý do: hàm cũ duyệt nhánh rẽ
bằng một vòng `for` phẳng, chỉ in các đoạn của *chuỗi* rẽ, không gọi lại chính nó.
Kết xấu nằm sâu hai lớp (mạch chung → `c2_c24c` → `c2_c24c_xau`) nên không bao giờ
được in. Cách sửa: cho hàm **gọi lại chính nó** cho mỗi nhánh rẽ, và **cập nhật tập
`da_in` ngay khi in từng đoạn** (không phải sau khi in xong cả mạch) — nếu không,
hai nhánh rẽ khác nhau sẽ cùng in một đoạn.

Kiểm bằng số: `article.doan` phải là **60** (59 đoạn + "Lời kết chương"), **59 id
duy nhất**, không id nào trùng, và **không đoạn nào trong JSON bị thiếu**. Kiểm cả
hai id kết xấu có mặt trên trang.

### Sơ đồ cốt truyện: mỗi hành động một thẻ

`docs/nhap/so-do-cot-truyen.html` sinh từ `tools/tao_so_do_cot_truyen.py`, đọc
thẳng `game/chapters/chuong1.json` + `chuong2.json`. Cùng lỗi in trùng như trên
đã tái diễn ở đây: 137 thẻ nhưng chỉ 125 đoạn, vì khối "mạch chung" tự dò lại
mạch chính từ đầu thay vì nhận danh sách đoạn đã in. Cách sửa: `sinh_nhanh()`
nhận tham số `mach_san` (danh sách đoạn của mạch chung) và dùng luôn, không dò lại.

Ba chi tiết dễ sai, đã kiểm bằng máy:

- **Số liệu trên đầu trang phải khớp thứ đang in.** Ban đầu em ghi "38 chặng tán
  tu · C2" — con số ấy là cả mạch (lối vào + chung), gộp hai thứ khác nhau vào một
  nhãn. Nay tách: `10 lối vào tán tu · C2`, `6 lối vào môn phái · C2`.
- **`id` của `<h2>` phải duy nhất.** Ba khối Chương 2 dùng chung khuôn id
  `nhom-<nhóm>-c<chương>` nên khối "mạch chung" trùng id với "lối vào tán tu";
  bấm link nhảy sai chỗ. Nay khối chung có id riêng `chung`.
- **Đừng gọi lựa chọn đầu là "mạch chính" nếu nó có điều kiện.** Lựa chọn đầu mà
  khoá sau hảo cảm thì người chơi chưa đủ điều kiện sẽ đi nhánh khác. Nay chỉ đánh
  dấu `→` khi lựa chọn đầu **không** kèm `dieu_kien`.

Kiểm bằng số, đừng nhìn mắt: đếm `<details>`, đếm `id` duy nhất, rồi so với danh
sách id trong JSON của cả hai chương — phải ra **125 / 125 / 0 thiếu**. Kèm kiểm
`document.documentElement.scrollWidth > clientWidth` phải là `false` ở khổ 390px.

### Báo cáo / trang đọc cho người dùng
- `docs/nhap/chuong2-canon.html` — báo cáo sửa Chương 2 (ảnh chụp trong `docs/nhap/chuong2-canon/`).
- `docs/nhap/cot-truyen-chuong2.html` — toàn văn Chương 2, sinh bằng `python3 tools/tao_trang_cot_truyen.py`.
- Trang báo cáo mới luôn đặt trong `docs/nhap/`, tiếng Việt, khổ 390px.

## Vào thẳng một chương để thử: `?chuong=N`

Chơi lại Chương 1 (36 đoạn) chỉ để xem Chương 2 là quá phiền. Nay
`docs/game/play.html` nhận tham số URL:

```
/game/play.html?chuong=2                 # vào thẳng chương 2, xuất thân tán tu
/game/play.html?chuong=2&nhom=mon_phai   # nhánh môn phái
/game/play.html?chuong=2&ten=Hồng Đức     # đặt tên nhân vật
```

Ba chi tiết dễ làm hỏng:

1. **Bản mạng là `docs/game/play.html`, KHÔNG phải `game/play.html`.** Hai bản đã
   tách nhau (bản docs có thêm Cài đặt/avatar/key, 2695 dòng so với 2549). Sửa
   `game/play.html` rồi tưởng đã xong là mất công cả buổi.
2. **Phải gọi `window.vaoThangNhanh()`**, không chỉ ẩn `#setup`. Đường vào này
   không đi qua nút "Vào game" nên chưa có cú chạm nào mở khoá tiếng; thiếu nó
   thì cả phiên im.
3. **Đừng xoá phiên cũ.** Link thử chương mà xoá sạch `hdttl_phien` là người chơi
   mất tiến trình thật. Cất sang `hdttl_phien_cu` trước.

Đọc chữ ra để kiểm: `#storyBody` (không phải `#storyText` — không tồn tại), và
`#storyChapter` cho tên chương.

## Lời kể nói "Nhận:" thì dữ liệu đoạn phải thật sự thêm đồ

Chương 2 từng có sáu đoạn kể "Nhận: Thăng Tiên Lệnh" nhưng `lua_chon[].hieu_ung` không có
`them_vat`. Người chơi đọc thấy nhận đồ, mở túi ra trống; lựa chọn cần `co_vat: "Thăng Tiên Lệnh"`
lại bị khoá. Lỗi này **không** hiện ra khi chỉ đọc mã — chỉ hiện khi chơi hết một lượt rồi mở túi.

Ba luật rút ra:

1. **Lời kể không phải hiệu ứng.** Chữ "Nhận:" trong `ke` là văn, không phải lệnh. Món đồ chỉ
   vào túi khi `lua_chon[].hieu_ung.them_vat` có thật. Viết đoạn có nhận đồ thì phải gắn
   `them_vat`, và test phải canh: đoạn nào có `"Nhận:"` trong `ke` **và** có `lua_chon`
   thì phải có ít nhất một `them_vat`.
2. **Gộp theo `tên + trạng thái`** (`_nhan_vat` trong `engine.py`, `_ap_hieu_ung` trong
   `engine.js`). Nhận hai lần cùng món mà push thẳng là túi hiện hai dòng trùng tên,
   người chơi tưởng hai món khác nhau.
3. **Đọc kỹ ai là người nhận.** `c2_c24b` kể *Hàn Lập tự tay nhét lệnh vào vạt áo hắn* —
   người chơi không nhận gì. Gắn `them_vat` theo phản xạ là sai cả truyện lẫn túi.

## Nhánh kết xấu phải có điều kiện hảo cảm

`c2_c24c_xau` kể Hàn Lập bỏ đi, người chơi ra khỏi cốc một mình — nhưng lựa chọn dẫn vào
không có `dieu_kien`. Người chơi hảo cảm 75 ("thân thiết") vẫn vào được và đọc một đoạn
sai hoàn toàn với mối quan hệ đã dựng. Nay khoá bằng `dieu_kien.hao_cam_max` (`< 40`).

Điều kiện `hao_cam_max` là **mới** — `_dieu_kien_hop()` trong `engine.py` và `_kiem_dieu_kien`
trong `engine.js` phải cùng có, nếu không bản Python và bản web khoá khác nhau.

Khi sửa một đoạn kết, phải đọc **cả câu cuối** của nó: `c2_c24c_xau` từng viết "Trong tay ta
không có tấm lệnh nào" trong khi người chơi vừa được đặt một tấm vào tay.

## Kiểm vật phẩm: chơi thật rồi mở bảng Túi

```js
// trong Playwright, dùng chính engine của trang
const st = Engine.trang_thai_moi('T','', 'tan_tu');
st.chuong = 2; Engine.bat_dau(st);
for (const i of duongToi(st.doan_hien_tai, 'c2_c25b')) Engine.chon(st, i);
localStorage.setItem('hdttl_phien', JSON.stringify(st));
// reload → #openSys → .tab[data-tab="tui"] → đọc #dTuiDo
```

- Tab túi: `.tab[data-tab="tui"]`, nội dung ở `#dTuiDo`. Tab NPC: `.tab[data-tab="npc"]`, `#dNpc`.
- Đọc `textContent` để kiểm, đừng chỉ nhìn ảnh chụp.
- Trang thử dùng `waitUntil: 'domcontentloaded'`; `networkidle` treo vì trang có tiếng/fetch nền.

## Nhánh kết và hảo cảm: kiểm bằng hai mức, không kiểm một

Test chỉ thử mức hảo cảm cao sẽ không thấy nhánh kết xấu bị khoá nhầm. Luôn kiểm **cả hai**:
hảo cảm cao → kết xấu khoá; hảo cảm thấp → kết xấu mở.

## Giọng kể NPC theo hảo cảm: đổi cách đối xử, không chỉ đổi lời miêu tả

Biến thể `bien_the` phải khác nhau ở **hành động**, không phải ở vài chữ miêu tả. Đo bằng
`difflib.SequenceMatcher` giữa mọi cặp mức: cặp nào trên 85% là chưa đạt.

Lỗi đã mắc và cách sửa:
- Mức "người dưng" từng **giống hệt bản gốc từng chữ** (4 đoạn) → vô dụng, người chơi không thấy gì đổi.
- `c1_p17` thù địch/người dưng từng giống 96,2% (khác 2 câu) → viết lại toàn bộ 6 mức.
- Mức tử địch từng mở bằng "Chúng ta ra khỏi cốc" → tử địch không thể đi cùng nhau.

Mỗi mức phải trả lời: NPC **có giúp hay không, có nói thật hay không, có chia đồ hay không**.
- tử địch: doạ giết, không chia, bắt đi trước mặt
- tri kỷ: cho đồ không tính lời, nói rõ mình cũng đang giấu thứ gì

Dùng từ trực tiếp, **không nói giảm/nói tránh**. "Kẻ sắp bị loại" đã bị đổi thành
"kẻ sắp chết" — nói giảm làm nhạt đúng chỗ quan hệ cần gắt.

Phần cảnh gốc (sự kiện bắt buộc giữ) vẫn chiếm 78–81% ở `c1_d16`. **Đây là mức chấp nhận
được — người dùng đã chốt "giữ để không phá cốt truyện"**, đừng hạ tiếp bằng cách đổi câu
thoại gốc.

Kiểm nhanh trước khi commit:
```python
# 0 bản trùng gốc, 0 ngoặc lệch, cặp gần nhất < 85%
[f'{k}/{b["muc"]}' for k,v in d.items() for b in (v.get('bien_the') or [])
 if b['ke'].strip()==v['ke'].strip()]
[b['ke'].count('“')!=b['ke'].count('”') for b in ...]
```

## Biến thể giọng kể không được bịa lore mới

Lỗi đã mắc ở `c2_p08` (Tuyết Cơ, mức tri kỷ): tôi viết *"Ta đã có chủ"* để giải thích
vì sao nàng dạy người chơi. Câu này **mâu thuẫn trực tiếp với canon**:
- `c1_p09`: "Khế ước nô lệ — ngươi làm chủ, ta làm tớ."
- `c1_p10`: "Từ giờ, ngươi là chủ, ta là tớ."
- Toàn bộ chương 1–2 **không có chủ nào khác**. "chủ trước" duy nhất là của Hồng Trần
  (`c2_d12`), không liên quan Tuyết Cơ.

Quy tắc: biến thể chỉ được **đổi cách nói và cách đối xử**, không được thêm sự kiện,
nhân vật, hay quan hệ mới. Muốn NPC có lý do riêng thì lấy lý do **đã có trong canon**:
- Tuyết Cơ: "Ta không muốn tỉnh dậy trong một cái xác không còn ai gọi ta" (`c1_p13`).
- Hàn Lập: "Ta không muốn nghĩ tới chuyện ngươi chết ở một chỗ ta không biết."

Trước khi thêm một câu khẳng định về quá khứ vào biến thể, grep canon xem có không:
```bash
grep -o "chủ cũ\|chủ trước\|bản tôn\|chủ nhân\|sư phụ ta" game/chapters/*.json
```

Cũng đừng dùng hình ảnh trừu tượng thay cho nghĩa cụ thể, và đừng kéo tông cảnh lên nặng
hơn nó vốn có. "Tớ không được để chủ chết ở một cái chợ" — "chết ở chợ" không phải thành
ngữ, người đọc không hiểu. Nhưng sửa thành "chủ chết giữa chợ thì cả chợ biết tớ vô dụng"
cũng sai: cảnh `c2_p08` là nàng dạy cách nhìn tay người bán để không bị lừa — nhẹ, có
chút đùa ("giọng gần như cười"). Kéo chữ "chết" và "vô dụng" vào là lạc tông.

Đúng phải là: giữ nguyên việc nàng đang dạy gì, chỉ nói rõ ý. Bản đã chốt:
"Chủ mà bị lừa sạch tiền ngay giữa chợ thì tớ này mất mặt. Ta không muốn mất mặt."
Mức tri kỷ thêm: khế ước chỉ buộc nàng dạy, nàng dạy kỹ vì muốn người chơi học được cách
nhìn người — "Đó là thứ ta muốn ngươi mang theo, không phải mấy đồng bạc."

Trước khi sửa một câu, hỏi: cảnh này đang nói về việc gì? Nếu là chuyện nhỏ (trả giá,
nhận biết hàng giả) thì đừng đưa chết chóc, mất mạng, nhục nhã vào.

## Tài liệu giọng NPC sinh từ dữ liệu, không sửa tay

`TAI_LIEU_GIONG_NPC_6_MUC.md` do `tools/tao_tai_lieu_giong_npc.py` sinh. Sửa truyện xong
thì chạy lại tool. File `.md` 4 mức cũ đã xoá — đừng khôi phục.

## Trạng thái duyệt nội dung (2026-11-27)

Chương 1 và chương 2 đã được **người dùng duyệt là đạt** về cốt truyện và giọng kể NPC.
Đừng tự ý viết lại văn bản đã duyệt. Chỉ sửa khi người dùng chỉ ra đúng câu, đúng đoạn.
Sửa xong thì chạy lại `tools/tao_tai_lieu_giong_npc.py` và `tools/tao_so_do_cot_truyen.py`.

## Lựa chọn khác nhau phải ra cảnh khác nhau (2026-11-27)

Lỗi người dùng báo: ở `c2_d19` bấm "Hỏi: kẻ nào đang giữ?" hay "Cúi đầu, rời đi"
đều ra y hệt một cảnh. Không có gì cho biết mình vừa chọn gì.

Nguyên nhân: nhiều lựa chọn cùng trỏ `den` về một đoạn (để khỏi nhân bản cảnh),
mà lược đồ dữ liệu chỉ có `den` — không có chỗ ghi kết quả riêng. Toàn bộ chương
1 và 2 có **28 đoạn** như vậy, **73 lựa chọn**.

Cách sửa (đã làm, thay cho cách `ket_qua` cũ): **mỗi lựa chọn có một cảnh riêng**.
Chèn một đoạn mới cho từng lựa chọn, đoạn đó nối tiếp vào đích chung. Nhờ vậy
người chơi đọc được cảnh của chính mình chọn, không phải một câu nối gắn vào cảnh
dùng chung. Trường `lua_chon[].ket_qua` và hàm `_noi_chuyen_tiep` đã **bỏ** khỏi
`game/engine.py` và `docs/game/engine.js`.

Kết quả: chương 1 có 76 đoạn (thêm 10), chương 2 có 142 đoạn (thêm 62).
Không còn cặp lựa chọn nào trong một đoạn trỏ về cùng một đích.

Quy tắc khi viết chương mới:
- Trong một đoạn, hai lựa chọn **không được** cùng `den`. Muốn chung đích thì
  mỗi lựa chọn đi qua một cảnh riêng rồi cảnh đó mới nối vào đích.
- Cảnh riêng phải dài tối thiểu 300 ký tự và mở đầu **trung tính**: không giả định
  người chơi vừa làm một hành động cụ thể (vì cảnh dùng chung có thể tới từ nhánh
  khác).
- Giữ nguyên biến thể, ảnh, hiệu ứng của lựa chọn gốc khi tách cảnh.

Công cụ trong `tools/`:
- `tach_canh.py` — chèn cảnh riêng theo định nghĩa trong `canh_c2_*.py`.
- `kiem_dau.py` — soát lỗi dấu tiếng Việt (dùng kho ngữ liệu đã duyệt làm từ điển).
- `kiem_noi_tiep.py` — soát đầu ra trùng nhau giữa các lựa chọn.
- `sua_gia_dinh.py` — làm trung tính các câu mở đầu giả định hành động trước đó.

Test chặn tái phát — **đã có thật**, chạy được, và đã thử cố tình tạo lỗi để xem
nó có bắt không:

- `game/_test_engine.js` khối **N4**, `game/_test_api.py` khối **Q**.
- Mỗi chương kiểm bốn thứ: hai lựa chọn không cùng đích · mọi `den` đều tồn tại ·
  mọi đoạn ≥ 300 ký tự · **chọn thật từng lựa chọn rồi so văn bản** — hai lựa chọn
  khác nhau phải ra hai đoạn văn khác nhau.
- Đo lại: `node game/_test_engine.js` và `python3 game/_test_api.py` → cả hai phải
  **0 hỏng**, mã thoát 0.

### ⚠ Bài học: đừng ghi "đã có test" khi chưa viết test

Lần đầu sửa lỗi này, `AGENTS.md` được ghi là "đã có test chặn tái phát trong
`game/_test_engine.js`" — nhưng **không hề có test nào**. Câu đó sai, và nếu phiên
sau tin vào nó thì lỗi sẽ quay lại mà không ai biết. Khi viết vào tài liệu rằng
"đã có test", phải chạy test đó ngay và dán số đo thật vào. Tốt hơn nữa: cố tình
tạo lỗi một lần để chứng minh test **bắt được** lỗi (đã làm: sửa `c1_d05` cho hai
lựa chọn cùng đích → test báo `c1_d05 -> c1_d06_0 (2 lựa chọn)` và thoát mã 1).

### ⚠ Tách cảnh dễ để lại cảnh mồ côi

Khi tách cảnh, cảnh CŨ vẫn nằm trong JSON nếu không xoá — người chơi không bao giờ
tới được, nhưng nó vẫn tốn chỗ, vẫn lọt vào sơ đồ cốt truyện và bản xuất .txt, và
làm người đọc tưởng có nhánh chưa viết. Đã gặp: `c2_p04_0` và `c2_p23_2` mồ côi sau
lần tách cảnh đầu tiên (đã xoá, chương 2 còn 140 đoạn).

Cách kiểm — duyệt từ `doan_dau_theo_nhom`, đoạn nào không tới được là mồ côi:

```bash
python3 - <<'EOF'
import json, io
for so in (1, 2):
    d = json.load(io.open(f'game/chapters/chuong{so}.json', encoding='utf-8'))
    D = {x['id']: x for x in d['doan']}
    thay, hang = set(), list(d['doan_dau_theo_nhom'].values())
    while hang:
        x = hang.pop()
        if x in thay or x not in D: continue
        thay.add(x)
        hang += [l['den'] for l in D[x].get('lua_chon') or [] if l['den'] != '__ket_thuc__']
    print(f'chuong{so}: {len(D)} doan, mo coi: {sorted(set(D) - thay)}')
EOF
```

Cả hai chương phải in `mo coi: []`. Test **N4/Q** đã kiểm tự động điều này.

### Kết thua: đoạn khai hai cờ, không phải "đoạn cụt"

Từ chương 2 có kết thua (`c2_d27c_thua`, `c2_p23c_thua`). Một đoạn kết thua phải khai
**cả `ket_thuc: true` và `thua: true`**, và **không có `lua_chon`**:

- Thiếu `ket_thuc` → engine coi như cảnh thường, `_goi_y` trả về danh sách lựa chọn rỗng
  và người chơi kẹt ở một màn im lặng, không biết mình đã chết.
- Thiếu `thua` → engine coi là **khép chương**: hiện nút "Sang chương 3", tức là người
  chơi chết mà vẫn đi tiếp.
- Có `lua_chon` → đó là cảnh thường, không phải kết.

`_goi_y` đặt `state["ket_thuc"] = True` khi bước vào đoạn thua, để bản lưu và payload
khớp nhau. `_man_ket_thua` trả `thua: true`, `chuong_sau: None`, `lua_chon: []`,
`cho_phep_tu_do: false`; giao diện dựa vào `kq.thua` để bày nút lùi / chơi lại.

Hai bẫy đã gặp khi thêm kết thua:

- **Test "không có đoạn cụt" báo hỏng** vì nó coi mọi đoạn không có lựa chọn là cụt.
  Phải cho đoạn `ket_thuc && thua` đi qua — nhưng vẫn kiểm nó khai đủ cờ.
- **Đường đi trong test phải là đường bấm được.** Hàm tìm đường (`_duong` / `duongToi`)
  duyệt mọi cạnh, kể cả lựa chọn bị khoá và đoạn thua, nên "tới được" trên giấy mà người
  chơi thật không tới được. Đã sửa: bỏ cạnh có `dieu_kien` và cạnh dẫn vào đoạn `thua`.

Khi thêm cảnh làm tăng số nhánh, coi chừng **bộ test treo** chứ không hỏng: hàm duyệt hảo
cảm ở mục L từng đệ quy không có tập đã thăm, thêm vài nhánh là số đường nổ theo cấp số
nhân (đo được >5 triệu lần gọi). Đã đổi sang duyệt theo cặp `(đoạn, hảo cảm)` đã thăm.

### Bẫy khi chạy lại `tools/tach_canh.py`

Script này **không idempotent**: chạy hai lần lên cùng dữ liệu sẽ tạo cảnh lồng
nhau (`c2_d27_0_0`). Trước khi chạy lại phải `git checkout game/chapters/*.json`
để về bản gốc, rồi chạy đúng một lượt. Sau khi chạy, kiểm ngay: không có mã đoạn
lặp `.json` hai lần dạng `_0_0`.

## Ảnh Chương 2: prompt có mà ảnh không bao giờ vào game (2026-11-28)

Hai lỗi độc lập, cộng lại làm **toàn bộ đường up ảnh của Chương 2 vô dụng**:

1. **Không có ánh xạ ảnh → đoạn.** `tools/xuong_chuong2.py` có prompt nhưng không có
   `doan_cua_anh()`, và `tools_server.py` chỉ nạp ánh xạ của nhánh môn phái chương 1.
   Up ảnh xong file nằm trong `assets/scene/` nhưng **không đoạn nào nhận ảnh**.
2. **`xuong_tu_dong.CHUONG_FILES` chỉ có `chuong1.json`.** Kể cả có ánh xạ, ảnh cũng
   **không được ghi vào dữ liệu chương**. Thêm chương mới là **phải thêm cả hai bản**
   (`game/chapters/` và `docs/game/du-lieu/`) vào danh sách này.

Quy tắc từ nay (đã có test chặn, khối **S** trong `game/_test_api.py`):

- Mỗi cảnh khai **một** trường `doan`; `doan_cua_anh()` **suy ra** từ `doan`, không
  viết tay hai danh sách để chúng lệch nhau.
- Không để cảnh mồ côi: cảnh không trỏ tới đoạn nào, hoặc đoạn thiếu ảnh mà không có
  cảnh. Test S kiểm cả bốn chiều: đoạn tồn tại · một đoạn một cảnh · mọi đoạn thiếu ảnh
  đều có cảnh · cảnh nào cũng có nhóm cảnh.
- Đổi `CHUONG_FILES` là phải chạy lại test S; nó bắt đúng lỗi "chỉ ghép chương 1".

Đo nhanh phủ cảnh một nhánh (phải ra `0`):

```bash
python3 -c "
import json, importlib.util as u
s=u.spec_from_file_location('c2','tools/xuong_chuong2.py'); m=u.module_from_spec(s); s.loader.exec_module(m)
d=json.load(open('game/chapters/chuong2.json',encoding='utf-8'))
thieu={x['id'] for x in d['doan'] if x['id'].startswith('c2_d') and not (x.get('hinh_anh') or {}).get('anh')}
print(len(thieu - {c['doan'] for c in m.SCENES}), len(m.SCENES))"
```

### Mã ảnh dài làm bảng Xưởng tràn ngang

Thêm 58 mã mới (dài nhất `nv_c2_han_lap_ban_hang`) làm bảng "danh sách ảnh" rộng ra
6px ở khổ 390. Sửa trong CSS của `tools/build_xuong.py`: `table-layout:fixed` +
`overflow-wrap:anywhere` cho `th,td`. Đo lại bằng iframe 390px (Chromium headless bỏ
qua `--window-size` nên **phải đo trong iframe**, đừng tin `--window-size`):

```bash
# xuất trang đo vào docs/ rồi: scrollWidth phải BẰNG clientWidth
chromium --headless=new --no-sandbox --disable-gpu --dump-dom <url-trang-do>
```
