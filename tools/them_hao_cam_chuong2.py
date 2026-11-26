"""Thêm phản ứng theo hảo cảm vào Chương 2.

Ba việc, đúng thứ tự engine đọc:
1. `bien_the` — đổi giọng kể/lời thoại theo mức hảo cảm (giữ nguyên sự việc).
2. `dieu_kien.hao_cam` — lựa chọn chỉ mở khi đủ thân.
3. Nhánh hậu quả — hảo cảm thấp thì Hàn Lập không giúp, đường đi khác hẳn.

Chạy lại nhiều lần được: mỗi bước đều kiểm tra đã có chưa.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
P = GOC / "game" / "chapters" / "chuong2.json"


def json_khong_dau(s: str) -> str:
    """Bỏ dấu tiếng Việt để so khớp khoá NPC."""
    import unicodedata

    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def tim(ds: dict, did: str) -> dict:
    x = ds.get(did)
    if x is None:
        sys.exit(f"Không có đoạn {did} — dữ liệu đã đổi khác dự kiến")
    return x


def dat_bien_the(x: dict, npc: str, ds_bien_the: list[dict]) -> None:
    """Gắn bien_the, bỏ biến thể cũ của cùng NPC để chạy lại không nhân đôi."""
    cu = [b for b in (x.get("bien_the") or []) if b.get("npc") != npc]
    x["bien_the"] = cu + [{"npc": npc, **b} for b in ds_bien_the]


def them_lua_chon(x: dict, moi: dict) -> None:
    """Thêm lựa chọn nếu chưa có (so theo `chu`)."""
    lc = x.setdefault("lua_chon", [])
    if any(l.get("chu") == moi["chu"] for l in lc):
        return
    lc.append(moi)


def main() -> None:
    d = json.loads(P.read_text(encoding="utf-8"))
    ds = {x["id"]: x for x in d["doan"]}
    HL = "Hàn Lập"

    # ---------------------------------------------------------------- 1. bien_the
    # Mỗi biến thể giữ NGUYÊN sự việc của `ke` gốc, chỉ đổi giọng Hàn Lập và cách
    # người kể nhìn hắn. Bậc "thân thiết" trùng giọng gốc nên không cần viết lại.

    # c2_d06 — bà chủ Mạc phủ khinh người kể; Hàn Lập phản ứng theo mức thân.
    dat_bien_the(tim(ds, "c2_d06"), HL, [
        {"muc": "tử địch", "ke": (
            "Trong sân, người ta đã dựng một gian lều tang trắng. Khói hương quyện với mùi giấy "
            "vàng cháy, mùi ấy bám vào cổ họng ta đến khó thở.\n\n"
            "Ba người phụ nữ mặc đồ tang ngồi quỳ bên trong. Hai người khóc. Một người thì không.\n\n"
            "Hàn Lập quỳ xuống, đặt hòm gỗ lên chiếc bàn thấp trước linh vị. Hắn không nhìn ta.\n\n"
            "“Đệ tử Hàn Lập,” — hắn nói, giọng khàn — “Mang di vật của sư phụ về.”\n\n"
            "Người phụ nữ không khóc đứng dậy. Bà ta nhìn hắn một lúc lâu, rồi nhìn sang ta — "
            "ánh mắt sắc như dao cau.\n\n"
            "“Còn ngươi là ai?”\n\n"
            "“Bạn của hắn,” — ta đáp.\n\n"
            "“Bạn.” — Bà ta nhắc lại, giọng không giấu vẻ khinh. — “Một kẻ ăn mày làm bạn với "
            "đệ tử của phụ thân ta. Thời buổi này thật lạ.”\n\n"
            "Ta cúi đầu, không đáp. Ta đã nghe câu ấy nhiều lần đến mức nó không còn làm ta đau "
            "nữa.\n\n"
            "Khi bà ta quay đi, Hàn Lập mới lên tiếng — không phải để bênh ta.\n\n"
            "“Người này đi cùng ta,” — hắn nói, mắt vẫn nhìn linh vị. — “Có gì hỏi ta.”\n\n"
            "Giọng hắn phẳng, không ấm. Như đang khai một món đồ trong túi, không phải nói về "
            "một người."
        )},
        {"muc": "thù địch", "ke": (
            "Trong sân, người ta đã dựng một gian lều tang trắng. Khói hương quyện với mùi giấy "
            "vàng cháy, mùi ấy bám vào cổ họng ta đến khó thở.\n\n"
            "Ba người phụ nữ mặc đồ tang ngồi quỳ bên trong. Hai người khóc. Một người thì không.\n\n"
            "Hàn Lập quỳ xuống, đặt hòm gỗ lên chiếc bàn thấp trước linh vị.\n\n"
            "“Đệ tử Hàn Lập,” — hắn nói, giọng khàn — “Mang di vật của sư phụ về.”\n\n"
            "Người phụ nữ không khóc đứng dậy. Bà ta nhìn hắn một lúc lâu, rồi nhìn sang ta — "
            "ánh mắt sắc như dao cau.\n\n"
            "“Còn ngươi là ai?”\n\n"
            "“Bạn của hắn,” — ta đáp.\n\n"
            "“Bạn.” — Bà ta nhắc lại, giọng không giấu vẻ khinh. — “Một kẻ ăn mày làm bạn với "
            "đệ tử của phụ thân ta. Thời buổi này thật lạ.”\n\n"
            "Ta cúi đầu, không đáp.\n\n"
            "Hàn Lập không nói gì giúp ta. Hắn đứng dậy, phủi đầu gối, rồi bước ra phía cửa — "
            "và dừng lại khi ngang qua ta.\n\n"
            "“Đứng đây làm gì,” — hắn nói, rất khẽ, chỉ đủ cho ta nghe. — “Không ai giữ ngươi.”\n\n"
            "Rồi hắn đi. Ta ở lại giữa sân, giữa ba người đàn bà đang khóc, và không ai nhìn ta "
            "thêm một lần nào nữa."
        )},
        {"muc": "người dưng", "ke": (
            "Trong sân, người ta đã dựng một gian lều tang trắng. Khói hương quyện với mùi giấy "
            "vàng cháy, mùi ấy bám vào cổ họng ta đến khó thở.\n\n"
            "Ba người phụ nữ mặc đồ tang ngồi quỳ bên trong. Hai người khóc. Một người thì không.\n\n"
            "Hàn Lập quỳ xuống, đặt hòm gỗ lên chiếc bàn thấp trước linh vị.\n\n"
            "“Đệ tử Hàn Lập,” — hắn nói, giọng khàn — “Mang di vật của sư phụ về.”\n\n"
            "Người phụ nữ không khóc đứng dậy. Bà ta nhìn hắn một lúc lâu, rồi nhìn sang ta — "
            "ánh mắt sắc như dao cau.\n\n"
            "“Còn ngươi là ai?”\n\n"
            "“Bạn của hắn,” — ta đáp.\n\n"
            "“Bạn.” — Bà ta nhắc lại, giọng không giấu vẻ khinh. — “Một kẻ ăn mày làm bạn với "
            "đệ tử của phụ thân ta. Thời buổi này thật lạ.”\n\n"
            "Ta cúi đầu, không đáp. Ta đã nghe câu ấy nhiều lần đến mức nó không còn làm ta đau "
            "nữa.\n\n"
            "Hàn Lập đứng bên cạnh, không nhìn ta, cũng không nhìn bà ta. Hắn chỉ nói một câu, "
            "đều đều: “Xong việc rồi. Ta đi.”\n\n"
            "Bà ta không giữ hắn lại. Hắn cũng không đợi ta."
        )},
        {"muc": "quen biết", "ke": (
            "Trong sân, người ta đã dựng một gian lều tang trắng. Khói hương quyện với mùi giấy "
            "vàng cháy, mùi ấy bám vào cổ họng ta đến khó thở.\n\n"
            "Ba người phụ nữ mặc đồ tang ngồi quỳ bên trong. Hai người khóc. Một người thì không.\n\n"
            "Hàn Lập quỳ xuống, đặt hòm gỗ lên chiếc bàn thấp trước linh vị.\n\n"
            "“Đệ tử Hàn Lập,” — hắn nói, giọng khàn — “Mang di vật của sư phụ về.”\n\n"
            "Người phụ nữ không khóc đứng dậy. Bà ta nhìn hắn một lúc lâu, rồi nhìn sang ta — "
            "ánh mắt sắc như dao cau.\n\n"
            "“Còn ngươi là ai?”\n\n"
            "“Bạn của hắn,” — ta đáp.\n\n"
            "“Bạn.” — Bà ta nhắc lại, giọng không giấu vẻ khinh. — “Một kẻ ăn mày làm bạn với "
            "đệ tử của phụ thân ta. Thời buổi này thật lạ.”\n\n"
            "Ta cúi đầu, không đáp. Ta đã nghe câu ấy nhiều lần đến mức nó không còn làm ta đau "
            "nữa.\n\n"
            "“Bà ấy nói quá,” — Hàn Lập nói, khi bà ta đã đi khuất. — “Không phải vì ta. Vì hôm "
            "nay là ngày chôn sư phụ ta, và bà ấy cần một người để giận.”\n\n"
            "Hắn nói xong thì im, như hối đã nói nhiều hơn mình định nói."
        )},
    ])

    # c2_p02 — đám tang ở Thất Huyền Môn; Hàn Lập kể bí mật Trường Xuân Công.
    dat_bien_the(tim(ds, "c2_p02"), HL, [
        {"muc": "tử địch", "ke": (
            "Sân tập giờ là một bãi đất lộn xộn. Một nửa mái che đã sập, cột cờ gãy làm đôi, và ở "
            "góc sân người ta đang dựng một dãy giường tre để kê người bị thương.\n\n"
            "Các đệ tử đi lại như những cái bóng. Không ai nói to. Không ai cười.\n\n"
            "Ta thấy Hàn Lập đứng ở rìa sân, bên cạnh một cái cáng phủ vải trắng. Hắn không khóc. "
            "Hắn chỉ đứng đó, hai tay buông thõng, nhìn xuống.\n\n"
            "Ta tới gần. Hắn quay lại, thấy ta, và bước lùi nửa bước — rất nhỏ, nhưng ta thấy.\n\n"
            "“Ngươi tới đây làm gì?”\n\n"
            "“Ta—”\n\n"
            "“Sư phụ ta nằm đó.” — Hắn không cao giọng. — “Ngươi có việc thì nói. Không có thì đi.”\n\n"
            "Ta đứng im. Hắn cũng đứng im, và không nói thêm một lời nào về Trường Xuân Công. "
            "Cái bí mật ấy hắn giữ kín thêm một ngày nữa — khỏi ta."
        )},
        {"muc": "thù địch", "ke": (
            "Sân tập giờ là một bãi đất lộn xộn. Một nửa mái che đã sập, cột cờ gãy làm đôi, và ở "
            "góc sân người ta đang dựng một dãy giường tre để kê người bị thương.\n\n"
            "Các đệ tử đi lại như những cái bóng. Không ai nói to. Không ai cười.\n\n"
            "Ta thấy Hàn Lập đứng ở rìa sân, bên cạnh một cái cáng phủ vải trắng. Hắn không khóc. "
            "Hắn chỉ đứng đó, hai tay buông thõng, nhìn xuống.\n\n"
            "Ta tới gần. Hắn không quay lại, nhưng biết ta ở đó.\n\n"
            "“Sư phụ ta,” — hắn nói, giọng đều đến lạ — “Người ta bảo ông ấy là lang y.”\n\n"
            "Hắn dừng. Rồi hắn nói tiếp, và câu sau lạnh hơn câu trước: “Ngươi về đi. Hôm nay ta "
            "không nói chuyện với ai.”\n\n"
            "“Ta chỉ đứng đây.”\n\n"
            "“Thì đứng.” — Hắn nhìn xuống cái cáng. — “Nhưng đừng hỏi ta gì.”\n\n"
            "Ta đứng đó rất lâu. Hắn không nói thêm câu nào. Bí mật Trường Xuân Công vẫn nằm "
            "trong ngực hắn, và hắn chọn không trao nó cho ta."
        )},
        {"muc": "người dưng", "ke": (
            "Sân tập giờ là một bãi đất lộn xộn. Một nửa mái che đã sập, cột cờ gãy làm đôi, và ở "
            "góc sân người ta đang dựng một dãy giường tre để kê người bị thương.\n\n"
            "Các đệ tử đi lại như những cái bóng. Không ai nói to. Không ai cười.\n\n"
            "Ta thấy Hàn Lập đứng ở rìa sân, bên cạnh một cái cáng phủ vải trắng. Hắn không khóc. "
            "Hắn chỉ đứng đó, hai tay buông thõng, nhìn xuống.\n\n"
            "Ta tới gần. Hắn không quay lại, nhưng biết ta ở đó.\n\n"
            "“Sư phụ ta,” — hắn nói, giọng đều đến lạ — “Người ta bảo ông ấy là lang y. Nhưng ta "
            "biết ông ấy không phải.”\n\n"
            "Ta không đáp. Ta không biết phải đáp gì.\n\n"
            "Hắn đợi một lúc, như đợi ta hỏi tiếp. Ta không hỏi. Rồi hắn nói, ngắn hơn: “Thôi. "
            "Không có gì.”\n\n"
            "Bí mật ấy hắn giữ lại. Ta đứng cạnh hắn, và giữa hai người là khoảng cách của hai "
            "kẻ cùng đứng dưới một mái nhà nhưng không cùng một câu chuyện."
        )},
        {"muc": "quen biết", "ke": (
            "Sân tập giờ là một bãi đất lộn xộn. Một nửa mái che đã sập, cột cờ gãy làm đôi, và ở "
            "góc sân người ta đang dựng một dãy giường tre để kê người bị thương.\n\n"
            "Các đệ tử đi lại như những cái bóng. Không ai nói to. Không ai cười.\n\n"
            "Ta thấy Hàn Lập đứng ở rìa sân, bên cạnh một cái cáng phủ vải trắng. Hắn không khóc. "
            "Hắn chỉ đứng đó, hai tay buông thõng, nhìn xuống.\n\n"
            "Ta tới gần. Hắn không quay lại, nhưng biết ta ở đó.\n\n"
            "“Sư phụ ta,” — hắn nói, giọng đều đến lạ — “Người ta bảo ông ấy là lang y. Nhưng ta "
            "biết ông ấy không phải.”\n\n"
            "Ta không đáp.\n\n"
            "“Ông ấy dạy ta một bộ công pháp,” — hắn nói tiếp, ngập ngừng — “Trường Xuân Công. "
            "Ông bảo đừng nói với ai.”\n\n"
            "Hắn dừng, như tự hỏi có nên nói tiếp không. Rồi hắn thôi, và quay mặt đi. Ta hiểu: "
            "hắn đã trao cho ta một nửa, và giữ lại nửa kia."
        )},
    ])

    # c2_c04a — can thiệp giúp Hàn Lập ở chợ; hắn nhìn ta thế nào.
    dat_bien_the(tim(ds, "c2_c04a"), HL, [
        {"muc": "tử địch", "ke": (
            "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
            "“Mảnh ngọc ấy,” — ta nói, giọng bình thản đến mức chính ta cũng ngạc nhiên — “không "
            "phải ngọc thường. Ngươi thử cầm nó dưới nắng xem.”\n\n"
            "Gã áo gấm nhíu mày. Nhưng gã vẫn làm — giơ mảnh ngọc lên.\n\n"
            "Ánh hoàng hôn xuyên qua. Và trong lòng mảnh ngọc, một vệt sáng đỏ thẫm hiện ra, chậm "
            "rãi xoay như máu đang chảy.\n\n"
            "Mặt gã đổi màu.\n\n"
            "“Cái này… đây là huyết ngọc?”\n\n"
            "“Ta không biết nó là gì,” — ta nói thật — “Nhưng ta biết hai viên hạ phẩm là giá của "
            "kẻ không biết nó là gì.”\n\n"
            "Gã nhìn ta rất lâu. Rồi gã cười — lần này cười thật.\n\n"
            "“Ngươi là ai?”\n\n"
            "“Không ai cả.”\n\n"
            "“Không ai cả mà dám phá ngang việc của ta.” — Gã ném xuống tấm vải một cái túi nhỏ. — "
            "“Mười viên. Giá thật. Vì ta thích kẻ dám nói.”\n\n"
            "Gã đi. Ta quay lại, và thấy Hàn Lập đang nhìn ta — nhưng không phải ánh mắt của kẻ "
            "vừa được cứu. Là ánh mắt của kẻ đang tính xem ta muốn gì.\n\n"
            "“Vì sao ngươi giúp ta?” — hắn hỏi, và trong giọng hắn không có một chút hàm ơn nào.\n\n"
            "“Vì ta đã từng bị trả giá hai viên,” — ta đáp.\n\n"
            "“Vậy ngươi được gì?”\n\n"
            "Ta không trả lời. Hắn cũng không hỏi lại. Hắn chỉ nhìn cái túi trong tay ta, và tôi "
            "biết hắn đang nghĩ: đây là một món nợ, và nợ thì phải trả."
        )},
        {"muc": "thù địch", "ke": (
            "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
            "“Mảnh ngọc ấy,” — ta nói, giọng bình thản đến mức chính ta cũng ngạc nhiên — “không "
            "phải ngọc thường. Ngươi thử cầm nó dưới nắng xem.”\n\n"
            "Gã áo gấm nhíu mày. Nhưng gã vẫn làm — giơ mảnh ngọc lên.\n\n"
            "Ánh hoàng hôn xuyên qua. Và trong lòng mảnh ngọc, một vệt sáng đỏ thẫm hiện ra, chậm "
            "rãi xoay như máu đang chảy.\n\n"
            "Mặt gã đổi màu.\n\n"
            "“Cái này… đây là huyết ngọc?”\n\n"
            "“Ta không biết nó là gì,” — ta nói thật — “Nhưng ta biết hai viên hạ phẩm là giá của "
            "kẻ không biết nó là gì.”\n\n"
            "Gã nhìn ta rất lâu. Rồi gã cười — lần này cười thật.\n\n"
            "“Ngươi là ai?”\n\n"
            "“Không ai cả.”\n\n"
            "“Không ai cả mà dám phá ngang việc của ta.” — Gã ném xuống tấm vải một cái túi nhỏ. — "
            "“Mười viên. Giá thật. Vì ta thích kẻ dám nói.”\n\n"
            "Gã đi. Ta quay lại, và thấy Hàn Lập đang nhìn ta.\n\n"
            "“Đừng làm thế lần nữa,” — hắn nói. Không phải cảm ơn, cũng không phải mắng. — “Ta "
            "không cần ngươi đứng ra trước mặt ta.”\n\n"
            "Hắn cầm túi linh thạch, đếm, rồi nhét vào vạt áo — và không nhìn ta thêm một lần nào."
        )},
        {"muc": "người dưng", "ke": (
            "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
            "“Mảnh ngọc ấy,” — ta nói, giọng bình thản đến mức chính ta cũng ngạc nhiên — “không "
            "phải ngọc thường. Ngươi thử cầm nó dưới nắng xem.”\n\n"
            "Gã áo gấm nhíu mày. Nhưng gã vẫn làm — giơ mảnh ngọc lên.\n\n"
            "Ánh hoàng hôn xuyên qua. Và trong lòng mảnh ngọc, một vệt sáng đỏ thẫm hiện ra, chậm "
            "rãi xoay như máu đang chảy.\n\n"
            "Mặt gã đổi màu.\n\n"
            "“Cái này… đây là huyết ngọc?”\n\n"
            "“Ta không biết nó là gì,” — ta nói thật — “Nhưng ta biết hai viên hạ phẩm là giá của "
            "kẻ không biết nó là gì.”\n\n"
            "Gã nhìn ta rất lâu. Rồi gã cười — lần này cười thật.\n\n"
            "“Ngươi là ai?”\n\n"
            "“Không ai cả.”\n\n"
            "“Không ai cả mà dám phá ngang việc của ta.” — Gã ném xuống tấm vải một cái túi nhỏ. — "
            "“Mười viên. Giá thật. Vì ta thích kẻ dám nói.”\n\n"
            "Gã đi. Ta quay lại, và thấy Hàn Lập đang nhìn ta — lần đầu tiên, nhìn thẳng, không "
            "giấu gì.\n\n"
            "“Vì sao ngươi giúp ta?”\n\n"
            "“Vì ta đã từng bị trả giá hai viên,” — ta đáp.\n\n"
            "Hắn gật đầu, chậm. Rồi hắn nói, như đang ghi một món nợ vào sổ: “Ta nhớ.”"
        )},
        {"muc": "quen biết", "ke": (
            "Ta bước tới, đứng chắn giữa gã áo gấm và tấm vải.\n\n"
            "“Mảnh ngọc ấy,” — ta nói, giọng bình thản đến mức chính ta cũng ngạc nhiên — “không "
            "phải ngọc thường. Ngươi thử cầm nó dưới nắng xem.”\n\n"
            "Gã áo gấm nhíu mày. Nhưng gã vẫn làm — giơ mảnh ngọc lên.\n\n"
            "Ánh hoàng hôn xuyên qua. Và trong lòng mảnh ngọc, một vệt sáng đỏ thẫm hiện ra, chậm "
            "rãi xoay như máu đang chảy.\n\n"
            "Mặt gã đổi màu.\n\n"
            "“Cái này… đây là huyết ngọc?”\n\n"
            "“Ta không biết nó là gì,” — ta nói thật — “Nhưng ta biết hai viên hạ phẩm là giá của "
            "kẻ không biết nó là gì.”\n\n"
            "Gã nhìn ta rất lâu. Rồi gã cười — lần này cười thật.\n\n"
            "“Ngươi là ai?”\n\n"
            "“Không ai cả.”\n\n"
            "“Không ai cả mà dám phá ngang việc của ta.” — Gã ném xuống tấm vải một cái túi nhỏ. — "
            "“Mười viên. Giá thật. Vì ta thích kẻ dám nói.”\n\n"
            "Gã đi. Ta quay lại, và thấy Hàn Lập đang nhìn ta — lần đầu tiên, nhìn thẳng, không "
            "giấu gì.\n\n"
            "“Vì sao ngươi giúp ta?”\n\n"
            "“Vì ta đã từng bị trả giá hai viên,” — ta đáp.\n\n"
            "Hắn cười, rất khẽ — lần đầu tiên ta thấy hắn cười. Rồi hắn nói: “Vậy thì lần này ta "
            "nợ ngươi. Ta không thích nợ.”"
        )},
    ])

    # c2_c09 — Hàn Lập bị ép giá thuốc của sư phụ; hắn có kể lý do hay không.
    dat_bien_the(tim(ds, "c2_c09"), HL, [
        {"muc": "tử địch", "ke": (
            "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
            "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân "
            "nhỏ. Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
            "“Thuốc này là thuốc phàm,” — người đàn bà nói — “Không có linh khí. Nhưng công dụng "
            "thì thật. Ta cho ngươi một viên hạ phẩm cho cả mẻ.”\n\n"
            "“Một viên?”\n\n"
            "“Một viên. Hoặc ngươi mang về.”\n\n"
            "Hàn Lập im. Ta thấy tay hắn nắm lại rồi mở ra.\n\n"
            "“Được,” — hắn nói.\n\n"
            "Ta bước tới. “Khoan.”\n\n"
            "Hàn Lập quay phắt lại. “Ngươi làm gì ở đây?”\n\n"
            "“Ta—”\n\n"
            "“Việc của ta.” — Hắn chắn trước mặt ta, che mấy lọ thuốc. — “Ngươi không cần đứng ra. "
            "Đi đi.”\n\n"
            "Người đàn bà nhìn hai chúng ta, rồi cười một tiếng ngắn. “Thôi. Một viên. Lấy hay "
            "không?”\n\n"
            "Hàn Lập lấy một viên. Rồi hắn đi, và không đợi ta."
        )},
        {"muc": "thù địch", "ke": (
            "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
            "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân "
            "nhỏ. Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
            "“Thuốc này là thuốc phàm,” — người đàn bà nói — “Không có linh khí. Nhưng công dụng "
            "thì thật. Ta cho ngươi một viên hạ phẩm cho cả mẻ.”\n\n"
            "“Một viên?”\n\n"
            "“Một viên. Hoặc ngươi mang về.”\n\n"
            "Hàn Lập im. Ta thấy tay hắn nắm lại rồi mở ra.\n\n"
            "“Được,” — hắn nói.\n\n"
            "Ta bước tới. “Khoan.”\n\n"
            "Người đàn bà nhìn ta. “Ngươi là ai?”\n\n"
            "“Người biết giá.” — Ta chỉ vào mấy lọ thuốc. — “Bà nói công dụng thật. Vậy thử một lọ "
            "trước mặt mọi người. Nếu thật, giá phải gấp ba.”\n\n"
            "Im lặng.\n\n"
            "Rồi người đàn bà cười — một tiếng cười ngắn, sắc. “Ngươi không phải kẻ mới.”\n\n"
            "“Ta mới bốn ngày.”\n\n"
            "“Kẻ mới bốn ngày không biết nói thế.” — Bà ta nhìn ta rất lâu, rồi đặt lên quầy ba "
            "viên đá xanh. — “Ba viên. Và ta sẽ nhớ mặt ngươi.”\n\n"
            "Bà ta đi. Hàn Lập nhìn ba viên linh thạch trong tay, rồi nhìn ta — và không nói gì.\n\n"
            "Hắn cất thuốc, cất linh thạch, rồi đi về phía dãy hàng phía nam. Ta đi theo một "
            "quãng, và hắn không quay lại lần nào."
        )},
        {"muc": "người dưng", "ke": (
            "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
            "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân "
            "nhỏ. Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
            "“Thuốc này là thuốc phàm,” — người đàn bà nói — “Không có linh khí. Nhưng công dụng "
            "thì thật. Ta cho ngươi một viên hạ phẩm cho cả mẻ.”\n\n"
            "“Một viên?”\n\n"
            "“Một viên. Hoặc ngươi mang về.”\n\n"
            "Hàn Lập im. Ta thấy tay hắn nắm lại rồi mở ra.\n\n"
            "“Được,” — hắn nói.\n\n"
            "Ta bước tới. “Khoan.”\n\n"
            "Người đàn bà nhìn ta. “Ngươi là ai?”\n\n"
            "“Người biết giá.” — Ta chỉ vào mấy lọ thuốc. — “Bà nói công dụng thật. Vậy thử một lọ "
            "trước mặt mọi người. Nếu thật, giá phải gấp ba.”\n\n"
            "Im lặng.\n\n"
            "Rồi người đàn bà cười — một tiếng cười ngắn, sắc. “Ngươi không phải kẻ mới.”\n\n"
            "“Ta mới bốn ngày.”\n\n"
            "“Kẻ mới bốn ngày không biết nói thế.” — Bà ta nhìn ta rất lâu, rồi đặt lên quầy ba "
            "viên đá xanh. — “Ba viên. Và ta sẽ nhớ mặt ngươi.”\n\n"
            "Bà ta đi. Hàn Lập nhìn ba viên linh thạch trong tay, rồi nhìn ta.\n\n"
            "“Lần thứ hai,” — hắn nói.\n\n"
            "“Lần thứ hai gì?”\n\n"
            "Hắn không trả lời. Hắn chỉ chia cho ta một viên, rồi đi — và đó là tất cả những gì ta "
            "được nghe từ hắn ngày hôm ấy."
        )},
        {"muc": "quen biết", "ke": (
            "Ta tìm thấy Hàn Lập ở dãy hàng phía bắc, trước một quầy bán đan dược.\n\n"
            "Hắn đang nói chuyện với một người đàn bà trung niên, mặt lạnh, tay cầm một cái cân "
            "nhỏ. Trước mặt họ là mấy lọ thuốc của Mạc Đại Phu.\n\n"
            "“Thuốc này là thuốc phàm,” — người đàn bà nói — “Không có linh khí. Nhưng công dụng "
            "thì thật. Ta cho ngươi một viên hạ phẩm cho cả mẻ.”\n\n"
            "“Một viên?”\n\n"
            "“Một viên. Hoặc ngươi mang về.”\n\n"
            "Hàn Lập im. Ta thấy tay hắn nắm lại rồi mở ra.\n\n"
            "“Được,” — hắn nói.\n\n"
            "Ta bước tới. “Khoan.”\n\n"
            "Người đàn bà nhìn ta. “Ngươi là ai?”\n\n"
            "“Người biết giá.” — Ta chỉ vào mấy lọ thuốc. — “Bà nói công dụng thật. Vậy thử một lọ "
            "trước mặt mọi người. Nếu thật, giá phải gấp ba.”\n\n"
            "Im lặng.\n\n"
            "Rồi người đàn bà cười — một tiếng cười ngắn, sắc. “Ngươi không phải kẻ mới.”\n\n"
            "“Ta mới bốn ngày.”\n\n"
            "“Kẻ mới bốn ngày không biết nói thế.” — Bà ta nhìn ta rất lâu, rồi đặt lên quầy ba "
            "viên đá xanh. — “Ba viên. Và ta sẽ nhớ mặt ngươi.”\n\n"
            "Bà ta đi. Hàn Lập nhìn ba viên linh thạch trong tay, rồi nhìn ta.\n\n"
            "“Lần thứ hai,” — hắn nói.\n\n"
            "“Lần thứ hai gì?”\n\n"
            "“Lần thứ hai ngươi giúp ta mà ta không hiểu vì sao.” — Hắn chia cho ta một viên. — "
            "“Ta không thích mắc nợ người lạ. Nên lần sau, đừng làm nữa.”\n\n"
            "Nhưng hắn nói câu ấy mà không nhìn ta, và ta biết hắn không thật lòng."
        )},
    ])

    # c2_c15 — đêm Hàn Lập đổi chỗ ngủ cho ta. Đây là chỗ hảo cảm quyết định hắn có
    # làm hay không, nên biến thể phải khác cả HÀNH ĐỘNG, không chỉ giọng.
    dat_bien_the(tim(ds, "c2_c15"), HL, [
        {"muc": "tử địch", "ke": (
            "Ta kể cho Hàn Lập nghe mọi chuyện, trừ một điều.\n\n"
            "Ta kể về viên đá. Ta kể về sợi sáng mảnh như tơ. Ta kể về bà lão và hai kẻ bà đã "
            "thấy trước ta.\n\n"
            "Hắn nghe hết, rồi đứng dậy.\n\n"
            "“Vậy là ngươi có linh căn mạnh,” — hắn nói. — “Mạnh đến mức người ta đi tìm ngươi "
            "giữa đêm.”\n\n"
            "“Có vẻ vậy.”\n\n"
            "“Vậy thì đừng ngủ cạnh ta.” — Hắn nhặt túi lên. — “Ta không muốn chết vì một kẻ ta "
            "mới biết bốn ngày.”\n\n"
            "Hắn đi về phía đông, tới chỗ những túp lều khác. Ta ngồi lại một mình bên đống lửa "
            "đã tàn.\n\n"
            "Đêm ấy ta ngủ không nhắm mắt. Không ai tới. Nhưng cũng không ai ở đó."
        )},
        {"muc": "thù địch", "ke": (
            "Ta kể cho Hàn Lập nghe mọi chuyện, trừ một điều.\n\n"
            "Ta kể về viên đá. Ta kể về sợi sáng mảnh như tơ. Ta kể về bà lão và hai kẻ bà đã "
            "thấy trước ta — một người được đưa lên núi rồi biệt tăm, một người chết không còn "
            "nguyên vẹn.\n\n"
            "Hắn nghe, mặt không đổi.\n\n"
            "“Vậy là ngươi có linh căn mạnh,” — hắn nói. — “Mạnh đến mức bà ta sợ.”\n\n"
            "“Có vẻ vậy.”\n\n"
            "Hắn im một lúc. Rồi: “Vậy thì ngươi tự lo đi.”\n\n"
            "“Ngươi nói gì?”\n\n"
            "“Ta nói ta không gánh nổi.” — Hắn nhìn thẳng vào ta, không né. — “Ba kẻ kia đang tìm "
            "ngươi. Ta mới tu được mấy năm. Ta không phải kẻ để ngươi dựa vào.”\n\n"
            "Hắn đứng dậy, đi về phía chỗ hắn ngủ, và nằm xuống. Ta ngồi đó rất lâu.\n\n"
            "Đêm ấy ta ngủ một mình. Không ai đổi chỗ cho ta."
        )},
        {"muc": "người dưng", "ke": (
            "Ta kể cho Hàn Lập nghe mọi chuyện, trừ một điều.\n\n"
            "Ta kể về viên đá. Ta kể về sợi sáng mảnh như tơ. Ta kể về bà lão và hai kẻ bà đã "
            "thấy trước ta — một người được đưa lên núi rồi biệt tăm, một người chết không còn "
            "nguyên vẹn.\n\n"
            "Hắn nghe hết. Rồi hắn hỏi một câu ta không ngờ: “Ngươi muốn ta làm gì?”\n\n"
            "“Ta không muốn ngươi làm gì cả.”\n\n"
            "“Vậy thì ta không làm gì cả.” — Hắn gật đầu. — “Có người tới thì gọi ta.”\n\n"
            "Hắn nằm xuống chỗ hắn, cách ta vài bước. Không đổi chỗ. Không hứa gì.\n\n"
            "Đêm ấy ta ngủ chập chờn, và mỗi lần tỉnh dậy, ta đều thấy bóng hắn vẫn ở đó — không "
            "phải để che cho ta, chỉ là ở đó."
        )},
        {"muc": "quen biết", "ke": (
            "Ta kể cho Hàn Lập nghe mọi chuyện, trừ một điều.\n\n"
            "Ta kể về viên đá. Ta kể về sợi sáng mảnh như tơ. Ta kể về bà lão và hai kẻ bà đã "
            "thấy trước ta — một người được đưa lên núi rồi biệt tăm, một người chết không còn "
            "nguyên vẹn.\n\n"
            "Hắn im rất lâu.\n\n"
            "“Vậy là ngươi có linh căn mạnh,” — hắn nói. — “Mạnh đến mức bà ta sợ.”\n\n"
            "“Có vẻ vậy.”\n\n"
            "“Và ngươi mới tu bốn ngày.”\n\n"
            "“Có vẻ vậy.”\n\n"
            "Hắn nhìn đống lửa. Rồi hắn nói, chậm rãi, như đang tự thuyết phục mình: “Đêm nay ta "
            "ngủ gần ngươi hơn một chút. Không phải vì ta tốt. Vì nếu ngươi chết, ta mất một "
            "người biết chuyện của sư phụ ta.”\n\n"
            "Hắn kéo túi lại gần hơn, và không nói thêm gì."
        )},
    ])

    # c2_c25 — chia tay ở rìa thung lũng. Hảo cảm thấp thì hắn không ngỏ lời đợi ta.
    dat_bien_the(tim(ds, "c2_c25"), HL, [
        {"muc": "tử địch", "ke": (
            "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
            "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở "
            "rìa, chỗ những lều bị đốt.\n\n"
            "Hàn Lập dừng lại ở miệng một khe núi, quay đầu nhìn lần cuối.\n\n"
            "“Ta đi đường này,” — hắn nói. — “Ngươi đi đường ngươi.”\n\n"
            "“Hàn Lập—”\n\n"
            "“Đừng.” — Hắn không quay lại. — “Ta đã nói rồi. Ta không gánh nổi ngươi. Đừng bắt ta "
            "nói lần thứ ba.”\n\n"
            "Rồi hắn đi. Áo xám của hắn lẫn vào đá, rồi mất hẳn.\n\n"
            "Ta đứng đó, tay không, và lần đầu tiên trong sáu ngày, ta hiểu thế nào là ở một mình "
            "trong thế giới này."
        )},
        {"muc": "thù địch", "ke": (
            "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
            "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở "
            "rìa, chỗ những lều bị đốt.\n\n"
            "Hàn Lập dừng lại ở miệng một khe núi.\n\n"
            "“Ta có một tấm lệnh,” — hắn nói. — “Ngươi không có.”\n\n"
            "“Ta biết.”\n\n"
            "“Ta đi Hoàng Phong Cốc.” — Hắn nói, không do dự. — “Đó là đường của ta.”\n\n"
            "Hắn không hỏi ta đi đâu. Hắn cũng không đưa tay ra.\n\n"
            "“Cảm ơn vì đã cứu ta ở chợ,” — hắn nói, và câu ấy nghe như một món nợ đã trả xong.\n\n"
            "Rồi hắn đi. Ta đứng lại, và không ai đợi ta ở đâu cả."
        )},
        {"muc": "người dưng", "ke": (
            "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
            "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở "
            "rìa, chỗ những lều bị đốt.\n\n"
            "Hàn Lập dừng lại ở miệng một khe núi, quay đầu nhìn lần cuối.\n\n"
            "“Ba tấm lệnh,” — hắn nói. — “Ta có một. Hai tấm kia đã mất cùng người giữ chúng.”\n\n"
            "“Vậy ngươi sẽ đi đâu?”\n\n"
            "“Hoàng Phong Cốc.” — Hắn nói, không do dự. — “Một trong Thất Đại Môn Phái. Ở đó có "
            "người nhận lệnh.”\n\n"
            "Ta không nói gì.\n\n"
            "“Còn ngươi?” — hắn hỏi.\n\n"
            "Ta nhìn xuống tay mình. Không có gì trong tay.\n\n"
            "“Ta không có lệnh,” — ta nói. — “Nhưng ta có linh căn.”\n\n"
            "Hàn Lập gật đầu. Rồi hắn quay đi.\n\n"
            "“Đi được thì đi,” — hắn nói, không quay lại. — “Đường này không dành cho người chậm.”\n\n"
            "Đó là tất cả những gì hắn nói với ta trước khi đi."
        )},
        {"muc": "quen biết", "ke": (
            "Chúng ta ra khỏi cốc khi trời đã tối hẳn.\n\n"
            "Phía sau, Thái Nam Cốc vẫn còn cháy. Không phải cháy lớn — chỉ là mấy đám lửa nhỏ ở "
            "rìa, chỗ những lều bị đốt.\n\n"
            "Hàn Lập dừng lại ở miệng một khe núi, quay đầu nhìn lần cuối.\n\n"
            "“Ba tấm lệnh,” — hắn nói. — “Ta có một.”\n\n"
            "“Vậy ngươi sẽ đi đâu?”\n\n"
            "“Hoàng Phong Cốc.” — Hắn nói, không do dự. — “Một trong Thất Đại Môn Phái. Ở đó có "
            "người nhận lệnh.”\n\n"
            "“Còn ngươi?” — hắn hỏi.\n\n"
            "Ta nhìn xuống tay mình. Không có gì trong tay.\n\n"
            "“Ta không có lệnh,” — ta nói. — “Nhưng ta có linh căn.”\n\n"
            "Hàn Lập gật đầu. Rồi hắn nói thêm, hơi khó khăn: “Nếu ngươi tới Hoàng Phong Cốc, hỏi "
            "người tên Hàn Lập. Có thể có, có thể không.”\n\n"
            "Hắn nói như thể đang tự cho phép mình nói câu ấy."
        )},
    ])

    # c2_c18 — khe đá, "vì sao ngươi giúp ta?". Đây là chỗ hắn mở lòng; hảo cảm
    # thấp thì hắn không mở.
    dat_bien_the(tim(ds, "c2_c18"), HL, [
        {"muc": "tử địch", "ke": (
            "Chúng ta ngồi im rất lâu. Bên ngoài, tiếng bước chân đã xa hẳn.\n\n"
            "“Hàn Lập.”\n\n"
            "Hắn không đáp.\n\n"
            "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta bốn ngày.”\n\n"
            "“Ta không giúp ngươi.” — Hắn nói, mắt vẫn nhìn ra cửa khe. — “Ta giúp ta. Ngươi ở "
            "cạnh ta thì ngươi là thứ người ta nhìn thấy trước khi thấy ta.”\n\n"
            "Ta im.\n\n"
            "“Đừng nghĩ nhiều,” — hắn nói. — “Sáng mai ai đi đường nấy.”\n\n"
            "Hắn không kể gì cho ta. Ta cũng không kể gì cho hắn. Hai người ngồi trong một cái "
            "hốc đá, cách nhau một gang tay, và cách nhau xa hơn thế."
        )},
        {"muc": "thù địch", "ke": (
            "Chúng ta ngồi im rất lâu. Bên ngoài, tiếng bước chân đã xa hẳn.\n\n"
            "“Hàn Lập.”\n\n"
            "“Ừ.”\n\n"
            "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta bốn ngày.”\n\n"
            "Hắn im lâu đến mức ta tưởng hắn không trả lời.\n\n"
            "“Vì ngươi ở đây.” — Hắn nói, giọng đều. — “Ta không giúp ngươi. Ta chỉ không đẩy "
            "ngươi ra ngoài.”\n\n"
            "“Đó là cùng một việc.”\n\n"
            "“Không.” — Hắn quay sang. — “Cùng một việc với người ta tin. Khác với người ta chưa "
            "tin.”\n\n"
            "Hắn nhìn ta một lúc, rồi quay đi.\n\n"
            "Ta hiểu: bốn ngày vừa rồi chưa đủ. Có lẽ chưa bao giờ đủ."
        )},
        {"muc": "người dưng", "ke": (
            "Chúng ta ngồi im rất lâu. Bên ngoài, tiếng bước chân đã xa hẳn.\n\n"
            "“Hàn Lập.”\n\n"
            "“Ừ.”\n\n"
            "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta bốn ngày.”\n\n"
            "Hắn im lâu đến mức ta tưởng hắn không trả lời.\n\n"
            "“Vì ngươi không hỏi ta có gì.” — Hắn nói, giọng đều. — “Ở đây ai cũng hỏi ta có gì.”\n\n"
            "“Ta cũng muốn biết ngươi có gì.”\n\n"
            "“Nhưng ngươi không hỏi.” — Hắn nhún vai. — “Thế thôi. Đừng nghĩ nó to hơn nó là.”\n\n"
            "Ta nhìn hắn trong ánh sáng mờ. Hắn nhìn ra cửa khe.\n\n"
            "“Ta có một chuyện phải nói,” — ta nói.\n\n"
            "“Đừng nói.” — Hắn không quay lại. — “Đêm nay nói gì cũng thành lời thề. Mai hẵng nói.”"
        )},
        {"muc": "quen biết", "ke": (
            "Chúng ta ngồi im rất lâu. Bên ngoài, tiếng bước chân đã xa hẳn.\n\n"
            "“Hàn Lập.”\n\n"
            "“Ừ.”\n\n"
            "“Vì sao ngươi giúp ta?” — ta hỏi. — “Ngươi mới biết ta bốn ngày.”\n\n"
            "Hắn im lâu đến mức ta tưởng hắn không trả lời.\n\n"
            "“Vì ngươi là người duy nhất ở đây không hỏi ta có gì.” — Hắn nói, giọng đều. — “Ở "
            "Thất Huyền Môn, ai cũng hỏi ta có gì. Ở đây, ai cũng hỏi ta có gì. Ngươi thì không.”\n\n"
            "“Ta cũng muốn biết ngươi có gì.”\n\n"
            "“Nhưng ngươi không hỏi.” — Hắn quay sang. — “Đó là khác biệt.”\n\n"
            "Ta nhìn hắn. Hắn nhìn ta. Rồi hắn quay đi trước, như thể câu vừa rồi đã là nhiều hơn "
            "hắn định nói.\n\n"
            "“Ta có một chuyện,” — ta nói.\n\n"
            "“Nói đi.” — Hắn ngừng. — “Nhưng nếu là chuyện ngươi chưa từng nói với ai, thì đừng "
            "nói đêm nay. Đêm nay ta không chắc ta giữ được.”"
        )},
    ])

    # c2_c19 — sáng hôm sau, Hàn Lập bày kế. Hảo cảm thấp thì hắn bày kế một mình.
    dat_bien_the(tim(ds, "c2_c19"), HL, [
        {"muc": "tử địch", "ke": (
            "Trời sáng. Chúng ta ra khỏi khe đá.\n\n"
            "Ba kẻ ấy không tìm thấy chúng ta. Nhưng họ vẫn ở đây, và hội còn hai ngày.\n\n"
            "Hàn Lập ăn bánh khô một mình, ở đầu kia dãy hàng. Ta tới gần thì hắn đứng dậy.\n\n"
            "“Ta đi trước,” — hắn nói. — “Ngươi đừng đi sau ta.”\n\n"
            "“Vì sao?”\n\n"
            "“Vì người ta đang tìm một kẻ đi cùng một kẻ khác. Hai người đi riêng thì chỉ có một "
            "người bị tìm.” — Hắn nhét phần bánh còn lại vào vạt áo. — “Ta không muốn là người "
            "đó. Chắc ngươi cũng vậy.”\n\n"
            "Hắn đi về phía nam. Ta đi về phía bắc.\n\n"
            "Kế nghi binh ấy ta phải tự nghĩ ra, một mình, vào buổi trưa."
        )},
        {"muc": "thù địch", "ke": (
            "Trời sáng. Chúng ta ra khỏi khe đá.\n\n"
            "Ba kẻ ấy không tìm thấy chúng ta. Nhưng họ vẫn ở đây, và hội còn hai ngày.\n\n"
            "“Ta có một ý,” — Hàn Lập nói, khi chúng ta đang ăn mấy cái bánh khô. — “Kẻ tìm ngươi "
            "là kẻ muốn thứ trong áo ngươi. Nhưng họ không biết mặt ngươi.”\n\n"
            "“Sao ngươi biết?”\n\n"
            "“Vì đêm qua họ chạm vào chăn và nói ‘không phải hắn’.” — Hắn nhìn ta. — “Họ chỉ biết "
            "ngươi ngủ ở đâu.”\n\n"
            "Ta hiểu ra. “Vậy ta chỉ cần đổi chỗ ngủ.”\n\n"
            "“Không.” — Hắn lắc đầu. — “Không phải việc của ta. Ta chỉ nói cho ngươi biết ngươi "
            "đang bị tìm thế nào. Phần còn lại ngươi tự lo.”\n\n"
            "Hắn đứng dậy, phủi vụn bánh trên tay, và đi.\n\n"
            "Ta ngồi lại một mình với cái bánh khô thứ hai và một kế hoạch phải tự nghĩ ra."
        )},
        {"muc": "người dưng", "ke": (
            "Trời sáng. Chúng ta ra khỏi khe đá.\n\n"
            "Ba kẻ ấy không tìm thấy chúng ta. Nhưng họ vẫn ở đây, và hội còn hai ngày.\n\n"
            "“Ta có một ý,” — Hàn Lập nói, khi chúng ta đang ăn mấy cái bánh khô mua ở quầy đầu "
            "chợ. — “Kẻ tìm ngươi là kẻ muốn thứ trong áo ngươi. Nhưng họ không biết mặt ngươi.”\n\n"
            "“Sao ngươi biết?”\n\n"
            "“Vì đêm qua họ chạm vào chăn và nói ‘không phải hắn’.” — Hắn nhìn ta. — “Họ chỉ biết "
            "ngươi ngủ ở đâu. Không biết ngươi là ai.”\n\n"
            "Ta hiểu ra. “Vậy ta chỉ cần đổi chỗ ngủ.”\n\n"
            "“Không.” — Hắn lắc đầu. — “Ngươi cần làm cho họ tưởng ngươi đã đi.”\n\n"
            "Hắn nói đến đó thì dừng, như đã nói hết phần của mình.\n\n"
            "Ta nghĩ một lúc. Rồi ta nghĩ ra.\n\n"
            "Ta nói ra kế. Hàn Lập nghe, gật đầu một cái — không cười, không khen. “Được. Ngươi "
            "làm phần ngươi, ta làm phần ta.”"
        )},
        {"muc": "quen biết", "ke": (
            "Trời sáng. Chúng ta ra khỏi khe đá.\n\n"
            "Ba kẻ ấy không tìm thấy chúng ta. Nhưng họ vẫn ở đây, và hội còn hai ngày.\n\n"
            "“Ta có một ý,” — Hàn Lập nói, khi chúng ta đang ăn mấy cái bánh khô mua ở quầy đầu "
            "chợ. — “Kẻ tìm ngươi là kẻ muốn thứ trong áo ngươi. Nhưng họ không biết mặt ngươi.”\n\n"
            "“Sao ngươi biết?”\n\n"
            "“Vì đêm qua họ chạm vào chăn và nói ‘không phải hắn’.” — Hắn nhìn ta. — “Họ chỉ biết "
            "ngươi ngủ ở đâu. Không biết ngươi là ai.”\n\n"
            "Ta hiểu ra. “Vậy ta chỉ cần đổi chỗ ngủ.”\n\n"
            "“Không.” — Hắn lắc đầu. — “Ngươi cần làm cho họ tưởng ngươi đã đi.”\n\n"
            "Ta nghĩ một lúc. Rồi ta nghĩ ra.\n\n"
            "“Ta cần một người rời khỏi hội,” — ta nói — “và đi về hướng bắc. Mang theo một cái "
            "túi.”\n\n"
            "Hàn Lập nhìn ta. Rồi khóe miệng hắn động, rất nhẹ.\n\n"
            "“Ngươi bắt đầu nghĩ như người ở đây rồi đấy.” — Hắn đứng dậy. — “Nhưng người mang "
            "túi không phải ngươi. Là ta.”"
        )},
    ])

    # --------------------------------------- 1b. lựa chọn làm GIẢM hảo cảm
    # Không có mấy lựa chọn này thì mức thù địch không bao giờ với tới được: mọi
    # lựa chọn cũ đều +5…+25, nên "hảo cảm thấp" chỉ là chuyện lý thuyết.

    them_lua_chon(tim(ds, "c2_d06"), {
        "chu": "Quay đi, để hắn tự chịu một mình",
        "den": "c2_d07",
        "hieu_ung": {"hao_cam": {HL: -12}, "co_su_kien": ["bo_mac_han_lap_o_mac_phu"]},
    })

    them_lua_chon(tim(ds, "c2_c09"), {
        "chu": "Đứng nhìn, để hắn tự trả giá",
        "den": "c2_c10",
        "hieu_ung": {"hao_cam": {HL: -10}, "co_su_kien": ["de_han_lap_bi_tra_gia"]},
    })

    them_lua_chon(tim(ds, "c2_c18"), {
        "chu": "“Ta không cần ngươi hiểu ta.”",
        "den": "c2_c19",
        "hieu_ung": {"hao_cam": {HL: -15}, "co_su_kien": ["cai_nhau_voi_han_lap"]},
    })

    # Đường "đứng nhìn" và "giấu chuyện" là đường lạnh nhạt — phải ra hảo cảm
    # thấp, nếu không thì mức thù địch vẫn chỉ là chuyện lý thuyết.
    for lc in tim(ds, "c2_c04b").get("lua_chon") or []:
        if lc.get("den") == "c2_c05":
            lc["hieu_ung"] = {"hao_cam": {HL: -8},
                              "co_su_kien": ["dung_nhin_de_han_lap_tu_quyet"]}
    them_lua_chon(tim(ds, "c2_c06b"), {
        "chu": "Đi theo hắn, và vẫn không nói",
        "den": "c2_c07",
        "hieu_ung": {"hao_cam": {HL: -10}, "co_su_kien": ["giu_bi_mat_voi_han_lap"]},
    })

    # c2_c04b — đứng nhìn Hàn Lập tự xử ở chợ. Đây là đường lạnh nhạt: hắn không
    # đưa mảnh ngọc cho ta.
    _c04b_goc = (
        "Ta đứng nhìn.\n\n"
        "Hàn Lập cầm mảnh ngọc lên, nhìn nó một lúc, rồi đặt xuống.\n\n"
        "“Không bán.”\n\n"
        "Gã áo gấm nhướng mày. “Hai viên là giá tốt cho kẻ như ngươi.”\n\n"
        "“Ta biết.” — Hàn Lập nói, giọng đều — “Nhưng ta không biết nó là gì. Và ta không bán "
        "thứ ta không biết giá.”\n\n"
        "Gã nhìn hắn một lúc, rồi nhún vai bỏ đi. “Tuỳ. Đến mai ta vẫn ở đây.”\n\n"
    )
    dat_bien_the(tim(ds, "c2_c04b"), HL, [
        {"muc": "quen biết", "ke": _c04b_goc + (
            "Khi gã đi khuất, Hàn Lập mới quay sang ta — không ngạc nhiên, như thể hắn biết ta "
            "đứng đó từ đầu.\n\n"
            "“Ngươi đứng nhìn nãy giờ.”\n\n"
            "“Ta muốn xem ngươi làm gì.”\n\n"
            "“Và ngươi thấy gì?”\n\n"
            "“Ta thấy một kẻ không bán thứ mình không hiểu.” — Ta ngồi xuống cạnh hắn. — “Đó là "
            "điều tốt. Nhưng ngươi vẫn chưa biết nó là gì.”\n\n"
            "Hắn im một lúc. Rồi hắn đưa mảnh ngọc cho ta.\n\n"
            "“Vậy thì cùng tìm hiểu.”"
        )},
        {"muc": "người dưng", "ke": _c04b_goc + (
            "Khi gã đi khuất, Hàn Lập mới quay sang ta.\n\n"
            "“Ngươi đứng nhìn nãy giờ.”\n\n"
            "“Ta muốn xem ngươi làm gì.”\n\n"
            "“Và ngươi thấy gì?”\n\n"
            "Ta định nói. Rồi ta thấy hắn cất mảnh ngọc vào vạt áo — không đưa cho ta, không giải "
            "thích. Động tác ấy khép lại mọi câu ta định nói.\n\n"
            "“Thấy một kẻ không bán thứ mình không hiểu,” — ta nói. — “Thế thôi.”\n\n"
            "“Ừ.” — Hắn gật đầu. — “Thế thôi.”"
        )},
        {"muc": "thù địch", "ke": _c04b_goc + (
            "Khi gã đi khuất, Hàn Lập thu mảnh ngọc, rồi đi thẳng — không nhìn ta, không gọi.\n\n"
            "Ta đi theo một quãng. Hắn dừng lại, không quay lưng, và nói: “Ngươi đi đường ngươi đi.”\n\n"
            "“Ta chỉ đi cùng chiều.”\n\n"
            "“Thì đổi chiều.”"
        )},
        {"muc": "tử địch", "ke": _c04b_goc + (
            "Hàn Lập đứng dậy. Khi ngang qua ta, hắn nói một câu, không dừng bước: “Ngươi đứng đó "
            "nãy giờ. Ngươi thấy đủ rồi chứ.”\n\n"
            "Rồi hắn đi, và ta mất một lúc mới hiểu: hắn không hỏi ta thấy gì. Hắn chỉ muốn ta đi."
        )},
    ])

    # c2_c06b — giấu chuyện. Hảo cảm thấp thì hắn không "đợi đến lúc ngươi nói".
    dat_bien_the(tim(ds, "c2_c06b"), HL, [
        {"muc": "thù địch", "ke": (
            "Ta đặt cuốn sách xuống.\n\n"
            "“Ta không đọc được.”\n\n"
            "Đó là lần đầu ta nói dối hắn. Câu dối trôi ra khỏi miệng ta dễ đến mức chính ta cũng "
            "thấy lạnh.\n\n"
            "Hàn Lập nhìn ta một lúc. Hắn không nói gì.\n\n"
            "“Được,” — hắn nói cuối cùng, và cất sách đi. — “Ta tự tìm cách đọc.”\n\n"
            "Hắn đứng dậy, phủi đất trên vạt áo. “Mai ta đi tìm chỗ nghỉ. Ngươi tự lo chỗ của ngươi.”\n\n"
            "Hắn đi về phía tây thung lũng. Ta đi phía sau, cách hắn chừng mười bước — đủ gần để "
            "không lạc, đủ xa để hắn không phải quay lại.\n\n"
            "*Ta sẽ nói với hắn,* ta tự nhủ. *Chỉ là chưa phải lúc.*\n\n"
            "Nhưng trong lòng ta có một chỗ lạnh, biết rằng cái “chưa phải lúc” ấy rất dễ kéo dài "
            "thành “không bao giờ”."
        )},
        {"muc": "tử địch", "ke": (
            "Ta đặt cuốn sách xuống.\n\n"
            "“Ta không đọc được.”\n\n"
            "Đó là lần đầu ta nói dối hắn. Câu dối trôi ra khỏi miệng ta dễ đến mức chính ta cũng "
            "thấy lạnh.\n\n"
            "Hàn Lập nhìn ta một lúc. Hắn không nói gì.\n\n"
            "Rồi hắn cất sách đi, đứng dậy, và nói đúng một câu: “Ta biết ngươi nói dối.”\n\n"
            "“Hàn Lập—”\n\n"
            "“Không cần.” — Hắn xách túi lên. — “Ngươi giữ bí mật của ngươi. Ta giữ của ta. Từ giờ "
            "khỏi phải giả vờ.”\n\n"
            "Hắn đi. Lần này hắn không hỏi ta có đi cùng không. Và ta — ta cũng không biết mình có "
            "nên đi theo hay không nữa."
        )},
    ])

    # ------------------------------------------------- 2. lựa chọn khoá theo hảo cảm
    # Chỉ mở khi đã thân. Khoá thì vẫn HIỆN kèm lý do — người chơi thấy mình bỏ lỡ gì.

    them_lua_chon(tim(ds, "c2_p02"), {
        "chu": "“Vì ta cũng từng mất một người thầy.”",
        "den": "c2_p03",
        "dieu_kien": {"hao_cam": {HL: 20}},
        "ly_do_khoa": "Cần Hàn Lập ở mức quen biết trở lên mới dám nói câu này",
        "hieu_ung": {"hao_cam": {HL: 6}},
    })

    them_lua_chon(tim(ds, "c2_c18"), {
        "chu": "“Ta sẽ không để ngươi chết một mình.”",
        "den": "c2_c19",
        "dieu_kien": {"hao_cam": {HL: 50}},
        "ly_do_khoa": "Cần Hàn Lập ở mức thân thiết trở lên",
        "hieu_ung": {"hao_cam": {HL: 10}, "co_su_kien": ["hua_khong_bo_han_lap"]},
    })

    them_lua_chon(tim(ds, "c2_c25"), {
        "chu": "Đưa lại một tấm Thăng Tiên Lệnh",
        "den": "c2_c26",
        "dieu_kien": {"hao_cam": {HL: 70}, "co_vat": "Thăng Tiên Lệnh"},
        "ly_do_khoa": "Cần Hàn Lập ở mức thân thiết trở lên và có Thăng Tiên Lệnh trong túi",
        "hieu_ung": {"co_su_kien": ["tang_lai_thang_tien_lenh"]},
    })

    # ---------------------------------------------------------- 3. nhánh hậu quả
    # Hảo cảm thấp: Hàn Lập KHÔNG che cho ta ở khe đá. Ta chạy một mình và tới chỗ
    # khác hẳn, chứ không có kết "cùng nhau ra khỏi cốc".

    if "c2_c24c_xau" not in ds:
        idx = next(i for i, x in enumerate(d["doan"]) if x["id"] == "c2_c24c2") + 1
        d["doan"].insert(idx, {
            "id": "c2_c24c_xau",
            "hoi": "Kết",
            "boi_canh": "Trong hốc đá — đêm, và không có ai quay lại",
            "ke": (
                "Ta nằm im trong hốc đá và nghe tiếng bước chân dừng lại ngay cửa.\n\n"
                "Ta chờ tiếng hắn. Ta chờ một câu gì đó — dù chỉ một tiếng động nhỏ cũng đủ "
                "cho ta biết hắn vẫn ở đó.\n\n"
                "Không có gì cả.\n\n"
                "“Ra đi,” — giọng trung niên nói, lần này gần hơn. — “Ta biết có người.”\n\n"
                "Ta hiểu ra, và cái hiểu ấy lạnh hơn cả đêm núi: bốn ngày vừa rồi, ta đã tiêu hết "
                "vào những lựa chọn không để lại gì. Không ai quay lại vì một kẻ chưa từng ở lại.\n\n"
                "Ta bò ra bằng cửa sau của hốc — khe hở hẹp đến mức đá cào rách cả vai áo. Ta "
                "không dám thở. Ta không dám nhìn lại.\n\n"
                "Phía sau, có tiếng ai đó nói, rồi tiếng bước chân bỏ đi — không phải đuổi theo "
                "ta. Đuổi theo một kẻ khác.\n\n"
                "Ta đi suốt đêm về phía bắc. Khi trời sáng, ta ra khỏi thung lũng bằng một con "
                "đường mòn mà ta tìm thấy một mình.\n\n"
                "Trong tay ta không có tấm lệnh nào. Trong túi ta không có ai tên Hàn Lập."
            ),
            "lua_chon": [{
                "chu": "Đi về phía bắc, không nhìn lại",
                "den": "c2_c26_xau",
            }],
        })

    if "c2_c26_xau" not in ds:
        idx = next(i for i, x in enumerate(d["doan"]) if x["id"] == "c2_c26") + 1
        d["doan"].insert(idx, {
            "id": "c2_c26_xau",
            "hoi": "Kết",
            "boi_canh": "Chân núi — gần sáng, một mình",
            "ke": (
                "Trời sáng khi ta ra tới chân núi.\n\n"
                "Thái Nam Cốc ở phía sau, im. Một cái chợ của mấy trăm người, và trong một đêm "
                "nó thành một cái thung lũng trống.\n\n"
                "Ta ngồi xuống bên một tảng đá. Không có ai ngồi cạnh. Không có bình nhỏ màu "
                "xanh nào được rút ra, không có câu hỏi nào về bí mật của ta.\n\n"
                "Sáu ngày. Ta học được linh thạch là gì, Thăng Tiên Lệnh là gì, và người ta giết "
                "nhau vì cái gì. Ta cũng học được một điều mà không ai nói cho ta: ở đây, người "
                "ta chỉ chết thay cho kẻ họ thật sự coi là người của mình.\n\n"
                "Ta đứng dậy. Ta có linh căn mạnh — mạnh đến mức một bà lão phải sợ. Ta có một "
                "thứ trong vạt áo mà cả cái hội này sẽ giết để có.\n\n"
                "Ta đi về phía bắc, một mình. Và ta không nhìn lại."
            ),
            "lua_chon": [{"chu": "Khép lại Chương 2", "den": "__ket_thuc__"}],
        })

    # c2_c24c: ở lại trong khe. Hàn Lập quay lại cứu — nhưng chỉ khi hắn đủ thân.
    # Hảo cảm thấp thì hắn quay lại chỗ hắn ngủ và để ta tự lo, đúng như biến thể
    # c2_c15/c2_c19 đã nói ("ta không gánh nổi ngươi").
    c24c = tim(ds, "c2_c24c")
    for lc in c24c.get("lua_chon") or []:
        if lc.get("den") == "c2_c24c2":
            lc["dieu_kien"] = {"hao_cam": {HL: 40}}
            lc["ly_do_khoa"] = ("Hàn Lập phải ở mức quen biết cao trở lên mới quay lại "
                                "chắn cho ngươi")
    them_lua_chon(c24c, {
        "chu": "Nằm im, và biết hắn sẽ không quay lại",
        "den": "c2_c24c_xau",
    })

    P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Xong. Đoạn:", len(d["doan"]))
    print("Số đoạn có bien_the:",
          sum(1 for x in d["doan"] if x.get("bien_the")))
    print("Số lựa chọn khoá theo hảo cảm:",
          sum(1 for x in d["doan"] for l in (x.get("lua_chon") or [])
              if "hao_cam" in ((l.get("dieu_kien") or {}))))


if __name__ == "__main__":
    main()
