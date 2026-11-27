"""Sinh sơ đồ cốt truyện hai nhánh xuất thân — docs/nhap/so-do-cot-truyen.html

Đọc thẳng từ game/chapters/chuong1.json và chuong2.json nên sơ đồ không lệch game.
Mỗi bước là một hành động: đoạn truyện + các lựa chọn dẫn đi đâu.
Bấm một bước để mở nguyên văn đoạn đó.
"""

from __future__ import annotations

import html
import json
import os
import re

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "docs", "nhap", "so-do-cot-truyen.html")

TEN_NHOM = {
    "tan_tu": "Tán tu",
    "mon_phai": "Môn phái",
}
MAU_NHOM = {"tan_tu": "a", "mon_phai": "b"}

# Nhãn hành động ngắn cho từng đoạn — sơ đồ cần đọc được trong một liếc.
# Đoạn không có ở đây thì cắt câu đầu của lời kể.
NHAN = {
    # --- Chương 1 · Tán tu ---
    "c1_d01": "Tỉnh dậy giữa chợ, thân xác ăn mày",
    "c1_d02": "Vào ngõ sau chợ, gặp đám ăn mày",
    "c1_d02b": "Ở lại trấn kiếm ăn",
    "c1_d03": "Lên núi, tới miếu hoang",
    "c1_d04": "Đứng ngoài quan sát miếu",
    "c1_d04b": "Trong miếu có người — quay phắt lại",
    "c1_d04c": "Đỗ Tam chắn cửa, đòi cái hộp",
    "c1_d04d": "Xông ra giành hộp",
    "c1_d05": "Mở hộp: hai thanh kiếm, kiếm linh tỉnh",
    "c1_d06": "Kiếm linh nói chuyện, đòi khế ước",
    "c1_d06b": "Nghe rõ thân phận kiếm linh",
    "c1_d07": "Nhận làm chủ kiếm linh",
    "c1_d07b": "Hỏi rõ điều kiện rồi nhận",
    "c1_d08": "Kiếm linh dạy kiếm đạo",
    "c1_d09": "Khổ luyện theo lời kiếm linh",
    "c1_d10": "Nắm thực lực mới",
    "c1_d11": "Dã Lang Bang đánh trấn — tù và vang",
    "c1_d12": "Xuống trấn cứu dân",
    "c1_d13": "Tới Thất Huyền Môn, chỗ trận chính",
    "c1_d14": "Bám theo một bóng người",
    "c1_d14b": "Về nơi trú lấy sức",
    "c1_d15": "Bóng người ấy là Hàn Lập",
    "c1_d16": "Nói chuyện với Hàn Lập",
    "c1_d17": "Chia tay, khép Chương 1",
    # --- Chương 1 · Môn phái ---
    "c1_p01": "Tỉnh dậy ở tân xá Thất Huyền Môn",
    "c1_p02": "Ra sân tập, hoà nhập sư huynh",
    "c1_p03": "Bị sư huynh chèn ép ở sân tập",
    "c1_p03b": "Nuốt nhục, luyện lại một mình",
    "c1_p03c": "Cãi lại, biết mình sẽ thua",
    "c1_p03d": "Thấy ánh sáng lạ dưới gốc cổ thụ",
    "c1_p03e": "Hoảng, chôn trả khối ngọc",
    "c1_p04": "Tới vườn thuốc của môn",
    "c1_p04a": "Hỏi Mạc Đại Phu chuyện lạ",
    "c1_p04b": "Im lặng phụ ông bó thuốc",
    "c1_p05": "Dò la tin Dã Lang Bang",
    "c1_p05b": "Ra khe núi sau hậu sơn",
    "c1_p05c": "Chôn trả khối ngọc ở khe núi",
    "c1_p06": "Đào khối ngọc Mạc Đại Phu giấu",
    "c1_p06b": "Chôn trả khối ngọc",
    "c1_p07": "Đêm: khối ngọc hiện ra Tuyết Cơ",
    "c1_p08": "Tuyết Cơ kể thân phận",
    "c1_p08b": "Nghe rõ điều kiện của nàng",
    "c1_p09": "Khế ước nô lệ: nàng dạy tu tiên",
    "c1_p09b": "Suy nghĩ kỹ trước khi ký",
    "c1_p09c": "Ký khế ước",
    "c1_p10": "Đêm song tu đầu tiên",
    "c1_p10b": "Tuyết Cơ hướng dẫn tu luyện",
    "c1_p11": "Khổ tu những đêm sau",
    "c1_p11b": "Đêm sau lại tiếp tục",
    "c1_p11c": "Tiếp tục khổ tu bằng sức mình",
    "c1_p12": "Nắm thực lực mới",
    "c1_p13": "Dã Lang Bang đánh — tù và vang",
    "c1_p14": "Xông ra cổng đông, gặp Hùng Bá",
    "c1_p14b": "Giấu thực lực, chỉ dùng võ phàm",
    "c1_p14c": "Dùng toàn lực ngọc cốt",
    "c1_p14d": "Vận Thất Huyền quyền phản kích",
    "c1_p14e": "Quát gọi Hùng Bá ra mặt",
    "c1_p15": "Chạy về phía tiếng kêu cứu",
    "c1_p16": "Nấp vào bóng tối chờ trận lắng",
    "c1_p16b": "Về tân xá lấy sức",
    "c1_p17": "Bám theo Hàn Lập ra hậu sơn",
    "c1_p18a": "Thú thật: biết tương lai hắn",
    "c1_p18b": "Cười trừ: chỉ là kẻ tình cờ",
    "c1_p18c": "Hỏi ngược: ngươi là ai",
    "c1_p18d": "Im lặng, đưa bầu nước",
    "c1_p19": "Chia tay, khép Chương 1",
    # --- Chương 2 · Tán tu ---
    "c2_d01": "Hàn Lập gọi dậy, đi theo hắn",
    "c2_d01b": "Ngồi thêm, nghĩ đã rồi đi",
    "c2_d02": "Đi về phía đông",
    "c2_d03": "Hỏi đường tới Gia Nguyên",
    "c2_d04": "Tìm ngõ Thanh Trúc",
    "c2_d05": "Theo Hàn Lập vào nhà",
    "c2_d06": "Đám tang Mạc Đại Phu",
    "c2_d07": "Kể chuyện trong tang lễ cho Hàn Lập",
    "c2_d08": "Hàn Lập kể chuyện Thái Nam",
    "c2_d08b": "Cảnh giác, nghe tiếp",
    "c2_d09": "Vạn Tiểu Sơn mời đi cùng",
    "c2_d10": "Sáng mai có mặt ở cổng đông",
    # --- Chương 2 · Môn phái ---
    "c2_p01": "Tỉnh dậy sau trận Dã Lang Bang",
    "c2_p01b": "Hỏi Tuyết Cơ cho rõ",
    "c2_p02": "Ra sân tập tan hoang",
    "c2_p03": "Hàn Lập rời đi, mình đi cùng không",
    "c2_p04": "Xuống núi",
    "c2_p05": "Hỏi đường lên Thái Nam",
    "c2_p06": "Xuống thung lũng",
    # --- Chương 2 · mạch chung ---
    "c2_c01": "Thấy người ta bay — tới Thái Nam",
    "c2_c02": "Xuống chợ tán tu",
    "c2_c02b": "Ngồi bên lề quan sát",
    "c2_c03": "Thấy Hàn Lập bán đồ, bị ép giá",
    "c2_c04a": "Bước vào phá ngang",
    "c2_c04b": "Đứng nhìn để hắn tự quyết",
    "c2_c05": "Cầm mảnh ngọc lên xem",
    "c2_c06a": "Nói cho Hàn Lập biết sách viết gì",
    "c2_c06b": "Giấu, chưa nói",
    "c2_c07": "Tìm Hàn Lập",
    "c2_c08": "Gặp ông lão bán nước",
    "c2_c08b": "Đi theo ông lão",
    "c2_c09": "Hàn Lập hỏi: vì sao giúp ta",
    "c2_c10": "Đi tới quầy sách",
    "c2_c11": "Hỏi gã bán sách về cuốn sách lạ",
    "c2_c12a": "Nhận nhiệm vụ của gã bán sách",
    "c2_c12b": "Mua sách cơ bản, bỏ qua",
    "c2_c13": "Bà lão đo linh căn",
    "c2_c14a": "Hỏi sao bà cất viên đá đi",
    "c2_c14b": "Im lặng chờ bà nói",
    "c2_c15": "Hàn Lập trả tiền thay mình",
    "c2_c16": "Đêm: có người tới khe đá",
    "c2_c17": "Chạy đi tìm Hàn Lập",
    "c2_c18": "Hàn Lập bị thương, nói chuyện",
    "c2_c19": "Bàn kế ra khỏi cốc",
    "c2_c20": "Hỏi: khi nào làm",
    "c2_c21": "Chuẩn bị cho ngày mai",
    "c2_c22": "Ngủ, chờ trời sáng",
    "c2_c23": "Ngày cuối: tà tu phong toả cốc",
    "c2_c24a": "Lên theo lối Hàn Lập",
    "c2_c24b": "Lên, nhưng không để họ chọn mình",
    "c2_c24c": "Không lên — nấp trong hốc đá",
    "c2_c24b2": "Đứng nhìn, không nói gì",
    "c2_c24b3": "“Ngươi vừa giết người.”",
    "c2_c24c2": "Hàn Lập quay lại đón",
    "c2_c24c_xau": "Hàn Lập không quay lại",
    "c2_c25": "Ra khỏi cốc cùng Hàn Lập",
    "c2_c25b": "Đỡ Hàn Lập bị thương ra khỏi cốc",
    "c2_c26": "Nhìn lại thung lũng lần cuối",
    "c2_c26_xau": "Ra khỏi cốc một mình",
}

# Ghi chú cho những chỗ rẽ quan trọng — lý do nên đọc kỹ khi đánh giá.
GHI_CHU = {
    "c1_d04c": "Chỗ chết đầu tiên: Đỗ Tam mạnh hơn gấp nhiều lần.",
    "c1_d07": "Đây là khế ước với kiếm linh — nhánh tán tu không có Tuyết Cơ.",
    "c1_p09": "Đây là khế ước nô lệ với Tuyết Cơ — nhánh môn phái không có kiếm linh.",
    "c1_p14": "Bốn lựa chọn, hai cái khoá sau điều kiện sự kiện.",
    "c2_c03": "Hai nhánh gặp lại nhau ở đây, sau 12–7 đoạn đi riêng.",
    "c2_c09": "Lựa chọn thứ ba mở khi hảo cảm Hàn Lập ≥ 20.",
    "c2_c13": "Đo linh căn: quyết định người chơi có thiên linh căn hay không.",
    "c2_c18": "Lựa chọn thứ ba mở khi hảo cảm Hàn Lập ≥ 50.",
    "c2_c23": "Ba lối rẽ lớn nhất chương — quyết định kết thúc.",
    "c2_c24c": "Kết xấu chỉ mở khi hảo cảm ≤ 39; kết thường cần ≥ 40.",
    "c2_c25": "Lựa chọn thứ hai cần hảo cảm ≥ 70 và còn Thăng Tiên Lệnh trong túi.",
}


def doc(chuong: int) -> dict:
    p = os.path.join(GOC, "game", "chapters", f"chuong{chuong}.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- xuất TXT
# Người dùng chỉ có điện thoại: cần một tệp tải về đọc được offline, không
# phụ thuộc JS hay mạng. Tệp sinh sẵn lúc build, không sinh trong trình duyệt.

def _dk_chu(dk: dict | None) -> str:
    """Điều kiện thành câu chữ thường, không mã HTML."""
    if not dk:
        return ""
    phan = []
    for ten, muc in (dk.get("hao_cam") or {}).items():
        phan.append(f"hảo cảm {ten} ≥ {muc}")
    for ten, muc in (dk.get("hao_cam_max") or {}).items():
        phan.append(f"hảo cảm {ten} ≤ {muc}")
    for sk in dk.get("co_su_kien") or []:
        phan.append(f"đã có sự kiện {sk}")
    for sk in dk.get("khong_su_kien") or []:
        phan.append(f"chưa có sự kiện {sk}")
    for vt in dk.get("co_vat") or []:
        phan.append(f"trong túi có {vt}")
    return "; ".join(phan)


def _hu_chu(hu: dict | None) -> str:
    if not hu:
        return ""
    phan = []
    for ten, muc in (hu.get("hao_cam") or {}).items():
        phan.append(f"{ten} {'+' if muc >= 0 else ''}{muc}")
    for vt in hu.get("them_vat") or []:
        phan.append(f"nhận {vt.get('ten')} ×{vt.get('so', 1)}")
    for sk in hu.get("su_kien") or []:
        phan.append(f"mở sự kiện {sk}")
    return "; ".join(phan)


def _ngat(chu: str, rong: int = 78) -> str:
    """Ngắt dòng theo từ, để tệp đọc được trên màn hình hẹp.

    Bỏ dấu `*` của in nghiêng: văn bản thuần không có kiểu chữ, giữ lại chỉ
    thành nhiễu.
    """
    # In nghiêng có thể mở ở đoạn này, đóng ở đoạn kia, nên phải bắt trước khi
    # cắt đoạn; dấu sao còn lẻ thì bỏ luôn.
    chu = re.sub(r"\*([^*]+?)\*", r"\1", chu or "", flags=re.S)
    chu = chu.replace("*", "")
    ra = []
    for doan in (chu or "").split("\n\n"):
        doan = doan.strip()
        if not doan:
            continue
        dong, dai = [], 0
        for tu in doan.split():
            if dai + len(tu) + 1 > rong and dong:
                ra.append(" ".join(dong))
                dong, dai = [tu], len(tu)
            else:
                dong.append(tu)
                dai += len(tu) + 1
        if dong:
            ra.append(" ".join(dong))
        ra.append("")
    return "\n".join(ra)


def _xuat_nhanh(o: list[str], ds: dict, dau: str, ten_nhanh: str,
                so_chuong: int) -> None:
    """In trọn một nhánh theo thứ tự đọc, mỗi đoạn một lần."""
    o.append("")
    o.append("=" * 78)
    o.append(f"NHÁNH {ten_nhanh.upper()} — CHƯƠNG {so_chuong}")
    o.append("=" * 78)
    o.append("")

    da_in: set[str] = set()

    def di(did: str, sau: int) -> None:
        if not did or did not in ds or did in da_in:
            return
        da_in.add(did)
        d = ds[did]
        le = "    " * min(sau, 6)

        o.append("")
        o.append(f"{le}── [{did}]" + (f" · {d.get('boi_canh')}" if d.get("boi_canh") else ""))
        o.append("")
        than = _ngat(d.get("ke") or "").rstrip()
        for dong in than.split("\n"):
            o.append(f"{le}{dong}" if dong else "")

        for bt in d.get("bien_the") or []:
            o.append("")
            o.append(f"{le}» GIỌNG KỂ KHÁC khi {bt.get('npc')} ở mức "
                     f"“{bt.get('muc')}”:")
            for dong in _ngat(bt.get("ke") or "").rstrip().split("\n"):
                o.append(f"{le}  {dong}" if dong else "")

        lua_chon = d.get("lua_chon") or []
        if lua_chon:
            o.append("")
        for i, lc in enumerate(lua_chon, 1):
            den = lc.get("den")
            dich = "KẾT THÚC CHƯƠNG" if den == "__ket_thuc__" else den
            o.append(f"{le}  {i}. {lc.get('chu', '').strip()}")
            o.append(f"{le}     → {dich}")
            dk, hu = _dk_chu(lc.get("dieu_kien")), _hu_chu(lc.get("hieu_ung"))
            if dk:
                o.append(f"{le}     [cần: {dk}]")
            if hu:
                o.append(f"{le}     [đổi: {hu}]")

        for lc in lua_chon:
            den = lc.get("den")
            if den and den != "__ket_thuc__":
                di(den, sau + 1)

    di(dau, 0)


def xuat_txt(d1: dict, d2: dict) -> str:
    """Sinh toàn bộ cốt truyện thành văn bản thuần, trả về đường dẫn tệp."""
    o: list[str] = []
    o.append("=" * 78)
    o.append("HỒNG ĐỨC TU TIÊN LỘ — TOÀN BỘ CỐT TRUYỆN")
    o.append("=" * 78)
    o.append("")
    o.append("Tệp sinh tự động từ dữ liệu game. Sửa truyện thì chạy lại")
    o.append("tools/tao_so_do_cot_truyen.py, đừng sửa tay tệp này.")
    o.append("")
    o.append("Quy ước đọc:")
    o.append("  [mã đoạn]  là mã đoạn trong dữ liệu game")
    o.append("  »          là giọng kể đổi theo mức hảo cảm")
    o.append("  [cần: …]   là điều kiện phải đủ mới chọn được")
    o.append("  [đổi: …]   là thay đổi khi chọn")
    o.append("")
    o.append("Mỗi mã đoạn in một lần. Chỗ khác cùng dẫn tới đoạn đó thì chỉ ghi")
    o.append("mã — tra mã trong tệp là thấy nguyên văn.")
    o.append("")

    for so, d in ((1, d1), (2, d2)):
        o.append("")
        o.append("#" * 78)
        o.append(f"# CHƯƠNG {so} — {d.get('ten', '')}")
        o.append("#" * 78)
        o.append("")
        for dong in _ngat(d.get("tom_tat") or "").rstrip().split("\n"):
            o.append(dong)
        ds = {x["id"]: x for x in d["doan"]}
        for nhom, ten in (("tan_tu", "Tán tu"), ("mon_phai", "Môn phái")):
            dau = (d.get("doan_dau_theo_nhom") or {}).get(nhom)
            if dau:
                _xuat_nhanh(o, ds, dau, ten, so)
        ket = d.get("ket") or {}
        if ket.get("ke"):
            o.append("")
            o.append("-" * 78)
            o.append("LỜI KẾT CHƯƠNG")
            o.append("-" * 78)
            o.append("")
            for dong in _ngat(ket["ke"]).rstrip().split("\n"):
                o.append(dong)

    o.append("")
    o.append("=" * 78)
    o.append("HẾT")
    o.append("=" * 78)

    dich = os.path.join(GOC, "docs", "nhap", "cot-truyen-day-du.txt")
    os.makedirs(os.path.dirname(dich), exist_ok=True)
    with open(dich, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return dich



def nhan(did: str, doan: dict) -> str:
    if did in NHAN:
        return NHAN[did]
    cau = (doan.get("ke") or "").strip().split("\n")[0]
    cau = re.sub(r"[*_]", "", cau)
    return cau[:58] + ("…" if len(cau) > 58 else "")


def mach_chinh(ds: dict, dau: str, dung: set[str] | None = None) -> list[str]:
    """Đi theo lựa chọn đầu tiên ở mỗi đoạn — đó là mạch chính.

    `dung`: đoạn đã in ở chỗ khác thì dừng trước nó, khỏi in lặp.
    """
    dung = dung or set()
    ra, cur = [], dau
    while cur and cur in ds and cur not in ra and cur not in dung:
        ra.append(cur)
        nx = [lc.get("den") for lc in (ds[cur].get("lua_chon") or [])
              if lc.get("den") in ds]
        cur = nx[0] if nx else None
    return ra


def doan_van(chu: str) -> str:
    o = []
    for p in (chu or "").split("\n\n"):
        p = p.strip()
        if not p:
            continue
        an = html.escape(p)
        an = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", an)
        lop = ' class="he"' if an.startswith("👁") else ""
        o.append(f"<p{lop}>{an}</p>")
    return "\n".join(o)


def mo_ta_dieu_kien(dk: dict | None) -> str:
    if not dk:
        return ""
    phan = []
    for ten, toi_thieu in (dk.get("hao_cam") or {}).items():
        phan.append(f"hảo cảm {html.escape(ten)} ≥ {toi_thieu}")
    for ten, toi_da in (dk.get("hao_cam_max") or {}).items():
        phan.append(f"hảo cảm {html.escape(ten)} ≤ {toi_da}")
    for sk in dk.get("co_su_kien") or []:
        phan.append(f"đã có sự kiện <code>{html.escape(sk)}</code>")
    if dk.get("co_vat"):
        phan.append(f"túi có <b>{html.escape(dk['co_vat'])}</b>")
    return " · ".join(phan)


def hieu_ung_ngan(hu: dict | None) -> str:
    if not hu:
        return ""
    phan = []
    for ten, d in (hu.get("hao_cam") or {}).items():
        phan.append(f"{html.escape(ten)} {d:+d}")
    for v in hu.get("them_vat") or []:
        so = v.get("so") or 1
        phan.append(f"+{so} {html.escape(v['ten'])}")
    if hu.get("co_su_kien"):
        phan.append("ghi sự kiện")
    return " · ".join(phan)


def the_buoc(ds: dict, did: str, so: int, lop: str, da_ve: set[str]) -> str:
    d = ds[did]
    lc_list = d.get("lua_chon") or []
    o = [f'<li class="buoc {lop}">']
    o.append(f'<details id="b-{did}"><summary><span class="so">{so}</span>'
             f'<span class="ten">{html.escape(nhan(did, d))}</span></summary>')
    o.append(f'<div class="than"><p class="ma">{html.escape(did)}</p>')
    o.append(f'<div class="van">{doan_van(d.get("ke"))}</div>')

    if did in GHI_CHU:
        o.append(f'<p class="chugiai">◆ {html.escape(GHI_CHU[did])}</p>')

    if lc_list:
        o.append('<p class="nhan-nh">Lựa chọn ở bước này</p><ul class="chon">')
        for i, lc in enumerate(lc_list, 1):
            den = lc.get("den")
            dk = mo_ta_dieu_kien(lc.get("dieu_kien"))
            hu = hieu_ung_ngan(lc.get("hieu_ung"))
            # Chỉ gọi là mạch chính khi lựa chọn đầu KHÔNG kèm điều kiện —
            # lựa chọn đầu mà có khoá thì người chơi chưa đủ điều kiện sẽ đi nhánh khác.
            chinh = (i == 1 and not dk)
            dau = "→" if chinh else "↳"
            ten_dich = ""
            if den == "__ket_thuc__":
                ten_dich = "hết chương"
            elif den in ds:
                ten_dich = nhan(den, ds[den])
            lop_dich = "dich-chinh" if chinh else "dich-phu"
            o.append(f'<li class="{lop_dich}"><span class="dau">{dau}</span>'
                     f'<span class="chu">{html.escape(lc["chu"])}</span>')
            if ten_dich:
                o.append(f'<span class="toi">▸ {html.escape(ten_dich)}</span>')
            if dk:
                o.append(f'<span class="dk">🔒 {dk}</span>')
            if hu:
                o.append(f'<span class="hu">{hu}</span>')
            o.append("</li>")
        o.append("</ul>")
    o.append("</div></details>")

    # Nhánh rẽ: mọi đích không phải lựa chọn đầu, chưa in ở chỗ khác
    re_ = [lc.get("den") for lc in lc_list[1:] if lc.get("den") in ds]
    for den in re_:
        if den in da_ve:
            continue
        sub = mach_chinh(ds, den, da_ve)
        for ma in sub:
            da_ve.add(ma)
        if not sub:
            continue
        o.append('<div class="re"><p class="re-nhan">nhánh rẽ</p><ol class="mach">')
        for k, ma in enumerate(sub, 1):
            o.append(the_buoc(ds, ma, k, "re-buoc", da_ve))
        o.append("</ol></div>")

    o.append("</li>")
    return "\n".join(o)


def sinh_nhanh(d: dict, nhom: str, so_chuong: int,
               dung: set[str] | None = None,
               tieu_de: str | None = None,
               ghi_chu: str | None = None,
               mach_san: list[str] | None = None) -> str:
    ds = {x["id"]: x for x in d["doan"]}
    dung_set = set(dung or ())
    if mach_san is None:
        dau = d["doan_dau_theo_nhom"][nhom]
        mach = mach_chinh(ds, dau, dung_set)
    else:
        mach = mach_san
    da_ve = set(mach) | dung_set

    ten = tieu_de or f"Nhánh {TEN_NHOM[nhom]}"
    ma_anchor = "chung" if mach_san is not None else f"{nhom}-c{so_chuong}"
    o = [f'<h2 id="{ma_anchor}">{ten} '
         f'<span class="ghi">Chương {so_chuong} · {len(mach)} bước</span></h2>']
    if ghi_chu:
        o.append(f'<p class="phu">{ghi_chu}</p>')

    # Dải số bước: nhìn một liếc thấy độ dài nhánh và chỗ rẽ, bấm số để nhảy tới.
    o.append('<div class="dai-so">')
    for i, ma in enumerate(mach, 1):
        co_re = ' co-re' if len(ds[ma].get("lua_chon") or []) > 1 else ""
        o.append(f'<a class="o{co_re}" href="#b-{ma}">{i}</a>')
    o.append("</div>")

    o.append('<ol class="mach">')
    for i, ma in enumerate(mach, 1):
        o.append(the_buoc(ds, ma, i, f"nhom-{MAU_NHOM[nhom]}", da_ve))
    o.append("</ol>")
    return "\n".join(o)


def sinh() -> tuple[str, dict]:
    d1, d2 = doc(1), doc(2)
    ds2 = {x["id"]: x for x in d2["doan"]}

    # Đoạn chung: cả hai nhóm cùng tới được
    def toi_duoc(dau: str, ds: dict) -> set[str]:
        seen, st = set(), [dau]
        while st:
            i = st.pop()
            if i in seen or i not in ds:
                continue
            seen.add(i)
            for lc in (ds[i].get("lua_chon") or []):
                t = lc.get("den")
                if t and t != "__ket_thuc__":
                    st.append(t)
        return seen

    t1 = toi_duoc(d2["doan_dau_theo_nhom"]["tan_tu"], ds2)
    t2 = toi_duoc(d2["doan_dau_theo_nhom"]["mon_phai"], ds2)
    chung = t1 & t2
    chi_a, chi_b = t1 - chung, t2 - chung

    o = ["""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sơ đồ cốt truyện — Tán tu &amp; Môn phái</title>
<style>
  :root{--giay:#f4ecd8;--muc:#241c14;--son:#8a3a20;--luc:#3f7d4e;--lam:#2f5d7c}
  *{box-sizing:border-box}
  body{margin:0;background:#14100b;color:var(--muc);
       font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
       line-height:1.65;-webkit-text-size-adjust:100%}
  .khung{max-width:760px;margin:0 auto;padding:16px 10px 64px}
  .to{background:var(--giay);border-radius:14px;padding:18px 13px;
      box-shadow:0 10px 40px rgba(0,0,0,.5)}
  h1{font-size:21px;line-height:1.3;margin:0 0 6px;color:var(--son)}
  .phu{font-size:13px;color:#6b5b48;margin:0 0 14px}
  h2{font-size:17px;margin:28px 0 4px;color:var(--son);
     border-bottom:1px solid rgba(138,58,32,.25);padding-bottom:6px}
  .ghi{display:block;font-size:12px;color:#8b7a63;font-weight:400;
       text-transform:none;letter-spacing:0;margin-top:3px}
  .tomtat{background:rgba(138,58,32,.07);border-left:3px solid var(--son);
          border-radius:0 8px 8px 0;padding:11px 13px;margin:12px 0;font-size:14px}

  /* mạch: danh sách dọc, mỗi bước một thẻ */
  ol.mach{list-style:none;margin:0;padding:0}
  ol.mach>li{position:relative;padding-left:22px;margin:0}
  ol.mach>li::before{content:"";position:absolute;left:8px;top:0;bottom:0;
       width:2px;background:rgba(138,58,32,.22)}
  ol.mach>li:last-child::before{bottom:auto;height:26px}
  ol.mach>li::after{content:"";position:absolute;left:5px;top:18px;width:8px;height:8px;
       border-radius:50%;background:var(--son);border:2px solid var(--giay)}
  li.nhom-b::after{background:var(--lam)}
  li.nhom-b::before{background:rgba(47,93,124,.28)}

  details{background:rgba(255,255,255,.5);border:1px solid rgba(36,28,20,.13);
          border-radius:10px;margin:6px 0;overflow:hidden}
  summary{display:flex;gap:8px;align-items:flex-start;padding:10px 11px;
          font-size:14px;font-weight:600;color:#3a2a1c;cursor:pointer;list-style:none}
  summary::-webkit-details-marker{display:none}
  summary::after{content:"▾";margin-left:auto;color:#a08a70;font-size:12px}
  details[open] summary::after{content:"▴"}
  .so{flex:0 0 auto;min-width:20px;height:20px;border-radius:6px;
      background:rgba(138,58,32,.14);color:var(--son);font-size:11.5px;
      font-weight:700;text-align:center;line-height:20px}
  li.nhom-b .so{background:rgba(47,93,124,.14);color:var(--lam)}
  .ten{flex:1}
  .than{padding:0 12px 12px;border-top:1px solid rgba(36,28,20,.08)}
  .ma{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:#a08a70;
      margin:8px 0 4px;letter-spacing:.4px}
  .van p{font-size:14px;margin:9px 0}
  .van p.he{font-size:13px;color:var(--luc);background:rgba(63,125,78,.09);
            border-left:3px solid var(--luc);border-radius:0 8px 8px 0;padding:8px 11px}
  em{color:#5a3a22}
  .chugiai{font-size:13px;color:#7a4a1e;background:rgba(200,150,40,.13);
           border-left:3px solid #c89628;border-radius:0 8px 8px 0;
           padding:8px 11px;margin:10px 0}
  .nhan-nh{font-size:11px;text-transform:uppercase;letter-spacing:.7px;
           color:#8b7a63;margin:14px 0 5px}
  ul.chon{list-style:none;margin:0;padding:0}
  ul.chon li{font-size:13.5px;padding:7px 9px;border-radius:8px;margin-bottom:5px;
             background:rgba(36,28,20,.045);border:1px solid rgba(36,28,20,.08)}
  ul.chon li.dich-chinh{background:rgba(138,58,32,.09);
             border-color:rgba(138,58,32,.22)}
  .dau{color:var(--son);font-weight:700;margin-right:5px}
  .chu{color:#2f2318}
  .toi{display:block;font-size:12px;color:#6b5b48;margin:2px 0 0 15px}
  .dk{display:block;font-size:12px;color:#8a5a12;margin:3px 0 0 15px}
  .hu{display:block;font-size:12px;color:var(--luc);margin:2px 0 0 15px}
  .ma{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:#a08a70;
      margin:8px 0 4px;letter-spacing:.4px}
  code{font-family:ui-monospace,Menlo,monospace;font-size:12px;
       background:rgba(36,28,20,.08);padding:1px 4px;border-radius:4px}
  .mo-het{display:block;width:100%;margin:10px 0 0;padding:10px;
          border-radius:9px;border:1px solid rgba(138,58,32,.3);
          background:rgba(138,58,32,.08);color:var(--son);
          font-size:13.5px;font-weight:600;font-family:inherit}
  .mo-het.tai{display:block;text-align:center;text-decoration:none;
          border-color:rgba(47,107,69,.4);background:rgba(47,107,69,.1);
          color:var(--luc);margin-top:8px}
  .ghi-tai{font-size:11.5px;color:#8b7a63;margin:6px 0 0;text-align:center}

  /* dải số bước */
  .dai-so{display:flex;flex-wrap:wrap;gap:4px;margin:10px 0 8px}
  .dai-so a{width:26px;height:26px;line-height:26px;text-align:center;
       border-radius:6px;font-size:12px;font-weight:700;text-decoration:none;
       background:rgba(138,58,32,.1);color:var(--son);
       border:1px solid rgba(138,58,32,.22)}
  .dai-so a.co-re{background:rgba(200,150,40,.2);color:#7a4a1e;
       border-color:rgba(200,150,40,.5)}

  /* khối nhánh rẽ */
  .re{margin:8px 0 2px 4px;padding:2px 0 2px 10px;
      border-left:2px dashed rgba(138,58,32,.35)}
  .re-nhan{font-size:10.5px;text-transform:uppercase;letter-spacing:.8px;
           color:#a0764a;margin:2px 0 4px}
  .re ol.mach>li::before{background:none}
  .re ol.mach>li{padding-left:14px}
  .re ol.mach>li::after{left:0;top:16px;width:6px;height:6px;
       background:#c89628;border-color:var(--giay)}

  .luoi{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
  .luoi div{background:rgba(36,28,20,.05);border-radius:8px;padding:9px 11px;
            font-size:12.5px}
  .luoi b{display:block;font-size:19px;color:var(--son);
          font-family:ui-monospace,Menlo,monospace}
  .dai{font-size:12px;color:#6b5b48;margin-top:26px;padding-top:12px;
       border-top:1px solid rgba(36,28,20,.15)}
  a{color:var(--son)}
  .nen{display:flex;gap:8px;margin:12px 0}
  .nen a{flex:1;text-align:center;background:rgba(138,58,32,.1);color:var(--son);
         text-decoration:none;padding:11px 6px;border-radius:9px;font-size:13px;
         font-weight:600;border:1px solid rgba(138,58,32,.3)}
  .nen a.b{background:rgba(47,93,124,.1);color:var(--lam);
           border-color:rgba(47,93,124,.3)}
</style>
</head>
<body>
<div class="khung"><div class="to">
<h1>Sơ đồ cốt truyện — hai nhánh xuất thân</h1>
<p class="phu">Tán tu &amp; Môn phái · Chương 1–2 · sinh thẳng từ dữ liệu game ·
bấm một bước để mở nguyên văn</p>
"""]

    so_buoc1 = len(mach_chinh({x["id"]: x for x in d1["doan"]},
                              d1["doan_dau_theo_nhom"]["tan_tu"]))
    so_buoc1b = len(mach_chinh({x["id"]: x for x in d1["doan"]},
                               d1["doan_dau_theo_nhom"]["mon_phai"]))
    mach_a = mach_chinh(ds2, d2["doan_dau_theo_nhom"]["tan_tu"])
    mach_b = mach_chinh(ds2, d2["doan_dau_theo_nhom"]["mon_phai"])
    gap_a = next((i for i, m in enumerate(mach_a) if m in chung), len(mach_a))
    gap_b = next((i for i, m in enumerate(mach_b) if m in chung), len(mach_b))
    mach_chung = mach_a[gap_a:]
    so_buoc2, so_buoc2b = len(mach_a), len(mach_b)

    o.append('<div class="tomtat">'
             'Mỗi thẻ là <b>một hành động</b> của người chơi. Mũi tên <b>→</b> là '
             'lựa chọn mạch chính, <b>↳</b> là nhánh rẽ. Khối nét đứt vàng là phần '
             'truyện riêng của nhánh đó. 🔒 là điều kiện phải đủ mới mở được.'
             '</div>')

    o.append('<div class="luoi">')
    o.append(f'<div><b>{so_buoc1}</b>chặng tán tu · C1</div>')
    o.append(f'<div><b>{so_buoc1b}</b>chặng môn phái · C1</div>')
    o.append(f'<div><b>{len(t1)}</b>đoạn tán tu · C2</div>')
    o.append(f'<div><b>{len(t2)}</b>đoạn môn phái · C2</div>')
    o.append("</div>")

    o.append('<div class="nen"><a href="#c1">Chương 1</a>'
             '<a class="b" href="#c2">Chương 2</a></div>')
    o.append('<button class="mo-het" id="mo-het">Mở tất cả nguyên văn</button>')
    o.append('<a class="mo-het tai" id="tai-txt" download '
             'href="cot-truyen-day-du.txt">⬇ Tải toàn bộ cốt truyện (.txt)</a>')
    o.append('<p class="ghi-tai">Tệp văn bản thuần, đọc offline được. Trên iPhone '
             'nếu tệp mở thành trang chữ, bấm <b>Chia sẻ → Lưu vào Tệp</b>.</p>')

    o.append('<div class="tomtat" style="border-left-color:#2f5d7c;'
             'background:rgba(47,93,124,.08)">'
             '<b>Khác biệt lớn nhất giữa hai nhánh:</b> hai nhánh <b>không gặp nhau</b> ở '
             'bất kỳ đâu — không phải Chương 1, cũng không phải Chương 2. Tán tu nhận '
             '<b>kiếm linh Hồng Trần</b> trong miếu hoang, môn phái nhận <b>Tuyết Cơ</b> '
             'trong khối ngọc. Chương 2 là <b>hai lần chơi riêng biệt</b>: mỗi bên có '
             'đường đi, bạn đồng hành và kết thúc của riêng mình.</div>')

    # ---- Chương 1 ----
    o.append('<h2 id="c1">Chương 1 — Đại chiến Dã Lang Bang</h2>')
    o.append(f'<p class="phu">{html.escape(d1.get("tom_tat") or "")}</p>')
    o.append(sinh_nhanh(d1, "tan_tu", 1))
    o.append(sinh_nhanh(d1, "mon_phai", 1))

    # ---- Chương 2 ----
    o.append('<h2 id="c2">Chương 2 — Tiểu hội Thái Nam Sơn Cốc</h2>')
    o.append(f'<p class="phu">{html.escape(d2.get("tom_tat") or "")}</p>')

    o.append(f'<div class="tomtat">Chương 2 là <b>hai lần chơi độc lập</b>: '
             f'<b>tán tu</b> ({len(t1)} đoạn) và <b>môn phái</b> ({len(t2)} đoạn). '
             f'Hai bên <b>không chia sẻ một đoạn nào</b> — chơi nhánh này không mở '
             f'khóa gì cho nhánh kia, và mỗi nhánh có kết thúc riêng.</div>')

    # Mỗi nhóm in trọn nhánh mình, không có phần chung.
    o.append(sinh_nhanh(d2, "tan_tu", 2,
                        tieu_de="Nhánh Tán tu — trọn vẹn",
                        ghi_chu="Từ Gia Nguyên tới chân Thái Nam sơn rồi ra khỏi cốc. "
                                "Bạn đồng hành: kiếm linh Hồng Trần, hảo cảm 100 từ đầu."))
    o.append(sinh_nhanh(d2, "mon_phai", 2,
                        tieu_de="Nhánh Môn phái — trọn vẹn",
                        ghi_chu="Từ Thất Huyền Môn xuống núi rồi ra khỏi cốc. "
                                "Bạn đồng hành: Tuyết Cơ, hảo cảm 100 từ đầu."))

    o.append('<p class="dai">Sinh từ <code>game/chapters/chuong1.json</code> và '
             '<code>chuong2.json</code> bằng <code>tools/tao_so_do_cot_truyen.py</code>. '
             'Sửa truyện thì chạy lại script, đừng sửa tay trang này.<br>'
             '<a href="cot-truyen-chuong2.html">Đọc toàn văn Chương 2</a> · '
             '<a href="../game/play.html">Vào chơi</a></p>')
    o.append("</div></div>")
    o.append("""<script>
document.getElementById('mo-het').addEventListener('click', function(){
  var het = this.dataset.mo === '1';
  document.querySelectorAll('details').forEach(function(d){ d.open = !het; });
  this.dataset.mo = het ? '0' : '1';
  this.textContent = het ? 'Mở tất cả nguyên văn' : 'Đóng tất cả';
});
</script>""")
    o.append("</body></html>")

    os.makedirs(os.path.dirname(RA), exist_ok=True)
    with open(RA, "w", encoding="utf-8") as f:
        f.write("\n".join(o))

    tep_txt = xuat_txt(d1, d2)

    return RA, {
        "c1_tan_tu": so_buoc1, "c1_mon_phai": so_buoc1b,
        "c2_tan_tu": so_buoc2, "c2_mon_phai": so_buoc2b,
        "doan_chung": len(chung),
    }


if __name__ == "__main__":
    ra, so = sinh()
    print(f"Đã ghi {ra}")
    print(f"Đã ghi {os.path.join(GOC, 'docs', 'nhap', 'cot-truyen-day-du.txt')}")
    for k, v in so.items():
        print(f"  {k}: {v}")
