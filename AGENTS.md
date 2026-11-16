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

## Bản game JS trên GitHub Pages (đã phát hành)

> ⚠️ **QUYẾT ĐỊNH CỐ ĐỊNH — KHÔNG TẠO REPO MỚI.** Chỉ dùng **duy nhất** repo
> `huuducbkb/game-hong-duc-lam`. Người dùng đã nhắc **5 lần** (13/11 "nếu đã có repo
> game hong duc lam rồi thì không cần tạo nữa"; "tại sao bạn cứ muốn làm repo game tu
> tiên"; 15/11 "bỏ cái yêu cầu tạo repo đó chúng ta đã có repo rồi"). **Tuyệt đối
> không gọi** `POST /user/repos`, `gh repo create`, hay mở https://github.com/new.
> Mọi thay đổi push thẳng vào `main` của repo có sẵn.

- **Link chơi**: https://huuducbkb.github.io/game-hong-duc-lam/game/
- Nguồn JS nằm ở `docs/game/`: `play.html` (giao diện), `engine.js` (dịch từ `game/engine.py`),
  `ai.js` (dịch từ `game/ai.py`), `du-lieu/` (JSON dùng chung với bản Python).
- Chạy **không cần server** — mở file là chơi. Key Gemini do người chơi tự nhập qua nút
  **⚙️ Cài đặt**, lưu trong `localStorage` (`hdttl_gemini_key`). **Không nhúng key vào code.**
- Trang `docs/index.html` (GitHub Pages) có nút "🎮 Chơi game".
- **Bẫy cần nhớ**: công cụ trình duyệt tự động không gõ được vào ô `type="password"`;
  muốn kiểm thử luồng key thì đặt thẳng vào `localStorage` hoặc dùng Node (mock `localStorage` + `fetch`).
- Engine không dùng `random` → chơi lại cho kết quả y hệt (tất định).
- Test: `node game/_test_engine.js` → 105/105; `python3 game/_test_api.py` → 157/157 (cần `game_server.py` đang chạy).

### Túi đồ khởi đầu

Nhân vật mới chỉ có **Bạc vụn ×3** (`bac: 3` + `tui_do`). Trước đây có thêm
`Ngọc vụn bí ẩn ×1` — di chứng của bản thảo ngôi-thứ-hai cũ (mảnh ngọc dẫn
xuyên không, xem `GOP-Y-BAN-THAO.md`). Chi tiết đó đã bỏ khỏi truyện nên món
này không đoạn nào nhắc, không logic nào dùng → đã xóa khỏi `trang_thai_moi()`
ở **cả** `game/engine.py` và `docs/game/engine.js` (giữ 2 bản khớp nhau).
- Deploy tự động qua `.github/workflows/pages.yml` khi push lên `main` (đường dẫn `docs/**`).

### Cơ duyên trong túi (đã chốt với người dùng)

Cơ duyên (bảo vật gắn với nhân vật) là **linh hồn truyện** — mỗi nhánh xuất thân có
một cơ duyên riêng (môn phái: Ngọc cốt; tán tu: Hồng Trần Kiếm Hạp). Quyết định giao
diện, chốt trong `tai-lieu/KE-HOACH-SUA-CHUONG-1.md` mục 7:

- Vật có cờ `co_duyen: true` **luôn xếp đầu** danh sách túi đồ.
- **Viền gradient nhiều màu** chạy động (`.sys-row.co-duyen::before` + `@keyframes cdChay`).
- **Bấm vào → hiện bảng thông tin** (`#coDuyen`): tên, `trang_thai`, `mo_ta`.
- Dữ liệu món cơ duyên có thêm 2 trường: `co_duyen` (cờ) + `trang_thai` (chuỗi hiển thị,
  ví dụ `"chưa khế ước"` → `"đã khế ước · đang hồi phục"`).

**Cách đổi trạng thái cơ duyên:** dùng khoá hiệu ứng `doi_trang_thai` trong `hieu_ung`
của lựa chọn — dạng `{"doi_trang_thai": {"Ngọc cốt bí ẩn": "đã khế ước · đang hồi phục"}}`.
Engine tìm món theo **đúng tên** trong `tui_do` rồi ghi đè `trang_thai`. Hiện gán ở
`c1_p09c` (lựa chọn "Ta ký"). **Sửa cả 2 engine** (`game/engine.py` + `docs/game/engine.js`)
và **cả 2 file dữ liệu** (`game/chapters/chuong1.json` + `docs/game/du-lieu/chuong1.json`).

**Đừng quên:** khi thêm món cơ duyên mới, phải có cả `co_duyen`, `trang_thai`, `mo_ta` —
thiếu `trang_thai` thì bảng thông tin sẽ ẩn dòng trạng thái (không lỗi, chỉ thiếu thông tin).

### Bài học: gắn sự kiện phải an toàn với null

Lỗi "giao diện tè le" (nút Hệ Thống / tab / đổi ảnh không bấm được) do một dòng
`$("#closeCaiDat").onclick = ...` trỏ tới phần tử **không tồn tại** → `TypeError` →
**mọi dòng gắn sự kiện phía sau đều chết theo**. Vì vậy trong `play.html` dùng hàm
`gan(sel, ev, fn)` (kiểm tra `null` trước khi gắn) cho các nút ở cấp cao nhất.

Khi thêm nút/màn mới: **luôn kiểm tra `id` trong JS có tồn tại trong HTML**, và
kiểm thử bằng chromium headless (dump-DOM + iframe tự bấm) trước khi đẩy lên.

### Bẫy bố cục thanh trên (màn hẹp)

Thanh trên (`header.topbar`) là flex 1 hàng. Trên iPhone (≤430px) nhồi nhiều nút sẽ
bóp `.titles` xuống ~28px → chữ tiêu đề/phụ **wrap thành cột dọc**, thanh cao vọt lên
146–163px. Cách xử lý: `@media (max-width:430px)` cho `.topbar{flex-wrap:wrap}`, cho
tiêu đề chung hàng với avatar và các nút xuống hàng dưới trải đều; `.titles .sub` cần
`white-space:nowrap;overflow:hidden;text-overflow:ellipsis`.

### Cách tự kiểm thử giao diện (không cần server)

`chromium --headless=new --no-sandbox --dump-dom` một trang harness tự tạo iframe
`play.html` rồi tự bấm nút, in kết quả vào `<pre>` để đọc. Chạy server tĩnh tạm bằng
`python3 -m http.server <cổng>` trỏ vào thư mục chứa bản cần đo.

### Ảnh cảnh truyện (thư viện ảnh — đã chốt với người dùng)

Ảnh lớn trên đầu khung truyện, **đổi theo mỗi đoạn** (kiểu visual novel). Đoạn nào
chưa gắn ảnh thì khung ảnh **ẩn**, hiện nền giấy như cũ.

- **Cách A (đang dùng):** mỗi đoạn ghi thẳng tên ảnh — `hinh_anh.anh` trong
  `chuong1.json` (giữ nguyên `hinh_anh.tags` cũ). Không tốn token, không đoán sai.
  Cách B (AI tự tra theo thuộc tính) để sau.
- Thư viện: `docs/assets/library/index.json` (mô tả `loai`, `mo_ta`, `tags`, `dung_o`).
  Ảnh để ở `assets/scene/` (bản Python) **và** `docs/assets/scene/` (bản Pages) — phải có **cả hai**.
- Giao diện: `#sceneBox` + `#sceneImg` + `#sceneCap` (caption = `boi_canh`), bấm ảnh mở
  phóng to `#sceneLb`; đóng bằng nút `#closeSceneLb` hoặc phím Escape.
- Nạp ảnh: mở **Xưởng** (`python3 tools_server.py`, cổng 12001) → copy prompt → vẽ →
  upload. Tên file phải bắt đầu `bc_` (bối cảnh) / `vt_` (vật phẩm) / `nv_` (nhân vật)
  thì Xưởng tự lưu vào `assets/scene/` + `docs/assets/scene/`.
- Xưởng cũng nằm trong `game_server.py` tại `/upload` (chỉ cần 1 server đang chạy). Hàm
  lưu ảnh dùng chung: `tools_server.luu_anh(name, b64)`.
- **Bẫy**: `game_server.py` phải định tuyến `/upload` **trước** khi đọc body JSON —
  `_body_json()` đọc hết `Content-Length` nên đọc trước là body cạn, upload trả 400/500.
- Prompt 4 ảnh thử nằm trong `tools_server.py` mục `ASSETS` (nhóm "Bối cảnh truyện").
  Đã gắn 20 đoạn Chương 1 với 4 ảnh: `bc_cho_01.jpg`, `bc_tan_xa_dem.jpg`,
  `vt_ngoc_cot.jpg`, `nv_tuyet_co.jpg`. Ưu tiên khi một đoạn khớp nhiều ảnh:
  **nhân vật > vật phẩm > bối cảnh**.

#### Nhận diện ảnh hàng loạt — không phải đặt tên file (đã chốt với người dùng)

Người dùng vẽ nhiều ảnh trên iPad; tên file kiểu `IMG_4821.JPG` và **không phải đổi tên**.
Xưởng tự đoán mỗi ảnh thuộc prompt nào rồi cho xác nhận. Mô-đun: `game/nhan_dien_anh.py`.

Bốn lớp, xếp theo mức tăng độ đúng:
1. **Lọc theo tỷ lệ** (thuần Python, đúng 100%, không tốn token): `kich_thuoc_anh()` đọc
   header PNG/JPEG/GIF/WebP (không cần PIL); `loc_ung_vien()` loại asset sai tỷ lệ. Nếu chỉ
   còn **1 ứng viên** → gán luôn, **không gọi AI**.
2. **Đưa AI nguyên văn `prompt` tiếng Anh** (không chỉ tên ngắn) — khớp câu gốc đã dùng để vẽ.
3. **Tả trước, chọn sau**: AI trả JSON `{mo_ta, key, do_tin_cay, ly_do}`, `temperature=0`,
   `responseMimeType=application/json`.
4. **Màn duyệt**: `do_tin_cay >= 80` (và có key) → `tu_dong=True`; dưới ngưỡng → hiện lưới
   ảnh thu nhỏ + ô chọn prompt để người dùng xác nhận.

API (cả `tools_server.py` lẫn `game_server.py`, định tuyến **trước** khi đọc body):
- `POST /doan_anh` `{anh:[{name,data(b64)}]}` → `{ok, ket_qua:[{name,kich_thuoc,ung_vien,key,ten,file,do_tin_cay,mo_ta,ly_do,tu_dong}], loi}`
- `POST /luu_loat` `{ds:[{key,data(b64)}]}` → `{ok, da_luu:[{key,file}], loi}` (lưu theo **key**, tự đặt tên file đúng)
- Hàm dùng chung: `TS.xu_ly_nhan_dien(anh_list, env)`, `TS.xu_ly_luu_loat(ds)`, `TS.luu_theo_key(key, b64)`, `TS.con_thieu_anh()`.

Giao diện Xưởng: khu **Duyệt ảnh** (`#review`/`#grid`) + `DANH_SACH` (danh sách asset cho ô chọn),
nút **Lưu ảnh** (`#saveBtn` → `/luu_loat`); phần "Ảnh đã nhận" nhắc **còn thiếu mấy ảnh**.

Lưu ý: model Gemini có thể bị khai tử/503 theo tài khoản — dùng danh sách dự phòng
`MODEL_DU_PHONG` (hiện `gemini-flash-lite-latest` chạy tốt; `gemini-2.5-flash` đã 404).

**Người dùng vẽ ảnh bằng Gemini chat bên ngoài** (không dùng API để vẽ; key Gemini chỉ dùng
cho nhận diện). Nên Xưởng có khu **"🎨 Vẽ cả bộ bằng 1 prompt"**: `build_gop_prompt()` gộp
cả 11 asset thành 1 prompt (chung phong cách + danh sách từng ảnh kèm tỷ lệ/tên file), hiện
trong `#gop` + nút Copy + nút tải `.txt` (`taiPromptGop()`). `_prompt_than()` bỏ phần `STYLE`
chung để không lặp. Prompt gộp nhắc AI vẽ lần lượt, hết lượt thì người dùng nhắn "tiếp tục".

`STYLE` = `STYLE_GOC` + `NO_TEXT`. Ấn son dùng `STYLE_CHU` (= `STYLE_GOC` + cho phép đúng 2
chữ Hán **洪德** trong dấu) — nếu để `NO_TEXT` thì AI vẽ ra con dấu trống.

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
