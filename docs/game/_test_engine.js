/* Kiểm thử engine.js (bản JS) — đối chiếu với luồng thật của engine.py.
 *
 * Chạy: node docs/game/_test_engine.js
 * Không cần server, không cần mạng — chỉ kiểm logic engine.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const Engine = require("./engine.js");

// localStorage giả cho Node
const _kho = {};
globalThis.localStorage = {
  getItem: (k) => (k in _kho ? _kho[k] : null),
  setItem: (k, v) => { _kho[k] = String(v); },
  removeItem: (k) => { delete _kho[k]; },
  key: (i) => Object.keys(_kho)[i] || null,
  get length() { return Object.keys(_kho).length; },
};

const GOC = path.join(__dirname, "du-lieu");
Engine.napXuatThan(JSON.parse(fs.readFileSync(path.join(GOC, "xuat_than.json"), "utf8")));
Engine.napChuong(1, JSON.parse(fs.readFileSync(path.join(GOC, "chuong1.json"), "utf8")));

let ok = 0, fail = 0;
function check(ten, dieu, thuc) {
  if (JSON.stringify(dieu) === JSON.stringify(thuc)) { ok++; console.log(`  ✓ ${ten}`); }
  else { fail++; console.log(`  ✗ ${ten}\n      mong đợi: ${JSON.stringify(dieu)}\n      nhận được: ${JSON.stringify(thuc)}`); }
}
const mk = (ten, nhom) => Engine.trang_thai_moi(ten, "", nhom);
function toi(st, dich, toi_da) {
  toi_da = toi_da || 40;
  let r = {};
  for (let i = 0; i < toi_da; i++) {
    r = Engine.chon(st, 0);
    if (r.doan_id === dich || r.ket_thuc) break;
  }
  return r;
}

console.log("=== A. Xuất thân ===");
check("đủ 2 nhóm chơi được", Engine.ds_xuat_than().map((n) => n.ma), ["tan_tu", "mon_phai"]);
check("nhóm ẩn bị giấu", Engine.ds_xuat_than(true).length > Engine.ds_xuat_than().length, true);
check("nhận diện 'ăn mày' → tan_tu", Engine.nhan_dien_xuat_than("ăn mày lang thang"), "tan_tu");
check("nhận diện 'tạp dịch' → mon_phai", Engine.nhan_dien_xuat_than("tạp dịch đệ tử"), "mon_phai");
check("nhận diện lạ → tan_tu", Engine.nhan_dien_xuat_than("xyz abc"), "tan_tu");
check("nhóm ẩn không tự nhận", Engine.nhan_dien_xuat_than("ngọc cốt tuyết cơ"), "tan_tu");
check("doan_dau tan_tu", Engine.doan_dau_cua("tan_tu"), "c1_d01");
check("doan_dau mon_phai", Engine.doan_dau_cua("mon_phai"), "c1_p01");

console.log("\n=== B. Trạng thái mới ===");
let st = mk("A", "tan_tu");
check("bạc khởi đầu 3", st.bac, 3);
check("sinh lực 30/30", [st.chi_so.sinh_luc.hien, st.chi_so.sinh_luc.max], [30, 30]);
check("tu vi 12/100", [st.tu_vi.hien, st.tu_vi.max], [12, 100]);
check("cảnh giới Luyện Khí tầng 1", st.canh_gioi, "Luyện Khí tầng 1");
check("nhóm lạ rơi về tan_tu", mk("B", "xyz").nhom_xuat_than, "tan_tu");

console.log("\n=== C. Nhánh TÁN TU — đường 1 (miếu hoang) ===");
let o = mk("TT", "tan_tu");
let r = Engine.bat_dau(o);
check("mở đầu d01", r.doan_id, "c1_d01");
check("d01 → d02", Engine.chon(o, 0).doan_id, "c1_d02");
check("d02 → d03", Engine.chon(o, 0).doan_id, "c1_d03");
check("d03 → d04b (vào trong)", Engine.chon(o, 0).doan_id, "c1_d04b");
check("d04b → d04c", Engine.chon(o, 0).doan_id, "c1_d04c");
check("d04c → d04d", Engine.chon(o, 0).doan_id, "c1_d04d");
const sl_truoc = o.chi_so.sinh_luc.hien;
r = Engine.chon(o, 0);
check("d04d → d05 (chạm hộp)", r.doan_id, "c1_d05");
check("cờ thay_do_tam_chet", o.co_su_kien.includes("thay_do_tam_chet"), true);
check("sinh lực trừ 12", sl_truoc - o.chi_so.sinh_luc.hien, 12);

console.log("\n=== D. Nhánh TÁN TU — đường 2 (quan sát) ===");
o = mk("TT2", "tan_tu");
Engine.bat_dau(o);
Engine.chon(o, 0);  // d02
check("d02 → d02b (ở lại trấn)", Engine.chon(o, 1).doan_id, "c1_d02b");
check("d02b → d03", Engine.chon(o, 0).doan_id, "c1_d03");
check("d03 → d04 (quan sát)", Engine.chon(o, 1).doan_id, "c1_d04");
check("d04 → d04b", Engine.chon(o, 0).doan_id, "c1_d04b");

console.log("\n=== E. Nhánh TÁN TU — cảnh giác & do dự ===");
o = mk("TT3", "tan_tu");
Engine.bat_dau(o);
r = toi(o, "c1_d06");
check("tới d06 (kiếm linh)", r.doan_id, "c1_d06");
check("d06 → d06b (cảnh giác)", Engine.chon(o, 1).doan_id, "c1_d06b");
check("d06b → d07", Engine.chon(o, 0).doan_id, "c1_d07");
check("d07 → d07b (do dự)", Engine.chon(o, 1).doan_id, "c1_d07b");
check("d07b → d08", Engine.chon(o, 0).doan_id, "c1_d08");
check("d08 → d09", Engine.chon(o, 0).doan_id, "c1_d09");
check("nhận Hồng Trần Kiếm Hạp", o.tui_do.some((v) => v.ten === "Hồng Trần Kiếm Hạp"), true);
check("cờ co_kiem_hong_tran", o.co_su_kien.includes("co_kiem_hong_tran"), true);

console.log("\n=== F. Nhánh TÁN TU — chiến trận & tu luyện ===");
o = mk("TT4", "tan_tu");
Engine.bat_dau(o);
r = toi(o, "c1_d11");
check("tới d11 (Dã Lang Bang)", r.doan_id, "c1_d11");
check("d11 → d13 (môn phái)", Engine.chon(o, 1).doan_id, "c1_d13");
check("d13 → d14", Engine.chon(o, 0).doan_id, "c1_d14");

o = mk("TT5", "tan_tu");
Engine.bat_dau(o);
toi(o, "c1_d11");
check("d11 → d12 (cứu dân)", Engine.chon(o, 0).doan_id, "c1_d12");
check("d12 → d14", Engine.chon(o, 0).doan_id, "c1_d14");

o = mk("TT6", "tan_tu");
Engine.bat_dau(o);
toi(o, "c1_d09");
check("d09 → d10 (đột phá)", Engine.chon(o, 0).doan_id, "c1_d10");
check("học Hồng Trần kiếm khí", o.ky_nang.includes("Hồng Trần kiếm khí"), true);

console.log("\n=== G. Nhánh TÁN TU — 4 cách gặp Hàn Lập ===");
for (const [cs, ten, coco, hc] of [[0, "thành thật", "noi_that_han_lap", 10],
  [1, "cười trừ", null, 0], [2, "hỏi ngược", null, 5], [3, "bầu nước", null, 8]]) {
  const ot = mk("HL", "tan_tu");
  Engine.bat_dau(ot);
  const rr = toi(ot, "c1_d15");
  check(`tới d15 (${ten})`, rr.doan_id, "c1_d15");
  check(`d15 ${ten} → d16`, Engine.chon(ot, cs).doan_id, "c1_d16");
  check(`  ${ten}: hảo cảm = ${hc}`, (ot.npc["Hàn Lập"] || {}).hao_cam || 0, hc);
  if (coco) check(`  ${ten}: cờ ${coco}`, ot.co_su_kien.includes(coco), true);
  check(`  ${ten} → d17`, Engine.chon(ot, 0).doan_id, "c1_d17");
  check(`  ${ten} → kết chương`, Engine.chon(ot, 0).ket_thuc, true);
}

console.log("\n=== H. Nhánh MÔN PHÁI — cơ bản ===");
o = mk("MP", "mon_phai");
r = Engine.bat_dau(o);
check("mở đầu p01", r.doan_id, "c1_p01");
check("p01 → p02", Engine.chon(o, 0).doan_id, "c1_p02");
check("p02 → p03 (chèn ép)", Engine.chon(o, 0).doan_id, "c1_p03");
check("p03 → p03b (nuốt nhục)", Engine.chon(o, 0).doan_id, "c1_p03b");
Engine.chon(o, 0);
check("học Thất Huyền quyền", o.ky_nang.includes("Thất Huyền quyền"), true);
check("cờ hoc_that_huyen_quyen", o.co_su_kien.includes("hoc_that_huyen_quyen"), true);

console.log("\n=== I. Nhánh MÔN PHÁI — đường ③ hậu sơn ===");
o = mk("MP2", "mon_phai");
Engine.bat_dau(o);
Engine.chon(o, 0);  // p02
check("p02 → p05 (dò tin)", Engine.chon(o, 2).doan_id, "c1_p05");
check("p05 → p05b (khe núi)", Engine.chon(o, 0).doan_id, "c1_p05b");
check("biết Hùng Bá", o.co_su_kien.includes("biet_dau_linh"), true);
check("p05b → p07 (lấy ngọc)", Engine.chon(o, 0).doan_id, "c1_p07");

console.log("\n=== J. Nhánh MÔN PHÁI — đường ② p04 ===");
o = mk("MP3", "mon_phai");
Engine.bat_dau(o);
Engine.chon(o, 0);  // p02
r = Engine.chon(o, 1);  // p04
check("p04 2 lựa chọn khác nhau", new Set(r.lua_chon.map((l) => l.chu)).size, 2);
check("p04 → p04b (im lặng)", Engine.chon(o, 1).doan_id, "c1_p04b");

console.log("\n=== K. Nhánh MÔN PHÁI — 4 cách gặp Hàn Lập ===");
for (const [cs, dich, ten] of [[0, "c1_p18a", "thành thật"], [1, "c1_p18b", "cười trừ"],
  [2, "c1_p18c", "hỏi ngược"], [3, "c1_p18d", "bầu nước"]]) {
  const ox = mk("MPHL", "mon_phai");
  Engine.bat_dau(ox);
  Engine.chon(ox, 0);
  Engine.chon(ox, 1);
  Engine.chon(ox, 0);
  toi(ox, "c1_p17", 30);
  check(`p17 ${ten} → ${dich}`, Engine.chon(ox, cs).doan_id, dich);
  check(`  ${ten} → kết p19`, Engine.chon(ox, 0).doan_id, "c1_p19");
}

console.log("\n=== L. Lưu / nạp ===");
o = mk("Save", "tan_tu");
Engine.bat_dau(o);
Engine.chon(o, 0);
Engine.luu(o, "test_slot");
const nap = Engine.nap("test_slot");
check("nạp đúng đoạn", nap.doan_hien_tai, o.doan_hien_tai);
check("nạp đúng tên", nap.ten_nhan_vat, "Save");
check("ds_luu có slot", Engine.ds_luu().includes("test_slot"), true);
Engine.xoa_luu("test_slot");
check("xoá rồi không còn", Engine.nap("test_slot"), null);

console.log("\n=== M. Tự do (không AI) ===");
o = mk("Free", "tan_tu");
Engine.bat_dau(o);
const doan_truoc = o.doan_hien_tai;
(async () => {
  r = await Engine.hanh_dong_tu_do(o, "nhìn quanh tìm lối thoát", null);
  check("tự do trả đoạn", "doan_id" in r, true);
  check("tự do không đổi đoạn", o.doan_hien_tai, doan_truoc);
  check("tự do có thông báo", Array.isArray(r.thong_bao) && r.thong_bao.length > 0, true);
  r = await Engine.hanh_dong_tu_do(o, "   ", null);
  check("nhập rỗng → lỗi", r.loi !== undefined, true);
  check("chọn sai → lỗi", Engine.chon(o, 99).loi !== undefined, true);
  check("chọn âm → lỗi", Engine.chon(o, -1).loi !== undefined, true);

  console.log(`\n${"=".repeat(46)}\nKẾT QUẢ: ${ok} đạt, ${fail} hỏng`);
  process.exit(fail ? 1 : 0);
})();
