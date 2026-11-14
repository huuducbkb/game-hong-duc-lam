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
check("/api/xuat_than đủ 5 nhóm",
      [n["ma"] for n in call(o, "/api/xuat_than")["nhom"]],
      ["tan_tu", "mon_phai", "duoc", "gia_toc", "hac_dao"])
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
call(o3, "/api/new", {"ten": "C", "nhom": "hac_dao"})
call(o3, "/api/chon", {"chi_so": 0})     # mua tin: -5 bạc
call(o3, "/api/chon", {"chi_so": 0})
st = call(o3, "/api/state")
check("sau 2 bước, so_lui = 2", st["so_lui"], 2)
check("bạc đã trừ", st["trang_thai"]["bac"], 0)
r = call(o3, "/api/lui", {})
check("lùi 1 → đúng đoạn", r["doan_id"], "c1_h02")
check("lùi 1 có thông báo", bool(r.get("thong_bao")), True)
check("so_lui sau lùi = 1", call(o3, "/api/state")["so_lui"], 1)
r = call(o3, "/api/lui", {})
check("lùi 2 → về đầu", r["doan_id"], "c1_h01")
check("bạc hoàn lại 3", r["trang_thai"]["bac"], 3)
check("lùi khi cạn → 400", call(o3, "/api/lui", {}).get("_http"), 400)
check("so_lui sau cạn = 0", call(o3, "/api/state")["so_lui"], 0)

print("\n=== D. Nhập tự do + lỗi nhập ===")
o4 = mk()
call(o4, "/api/new", {"ten": "D", "nhom": "duoc"})
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
call(o7, "/api/new", {"ten": "R2", "nhom": "hac_dao"})
for _ in range(40):
    r = call(o7, "/api/chon", {"chi_so": 0})
    if r.get("ket_thuc"):
        break
check("tới màn kết chương", r.get("ket_thuc"), True)
check("bấm khép chương lần 1", call(o7, "/api/chon", {"chi_so": 0}).get("doan_id"), "__ket_thuc__")
check("bấm lần 2 (chạm đúp) không sập",
      call(o7, "/api/chon", {"chi_so": 0}).get("doan_id"), "__ket_thuc__")
check("bấm lần 3 vẫn ổn", call(o7, "/api/chon", {"chi_so": 0}).get("ket_thuc"), True)
check("lùi ở màn kết → về đoạn cuối", call(o7, "/api/lui", {}).get("doan_id"), "c1_d18")
check("lùi tiếp → về đoạn kế trước", call(o7, "/api/lui", {}).get("doan_id"), "c1_h17b")
check("máy chủ vẫn sống sau tất cả", call(o7, "/api/state").get("co_phien"), True)

print("\n=== I. Nhánh môn phái: cơ duyên + tu luyện ===")
o8 = mk()
r = call(o8, "/api/new", {"ten": "MP", "nhom": "mon_phai"})
check("mở nhánh môn phái", r["doan_id"], "c1_p01")
r = call(o8, "/api/chon", {"chi_so": 0})
check("p01 → sân tập", r["doan_id"], "c1_p02")
r = call(o8, "/api/chon", {"chi_so": 1})
check("chọn vườn thuốc", r["doan_id"], "c1_p04")
r = call(o8, "/api/chon", {"chi_so": 0})
check("gặp Mạc Đại Phu → vườn thuốc", r["doan_id"], "c1_p06")
r = call(o8, "/api/chon", {"chi_so": 0})   # đào lên, giữ ngọc
st = call(o8, "/api/state")["trang_thai"]
check("nhận Ngọc cốt bí ẩn", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)
check("cờ co_ngoc_cot", "co_ngoc_cot" in st["co_su_kien"], True)
# p07 → p08 → p08b → p09 → p09b → p09c (do dự) → p10 (ký) → p11 (tu luyện)
for _ in range(6):
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

# đường "chôn trả lại rồi đào lại"
o9 = mk()
call(o9, "/api/new", {"ten": "MP2", "nhom": "mon_phai"})
call(o9, "/api/chon", {"chi_so": 0})   # p02
call(o9, "/api/chon", {"chi_so": 1})   # p04
call(o9, "/api/chon", {"chi_so": 0})   # p06
r = call(o9, "/api/chon", {"chi_so": 1})  # chôn trả lại
check("chôn trả lại → p06b", r["doan_id"], "c1_p06b")
r = call(o9, "/api/chon", {"chi_so": 0})  # đào lại
st = call(o9, "/api/state")["trang_thai"]
check("đào lại vẫn nhận ngọc cốt", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)

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

print(f"\n{'='*46}\nKẾT QUẢ: {ok} đạt, {fail} hỏng")
sys.exit(1 if fail else 0)
