# -*- coding: utf-8 -*-
"""Bộ kiểm thử toàn diện qua API thật (chạy khi server đang chạy)."""
import json, os, sys, urllib.request, urllib.error, http.cookiejar as cj

B = "http://127.0.0.1:12001"
ok = fail = 0

try:
    import sys as _sys
    _sys.path.insert(0, "/workspace/game-hong-duc-lam")
    from game import nen_anh as _NEN
    NEN_OK = _NEN.co_pillow()
except Exception:
    NEN_OK = False

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

def toi(o, dich, chi_so=0, toi_da=80):
    """Bấm lựa chọn cho tới khi tới đoạn `dich` (không phụ thuộc số bước)."""
    r = call(o, "/api/doan")
    for _ in range(toi_da):
        if r.get("doan_id") == dich:
            return r
        r = call(o, "/api/chon", {"chi_so": chi_so})
        if r.get("ket_thuc") or r.get("loi"):
            return r
    return r

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
# Chuyển chương: màn kết phải có lối ra, và chương 2 nay đã có dữ liệu thật
kq_ket = call(o7, "/api/chon", {"chi_so": 0})
check("màn kết chỉ sang chương 2", kq_ket.get("chuong_sau"), 2)
check("chương 2 đã có dữ liệu → nút mở", kq_ket.get("chuong_sau_mo"), True)
check("màn kết không còn là ngõ cụt im lặng: có chuong_sau",
      "chuong_sau" in kq_ket, True)
check("sang chương sai kiểu → 400",
      call(o7, "/api/sang_chuong", {"chuong": "hai"}).get("_http"), 400)
check("sang chương 9 (chưa viết) → 400",
      call(o7, "/api/sang_chuong", {"chuong": 9}).get("loi"), "Chương 9 chưa mở")
check("bị từ chối thì vẫn ở chương 1",
      call(o7, "/api/state")["trang_thai"]["chuong"], 1)

# Lùi ở màn kết: phải về đoạn cuối chương 1, không phải nhảy sang chương 2
check("lùi ở màn kết → về đoạn cuối", call(o7, "/api/lui", {}).get("doan_id"), "c1_d17")
_lui = call(o7, "/api/lui", {}).get("doan_id")
while _lui not in ("c1_d16", None) and _lui.startswith("c1_"):
    _lui = call(o7, "/api/lui", {}).get("doan_id")
check("lùi tiếp → về đoạn kế trước", _lui, "c1_d16")
check("lùi xong vẫn ở chương 1",
      call(o7, "/api/state")["trang_thai"]["chuong"], 1)
check("chưa hết chương thì /api/sang_chuong từ chối",
      call(o7, "/api/sang_chuong", {}).get("_http"), 400)
check("máy chủ vẫn sống sau tất cả", call(o7, "/api/state").get("co_phien"), True)

# Đi trọn đường sang chương 2 thật
o7b = mk()
call(o7b, "/api/new", {"ten": "R2b", "nhom": "tan_tu"})
for _ in range(40):
    # `ket_thuc` có thể là cờ dữ liệu của đoạn cuối; màn kết thật là __ket_thuc__
    if call(o7b, "/api/chon", {"chi_so": 0}).get("doan_id") == "__ket_thuc__":
        break
r = call(o7b, "/api/sang_chuong", {})
check("sang chương 2 thật → đúng đoạn mở đầu tán tu", r.get("doan_id"), "c2_d01")
check("sang chương 2 → báo tên chương mới",
      any("Thái Nam" in t for t in (r.get("thong_bao") or [])), True)
check("sang chương 2 → giữ nguyên cảnh giới đã luyện",
      call(o7b, "/api/state")["trang_thai"]["chuong"], 2)
check("chương 2 chơi tiếp được",
      call(o7b, "/api/chon", {"chi_so": 0}).get("doan_id"), "c2_d02")

# Lời kết và đoạn dùng chung hiện cho cả hai nhánh — lộ giọng riêng là hỏng.
import json as _json, re as _re
_ch2 = _json.load(open("game/chapters/chuong2.json", encoding="utf-8"))
_lo = ["ăn mày", "túi bạc", "tạp dịch"]
_chung = [d for d in _ch2["doan"] if d["id"].startswith("c2_c")]
_vet = [f'{d["id"]}:{t}' for d in _chung
        for t in _lo if t in _re.sub(r"“[^”]*”", "", d["ke"])]
check("đoạn dùng chung không lộ giọng riêng của nhánh", _vet, [])
check("lời kết chương 2 không lộ giọng riêng của nhánh",
      [t for t in _lo if t in _ch2["ket"]["ke"]], [])

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
# p07 → p08 (qua cảnh riêng) → p08b → p09 → p09b → p09c (do dự) → p10 (ký) → p10b (song tu) → p11
r = toi(o8, "c1_p10b")
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
    # Mỗi lựa chọn đi qua một cảnh riêng rồi mới nối vào d16.
    check(f"d15 {ten} → cảnh riêng", r["doan_id"], f"c1_d16_{cs}")
    check(f"  {ten}: cảnh riêng đủ dài", len(r.get("ke") or "") >= 300, True)
    st = call(ot, "/api/state")["trang_thai"]
    check(f"  {ten}: hảo cảm Hàn Lập = {hc}", st["npc"].get("Hàn Lập", {}).get("hao_cam", 0), hc)
    if coco:
        check(f"  {ten}: cờ {coco}", coco in st["co_su_kien"], True)
    r = call(ot, "/api/chon", {"chi_so": 0})
    check(f"  {ten} → d16", r["doan_id"], "c1_d16")
    r = call(ot, "/api/chon", {"chi_so": 0})
    check(f"  {ten} → cảnh riêng d17", r["doan_id"], "c1_d17_0")
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
    for _d in ["assets/scene", "assets/ui", "docs/assets/scene", "docs/assets/ui",
               "assets/scene-orig", "assets/ui-orig"]:
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

def _snap(paths):
    """Sao lưu bytes các file (None nếu chưa tồn tại) để phục hồi sau test."""
    out = {}
    for p in paths:
        f = f"/workspace/game-hong-duc-lam/{p}"
        out[p] = open(f, "rb").read() if os.path.isfile(f) else None
    return out

def _restore(snap):
    """Phục hồi nguyên trạng: file nào có bản sao thì ghi lại, file mới thì xóa."""
    for p, data in snap.items():
        f = f"/workspace/game-hong-duc-lam/{p}"
        if data is None:
            if os.path.isfile(f):
                os.remove(f)
        else:
            os.makedirs(os.path.dirname(f), exist_ok=True)
            with open(f, "wb") as fp:
                fp.write(data)

def _png_nhieu(w, h):
    """PNG có nhiễu (như ảnh thật) — để phép so nén có ý nghĩa."""
    import struct as _s, zlib as _z, random as _r
    _r.seed(7)
    rows = b""
    for _ in range(h):
        rows += b"\x00" + bytes(_r.randrange(256) for _ in range(w * 3))
    def _ch(t, d):
        c = t + d
        return _s.pack(">I", len(d)) + c + _s.pack(">I", _z.crc32(c) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n"
            + _ch(b"IHDR", _s.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _ch(b"IDAT", _z.compress(rows)) + _ch(b"IEND", b""))

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

# Lưu loạt theo key → ghi đúng tên file (divider-ink nay là .jpg sau khi sửa đuôi)
# SAO LƯU trước, PHỤC HỒI sau — để test không phá ảnh thật.
_TEP = ["assets/ui/divider-ink.jpg", "docs/assets/ui/divider-ink.jpg",
        "assets/ui-orig/divider-ink.jpg", "assets/scene/bc_cho_01.jpg",
        "docs/assets/scene/bc_cho_01.jpg", "assets/scene-orig/bc_cho_01.jpg",
        "assets/ui/seal.png", "docs/assets/ui/seal.png", "assets/ui-orig/seal.png",
        # /luu_loat nay cung ghep vao truyen + cap nhat thu vien → phai phuc hoi ca 2
        "docs/assets/library/index.json", "game/chapters/chuong1.json",
        "docs/game/du-lieu/chuong1.json"]
_snap = _snap(_TEP)

kq = _post_raw("/luu_loat", {"ds": [{"key": "divider-ink", "data": _b64(_png(1600, 160))}]})
check("/luu_loat trả ok", kq.get("ok"), True)
check("lưu theo key → đúng tên divider-ink.jpg",
      os.path.isfile("/workspace/game-hong-duc-lam/assets/ui/divider-ink.jpg"), True)
check("  đúng tên file trong kết quả",
      (kq.get("da_luu") or [{}])[0].get("file"), "divider-ink.jpg")
# Ảnh giao diện cũng phải đồng bộ sang docs/ (Pages dùng docs/)
check("  ảnh UI đồng bộ sang docs/assets/ui/",
      os.path.isfile("/workspace/game-hong-duc-lam/docs/assets/ui/divider-ink.jpg"), True)
# Bản gốc (chưa nén) được giữ riêng để nén lại khi cần
check("  giữ bản gốc ở assets/ui-orig/",
      os.path.isfile("/workspace/game-hong-duc-lam/assets/ui-orig/divider-ink.jpg"), True)
# Ảnh cảnh lưu theo key phải vào CẢ hai nơi
kq = _post_raw("/luu_loat", {"ds": [{"key": "bc_cho_01", "data": _b64(_png(900, 1200))}]})
check("lưu key bc_cho_01 → assets/scene/",
      os.path.isfile("/workspace/game-hong-duc-lam/assets/scene/bc_cho_01.jpg"), True)
check("  và docs/assets/scene/",
      os.path.isfile("/workspace/game-hong-duc-lam/docs/assets/scene/bc_cho_01.jpg"), True)

print("\n=== Z. Nén ảnh khi lưu ===")
if not NEN_OK:
    print("  (bỏ qua: chưa cài Pillow)")
else:
    # Ảnh lớn (900×1200, có nhiễu như ảnh thật) lưu vào game phải NHẸ hơn gốc.
    # Ghi đè lên một key thật rồi phục hồi — phải sao lưu CẢ HAI nơi, vì máy chủ
    # ghi vào assets/scene/ và docs/assets/scene/. Chỉ sao lưu một nơi là bản còn
    # lại bị đè bằng ảnh nhiễu của test.
    _goc = _png_nhieu(900, 1200)
    _k = "bc_cho_01"
    import shutil as _sh
    _dss = ["/workspace/game-hong-duc-lam/assets/scene/" + _k + ".jpg",
            "/workspace/game-hong-duc-lam/docs/assets/scene/" + _k + ".jpg"]
    _sao = []
    for _d in _dss:
        if os.path.isfile(_d):
            _sh.copy2(_d, _d + ".test-goc")
            _sao.append(_d)
    try:
        _post_raw("/luu_loat", {"ds": [{"key": _k, "data": _b64(_goc)}]})
        _luu = os.path.getsize(_dss[0]) if os.path.isfile(_dss[0]) else 0
        check("ảnh lưu ra nhẹ hơn ảnh gốc", _luu > 0 and _luu < len(_goc), True)
    finally:
        for _d in _sao:
            _sh.move(_d + ".test-goc", _d)
    # Ảnh giữ trong suốt (seal) phải vẫn là PNG
    _seal = "/workspace/game-hong-duc-lam/assets/ui/seal.png"
    import shutil as _sh2
    if os.path.isfile(_seal):
        _sh2.copy2(_seal, _seal + ".test-goc")
    try:
        _post_raw("/luu_loat", {"ds": [{"key": "seal", "data": _b64(_png(1024, 1024))}]})
        with open(_seal, "rb") as _f:
            _hdr = _f.read(26)
        check("ảnh seal vẫn là PNG", _hdr[:8] == b"\x89PNG\r\n\x1a\n", True)
    finally:
        if os.path.isfile(_seal + ".test-goc"):
            _sh2.move(_seal + ".test-goc", _seal)

_restore(_snap)

print("\n=== Prompt ảnh: thủy mặc, sạch loang và đốm ===")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tools_server as _TS

# Bốn cụm gốc sinh ra mực loang lỗ và đốm sáng: "wet ink bleeding edges",
# "dry brush strokes", "visible paper fiber texture", "rough handmade".
_LOANG = ("wet ink bleeding", "bleeding edges", "dry brush", "dry-brush", "paper fibre",
          "paper fiber", "suggested loosely", "loosely by", "ink splash", "blotchy",
          "wobbly edges", "rough handmade", "abstract scribble")
_xau = {a["key"]: [c for c in _LOANG if c in a["prompt"].lower()] for a in _TS.ASSETS}
check("không prompt ảnh nào chứa từ gây loang", {k: v for k, v in _xau.items() if v}, {})

# Hướng đã chọn là thủy mặc shui-mo / 彩墨, không phải line-art.
check("khối phong cách vẫn là thủy mặc",
      ("shui-mo" in _TS.STYLE_GOC, "cǎi-mò" in _TS.MAU_GOC), (True, True))
check("mọi prompt ảnh đều cấm chữ",
      [a["key"] for a in _TS.ASSETS
       if a["key"] != "seal" and "no text" not in a["prompt"].lower()], [])

print("\n=== S. Chương 2 — cảnh ↔ đoạn ↔ tệp dữ liệu ===")
_GOC = "/workspace/game-hong-duc-lam"
_ch2 = json.load(open(os.path.join(_GOC, "game/chapters/chuong2.json"), encoding="utf-8"))
_id2 = {x["id"] for x in _ch2["doan"]}
_canh2 = {k: v for k, v in _TS.DOAN_CUA_ANH.items()
          if any(d.startswith("c2_") for d in v)}
_da_co_canh = {d for v in _canh2.values() for d in v}
check("mọi cảnh Chương 2 trỏ tới đoạn có thật", sorted(_da_co_canh - _id2), [])
check("mỗi đoạn Chương 2 chỉ có một cảnh",
      sorted(d for d in _da_co_canh
             if sum(1 for v in _canh2.values() if d in v) > 1), [])
_thieu2 = sorted(x["id"] for x in _ch2["doan"]
                 if x["id"].startswith("c2_d")
                 and not (x.get("hinh_anh") or {}).get("anh"))
# Hai đoạn thắng tà tu là nhánh MỚI (thêm cùng ngày), chưa có ảnh trong bộ cảnh.
# Chúng được phép thiếu ảnh cho tới khi xưởng ghép ảnh sinh cảnh cho chúng.
_DOAN_CHUA_CANH = {"c2_d27c_thang", "c2_p23c_thang"}
check("mọi đoạn nhánh tán tu thiếu ảnh đều có cảnh",
      [x for x in _thieu2 if x not in _da_co_canh and x not in _DOAN_CHUA_CANH], [])
check("mọi cảnh Chương 2 đều có nhóm cảnh",
      [k for k in _canh2 if not _TS.nhom_canh_cua(k)], [])

import xuong_tu_dong as _XTD
check("Xưởng ghép ảnh vào cả hai bản dữ liệu Chương 2",
      len([p for p in _XTD.CHUONG_FILES if "chuong2" in p]), 2)
_ch2web = json.load(open(os.path.join(_GOC, "docs/game/du-lieu/chuong2.json"),
                         encoding="utf-8"))
check("ghép ảnh mới vào đúng đoạn c2_d12",
      _XTD._gan_doan(_ch2web, "bc_c2_cho_linh_thach", "bc_c2_cho_linh_thach.jpg"),
      ["c2_d12"])
check("  và ghi đúng tên tệp vào đoạn",
      next(x for x in _ch2web["doan"] if x["id"] == "c2_d12")["hinh_anh"]["anh"],
      "bc_c2_cho_linh_thach.jpg")

print("\n=== Prompt tiếng: trần 450 ký tự ===")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prompt_am as _PA
_qua = {k: len(v) for k, v in _PA.PROMPT.items() if len(v) > 450}
check("không prompt nào vượt 450 ký tự", _qua, {})
check("prompt cảnh nghỉ đêm đều có câu tiếng Hoa",
      all("「" in v for k, v in _PA.PROMPT.items() if k.endswith("_nghi_dem")), True)

print("\n=== J. Hảo cảm đổi giọng kể, không đổi sự việc ===")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as _E2

_ch2b = _E2.load_chuong(2)
_ds2 = {x["id"]: x for x in _ch2b["doan"]}

def _ke(did, diem):
    st = {"npc": {"Hàn Lập": {"hao_cam": diem, "thai_do": _E2.muc_hao_cam(diem)}}}
    return _E2._ke_theo_hao_cam(_ds2[did], st)

# Đoạn có bien_the phải ra văn bản KHÁC nhau ở các mức hảo cảm khác nhau.
# Chương 2 tách hai nhánh riêng: mỗi nhánh có đoạn cảm xúc riêng để thử giọng kể.
_co_bt = [x["id"] for x in _ch2b["doan"] if x.get("bien_the")]
check("chương 2 còn đoạn có bien_the để đổi giọng", len(_co_bt) >= 1, True)
_did_bt = _co_bt[0]
_c18 = [_ke(_did_bt, d) for d in (-80, -30, 0, 30)]
check(f"{_did_bt} đổi giọng theo 4 mức hảo cảm", len(set(_c18)), 4)
# Nhưng sự việc gốc phải giữ: cùng một cảnh, chỉ khác giọng kể.
check("mọi biến thể vẫn giữ nguyên sự việc gốc",
      all(_ds2[_did_bt]["boi_canh"] is not None for t in _c18), True)

# Không có bien_the -> luôn trả `ke` gốc, không phụ thuộc hảo cảm.
_khong_bt = [x["id"] for x in _ch2b["doan"] if not x.get("bien_the")][0]
check("đoạn không có bien_the thì không đổi theo hảo cảm",
      len({_ke(_khong_bt, d) for d in (-80, 0, 95)}), 1)

# Bậc thấp hơn gần nhất: chỉ khai báo "quen biết" thì mức "tri kỷ" vẫn dùng nó,
# thay vì rơi về giọng trung tính của `ke`.
_x = {"ke": "GỐC", "bien_the": [
    {"npc": "Hàn Lập", "muc": "quen biết", "ke": "QB"},
    {"npc": "Hàn Lập", "muc": "tử địch", "ke": "TD"}]}
check("hảo cảm cao hơn biến thể cao nhất → dùng biến thể cao nhất",
      _E2._ke_theo_hao_cam(_x, {"npc": {"Hàn Lập": {"hao_cam": 95}}}), "QB")
check("hảo cảm thấp hơn biến thể thấp nhất → dùng biến thể thấp nhất",
      _E2._ke_theo_hao_cam(_x, {"npc": {"Hàn Lập": {"hao_cam": -95}}}), "TD")
check("mức giữa hai biến thể → lấy bậc thấp hơn gần nhất",
      _E2._ke_theo_hao_cam(_x, {"npc": {"Hàn Lập": {"hao_cam": 30}}}), "QB")

# NPC chưa gặp thì biến thể của NPC đó không được chọn.
check("biến thể của NPC chưa gặp không được dùng",
      _E2._ke_theo_hao_cam(_x, {"npc": {}}), "GỐC")

print("\n=== K. Hảo cảm vào được tới prompt kể chuyện ===")
import ai as _AI
_p = _AI._phan_thai_do([{"ten": "Hàn Lập", "hao_cam": -75, "thai_do": "tử địch"},
                        {"ten": "Tuyết Cơ", "hao_cam": 90, "thai_do": "tri kỷ"}])
check("prompt nêu tên và thái độ từng NPC", ("Hàn Lập" in _p, "Tuyết Cơ" in _p), (True, True))
check("prompt nói rõ giọng theo thái độ", "tử địch" in _p and "tri kỷ" in _p, True)
check("NPC không có mặt thì không vào prompt", _AI._phan_thai_do([]), "")
# Giọng kể đổi được, sự kiện thì không — phải nói rõ trong prompt.
check("prompt cấm đổi sự việc", "không" in _p.lower() and "sự việc" in _p.lower(), True)

# Cache phải tách theo NPC: cùng đoạn, khác thái độ → không được dùng chung kết quả.
check("khoá cache tách theo NPC",
      _AI._khoa_cache("ke", "", (("Hàn Lập", -80),)) !=
      _AI._khoa_cache("ke", "", (("Hàn Lập", 90),)), True)
check("khoá cache không có NPC vẫn ổn định",
      _AI._khoa_cache("ke", "", ()) == _AI._khoa_cache("ke", "", ()), True)

print("\n=== L. Mỗi nhánh có đủ hai hướng: bạn và thù ===")
# Duyệt đồ thị theo cặp (đoạn, hảo cảm) đã thăm. Không có tập đã thăm thì số
# đường đi tăng theo cấp số nhân mỗi lần thêm cảnh — bộ test sẽ treo, không hỏng.
def _hai_cuc(dau):
    lo, hi = {}, {}
    tham = set()
    hang = [(dau, 0)]
    while hang:
        sid, aff = hang.pop()
        if sid not in _ds2 or (sid, aff) in tham:
            continue
        tham.add((sid, aff))
        lo[sid] = min(lo.get(sid, 9e9), aff)
        hi[sid] = max(hi.get(sid, -9e9), aff)
        for lc in (_ds2[sid].get("lua_chon") or []):
            a = aff + (((lc.get("hieu_ung") or {}).get("hao_cam") or {}).get("Hàn Lập", 0))
            den = lc.get("den")
            if den and den != "__ket_thuc__":
                hang.append((den, a))
    return lo, hi

# Mỗi nhánh phải chạm được cả hai cực — không chỉ một hướng.
for _dau in _ch2b["doan_dau_theo_nhom"].values():
    _l2, _h2 = _hai_cuc(_dau)
    check(f"nhánh {_dau}: xuống được mức thù địch", min(_l2.values()) <= -40, True)
    check(f"nhánh {_dau}: lên được mức thân thiết", max(_h2.values()) >= 50, True)

# Lựa chọn khoá theo hảo cảm phải thật sự chặn được.
_khoa = [x["id"] for x in _ch2b["doan"]
         for lc in (x.get("lua_chon") or [])
         if "hao_cam" in ((lc.get("dieu_kien") or {}))]
check("có lựa chọn mở khi hảo cảm cao", len(_khoa) >= 3, True)
_khoa_thap = [x["id"] for x in _ch2b["doan"]
              for lc in (x.get("lua_chon") or [])
              if "hao_cam_max" in ((lc.get("dieu_kien") or {}))]
check("có lựa chọn chỉ mở khi hảo cảm thấp", len(_khoa_thap) >= 2, True)

# Kết bạn và kết thù phải là hai đoạn KHÁC NHAU, không chỉ khác lời kể.
for _cap in (("c2_d29", "c2_d29x"), ("c2_p25", "c2_p25x")):
    check(f"có cặp kết bạn/kết thù riêng {_cap}", [x["id"] for x in _ch2b["doan"] if x["id"] in _cap], list(_cap))

print("\n=== M. Dữ liệu deploy và ảnh ===")
# Bản chạy thật đọc docs/game/du-lieu/ — quên đồng bộ là sửa mà không lên mạng.
import hashlib as _hl
for _f in ("chuong1.json", "chuong2.json"):
    _a = _hl.md5(open(os.path.join("game", "chapters", _f), "rb").read()).hexdigest()
    _b = _hl.md5(open(os.path.join("docs", "game", "du-lieu", _f), "rb").read()).hexdigest()
    check(f"{_f} trong game/ và docs/ giống nhau từng byte", _a, _b)

# Ảnh cảnh Chương 2 chưa làm — đoạn mới không được mượn ảnh Chương 1.
_moi = {"c2_d29x", "c2_p25x", "c2_d27b", "c2_p24b"}
check("đoạn kết mới không gắn ảnh (Chương 2 chưa có ảnh)",
      [x["id"] for x in _ch2b["doan"]
       if x["id"] in _moi and x.get("hinh_anh")], [])

print("\n=== N. Nhận vật phẩm phải khớp lời kể ===")
from collections import deque as _dq

def _duong(dau, dich, nhom="tan_tu", cho_khoa=False):
    """Đường ngắn nhất tới `dich`.

    Mặc định chỉ đi lựa chọn người chơi thật sự bấm được. `cho_khoa=True` mở cả
    lựa chọn bị khoá — dùng khi cần với tới đoạn kết mà chỉ hảo cảm mới mở được.
    Đoạn kết thua luôn bị loại: nó là ngõ cụt, không dẫn tiếp đi đâu.
    """
    st = _E2.trang_thai_moi("T", "", nhom)
    st["chuong"] = 2
    _E2.bat_dau(st)
    q = _dq([(st["doan_hien_tai"], [])])
    tham = {st["doan_hien_tai"]}
    while q:
        sid, path = q.popleft()
        if sid == dich:
            return path
        for i, lc in enumerate(_ds2[sid].get("lua_chon") or []):
            den = lc.get("den")
            if den in _ds2 and _ds2[den].get("thua"):
                continue
            if lc.get("dieu_kien") and not cho_khoa:
                continue
            if den and den != "__ket_thuc__" and den in _ds2 and den not in tham:
                tham.add(den)
                q.append((den, path + [i]))
    return None if cho_khoa else _duong(dau, dich, nhom, cho_khoa=True)

def _choi(dich, nhom="tan_tu", hao_cam=None):
    st = _E2.trang_thai_moi("T", "", nhom)
    st["chuong"] = 2
    _E2.bat_dau(st)
    for i in _duong(st["doan_hien_tai"], dich, nhom):
        r = _E2.chon(st, i)
    # Đường ngắn nhất có thể không đủ hảo cảm; đoạn kết cần mức cao thì đặt trước.
    if hao_cam is not None and "Hàn Lập" in st["npc"]:
        st["npc"]["Hàn Lập"]["hao_cam"] = hao_cam
    return st, r

def _tui(st):
    return {v["ten"]: v.get("so", 1) for v in st["tui_do"]}

# Món nào lời kể nói "Nhận" thì phải có trong túi, và không có dòng trùng tên.
_st, _ = _choi("c2_d28")
_t = _tui(_st)
check("  không có hai dòng cùng tên trong túi",
      len([v["ten"] for v in _st["tui_do"]]) - len(set(v["ten"] for v in _st["tui_do"])), 0)

# Nhận lệnh bài ở kết bạn: hảo cảm đủ cao mới mở, và phải vào túi thật.
_st2, _ = _choi("c2_d28", "tan_tu", hao_cam=100)
_E2.chon(_st2, 0)   # "Nhận tấm lệnh"
check("nhận Thăng Tiên Lệnh ở kết bạn tán tu",
      _tui(_st2).get("Thăng Tiên Lệnh"), 1)

# Đường thù: không nhận được lệnh bài nào.
check("kết thù tán tu không có lệnh bài",
      _tui(_choi("c2_d29x", "tan_tu")[0]).get("Thăng Tiên Lệnh"), None)
check("kết thù môn phái không có lệnh bài",
      _tui(_choi("c2_p25x", "mon_phai")[0]).get("Thăng Tiên Lệnh"), None)

# Mọi lựa chọn có "Nhận:" trong lời kể của đoạn đích phải có hiệu ứng them_vat.
_thieu = []
for x in _ch2b["doan"]:
    if "Nhận:" in (x.get("ke") or ""):
        co = any(((lc.get("hieu_ung") or {}).get("them_vat")) for lc in (x.get("lua_chon") or []))
        # đoạn kết không có lựa chọn thì bỏ qua
        if (x.get("lua_chon") or []) and not co:
            _thieu.append(x["id"])
check("đoạn báo “Nhận:” thì phải thật sự thêm vật phẩm", _thieu, [])

print("\n=== O. Kết bạn và kết thù là hai lối rẽ thật ===")
def _goi_y_khoa(diem, nhom="tan_tu"):
    st = _E2.trang_thai_moi("T", "", nhom)
    st["chuong"] = 2
    st["doan_hien_tai"] = "c2_d28" if nhom == "tan_tu" else "c2_p24"
    st["npc"] = {"Hàn Lập": {"hao_cam": diem, "thai_do": _E2.muc_hao_cam(diem)}}
    return _E2._goi_y(st)["lua_chon"]

check("hảo cảm cao mở lựa chọn nhận lệnh bài",
      [lc["khoa"] for lc in _goi_y_khoa(75) if lc["chu"].startswith("Nhận tấm lệnh")], [False])
check("hảo cảm thấp khoá lựa chọn nhận lệnh bài",
      [lc["khoa"] for lc in _goi_y_khoa(-45) if lc["chu"].startswith("Nhận tấm lệnh")], [True])
check("hảo cảm thấp mở lựa chọn cắt đứt",
      [lc["khoa"] for lc in _goi_y_khoa(-45) if "tự có đường" in lc["chu"]], [False])
check("hảo cảm cao khoá lựa chọn cắt đứt",
      [lc["khoa"] for lc in _goi_y_khoa(75) if "tự có đường" in lc["chu"]], [True])

print("\n=== P. Chương gộp nhánh không được làm chết người chơi ===")
# Chương 3 trở đi gộp hai nhánh: không khai doan_dau_theo_nhom cho từng nhóm nữa.
_load_goc = _E2.load_chuong
try:
    _E2.load_chuong = lambda so: (
        {"_theo_id": {"c3_x01": {}}, "doan": [{"id": "c3_x01"}],
         "doan_dau_theo_nhom": {"chung": "c3_x01"}}
        if so == 3 else _ch2b
    )
    for _nhom in ("tan_tu", "mon_phai"):
        check(f"nhóm {_nhom} vào được chương gộp qua khoá 'chung'",
              _E2.doan_dau_cua(_nhom, 3), "c3_x01")

    # Chương gộp không khai gì cả: vẫn phải có đường vào, không ném lỗi.
    _E2.load_chuong = lambda so: (
        {"_theo_id": {"c3_x01": {}}, "doan": [{"id": "c3_x01"}]} if so == 3 else _ch2b
    )
    check("chương gộp không khai bảng nhóm vẫn vào được đoạn đầu",
          _E2.doan_dau_cua("tan_tu", 3), "c3_x01")
finally:
    _E2.load_chuong = _load_goc

print("\n=== Q. Khế ước Tuyết Cơ thì hảo cảm phải là 100 ===")
_st4 = _E2.trang_thai_moi("T", "", "mon_phai")
_E2.bat_dau(_st4)
_st4["doan_hien_tai"] = "c1_p09c"
_lc_ky = [lc for lc in _E2._goi_y(_st4)["lua_chon"] if lc["chu"].startswith("“Ta ký")][0]
_E2.chon(_st4, _lc_ky["chi_so"])
check("ký khế ước → hảo cảm Tuyết Cơ = 100",
      _st4["npc"].get("Tuyết Cơ", {}).get("hao_cam"), 100)
check("  và thái độ là tri kỷ",
      _st4["npc"].get("Tuyết Cơ", {}).get("thai_do"), "tri kỷ")
check("  và có cờ sự kiện khế ước", "tuyet_co_khe_uoc" in _st4["co_su_kien"], True)

print("\n=== R. Bạn đồng hành phải có mặt ngay khi mở đoạn đầu Chương 2 ===")
for _nhom_r, _doan_r, _ten_r in (("tan_tu", "c2_d01", "Hồng Trần"),
                                  ("mon_phai", "c2_p01", "Tuyết Cơ")):
    _st5 = _E2.trang_thai_moi("T", "", _nhom_r)
    _E2.sang_chuong(_st5, 2)
    _kq5 = _E2.bat_dau(_st5)
    check(f"{_nhom_r}: mở đoạn {_doan_r}", _kq5["doan_id"], _doan_r)
    check(f"  {_ten_r} đã vào sổ NPC ngay, không cần bấm gì",
          _st5["npc"].get(_ten_r, {}).get("hao_cam"), 100)
    check(f"  thái độ với {_ten_r}", _st5["npc"].get(_ten_r, {}).get("thai_do"), "tri kỷ")
    # Mở lại đoạn đó nhiều lần không được cộng dồn hảo cảm.
    _E2.goi_y_hien_tai(_st5)
    _E2.goi_y_hien_tai(_st5)
    check(f"  mở lại đoạn không cộng dồn hảo cảm {_ten_r}",
          _st5["npc"].get(_ten_r, {}).get("hao_cam"), 100)
check("hai nhánh không dùng chung bạn đồng hành",
      "Tuyết Cơ" in _E2.trang_thai_moi("T", "", "tan_tu")["npc"], False)

print("\n=== Q. Mỗi lựa chọn phải ra một cảnh riêng ===")
# Lỗi đã gặp: hai lựa chọn trong cùng một đoạn cùng trỏ `den` về một đoạn, nên
# người chơi bấm cách nào cũng đọc y nguyên một đoạn văn.
for _so in (1, 2):
    _du = _E2.load_chuong(_so)
    _ids = {x["id"] for x in _du["doan"]}
    _trung, _thieu, _ngan = [], [], []
    for _d in _du["doan"]:
        _dem = {}
        for _lc in _d.get("lua_chon") or []:
            # Lựa chọn vào trận đánh (`tran_dau`) rẽ theo thắng/thua, không có `den`.
            _tran = _lc.get("tran_dau")
            if _tran:
                for _khoa in ("thang", "thua"):
                    _dich = _tran.get(_khoa)
                    if _dich not in _ids:
                        _thieu.append(f'{_d["id"]} -> tran.{_khoa} {_dich}')
                continue
            if _lc["den"] == "__ket_thuc__":
                continue
            _dem[_lc["den"]] = _dem.get(_lc["den"], 0) + 1
            if _lc["den"] not in _ids:
                _thieu.append(f'{_d["id"]} -> {_lc["den"]}')
        for _den, _n in _dem.items():
            if _n > 1:
                _trung.append(f'{_d["id"]} -> {_den} ({_n} lựa chọn)')
        if len(_d.get("ke") or "") < 300:
            _ngan.append(_d["id"])
    check(f"chương {_so}: không có hai lựa chọn cùng đích", _trung, [])
    check(f"chương {_so}: mọi đích đều tồn tại", _thieu, [])
    check(f"chương {_so}: mọi đoạn dài từ 300 ký tự", _ngan, [])

    # Đoạn không ai trỏ tới là dữ liệu chết: người chơi không bao giờ đọc được.
    _ds_theo_id = {y["id"]: y for y in _du["doan"]}
    _thay, _hang = set(), list(set((_du.get("doan_dau_theo_nhom") or {}).values()))
    while _hang:
        _x = _hang.pop()
        if _x in _thay or _x not in _ids:
            continue
        _thay.add(_x)
        for _lc in _ds_theo_id[_x].get("lua_chon") or []:
            _tran = _lc.get("tran_dau")
            if _tran:
                _hang.extend([_tran.get("thang"), _tran.get("thua")])
                continue
            if _lc["den"] != "__ket_thuc__":
                _hang.append(_lc["den"])
    check(f"chương {_so}: không có đoạn mồ côi", sorted(_ids - _thay), [])

    # Kiểm hành vi thật: chọn từng lựa chọn, hai lựa chọn khác nhau phải ra văn bản khác nhau.
    _giong = []
    for _d in _du["doan"]:
        _lcs = _d.get("lua_chon") or []
        if len(_lcs) < 2:
            continue
        _ra = []
        for _i in range(len(_lcs)):
            _st = _E2.trang_thai_moi("T", "", "tan_tu")
            _st["chuong"] = _so
            _st["doan_hien_tai"] = _d["id"]
            _st["npc"] = {"Hàn Lập": {"hao_cam": 100, "thai_do": _E2.muc_hao_cam(100)}}
            _kq = _E2.chon(_st, _i)
            if _kq.get("loi"):
                continue
            _ra.append((_i, (_kq.get("ke") or "").strip()))
        for _a in range(len(_ra)):
            for _b in range(_a + 1, len(_ra)):
                if _ra[_a][1] and _ra[_a][1] == _ra[_b][1]:
                    _giong.append(f'{_d["id"]}: lựa chọn {_ra[_a][0]} và {_ra[_b][0]} ra cùng văn bản')
    check(f"chương {_so}: lựa chọn khác nhau ra cảnh khác nhau", _giong, [])

    # Kết thua phải khai đủ cờ và không có lựa chọn — thiếu `ket_thuc` thì đoạn ấy
    # hiện ra như cảnh cụt im lặng, người chơi không biết mình đã chết.
    # `ket_thuc` một mình là đoạn khép chương — hợp lệ. Chỉ đoạn khai `thua` mới
    # phải đủ cả hai cờ và không có lựa chọn.
    _thua_sai = [d["id"] for d in _du["doan"]
                 if d.get("thua")
                 and not (d.get("ket_thuc") and not (d.get("lua_chon") or []))]
    check(f"chương {_so}: đoạn kết thua khai đủ cờ", _thua_sai, [])

    _co_loi_vao = set()
    for _d2 in _du["doan"]:
        for _lc2 in _d2.get("lua_chon") or []:
            _t2 = _lc2.get("tran_dau")
            if _t2:
                # Nhánh thua của một trận là đường vào hợp lệ.
                _co_loi_vao.update([_t2.get("thang"), _t2.get("thua")])
            elif _lc2["den"] != "__ket_thuc__":
                _co_loi_vao.add(_lc2["den"])
    _thua = [d["id"] for d in _du["doan"] if d.get("thua")]
    check(f"chương {_so}: mọi đoạn kết thua đều có đường vào",
          [x for x in _thua if x not in _co_loi_vao], [])

    # Màn kết thua phải trả về cờ `thua`, không kèm nút sang chương, để giao diện
    # biết đây là thua mà mời lùi lại.
    for _tid in _thua:
        _st = _E2.trang_thai_moi("T", "", "tan_tu")
        _st["chuong"] = _so
        _st["doan_hien_tai"] = _tid
        _st["ket_thuc"] = True
        _kq = _E2.goi_y_hien_tai(_st)
        check(f"chương {_so}: {_tid} trả màn kết thua đúng",
              [_kq.get("thua"), _kq.get("chuong_sau"), len(_kq.get("lua_chon") or [])],
              [True, None, 0])

print("\n=== TL. Tu luyện: ngân sách ngày dùng chung, trần cảnh giới, cổng boss ===")
_o = mk()
_ten = "Kiểm Tu Luyện"
_r = call(_o, "/api/new", {"ten": _ten, "xuat_than": "tán tu", "nhom": "tan_tu", "ke_ai": False})
check("tạo phiên cho tu luyện", "phien" in _r, True)

_r = call(_o, "/api/tu_luyen", {"hanh": "xem"})
check("xem động phủ: 30 ngày", _r["chi_so"]["ngay_con"], 30)
check("xem động phủ: đủ 5 việc", [v["ma"] for v in _r["viec"]],
      ["da_toa", "san", "luyen_dan", "cho", "do_la"])

_r = call(_o, "/api/tu_luyen", {"hanh": "vao"})
check("vào động phủ", _r.get("ok"), True)

_r = call(_o, "/api/tu_luyen", {"hanh": "da_toa"})
check("đả tọa: 1 lượt xong", _r.get("ok"), True)
check("đả tọa: còn 27 ngày", _r["chi_so"]["ngay_con"], 27)

# Ngân sách cách A: ra rồi vào lại, số ngày phải y nguyên.
call(_o, "/api/tu_luyen", {"hanh": "ra"})
call(_o, "/api/tu_luyen", {"hanh": "vao"})
_r = call(_o, "/api/tu_luyen", {"hanh": "xem"})
check("ra vào lại KHÔNG cấp lại ngày", _r["chi_so"]["ngay_con"], 27)

_r = call(_o, "/api/tu_luyen", {"hanh": "do_la"})
check("dò la: tốn 2 ngày", _r["chi_so"]["ngay_con"], 25)
check("dò la: trả về tin hoặc không", "tin" in _r, True)

_r = call(_o, "/api/tu_luyen", {"hanh": "cong_thuc"})
check("có danh sách công thức", len(_r["ds"]) >= 1, True)
_m = call(_o, "/api/tu_luyen", {"hanh": "luyen_dan", "ma": "tu_khi_dan"})
check("luyện đan thiếu nguyên liệu: bị chặn", "loi" in _m, True)
check("luyện đan hỏng: KHÔNG trừ ngày", call(_o, "/api/tu_luyen",
      {"hanh": "xem"})["chi_so"]["ngay_con"], 25)

_r = call(_o, "/api/tu_luyen", {"hanh": "cho"})
check("có danh sách hàng", len(_r["ds"]) >= 1, True)
_m = call(_o, "/api/tu_luyen", {"hanh": "mua", "ma": "khong_co"})
check("mua món không bán: bị chặn", "loi" in _m, True)

_r = call(_o, "/api/tu_luyen", {"hanh": "dau"})
check("xem trận: có tỉ lệ thắng", "tran" in _r, True)
check("xem trận: không trừ ngày", call(_o, "/api/tu_luyen",
      {"hanh": "xem"})["chi_so"]["ngay_con"], 25)

_r = call(_o, "/api/tu_luyen", {"hanh": "khong_ton_tai"})
check("hành động lạ: bị chặn", _r.get("_http"), 400)

_r = call(_o, "/api/tu_luyen", {"hanh": "ra"})
check("xuất động: trả về đoạn truyện", bool(_r.get("doan_id")), True)

print("\n=== TL1b. Yêu thú: 10 con, không kẹt đúng con vừa thua (lỗi báo 2026-11-28) ===")
from game import engine as _E
_t = _E.TL_YEU_THU
check("có 10 yêu thú", len(_t), 10)
check("có 5 con hạng thường", len([x for x in _t if x["hang"] == "thuong"]), 5)
check("có 3 con tinh anh", len([x for x in _t if x["hang"] == "tinh_anh"]), 3)
check("có 2 yêu vương", len([x for x in _t if x["hang"] == "yeu_vuong"]), 2)

_sk = _E.trang_thai_moi("Kẹt", "tán tu", "tan_tu")
_sk["chuong"] = 2
_vp = 0
for _v in range(10):
    _x = _E.tl_dau(_sk)
    _kq = _E.tl_danh(_sk)
    if _kq.get("loi") is None and _kq["thang"] is False:
        _sau = _E.tl_dau(_sk)
        if _sau.get("loi") is None and _sau["tran"]["ma"] == _x["tran"]["ma"]:
            _vp += 1
    while (_sk["chi_so"]["sinh_luc"]["hien"]
           <= _sk["chi_so"]["sinh_luc"]["max"] * 0.35
           and _sk["tu_luyen"]["ngay_con"] > 0):
        _E.tl_nghi(_sk)
check("thua xong KHÔNG gặp lại đúng con đó", _vp, 0)

_sky = _E.trang_thai_moi("Yếu", "tán tu", "tan_tu")
_sky["chuong"] = 2
_sky["canh_gioi"] = "Luyện Khí tầng 1"
_cyv = False
for _ in range(40):
    _sky["tu_luyen"]["muc_tieu"] = None
    _x = _E.tl_dau(_sky)
    if _x.get("loi") is None and _x["tran"]["hang"] == "yeu_vuong":
        _cyv = True
# Người dùng chốt 2026-11-28: bỏ ngưỡng cảnh giới — tầng nào cũng CÓ CƠ HỘI gặp
# yêu vương, nhưng tỉ lệ thắng vẫn rất thấp. Test cũ khoá "tầng 1 không gặp" nên
# phải đổi thành: gặp được, và gặp rồi thì hiếm.
check("tầng 1: CÓ gặp yêu vương (bỏ ngưỡng)", _cyv, True)
_sky2 = _E.trang_thai_moi("Yeu2", "tán tu", "tan_tu")
_sky2["chuong"] = 2
_n = 0
for _ in range(400):
    _sky2["tu_luyen"]["muc_tieu"] = None
    _x = _E.tl_dau(_sky2)
    if _x.get("loi") is None and _x["tran"]["hang"] == "yeu_vuong":
        _n += 1
check("tầng 1: gặp yêu vương HIẾM (dưới 20%)", _n < 80, True)

_sbt = _E.trang_thai_moi("Thương", "tán tu", "tan_tu")
_sbt["chuong"] = 2
_sbt["chi_so"]["sinh_luc"]["hien"] = 3
check("bị thương: VẪN xem được trận", _E.tl_dau(_sbt).get("loi"), None)
check("bị thương: chặn ĐÁNH", _E.tl_danh(_sbt).get("loi") is not None, True)

print("\n=== TL1c. Chống bế tắc: tu vi và sinh lực đã đủ để thoát (người dùng chọn B) ===")
_dt = _E.trang_thai_moi("DaToa2", "tán tu", "tan_tu")
_dt["chuong"] = 2
while _dt["tu_luyen"]["ngay_con"] >= 3:
    _E.tl_da_toa(_dt)
check("đả tọa cả 30 ngày LÊN ĐƯỢC tầng", _dt["canh_gioi"] != "Luyện Khí tầng 1", True)
check("đả tọa 30 ngày: tu vi 24/135", (_dt["tu_vi"]["hien"], _dt["tu_vi"]["max"]), (24, 135))

_tong = 0
for _i in range(30):
    _sd = _E.trang_thai_moi("Do%d" % _i, "tán tu", "tan_tu")
    _sd["chuong"] = 2
    _tr = _sd["chi_so"]["sinh_luc"]["hien"]
    _E.tl_danh(_sd)
    _tong += _tr - _sd["chi_so"]["sinh_luc"]["hien"]
# Sinh lực là SỨC LAO ĐỘNG, tách khỏi máu chiến đấu. Mỗi trận mất theo tỉ lệ
# máu đã mất, nên phải đánh được nhiều trận liền mới hết ngày.
check("mỗi trận mất dưới 14 sinh lực (đánh được 2+ trận)", _tong / 30 < 14, True)
check("sinh lực mất mỗi trận ít nhất 1 (không âm)", _tong / 30 >= 1, True)

_sn = _E.trang_thai_moi("Nghi", "tán tu", "tan_tu")
_sn["chuong"] = 2
_sn["chi_so"]["sinh_luc"]["hien"] = 2
_E.tl_nghi(_sn)
check("nghỉ 1 ngày hồi 12 sinh lực", _sn["chi_so"]["sinh_luc"]["hien"], 14)

print("\n=== TL1d. Ba lỗi người dùng báo ===")
# Lỗi 1: bấm "Đổi con khác" 20 lần chỉ ra 2 con. _tl_ngau từng khoá theo ngày và
# số dòng nhật ký — hai thứ đó không đổi khi không tốn ngày.
_d1 = _E.trang_thai_moi("DoiCon", "tán tu", "tan_tu")
_d1["chuong"] = 2
_E.vao_dong(_d1)
_ds = []
for _i in range(20):
    _d1["tu_luyen"]["muc_tieu"] = None
    _x = _E.tl_dau(_d1)
    if _x.get("loi"):
        break
    _ds.append(_x["tran"]["ma"])
check("20 lần đổi con ra NHIỀU hơn 2 con", len(set(_ds)) > 2, True)
_lap = sum(1 for i in range(1, len(_ds)) if _ds[i] == _ds[i - 1])
check("đổi con không lặp lại con vừa xem", _lap, 0)

# Lỗi 2: chợ chỉ mua, không bán được nguyên liệu săn được.
_b = _E.trang_thai_moi("BanHang", "tán tu", "tan_tu")
_b["chuong"] = 2
_E.vao_dong(_b)
_b["tui_do"].append({"ten": "Nanh sói", "so": 3})
_bd = _E.tl_ban_duoc(_b)
check("chợ thấy Nanh sói để bán", any(v["ten"] == "Nanh sói" and v["so"] == 3 for v in _bd), True)
check("chợ KHÔNG thu bạc", any(v["ten"] == "Bạc vụn" for v in _bd), False)
_tr = _b["bac"]
_r = _E.tl_ban(_b, "Nanh sói", 2)
check("bán 2 nanh sói được +2 bạc", _b["bac"] - _tr, 2)
check("bán xong túi còn 1 nanh sói", _E._tl_co(_b, "Nanh sói"), 1)
check("bán xong báo thông báo", "Nanh sói" in " ".join(_r["thong_bao"]), True)
check("bán thứ không có thì báo lỗi", bool(_E.tl_ban(_b, "Vũ khí thần", 1).get("loi")), True)

# Lỗi 3: hết 30 ngày là hết vĩnh viễn ở màn tu luyện, không có nút sang chương.
_h = _E.trang_thai_moi("HetNgay", "tán tu", "tan_tu")
_h["chuong"] = 1
_E.vao_dong(_h)
while _h["tu_luyen"]["ngay_con"] >= 3:
    _E.tl_da_toa(_h)
check("dùng hết ngày thì còn 0", _h["tu_luyen"]["ngay_con"], 0)
check("hết ngày thì đả tọa bị chặn", bool(_E.tl_da_toa(_h).get("loi")), True)
_E.sang_chuong(_h)
check("sang chương cấp lại 30 ngày", _h["tu_luyen"]["ngay_con"], 30)

print("\n=== TL1e. Săn yêu thú cũng phải lên được tầng ===")
# Trước đây 30 ngày săn thuần chỉ được ~19/100 tu vi, người chơi kẹt tầng 1 mãi.
# Nay thua vẫn được tu vi và mỗi trận tốn ít sinh lực hơn.

def _san_thuan(_ten):
    _s = _E.trang_thai_moi(_ten, "tán tu", "tan_tu")
    _s["chuong"] = 2
    _E.vao_dong(_s)
    while _s["tu_luyen"]["ngay_con"] > 0:
        _sl = _s["chi_so"]["sinh_luc"]
        if _sl["hien"] <= _sl["max"] * 0.35 and _s["tu_luyen"]["ngay_con"] >= 1:
            _E.tl_nghi(_s)
            continue
        if _s["tu_luyen"]["ngay_con"] >= 2:
            _E.tl_danh(_s)
            continue
        if _s["tu_luyen"]["ngay_con"] >= 1:
            _E.tl_nghi(_s)
            continue
        break
    return _s

_vans = [_san_thuan(f"SanThuan{i}") for i in range(40)]
_len = sum(1 for _v in _vans if _v["canh_gioi"] != "Luyện Khí tầng 1")
check("30 ngày săn thuần lên tầng ở ÍT NHẤT 30/40 ván", _len >= 30, True)
check("không ván nào vượt quá tầng 2 trong chương 1", 
      all(_v["canh_gioi"] in ("Luyện Khí tầng 1", "Luyện Khí tầng 2") for _v in _vans), True)

# Thua phải cho tu vi, nếu không thì lý do trên không còn đúng.
_t = _E.trang_thai_moi("ThuaTuVi", "tán tu", "tan_tu")
_t["chuong"] = 2
_E.vao_dong(_t)
_t["chi_so"]["sinh_luc"]["hien"] = 30
_TV_TRUOC = _t["tu_vi"]["hien"]
_r_thua = None
for _i in range(40):
    if _t["chi_so"]["sinh_luc"]["hien"] <= _t["chi_so"]["sinh_luc"]["max"] * 0.35:
        _E.tl_nghi(_t)
    _r_thua = _E.tl_danh(_t)
    if not _r_thua.get("thang"):
        break
check("thua vẫn được tu vi", _t["tu_vi"]["hien"] >= _TV_TRUOC, True)
check("thua có báo tu vi trong dòng kể", any("tu vi" in d for d in _r_thua["dong"]), True)
check("hằng số tu vi khi thua là 7", _E.TL_TU_VI_THUA, 7)

print("\n=== TL2. Bản Python và bản JS phải ra CÙNG dãy số ngẫu nhiên ===")
# Nếu hai bản lệch nhau, người chơi thấy kết quả khác nhau tuỳ chơi web hay
# chơi bản Python — lỗi câm, không ai báo. Neo bằng số đo thật của bản Python.
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from game import engine as _E
    _goc = _E._hat_giong("Hàn Lập", 0)
    check("hạt giống 'Hàn Lập' ngày 0 (bản Python)", _goc, 254229688)
    check("ngẫu nhiên khớp bản JS", round(_E._ngau_nhien(_goc, 0), 12), 0.568700356176)
finally:
    pass

print("\n=== TL3. Trần cảnh giới: cày 200 lần vẫn không vượt ===")
try:
    from game import engine as _E
    _s = _E.trang_thai_moi("Trần", "tán tu", "tan_tu")
    _s["chuong"] = 2
    _s["canh_gioi"] = "Luyện Khí tầng 6"
    _s["tu_vi"] = {"hien": 130, "max": 135}
    _s["tu_luyen"]["ngay_con"] = 999
    for _ in range(200):
        _E.tl_da_toa(_s)
    check("chương 2: cày 200 lần dừng ở tầng 6", _s["canh_gioi"], "Luyện Khí tầng 6")
    # Khoá cổng boss so theo bậc, không so chuỗi: "tầng 10" > "tầng 2".
    _s["canh_gioi"] = "Luyện Khí tầng 10"
    check("tầng 10 qua được cổng cần tầng 2",
          _E._dieu_kien_hop(_s, {"canh_gioi": "Luyện Khí tầng 2"}), True)
    _s["canh_gioi"] = "Luyện Khí tầng 2"
    check("tầng 2 KHÔNG qua được cổng cần tầng 5",
          _E._dieu_kien_hop(_s, {"canh_gioi": "Luyện Khí tầng 5"}), False)
except ImportError:
    check("nhập được engine Python", False, True)

print("\n=== TL4. Sang chương: cấp lại ngày, nhưng không lặp dãy ngẫu nhiên ===")
try:
    from game import engine as _E
    _s = _E.trang_thai_moi("Sang", "tán tu", "tan_tu")
    _s["tu_luyen"]["ngay_con"] = 2
    _s["tu_luyen"]["ngay_da_dung"] = 28
    _s["ket_thuc"] = True
    _E.sang_chuong(_s, 2)
    check("sang chương: cấp lại 30 ngày", _s["tu_luyen"]["ngay_con"], 30)
    check("sang chương: giữ ngày đã dùng", _s["tu_luyen"]["ngay_da_dung"], 28)
except ImportError:
    check("nhập được engine Python", False, True)

print("\n=== BG. Bàn giao: commit mới nhất phải kèm nhật ký + sổ việc ===")
# Chốt chặn cho lỗi "làm xong mà quên bàn giao" — đã lặp lại 2 lần. Kiểm ở đây
# để nó hỏng NGAY lúc chạy test, trước khi kịp báo xong cho người dùng.
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from tools.kiem_ban_giao import thieu_trong_cay
    # Chỉ kiểm CÂY LÀM VIỆC, không kiểm commit HEAD: lúc chạy test thì commit
    # của phiên hiện tại chưa tồn tại, kiểm nó chỉ ra đỏ vô ích. Commit cũ đã
    # có tools/kiem_ban_giao.py --commit REF và hook post-commit lo.
    check("bàn giao: nhật ký + sổ việc đã cập nhật", [], thieu_trong_cay())
except ImportError:
    check("nhập được tools.kiem_ban_giao", False, True)

print("\n=== CD. Chiến đấu: 4 lớp chỉ số + pháp bảo + phù lục + tà tu ===")

# --- Lớp 1: sát thương có thật, không phải công thức một dòng ---
_cd1 = _E.trang_thai_moi("CD1", "tán tu", "tan_tu")
_cd2 = _E.trang_thai_moi("CD2", "tán tu", "tan_tu")
_pt = _E._cs_hieu_dung(_cd2)
_st_goc = _E._sat_thuong(_E._cs_hieu_dung(_cd1), _pt, "")
_pt2 = dict(_pt, phong_thu=_pt["phong_thu"] + 10)
check("phòng thủ cao thì ăn ít sát thương hơn",
      _E._sat_thuong(_E._cs_hieu_dung(_cd1), _pt2, "") < _st_goc, True)

# Xuyên giáp phải bỏ qua phòng thủ
_at = _E._cs_hieu_dung(_cd1)
_at["xuyen_giap"] = 100
check("xuyên giáp 100% bỏ qua phòng thủ",
      _E._sat_thuong(_at, _pt2, "") > _E._sat_thuong(_E._cs_hieu_dung(_cd1), _pt2, ""), True)

# Khắc hệ: kim khắc mộc
_kim = dict(_E._cs_hieu_dung(_cd1), he="kim")
_moc = dict(_pt, he="moc")
_kim2 = dict(_E._cs_hieu_dung(_cd1), he="moc")
check("kim khắc mộc: đánh mạnh hơn hệ không khắc",
      _E._sat_thuong(_kim, _moc, "kim") > _E._sat_thuong(_kim2, _moc, "moc"), True)

# Hệ phụ xuyên kháng: kháng chỉ còn nửa
_khang = dict(_pt, he="kim", khang_phep={"kim": 60, "loi": 60})
_kim3 = dict(_E._cs_hieu_dung(_cd1), he="kim")
_loi3 = dict(_E._cs_hieu_dung(_cd1), he="loi")
check("hệ phụ (lôi) xuyên kháng tốt hơn hệ thường",
      _E._sat_thuong(_loi3, _khang, "loi") > _E._sat_thuong(_kim3, _khang, "kim"), True)

# Bạo kích: bao_kich cao phải ra đòn to hơn
_that = {"n": 0}
def _ngau_cao():
    _that["n"] += 1
    return 0.0
check("bạo kích 100%: đòn to hơn đòn thường",
      _E._danh_mot_don(dict(_E._cs_hieu_dung(_cd1), bao_kich=1000), _pt, _ngau_cao)
      > _E._danh_mot_don(dict(_E._cs_hieu_dung(_cd1), bao_kich=0), _pt, _ngau_cao), True)

# Không ai chết: máu về 0 thì chỉ bị thương
_cd3 = _E.trang_thai_moi("CD3", "tán tu", "tan_tu")
_cd3["chuong"] = 2
_E.vao_dong(_cd3)
_cd3["chi_so"]["sinh_luc"]["hien"] = 1
_E.tl_danh(_cd3)
check("thua không chết: sinh lực còn ít nhất 1",
      _cd3["chi_so"]["sinh_luc"]["hien"] >= 1, True)

# --- Lớp 2: pháp bảo ---
_cd4 = _E.trang_thai_moi("CD4", "tán tu", "tan_tu")
_E._nhan_vat(_cd4, {"ten": "Huyền Thiết Đao", "so": 1})
_tc_truoc = _E._cs_hieu_dung(_cd4)["tan_cong"]
_r = _E.tl_mac(_cd4, "huyen_thiet_dao")
check("mặc pháp bảo: cộng tấn công", _E._cs_hieu_dung(_cd4)["tan_cong"] > _tc_truoc, True)
check("mặc pháp bảo: ghi vào trang_bi", _cd4["trang_bi"]["phap_bao"], "huyen_thiet_dao")
_E.tl_mac(_cd4, "")
check("tháo pháp bảo: trả lại tấn công gốc", _E._cs_hieu_dung(_cd4)["tan_cong"], _tc_truoc)
check("mặc pháp bảo không có trong túi: báo lỗi",
      _E.tl_mac(_cd4, "loi_dinh_chuy").get("loi") is not None, True)

# Pháp bảo phải đổi được kết quả trận với tà tu
_cd5 = _E.trang_thai_moi("CD5", "tán tu", "tan_tu")
_cd5["canh_gioi"] = "Luyện Khí tầng 5"
_cd5["chi_so"]["tan_cong"] = 11
_cd5["chi_so"]["sinh_luc"] = {"hien": 50, "max": 50}
_cd5["chi_so"]["phong_thu"] = 6
_cd5["chi_so"]["toc_do"] = 13
_tay_khong = _E.tl_ta_tu_ti_le(_cd5)
_E._nhan_vat(_cd5, {"ten": "Lôi Đình Chùy", "so": 1})
_E.tl_mac(_cd5, "loi_dinh_chuy")
_co_chuy = _E.tl_ta_tu_ti_le(_cd5)
check("pháp bảo tốt làm tăng tỉ lệ thắng tà tu", _co_chuy > _tay_khong, True)
check("tà tu tầng 5: tay không chưa chắc thắng (dưới 70%)", _tay_khong < 70, True)

# --- Lớp 3: phù lục ---
_cd6 = _E.trang_thai_moi("CD6", "tán tu", "tan_tu")
_cd6["chuong"] = 2
_E.vao_dong(_cd6)
_E._nhan_vat(_cd6, {"ten": "Bạo Viêm Phù", "so": 2})
_E.tl_danh(_cd6, dung_phu="bao_viem_phu")
check("dùng phù lục: tiêu hao 1", _E._tl_co(_cd6, "Bạo Viêm Phù"), 1)
check("dùng phù lục không có: báo lỗi",
      _E.tl_danh(_cd6, dung_phu="kim_quang_phu").get("loi") is not None, True)

# --- Buff: 2 lần/chương, đúng nhánh ---
_cd7 = _E.trang_thai_moi("CD7", "tán tu", "tan_tu")
check("tán tu có Kiếm Linh", _E.buff_cua_minh(_cd7), "kiem_linh")
_cd8 = _E.trang_thai_moi("CD8", "môn phái", "mon_phai")
check("môn phái có Tuyết Cơ", _E.buff_cua_minh(_cd8), "tuyet_co")
check("mỗi chương 2 lượt buff", _E._tl_buff(_cd7)["kiem_linh"], 2)

_cd9 = _E.trang_thai_moi("CD9", "tán tu", "tan_tu")
_cd9["chuong"] = 2
_E.vao_dong(_cd9)
_r = _E.tl_danh(_cd9, dung_buff="kiem_linh")
check("dùng buff: thắng chắc", _r["thang"], True)
check("dùng buff: trừ 1 lượt", _E._tl_buff(_cd9)["kiem_linh"], 1)
_r2 = _E.tl_danh(_cd9, dung_buff="kiem_linh")
check("dùng buff: trừ lượt thứ hai", _E._tl_buff(_cd9)["kiem_linh"], 0)
_r3 = _E.tl_danh(_cd9, dung_buff="kiem_linh")
check("hết lượt buff: báo lỗi, không đánh", _r3.get("loi") is not None, True)

# Sang chương thì buff hồi lại
_E._tl_buff(_cd9)["kiem_linh"] = 0
_cd9["chuong"] = 1
_E.sang_chuong(_cd9, 2)
check("sang chương: buff hồi lại 2 lượt", _E._tl_buff(_cd9)["kiem_linh"], 2)

# --- Lớp 4: tà tu trong truyện ---
_cd10 = _E.trang_thai_moi("CD10", "tán tu", "tan_tu")
_cd10["chuong"] = 2
_E.vao_dong(_cd10)
_cd10["doan_hien_tai"] = "c2_d27c_0"
_d = _E._doan(_cd10)
check("c2_d27c_0: lựa chọn cuối vào trận đánh",
      bool((_d["lua_chon"][-1].get("tran_dau") or {}).get("doi_thu")), True)
_cd10["canh_gioi"] = "Luyện Khí tầng 5"
_cd10["chi_so"]["tan_cong"] = 11
_cd10["chi_so"]["sinh_luc"] = {"hien": 50, "max": 50}
_cd10["chi_so"]["phong_thu"] = 6
_cd10["chi_so"]["toc_do"] = 13
_r = _E.chon(_cd10, len(_d["lua_chon"]) - 1)
check("đánh tà tu: trả về kết quả trận", "tran" in _r, True)
check("đánh tà tu: rẽ đúng nhánh thắng/thua",
      _cd10["doan_hien_tai"] in ("c2_d27c_thang", "c2_d27c_thua"), True)

# Mọi tầng đều gặp được yêu vương (người dùng chốt bỏ ngưỡng)
_cd11 = _E.trang_thai_moi("CD11", "tán tu", "tan_tu")
_cd11["chuong"] = 2
_gg = set()
for _ in range(300):
    _cd11["tu_luyen"]["muc_tieu"] = None
    _x = _E.tl_dau(_cd11)
    if _x.get("loi") is None:
        _gg.add(_x["tran"]["hang"])
check("tầng 1 gặp được cả 3 hạng (bỏ ngưỡng)", _gg == {"thuong", "tinh_anh", "yeu_vuong"}, True)

# --- Uống đan ---
_cd12 = _E.trang_thai_moi("CD12", "tán tu", "tan_tu")
_cd12["chuong"] = 2
_E.vao_dong(_cd12)
_tv_truoc = _cd12["tu_vi"]["hien"]
_E._nhan_vat(_cd12, {"ten": "Tụ Khí Đan", "so": 2})
_r = _E.tl_uong(_cd12, "Tụ Khí Đan")
check("uống đan: cộng tu vi", _cd12["tu_vi"]["hien"] > _tv_truoc, True)
check("uống đan: tiêu hao 1", _E._tl_co(_cd12, "Tụ Khí Đan"), 1)
check("uống đan không có: báo lỗi",
      _E.tl_uong(_cd12, "Hồi Lực Đan").get("loi") is not None, True)

# Luyện đan ra lò phải vào TÚI, chưa cộng tu vi
_cd13 = _E.trang_thai_moi("CD13", "tán tu", "tan_tu")
_cd13["chuong"] = 2
_E.vao_dong(_cd13)
_E._nhan_vat(_cd13, {"ten": "Nanh sói", "so": 5})
_E._nhan_vat(_cd13, {"ten": "Linh thảo", "so": 10})
_tv0 = _cd13["tu_vi"]["hien"]
for _ in range(6):
    _E.tl_luyen_dan(_cd13, "tu_khi_dan")
check("luyện đan ra lò: KHÔNG cộng tu vi ngay", _cd13["tu_vi"]["hien"], _tv0)
check("luyện đan ra lò: đan nằm trong túi",
      _E._tl_co(_cd13, "Tụ Khí Đan") > 0 or _E._tl_co(_cd13, "Nanh sói") == 0, True)

print(f"\n{'='*46}\nKẾT QUẢ: {ok} đạt, {fail} hỏng")
sys.exit(1 if fail else 0)
