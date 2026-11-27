/* Kiểm thử engine.js (bản JS) — đối chiếu với luồng thật của engine.py.
 *
 * Chạy: node docs/game/_test_engine.js
 * Không cần server, không cần mạng — chỉ kiểm logic engine.
 */
"use strict";

const fs = require("fs");
const path = require("path");
// engine.js + du-lieu/ nam trong thu muc deploy (docs/game/) — tro nguoc ve do
const GAME_DIR = path.join(__dirname, "..", "docs", "game");
const Engine = require(path.join(GAME_DIR, "engine.js"));

// localStorage giả cho Node
const _kho = {};
globalThis.localStorage = {
  getItem: (k) => (k in _kho ? _kho[k] : null),
  setItem: (k, v) => { _kho[k] = String(v); },
  removeItem: (k) => { delete _kho[k]; },
  key: (i) => Object.keys(_kho)[i] || null,
  get length() { return Object.keys(_kho).length; },
};

const GOC = path.join(GAME_DIR, "du-lieu");
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
check("tán tu: bạc khởi đầu 3", st.bac, 3);
check("tán tu: sinh lực 26/26", [st.chi_so.sinh_luc.hien, st.chi_so.sinh_luc.max], [26, 26]);
check("tán tu: tu vi 12/100", [st.tu_vi.hien, st.tu_vi.max], [12, 100]);
check("tán tu: tấn công 3", st.chi_so.tan_cong, 3);
check("tán tu: bạc vụn trong túi khớp bạc", st.tui_do[0].so, 3);

// --- chỉ số khởi đầu phải KHÁC nhau giữa hai xuất thân ---
const mp = mk("MP", "mon_phai");
check("môn phái: bạc khởi đầu 1", mp.bac, 1);
check("môn phái: sinh lực 34/34", [mp.chi_so.sinh_luc.hien, mp.chi_so.sinh_luc.max], [34, 34]);
check("môn phái: tu vi 10/100", [mp.tu_vi.hien, mp.tu_vi.max], [10, 100]);
check("môn phái: tấn công 7", mp.chi_so.tan_cong, 7);
check("môn phái: bạc vụn trong túi khớp bạc", mp.tui_do[0].so, 1);
check("môn phái có võ công phàm nhân", mp.ky_nang.includes("Thất Huyền quyền nhập môn"), true);
check("tán tu không có võ công", st.ky_nang.includes("Thất Huyền quyền nhập môn"), false);
check("môn phái khỏe hơn tán tu",
      mp.chi_so.sinh_luc.max > st.chi_so.sinh_luc.max, true);
check("môn phái đánh mạnh hơn tán tu",
      mp.chi_so.tan_cong > st.chi_so.tan_cong, true);
check("tán tu tu vi khởi đầu cao hơn môn phái",
      st.tu_vi.hien > mp.tu_vi.hien, true);
check("chỉ số lấy từ dữ liệu, không hardcode",
      Engine.chi_so_dau_cua("mon_phai").bac, 1);
check("nhóm lạ dùng chỉ số mặc định",
      Engine.chi_so_dau_cua("khong_co").bac, 3);
check("cảnh giới Luyện Khí tầng 1", st.canh_gioi, "Luyện Khí tầng 1");
check("nhóm lạ rơi về tan_tu", mk("B", "xyz").nhom_xuat_than, "tan_tu");

// Cảnh giới cuối chương PHẢI khớp nguyên văn truyện, nếu không truyện nói một đằng
// mà bảng chỉ số nói một nẻo. Tán tu: c1_d17 nói "Luyện Khí tầng ba".
// Môn phái: c1_p12 nói "Luyện Khí tầng hai", c1_p19 vẫn "tầng hai".
function diHet(nhom) {
  const s = mk("H", nhom);
  let r = Engine.bat_dau(s), buoc = 0, lo = {};
  while (!r.ket_thuc && buoc < 60 && r.lua_chon && r.lua_chon.length) {
    lo[r.doan_id] = s.canh_gioi;
    r = Engine.chon(s, 0); buoc++;
  }
  lo[r.doan_id] = s.canh_gioi;
  return { cuoi: r.doan_id, canh_gioi: s.canh_gioi, lo };
}
const hT = diHet("tan_tu");
check("tán tu kết chương ở c1_d17", hT.cuoi, "c1_d17");
check("tán tu kết Luyện Khí tầng 3 (đúng nguyên văn c1_d17)", hT.canh_gioi, "Luyện Khí tầng 3");
const hM = diHet("mon_phai");
check("môn phái kết chương ở c1_p19", hM.cuoi, "c1_p19");
check("môn phái lên tầng hai ở c1_p12 (đúng nguyên văn)", hM.lo["c1_p12"], "Luyện Khí tầng 2");
check("môn phái kết vẫn tầng hai (đúng nguyên văn c1_p19)", hM.canh_gioi, "Luyện Khí tầng 2");

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

console.log("\n=== N. Cơ duyên trong túi ===");
{
  const o = mk("CơDuyên", "mon_phai");
  Engine.bat_dau(o);
  check("túi đầu chưa có cơ duyên", o.tui_do.some((v) => v.co_duyen), false);
  let r2 = {};
  for (let i = 0; i < 12; i++) {
    r2 = Engine.chon(o, 0);
    if (o.tui_do.some((v) => v.co_duyen)) break;
  }
  const ngoc = o.tui_do.find((v) => v.ten === "Ngọc cốt bí ẩn");
  check("nhặt được Ngọc cốt", !!ngoc, true);
  check("Ngọc cốt có cờ co_duyen", ngoc && ngoc.co_duyen, true);
  check("trạng thái ban đầu", ngoc && ngoc.trang_thai, "chưa khế ước");
  check("có mô tả", !!(ngoc && ngoc.mo_ta), true);
  toi(o, "c1_p09", 20);
  Engine.chon(o, 0); // p09 → p09c
  r2 = Engine.chon(o, 0); // p09c "Ta ký" → p10
  const ngoc2 = r2.trang_thai.tui_do.find((v) => v.ten === "Ngọc cốt bí ẩn");
  check("ký khế ước → đổi trạng thái", ngoc2 && ngoc2.trang_thai, "đã khế ước · đang hồi phục");
  check("trạng thái ra tới giao diện", JSON.stringify(r2.trang_thai.tui_do).includes("đã khế ước"), true);
}

console.log("\n=== O. Ảnh cảnh truyện ===");
{
  const index = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "docs", "assets", "library", "index.json"), "utf8"));
  const chuong = JSON.parse(fs.readFileSync(path.join(GOC, "chuong1.json"), "utf8"));
  const co_anh = chuong.doan.filter((d) => d.hinh_anh && d.hinh_anh.anh);
  check("có đoạn gắn ảnh", co_anh.length > 0, true);
  check("tên ảnh có trong thư viện", co_anh.every((d) => index.anh[d.hinh_anh.anh]), true);
  check("đoạn gắn ảnh vẫn giữ tags", co_anh.every((d) => Array.isArray(d.hinh_anh.tags)), true);
  check("mọi mục thư viện có loai + tags", Object.values(index.anh).every((a) => a.loai && a.tags.length), true);
  // engine trả hinh_anh ra giao diện
  const o = mk("Anh", "tan_tu");
  const r = Engine.bat_dau(o);
  check("engine trả hinh_anh.anh ở d01", r.hinh_anh && r.hinh_anh.anh, "bc_cho_01.jpg");
  const r2 = Engine.chon(o, 0);
  check("đổi đoạn vẫn có ảnh", r2.hinh_anh && r2.hinh_anh.anh, "bc_cho_02.jpg");
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

  // ---------------------------------------------- N. Chuyển chương
  console.log("\n=== N. Chuyển chương 1 → 2 ===");

  // Chương 2 THẬT, đọc từ đĩa — không còn chương giả.
  const ch2 = JSON.parse(fs.readFileSync(path.join(GOC, "chuong2.json"), "utf8"));

  // Tới màn kết chương 1 bằng đường thật
  const o9 = mk("Chuyen", "tan_tu");
  Engine.bat_dau(o9);
  let r9 = null;
  for (let i = 0; i < 40; i++) {
    r9 = Engine.chon(o9, 0);
    // d17/p19 tu khai ket_thuc:true — phai di qua no moi toi man ket that
    if (r9.doan_id === "__ket_thuc__") break;
  }
  check("tới được màn kết chương 1", r9.ket_thuc, true);
  check("màn kết không có lựa chọn nào (ngõ cụt cũ)", r9.lua_chon.length, 0);
  check("màn kết chỉ sang chương 2", r9.chuong_sau, 2);

  // Nạp chương 2 thật rồi sang
  Engine.napChuong(2, JSON.parse(JSON.stringify(ch2)));
  check("nạp chương 2 → nút mở", Engine.goi_y_hien_tai(o9).chuong_sau_mo, true);

  // Ghi lại vài thứ để chắc chuyển chương không làm mất nhân vật
  o9.bac = 77;
  o9.canh_gioi = "Luyện Khí tầng 4";
  o9.co_su_kien = ["gap_han_lap"];
  o9.npc = { "Hàn Lập": { hao_cam: 35, thai_do: "quen biết" } };
  const tuiTruoc = o9.tui_do.length;
  const kyNangTruoc = o9.ky_nang.length;

  const r10 = Engine.sang_chuong(o9);
  check("sang được chương 2", o9.chuong, 2);
  check("đứng ở đoạn mở đầu của nhóm tán tu", r10.doan_id, "c2_d01");
  check("hết trạng thái kết thúc", o9.ket_thuc, false);
  check("GIỮ bạc", o9.bac, 77);
  check("GIỮ cảnh giới", o9.canh_gioi, "Luyện Khí tầng 4");
  check("GIỮ cờ sự kiện", o9.co_su_kien, ["gap_han_lap"]);
  check("GIỮ hảo cảm NPC", o9.npc["Hàn Lập"].hao_cam, 35);
  check("GIỮ túi đồ", o9.tui_do.length, tuiTruoc);
  check("GIỮ kỹ năng", o9.ky_nang.length, kyNangTruoc);
  check("có thông báo tên chương mới",
        r10.thong_bao[0].includes("Thái Nam"), true);
  check("ghi nhật ký chuyển chương",
        o9.nhat_ky[o9.nhat_ky.length - 1].viec, "Sang chương 2");
  check("chơi tiếp được ở chương 2", Engine.goi_y_hien_tai(o9).chuong, 2);

  // Môn phái phải vào đúng nhánh của mình, không rơi về đoạn đầu tiên
  const o10 = mk("Phai", "mon_phai");
  Engine.bat_dau(o10);
  for (let i = 0; i < 40; i++) if (Engine.chon(o10, 0).doan_id === "__ket_thuc__") break;
  Engine.sang_chuong(o10);
  check("nhóm môn phái vào đúng đoạn mở chương 2", o10.doan_hien_tai, "c2_p01");

  // Lời kết đọc từ dữ liệu chương, không viết cứng
  const o11 = mk("Ket", "tan_tu");
  Engine.bat_dau(o11);
  for (let i = 0; i < 40; i++) if (Engine.chon(o11, 0).doan_id === "__ket_thuc__") break;
  check("lời kết chương 1 lấy từ chuong1.json",
        Engine.goi_y_hien_tai(o11).ke.startsWith("Chương một khép lại"), true);

  // ---------------------------------------------- N2. Nội dung chương 2 thật
  console.log("\n=== N2. Nội dung chương 2 (Thái Nam Sơn Cốc) ===");

  check("chương 2 nạp được, không lỗi kết cấu",
        Engine.kiem_chuong(ch2).length, 0);
  check("tên chương đúng canon", ch2.ten, "Tiểu hội Thái Nam Sơn Cốc");
  check("có đủ hai lối vào theo nhóm",
        !!(ch2.doan_dau_theo_nhom.tan_tu && ch2.doan_dau_theo_nhom.mon_phai), true);
  check("mã đoạn theo quy ước c2_",
        ch2.doan.every(d => d.id.startsWith("c2_")), true);
  // Ảnh cảnh Chương 2 chưa làm xong: đoạn mới được phép không có ảnh (khung ảnh
  // tự ẩn), nhưng đoạn ĐÃ có ảnh thì ảnh phải tồn tại thật trên đĩa.
  check("đoạn cũ vẫn giữ ảnh, đoạn mới thì không bắt buộc",
        ch2.doan.every(d => d.hinh_anh === undefined || (d.hinh_anh && d.hinh_anh.anh)), true);
  check("mọi đoạn đều có chữ kể",
        ch2.doan.every(d => (d.ke || "").length >= 300), true);
  check("không nhắc chương sai canon cũ",
        JSON.stringify(ch2).includes("Huyết Sát"), false);

  // Mọi đoạn đều tới được màn kết, không nhánh cụt
  const theoId = {};
  for (const d of ch2.doan) theoId[d.id] = d;
  function toiKet(id, tham) {
    if (id === "__ket_thuc__") return true;
    if (tham.has(id) || !theoId[id]) return false;
    tham.add(id);
    const lcs = theoId[id].lua_chon || [];
    return lcs.length > 0 && lcs.some(l => toiKet(l.den, tham));
  }
  const cut = ch2.doan.filter(d => !toiKet(d.id, new Set())).map(d => d.id);
  check("không có đoạn cụt", cut, []);

  // Ảnh phải có thật trên đĩa
  const ANH = path.join(GOC, "..", "..", "assets", "scene");
  const thieu = [...new Set(ch2.doan.filter(d => d.hinh_anh).map(d => d.hinh_anh.anh))]
    .filter(f => !fs.existsSync(path.join(ANH, f)));
  check("mọi ảnh dùng trong chương 2 đều tồn tại", thieu, []);

  // Chơi thật 200 lượt mỗi nhóm, đi ngẫu nhiên, phải luôn tới kết
  for (const nhom of ["tan_tu", "mon_phai"]) {
    let hong = null;
    for (let lan = 0; lan < 200 && !hong; lan++) {
      const st = mk("C2", nhom);
      st.chuong = 2;
      st.doan_hien_tai = null;
      st.ket_thuc = false;
      let xong = false;
      for (let buoc = 0; buoc < 120; buoc++) {
        const kq = Engine.goi_y_hien_tai(st);
        if (kq.ket_thuc) { xong = true; break; }
        const mo = kq.lua_chon.map((l, i) => [l, i]).filter(([l]) => !l.khoa);
        if (!mo.length) { hong = `ngõ cụt ở ${kq.doan_id}`; break; }
        const chon = mo[Math.floor(Math.random() * mo.length)][1];
        const r = Engine.chon(st, chon);
        if (r.loi) { hong = `lỗi chọn ở ${kq.doan_id}: ${r.loi}`; break; }
      }
      if (!xong && !hong) hong = "không tới được màn kết";
    }
    check(`nhóm ${nhom}: 200 lượt chơi đều tới kết, không ngõ cụt`, hong, null);
  }

  // Cảnh báo tiền tệ: chương 2 phải có chỗ dạy người chơi tiền phàm vô dụng ở
  // chợ tu sĩ, và tiền ở đây là linh thạch.
  check("có đoạn nói rõ tiền phàm không dùng được ở chợ tu sĩ",
        ch2.doan.some(d => (d.ke || "").includes("Thứ tiền của người tu hành")), true);

  console.log("\n=== O. Bắt lỗi dữ liệu chương ===");
  check("đích trỏ vào đoạn không có → báo lỗi",
        Engine.kiem_chuong({
          doan: [{ id: "x1", lua_chon: [{ chu: "đi", den: "x2" }] }],
        }).length, 1);
  check("thông báo lỗi nêu đúng mã sai",
        Engine.kiem_chuong({
          doan: [{ id: "x1", lua_chon: [{ chu: "đi", den: "x2" }] }],
        })[0].includes("x2"), true);
  check("mã đoạn trùng → báo lỗi",
        Engine.kiem_chuong({ doan: [{ id: "x1" }, { id: "x1" }] })[0].includes("trùng"), true);
  check("đoạn mở đầu trỏ sai → báo lỗi",
        Engine.kiem_chuong({
          doan: [{ id: "x1" }], doan_dau_theo_nhom: { tan_tu: "x9" },
        })[0].includes("x9"), true);
  check("chương 1 thật không có lỗi",
        Engine.kiem_chuong(
          JSON.parse(fs.readFileSync(path.join(GOC, "chuong1.json"), "utf8"))).length, 0);
  let nem = false;
  try { Engine.napChuong(9, { doan: [{ id: "a", lua_chon: [{ chu: "x", den: "b" }] }] }); }
  catch (e) { nem = true; }
  check("nạp chương hỏng thì ném lỗi, không im lặng", nem, true);

  // Lời kết và đoạn dùng chung hiện cho cả hai nhánh — lộ giọng riêng là hỏng.
  const ch2kt = JSON.parse(fs.readFileSync(path.join(GOC, "chuong2.json"), "utf8"));
  const loNhanh = ["ăn mày", "túi bạc", "tạp dịch"];
  const chung = ch2kt.doan.filter((d) => /^c2_c/.test(d.id));
  // Bỏ lời thoại trong ngoặc kép: nhân vật nói về thân phận mình là chuyện khác
  // với người kể gán thân phận cho người chơi.
  const loiKe = (d) => d.ke.replace(/“[^”]*”/g, "");
  const vet = chung.flatMap((d) => loNhanh.filter((t) => loiKe(d).includes(t))
                                  .map((t) => `${d.id}:${t}`));
  check("đoạn dùng chung không lộ giọng riêng của nhánh", vet, []);
  check("lời kết chương 2 không lộ giọng riêng của nhánh",
        loNhanh.filter((t) => (ch2kt.ket?.ke || "").includes(t)), []);
  check("lời kết không lặp câu chuyển chương đã có ở đoạn cuối",
        (ch2kt.ket?.ke || "").includes("Chương sau") &&
        (chung.at(-1)?.ke || "").includes("Chương sau"), false);

  // -------------------------------------------------- N3. Hảo cảm đổi giọng kể
  {
    Engine.napChuong(2, JSON.parse(fs.readFileSync(path.join(GOC, "chuong2.json"), "utf8")));
    const ch2h = Engine.load_chuong(2);
    const theoId = {};
    for (const d of ch2h.doan) theoId[d.id] = d;

    // goi_y_hien_tai đọc hảo cảm từ state, nên dựng state trỏ thẳng vào đoạn cần xem.
    const xem = (did, diem) => {
      const st = Engine.trang_thai_moi("T", "", "tan_tu");
      st.chuong = 2;
      st.doan_hien_tai = did;
      st.npc = { "Hàn Lập": { hao_cam: diem, thai_do: Engine.muc_hao_cam(diem) } };
      return Engine.goi_y_hien_tai(st);
    };

    // c2_d06 là đoạn còn bien_the sau khi hai nhánh tách riêng (c2_c18 đã bỏ).
    const c18 = [-80, -30, 0, 30].map((d) => xem("c2_d06", d).ke);
    check("c2_d06 đổi giọng theo 4 mức hảo cảm", 4, new Set(c18).size);
    // Giọng đổi được, sự việc thì không.
    check("mọi biến thể vẫn giữ nguyên sự việc gốc",
          true, c18.every((t) => t.includes("Mang di vật của sư phụ về")));

    // Cùng một mức hảo cảm phải ra cùng một câu (không phụ thuộc thứ tự gọi).
    check("cùng mức hảo cảm → cùng câu kể",
          xem("c2_d06", -80).ke, xem("c2_d06", -80).ke);

    // Đoạn không có bien_the thì không đổi.
    const khongBt = ch2h.doan.find((d) => !d.bien_the);
    check("đoạn không có bien_the thì không đổi theo hảo cảm",
          1, new Set([-80, 0, 95].map((d) => xem(khongBt.id, d).ke)).size);

    // NPC phải được báo cho AI kể, kèm thái độ hiện tại.
    const kq18 = xem("c2_d06", -75);
    check("cảnh báo đúng NPC cho AI", ["Hàn Lập"], (kq18.npc_trong_canh || []).map((n) => n.ten));
    check("  kèm đúng thái độ", "tử địch", (kq18.npc_trong_canh || [{}])[0].thai_do);
    check("  kèm đúng điểm hảo cảm", -75, (kq18.npc_trong_canh || [{}])[0].hao_cam);

    // Chưa gặp NPC thì không bịa ra thái độ.
    const stTrong = Engine.trang_thai_moi("T", "", "tan_tu");
    stTrong.chuong = 2;
    stTrong.doan_hien_tai = "c2_d06";
    stTrong.npc = {};
    check("NPC chưa gặp thì không có trong danh sách",
          [], Engine.goi_y_hien_tai(stTrong).npc_trong_canh);

    // Hảo cảm thấp phải với tới được, và phải dẫn tới đoạn kết khác.
    const lo = {}, hi = {};
    const di = (sid, aff, sau) => {
      if (sau > 60 || !theoId[sid]) return;
      lo[sid] = Math.min(lo[sid] ?? 9e9, aff);
      hi[sid] = Math.max(hi[sid] ?? -9e9, aff);
      for (const lc of theoId[sid].lua_chon || []) {
        const a = aff + (((lc.hieu_ung || {}).hao_cam || {})["Hàn Lập"] || 0);
        if (lc.den && lc.den !== "__ket_thuc__") di(lc.den, a, sau + 1);
      }
    };
    for (const dau of Object.values(ch2h.doan_dau_theo_nhom)) di(dau, 0, 0);
    // Hai nhánh tách riêng nên mỗi nhánh có đoạn chốt riêng.
    for (const chot of ["c2_d28", "c2_p24"]) {
      check(`${chot}: đi được xuống mức thù địch`, true, lo[chot] <= -20);
      check(`${chot}:   và lên được mức thân thiết`, true, hi[chot] >= 50);
    }

    const khoa = ch2h.doan.flatMap((d) => (d.lua_chon || [])
      .filter((lc) => lc.dieu_kien && lc.dieu_kien.hao_cam).map(() => d.id));
    check("có lựa chọn bị khoá theo hảo cảm", true, khoa.length >= 3);
    // Mỗi nhánh có kết riêng cho hảo cảm thấp, chỉ mở khi chưa đủ thân.
    const ketThap = ["c2_d29x", "c2_p25x"];
    check("có nhánh kết riêng cho hảo cảm thấp",
          true, ketThap.every((id) => ch2h.doan.some((d) => d.id === id)));

    // ------------------------------------------- N4. Nhận vật phẩm khớp lời kể
    const duongToi = (dau, dich) => {
      const q = [[dau, []]], tham = new Set([dau]);
      while (q.length) {
        const [sid, p] = q.shift();
        if (sid === dich) return p;
        for (let i = 0; i < (theoId[sid].lua_chon || []).length; i++) {
          const den = theoId[sid].lua_chon[i].den;
          if (den && den !== "__ket_thuc__" && theoId[den] && !tham.has(den)) {
            tham.add(den); q.push([den, [...p, i]]);
          }
        }
      }
      return null;
    };
    const choi = (dich) => {
      const st = Engine.trang_thai_moi("T", "", "tan_tu");
      st.chuong = 2;
      Engine.bat_dau(st);
      for (const i of duongToi(st.doan_hien_tai, dich)) Engine.chon(st, i);
      return st;
    };
    const tui = (st) => Object.fromEntries(st.tui_do.map((v) => [v.ten, v.so ?? 1]));

    // Nhận lệnh ở c2_d28 thì túi có đúng một tấm; từ chối thì không có tấm nào.
    const stNhan = choi("c2_d28");
    stNhan.npc["Hàn Lập"] = { hao_cam: 100, thai_do: Engine.muc_hao_cam(100) };
    Engine.chon(stNhan, 0);
    check("nhận lệnh → túi có 1 Thăng Tiên Lệnh",
          tui(stNhan)["Thăng Tiên Lệnh"], 1);
    check("  không có hai dòng cùng tên trong túi",
          stNhan.tui_do.length === new Set(stNhan.tui_do.map((v) => v.ten)).size, true);

    const stTuChoi = choi("c2_d28");
    stTuChoi.npc["Hàn Lập"] = { hao_cam: 100, thai_do: Engine.muc_hao_cam(100) };
    Engine.chon(stTuChoi, theoId["c2_d28"].lua_chon
      .findIndex((lc) => lc.chu.startsWith("Không nhận")));
    check("từ chối lệnh → túi không có Thăng Tiên Lệnh",
          tui(stTuChoi)["Thăng Tiên Lệnh"], undefined);

    // Đoạn nào nói "Nhận:" thì phải thật sự thêm vật phẩm.
    const thieuVat = ch2h.doan.filter((d) => (d.ke || "").includes("Nhận:") &&
      (d.lua_chon || []).length &&
      !d.lua_chon.some((lc) => (lc.hieu_ung || {}).them_vat)).map((d) => d.id);
    check("đoạn báo “Nhận:” thì phải thật sự thêm vật phẩm", thieuVat, []);

    // --------------------------------------- N5. Kết xấu chỉ dành cho hảo cảm thấp
    const khoaKetXau = (did, chu, diem) => {
      const st = Engine.trang_thai_moi("T", "", "tan_tu");
      st.chuong = 2;
      st.doan_hien_tai = did;
      st.npc = { "Hàn Lập": { hao_cam: diem, thai_do: Engine.muc_hao_cam(diem) } };
      return Engine.goi_y_hien_tai(st).lua_chon
        .filter((lc) => lc.chu.startsWith(chu)).map((lc) => !!lc.khoa);
    };
    check("tán tu: kết xa cách bị khoá khi hảo cảm đã cao",
          khoaKetXau("c2_d28", "“Ngươi giữ đi", 75), [true]);
    check("tán tu: kết xa cách mở khi hảo cảm thấp",
          khoaKetXau("c2_d28", "“Ngươi giữ đi", 20), [false]);
    check("môn phái: kết xa cách bị khoá khi hảo cảm đã cao",
          khoaKetXau("c2_p24", "“Đi đi", 75), [true]);
    check("môn phái: kết xa cách mở khi hảo cảm thấp",
          khoaKetXau("c2_p24", "“Đi đi", 20), [false]);
  }

  console.log(`\n${"=".repeat(46)}\nKẾT QUẢ: ${ok} đạt, ${fail} hỏng`);
  process.exit(fail ? 1 : 0);
})();
