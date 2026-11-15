# -*- coding: utf-8 -*-
"""Bộ kiểm thử toàn diện qua API thật (chạy khi server đang chạy)."""
import json, os, sys, urllib.request, urllib.error, http.cookiejar as cj

B = "http://127.0.0.1:12001"
ok = fail = 0

def mk():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj.CookieJar()))

def call(o, p, d=None):
    r = urllib.request.Request(
        B + p,
        data=json.dumps(d).encode() if d is not None else None,
        headers={"Content-Type": "application/json"} if d is not None else {})
    try:
        return json.load(o.open(r))
    except urllib.error.HTTPError as e:
        try:
            return {"_http": e.code, **json.loads(e.read())}
        except Exception:
            return {"_http": e.code}

def check(ten, dieu, thuc):
    global ok, fail
    if dieu == thuc:
        ok += 1; print(f"  ✓ {ten}")
    else:
        fail += 1; print(f"  ✗ {ten}\n      mong đợi: {dieu!r}\n      nhận được: {thuc!r}")

print("=== A. Endpoint cơ bản ===")
o = mk()
check("/api/xuat_than đủ 2 nhóm chơi được",
      [n["ma"] for n in call(o, "/api/xuat_than")["nhom"]],
      ["tan_tu", "mon_phai"])
check("/api/state chưa phiên", call(o, "/api/state"), {"co_phien": False})
check("/api/doan chưa phiên → 400", call(o, "/api/doan").get("_http"), 400)

print("\n=== B. Tạo phiên ===")
check("thiếu tên → 400", call(o, "/api/new", {"ten": "  "}).get("_http"), 400)
check("nhóm lạ rơi về tán tu", call(o, "/api/new", {"ten": "A", "nhom": "xyz"})["doan_id"], "c1_d01")
o2 = mk()
check("nhóm ẩn Tuyết Cơ không kích hoạt",
      call(o2, "/api/new", {"ten": "B", "nhom": "tuyet_co"})["doan_id"], "c1_d01")
check("nhóm môn phái đúng đoạn mở", call(o2, "/api/new", {"ten": "B2", "nhom": "mon_phai"})["doan_id"], "c1_p01")

print("\n=== C. Lùi hành động ===")
o3 = mk()
call(o3, "/api/new", {"ten": "C", "nhom": "tan_tu"})
call(o3, "/api/chon", {"chi_so": 0})     # d01 → d02
call(o3, "/api/chon", {"chi_so": 0})     # d02 → d03
st = call(o3, "/api/state")
check("sau 2 bước, so_lui = 2", st["so_lui"], 2)
r = call(o3, "/api/lui", {})
check("lùi 1 → đúng đoạn", r["doan_id"], "c1_d02")
check("lùi 1 có thông báo", bool(r.get("thong_bao")), True)
check("so_lui sau lùi = 1", call(o3, "/api/state")["so_lui"], 1)
r = call(o3, "/api/lui", {})
check("lùi 2 → về đầu", r["doan_id"], "c1_d01")
check("lùi khi cạn → 400", call(o3, "/api/lui", {}).get("_http"), 400)
check("so_lui sau cạn = 0", call(o3, "/api/state")["so_lui"], 0)

print("\n=== D. Nhập tự do + lỗi nhập ===")
o4 = mk()
call(o4, "/api/new", {"ten": "D", "nhom": "tan_tu"})
r = call(o4, "/api/tu_do", {"van_ban": "nhìn quanh tìm lối thoát"})
check("tự do trả đoạn hợp lệ", "doan_id" in r, True)
check("nhập rỗng → báo lỗi", call(o4, "/api/tu_do", {"van_ban": "   "}).get("loi") is not None, True)
check("chi_so sai → báo lỗi", call(o4, "/api/chon", {"chi_so": 99}).get("loi") is not None, True)
check("chi_so âm → báo lỗi", call(o4, "/api/chon", {"chi_so": -1}).get("loi") is not None, True)

print("\n=== E. Lưu / nạp ===")
r = call(o4, "/api/luu", {"slot": "test_slot"})
check("lưu trả ok", r.get("ok"), True)
save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "saves")
check("tệp lưu tồn tại", any("test_slot" in f for f in os.listdir(save_dir)), True)

print("\n=== F. Chơi lại ===")
check("trước có phiên", call(o4, "/api/state")["co_phien"], True)
check("/api/moi ok", call(o4, "/api/moi", {}).get("ok"), True)
check("sau không còn phiên", call(o4, "/api/state"), {"co_phien": False})

print("\n=== G. Bảo mật ===")
o5 = mk()
call(o5, "/api/new", {"ten": "E", "nhom": "tan_tu"})
check("endpoint lạ (có phiên) → 404", call(o5, "/api/khong_ton_tai", {}).get("_http"), 404)
check("endpoint lạ (không phiên) → 400", call(o4, "/api/khong_ton_tai", {}).get("_http"), 400)
try:
    r = urllib.request.urlopen(B + "/../../etc/passwd", timeout=5)
    check("path traversal bị chặn", False, True)
except urllib.error.HTTPError as e:
    check("path traversal bị chặn (404)", e.code, 404)

print("\n=== H. Hồi quy: các đường từng làm SẬP máy chủ ===")
o6 = mk()
call(o6, "/api/new", {"ten": "R", "nhom": "tan_tu"})
check("chi_so='abc' → báo lỗi, không sập",
      call(o6, "/api/chon", {"chi_so": "abc"}).get("loi"), "Lựa chọn không hợp lệ")
check("chi_so=null → báo lỗi, không sập",
      call(o6, "/api/chon", {"chi_so": None}).get("loi"), "Lựa chọn không hợp lệ")
check("chi_so=[1,2] → báo lỗi, không sập",
      call(o6, "/api/chon", {"chi_so": [1, 2]}).get("loi"), "Lựa chọn không hợp lệ")
check("van_ban=123 → báo lỗi, không sập",
      call(o6, "/api/tu_do", {"van_ban": 123}).get("loi"), "Hãy nhập hành động")
check("ten=123 → 400, không sập", call(mk(), "/api/new", {"ten": 123}).get("_http"), 400)

# chạm đúp "Khép lại Chương 1" (lỗi gốc: KeyError '__ket_thuc__')
o7 = mk()
call(o7, "/api/new", {"ten": "R2", "nhom": "tan_tu"})
for _ in range(40):
    r = call(o7, "/api/chon", {"chi_so": 0})
    if r.get("ket_thuc"):
        break
check("tới màn kết chương", r.get("ket_thuc"), True)
check("bấm khép chương lần 1", call(o7, "/api/chon", {"chi_so": 0}).get("doan_id"), "__ket_thuc__")
check("bấm lần 2 (chạm đúp) không sập",
      call(o7, "/api/chon", {"chi_so": 0}).get("doan_id"), "__ket_thuc__")
check("bấm lần 3 vẫn ổn", call(o7, "/api/chon", {"chi_so": 0}).get("ket_thuc"), True)
check("lùi ở màn kết → về đoạn cuối", call(o7, "/api/lui", {}).get("doan_id"), "c1_d17")
check("lùi tiếp → về đoạn kế trước", call(o7, "/api/lui", {}).get("doan_id"), "c1_d16")
check("máy chủ vẫn sống sau tất cả", call(o7, "/api/state").get("co_phien"), True)

print("\n=== I. Nhánh môn phái: cơ duyên + tu luyện ===")
o8 = mk()
r = call(o8, "/api/new", {"ten": "MP", "nhom": "mon_phai"})
check("mở nhánh môn phái", r["doan_id"], "c1_p01")
r = call(o8, "/api/chon", {"chi_so": 0})
check("p01 → sân tập", r["doan_id"], "c1_p02")
r = call(o8, "/api/chon", {"chi_so": 1})
check("chọn vườn thuốc", r["doan_id"], "c1_p04")
r = call(o8, "/api/chon", {"chi_so": 0})   # p04 → p04a hỏi thẳng
check("gặp Mạc Đại Phu → p04a", r["doan_id"], "c1_p04a")
r = call(o8, "/api/chon", {"chi_so": 0})   # p04a → p06
check("phụ bó thuốc → p06", r["doan_id"], "c1_p06")
r = call(o8, "/api/chon", {"chi_so": 0})   # đào lên, giữ ngọc
st = call(o8, "/api/state")["trang_thai"]
check("nhận Ngọc cốt bí ẩn", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)
check("cờ co_ngoc_cot", "co_ngoc_cot" in st["co_su_kien"], True)
# p07 → p08 → p08b → p09 → p09b → p09c (do dự) → p10 (ký) → p10b (song tu) → p11 (tu luyện)
for _ in range(6):
    r = call(o8, "/api/chon", {"chi_so": 0})
check("tới đoạn song tu p10b", r["doan_id"], "c1_p10b")
r = call(o8, "/api/chon", {"chi_so": 0})
check("tới đoạn tu luyện p11", r["doan_id"], "c1_p11")
check("đêm đầu chưa đột phá", call(o8, "/api/state")["trang_thai"]["canh_gioi"], "Luyện Khí tầng 1")
r = call(o8, "/api/chon", {"chi_so": 0})   # p11b khổ tu
check("khổ tu p11b", r["doan_id"], "c1_p11b")
r = call(o8, "/api/chon", {"chi_so": 0})   # p11c suýt lộ
check("suýt lộ p11c", r["doan_id"], "c1_p11c")
r = call(o8, "/api/chon", {"chi_so": 0})   # p12 đột phá
check("p12 đột phá tầng 2", call(o8, "/api/state")["trang_thai"]["canh_gioi"], "Luyện Khí tầng 2")
check("học Hợp Hoan hô hấp pháp", "Hợp Hoan hô hấp pháp" in call(o8, "/api/state")["trang_thai"]["ky_nang"], True)
r = call(o8, "/api/chon", {"chi_so": 0})   # p13
r = call(o8, "/api/chon", {"chi_so": 0})   # p14
r = call(o8, "/api/chon", {"chi_so": 0})   # p14b giấu lực
st = call(o8, "/api/state")["trang_thai"]
check("cảnh giới vẫn tầng 2 (không vượt)", st["canh_gioi"], "Luyện Khí tầng 2")
# đi tới hết chương
for _ in range(20):
    r = call(o8, "/api/chon", {"chi_so": 0})
    if r.get("ket_thuc"):
        break
check("kết riêng nhánh môn phái", r["doan_id"], "c1_p19")
st = call(o8, "/api/state")["trang_thai"]
check("gặp Hàn Lập, có hảo cảm", st["npc"].get("Hàn Lập", {}).get("hao_cam", 0) > 0, True)

# đường "chôn trả lại rồi đào lại" (đường ②)
o9 = mk()
call(o9, "/api/new", {"ten": "MP2", "nhom": "mon_phai"})
call(o9, "/api/chon", {"chi_so": 0})   # p02
call(o9, "/api/chon", {"chi_so": 1})   # p04
call(o9, "/api/chon", {"chi_so": 0})   # p04a
call(o9, "/api/chon", {"chi_so": 0})   # p06
r = call(o9, "/api/chon", {"chi_so": 1})  # chôn trả lại
check("chôn trả lại → p06b", r["doan_id"], "c1_p06b")
r = call(o9, "/api/chon", {"chi_so": 0})  # đào lại
st = call(o9, "/api/state")["trang_thai"]
check("đào lại vẫn nhận ngọc cốt", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)

# đường ① sân sau — gốc cổ thụ (p03b → p03d → p07)
o13 = mk()
call(o13, "/api/new", {"ten": "MP6", "nhom": "mon_phai"})
call(o13, "/api/chon", {"chi_so": 0})   # p02
call(o13, "/api/chon", {"chi_so": 0})   # p03
call(o13, "/api/chon", {"chi_so": 0})   # p03b nuốt nhục
r = call(o13, "/api/chon", {"chi_so": 0})  # → p03d
check("đường ① p03b → p03d (sân sau)", r["doan_id"], "c1_p03d")
r = call(o13, "/api/chon", {"chi_so": 0})  # lấy ngọc → p07
check("đường ① lấy ngọc → p07", r["doan_id"], "c1_p07")
st = call(o13, "/api/state")["trang_thai"]
check("đường ① có ngọc cốt", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)

# đường ① do dự: p03d → chôn trả lại → p03e → p07
o14 = mk()
call(o14, "/api/new", {"ten": "MP7", "nhom": "mon_phai"})
call(o14, "/api/chon", {"chi_so": 0})
call(o14, "/api/chon", {"chi_so": 0})
call(o14, "/api/chon", {"chi_so": 0})   # p03b
call(o14, "/api/chon", {"chi_so": 0})   # p03d
r = call(o14, "/api/chon", {"chi_so": 1})  # chôn trả lại
check("đường ① do dự → p03e", r["doan_id"], "c1_p03e")
r = call(o14, "/api/chon", {"chi_so": 0})  # đào lại → p07
check("đường ① do dự đào lại → p07", r["doan_id"], "c1_p07")
st = call(o14, "/api/state")["trang_thai"]
check("đường ① do dự vẫn có ngọc", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)

# đường ③ hậu sơn — khe núi (p05 → p05b → p07)
o15 = mk()
call(o15, "/api/new", {"ten": "MP8", "nhom": "mon_phai"})
call(o15, "/api/chon", {"chi_so": 0})   # p02
r = call(o15, "/api/chon", {"chi_so": 2})  # p05 dò tin
check("đường ③ p02 → p05", r["doan_id"], "c1_p05")
r = call(o15, "/api/chon", {"chi_so": 0})  # → p05b
check("đường ③ p05 → p05b (khe núi)", r["doan_id"], "c1_p05b")
st = call(o15, "/api/state")["trang_thai"]
check("đường ③ biết Hùng Bá", "biet_dau_linh" in st["co_su_kien"], True)
r = call(o15, "/api/chon", {"chi_so": 0})  # lấy ngọc → p07
check("đường ③ lấy ngọc → p07", r["doan_id"], "c1_p07")

# đường ③ do dự: p05b → chôn trả lại → p05c → p07
o16 = mk()
call(o16, "/api/new", {"ten": "MP9", "nhom": "mon_phai"})
call(o16, "/api/chon", {"chi_so": 0})
call(o16, "/api/chon", {"chi_so": 2})   # p05
call(o16, "/api/chon", {"chi_so": 0})   # p05b
r = call(o16, "/api/chon", {"chi_so": 1})  # chôn trả lại
check("đường ③ do dự → p05c", r["doan_id"], "c1_p05c")
r = call(o16, "/api/chon", {"chi_so": 0})  # đào lại → p07
check("đường ③ do dự đào lại → p07", r["doan_id"], "c1_p07")

# đường ② p04 lựa chọn KHÔNG còn giả (2 đích khác nhau)
o17 = mk()
call(o17, "/api/new", {"ten": "MP10", "nhom": "mon_phai"})
call(o17, "/api/chon", {"chi_so": 0})   # p02
r = call(o17, "/api/chon", {"chi_so": 1})  # p04
chu = {l["chu"] for l in r["lua_chon"]}
check("p04 2 lựa chọn khác nhau", len(chu), 2)
r = call(o17, "/api/chon", {"chi_so": 1})  # im lặng → p04b
check("đường ② im lặng → p04b", r["doan_id"], "c1_p04b")

# đường luyện võ p03 (nuốt nhục) → học Thất Huyền quyền → p14 mở lựa chọn quyền
o10 = mk()
call(o10, "/api/new", {"ten": "MP3", "nhom": "mon_phai"})
call(o10, "/api/chon", {"chi_so": 0})   # p02
r = call(o10, "/api/chon", {"chi_so": 0})  # p03 bị chèn ép
check("p03 bị chèn ép", r["doan_id"], "c1_p03")
r = call(o10, "/api/chon", {"chi_so": 0})  # nuốt nhục
check("nuốt nhục → p03b", r["doan_id"], "c1_p03b")
r = call(o10, "/api/chon", {"chi_so": 0})  # học Thất Huyền quyền
st = call(o10, "/api/state")["trang_thai"]
check("học Thất Huyền quyền", "Thất Huyền quyền" in st["ky_nang"], True)
check("cờ hoc_that_huyen_quyen", "hoc_that_huyen_quyen" in st["co_su_kien"], True)

# đường dò tin p05 → biết Hùng Bá → p14 mở lựa chọn gọi tên
o11 = mk()
call(o11, "/api/new", {"ten": "MP4", "nhom": "mon_phai"})
call(o11, "/api/chon", {"chi_so": 0})   # p02
call(o11, "/api/chon", {"chi_so": 2})   # p05 dò tin
call(o11, "/api/chon", {"chi_so": 0})   # rời p05 → cờ biet_dau_linh
st = call(o11, "/api/state")["trang_thai"]
check("dò tin → biết Hùng Bá", "biet_dau_linh" in st["co_su_kien"], True)
# đi tới p14
for _ in range(20):
    r = call(o11, "/api/chon", {"chi_so": 0})
    if r["doan_id"] == "c1_p14":
        break
check("tới p14", r["doan_id"], "c1_p14")
chon_p14 = {l["chu"]: l for l in r["lua_chon"]}
check("p14 có lựa chọn gọi Hùng Bá", any("Hùng Bá" in c for c in chon_p14), True)
check("lựa chọn Hùng Bá không bị khoá", chon_p14[[c for c in chon_p14 if "Hùng Bá" in c][0]]["khoa"], False)
r = call(o11, "/api/chon", {"chi_so": 3})  # gọi tên Hùng Bá
check("gọi tên → p14e", r["doan_id"], "c1_p14e")
st = call(o11, "/api/state")["trang_thai"]
check("cờ goi_ten_hung_ba", "goi_ten_hung_ba" in st["co_su_kien"], True)

# đường p14 "dùng toàn lực" → cờ nghi_ngo_tu_vi
o12 = mk()
call(o12, "/api/new", {"ten": "MP5", "nhom": "mon_phai"})
call(o12, "/api/chon", {"chi_so": 0})
call(o12, "/api/chon", {"chi_so": 1})   # p04
call(o12, "/api/chon", {"chi_so": 0})   # p06
for _ in range(30):
    r = call(o12, "/api/chon", {"chi_so": 0})
    if r["doan_id"] == "c1_p14":
        break
r = call(o12, "/api/chon", {"chi_so": 1})  # dùng toàn lực
check("dùng toàn lực → p14c", r["doan_id"], "c1_p14c")
r = call(o12, "/api/chon", {"chi_so": 0})  # rời p14c → cờ nghi_ngo_tu_vi
st = call(o12, "/api/state")["trang_thai"]
check("cờ nghi_ngo_tu_vi", "nghi_ngo_tu_vi" in st["co_su_kien"], True)

# 4 nhánh gặp Hàn Lập khác nhau
for cs, dich, ten in [(0, "c1_p18a", "thành thật"), (1, "c1_p18b", "cười trừ"),
                      (2, "c1_p18c", "hỏi ngược"), (3, "c1_p18d", "bầu nước")]:
    ox = mk()
    call(ox, "/api/new", {"ten": "HL", "nhom": "mon_phai"})
    call(ox, "/api/chon", {"chi_so": 0})
    call(ox, "/api/chon", {"chi_so": 1})
    call(ox, "/api/chon", {"chi_so": 0})
    for _ in range(30):
        r = call(ox, "/api/chon", {"chi_so": 0})
        if r["doan_id"] == "c1_p17":
            break
    r = call(ox, "/api/chon", {"chi_so": cs})
    check(f"p17 {ten} → {dich}", r["doan_id"], dich)
    r = call(ox, "/api/chon", {"chi_so": 0})
    check(f"  {ten} → kết p19", r["doan_id"], "c1_p19")

print("\n=== J. Nhánh TÁN TU: cơ duyên + mọi đường ===")
def toi(o, dich, toi_da=40):
    """Tiến (chọn chi_so=0) cho tới khi tới `dich`; trả đoạn cuối."""
    r = {}
    for _ in range(toi_da):
        r = call(o, "/api/chon", {"chi_so": 0})
        if r.get("doan_id") == dich or r.get("ket_thuc"):
            break
    return r

# Đường 1: d02 → d03 → d04b → d04c → d04d → d05 (chạm hộp)
o20 = mk()
r = call(o20, "/api/new", {"ten": "TT", "nhom": "tan_tu"})
check("tán tu mở đoạn d01", r["doan_id"], "c1_d01")
r = call(o20, "/api/chon", {"chi_so": 0})
check("d01 → d02", r["doan_id"], "c1_d02")
r = call(o20, "/api/chon", {"chi_so": 0})
check("d02 → d03 (miếu hoang)", r["doan_id"], "c1_d03")
r = call(o20, "/api/chon", {"chi_so": 0})
check("d03 → d04b (vào trong)", r["doan_id"], "c1_d04b")
r = call(o20, "/api/chon", {"chi_so": 0})
check("d04b → d04c (Đỗ Tam)", r["doan_id"], "c1_d04c")
r = call(o20, "/api/chon", {"chi_so": 0})
check("d04c → d04d (đoạt hộp)", r["doan_id"], "c1_d04d")
sl_truoc = call(o20, "/api/state")["trang_thai"]["sinh_luc"]["hien"]
r = call(o20, "/api/chon", {"chi_so": 0})   # chạm hai thanh kiếm: -12 sinh lực
check("d04d → d05 (chạm hộp)", r["doan_id"], "c1_d05")
st = call(o20, "/api/state")["trang_thai"]
check("cờ thay_do_tam_chet", "thay_do_tam_chet" in st["co_su_kien"], True)
check("sinh lực bị trừ 12", sl_truoc - st["sinh_luc"]["hien"], 12)

# Đường 2: d02 → d02b (ở lại trấn) → d03 → d04 (đứng ngoài) → d04b
o21 = mk()
call(o21, "/api/new", {"ten": "TT2", "nhom": "tan_tu"})
call(o21, "/api/chon", {"chi_so": 0})   # d02
r = call(o21, "/api/chon", {"chi_so": 1})   # ở lại trấn
check("d02 → d02b (ở lại trấn)", r["doan_id"], "c1_d02b")
r = call(o21, "/api/chon", {"chi_so": 0})   # lên núi
check("d02b → d03", r["doan_id"], "c1_d03")
r = call(o21, "/api/chon", {"chi_so": 1})   # đứng ngoài quan sát
check("d03 → d04 (quan sát)", r["doan_id"], "c1_d04")
r = call(o21, "/api/chon", {"chi_so": 0})   # quỳ chạm nắp hộp
check("d04 → d04b", r["doan_id"], "c1_d04b")

# đường cảnh giác: d06 → d06b (thử thách) → d07
o22 = mk()
call(o22, "/api/new", {"ten": "TT3", "nhom": "tan_tu"})
r = toi(o22, "c1_d06")
check("tới d06 (kiếm linh)", r["doan_id"], "c1_d06")
r = call(o22, "/api/chon", {"chi_so": 1})   # cảnh giác
check("d06 → d06b (thử thách)", r["doan_id"], "c1_d06b")
r = call(o22, "/api/chon", {"chi_so": 0})   # nghe rõ điều kiện
check("d06b → d07", r["doan_id"], "c1_d07")

# đường do dự: d07 → d07b (điều kiện) → d08
o23 = mk()
call(o23, "/api/new", {"ten": "TT4", "nhom": "tan_tu"})
r = toi(o23, "c1_d07")
check("tới d07", r["doan_id"], "c1_d07")
r = call(o23, "/api/chon", {"chi_so": 1})   # do dự
check("d07 → d07b (điều kiện)", r["doan_id"], "c1_d07b")
r = call(o23, "/api/chon", {"chi_so": 0})   # đưa tay nhận chủ
check("d07b → d08", r["doan_id"], "c1_d08")
r = call(o23, "/api/chon", {"chi_so": 0})   # nghe dạy kiếm đạo
check("d08 → d09", r["doan_id"], "c1_d09")
st = call(o23, "/api/state")["trang_thai"]
check("nhận Hồng Trần Kiếm Hạp", any(v["ten"] == "Hồng Trần Kiếm Hạp" for v in st["tui_do"]), True)
check("cờ co_kiem_hong_tran", "co_kiem_hong_tran" in st["co_su_kien"], True)

# đường chiến trận: d11 → d13 (môn phái)
o24 = mk()
call(o24, "/api/new", {"ten": "TT5", "nhom": "tan_tu"})
r = toi(o24, "c1_d11")
check("tới d11 (Dã Lang Bang tập kích)", r["doan_id"], "c1_d11")
r = call(o24, "/api/chon", {"chi_so": 1})   # tới Thất Huyền Môn
check("d11 → d13 (cổng vỡ)", r["doan_id"], "c1_d13")
r = call(o24, "/api/chon", {"chi_so": 0})
check("d13 → d14 (sau trận)", r["doan_id"], "c1_d14")

# đường chiến trận: d11 → d12 (cứu dân)
o24b = mk()
call(o24b, "/api/new", {"ten": "TT5b", "nhom": "tan_tu"})
r = toi(o24b, "c1_d11")
r = call(o24b, "/api/chon", {"chi_so": 0})   # xuống trấn cứu dân
check("d11 → d12 (cứu dân)", r["doan_id"], "c1_d12")
r = call(o24b, "/api/chon", {"chi_so": 0})
check("d12 → d14 (sau trận)", r["doan_id"], "c1_d14")

# tán tu tu luyện: d09 → d10 đột phá Luyện Khí
o25 = mk()
call(o25, "/api/new", {"ten": "TT6", "nhom": "tan_tu"})
r = toi(o25, "c1_d09")
r = call(o25, "/api/chon", {"chi_so": 0})   # tiếp tục tu luyện
check("d09 → d10 (đột phá)", r["doan_id"], "c1_d10")
st = call(o25, "/api/state")["trang_thai"]
check("học Hồng Trần kiếm khí", "Hồng Trần kiếm khí" in st["ky_nang"], True)

# 4 nhánh gặp Hàn Lập của tán tu (hảo cảm theo dữ liệu: 10 / 0 / 5 / 8)
for cs, ten, coco, hc in [(0, "thành thật", "noi_that_han_lap", 10), (1, "cười trừ", None, 0),
                          (2, "hỏi ngược", None, 5), (3, "bầu nước", None, 8)]:
    ot = mk()
    call(ot, "/api/new", {"ten": "TT7", "nhom": "tan_tu"})
    r = toi(ot, "c1_d15")
    check(f"tới d15 (gặp Hàn Lập)", r["doan_id"], "c1_d15")
    r = call(ot, "/api/chon", {"chi_so": cs})
    check(f"d15 {ten} → d16", r["doan_id"], "c1_d16")
    st = call(ot, "/api/state")["trang_thai"]
    check(f"  {ten}: hảo cảm Hàn Lập = {hc}", st["npc"].get("Hàn Lập", {}).get("hao_cam", 0), hc)
    if coco:
        check(f"  {ten}: cờ {coco}", coco in st["co_su_kien"], True)
    r = call(ot, "/api/chon", {"chi_so": 0})
    check(f"  {ten} → kết d17", r["doan_id"], "c1_d17")

# tán tu đi tới hết chương (màn kết)
o26 = mk()
call(o26, "/api/new", {"ten": "TT8", "nhom": "tan_tu"})
r = toi(o26, "c1_d17")
check("tán tu tới d17 (kết chương)", r["doan_id"], "c1_d17")
r = call(o26, "/api/chon", {"chi_so": 0})
check("d17 khép chương → kết", r.get("ket_thuc"), True)

print("\n=== Z. Upload ảnh cảnh (Xưởng) ===")
_anh_test = ["bc_test_api.jpg", "nv_test_api.jpg", "ui_test_api.jpg"]
def _post_raw(p, obj):
    r = urllib.request.Request(B + p, data=json.dumps(obj).encode(),
                               headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        return {"_http": e.code, **json.loads(e.read())}
_png = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
kq = _post_raw("/upload", {"name": "bc_test_api.jpg", "data": _png})
check("upload ảnh cảnh → ok", kq.get("ok"), True)
check("ảnh cảnh lưu vào assets/scene/", os.path.isfile(f"/workspace/game-hong-duc-lam/assets/scene/bc_test_api.jpg"), True)
check("ảnh cảnh lưu cả docs/assets/scene/", os.path.isfile(f"/workspace/game-hong-duc-lam/docs/assets/scene/bc_test_api.jpg"), True)
kq = _post_raw("/upload", {"name": "nv_test_api.jpg", "data": _png})
check("ảnh nhân vật (nv_) cũng vào scene", os.path.isfile(f"/workspace/game-hong-duc-lam/assets/scene/nv_test_api.jpg"), True)
kq = _post_raw("/upload", {"name": "ui_test_api.jpg", "data": _png})
check("ảnh UI (không tiền tố) → assets/ui/", os.path.isfile(f"/workspace/game-hong-duc-lam/assets/ui/ui_test_api.jpg"), True)
check("ảnh UI KHÔNG vào scene", os.path.isfile(f"/workspace/game-hong-duc-lam/assets/scene/ui_test_api.jpg"), False)
for _n in _anh_test:
    for _d in ["assets/scene", "assets/ui", "docs/assets/scene"]:
        _p = f"/workspace/game-hong-duc-lam/{_d}/{_n}"
        if os.path.isfile(_p):
            os.remove(_p)

print("\n=== Y. Nhận diện ảnh (Xưởng B+) ===")
def _png(w, h):
    import struct as _s, zlib as _z
    rows = b""
    for _ in range(h):
        rows += b"\x00" + bytes([240, 235, 225]) * w
    def _ch(t, d):
        c = t + d
        return _s.pack(">I", len(d)) + c + _s.pack(">I", _z.crc32(c) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n"
            + _ch(b"IHDR", _s.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _ch(b"IDAT", _z.compress(rows)) + _ch(b"IEND", b""))

def _b64(data):
    import base64 as _b
    return _b.b64encode(data).decode()

# 9:16 chỉ có 1 ứng viên khớp tỷ lệ → đường tắt, KHÔNG gọi AI (nhanh, ổn định)
kq = _post_raw("/doan_anh", {"anh": [{"name": "IMG_9999.PNG", "data": _b64(_png(1080, 1920))}]})
check("/doan_anh trả ok", kq.get("ok"), True)
_k0 = (kq.get("ket_qua") or [{}])[0]
check("ảnh 9:16 → tự gán bg-main (không cần AI)", _k0.get("key"), "bg-main")
check("  độ tin cậy 100", _k0.get("do_tin_cay"), 100)
check("  đánh dấu tự động", _k0.get("tu_dong"), True)
check("  có tên tiếng Việt của asset", bool(_k0.get("ten")), True)
check("  giữ tên file gốc", _k0.get("name"), "IMG_9999.PNG")

# 5:1 chỉ có 1 ứng viên → btn-choice
kq = _post_raw("/doan_anh", {"anh": [{"name": "a.png", "data": _b64(_png(1200, 240))}]})
check("ảnh 5:1 → btn-choice", (kq.get("ket_qua") or [{}])[0].get("key"), "btn-choice")

# Lưu loạt theo key → ghi đúng tên file
kq = _post_raw("/luu_loat", {"ds": [{"key": "divider-ink", "data": _b64(_png(1600, 160))}]})
check("/luu_loat trả ok", kq.get("ok"), True)
check("lưu theo key → đúng tên divider-ink.png",
      os.path.isfile("/workspace/game-hong-duc-lam/assets/ui/divider-ink.png"), True)
check("  đúng tên file trong kết quả",
      (kq.get("da_luu") or [{}])[0].get("file"), "divider-ink.png")
# Ảnh cảnh lưu theo key phải vào CẢ hai nơi
kq = _post_raw("/luu_loat", {"ds": [{"key": "bc_cho_01", "data": _b64(_png(900, 1200))}]})
check("lưu key bc_cho_01 → assets/scene/",
      os.path.isfile("/workspace/game-hong-duc-lam/assets/scene/bc_cho_01.jpg"), True)
check("  và docs/assets/scene/",
      os.path.isfile("/workspace/game-hong-duc-lam/docs/assets/scene/bc_cho_01.jpg"), True)
for _p in ["assets/ui/divider-ink.png", "assets/scene/bc_cho_01.jpg", "docs/assets/scene/bc_cho_01.jpg"]:
    _f = f"/workspace/game-hong-duc-lam/{_p}"
    if os.path.isfile(_f):
        os.remove(_f)

print(f"\n{'='*46}\nKẾT QUẢ: {ok} đạt, {fail} hỏng")
sys.exit(1 if fail else 0)
