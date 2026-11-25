# Nhật ký công việc

File này để **mở khung chat mới vẫn nắm được việc đã làm**. Chat cũ lỗi thì đọc file này
là hiểu ngay: đã làm gì, đang ở đâu, còn gì chưa xong, đo bằng cách nào.

Quy ước ghi: mới nhất ở **trên cùng**. Mỗi mục có **ngày · việc · đã đổi file nào ·
kiểm chứng bằng số đo nào**. Không ghi "đã sửa cho đẹp hơn" — phải ghi đo được cái gì.

Nằm ở `tai-lieu/` (ngoài `docs/`) nên **không bị Pages phục vụ ra web công khai**.

---

## 2026-11-17 · CHỐT CHƯƠNG 1 — bàn giao sang chương 2

Người dùng: "chương 1 đã xong, ghi nhớ những gì đã làm để sang chương 2." Đây là mục
bàn giao. Đọc mục này là đủ để bắt đầu chương 2 mà không cần dựng lại từ chat cũ.

### Chương 1 đã có gì (số đo thật, đếm từ file)

| Hạng mục | Số lượng | Ghi chú |
|---|---|---|
| File truyện | `game/chapters/chuong1.json` | Chỉ có **1 file chương** trong `game/chapters/` |
| Tên chương | Đại chiến Dã Lang Bang | |
| Tổng số đoạn | **66** | Mở 19 · Thân 38 · Kết 9 |
| Nhánh **tán tu** | **24 đoạn**, `c1_d01` → `c1_d17` | Kết riêng `c1_d17` |
| Nhánh **môn phái** | **42 đoạn**, `c1_p01` → `c1_p19` | Kết riêng `c1_p19` |
| Tổng lựa chọn | **95** | Không đoạn nào thiếu lựa chọn (0 đoạn rỗng) |
| Ảnh minh họa | **66 ảnh, mỗi đoạn một ảnh riêng** | Không ảnh nào dùng lại; **0 ảnh thiếu file** |
| Prompt tiếng | **66/66** cảnh có | `game/prompt_am.py` |
| File tiếng thật | **64/66** | Thiếu `kiem_hap_nhan.mp3`, `ngoc_cot.mp3` (2 ảnh vật phẩm) |
| Đoạn có `video` | **0** | Chương 1 không dùng video nào |

Hai nhánh **không hội tụ**: mỗi nhánh có đoạn kết riêng. Ràng buộc cũ "mọi nhánh về
`c1_d18`" đã bỏ, `c1_d18` đã xoá. Đừng dựng lại chỗ hội tụ.

### Mẫu dữ liệu một đoạn (chép đúng khuôn này khi viết chương 2)

```json
{
  "id": "c1_d01",
  "hoi": "Mở",                      // Mở | Thân | Kết
  "boi_canh": "Chợ sớm Thất Huyền trấn",
  "hinh_anh": {"tags": ["chợ", "ăn mày", "sáng"], "anh": "bc_cho_01.jpg"},
  "ke": "Ta mở mắt giữa một góc chợ…",
  "lua_chon": [{"chu": "Lê bước tới ngõ sau chợ", "den": "c1_d02"}]
}
```

Trường tuỳ chọn đã dùng thật trong chương 1 — chỉ **2 lựa chọn** có điều kiện:

```json
{"chu": "Vận Thất Huyền quyền đỡ đòn rồi phản kích", "den": "c1_p14d",
 "dieu_kien": {"co_su_kien": ["hoc_that_huyen_quyen"]},
 "ly_do_khoa": "Chưa học Thất Huyền quyền"}
```

Tức cơ chế điều kiện **có sẵn và đã chạy**, nhưng chương 1 dùng rất tiết kiệm. Chương 2
có thể dùng nhiều hơn cho nhánh Huyết Sát Thí Luyện (ví dụ bắt buộc đã có ngọc cốt /
đã học Thất Huyền quyền mới mở lựa chọn sống sót).

### Quy ước ID — chương 2 phải theo

- Chương 1: nhánh tán tu `c1_dNN`, nhánh môn phái `c1_pNN`.
- Chương 2 đặt **`c2_dNN`** (tán tu) và **`c2_pNN`** (môn phái). Đừng dùng lại tiền tố `c1_`.
- `id` không được trùng trong cùng file — chương 1 có 66 id, 0 trùng.
- Đoạn kết đánh dấu `"ket_thuc": true` (chương 1: `c1_d17`, `c1_p19`).

### Cơ chế chuyển chương — CHƯA CÓ, phải làm

Đây là **việc đầu tiên của chương 2**, chưa ai làm:

- `engine.load_chuong(so)` đọc `game/chapters/chuong{so}.json`.
- `engine._chuyen_doan()`: khi `den` không có trong chương hiện tại → đặt
  `state["ket_thuc"] = True`. Tức chương 1 kết thúc bằng cách **đi tới một đoạn không
  tồn tại**, không phải bằng cách tăng số chương.
- **Không có** hàm nào tăng `state["chuong"]`, không có API "sang chương 2", không có
  nút trên giao diện. Grep `sang chuong` / `next_chapter` / `tiep_chuong` → 0 kết quả.
- `_man_ket_chuong()` đang **viết cứng** chữ "Chương 1 — hết" và câu
  "*Chương sau: Huyết Sát Thí Luyện.*" → khi làm chương 2 phải sửa thành theo
  `state["chuong"]`, nếu không chương 2 vẫn hiện "Chương 1 — hết".
- `khởi tạo state` đặt cứng `"chuong": 1`; `doan_dau_cua(nhom)` lấy `doan_dau` từ
  `game/xuat_than.json` — trường này đang trỏ đoạn `c1_*`, nên chương 2 cần bảng
  đoạn đầu **riêng theo chương**, đừng sửa đè lên `doan_dau` của chương 1.

### Ràng buộc canon chương 2 — Huyết Sát Thí Luyện

Đã chốt trong `SPEC.md`: chương 2 = **Huyết Sát Thí Luyện**, Hàn Lập ở trong môn phái,
người chơi chen vào thí luyện tranh cơ duyên.

**Vẫn ở tầng phàm nhân/giang hồ** (SPEC ghi rõ chương 1–3 là tầng giang hồ). Canon bắt buộc:

- Tiền tệ là **bạc/vàng**, **KHÔNG "linh thạch"**.
- Thất Huyền Môn vẫn là **môn phái võ lâm phàm nhân**, đừng gọi đệ tử là "tu sĩ".
- Tu luyện vẫn **bí mật**: người chơi giấu ngọc cốt, Hàn Lập giấu Trường Xuân Công.
- "Xuyên không" **chỉ trong suy nghĩ nội tâm**, không nói ra với người bản địa.
- Giọng Hệ thống đúng định dạng `👁️‍🗨️ 【Hệ thống】“…”`.
- Văn phong: tránh từ đời thường ("đồ bỏ" → "phàm vật"); **ngoại lệ nhánh tán tu** giữ
  giọng dân dã vì thân phận ăn mày là dụng ý.

### Bài học chương 1 phải mang sang (đã trả giá thật)

1. **Ảnh phải vẽ bằng prompt thủy mặc đã sửa** (commit `14a108a`). Prompt cũ có bốn cụm
   `wet ink bleeding edges` / `dry brush strokes` / `visible paper fiber texture` /
   `rough handmade` → mực loang lỗ, mặt như tranh trừu tượng.

   **Đã đo lại toàn bộ 66 ảnh chương 1 (2026-11-17, `tools/do_net_anh.py`):**

   | Số đo | Kết quả |
   |---|---|
   | Đo được | 66/66 |
   | Trung vị `LOANG` | **0.279** |
   | Thấp nhất / cao nhất | 0.087 / **0.477** |
   | Loang, trên ngưỡng 0.15 | **60 ảnh** |
   | Đạt (≤ 0.15) | **6 ảnh** |

   Ảnh tệ nhất: `nv_han_lap` 0.477 · `bc_vuon_thuoc_im` 0.430 · `nv_han_lap_cuoi_tru` 0.428.
   Tốt nhất: `bc_khe_nui_chon` 0.087 · `nv_tuyet_co_dieu_kien` 0.089.

   Tức **gần như cả chương 1 phải vẽ lại** mới sạch. Chương 2 đừng dùng lại ảnh chương 1
   trừ khi đo từng ảnh và thấy ≤ 0.15.
2. **Mỗi đoạn một ảnh riêng** là chuẩn chương 1 (66 đoạn / 66 ảnh). Chương 2 nên theo,
   nhưng **vẽ một ảnh thử rồi đo** trước khi vẽ cả loạt — đừng vẽ 40 ảnh rồi mới phát
   hiện prompt sai.
3. **Tiếng theo cảnh** dùng tên file đã bỏ tiền tố: `bc_cho_01.jpg` → `cho_01.mp3`.
   Quên bỏ tiền tố là cảnh im hoàn toàn (lỗi đã từng xảy ra).
4. **Trạng thái "đã có tiếng" phải sinh từ dữ liệu**, không viết cứng.
5. **Sửa mã sinh trang thì sửa ở NGUỒN** (`tools/build_*.py`), rồi sinh lại — đừng sửa
   thẳng file HTML đã sinh.
6. **Kiểm hành vi, không chỉ kiểm "có tín hiệu"**: "có tiếng" khác "tiếng đổi đúng";
   "có ảnh" khác "ảnh đúng cảnh".

### Việc còn nợ của chương 1 (nên trả trước khi làm chương 2)

- [x] ~~`AGENTS.md` mục "NÉT VẼ" đã SAI~~ — đã viết lại theo thủy mặc (2026-11-17).
- [ ] **60/66 ảnh chương 1 vẽ bằng prompt cũ** (trung vị loang 0.279) — chưa vẽ lại.
- [ ] **Thiếu tiếng 2 ảnh**: `vt_kiem_hap_nhan.jpg`, `vt_ngoc_cot.jpg`.
- [ ] **Chưa có cơ chế chuyển chương 1 → 2** (xem mục trên).

### File đã đụng trong việc này

`tai-lieu/NHAT-KY.md` (mục này), `AGENTS.md` (sửa mục NÉT VẼ). Không đụng mã game,
không đụng ảnh, không đụng `chuong1.json`.

---


## 2026-11-21 (tiếp) · Hướng 3 — tiếng theo cảnh

Người dùng chọn hướng 3 thay vì nhạc nền. Lý do đúng: nhạc nền vướng **nguồn nhạc** (đang đăng
công khai trên Pages), còn tiếng cảnh sinh bằng sóng âm trong máy nên không có file để truy
nguyên.

**68 cảnh chia chín nhóm** theo nghĩa (đọc tên ảnh, không chia máy móc): chợ (3), trận (3),
núi (3), sân tập (6), vườn thuốc (5), miếu (2), đêm (3), làng (11), tĩnh (còn lại). Ảnh nhân
vật/vật (26) không phải nơi chốn → không cắt nền, chỉ thêm một nốt trầm ngắn.

**Kỹ thuật:** nhiễu nâu lặp vòng (buffer 2 giây, `loop = true`) lọc bandpass, mỗi nhóm một tâm
tần và Q riêng; chỗ nối đầu-cuối trộn 0.2 giây để không "cạch" khi lặp. Thêm lớp "thưa": chuông
chùa, dế, gió qua khe, lá động, tiếng xa — hẹn giờ ngẫu nhiên.

**Ba lỗi tự tìm ra khi đo:**

1. `nhomCanh` không khớp vì `src` là đường dẫn đầy đủ (`../assets/scene/bc_cho_01.jpg`) chứ
   không phải tên file trần → cảnh im hoàn toàn. Đo được `nhom=""`, đỉnh 0. Sửa: lấy
   `split("/").pop()` trước khi so tiền tố.
2. Cắt tiếng nền khi hiện ảnh nhân vật → tiếng tụt về 0 đúng lúc đang đọc. Đang đứng giữa chợ
   mà nhìn cận mặt nhân vật thì tiếng chợ vẫn phải còn. Sửa: giữ nền, chỉ thêm điểm nhấn.
3. Đặt nút lên thanh trên làm thanh cao thêm **52px** ở màn 320px, khung truyện còn 238px. Game
   đọc chữ nên đây là hồi quy thật. Chuyển nút vào bảng Hệ Thống (tab Nhân vật).

**Số đo (analyser song song, WebKit iPhone 13):** nền chín nhóm 0.023–0.043; tiếng bấm 0.333;
bấm 8 lần chồng lên nền 0.349 (không vượt 1.0); tắt phông cảnh → 0; tắt tiếng chính → phông
cảnh im theo; bốn tiếng cũ không đổi.

**Mặc định TẮT.** Người chơi phải tự bật trong bảng Hệ Thống. Lý do: tiếng nền là lựa chọn,
bật sẵn thì ai không thích phải đi tìm nút tắt.

**Giới hạn đã nói rõ với người dùng:** tôi đo được mức tín hiệu nhưng **không nghe được**, nên
không biết nghe có hay không — cái đó phải do người dùng quyết.

**File:** `docs/nhap/tieng-theo-canh.html` (báo cáo), ảnh `canh-1-tat.jpg`, `canh-2-bat.jpg`,
`canh-3-trong-game.jpg`. Test: 124 đạt; API 161 đạt/0 hỏng.

**Ba chỗ tôi nói sai, kiểm lại mới thấy:**

1. **Bản `game/play.html` thiếu dòng gọi `doiCanhTieng(ten)` trong `hienThiAnh`.** Lần đầu tôi
   thử bản đó, thấy tiếng nền chạy nên kết luận đã đúng — nhưng tiếng đang chạy là tiếng của
   cảnh **đầu**, không đổi khi sang cảnh mới. Đo lại bằng cách đếm số nhóm khác nhau qua sáu
   cảnh mới thấy: chỉ 1 nhóm. Đã thêm dòng gọi; giờ cả hai bản đều đổi đúng (4 nhóm qua 6 cảnh).
   **Bài học: "có tiếng" không bằng "tiếng đổi đúng".** Phải kiểm hành vi theo thời gian, không
   chỉ kiểm có tín hiệu.
2. **Test "ảnh lưu ra nhẹ hơn ảnh gốc" hỏng, tôi đổ cho Pillow 13 nén tốt hơn — sai.** Đo trực
   tiếp mới thấy file lưu ra **đúng bằng kích thước PNG gốc**, tức khâu nén thất bại và rơi vào
   nhánh dự phòng, ghi thẳng PNG vào file `.jpg`. Nguyên nhân thật: **tiến trình `game_server.py`
   đang chạy được khởi động từ trước khi cài Pillow**, nên `import PIL` trong tiến trình đó thất
   bại và mọi ảnh lưu ra đều là PNG đội lốt `.jpg`. Khởi động lại server: nén đúng 3.2MB → 665KB,
   đầu file `ffd8ff`. Test xanh 161/161.

   **Bài học: `catch Exception` nuốt lỗi biến lỗi nặng thành lỗi im lặng.** Nhánh dự phòng ghi
   nguyên bản là đúng ý đồ, nhưng không để lại dấu vết nào nên không ai biết nén đã hỏng. Và khi
   chẩn đoán, **phải khởi động lại tiến trình sau khi cài thư viện** — tiến trình cũ giữ
   `sys.modules` cũ.

3. **Tiếng phông cảnh đặt quá nhỏ VÀ sai dải tần — người dùng không nghe được gì.** Tôi đo
   đỉnh tín hiệu 0.023–0.043 và báo "có nền", nhưng đo RMS sau khi lọc như loa điện thoại
   (highpass 700 Hz) ra −39…−50 dBFS: gần như im lặng. Nguyên nhân kép: (a) mức đặt để "có
   số trong máy", không phải để nghe trên loa; (b) nhiễu nâu dồn ~70% năng lượng dưới 300 Hz,
   mà loa điện thoại cắt dưới ~700 Hz — phần lớn tiếng **không ra khỏi loa**. Sửa: nhiễu hồng
   (1/f), tâm dải 800–1500 Hz, highpass 400 Hz, nâng mức ~8 lần. Giờ −31…−37 dBFS, 42–81%
   năng lượng ở 700–2000 Hz. Thêm thanh trượt âm lượng 0–150% vì tôi không nghe được trên
   máy người dùng — phần đó để họ quyết.

   **Bài học: đo đỉnh tín hiệu không nói được gì về việc tai người có nghe thấy hay không.**
   Phải đo RMS và phải đo qua bộ lọc của loa đích.

4. **Bật phông cảnh lên thì cả tiếng bấm lẫn tiếng nền đều câm.** Người dùng báo đúng
   triệu chứng này. Tìm ra **ba** lỗi, cùng một dạng: *thoát sớm rồi không ai gọi lại*.
   - `doiCanhTieng` gọi `resume()` (bất đồng bộ) rồi `return` ngay vì `state !== "running"`.
     `resume()` xong thì không ai dựng lại lớp nền.
   - `thucDayTieng` chỉ dựng lại nền **bên trong** nhánh `state !== "running"`. Nền chết
     trong lúc context vẫn `"running"` thì không có gì chữa — mọi cú chạm sau đều vô ích.
   - `if (nhom === canhLoai) return;` chặn trước khi biết chắc đã phát được, vì `canhLoai`
     được gán **trước** khi kiểm tra context.

   **Bài học quan trọng nhất về cách kiểm:** WebKit headless **không tái hiện** được lỗi
   này — mọi thứ vẫn kêu. Tôi phải chủ động tạo đúng điều kiện (`ctxTieng.suspend()`, hoặc
   `nguon.stop()` để làm chết lớp nền) rồi mới thấy. Và phải chạy **cùng phép thử trên bản
   cũ** để chứng minh phép thử thật sự bắt được lỗi: 0 → 0.107 và 0 → 0.10. Nếu bản cũ
   không hỏng thì phép thử của tôi vô dụng, không phải code đã đúng.

5. **"Tiếng chợ" mà tôi làm ra là tiếng rè dò đài.** Người dùng phản hồi đúng: "nghe giống
   tiếng rè rè dò đài", và hỏi sao không có tiếng người qua lại, tiếng rao bán hàng. Lỗi gốc:
   tôi lấy **nhiễu lọc qua bandpass** rồi đổi tần số theo cảnh, và gọi đó là gió/chợ/chuông.

   **Nhiễu lọc không bao giờ thành tiếng người.** Nhiễu là tín hiệu không cấu trúc; tai nhận
   ra nơi chốn qua **sự kiện rời rạc có cấu trúc**: nhịp âm tiết, đường cao độ của giọng, bước
   chân, kim loại chạm. Đổi tần số lọc chỉ đổi màu "xì xì", không đổi nghĩa.

   Đã làm lại bằng **tổng hợp formant**: sóng răng cưa (dây thanh) qua 3 bandpass ở tần số
   formant nguyên âm, cộng LFO rung giọng, cộng đường bao từng âm tiết. Rao hàng khác nói
   chuyện ở **đường cao độ: lên nửa đầu, xuống nửa sau**. Nhiễu chỉ còn làm nền ở nơi tiếng
   thật cũng là nhiễu, và phải có LFO làm "thở".

   Đo lại bằng hai chỉ số đúng: **số sự kiện/8 giây** (đếm khung RMS vọt lên rồi xuống) và
   **độ nhấp nhô** (độ lệch chuẩn / trung bình). Nhiễu đều → nhấp nhô thấp = rè.

   **Lỗi phụ tìm ra khi đo:** một âm tiết giọng người có 69% năng lượng **dưới 700 Hz** —
   dải loa điện thoại không phát được — nên dù formant đúng, tai vẫn chỉ nghe phần đuôi.
   Sửa: highpass 620 Hz + cho F2/F3 to hơn F1 → 30% lên 56% năng lượng trong dải phát được.
   Chuông chùa tương tự: gốc 196 Hz → 520 Hz, hài 2–3 to hơn hài 1 → 67% xuống 3%.

   **Bài học: đổi tham số của một chất liệu sai không bao giờ ra chất liệu đúng.** Và khi
   người dùng nói "nghe giống X", phải kiểm **cấu trúc thời gian** của tín hiệu, không chỉ
   mức và phổ.

6. **Đừng tin `confirm()` khi test bằng Playwright.** Playwright tự huỷ hộp thoại, nên nút "Chơi
   lại" chưa hề chạy; mức 0.126 tôi đo được là tiếng `mo` của chính cú bấm, không phải lỗi game.
   Phải đăng ký `page.on("dialog", d => d.accept())`.

---

## 2026-11-21 (tiếp) · Phòng đo tiếng — trang đo trên iPhone thật

Người dùng xác nhận hướng 1 (tiếng bấm) đã chạy đúng trên iPhone thật. Hướng 2 (tiếng lật
trang khi truyện sang trang) đã có sẵn từ trước — `hienThi()` gọi `keTieng("lat")`.

Chỗ còn mù: máy giả lập Linux **không mô phỏng** trạng thái `interrupted` của iOS. Nên làm
`docs/phong-do/tieng.html` để người dùng tự đo trên máy thật.

**Trang đo được:** trạng thái `AudioContext` theo thời gian (bắt `statechange`, `visibilitychange`,
`pageshow`, `pagehide`, `freeze`, `resume`); mức đỉnh tín hiệu thật qua analyser móc **song song**
vào loa chung (không cắt đường tiếng); số lần chạm có tiếng; nút thử `suspend` và `close`; xuất
báo cáo dạng văn bản để copy gửi lại.

**Bài đo bắt được lỗi trong chính thiết kế:** lúc vừa mở trang, WebKit báo `interrupted` —
nhưng đó chỉ là "chưa có cú chạm nào", **không** phải bị ngắt phiên âm thanh. Bản đầu của trang
ghi "CÓ XẢY RA interrupted" trong báo cáo, tức là báo động sai và làm người đọc đi sai hướng.
Đã sửa: thêm cờ `daTungChay`, phân biệt `interrupted` **trước** khi mở khóa với `interrupted`
**thật giữa chừng**; báo cáo chỉ báo động khi là loại thứ hai.

**Số đo trên máy giả lập (WebKit, iPhone 13):** bốn tiếng đều kêu (bam 0.322, lat 0.178,
lui 0.280, mo 0.254); 10/10 lần chạm có tiếng; sau `suspend` tự hồi phục (0.171); sau `close`
tự dựng lại (0.148); cú chạm đầu sau khi tải lại trang vẫn kêu (0.235).

**File mới:** `docs/phong-do/tieng.html` (trang đo), `docs/nhap/phong-do-tieng.html` (hướng dẫn
kèm 3 ảnh chụp), ảnh `docs/nhap/pd-1-mo-trang.jpg`, `pd-3-muoi-lan.jpg`, `pd-4-bao-cao.jpg`.
Test: **161 đạt**, **124 đạt**.

---

## 2026-11-21 (tiếp) · Sửa "bấm lần đầu kêu, lần sau không"

**Người dùng báo:** "khó hiểu lần đầu bấm kêu lần sau không kêu nữa?"

Đo được **ba lỗi thật** trong phần tiếng, cộng một lỗi chặn bấm:

**1. Tải lại trang khi đang chơi dở → cả phiên im.** Đường vào này đi qua
`docPhien()` → `vaoThangNhanh()`, **không** đi qua nút "Vào game" nên chưa có cú chạm nào
mở khóa tiếng. Đo: sau khi tải lại, `ctxTieng.state = "suspended"`, bấm → tín hiệu **0**.
Đây chính là hiện tượng người dùng gặp: lần đầu vào qua nút thì kêu, lần sau tải lại thì không.

**2. `keTieng` bỏ tiếng khi context đang ngủ.** Trước đó tôi cho `keTieng` `return` luôn khi
`state !== "running"`, nên cú chạm đầu tiên sau khi mở lại trang **mất tiếng** dù `resume()`
vẫn chạy. Đo được: lần bấm 1 có `bam` bị bỏ (`state=suspended`), tới tiếng `lat` 320ms sau mới
kêu. Sửa: `resume().then(() => keTieng(loai))` — đánh thức rồi phát, không bỏ.

**3. Chỉ `resume()` khi `"suspended"`.** iOS còn hai trạng thái nữa: `"interrupted"` (cuộc gọi
tới, video/ứng dụng khác chiếm phiên âm thanh) và `"closed"` (bị thu hồi khi chạy nền lâu).
Đo: đóng hẳn context rồi bấm → trước khi sửa **im vĩnh viễn**; sau khi sửa **tự dựng lại và kêu
0.337**. Nay `moKhoaTieng`/`keTieng` dựng lại context nếu `"closed"` và `resume()` cho mọi
trạng thái khác `"running"`.

**4. Cờ `dangCho` có thể kẹt `true`.** `chon`, `tuDo`, `lui` đặt `dangCho = true` rồi nhả ở
cuối hàm; nếu `hienThi` ném lỗi thì cờ kẹt và **mọi lần bấm sau bị chặn ngay từ đầu** — không
kêu, không chuyển trang. Đã bọc `try/finally` cả ba hàm.

**Thêm:** `thucDayTieng()` gắn vào `touchstart`/`click`/`visibilitychange` để đánh thức tiếng
ở mọi cú chạm; gọi lại 60ms sau khi phim intro nhả phiên âm thanh; và ở đường khôi phục phiên
thì đánh thức ngay ở cú chạm đầu.

**Kiểm chứng (đo tín hiệu thật qua analyser móc song song vào loa chung):**

| Trường hợp | Trước | Sau |
| --- | --- | --- |
| 12 lần bấm liên tiếp | — | **12/12 kêu**, đỉnh 0.337 |
| Đóng hẳn AudioContext rồi bấm | im vĩnh viễn | **tự dựng lại, kêu 0.337** |
| Tải lại trang khi đang chơi dở | **0 (im)** | **0.227 kêu** |
| Tắt tiếng | — | **0, im đúng** |
| Bật lại | — | **0.337 kêu lại** |

Test `_test_api.py` **161 đạt**, `_test_engine.js` **124 đạt**, hai bản khớp khối âm thanh
từng ký tự, không lỗi JS.

**File đã sửa:** `docs/game/play.html`, `game/play.html`.

**Biết trước:** máy giả lập Linux không mô phỏng `"interrupted"` của iOS. Đã xử lý theo tài
liệu WebKit và đo được phần `"closed"`/`"suspended"`; phần `"interrupted"` chưa đo trực tiếp
được, nên nếu trên máy thật vẫn còn im thì cần biết lúc đó làm gì (nghe nhạc, có cuộc gọi...).

---

## 2026-11-21 (tiếp) · Bỏ nút loa trên phim + sửa gốc lỗi nút "Bắt đầu"

**Người dùng báo:** "trong video intro cái icon cái loa che mất chữ trong video nên bạn chỉ
bỏ cái icon trong video intro là được còn những chổ khác cứ giữ" và "lỗi này là lỗi cũ bị lại
ở trong giao diện xuất thân khi tôi chọn xuất thân xong bấm nút bắt đầu thì nó không bấm được".

**1. Bỏ nút loa trên phim mở đầu.** Xoá hẳn markup `#phimTieng`, CSS `.phim-intro .tieng-noi`,
và hai chỗ đăng ký trong `capNhatNutTieng()` / `ganNutTieng()`. Hai nút còn lại giữ nguyên
(thanh trên, trong thẻ tạo nhân vật). Đo lại: `#phimIntro` chỉ còn **một** nút là `phimThoi`.

**2. Nút "Bắt đầu" — tìm ra nguyên nhân GỐC, lần sửa trước chưa đúng gốc.**

Nguyên nhân thật: khung `.setup` dùng `position:fixed; inset:0`. Trên iPhone, khung `fixed`
được tính theo **chiều cao màn hình đầy đủ** (kể cả phần thanh công cụ Safari che), không
phải phần đang nhìn thấy. Thẻ `.card` lại dùng `max-height:92vh` — cũng tính theo màn đầy đủ.
Nên thẻ cao hơn vùng nhìn thấy và nút ở đáy bị đẩy ra ngoài.

Số đo tái hiện (ép khung cao 776 như iPhone 13 thật, vùng nhìn thấy 664):
thẻ cao **776**, nút ở `top=651..701`, bị cắt **37 điểm** dưới đáy; đo 13 điểm dọc nút chỉ
**2/13** bấm được. Trên iPhone SE (nhìn thấy 500): nút ra **hoàn toàn ngoài màn**, **0/13** điểm.

**Vì sao lần trước không bắt được:** máy giả lập trên Linux không có thanh công cụ Safari,
nên `vh` = `svh` = chiều cao viewport, lỗi không xuất hiện. Lần này phải **ép** khung cao hơn
vùng nhìn thấy mới tái hiện được.

**Cách sửa:**
- `.setup`: `height:100vh; height:100svh` (bỏ `inset:0`, dùng `left/right/top:0` + height).
- `.setup .card`: `max-height:calc(100vh - 40px); max-height:calc(100svh - 40px)`.
- `svh` = chiều cao vùng nhìn thấy **khi thanh công cụ đang hiện** (trường hợp nhỏ nhất) nên
  luôn vừa, và không giật khi thanh công cụ ẩn/hiện. Máy cũ không hiểu `svh` thì lùi về `vh`.

**Kiểm chứng (bấm thật rồi kiểm có vào game, cả 6 trường hợp đều ĐẠT):**

| Trường hợp | Nút trong màn | Điểm bấm được | Vào game |
| --- | --- | --- | --- |
| iPhone 13 (664) | có | 13/13 | được |
| iPhone SE (500) | có | 13/13 | được |
| iPhone 13 xoay ngang (430) | có | 13/13 | được |
| Màn ngang 390 | có | 13/13 | được |
| iPhone 15 Pro Max (700) | có | 13/13 | được |
| Màn rất thấp (600) | có | 13/13 | được |

Không hỏng gì khác: bốn tiếng vẫn kêu **0.149 / 0.076 / 0.122 / 0.113**; tắt tiếng vẫn nhớ;
chơi 2 lượt không lỗi JS; test `_test_api.py` **161 đạt** và `_test_engine.js` **124 đạt**;
hai bản khớp nhau (`phimTieng` = 0 ở cả hai, `100svh` và `setupTieng`/`nutTieng` khớp).

**File đã sửa:** `game/play.html`, `docs/game/play.html`, `docs/nhap/sua-loi.html`,
`docs/nhap/sua-1-phim.jpg`, `docs/nhap/sua-2-nut-bat-dau.jpg`, `docs/nhap/index.html`.

---

## 2026-11-21 (tiếp) · Tầng 1 âm thanh: bốn tiếng, có nút tắt

**Người dùng yêu cầu:** "làm tầng 1 theo đề xuất của bạn" — tức tầng đơn giản nhất trong
ba tầng đã đề xuất: chỉ thêm tiếng cho thao tác, chưa làm nhạc nền.

**Đã làm:** game từ chỗ **im ru hoàn toàn** giờ có bốn tiếng ngắn, dựng **ngay trong máy**
bằng Web Audio, **không thêm file âm thanh nào** (repo vốn không có file âm thanh nào; thêm
file là nặng thêm và vướng bản quyền).

| Tiếng | Kêu khi |
| --- | --- |
| `bam` | Bấm một dòng hành động |
| `lat` | Truyện sang trang mới |
| `lui` | Lùi hành động |
| `mo` | Mở Hệ Thống, Bắt đầu, Chơi lại, đổi tab |

**Nút tắt tiếng ở ba chỗ** (vì ba chỗ đó người chơi ở lâu): trên thanh trên, nổi trên phim
mở đầu, và trong thẻ tạo nhân vật. Trạng thái nhớ trong `localStorage` khoá `hdttl_tieng`.
Phim mở đầu cũng theo trạng thái này (`v.muted = !tiengBat`).

**Đã đổi file:** `game/play.html`, `docs/game/play.html` (thêm khối `napTieng` /
`keTieng` / `batTatTieng` / `moKhoaTieng` ngay sau `const $ =`), `docs/nhap/am-thanh.html`,
`docs/nhap/tieng-1..4.jpg`, `docs/nhap/index.html`.

**Bốn lỗi tìm ra khi đo, đã sửa (đều là lỗi thật):**

1. **Tín hiệu bị nhân đôi.** Dao động nối vào cả bộ lọc lẫn bộ điều âm lượng, nên đi hai
   đường: đỉnh đo được **1.45** (mức tối đa là 1.0) và một đường không có bao âm lượng →
   nghe "bụp". Đã nối lại một đường duy nhất.
2. **Tiếng lật giấy to gấp bảy lần.** Phần nhiễu nối tắt vào bộ lọc, **vòng qua** bộ điều âm
   lượng: đỉnh **0.544** trong khi đặt `vol: 0.075`. Đã cho nhiễu đi qua bộ điều âm lượng →
   còn **0.078**.
3. **Bấm nhanh thì rè.** 10 lần sát nhau → đỉnh **1.485**, 52 mẫu vượt 1.0. Đã thêm
   `DynamicsCompressor` trước loa: 20 lần sát nhau vẫn chỉ **0.732**, 0 mẫu vượt.
4. **Nút loa bị che ở hai màn.** Ở phim mở đầu và màn tạo nhân vật, thanh trên bị lớp phủ
   che nên **không nút nào bấm được** — đo `elementFromPoint` cho cả `openSys`, `nutKeAI`,
   `openReset` đều trả về phần tử khác. **Lỗi này có sẵn từ trước, không phải do lần này.**
   Đã đặt nút loa nổi trên hai màn đó.

**Kiểm chứng (số đo thật):**

- Render lại từng tiếng bằng `OfflineAudioContext` để có số chính xác (đo qua
  `requestAnimationFrame` chỉ được 5–6 mẫu, không đủ tin): đỉnh lần lượt
  **0.149 / 0.078 / 0.122 / 0.111**, mẫu đầu và mẫu cuối đều **0**, **0** chỗ nhảy đột ngột
  (không "bụp").
- Bấm nhiều lần sát nhau: 1 lần **0.073**, 5 lần **0.326**, 10 lần **0.588**, 20 lần
  **0.732** — không lần nào vượt 0.99.
- Có tiếng thật khi bấm hành động: đo tín hiệu ra **1.1** trước khi sửa, sau khi sửa nằm
  trong ngưỡng; tắt tiếng rồi bấm lại → **0 mẫu tín hiệu** (im hẳn).
- `AudioContext` sau cú chạm đầu: `state = "running"`. Sau 4 lượt chơi + mở Hệ Thống +
  đổi tab + lùi: vẫn `running`, **không lỗi JS** nào.
- Bố cục thanh trên: iPhone SE (320) / iPhone 13 (390) / iPad Pro 11 (834) — nút loa
  **44×44**, **không** nút nào chồng nút, **không** tràn ngang.
- Nhớ lựa chọn: tắt → tải lại → vẫn tắt; bật → tải lại → vẫn bật.
- Đo chồng chữ bằng `Range.getClientRects()` (hộp chữ thật, không phải hộp phần tử):
  iPhone SE ban đầu nút đè chữ "Lộ" cuối tiêu đề → đã đệm phải tiêu đề `46px`, đo lại
  **0 chỗ chồng** ở cả 3 máy.
- Test cũ: `game/_test_api.py` **161 đạt, 0 hỏng**; `game/_test_engine.js` **124 đạt, 0 hỏng**.
- Hai bản khớp nhau: khối module âm thanh **giống hệt từng ký tự**, số điểm gọi
  `keTieng` khớp (bam 4, lat 1, lui 1, mo 3), ba nút tiếng có đủ ở cả hai bản.

**Biết trước, chưa xử lý được:**

- WebKit giả lập trên Linux **không** mô phỏng luật chặn tự phát tiếng của iPhone. Nên
  không kết luận được gì về tự phát từ bài test này; đã thiết kế theo hướng chắc chắn:
  **chỉ mở khóa ở cú chạm đầu tiên**, không dựa vào tự phát.
- Nút loa dùng emoji 🔊/🔇. Trên iOS hiện đúng, nhưng nếu sau này muốn đồng bộ với nét
  vẽ của game thì nên thay bằng hình vector.

---

## 2026-11-21 (tiếp) · Dòng hành động sáng đỏ khi bấm

**Người dùng yêu cầu:** "khi bấm vô lựa chọn hành động nào thì dòng chữ hành động đó
sáng đỏ lên để người chơi biết là bấm vào đó".

**Làm:** thêm class `.choice.dang-chon` (đỏ `--seal-dam` + quầng sáng đỏ), hàm
`danhDauChon()` / `boDanhDauChon()`, gắn vào `onclick` của từng dòng. Chỉ dòng vừa bấm
đổi màu; số 壹 貳 ở đầu dòng cũng đổi theo.

**Vấp lần 1 — đổi màu mà không thấy gì:** game trả lời dưới 0.1 giây nên danh sách
hành động được dựng lại trước khi mắt kịp thấy đỏ. Đo được **0 dòng đỏ**. Sửa: giữ đỏ
tối thiểu `SANG_DO_MS = 320` rồi mới gọi `hienThi`. Đo lại: **1 dòng đỏ**, đúng dòng
bấm, sau đó tự tắt. Tổng thời gian bấm → truyện mới: **328 ms** (thêm 320 ms, vẫn
dưới 0.4 giây nên không thấy chậm).

**Vấp lần 2 — màu đỏ không đọc được:** đỏ son gốc `#a8352a` chỉ đạt **2.28:1** trên
nền thật. Lần đầu tôi chọn `#8a2a1e` tính trên giấy ra 5.05:1, nhưng **đo trên ảnh
chụp thật** chỉ còn **3.01:1** — vì nền thật sau chữ tối hơn: **(165,151,124)**, không
phải (213,196,167) như tôi lấy ở mép ảnh. Đổi sang `#5e150f`: đo trên ảnh thật
**4.62:1**, đạt ngưỡng 4.5:1.
- Vẫn ra đỏ chứ không thành nâu đen: điểm ảnh ngả đỏ trong vùng chữ **5.9% → 47.7%**.
- Chữ vẫn sắc nét: p90 **7 → 6**.

**Chống kẹt màu:** lỗi mạng → `boDanhDauChon()` ngay trong nhánh `kq.loi` (đã giả lập
lỗi, đo được 0 dòng đỏ, có hiện thông báo lỗi). Đang tải mà bấm tiếp → `if (dangCho) return`
trước khi đánh dấu.

**Kiểm chứng:** bấm dòng thứ 2 trong 2 dòng → chỉ dòng thứ 2 đỏ, dòng đầu vẫn mực đen.
Test engine **124 đạt / 0 hỏng**, API **161 / 0**. Hai bản `game/play.html` và
`docs/game/play.html` khớp nhau, cú pháp JS qua `node --check`.

**Báo cáo:** `docs/nhap/do-hanh-dong.html` (ảnh `do-1.jpg`).

## 2026-11-21 (tiếp) · Sửa nút "Bắt đầu" bị đẩy ra ngoài màn hình

**Người dùng báo:** "sau khi sửa thì lỗi hiện tại tôi không thể bấm bắt đầu sau khi
chọn xuất thân? tôi không thể vô game được".

**Nguyên nhân:** nút **không hỏng**, nó bị **đẩy ra ngoài màn hình**. Chọn xuất thân
làm hiện khối trích đoạn mở đầu (`.xt-trich`, cao 58px) ngay dưới hai thẻ, đẩy nút
xuống. Đo trên iPhone 13: trước khi chọn nút ở **y=593** (thấy được), sau khi chọn
nút ở **y=795** nhưng màn hình chỉ cao **664** → nút ngoài màn hình **131px**.
Bấm vào chỗ đó là bấm khoảng trống.

**Lỗi này KHÔNG do lần sửa nền vuông trước đó.** Đã lấy `git show 790d99c:docs/game/play.html`
chạy lại: cũng y=795, cũng ngoài màn hình. Nó có từ commit `74d1e16` (hiện trích đoạn
mở đầu khi chọn xuất thân).

**Cách sửa:** tách thẻ làm hai phần — `.card-than` cuộn riêng (`overflow-y:auto`),
nút `.go` là con trực tiếp của `.card` (flex, `flex:0 0 auto`) nên đứng yên ở đáy,
không bị đẩy. Thẻ `max-height:92vh;overflow:hidden`.

**Thử lần đầu thất bại (ghi lại để khỏi lặp):** dùng `position:sticky` cho nút thì
nút hiện ra nhưng **đè lên nội dung** (`.xt-trich` và `.xt-tu-do` bị che). Đã bỏ,
chuyển sang tách thân thẻ cuộn. Đo lại: phần tử ngay trên nút là `card`, không còn
là nội dung bị che; cuộn được tới cuối thẻ.

**Kiểm chứng (bấm thật rồi xem có vào game):**
- iPhone 13: nút y=568 trong màn hình, bấm OK, vào game, truyện 1512 ký tự, 1 lựa chọn.
- iPhone SE: y=476, OK, vào game.
- iPad Pro 11: y=948, OK, vào game.
- Xoay ngang iPhone 13 và iPad (màn cao 390px): y=305, OK, vào game.
- Mở ô "tự gõ xuất thân" (thẻ dài nhất): OK, vào game.
- Không lỗi JS ở cả 5 trường hợp. Test engine **124 đạt / 0 hỏng**, API **161 / 0**.

**File đã sửa:** `game/play.html`, `docs/game/play.html` (cả hai khớp nhau).
**Báo cáo:** `docs/nhap/nut-bat-dau.html` (ảnh `nut-1.jpg`).

## 2026-11-21 (tiếp) · Bỏ hộp giấy ở dòng hành động

**Người dùng báo:** "chổ chọn hành động mỗi dòng hành động nó có 1 cái nền vuông…
làm cái nền đó trong suốt và thu nhỏ nó lại, tốt hơn là xoá được thì xoá luôn,
nhìn nó mất thẩm mỹ".

**Nó là gì:** không phải viền CSS thường mà là **ảnh giấy** `btn-choice.jpg` cắt 9 mảnh
rồi lót bằng `border-image: … 67 42 73 41 fill / 11px 11px`. Chữ `fill` làm ảnh lót
**cả ruột** nút, nên thành một ô giấy đặc chứ không chỉ là đường kẻ.

**Sửa:** bỏ hẳn `border-image`, bỏ viền 10px, đệm `12px 16px` → `9px 6px`, thêm
`text-shadow` mờ để chữ tách khỏi vân giấy. Sửa **cả hai** bản `game/play.html`
và `docs/game/play.html` (Pages chạy bản trong `docs/`).

**Đo trước/sau (WebKit, iPhone 13, màn 2 dòng hành động):**
- Đường kẻ ngang chạy >60% chiều rộng: **11 → 0**.
- Chiều cao mỗi dòng: **62px → 44px** (gọn 29%); viền **10px → 0**; ảnh nền trong nút: có → không.
- Vẫn giữ **44px** chiều cao chạm (ngưỡng tối thiểu cho ngón tay).

**Chữ có bị nhạt đi không:** đo độ đậm nét chữ so với nền ngay cạnh —
p90 **100 → 102** (thang 0–255), tức **không nhạt**. Tương phản tổng **12,3:1**,
vượt mức cao nhất WCAG (7:1).

**Không vỡ chỗ khác:** iPhone 13 và iPad Pro 11 đều không tràn ngang, không lỗi JS;
nút "Lùi hành động" (36px) vẫn còn và không bị đè. Test engine **124 đạt / 0 hỏng**,
API **161 đạt / 0 hỏng**.

**Không xoá ảnh:** `btn-choice.jpg` vẫn để trong kho, vẫn dùng ở `demo/hybrid*.html`.

**File đã sửa:** `game/play.html`, `docs/game/play.html`.

**Báo cáo:** `docs/nhap/hop.html` (ảnh so sánh `hop-1.jpg`).

## 2026-11-21 (tiếp) · Tách nền ấn son `seal.png`

**Vì sao làm:** cùng loại lỗi với `avatar-ring.png` — ấn son cũng là PNG "có alpha"
nhưng **đục 100%**, nên nó hiện thành **khối giấy kem vuông 22×22px** đè lên thẻ
nhân vật. Người dùng đồng ý sửa luôn.

**Đo bản cũ:** 0% pixel trong suốt trên 300×300; 4 góc đều là giấy kem
(~232,216,184) chứ không trong suốt. Nền giấy có **độ đỏ** `r - max(g,b)` ≈ 14–18,
mực son đỏ ≈ 65–149 — hai nhóm tách rời hẳn nên tách theo độ đỏ chính xác hơn
tách theo độ sáng (cách cũ bị vân giấy lọt lại 30% nền).

**Cách sửa:** `alpha = (do_do - 25) / (70 - 25)`, kẹp 0..255. Cắt sát viền theo
alpha (khung thật 1,38 → 298,262), được **297×224**.

**Đo bản mới:** **86,5% trong suốt**, 11,6% đặc; 4 góc alpha = 0; màu mực đặc
trung bình (195, 87, 62) — đúng đỏ son.

**Kiểm chứng không làm hỏng hình:** đặt bản tách lên nền giấy kem rồi so với ảnh gốc
cùng khung — lệch trung bình **13,6/255 mỗi kênh**, chỉ **0,04%** pixel lệch > 40.
Tức là tách nền gần như không đổi hình.

**Kiểm chứng trong game thật** (WebKit, iPhone 13): `.seal-mini` hiện 22×22, ảnh tải
được, không lỗi JS. So ảnh chụp trước/sau: **91,9%** pixel đổi — trước là khối giấy
đặc, sau chỉ còn nét son, thấy được nền thẻ phía sau.

**Test:** engine 124 đạt / 0 hỏng · API 161 đạt / 0 hỏng.

**File đã sửa:** `assets/ui/seal.png`, `docs/assets/ui/seal.png`.

**Báo cáo:** `docs/nhap/seal.html` (ảnh so sánh `seal-1.jpg`).

## 2026-11-21 · Sửa lỗi không up được ảnh đại diện

**Người dùng báo:** "chổ avatar người chơi tôi up 1 tấm ảnh vô không đc".

**Tái hiện được (WebKit = Safari, khổ iPhone 13 / iPad Pro, cả bản live):** đúng là hỏng,
và hỏng vì **ba** nguyên nhân khác nhau, không phải một.

**Nguyên nhân 1 — ảnh vòng trang trí đục che kín avatar (nặng nhất).**
`assets/ui/avatar-ring.png` là PNG có kênh alpha nhưng **alpha = 255 ở mọi pixel**
(đo: 0% pixel trong suốt trên 512×512). Ảnh này đè lên avatar qua `.ring`/`.rg`
(`position:absolute;inset:-8px`), nên dù ảnh có up thành công thì người dùng
**vẫn chỉ thấy tờ giấy kem** — tưởng là up không được.
Sửa: tách nền theo độ sáng thật của ảnh (giấy kem ~232 → alpha 0, mực ~22 → alpha 255),
cả hai bản `assets/ui/` và `docs/assets/ui/`. Đo lại: **85,6% trong suốt**, alpha giữa = 0,
alpha ở vòng mực (bán kính 176/512) = 189.

**Nguyên nhân 2 — avatar trong tab Nhân vật không bấm được.**
`.char-avatar` chỉ có 2 thẻ `<img>`, **không** có `label`/`input`/`onclick` (đo:
`coLabelBenTrong: false`, `coNutBam: "KHONG co onclick"`, `cursor: auto`).
Chạm vào → không phản ứng gì. Trước đây chỉ up được qua avatar nhỏ trên thanh trên
hoặc nút trong hộp Cài đặt, chỗ dễ tìm nhất thì lại chết.
Sửa: thêm `<label>` bọc `<input type="file" id="avatarInput3">`, thêm CSS
`.char-avatar label{position:absolute;inset:0;...}` và `pointer-events:none` cho `.rg`
(để vòng không chặn cú chạm). Đo lại: chạm vào avatar tab Nhân vật → **mở được** hộp chọn ảnh.

**Nguyên nhân 3 — lưu thất bại thì im lặng.**
`luuAvatar()` bọc `try{}catch(e){}` rỗng. Khi localStorage đầy (`QuotaExceededError`),
ảnh hiện trong phiên nhưng **mất khi tải lại**, người dùng không biết vì sao.
Sửa: `luuAvatar()` trả `true/false`, hiện dòng chữ đỏ ở `#loiAvatar`; thêm vòng lặp
hạ chất lượng JPEG (0,82 → 0,4) khi ảnh > 400KB để giảm khả năng chạm trần.
Đo: làm đầy localStorage rồi up ảnh nhiễu → ô lỗi hiện `display:block` kèm câu giải thích.

**Kiểm chứng (WebKit, giả lập iPhone 13 `390×664` + iPad Pro 11, cảm ứng thật):**
- Trước khi sửa: chạm avatar tab Nhân vật → **không mở** hộp chọn ảnh.
- Sau khi sửa: chạm → mở; chọn ảnh → `#charAv` và `#avatarImg` cùng đổi sang
  `data:image/jpeg`, ảnh 256×192, lưu localStorage 1KB.
- Ảnh chụp `.char-head` trước/sau khác nhau thật (`ImageChops.difference` bbox
  `(2,3,152,153)`, trước đó là `None` — tức trước khi sửa ảnh **không hề đổi**).
- Đo màu trong ảnh chụp: tâm avatar = màu ảnh gốc 100%, mực đen chỉ ở bán kính ≥ 28px
  (mép ngoài) → vòng ôm quanh chứ không che.
- Nút "Xoá ảnh" vẫn đúng: cả hai chỗ về lại ảnh mặc định, xoá khỏi localStorage.
- Test: engine **124 đạt / 0 hỏng**, API **161 đạt / 0 hỏng**.

**File đã đổi:** `assets/ui/avatar-ring.png`, `docs/assets/ui/avatar-ring.png`,
`docs/game/play.html`, `game/play.html`.

**Lưu ý cho sau:** `game/play.html` (bản chạy bằng `game_server.py`) là bản **cũ hơn**
`docs/game/play.html` — nó **không có** hộp Cài đặt key AI, nên ô `#loiAvatar` phải đặt
ở chỗ khác (dưới `.char-head`). Đừng giả định hai file giống nhau.

**Còn để ngỏ:** `assets/ui/seal.png` cũng đục 100%, nhưng nó hiện thành khối vuông
có nền giấy nên không che gì — chưa sửa, chỉ ghi lại.

**Người dùng xác nhận (2026-11-21):** "đã ok rồi" — thử trên máy thật, up ảnh được.
Việc này **đóng**, không cần mở lại.

## 2026-11-20 (tiếp) · Mỗi xuất thân có chỉ số khởi đầu riêng

**Người dùng yêu cầu:** sau khi xem hướng C, thấy ghi chú "hai xuất thân vẫn cho chỉ số
y hệt nhau" → nói **"có hãy làm đi"**, tức là cho phép sửa dữ liệu + engine để mỗi xuất
thân có chỉ số riêng thật.

**Đã làm:**

- `xuat_than.json` (cả `docs/game/du-lieu/` và `game/`): thêm khối **`chi_so_dau`** cho
  từng nhóm, gồm `ly_do` (giải thích vì sao số như vậy, **dẫn nguyên văn truyện**),
  `bac`, `tu_vi`, `chi_so`, `ky_nang`. Nhóm ẩn `tuyet_co` **không** khai → rơi về mặc định.
- `game/engine.py` + `docs/game/engine.js`: thêm `chi_so_dau_cua(nhom)` +
  `CHI_SO_DAU_MAC_DINH`; `trang_thai_moi()` đọc từ đó thay vì số viết cứng.
- `game_server.py`: `/api/xuat_than` trả thêm `chi_so_dau` để giao diện bản `game/` hiện số.
- Hai `play.html`: thêm `daiChiSo()` vẽ dải số trên thẻ; thẻ tăng **126px → 148px**
  (126px cũ làm dải số bị cắt 13px — đo mới thấy).

**Số đã chốt và lý do (dựa trên nguyên văn, không tuỳ tiện):**

| | Tán tu / ăn mày | Đệ tử môn phái |
|---|---|---|
| Sinh lực | 26 | 34 |
| Tu vi khởi đầu | 12 | 10 |
| Tấn công | 3 | 7 |
| Phòng thủ | 2 | 4 |
| Tốc độ | 9 | 11 |
| Bạc | 3 | 1 |
| Kỹ năng | Hô hấp pháp, Nhận biết linh khí | Thất Huyền quyền nhập môn, Hô hấp pháp |

- Tán tu: `c1_d01` "vài đồng bạc lẻ trong túi rách" → **3 bạc**; `c1_d02` "không võ công"
  → công/thủ thấp.
- Môn phái: `c1_p01` "thân thủ hạng bét, chỉ hơn kẻ mới học võ chút đỉnh" → **có** võ công
  nên công 7 > 3; ở trong môn không cần tiền mặt → **1 bạc**.

**Ràng buộc quan trọng đã kiểm tra: cảnh giới cuối chương phải khớp nguyên văn.**
Đây là chỗ dễ hỏng nhất, vì tu vi khởi đầu đổi là mốc lên tầng lệch theo.

- `c1_d17` (tán tu) nói *"ngươi đã lên Luyện Khí tầng ba"* → phải kết ở **tầng 3**.
- `c1_p12` (môn phái) nói *"Luyện Khí tầng hai"*, `c1_p19` nói *"đã lên Luyện Khí tầng hai"*
  → phải lên tầng 2 ở `p12` và **giữ** tầng 2 tới hết chương.

Lần đầu tôi đặt môn phái tu vi 8 → mô phỏng cho ra **tầng 1**, sai nguyên văn. Dò lại
thấy **10** mới đúng (mô phỏng: `p12`=tầng 2, `p19`=tầng 2). Đã khoá bằng test.

**Kiểm chứng (số đo):**

- `game/_test_engine.js`: **124 đạt, 0 hỏng** (thêm 19 test: số từng nhóm, khác biệt giữa
  hai nhóm, và 5 test khoá cảnh giới cuối chương khớp nguyên văn).
- `game/_test_api.py`: **161 đạt, 0 hỏng**.
- Trình duyệt thật (390×844, server 12001): thẻ hiện đúng
  `Sinh lực 26 · Tu vi 12 · Công 3 · Thủ 2 · Tốc độ 9 · Bạc 3` (tán tu) và
  `34 · 10 · 7 · 4 · 11 · 1` (môn phái). Vào game chọn môn phái, bảng Hệ Thống hiện
  `Tu vi 10/100, Sinh lực 34/34, Công 7, Thủ 4, Tốc độ 11, Bạc 1 lượng` → khớp thẻ.
- Đo tràn thẻ: trước khi tăng chiều cao, `.xt-so` thò ra ngoài đáy thẻ **13px**; sau khi
  lên 148px thì đáy nội dung ở 135px, gọn trong thẻ. Không lỗi JS.
- Tự gõ xuất thân vẫn nhận đúng: "ăn mày" → 26 sinh lực/3 bạc; "tạp dịch" → 34/1.

**Chưa làm:** chưa cân lại độ khó chiến đấu theo bộ số mới (chương 1 hiện không có
công thức so sánh công/thủ, chỉ trừ sinh lực theo kịch bản), nên đổi số **không** làm
hỏng trận nào. Nếu sau này thêm chiến đấu theo chỉ số thì phải cân lại.

---

## 2026-11-20 · Giao diện chọn xuất thân — hướng C

**Người dùng yêu cầu:** màn chọn xuất thân "đơn điệu quá", xin đề xuất làm đẹp hơn.
Ràng buộc nói rõ: *"cái giao diện lúc chọn xuất thân không đụng gì vô game"* → chỉ
giao diện, **không** đổi logic, chỉ số, dữ liệu, luồng chơi.

**Đã làm qua 2 bước:**

1. Bước đầu (commit `f501130`): đổi thẻ xuất thân thành **thẻ có ảnh nền**, tên lớn kiểu
   thư pháp, dấu ✓ khi chọn, xếp **một cột** cho dễ chạm trên iPhone; ô "tự gõ" thu lại
   thành một link.
2. Người dùng hỏi xin **đề xuất** (agent đã lỡ làm luôn — rút kinh nghiệm: hỏi trước khi
   sửa khi người dùng hỏi "có đề xuất gì không"). Agent dựng 3 bản xem thử, chụp ảnh,
   người dùng **chọn hướng C** (commit này).

**Hướng C là gì:** giữ nguyên bố cục thẻ ngang đã kiểm tra chạy tốt, **thêm 2 thứ**:

- **Nền màn hình đổi theo xuất thân đang chọn** — `<div class="nen-chon">` phủ toàn màn,
  `opacity:.42`, ảnh lấy từ chính đoạn mở đầu của xuất thân đó. Bỏ chọn → nền tắt.
- **Trích đoạn mở đầu thật** — `#xtTrich` hiện **câu đầu tiên** của đoạn `doan_dau`,
  cắt ở ~120 ký tự. Lấy từ dữ liệu truyện, **không bịa**.

Thẻ card đổi sang nền trắng đục + `backdrop-filter:blur(9px)` để chữ vẫn đọc rõ trên nền ảnh.

**File đã sửa:**

| File | Sửa gì |
|---|---|
| `docs/game/play.html` | CSS `.nen-chon`/`.lop-phu`/`.xt-trich`; HTML 2 div mới; JS `doiNenXuatThan()`, `trichDoanDau()`; gọi trong `onclick` thẻ |
| `game/play.html` | Y hệt, nhưng `doiNenXuatThan()` đọc từ `_doanDau` (nạp sẵn), và `cauDau()` tách câu |
| `.gitignore` | thêm `node_modules/`, `package-lock.json` (chỉ để test giao diện) |
| `tai-lieu/NHAT-KY.md` | file này |

**Một lỗi đã gặp và sửa:** bản `game/` gọi `fetch("/chapters/chuong1.json")` → **404**,
vì `game_server.py` phục vụ từ **gốc repo** chứ không phải từ `game/`. Đường dẫn đúng là
`/game/chapters/chuong1.json`. Và API `/api/xuat_than` **không trả `doan_dau`**, nên phải
đọc thêm `/game/xuat_than.json` để biết xuất thân nào mở đầu ở đoạn nào.

**Kiểm chứng (số đo thật, không phải "trông có vẻ đúng"):**

- `node --check` phần script inline cả 2 file → **OK**.
- Test jsdom mới (`28` điểm kiểm): nền ẩn trước khi chọn, hiện sau khi chọn, đổi ảnh khi
  chọn thẻ khác, tắt khi bỏ chọn, trích đoạn khớp chữ thật trong truyện, không lẫn chỉ số
  bịa, `Bắt đầu` vẫn chạy → **PASS cả 2 bản**.
- Test cũ: `game/_test_engine.js` **105 đạt, 0 hỏng**; `game/_test_api.py` **161 đạt, 0 hỏng**.
- Trình duyệt thật (Playwright, khổ iPhone 390×844, server cổng 12001): trước khi chọn
  `nenHien=false, trich=""`; chọn tán tu → `bg=bc_cho_01.jpg`, trích đoạn *"Ta mở mắt giữa
  một góc chợ…"*; so 2 ảnh chụp tán tu vs môn phái → **78%** điểm ảnh vùng mép trái đổi
  màu → nền **thật sự** đổi theo lựa chọn.

**Ảnh chụp kết quả:** `docs/nhap/` (`C-truoc.png`, `C-tantu.png`, `C-monphai.png`).

**Chưa làm / biết trước:**

- Cả 2 xuất thân vẫn cho **chỉ số khởi đầu y hệt nhau** (30 sinh lực, 12 tu vi, 3 bạc) —
  chỉ đoạn mở đầu khác. Vì vậy **không** hiện chỉ số trên thẻ (bản demo hướng A từng bịa
  số, đã bỏ). Muốn mỗi xuất thân có chỉ số riêng thì phải sửa **dữ liệu + engine** —
  người dùng đã dặn không đụng, nên **chưa làm**.
- `docs/nhap/` là thư mục tạm để người dùng xem ảnh; **xoá được** khi không cần.
