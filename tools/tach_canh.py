"""Tách mỗi lựa chọn thành một cảnh riêng.

Với mỗi cặp lựa chọn cùng trỏ về một đoạn, chèn một đoạn mới ngay sau đoạn nguồn:
lựa chọn trỏ vào đoạn mới, đoạn mới kể cảnh riêng rồi mới nối vào đoạn chung.

Chạy: python3 tools/tach_canh.py <chuong> [--ghi]
"""
import io
import json
import sys

GOC = "/workspace/project"
sys.path.insert(0, GOC + "/tools")

# (id đoạn nguồn, chỉ số lựa chọn) -> (văn bản cảnh riêng, chữ trên nút tiếp)
CANH: dict = {}


def them(nguon, chi_so, van_ban, nut):
    CANH[(nguon, chi_so)] = (van_ban.strip(), nut)


# --------------------------------------------------------------- chương 1
them("c1_d05", 0,
     """
Ta bật ngửa ra sau, lưng đập vào cột miếu. Bụi rơi lả tả từ xà nhà xuống vai ta.

“Ngươi là ai?” — ta hỏi, giọng vỡ ra như có ai bóp nghẹn cổ họng. “Sao lại nói trong đầu ta?”

Không ai đáp. Trong miếu chỉ có hai thanh kiếm nằm trên nền đá, lưỡi sáng lên dưới ánh trăng chéo qua mái rách.

Rồi một tiếng cười khẽ. Không vui, không ác — như tiếng đá lạnh cạ vào đá lạnh.

“Ngươi lùi lại,” — giọng ấy nói. — “Nhưng tay ngươi vẫn còn trên nắp hộp. Kẻ sợ thì không làm vậy.”

Ta nhìn xuống. Đúng thế thật. Tay ta vẫn đặt trên thành hộp, như có thứ gì khác đã giữ tay ta lại.
""",
     "Nghe tiếng nói ấy")

them("c1_d05", 1,
     """
Ta không lùi, cũng không đáp. Ta đứng nguyên tại chỗ, hai tay buông, mắt không rời hai lưỡi kiếm.

Trong miếu im đến mức ta nghe được tiếng máu mình chạy trong tai. Một hạt bụi rơi từ xà nhà, chạm xuống nắp hộp, kêu một tiếng khẽ đến mức không đáng kể.

Ta chờ. Ta đã học được cách chờ — chờ qua đêm, chờ người ta khinh rẻ, chờ cho cơn đau dịu xuống.

“Ngươi không sợ,” — giọng ấy lên tiếng, và lần này nó chậm hơn, như đã quyết định. — “Bọn chúng lùi lại, hoặc bỏ chạy. Ngươi đứng im.”

Một lưỡi kiếm khẽ nhích trên nền đá. Không phải ta làm. Ta vẫn không nhúc nhích.
""",
     "Nghe tiếng nói ấy")

them("c1_d15", 0,
     """
Ta không cười, không đánh lưng. Ta nhìn thẳng vào hắn và nói thật — không phải nửa sự thật, mà là tất cả.

“Ta biết tương lai của ngươi.”

Gió ngừng. Hắn không đổi sắc mặt, nhưng bàn tay phải khẽ dừng lại.

“Ngươi biết gì?”

“Ta biết ngươi sẽ đứng trên đỉnh của thế gian này.” — ta nói. — “Ta biết ngươi sẽ mất rất nhiều thứ trước khi tới được đó. Và ta biết, trong tất cả những kẻ ở đây, chỉ có ngươi là còn sống khi những người này đã chết.”

Lần này hắn nhìn ta lâu hơn. Trong mắt hắn có thứ gì đó lạnh hơn cả sự khinh ngạc.
""",
     "Nghe hắn nói tiếp")

them("c1_d15", 1,
     """
Ta bật cười. Một nụ cười nhẹ, không tới mắt — thứ cười ta đã tập đủ nhiều lần để không ai thấy ta đang sợ.

“Ta chỉ là kẻ tình cờ ở đây.” — ta nói, giọng nhẹ như không có gì. — “Đi ngang thì lạc đường, đứng lại thì nghe chuyện. Chỉ thế thôi.”

Hắn nhìn ta. Không đáp. Ánh mắt ấy không đổi, nhưng ta biết hắn không tin một chữ nào trong câu ta vừa nói.

“Tình cờ,” — hắn nhắc lại, chậm rãi. — “Tình cờ thì không đứng đây nghe người ta nói chuyện.”

Ta không đáp được. Hắn đã bắt đúng chỗ ta không nói.
""",
     "Nghe hắn nói tiếp")

them("c1_d15", 2,
     """
Ta không trả lời. Ta hỏi ngược.

“Vậy ngươi là ai?” — ta nói. — “Ngươi biết ta đang giấu thứ gì, còn ta thì chỉ biết ngươi là đệ tử Thất Huyền Môn. Thế thì không công bằng.”

Hắn khẽ nhích mày. Lần đầu tiên, có gì đó trong mắt hắn đổi — không phải giận, mà như một thứ ta không ngờ tới.

“Ngươi không sợ người,” — hắn nói. — “Người ở đây không hỏi thẳng như thế.”

Rồi hắn im. Và trong cái im ấy, ta nghe rõ hơn tiếng áo hắn sột soạt qua lớp vải mỏng.
""",
     "Nghe hắn nói tiếp")

them("c1_d15", 3,
     """
Ta không nói. Ta không biết phải nói gì.

Thay vào đó, ta tháo cái bầu nước ở thắt lưng ra, đưa tới trước mặt hắn. Bầu bằng gốm, đậy nắp, còn ấm. Ta đã hứng nó từ sáng, chưa uống ngụm nào.

Hắn nhìn cái bầu, rồi nhìn ta. Một lúc lâu.

Rồi hắn cầm lấy. Hắn uống — không vội, mà từng ngụm một, như người ta uống thứ quý giá.

“Ngươi không sợ người,” — hắn nói, giọng khàn hơn trước. Rồi hắn đưa bầu lại, và im.
""",
     "Nghe hắn nói tiếp")

them("c1_d16", 0,
     """
Ta đứng dậy, phủi bụi trên vạt áo.

“Vậy hẹn gặp lại khi ngươi mạnh hơn.” — ta nói.

Hắn ngước lên nhìn ta. Lần đầu tiên trong mắt hắn có gì đó không phải lạnh.

“Ngươi chắc?” — hắn hỏi.

“Chắc.” — ta đáp. — “Ta sẽ còn ở đây khi ngươi quay lại.”

Hắn không cười, không gật, chỉ nhìn ta một lúc rồi cúi xuống tiếp tục lau vết máu. Ta quay đi. Đêm còn lại phía sau.
""",
     "Rời hậu sơn")

them("c1_d16", 1,
     """
Ta không nói gì. Ta gật đầu, một cái gật nhẹ, rồi quay đi.

Sau lưng, ta nghe tiếng hắn dừng tay lại — một nhịp, rồi tiếp tục. Hắn không gọi ta lại.

Ta đi dọc theo bức tường hậu sơn, tay sờ vào vách đá lạnh. Trong đêm ấy, ta đã học được một điều: có những người không cần lời hứa, họ chỉ cần người khác đứng đây.
""",
     "Rời hậu sơn")

them("c1_p07", 0,
     """
Ta lùi lại một bước, lưng chạm vào vách gỗ.

“Ngươi… ngươi là ai? Sao lại ở trong khối ngọc này?”

Nàng không bước ra khỏi khối ngọc, chỉ nghiêng đầu nhìn ta. Đôi mắt nàng sáng như sao, nhưng sâu hun hút như vực thẳm.

“Ngươi hỏi ta trước à.” — Nàng khẽ cười, một nụ cười không ấm. — “Kẻ lạc vào đây thường sợ đến mức không hỏi được gì.”
""",
     "Nghe nàng nói")

them("c1_p07", 1,
     """
Ta không lùi, cũng không hỏi. Ta ngồi im, khối ngọc trên lòng bàn tay, mắt không rời bóng người trong ấy.

Nàng cũng không nói. Hai bên im, và trong cái im ấy, khối ngọc sáng lên nhấp nháy như có mạch đập.

Rồi nàng nghiêng đầu.

“Ngươi không sợ người,” — nàng nói, giọng như rót mật. — “Ta đợi ngươi hỏi, mà ngươi ngồi im. Người ta thường thấy lạ thì hỏi trước.”

“Ta không biết phải hỏi gì.” — ta nói thật.

“Vậy thì để ta mở lời.” — Nàng nhìn ta, mắt sáng lên. — “Ngươi có biết mình đang cầm thứ gì trong tay không?”
""",
     "Nghe nàng nói")

# Các cụm cảnh chương 2 nằm ở tools/canh_c2_*.py
for _ten in ("canh_c2_1", "canh_c2_2", "canh_c2_3", "canh_c2_4"):
    _m = __import__(_ten)
    CANH.update(_m.CANH)

# Mở đầu c1_p08 vốn là hành động của lựa chọn [0], nên phải đổi cho trung tính.
SUA_MO_DAU = {
    "c1_p08": (
        """Ta lùi lại một bước, lưng chạm vào vách gỗ. “Ngươi… ngươi là ai? Sao lại ở trong khối ngọc này?”

Nàng không bước ra khỏi khối ngọc, chỉ nghiêng đầu nhìn ta. Đôi mắt nàng sáng như sao, nhưng sâu hun hút như vực thẳm.

“Ta hỏi ngươi trước — ngươi là ai?” — nàng nói, rồi khẽ nhíu mày,""",
        """“Trước hết — ngươi là ai?” — nàng nói, rồi khẽ nhíu mày,""",
    ),
}


def main():
    so = int(sys.argv[1])
    ghi = "--ghi" in sys.argv
    p = f"{GOC}/game/chapters/chuong{so}.json"
    ch = json.loads(io.open(p, encoding="utf-8").read())
    D = {x["id"]: x for x in ch["doan"]}

    for did, (cu, moi) in SUA_MO_DAU.items():
        if did in D and cu in D[did]["ke"]:
            D[did]["ke"] = D[did]["ke"].replace(cu, moi, 1)
            print(f"  sua mo dau {did}")

    moi_doan = []
    for (src_id, i), (van_ban, nut) in sorted(CANH.items()):
        if src_id not in D:
            continue
        src = D[src_id]
        lc = src["lua_chon"][i]
        den = lc["den"]
        new_id = f"{den}_{i}"
        if new_id in D:
            print(f"  bo qua (da co): {new_id}")
            continue
        d = {
            "id": new_id,
            "hoi": src.get("hoi"),
            "boi_canh": src.get("boi_canh"),
            "ke": van_ban,
            "lua_chon": [{"chu": nut, "den": den}],
        }
        anh = D[den].get("hinh_anh") or src.get("hinh_anh")
        if anh:
            d["hinh_anh"] = anh
        moi_doan.append((src_id, d))
        lc["den"] = new_id
        print(f"  {src_id}[{i}] -> {new_id} -> {den}")

    for src_id, d in moi_doan:
        vi_tri = next(k for k, x in enumerate(ch["doan"]) if x["id"] == src_id)
        ch["doan"].insert(vi_tri + 1, d)

    print(f"chuong{so}: {len(ch['doan'])} doan ({len(moi_doan)} moi)")
    if ghi:
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(ch, ensure_ascii=False, indent=2) + "\n")
        print("da ghi", p)
    else:
        print("(chay lai voi --ghi de ghi)")


if __name__ == "__main__":
    main()
