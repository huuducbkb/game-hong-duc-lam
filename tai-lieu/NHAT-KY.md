# Nhật ký công việc

File này để **mở khung chat mới vẫn nắm được việc đã làm**. Chat cũ lỗi thì đọc file này
là hiểu ngay: đã làm gì, đang ở đâu, còn gì chưa xong, đo bằng cách nào.

Quy ước ghi: mới nhất ở **trên cùng**. Mỗi mục có **ngày · việc · đã đổi file nào ·
kiểm chứng bằng số đo nào**. Không ghi "đã sửa cho đẹp hơn" — phải ghi đo được cái gì.

Nằm ở `tai-lieu/` (ngoài `docs/`) nên **không bị Pages phục vụ ra web công khai**.

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
