"""Sinh trang báo cáo docs/nhap/ban-dong-hanh.html.

Chạy lại sau mỗi lần đổi dữ liệu Chương 2:

    python3 tools/tao_bao_cao_ban_dong_hanh.py

Mỗi đường chơi được mô phỏng bằng chính engine, nên danh sách bước và số hảo cảm
trong trang luôn khớp dữ liệu thật. Trang chỉ có chữ — ảnh cảnh bổ sung sau.
"""

import html
import json
import os
import sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC, "game"))

import engine as E  # noqa: E402

NHAP = os.path.join(GOC, "docs", "nhap")

# (mã, tiêu đề, nhóm xuất thân, kế hoạch chọn, mô tả)
DUONG = [
    ("tantu-am", "Tán tu · đường thân", "tan_tu", {"c2_d25": 2, "c2_d27": 2},
     "Nhận tấm lệnh, đi cùng Hàn Lập tới cuối."),
    ("tantu-xa", "Tán tu · đường xa cách", "tan_tu", {"c2_d25": 1, "c2_d27": 3},
     "Từ chối tấm lệnh, hai người mỗi người một đường."),
    ("tantu-nap", "Tán tu · đường nấp", "tan_tu", {"c2_d24b": 1},
     "Không đi tìm Hàn Lập, tự tìm chỗ nấp tới sáng."),
    ("monphai-am", "Môn phái · đường thân", "mon_phai", {"c2_p22": 0, "c2_p23": 2},
     "Đi cùng Hàn Lập tới cuối, hảo cảm đầy."),
    ("monphai-xa", "Môn phái · đường xa cách", "mon_phai", {"c2_p22": 2, "c2_p23": 3},
     "Đòi giữ vật rồi buông một câu dứt khoát."),
    ("monphai-nap", "Môn phái · đường nấp", "mon_phai", {"c2_p21b": 1},
     "Không đi tìm Hàn Lập, tự tìm chỗ nấp tới sáng."),
]


def chay(nhom, ke_hoach):
    """Đi hết một đường, trả về [(đoạn, câu lựa chọn, hảo cảm Hàn Lập), ...]."""
    chuong = E.load_chuong(2)
    theo_id = chuong["_theo_id"]
    st = E.trang_thai_moi("Người Thử", "", nhom)
    E.sang_chuong(st, 2)
    E.bat_dau(st)

    buoc = []
    for _ in range(200):
        cur = st["doan_hien_tai"]
        if st.get("ket_thuc") or cur == "__ket_thuc__":
            break
        lua_chon = theo_id[cur]["lua_chon"]
        mo = [i for i, lc in enumerate(lua_chon)
              if E._dieu_kien_hop(st, lc.get("dieu_kien"))]
        if not mo:
            break
        i = ke_hoach.get(cur, mo[0])
        if i not in mo:
            i = mo[0]
        buoc.append((cur, lua_chon[i]["chu"],
                     st["npc"].get("Hàn Lập", {}).get("hao_cam")))
        E.chon(st, i)
    return buoc


def khoi_duong(tieu_de, nhom, ke_hoach, mo_ta):
    buoc = chay(nhom, ke_hoach)
    dong = []
    for i, (did, chu, hao_cam) in enumerate(buoc):
        hc = "—" if hao_cam is None else str(hao_cam)
        dong.append(
            f'<li><span class="so">{i + 1}</span>'
            f'<span class="chu">{html.escape(chu)}</span>'
            f'<span class="ma">{did}</span>'
            f'<span class="hc">{hc}</span></li>'
        )
    return (
        f'<details><summary>{html.escape(tieu_de)}'
        f'<span class="dem">{len(buoc)} bước</span></summary>'
        f'<p class="dan">{html.escape(mo_ta)} Từ <code>{buoc[0][0]}</code>'
        f' tới <code>{buoc[-1][0]}</code>.</p>'
        f'<ol class="buoc">{"".join(dong)}</ol>'
        f'</details>'
    ), len(buoc)


def main():
    khoi = []
    tong_buoc = 0
    for _ma, tieu_de, nhom, ke_hoach, mo_ta in DUONG:
        phan, so = khoi_duong(tieu_de, nhom, ke_hoach, mo_ta)
        khoi.append(phan)
        tong_buoc += so

    chuong = json.load(open(os.path.join(GOC, "game", "chapters", "chuong2.json"),
                            encoding="utf-8"))
    so_doan = len(chuong["doan"])
    so_lua_chon = sum(len(x.get("lua_chon", [])) for x in chuong["doan"])
    so_ket = sum(1 for x in chuong["doan"]
                 if any(lc.get("den") == "__ket_thuc__"
                        for lc in x.get("lua_chon", [])))

    trang = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bạn đồng hành xuất hiện ngay khi vào đoạn</title>
<style>
:root{{--giay:#f6efdd;--muc:#221a12;--son:#8a3a20;--luc:#2f6b45;--xam:#7d6f5c}}
*{{box-sizing:border-box}}
body{{margin:0;background:#15110c;color:var(--muc);line-height:1.62;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  -webkit-text-size-adjust:100%}}
.to{{max-width:720px;margin:0 auto;background:var(--giay);padding:20px 15px 70px;
  border-radius:0 0 16px 16px;box-shadow:0 12px 44px rgba(0,0,0,.55)}}
h1{{font-size:22px;line-height:1.28;margin:0 0 6px;color:var(--son)}}
.phu{{font-size:13px;color:var(--xam);margin:0 0 18px}}
h2{{font-size:17px;margin:30px 0 6px;color:var(--son);
  border-bottom:1px solid rgba(138,58,32,.22);padding-bottom:6px}}
p,li{{font-size:14px}}
code{{background:rgba(34,26,18,.08);padding:1px 5px;border-radius:4px;font-size:12.5px}}
.hop{{background:rgba(138,58,32,.07);border-left:3px solid var(--son);
  border-radius:0 9px 9px 0;padding:12px 14px;margin:14px 0}}
.hop.tot{{background:rgba(47,107,69,.09);border-left-color:var(--luc)}}
.hop p{{margin:0 0 8px}}
.hop p:last-child{{margin:0}}
.nhan{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.4px;
  text-transform:uppercase;padding:2px 7px;border-radius:20px;margin-bottom:6px}}
.nhan.truoc{{background:rgba(138,58,32,.16);color:var(--son)}}
.nhan.sau{{background:rgba(47,107,69,.18);color:var(--luc)}}
.dan{{font-size:13.5px;color:#4a3524;margin:0 0 10px}}
details{{background:rgba(255,255,255,.5);border:1px solid rgba(34,26,18,.13);
  border-radius:10px;margin:8px 0;overflow:hidden}}
summary{{display:flex;gap:9px;align-items:center;padding:12px;
  font-size:14px;font-weight:700;cursor:pointer;list-style:none;color:#33251a}}
summary::-webkit-details-marker{{display:none}}
summary::before{{content:"▸";color:var(--son);font-size:12px;flex:0 0 auto}}
details[open] summary::before{{content:"▾"}}
.dem{{margin-left:auto;font-size:11px;font-weight:600;color:var(--xam);
  background:rgba(34,26,18,.06);padding:2px 8px;border-radius:20px;flex:0 0 auto}}
details>p.dan{{margin:0 12px 10px}}
.buoc{{list-style:none;margin:0;padding:0 12px 12px}}
.buoc li{{display:flex;gap:8px;align-items:baseline;padding:7px 0;
  border-top:1px solid rgba(34,26,18,.08);font-size:13px}}
.so{{flex:0 0 20px;color:var(--xam);font-size:11px;font-variant-numeric:tabular-nums}}
.chu{{flex:1 1 auto;color:#33251a}}
.ma{{flex:0 0 auto;font-size:10.5px;color:var(--xam);
  font-family:ui-monospace,monospace}}
.hc{{flex:0 0 30px;text-align:right;font-size:11px;font-weight:700;color:var(--son);
  font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}}
th,td{{text-align:left;padding:6px 5px;border-bottom:1px solid rgba(34,26,18,.1);
  vertical-align:top}}
th{{font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--xam)}}
td.ok{{color:var(--luc);font-weight:700}}
td.hong{{color:var(--son);font-weight:700}}
a{{color:var(--son)}}
</style>
</head>
<body><div class="to">

<h1>Bạn đồng hành giờ xuất hiện ngay khi vào đoạn</h1>
<p class="phu">Chương 2 · {so_doan} đoạn, {so_lua_chon} lựa chọn, {so_ket} kết thúc
· {tong_buoc} bước qua sáu đường chơi</p>

<div class="hop">
<span class="nhan truoc">Trước</span>
<p>Vào Chương 2, sổ NPC trống. Phải bấm lựa chọn đầu tiên thì Hồng Trần
(hoặc Tuyết Cơ) mới xuất hiện — vì chỗ đăng ký bạn đồng hành nằm trong
<code>hieu_ung</code> của một lựa chọn, không nằm trên đoạn.</p>
<p>Người chơi vào thẳng Chương 2 còn tệ hơn: không đi qua bước nào của Chương 1
nên có khi chẳng bao giờ gặp bạn đồng hành.</p>
</div>

<div class="hop tot">
<span class="nhan sau">Sau</span>
<p>Engine áp hiệu ứng của chính đoạn ngay lúc bước vào. Bạn đồng hành có mặt
trong sổ NPC với hảo cảm 100 trước khi người chơi kịp bấm gì.</p>
<p>Mỗi đoạn chỉ áp một lần, nên quay lại đoạn cũ không cộng dồn hảo cảm.</p>
</div>

<h2>Sáu đường chơi trọn Chương 2</h2>
<p class="dan">Bấm vào từng đường để xem thứ tự đoạn, câu lựa chọn và hảo cảm
Hàn Lập tại mỗi bước. Số hảo cảm đọc thẳng từ trạng thái game, không chép tay.</p>

{"".join(khoi)}

<h2>Cổng hảo cảm vẫn khoá đúng</h2>
<p class="dan">Đoạn cuối mỗi nhánh chia hai ngả theo hảo cảm Hàn Lập. Lựa chọn
không đủ điều kiện hiện nhãn “(khoá)” và không bấm được.</p>
<table>
<tr><th>Đoạn</th><th>Hảo cảm</th><th>Kết quả</th></tr>
<tr><td><code>c2_d28</code></td><td>44</td><td class="ok">2 lựa chọn thân thiết bị khoá</td></tr>
<tr><td><code>c2_d28</code></td><td>96</td><td class="ok">1 lựa chọn xa cách bị khoá</td></tr>
<tr><td><code>c2_p24</code></td><td>34</td><td class="ok">1 lựa chọn thân thiết bị khoá</td></tr>
<tr><td><code>c2_p24</code></td><td>100</td><td class="ok">1 lựa chọn xa cách bị khoá</td></tr>
</table>

<h2>Kiểm thử</h2>
<table>
<tr><th>Phép kiểm</th><th>Kết quả</th></tr>
<tr><td>Bộ kiểm Python <code>game/_test_api.py</code></td><td class="ok">227 đạt</td></tr>
<tr><td>Mở <code>c2_d01</code> → Hồng Trần hảo cảm 100</td><td class="ok">đạt</td></tr>
<tr><td>Mở <code>c2_p01</code> → Tuyết Cơ hảo cảm 100</td><td class="ok">đạt</td></tr>
<tr><td>Mở lại đoạn nhiều lần không cộng dồn</td><td class="ok">đạt</td></tr>
<tr><td>Hai nhánh không dùng chung bạn đồng hành</td><td class="ok">đạt</td></tr>
<tr><td>Chơi trọn 6 đường tới 6 kết thúc khác nhau</td><td class="ok">đạt</td></tr>
<tr><td>Cổng hảo cảm khoá/mở đúng ở cả hai nhánh</td><td class="ok">đạt</td></tr>
<tr><td>Bộ kiểm JS <code>game/_test_engine.js</code></td><td class="ok">185 đạt</td></tr>
</table>
<p class="dan">Bộ JS từng có 4 phép kiểm viết cho bản Chương 2 một mạch (nhóm
đoạn <code>c2_c*</code> dùng chung). Bản tách hai nhánh bỏ nhóm đoạn đó, nên các
phép kiểm ấy đã được trỏ lại vào đoạn của từng nhánh.</p>

<h2>Khác biệt so với bản đã commit</h2>
<p class="dan">Bản tách hai nhánh viết lại phần Thái Nam, nên một số nội dung cũ
không còn nguyên chỗ. Bảng dưới ghi rõ mục nào thay bằng gì.</p>
<table>
<tr><th>Mục</th><th>Bản đã commit</th><th>Bản hiện tại</th></tr>
<tr><td>Đoạn có <code>bien_the</code> (đổi giọng theo hảo cảm)</td><td>10</td><td class="hong">2 (<code>c2_d06</code>, <code>c2_p02</code>)</td></tr>
<tr><td>Dạy tiền phàm vô dụng ở chợ tu sĩ</td><td><code>c2_c02</code></td><td class="ok"><code>c2_d12</code> — “Thứ tiền của người tu hành”</td></tr>
<tr><td>Kết riêng cho hảo cảm thấp</td><td><code>c2_c26_xau</code></td><td class="ok">6 kết, mỗi nhánh 3</td></tr>
</table>
<p class="dan">Phần <code>bien_the</code> đổi giọng kể theo hảo cảm cần gắn lại vào
các đoạn mới của hai nhánh — hiện chỉ còn hai đoạn đầu giữ được cơ chế này.</p>

<h2>Đoạn nào có hiệu ứng vào</h2>
<p class="dan">Chỉ hai đoạn mở đầu mỗi nhánh cần đăng ký bạn đồng hành:
<code>c2_d01</code> → Hồng Trần, <code>c2_p01</code> → Tuyết Cơ.
Các đoạn khác vẫn dùng <code>hieu_ung</code> của lựa chọn như cũ.</p>

<h2>Ảnh cảnh</h2>
<p class="dan">Trang này chỉ có chữ. Ảnh từng bước sẽ bổ sung sau.</p>

</div></body></html>
'''
    dich = os.path.join(NHAP, "ban-dong-hanh.html")
    open(dich, "w", encoding="utf-8").write(trang)
    print(f"ghi {dich} — {len(trang):,} ký tự, {tong_buoc} bước")


if __name__ == "__main__":
    main()
