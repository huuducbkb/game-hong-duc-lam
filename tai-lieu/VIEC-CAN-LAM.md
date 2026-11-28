# Việc cần làm — Hồng Đức Tu Tiên Lộ

> **Sổ việc sống.** Cập nhật mỗi khi có việc mới hoặc xong việc.
> Quy ước: `[ ]` chưa làm · `[~]` đang làm · `[x]` xong.
> Cập nhật lần cuối: **2026-11-28 (tiếp 3)**

---

## ✅ XONG 2026-11-28 (tiếp 4) — "Tiến vào tu luyện": RPG cày cuốc đã chạy được

Trước phiên này chỉ là **thảo luận trên giấy**. Nay đã có mã, có giao diện, có test.
Người dùng chốt 3 câu cuối: **ngân sách cách A** · **theo bảng chi phí đề xuất** ·
**dò la ra tin ngẫu nhiên**.

### Đã chốt và đã làm đúng như chốt

| Chốt | Cài trong mã |
|---|---|
| Ngân sách **30 ngày dùng chung cả chương** (cách A) | `NGAY_MOI_CHUONG = 30`; `vao_dong`/`ra_dong` **không** cấp lại ngày. Sang chương mới cấp lại 30, nhưng giữ `ngay_da_dung` để dãy ngẫu nhiên không lặp y nguyên |
| Trần **Luyện Khí tầng 6** chương 2 | `TRAN_CANH_GIOI = {2: "Luyện Khí tầng 6"}`, ép trong `_thang_cap`. Cày 200 lần vẫn dừng ở tầng 6 — có test |
| Nhân vật tu luyện **là** nhân vật truyện | Dùng chung `state`: tu vi, sinh lực, bạc, túi đồ. Xuất động là tab Nhân vật đổi ngay |
| Nút trong ngăn kéo **Hệ Thống** → màn toàn khổ | `#moTuLuyen` trong `docs/game/play.html`, mở `#tuLuyen` (fixed, `z-index:16`) |
| **Mỗi nút ghi rõ giá trước khi bấm** | Mỗi dòng việc có `3 ngày` / `2 ngày · 45% thắng` ngay trên nút |
| Đấu pháp ngắn, hiện tỉ lệ thắng bằng số, có Rút | `tl_dau` (xem trước, **không tốn ngày**) → `tl_danh` (3 hiệp) |
| Thua = bị thương, **không chết** | `sinh_lực` giảm, chặn săn khi dưới 30%, nghỉ 1 ngày hồi 6 |
| Xúc xắc **có hạt giống** | FNV-1a + LCG 32 bit; bản Python và bản JS ra **đúng cùng dãy số** |
| Lưu game = **xuất file save** + dòng nhắc | `#xuatSave` / `#nhapSave` + dòng nhắc trong bảng Hệ Thống |
| Boss **nhiều đường qua** | Khoá `canh_gioi` (đánh thẳng) và khoá `tin` (đường mưu) — cả hai thêm vào cơ chế khoá sẵn có, không xây hệ mới |

### 5 việc trong động phủ (số là **đoán, chưa cân bằng**)

| Việc | Ngày | Kết quả |
|---|---|---|
| Đả tọa | 3 | +8 tu vi, không rủi ro |
| Săn yêu thú | 2 | nguyên liệu + 3 tu vi, 35% bị cắn −8 sinh lực |
| Luyện đan | 1 | 2 công thức (Tụ Khí Đan 70%, Hồi Lực Đan 65%), tốn bạc + nguyên liệu |
| Đi chợ | 1 | Linh thảo 2 bạc · Bánh nướng 1 bạc |
| Dò la | 2 | 55% chỉ nghe chuyện vặt; ra tin thì mở một đường qua cổng boss |
| Nghỉ | 1 | +6 sinh lực (cần sau khi bị thương) |

**Dò la ngẫu nhiên có chủ đích**: 3 tin (`bi_thuong`, `thoi_quen`, `so_lenh_bai`), mỗi tin
mở một đường khác nhau. Đã ra tin rồi thì không ra lại tin đó.

### Số đo kiểm chứng (chạy lại được)

| Lệnh | Kết quả |
|---|---|
| `node game/_test_engine.js` | **248 đạt, 0 hỏng** (thêm 39 phép kiểm khối TL) |
| `python3 game/_test_api.py` | **289 đạt, 0 hỏng** (thêm 27 phép kiểm khối TL) |
| Đối chiếu hạt giống Python ↔ JS | `_hat_giong("Hàn Lập", 0)` = **254229688** ở **cả hai** bản |
| Cố tình phá trần (`tran = null`) | test báo **"mong đợi tầng 11, nhận được tầng 6"** → chốt chặn bắt đúng lỗi |
| Khổ 390×844 | 7 nút màn chính đều **≥44px**, không tràn chữ, `scrollWidth 390 = clientWidth 390` |
| Xuất → xoá localStorage → nạp file | tu vi 20, ngày 27 **khớp tuyệt đối** |

### File đã sửa

- `game/engine.py` — khối tu luyện (5 việc + nghỉ), trần cảnh giới, khoá `canh_gioi`/`tin`
- `docs/game/engine.js` — bản dịch **khớp từng số** với bản Python
- `docs/game/play.html` — nút trong ngăn kéo, màn Động phủ + 4 màn phụ, xuất/nhập save
- `game_server.py` — thêm `POST /api/tu_luyen` (một đường cho xem/việc/vào/ra)
- `game/_test_engine.js`, `game/_test_api.py` — khối TL, TL2, TL3, TL4

### Còn để ngỏ (không chặn)

- **Chưa nối vào dữ liệu truyện**: chưa có đoạn nào trong `chuong2.json` khai
  `dieu_kien: {canh_gioi: ...}` hay `{tin: ...}`. Cơ chế đã sẵn, chỉ chờ quyết cảnh nào làm cổng.
- Số cân bằng (8 tu vi / 3 ngày, 45% thắng…) là **đoán** — chơi thử rồi chỉnh.
- Chưa có ảnh cho màn Động phủ; đang dùng nền giấy sẵn có.

## 🔴 ĐANG LÀM

### ✅ XONG 2026-11-28 — Chương 2 nhánh tán tu: đủ 58 cảnh + ảnh vào được game

- [x] `tools/xuong_chuong2.py` viết lại: **58 cảnh**, mỗi cảnh đúng **một** đoạn
  (trường `doan`), 19 nhóm cảnh, `doan_cua_anh()` suy từ `doan` → không thể lệch.
- [x] **Sửa lỗi 1**: prompt Chương 2 trước đây không có ánh xạ đoạn → up ảnh không ai nhận.
- [x] **Sửa lỗi 2**: `xuong_tu_dong.CHUONG_FILES` chỉ có `chuong1.json` → ảnh Chương 2
  không được ghi vào dữ liệu chương. Đã thêm cả 2 bản của `chuong2.json`.
- [x] Bảng danh sách ảnh trong Xưởng hết tràn ngang ở khổ 390 (`table-layout:fixed`).
- [x] Chốt chặn: khối **S** trong `game/_test_api.py` (7 phép kiểm).

### ✅ XONG 2026-11-27 (tiếp 3) — Cảnh chiến đấu chương 2 + nhánh "kết thua"

Trước: chương 2 **không có cảnh nào người chơi thật sự đánh nhau**; cao trào chỉ là đứng
nhìn Hàn Lập giết người. Nay mỗi nhánh có **3 cảnh đánh** và **1 nhánh thua**.

Chương 2: **140 → 164 đoạn** (thêm 24).

| Nhánh | Cảnh | Mã đoạn |
|---|---|---|
| Tán tu | Ba kẻ áo xám đêm (3 cách đánh) | `c2_d22c_0/1/2/3` |
| Tán tu | Tà tu bị thương ở miệng khe | `c2_d25c_0/1/2` |
| Tán tu | Bị chặn đường (4 lựa chọn) | `c2_d27c_0/1/2/3` + `c2_d27c_thua` |
| Môn phái | Ba kẻ áo xám đêm | `c2_p19c_0/1/2/3` |
| Môn phái | Tà tu bị thương | `c2_p22c_0/1/2` |
| Môn phái | Bị chặn đường | `c2_p23c_0/1/2/3` + `c2_p23c_thua` |

Kết thua khai `ket_thuc: true` + `thua: true`, **không có `lua_chon`**; giao diện bày nút
"Lùi lại, đánh khác" và "Chơi lại từ đầu". Canon: người chơi Luyện Khí tầng 1–3 **không
giết được tà tu tầng cao** — mọi cảnh đánh là thoát thân/chọn địa hình, trừ tà tu đã bị
thương nặng (và đó là lựa chọn của người chơi).

Đo lại — cả hai phải **0 hỏng**, mã thoát 0:

```bash
node game/_test_engine.js      # -> 209 đạt, 0 hỏng
python3 game/_test_api.py      # -> 262 đạt, 0 hỏng  (cần game_server.py chạy cổng 12001)
```

Kiểm phủ cảnh Chương 2 (phải ra `0` / `0 70`):

```bash
python3 -c "
import json, importlib.util as u
s=u.spec_from_file_location('c2','tools/xuong_chuong2.py'); m=u.module_from_spec(s); s.loader.exec_module(m)
d=json.load(open('game/chapters/chuong2.json',encoding='utf-8'))
thieu={x['id'] for x in d['doan'] if x['id'].startswith('c2_d') and not (x.get('hinh_anh') or {}).get('anh')}
print(len(thieu - {c['doan'] for c in m.SCENES}), len(m.SCENES))   # -> 0 70"
```

- [ ] **Chương 2 nhánh môn phái — 67 đoạn chờ khai cảnh** (`c2_p07` → `c2_p23c_thua`)
  - Làm y hệt nhánh tán tu: mỗi cảnh một đoạn, khai trong `tools/xuong_chuong2.py`
    (hoặc module riêng `xuong_chuong2_monphai.py`), thêm nhóm cảnh, rồi dựng lại Xưởng.
  - **Chặn cứng**: khối **S** trong `game/_test_api.py` đòi mọi đoạn thiếu ảnh phải có cảnh,
    nên thêm đoạn mới mà không khai cảnh là test hỏng ngay (đã gặp 2026-11-27).
  - Đo được: `python3 -c "import json;d=json.load(open('game/chapters/chuong2.json'));print(sum(1 for x in d['doan'] if x['id'].startswith('c2_p') and not (x.get('hinh_anh') or {}).get('anh')))"`
    → hiện **67**, mục tiêu **0**

- [ ] **Chương 2 — vẽ 70 cảnh nhánh tán tu** (người dùng làm, Xưởng đã có prompt)
  - Đo được: Xưởng ghi `Chương 2 · Thái Nam Sơn Cốc` → **0/70 đã có**, mục tiêu **70/70**

Xưởng ảnh: 12 cảnh chiến đấu mới **đã khai** trong `tools/xuong_chuong2.py`
(**70 cảnh**, 23 nhóm) để khối **S** không báo hỏng — ảnh chưa vẽ, chỉ mới có prompt.

Sơ đồ + txt đã xuất lại: **240 thẻ**, 10 mã cảnh mới, không tràn ngang ở 390.

### ✅ XONG 2026-11-27 — Chốt chặn "lựa chọn khác nhau phải ra cảnh khác nhau"

Đã có test thật (trước đó tài liệu ghi nhầm là đã có): khối **N4** trong
`game/_test_engine.js`, khối **Q** trong `game/_test_api.py`.

Đo lại — cả hai phải **0 hỏng**, mã thoát 0:

```bash
node game/_test_engine.js      # -> 207 đạt, 0 hỏng
python3 game/_test_api.py      # -> 249 đạt, 0 hỏng  (cần game_server.py chạy cổng 12001)
```

Chứng minh chốt chặn bắt được lỗi: cho `c1_d05` hai lựa chọn cùng trỏ `c1_d06_0`
→ test báo `c1_d05 -> c1_d06_0 (2 lựa chọn)` và thoát mã 1.

Kiểm cảnh mồ côi (đoạn không ai trỏ tới) — cả hai chương phải ra `[]`:

```bash
python3 -c "
import json,io
for so in (1,2):
    d=json.load(io.open(f'game/chapters/chuong{so}.json',encoding='utf-8'))
    D={x['id']:x for x in d['doan']}
    thay,hang=set(),list(d['doan_dau_theo_nhom'].values())
    while hang:
        x=hang.pop()
        if x in thay or x not in D: continue
        thay.add(x); hang+=[l['den'] for l in D[x].get('lua_chon') or [] if l['den']!='__ket_thuc__']
    print(f'chuong{so}: {len(D)} doan, mo coi: {sorted(set(D)-thay)}')
"
```

⚠ `tools/tach_canh.py` **không idempotent** — chạy lại phải `git checkout
game/chapters/*.json` trước, nếu không sẽ sinh cảnh lồng `c2_d27_0_0`.

### ✅ XONG 2026-11-27 — Nút tải toàn bộ cốt truyện (.txt)

Trang `docs/nhap/so-do-cot-truyen.html` có nút **⬇ Tải toàn bộ cốt truyện (.txt)**.
Tệp `docs/nhap/cot-truyen-day-du.txt` sinh tự động, 144/144 đoạn, 256.669 byte.

Đo lại: `python3 tools/tao_so_do_cot_truyen.py` rồi
`grep -o '── \[[a-z0-9_]*\]' docs/nhap/cot-truyen-day-du.txt | wc -l` → phải ra **144**.

### ✅ XONG 2026-11-27 — Danh sách link bàn giao đúng năm chỗ

`tools/ban_giao.py` in đúng năm link cố định (xưởng âm · xưởng ảnh · xưởng video ·
game · sơ đồ cốt truyện), không phải "trang vừa đổi". Đo lại:
`python3 tools/ban_giao.py --khong-kiem` → phải ra đúng **5 dòng** link.


- [ ] **Chương 2 — gắn lại `bien_the` (đổi giọng kể theo hảo cảm)**
  - Bản tách hai nhánh viết lại phần Thái Nam → cơ chế chỉ còn ở `c2_d06`, `c2_p02`
  - Cần gắn lại vào đoạn mới: `c2_d22`, `c2_d23`, `c2_p19`, `c2_p20` (chỗ tương ứng cảnh cũ)
  - ⚠ Đây là **viết nội dung** → hỏi người dùng trước khi làm
  - Đo được: `python3 -c "import json;d=json.load(open('game/chapters/chuong2.json'));print(sum(1 for x in d['doan'] if x.get('bien_the')))"` → hiện **2**, mục tiêu ≥ 8

- [ ] **Trang báo cáo `docs/nhap/ban-dong-hanh.html` — người dùng tự bổ sung ảnh cảnh**
  - Trang hiện chỉ có chữ (theo yêu cầu). Mục "Ảnh cảnh" để trống chờ
  - Sinh lại trang: `python3 tools/tao_bao_cao_ban_dong_hanh.py`

- [~] **Phần ảnh — Xưởng TỰ ĐỘNG trên GitHub** (thay quy trình cũ)
  - [x] **Xưởng tĩnh trên Pages** ✓ — `docs/xuong/index.html`, bố cục theo từng chương,
        prompt từng ảnh + nút copy + trạng thái ảnh, không cần server
  - [x] **GitHub Action tự xử lý ảnh** ✓ — dán ảnh vào Issue (nhãn `xuong-anh`) hoặc bỏ
        vào `xuong-inbox/` → tự nhận diện → nén → ghép vào đúng đoạn → deploy → báo trong Issue
  - [x] **Bản đồ ảnh → đoạn** ✓ — `DOAN_CUA_ANH` (mỗi ảnh đúng **một** đoạn)
  - [~] **→ Người dùng: cần thêm secret `GEMINI_KEY`** (1 lần) để AI nhận diện ảnh
  - **Tiến độ ảnh cảnh Chương 1: 29/64 đoạn có ảnh** (mỗi đoạn một cảnh riêng)
    - [x] **Nhánh tán tu — 23 đoạn, đủ 23 ảnh** ✓
    - [x] **Nhánh môn phái — 6/41 đoạn có ảnh** (p05 · p07 · p08 · p11 · p16 · p19)
    - [ ] Nhánh môn phái còn **35 cảnh chờ vẽ** — prompt + nút 📁 Up đã sẵn trong Xưởng

---

## ✅ VỪA XONG — Dán ảnh ngay dưới prompt, tự đưa lên GitHub

- [x] **Bỏ nút 📤 Gửi ảnh này** (mở Issue nhiều bước). Thay bằng **ô dán ảnh ngay trong
  thẻ**: dán `Ctrl+V` / kéo thả / **📂 Chọn file** → ảnh **nén trên máy** → tự
  `PUT` lên `xuong-inbox/<mã>/` qua GitHub Contents API. Bot nhận theo **tên thư mục = mã ảnh**
  nên gán thẳng, không đoán sai.
- [x] **🔑 Kết nối GitHub (1 lần)**: dán fine-grained token (quyền **Contents: Read and write**);
  lưu ở `localStorage`, chỉ gửi tới `api.github.com`. Có nút **Quên token** và link tạo token sẵn.
- [x] Bấm vào ô = **chọn ô làm đích cho Ctrl+V** (không mở hộp chọn file → không dán nhầm thẻ).
- [x] Vẫn giữ đường lui: mở Issue trống, và "Up thẳng vào thư mục" (không cần token).
- [x] Kiểm thử: engine 105/105 · API 159/159 · logic `ghPutAnh` tạo mới/ghi đè/xoá đều OK trên repo thật.

## ✅ VỪA XONG — Gửi ảnh qua Issue (cách cũ, vẫn dùng được)

- [x] Mỗi nhóm cảnh (từ 2 ảnh) có nút **📤 Gửi ảnh cho CẢ NHÓM** — Issue điền sẵn danh sách
  mã theo thứ tự; dán ảnh đúng thứ tự là xong.
- [x] `tools/xu_ly_inbox.py`: thêm `ma_anh_trong()` đọc dòng `mã-ảnh:` (chịu được
  "ma-anh", "mã ảnh", "MÃ-ẢNH"); `tai_tu_urls()` gán mã theo thứ tự URL.

## ✅ VỪA XONG — Sửa lỗi copy + tách ảnh hai nhánh (không dùng chung)

- [x] **Sửa lỗi không copy được prompt**: 52 ID trùng — thẻ `<article>/<section>` và ô
  `<textarea>` dùng chung một `id`, nên `getElementById` trả về thẻ (không có `.value`)
  thay vì ô chữ. Tách id ô chữ thành `<id>-t`. Kiểm: 0 ID trùng, 58 nút copy đều trỏ
  đúng ô chữ.
- [x] Hàm `cpText` viết lại: không phụ thuộc `ta.select()`, có đường dự phòng
  (`execCommand`) và báo lỗi rõ nếu không tìm thấy ô chữ.
- [x] **Tách ảnh hai nhánh**: bỏ nhóm "Cảnh dùng chung hai nhánh". Ba ảnh từng chia sẻ
  thực ra là ba cảnh khác nhau → tạo 3 ảnh riêng cho nhánh môn phái:
  `bc_quan_nuoc` (p05), `bc_mon_phai_tan_hoang` (p16), `bc_binh_minh_ngoc_cot` (p19).
- [x] Gỡ `anh` khỏi 3 đoạn môn phái để chờ ảnh riêng (bot tự gán khi bạn gửi lên).
  Thư viện: 3 ảnh cũ giờ chỉ còn dùng ở nhánh tán tu.
- [x] Nhánh môn phái: **3 → 6 ảnh**; tổng Xưởng **36 ảnh cảnh**, 19 nhóm, 3 phần.
- [x] Kiểm thử: engine 105/105 · API 161/161.

## ✅ VỪA XONG — Sắp xếp lại Xưởng: 3 tầng phần · nhóm cảnh · từng ảnh

- [x] **Bố cục 3 tầng** trong `docs/xuong/index.html`:
  - **PHẦN**: 🧰 Dùng chung · 🍂 Chương 1 nhánh Tán tu · ⛩️ Chương 1 nhánh Môn phái
  - **NHÓM CẢNH**: 16 nhóm theo cảnh liên tiếp trong truyện (Chợ sớm, Miếu hoang — Đỗ Tam,
    Kiếm linh, Trấn cháy, Hàn Lập, Tân xá, Ngọc cốt, Tuyết Cơ…)
  - **TỪNG ẢNH**: 33 ảnh cảnh, đánh số C.x / D.x / P.x theo từng phần
- [x] **Prompt 3 mức**: toàn phần (3 nút) · cả nhóm cảnh (16 nút) · từng ảnh (33 nút).
  Prompt cả nhóm và toàn phần tự nhắc **đính kèm ảnh mẫu** để giữ mặt/tóc/áo nhân vật.
- [x] **Mục lục** nhảy nhanh tới từng phần/nhóm; **Hộp nhận ảnh** xếp theo phần.
- [x] Ảnh mẫu tách riêng ở **thư viện** (9 ảnh), không đánh số trùng với ảnh cảnh.
- [x] `ten_sach()` bỏ mã đợt cũ (B.x/C.x/D.x) khỏi tên hiển thị để không trùng số mới.
- [x] Dữ liệu bố cục: `XUONG_PHAN` + `NHOM_CANH` trong `tools_server.py`; dựng bằng
  `python3 tools/build_xuong.py`.
- [x] Kiểm thử: engine 105/105 · API 161/161 · trang dựng 0 placeholder sót.

## ✅ VỪA XONG — Xưởng ảnh tự động trên GitHub

- [x] **Xưởng tĩnh trên Pages** — `docs/xuong/index.html`, bố cục theo từng chương,
      prompt từng ảnh + nút copy + trạng thái ảnh. Không cần server.
- [x] **GitHub Action** `.github/workflows/xuong-anh.yml` — dán ảnh vào Issue (nhãn
      `xuong-anh`) hoặc bỏ vào `xuong-inbox/` → tự nhận diện → nén → ghép vào đúng đoạn →
      cập nhật thư viện → dựng lại Xưởng → commit → deploy Pages → báo lại trong Issue.
- [x] **Bản đồ ảnh → đoạn** `DOAN_CUA_ANH` — ảnh mới (D.x) thay ảnh dùng chung ở đúng đoạn.
- [x] **Nhận diện 3 đường**: thư mục = mã (100%) · tên file chứa mã (100%) · AI vision.
      Không có khoá AI → báo cần xác nhận, không gán bừa.
- [x] Kiểm thử: Engine **105/105** · API **161/161** · nhận diện thật **95%**.
- [ ] **Người dùng cần thêm secret `GEMINI_KEY`** (1 lần) để bật nhận diện AI.

---

## ✅ VỪA XONG — Ghép 3 ảnh nhóm 1 vào game

- [x] Ghép 3 ảnh phong cảnh vào đúng đoạn theo `use` trong Xưởng:
      `bc_cho_02`→`c1_d02` · `bc_cho_03`→`c1_d02b` · `bc_mieu_trong`→`c1_d04b`
- [x] Cập nhật `docs/assets/library/index.json`: thêm 3 mục mới, sửa `dung_o`
      (`bc_cho_01` bỏ `c1_d02`/`c1_d02b`; `bc_mieu_hoang` bỏ `c1_d04b`)
- [x] Sửa ảnh gán sai `c1_p19` (kết chương) → `bc_binh_minh` (thay `vt_ngoc_cot`)
- [x] Đồng bộ `game/chapters/chuong1.json` **và** `docs/game/du-lieu/chuong1.json`
- [x] Engine test **105/105** · API test **161/161**

---

## ✅ VỪA XONG — Nhóm 1 phong cảnh (PR #31)

- [x] Nhận 3 ảnh: `bc_cho_02` · `bc_cho_03` · `bc_mieu_trong` (900×1200, 3:4 ✓)
- [x] AI vision: khớp cảnh 95/100, phong cách 90/100, không chữ
- [x] Lưu cả `assets/` và `docs/assets/`

---

## ✅ VỪA XONG — Thư viện ảnh mẫu (PR #30)

- [x] Mục **📚 Thư viện ảnh mẫu**: lưới 9 ảnh, mỗi ảnh có xem trước + tên + badge + nút tải
- [x] Đường dẫn tuyệt đối `/assets/scene/...` (không hỏng khi URL có `/` cuối)
- [x] Engine test **105/105** · API test **161/161**

---

## ✅ VỪA XONG — Chia nhóm ảnh đợt 1 (PR #29)

- [x] 14 ảnh đợt 1 chia **7 nhóm theo nhân vật**, mỗi nhóm 1 nút Copy + tải .txt
  - Prompt nhóm có khối `ATTACHED REFERENCE IMAGE(S)` nhắc AI giữ mặt/tóc/áo
- [x] Engine test **105/105** · API test **161/161**
- [x] Xưởng: 7 thẻ nhóm hiển thị, 0 placeholder sót, ngữ pháp đúng

---

## ✅ VỪA XONG — Nhận 4 ảnh mẫu tham chiếu

- [x] 4 ảnh mẫu vào `assets/scene/` + `docs/assets/scene/` (commit `0ceacd7`)
  - `nv_chinh_mau` · `nv_mac_dai_phu_mau` · `nv_do_tam_mau` · `nv_hung_ba_mau`
  - Kiểm tra: 900×1200 (3:4 ✓) · AI xác nhận đúng canon + đúng dạng ảnh mẫu (1 nhân vật, nền trống)
- [x] **9 ảnh mẫu sẵn sàng** = 4 mới + 5 cũ (Tuyết Cơ, Hàn Lập, Kiếm linh, Ngọc cốt, Hộp kiếm)
- [x] Phân tích: 14 ảnh đợt 1 chia **6 nhóm theo nhân vật** (để đính kèm đúng ảnh mẫu)

---

## ✅ VỪA XONG — Thêm prompt ảnh vào Xưởng

- [x] Xưởng (`tools_server.py`): thêm **18 asset mới** (4 ảnh mẫu + 14 ảnh đợt 1)
  - Tổng ASSETS: 19 → **37**
  - 2 khối mới **lên đầu trang** + 2 nút copy + 2 nút tải .txt
- [x] Engine test **105/105** · API test **161/161** (test nén ảnh nay cũng đạt)
- [x] Đã khôi phục 2 ảnh thật bị API test ghi đè (`bc_cho_01`, `divider-ink`)

---

## ✅ VỪA XONG — Đẩy văn lên web

- [x] PR **#27** merged (commit `e530a3a`): sửa văn trùng Chương 1 + bảng canon + sổ việc
  - Đã kiểm chứng web thật: `p05c`/`p19` là bản mới, **0 đoạn** còn câu mơ cũ
  - GitHub Pages deploy: **success**
  - URL game: https://huuducbkb.github.io/game-hong-duc-lam/game/play.html

---

## 🟡 CHỜ LÀM — ẢNH (mỗi cảnh 1 ảnh riêng)

- [x] **Bảng canon nhân vật & đồ vật** — `tai-lieu/CANON-NHAN-VAT-DO-VAT.md`
- [~] **Ảnh mẫu tham chiếu** (vẽ 1 lần, dùng lại cho mọi chương sau)
  - [ ] 4 ảnh mẫu cần vẽ: nhân vật chính · Mạc Đại Phu · Đỗ Tam · Hùng Bá
- [ ] **Ảnh cảnh Chương 1 — mỗi đoạn một cảnh riêng**
  - Quy tắc: **mỗi đoạn truyện một ảnh riêng**, hai nhánh không dùng chung ảnh.
    Nhánh tán tu đã đủ (23 đoạn = 23 ảnh). Nhánh môn phái trước đây chỉ 6 ảnh
    gánh 41 đoạn → đã bổ sung **35 cảnh còn thiếu** vào Xưởng (`tools/xuong_monphai.py`).
  - [x] Nhánh tán tu — 23 đoạn, 23 ảnh riêng ✓
  - [x] Nhánh môn phái — 41 đoạn, **41 cảnh riêng** (6 ảnh đã có + 35 prompt mới)
        · 6 đoạn đã gán ảnh (p05 · p07 · p08 · p11 · p16 · p19)
        · 35 cảnh còn lại chờ vẽ (prompt + nút 📁 Up đã sẵn trong Xưởng)
  - Nhóm cảnh môn phái trong Xưởng: mở đầu · sân tập/sân sau · vườn thuốc ·
    quán nước & khe núi · ngọc cốt · Tuyết Cơ · tân xá · tập kích · cổng đông ·
    hỏa trường · sau trận · Hàn Lập · kết chương.
- [ ] Sửa ảnh gán sai: `c1_p19` (kết chương) → `bc_binh_minh` (thay `vt_ngoc_cot`)
      → [x] **ĐÃ SỬA** (xem "VỪA XONG — Ghép 3 ảnh nhóm 1 vào game")

---

## 🟢 ĐÃ XONG

- [x] **Sửa văn trùng Chương 1** — 8 đoạn viết lại (`c1_p03e`, `c1_p05c`, `c1_p06b`,
      `c1_p03d`, `c1_p05b`, `c1_p06`, `c1_p17`, `c1_p19`). Quét trùng: **5 cặp → 0 cặp**.
      Engine test 105/105 · API test 160/161 (1 test nén ảnh hỏng sẵn, không liên quan).
- [x] **Bảng canon nhân vật & đồ vật** — `tai-lieu/CANON-NHAN-VAT-DO-VAT.md`
      (7 nhân vật + 5 đồ vật + bối cảnh + quy tắc bất di bất dịch)
- [x] **Xoá kế hoạch viết lại** (`KE-HOACH-SUA-CHUONG-1.md`) — người dùng chốt
      **giữ hướng hiện tại**, không viết lại. Đã bảo tồn: khung 7 giai đoạn + chi tiết
      3 nhánh chưa xây → chuyển vào `Y-TUONG-3-NHANH-CHUA-XAY.md`
- [x] **Sổ việc** — `tai-lieu/VIEC-CAN-LAM.md` (file này)
- [x] Ghép 8 ảnh nhánh tán tu vào game — PR #24
- [x] Sửa Xưởng cảnh báo ảnh chưa gán prompt — PR #25
- [x] Ghép 4 ảnh tán tu cuối — đủ 12/12 ảnh truyện — PR #26

---

## ⏸️ ĐÃ QUYẾT — không còn là "chưa quyết"

- [x] ~~Kế hoạch viết lại Chương 1~~ → **HUỶ** (người dùng chốt 2026-11-17).
      Hướng hiện tại (2 nhánh: tán tu + môn phái) là **đúng**, tiếp tục phát triển.
- [ ] 3 nhánh dược đồng / gia tộc / hắc đạo — đã gỡ, xây lại sau
      (`tai-lieu/Y-TUONG-3-NHANH-CHUA-XAY.md` — đã bổ sung khung 7 giai đoạn + chi tiết cơ duyên)

---

## 📌 QUYẾT ĐỊNH ĐÃ CHỐT (không hỏi lại)

| Ngày | Quyết định |
|---|---|
| 2026-11-17 | **Mỗi cảnh = 1 ảnh riêng** — không dùng lại ảnh giữa các cảnh |
| 2026-11-17 | Cùng nhân vật nhưng **khác tư thế / biểu cảm** ở mỗi cảnh |
| 2026-11-17 | Nhân vật & đồ vật phải **nhất quán qua các chương** → dùng bảng canon + ảnh mẫu tham chiếu |
| 2026-11-17 | **Sửa văn trước**, ảnh sau |
| 2026-11-17 | Ảnh phải **thay được từng tấm** khi cần (tên file tách rời code) |
| — | Repo `huuducbkb/game-hong-duc-lam` public, deploy GitHub Pages |
| — | Người chơi dùng Safari (iPad/iPhone), **không có terminal** → mọi thao tác qua web |
| — | **Không tự thêm tính năng** — bàn trước khi làm |

---

## 📋 QUY TRÌNH THÊM ẢNH (đã chốt, dùng lại mỗi lần)

1. AI soạn **prompt gộp** (kèm ảnh mẫu tham chiếu nếu có)
2. Người dùng dán vào Gemini → vẽ ra
3. Người dùng tải lên **Xưởng** (`/upload`)
4. AI ghép vào game → đồng bộ `assets/scene/` **và** `docs/assets/scene/`
5. Cập nhật `docs/assets/library/index.json` (ghi `dung_o`)
6. Commit → PR → merge → deploy GitHub Pages → kiểm tra HTTP 200
