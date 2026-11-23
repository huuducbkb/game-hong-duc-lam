# Bảng giọng NPC — để prompt tiếng không tự đoán

Mỗi NPC có một chất giọng cố định. Prompt tiếng phải ghi đúng tuổi + giới + chất
giọng, nếu không công cụ tạo tiếng sẽ tự đoán và mỗi cảnh ra một người khác.

| Mã | NPC | Tuổi | Giới | Chất giọng | Câu tiếng Hoa |
|---|---|---|---|---|---|
| `tuyet_co` | Tuyết Cơ | 20 | nữ | mềm như tơ, lạnh ở dưới, nói chậm | 我先问你——你是谁？ |
| `kiem_linh` | Kiếm Linh (Hồng Trần) | ~20 | nam | phẳng, băng giá, rõ, hơi vang ma quái | 若我想杀你，你碰到盒子的那一刻就已经死了。 |
| `han_lap` | Hàn Lập | ~20 | nam | trầm, đều, không vội, phẳng lì | 今晚谁都有秘密。我不问你，你也别问我。 |
| `do_tam` | Đỗ Tam | ~40 | nam | khàn, thô, lớn, chậm, có mối đe dọa dưới | 又来一只老鼠。 |
| `mac_dai_phu` | Mạc Đại Phu | ~60 | nam | già, khàn nhẹ, chậm rãi, điềm tĩnh | 你…和他们不一样。 |
| `he_thong` | Hệ thống | — | máy | vô cảm, đều như máy, không ngữ điệu | — |
| `an_may_que` | Lão ăn mày què | ~60 | nam | lẩm bẩm, khàn, thì thào | — |
| `an_may_khac` | Gã ăn mày khác | ~35 | nam | cười gằn, chua chát | — |
| `phu_khuan_vac` | Phu khuân vác | ~35 | nam | quát to, gắt, hụt hơi | — |
| `su_huynh_to` | Sư huynh to con | ~25 | nam | oang oang, khoe khoang, độc địa | — |
| `hung_ba` | Hùng Bá | ~45 | nam | khàn, từ xa vọng lại, nặng | — |
| `de_tu_nho` | Đệ tử nhỏ | ~14 | nam | thều thào, yếu, đau | — |
| `ga_rau` | Gã râu quai nón | ~40 | nam | hạ giọng, bí mật, hào hứng | — |
| `su_huynh_thi_thao` | Sư huynh (chứng kiến) | ~25 | nam | thì thào, sửng sốt | — |

## Quy tắc chọn câu thoại

**Chỉ lấy lời NPC, không lấy lời nhân vật chính.** Nhân vật chính là người chơi —
người chơi tự đọc chữ trên màn hình. Nếu prompt đưa câu của nhân vật chính vào thì
máy sẽ đọc thành tiếng một giọng khác, sai hẳn.

Cách nhận biết trong truyện:

- Câu của NPC đứng sau dấu gạch nối có tên hoặc chức danh: `— Tuyết Cơ nói`,
  `— kiếm linh nói`, `— ông khẽ nói`, `— hắn gầm lên`.
- Câu của nhân vật chính đứng sau `— ta nói`, `— ta đáp`, `— ta quát`, hoặc nằm
  trong ngoặc kép ngay sau một câu kể ở ngôi thứ nhất.
- Câu không có ai dẫn, mà đứng một mình sau một dòng `*suy nghĩ*` — thường là
  nhân vật chính tự nhủ. Bỏ.

Nếu cảnh chỉ có nhân vật chính nói thì **không thêm thoại**. Prompt vẫn tả tiếng
không gian bình thường.

**Mỗi câu phải ghi tuổi và giới của người nói.** `A young woman's voice, around
twenty` — không ghi thì máy tự đoán, mỗi cảnh ra một người khác.
