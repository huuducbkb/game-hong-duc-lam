# Nhật ký công việc

File này để **mở khung chat mới vẫn nắm được việc đã làm**. Chat cũ lỗi thì đọc file này
là hiểu ngay: đã làm gì, đang ở đâu, còn gì chưa xong, đo bằng cách nào.

Quy ước ghi: mới nhất ở **trên cùng**. Mỗi mục có **ngày · việc · đã đổi file nào ·
kiểm chứng bằng số đo nào**. Không ghi "đã sửa cho đẹp hơn" — phải ghi đo được cái gì.

Nằm ở `tai-lieu/` (ngoài `docs/`) nên **không bị Pages phục vụ ra web công khai**.

---

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
