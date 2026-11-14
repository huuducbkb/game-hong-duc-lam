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
call(o3, "/api/chon", {"chi_so": 0})     # mua tin: -5 linh thạch
call(o3, "/api/chon", {"chi_so": 0})
st = call(o3, "/api/state")
check("sau 2 bước, so_lui = 2", st["so_lui"], 2)
check("linh thạch đã trừ", st["trang_thai"]["linh_thach"], 0)
r = call(o3, "/api/lui", {})
check("lùi 1 → đúng đoạn", r["doan_id"], "c1_h02")
check("lùi 1 có thông báo", bool(r.get("thong_bao")), True)
check("so_lui sau lùi = 1", call(o3, "/api/state")["so_lui"], 1)
r = call(o3, "/api/lui", {})
check("lùi 2 → về đầu", r["doan_id"], "c1_h01")
check("linh thạch hoàn lại 3", r["trang_thai"]["linh_thach"], 3)
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
# p02: bới vườn dược → đào ngọc cốt → giữ (chi_so 0)
r = call(o8, "/api/chon", {"chi_so": 0})
check("đào ngọc cốt", r["doan_id"], "c1_p02")
r = call(o8, "/api/chon", {"chi_so": 0})
st = call(o8, "/api/state")["trang_thai"]
check("nhận Ngọc cốt bí ẩn", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)
check("cờ co_ngoc_cot", "co_ngoc_cot" in st["co_su_kien"], True)
# p05 → p06 → p06b → p07 → p08 (ký khế ước) → p09 (tu luyện)
for _ in range(5):
    r = call(o8, "/api/chon", {"chi_so": 0})
check("tới đoạn tu luyện p09", r["doan_id"], "c1_p09")
r = call(o8, "/api/chon", {"chi_so": 0})
st = call(o8, "/api/state")["trang_thai"]
check("tu luyện đêm đầu → Luyện Khí tầng 2", st["canh_gioi"], "Luyện Khí tầng 2")
check("học Hợp Hoan hô hấp pháp", "Hợp Hoan hô hấp pháp" in st["ky_nang"], True)
r = call(o8, "/api/chon", {"chi_so": 0})
st = call(o8, "/api/state")["trang_thai"]
check("đột phá Luyện Khí tầng 3", st["canh_gioi"], "Luyện Khí tầng 3")
# đi tới hết chương
for _ in range(20):
    r = call(o8, "/api/chon", {"chi_so": 0})
    if r.get("ket_thuc"):
        break
check("kết riêng nhánh môn phái", r["doan_id"], "c1_p18")
st = call(o8, "/api/state")["trang_thai"]
check("gặp Hàn Lập, có hảo cảm", st["npc"].get("Hàn Lập", {}).get("hao_cam", 0) > 0, True)

# đường "chôn trả lại rồi đào lại"
o9 = mk()
call(o9, "/api/new", {"ten": "MP2", "nhom": "mon_phai"})
call(o9, "/api/chon", {"chi_so": 0})   # p02
r = call(o9, "/api/chon", {"chi_so": 1})  # chôn trả lại
check("chôn trả lại → p02b", r["doan_id"], "c1_p02b")
r = call(o9, "/api/chon", {"chi_so": 0})  # đào lại
st = call(o9, "/api/state")["trang_thai"]
check("đào lại vẫn nhận ngọc cốt", any(v["ten"] == "Ngọc cốt bí ẩn" for v in st["tui_do"]), True)

print(f"\n{'='*46}\nKẾT QUẢ: {ok} đạt, {fail} hỏng")
sys.exit(1 if fail else 0)
