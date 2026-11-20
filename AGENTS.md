# Hồng Đức Tu Tiên Lộ

Game AI text tu tiên chạy trên web. Đồng nhân xuyên không dựa trên *Phàm Nhân Tu Tiên* (Vong Ngữ).
Người chơi xuyên không vào thế giới đó, sống cùng thời Hàn Lập.

Người dùng chỉ có **Safari (iPad/iPhone), KHÔNG có terminal** → mọi thứ phải qua giao diện web.

## QUY TẮC BẮT BUỘC: dùng phương pháp PIC-IN-GAME

**Mọi việc đụng đến thiết kế giao diện, tạo hình ảnh, hoặc video ngắn → PHẢI dùng
quy trình PIC-IN-GAME.** Không tự nghĩ cách khác.

- Skill: `.agents/skills/pic-in-game/SKILL.md`
- Báo cáo đầy đủ: `tai-lieu/PIC-IN-GAME-report.md`

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
