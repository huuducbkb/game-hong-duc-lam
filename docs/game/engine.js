/* Engine game Hồng Đức Tu Tiên Lộ — bản JavaScript (chạy trong trình duyệt).
 *
 * Dịch từ game/engine.py. Cơ chế "chương + đoạn": đoạn đi một chiều, đánh dấu
 * `da_qua` để chống lặp. Trạng thái lưu vào localStorage (thay cho file trên máy chủ).
 *
 * Chạy được ở 2 nơi: trình duyệt (window.Engine) và Node (require).
 */
(function (goc) {
  "use strict";

  const HE_PHAP = ["kim", "moc", "thuy", "hoa", "tho", "loi", "phong", "bang", "doc"];

  const CANH_GIOI = [
    "Luyện Khí tầng 1", "Luyện Khí tầng 2", "Luyện Khí tầng 3", "Luyện Khí tầng 4",
    "Luyện Khí tầng 5", "Luyện Khí tầng 6", "Luyện Khí tầng 7", "Luyện Khí tầng 8",
    "Luyện Khí tầng 9", "Luyện Khí tầng 10", "Luyện Khí tầng 11", "Luyện Khí tầng 12",
    "Luyện Khí tầng 13", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần",
  ];

  const MUC_HAO_CAM = [
    [-100, -60, "tử địch"],
    [-59, -20, "thù địch"],
    [-19, 19, "người dưng"],
    [20, 49, "quen biết"],
    [50, 79, "thân thiết"],
    [80, 100, "tri kỷ"],
  ];

  const KHOA_LUU = "hdttl_save_";

  // ---------------------------------------------------------------- tu luyện
  // Bản dịch của khối tu luyện trong game/engine.py. Mọi phép đổ xúc xắc dùng
  // hạt giống sinh từ (tên nhân vật, số ngày đã dùng) — PHẢI cho đúng cùng dãy
  // số với bản Python, không thì test đối chiếu ở khối TL sẽ bắt được.

  const NGAY_MOI_CHUONG = 30;
  const TRAN_CANH_GIOI = { 2: "Luyện Khí tầng 6" };

  const TL_VIEC = {
    da_toa: { ten: "Đả tọa", ngay: 3 },
    san: { ten: "Săn yêu thú", ngay: 2 },
    luyen_dan: { ten: "Luyện đan", ngay: 1 },
    cho: { ten: "Đi chợ", ngay: 1 },
    do_la: { ten: "Dò la", ngay: 2 },
  };

  // 8 chỉ cho 80 tu vi trong 30 ngày, mà cần 88 để lên tầng 2. 12 cho 120.
  const TL_TU_VI_DA_TOA = 12;

  const TL_YEU_THU = [
    { ma: "son_tru", ten: "Sơn Trư", hang: "thuong", bac: 1, vat: "Nanh sói", so_vat: 1, tu_vi: 4, nguy_hiem: 25 },
    { ma: "thanh_xa", ten: "Thanh Xà", hang: "thuong", bac: 1, vat: "Mật xà", so_vat: 1, tu_vi: 4, nguy_hiem: 30 },
    { ma: "bach_tho", ten: "Bạch Thố Tinh", hang: "thuong", bac: 1, vat: "Linh thảo", so_vat: 2, tu_vi: 3, nguy_hiem: 15 },
    { ma: "da_lang", ten: "Dã Lang", hang: "thuong", bac: 2, vat: "Nanh sói", so_vat: 2, tu_vi: 5, nguy_hiem: 35 },
    { ma: "hac_thu", ten: "Hắc Thử", hang: "thuong", bac: 1, vat: "Bạc vụn", so_vat: 2, tu_vi: 3, nguy_hiem: 20 },
    { ma: "hac_lang", ten: "Hắc Lang Tinh Anh", hang: "tinh_anh", bac: 3, vat: "Nanh sói", so_vat: 3, tu_vi: 9, nguy_hiem: 40 },
    { ma: "thiet_giap", ten: "Thiết Giáp Thử", hang: "tinh_anh", bac: 3, vat: "Mật xà", so_vat: 2, tu_vi: 9, nguy_hiem: 40 },
    { ma: "xich_vien", ten: "Xích Viên Tinh Anh", hang: "tinh_anh", bac: 4, vat: "Linh thảo", so_vat: 3, tu_vi: 11, nguy_hiem: 45 },
    { ma: "bach_lang_vuong", ten: "Bạch Lang Yêu Vương", hang: "yeu_vuong", bac: 5, vat: "Nanh sói", so_vat: 5, tu_vi: 20, nguy_hiem: 55 },
    { ma: "hac_xa_vuong", ten: "Hắc Xà Yêu Vương", hang: "yeu_vuong", bac: 6, vat: "Mật xà", so_vat: 5, tu_vi: 24, nguy_hiem: 60 },
  ];

  const TL_GAP = { thuong: 62, tinh_anh: 30, yeu_vuong: 8 };
  const TL_NGUONG = { thuong: 0, tinh_anh: 2, yeu_vuong: 4 };

  const TL_CONG_THUC = [
    {
      ma: "tu_khi_dan", ten: "Tụ Khí Đan", ngay: 1, bac: 2, ti_le: 70,
      can: { "Nanh sói": 1, "Linh thảo": 2 }, tu_vi: 15,
      mo_ta: "Đan dược cơ bản, tụ khí vào đan điền.",
    },
    {
      ma: "hoi_luc_dan", ten: "Hồi Lực Đan", ngay: 1, bac: 3, ti_le: 65,
      can: { "Mật xà": 1, "Linh thảo": 1 }, sinh_luc: 12,
      mo_ta: "Hồi sinh lực, dùng được sau khi bị thương.",
    },
  ];

  const TL_TIN = [
    { ma: "bi_thuong", ten: "Kẻ gác cổng bị thương ở vai",
      ke: "Nghe nói kẻ gác cổng bị thương ở vai, mỗi đêm phải ra suối rửa vết." },
    { ma: "thoi_quen", ten: "Nó ngủ say trước giờ Dần",
      ke: "Một lão tiều phu nói kẻ gác cổng ngủ say trước giờ Dần, gọi mãi không dậy." },
    { ma: "so_lenh_bai", ten: "Lệnh bài cũ bán ở chợ đen",
      ke: "Chợ đen dưới chân núi có bán lệnh bài cũ, kẻ gác cổng thấy là cho qua." },
  ];

  const TL_CHO_HANG = [
    { ma: "linh_thao", ten: "Linh thảo", gia: 2, so: 1, mo_ta: "Nguyên liệu luyện đan." },
    { ma: "banh_nuong", ten: "Bánh nướng", gia: 1, so: 1, mo_ta: "Ăn hồi 3 sinh lực." },
  ];

  function _hat_giong(ten, ngay) {
    let h = 2166136261;
    const s = String(ten) + "|" + String(ngay);
    const b = new TextEncoder().encode(s);
    for (let i = 0; i < b.length; i++) {
      h ^= b[i];
      h = Math.imul(h, 16777619) >>> 0;
    }
    return h >>> 0;
  }

  function _ngau_nhien(hat, buoc) {
    let x = (hat + Math.imul(buoc, 2654435761)) >>> 0;
    x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
    return x / 4294967296;
  }

  function tl_moi() {
    return { ngay_con: NGAY_MOI_CHUONG, ngay_da_dung: 0, nhat_ky: [], tin_da_biet: [] };
  }

  function _tl(state) {
    if (!state.tu_luyen || typeof state.tu_luyen !== "object") {
      state.tu_luyen = tl_moi();
    }
    const tl = state.tu_luyen;
    if (tl.ngay_con === undefined) tl.ngay_con = NGAY_MOI_CHUONG;
    if (tl.ngay_da_dung === undefined) tl.ngay_da_dung = 0;
    if (!tl.nhat_ky) tl.nhat_ky = [];
    if (!tl.tin_da_biet) tl.tin_da_biet = [];
    return tl;
  }

  function _tl_ngau(state) {
    const tl = _tl(state);
    return _ngau_nhien(_hat_giong(state.ten_nhan_vat || "", tl.ngay_da_dung), tl.nhat_ky.length);
  }

  function _tl_ghi(state, viec, ngay) {
    const tl = _tl(state);
    tl.ngay_con = Math.max(0, tl.ngay_con - ngay);
    tl.ngay_da_dung += ngay;
    tl.nhat_ky.push(`Ngày ${tl.ngay_da_dung}: ${viec}`);
    if (tl.nhat_ky.length > 40) tl.nhat_ky = tl.nhat_ky.slice(-40);
  }

  function _tl_con_ngay(state, ngay) {
    return _tl(state).ngay_con >= ngay;
  }

  function _tl_co(state, ten_vat) {
    for (const v of state.tui_do) {
      if (v.ten === ten_vat) return v.so || 0;
    }
    return 0;
  }

  function _tl_bot(state, ten_vat, so) {
    for (let i = 0; i < state.tui_do.length; i++) {
      const v = state.tui_do[i];
      if (v.ten === ten_vat) {
        v.so = (v.so || 0) - so;
        if (v.so <= 0) state.tui_do.splice(i, 1);
        return;
      }
    }
  }

  function _tl_con_suc(state) {
    const sl = state.chi_so.sinh_luc;
    return sl.hien > sl.max * 0.3;
  }

  function _tl_chi_so(state) {
    const cs = state.chi_so;
    const tl = _tl(state);
    return {
      ngay_con: tl.ngay_con,
      ngay_da_dung: tl.ngay_da_dung,
      trong_dong: !!state.trong_dong,
      canh_gioi: state.canh_gioi,
      tran: TRAN_CANH_GIOI[state.chuong] || null,
      tu_vi: Object.assign({}, state.tu_vi),
      sinh_luc: Object.assign({}, cs.sinh_luc),
      linh_luc: Object.assign({}, cs.linh_luc),
      bac: state.bac,
      tan_cong: cs.tan_cong,
      phong_thu: cs.phong_thu,
      nhat_ky: tl.nhat_ky.slice(-8),
      tin_da_biet: TL_TIN.filter((t) => tl.tin_da_biet.includes(t.ma))
        .map((t) => ({ ma: t.ma, ten: t.ten })),
      con_suc: _tl_con_suc(state),
    };
  }

  function tl_trang_thai(state) {
    const chi = _tl_chi_so(state);
    const viec = [];
    for (const ma of Object.keys(TL_VIEC)) {
      const v = TL_VIEC[ma];
      let duoc = chi.ngay_con >= v.ngay;
      let ghi_chu = "";
      if (ma === "san" && !chi.con_suc) {
        duoc = false;
        ghi_chu = "Đang bị thương — nghỉ trước đã";
      }
      if (ma === "da_toa") {
        ghi_chu = `+${TL_TU_VI_DA_TOA} tu vi`;
        if (chi.tran && chi.canh_gioi === chi.tran) ghi_chu = "Đã chạm trần chương";
      }
      if (ma === "san") ghi_chu = ghi_chu || "Săn yêu thú, lấy nguyên liệu";
      if (ma === "luyen_dan") ghi_chu = `${TL_CONG_THUC.length} công thức`;
      if (ma === "cho") ghi_chu = `${TL_CHO_HANG.length} món bán`;
      if (ma === "do_la") ghi_chu = "Có thể nghe tin về kẻ gác cổng";
      viec.push({ ma, ten: v.ten, ngay: v.ngay, ghi_chu, duoc });
    }
    return { chi_so: chi, viec };
  }

  function _tl_kiem_tra(state, ma_viec) {
    const v = TL_VIEC[ma_viec];
    if (!v) return { loi: "Việc không có trong động phủ" };
    if (state.ket_thuc) return { loi: "Chương đã khép lại — không tu luyện được nữa" };
    if (!_tl_con_ngay(state, v.ngay)) {
      return { loi: `Không đủ ngày (cần ${v.ngay}, còn ${_tl(state).ngay_con})` };
    }
    if (ma_viec === "san" && !_tl_con_suc(state)) {
      return { loi: "Đang bị thương nặng — nghỉ cho hồi sinh lực đã" };
    }
    return null;
  }

  function tl_da_toa(state) {
    const loi = _tl_kiem_tra(state, "da_toa");
    if (loi) return loi;
    _tl_ghi(state, "đả tọa", TL_VIEC.da_toa.ngay);
    const tb = _ap_hieu_ung(state, { tu_vi: TL_TU_VI_DA_TOA });
    return {
      ok: true,
      thong_bao: tb.length ? tb : [`Tu vi +${TL_TU_VI_DA_TOA}`],
      chi_so: _tl_chi_so(state),
    };
  }

  function _tl_con_thua(state) {
    return (state.tu_luyen && state.tu_luyen.da_thua) ? state.tu_luyen.da_thua.slice() : [];
  }

  // Chọn yêu thú: không gặp lại con vừa thua, hạng theo cảnh giới.
  function _tl_chon_thu(state) {
    const tl = _tl(state);
    const da_thua = _tl_con_thua(state);
    const bac_minh = CANH_GIOI.indexOf(state.canh_gioi);
    let hop = Object.keys(TL_NGUONG).filter(h => bac_minh >= TL_NGUONG[h]);
    if (!hop.length) hop = ["thuong"];
    // Bỏ con vừa đánh (dù thắng hay thua) — gặp lại y nguyên con cũ ngay lượt sau
    // là đúng cái người dùng báo là "kẹt".
    const vua = tl.vua_gap;
    const loai = da_thua.concat(vua ? [vua] : []);
    let ung_vien = TL_YEU_THU.filter(t => hop.includes(t.hang) && !loai.includes(t.ma));
    if (!ung_vien.length) {
      // Thua hết cả nhóm. Ban vĩnh viễn là sai: bảng sẽ cạn và quay lại đúng con
      // vừa thua. Cho thử lại từ đầu nhưng VẪN tránh con vừa đánh.
      tl.da_thua = [];
      ung_vien = TL_YEU_THU.filter(t => hop.includes(t.hang) && t.ma !== vua);
    }
    if (!ung_vien.length) ung_vien = TL_YEU_THU.filter(t => t.hang === "thuong" && t.ma !== vua);
    if (!ung_vien.length) ung_vien = TL_YEU_THU.slice();
    const r = _tl_ngau(state);
    const tong = hop.reduce((a, h) => a + TL_GAP[h], 0) || 1;
    let diem = r * tong;
    let chon_hang = hop[0];
    for (const h of hop) {
      diem -= TL_GAP[h];
      if (diem <= 0) { chon_hang = h; break; }
    }
    let trong_hang = ung_vien.filter(t => t.hang === chon_hang);
    if (!trong_hang.length) trong_hang = ung_vien;
    const r2 = _tl_ngau(state);
    const thu = trong_hang[Math.floor(r2 * trong_hang.length) % trong_hang.length];
    tl.muc_tieu = thu.ma;
    tl.vua_gap = thu.ma;
    return thu;
  }

  function tl_san(state) {
    return tl_danh(state);
  }

  function _ti_le_thang(state, thu) {
    const cs = state.chi_so;
    const bac_minh = CANH_GIOI.indexOf(state.canh_gioi);
    const chenh = bac_minh - thu.bac;
    const goc = 50 + chenh * 22 + (cs.tan_cong - 5) * 3;
    return Math.max(5, Math.min(95, goc));
  }

  // Xem trận KHÔNG tốn ngày và KHÔNG khoá khi bị thương — chỉ đánh mới cần sức.
  function tl_dau(state) {
    if (state.ket_thuc) return { loi: "Chương đã khép lại — không tu luyện được nữa" };
    const tl = _tl(state);
    let thu = TL_YEU_THU.find(t => t.ma === tl.muc_tieu);
    if (!thu || _tl_con_thua(state).includes(tl.muc_tieu)) thu = _tl_chon_thu(state);
    return { ok: true, tran: { ma: thu.ma, ten: thu.ten, hang: thu.hang,
      bac: CANH_GIOI[thu.bac], ti_le: _ti_le_thang(state, thu),
      vat: thu.vat, so_vat: thu.so_vat } };
  }

  function tl_danh(state, so_hiep) {
    so_hiep = so_hiep || 3;
    const loi = _tl_kiem_tra(state, "san");
    if (loi) return loi;
    const tl = _tl(state);
    let thu = TL_YEU_THU.find(t => t.ma === tl.muc_tieu);
    if (!thu || _tl_con_thua(state).includes(tl.muc_tieu)) thu = _tl_chon_thu(state);
    const ti_le = _ti_le_thang(state, thu);
    _tl_ghi(state, `đánh ${thu.ten}`, TL_VIEC.san.ngay);
    const cs = state.chi_so.sinh_luc;
    const dong = [];
    const thang = _tl_ngau(state) * 100 < ti_le;
    for (let i = 0; i < so_hiep; i++) {
      // Mỗi hiệp 2–3 sinh lực (trước là 4–8): một trận mất 6–9, đánh được 3–4
      // trận mới phải nghỉ.
      const tru = 2 + Math.floor(_tl_ngau(state) * 2);
      cs.hien = Math.max(1, cs.hien - tru);
      dong.push(`Hiệp ${i + 1}: ngươi bị cắn, sinh lực -${tru} (còn ${cs.hien})`);
      if (cs.hien <= cs.max * 0.3) break;
    }
    let tb = [];
    if (thang) {
      _ap_hieu_ung(state, { them_vat: [{ ten: thu.vat, so: thu.so_vat }] });
      tb = _ap_hieu_ung(state, { tu_vi: thu.tu_vi });
      dong.push(`— THẮNG: ${thu.ten} gục, ${thu.vat} +${thu.so_vat}`);
      if ((tl.da_thua || []).includes(thu.ma)) tl.da_thua = tl.da_thua.filter(m => m !== thu.ma);
      tl.muc_tieu = null;
    } else {
      cs.hien = Math.max(1, cs.hien - 4);
      tl.da_thua = tl.da_thua || [];
      if (!tl.da_thua.includes(thu.ma)) tl.da_thua.push(thu.ma);
      tl.muc_tieu = null;
      dong.push("— THUA: bị thương, sinh lực -6. Lượt sau sẽ gặp con khác.");
    }
    const goi_y = _tl_chon_thu(state);
    return { ok: true, thang, dong, thong_bao: tb, chi_so: _tl_chi_so(state),
      muc_tieu_sau: { ten: goi_y.ten, hang: goi_y.hang, ti_le: _ti_le_thang(state, goi_y) } };
  }

  function tl_cong_thuc(state) {
    const ra = [];
    for (const ct of TL_CONG_THUC) {
      const can = [];
      let du = true;
      for (const ten of Object.keys(ct.can)) {
        const so = ct.can[ten];
        const co = _tl_co(state, ten);
        if (co < so) du = false;
        can.push({ ten, can: so, co });
      }
      if (state.bac < ct.bac) du = false;
      ra.push(Object.assign({}, ct, { can_chi_tiet: can, duoc: du }));
    }
    return ra;
  }

  function tl_luyen_dan(state, ma) {
    const ct = TL_CONG_THUC.find((c) => c.ma === ma);
    if (!ct) return { loi: "Công thức không có" };
    if (!_tl_con_ngay(state, ct.ngay)) return { loi: `Không đủ ngày (cần ${ct.ngay})` };
    for (const ten of Object.keys(ct.can)) {
      if (_tl_co(state, ten) < ct.can[ten]) {
        return { loi: `Thiếu ${ten} (cần ${ct.can[ten]}, có ${_tl_co(state, ten)})` };
      }
    }
    if (state.bac < ct.bac) return { loi: `Không đủ bạc (cần ${ct.bac})` };
    for (const ten of Object.keys(ct.can)) _tl_bot(state, ten, ct.can[ten]);
    state.bac -= ct.bac;
    _tl_ghi(state, `luyện ${ct.ten}`, ct.ngay);
    if (_tl_ngau(state) * 100 < ct.ti_le) {
      const hieu = { them_vat: [{ ten: ct.ten, so: 1 }] };
      if (ct.tu_vi !== undefined) hieu.tu_vi = ct.tu_vi;
      if (ct.sinh_luc !== undefined) hieu.sinh_luc = ct.sinh_luc;
      const tb = _ap_hieu_ung(state, hieu);
      return {
        ok: true, thanh_cong: true,
        thong_bao: [`Ra lò ${ct.ten}!`].concat(tb), chi_so: _tl_chi_so(state),
      };
    }
    return {
      ok: true, thanh_cong: false,
      thong_bao: [`Mẻ ${ct.ten} hỏng — mất nguyên liệu`], chi_so: _tl_chi_so(state),
    };
  }

  function tl_cho() {
    return TL_CHO_HANG.map((h) => Object.assign({}, h));
  }

  function tl_mua(state, ma) {
    const hang = TL_CHO_HANG.find((h) => h.ma === ma);
    if (!hang) return { loi: "Món này không bán" };
    if (!_tl_con_ngay(state, TL_VIEC.cho.ngay)) return { loi: "Không đủ ngày" };
    if (state.bac < hang.gia) {
      return { loi: `Không đủ bạc (cần ${hang.gia}, có ${state.bac})` };
    }
    state.bac -= hang.gia;
    _tl_ghi(state, `mua ${hang.ten}`, TL_VIEC.cho.ngay);
    _ap_hieu_ung(state, { them_vat: [{ ten: hang.ten, so: hang.so }] });
    return { ok: true, thong_bao: [`Mua ${hang.ten} (-${hang.gia} bạc)`], chi_so: _tl_chi_so(state) };
  }

  function tl_do_la(state) {
    const loi = _tl_kiem_tra(state, "do_la");
    if (loi) return loi;
    _tl_ghi(state, "dò la", TL_VIEC.do_la.ngay);
    const tl = _tl(state);
    const con = TL_TIN.filter((t) => !tl.tin_da_biet.includes(t.ma));
    const r = _tl_ngau(state);
    if (r < 0.55 || con.length === 0) {
      return {
        ok: true, tin: null,
        thong_bao: ["Dò la cả buổi, chỉ nghe chuyện vặt — không có gì dùng được"],
        chi_so: _tl_chi_so(state),
      };
    }
    const tin = con[Math.floor(r * 1000) % con.length];
    tl.tin_da_biet.push(tin.ma);
    return { ok: true, tin, thong_bao: [`Nghe được: ${tin.ke}`], chi_so: _tl_chi_so(state) };
  }

  function tl_nghi(state) {
    if (!_tl_con_ngay(state, 1)) return { loi: "Không còn ngày để nghỉ" };
    _tl_ghi(state, "nghỉ cho hồi sức", 1);
    const tb = _ap_hieu_ung(state, { sinh_luc: 12 });
    return { ok: true, thong_bao: ["Nghỉ một ngày."].concat(tb), chi_so: _tl_chi_so(state) };
  }

  function vao_dong(state) {
    if (state.ket_thuc) return { loi: "Chương đã khép lại — không tu luyện được nữa" };
    state.trong_dong = true;
    return Object.assign({ ok: true }, tl_trang_thai(state));
  }

  function ra_dong(state) {
    state.trong_dong = false;
    _ghi_nhat_ky(state, `Xuất động (tu vi ${state.tu_vi.hien}, ${state.canh_gioi})`);
    const kq = state.ket_thuc ? _man_ket_chuong(state) : _goi_y(state);
    kq.thong_bao = [`Xuất động: ${state.canh_gioi}, tu vi ${state.tu_vi.hien}`];
    return kq;
  }


  function muc_hao_cam(diem) {
    for (const [lo, hi, ten] of MUC_HAO_CAM) {
      if (lo <= diem && diem <= hi) return ten;
    }
    return "người dưng";
  }

  function _zero_he() {
    const o = {};
    for (const h of HE_PHAP) o[h] = 0;
    return o;
  }

  function _saoChepSau(x) {
    return typeof structuredClone === "function"
      ? structuredClone(x)
      : JSON.parse(JSON.stringify(x));
  }

  function _now() {
    // Giống Python datetime.now().isoformat(timespec="seconds")
    const d = new Date();
    const p = (n) => String(n).padStart(2, "0");
    return (
      d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()) +
      "T" + p(d.getHours()) + ":" + p(d.getMinutes()) + ":" + p(d.getSeconds())
    );
  }

  // ---------------------------------------------------------------- dữ liệu
  let _xt = null;
  const _chuong = {};

  function napXuatThan(o) {
    _xt = o;
  }

  function napChuong(so, o) {
    const loi = kiem_chuong(o);
    if (loi.length) {
      throw new Error(`chuong${so}.json hỏng: ` + loi.slice(0, 5).join("; "));
    }
    o._theo_id = {};
    for (const d of o.doan) o._theo_id[d.id] = d;
    _chuong[so] = o;
  }

  function load_xuat_than() {
    if (!_xt) throw new Error("Chưa nạp xuat_than.json (gọi napXuatThan trước)");
    return _xt;
  }

  function ds_xuat_than(ke_ca_an) {
    return load_xuat_than().nhom.filter((n) => ke_ca_an || !n.an);
  }

  function _khong_dau(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d");
  }

  function nhan_dien_xuat_than(xuat_than) {
    const t = _khong_dau(xuat_than);
    for (const n of load_xuat_than().nhom) {
      if (n.an) continue;
      for (const tk of n.tu_khoa || []) {
        if (t.includes(_khong_dau(tk))) return n.ma;
      }
    }
    return "tan_tu";
  }

  function doan_dau_cua(nhom, so_chuong) {
    if (so_chuong === undefined || so_chuong === null) {
      for (const n of load_xuat_than().nhom) {
        if (n.ma === nhom) return n.doan_dau;
      }
      return null;
    }
    let ch;
    try {
      ch = load_chuong(so_chuong);
    } catch (e) {
      return null;
    }
    const bang = ch.doan_dau_theo_nhom || {};
    if (nhom in bang) return bang[nhom];
    if ("chung" in bang) return bang.chung;
    const theo_id = new Set((ch.doan || []).map((d) => d.id));
    for (const n of load_xuat_than().nhom) {
      if (n.ma === nhom && theo_id.has(n.doan_dau)) return n.doan_dau;
    }
    return ch.doan && ch.doan.length ? ch.doan[0].id : null;
  }

  // Chỉ số khởi đầu dùng chung khi nhóm không khai `chi_so_dau` (vd nhóm ẩn).
  const CHI_SO_DAU_MAC_DINH = {
    bac: 3,
    tu_vi: { hien: 12, max: 100 },
    chi_so: {
      sinh_luc: { hien: 30, max: 30 },
      linh_luc: { hien: 10, max: 10 },
      than_niem: 8,
      tan_cong: 5,
      phong_thu: 3,
      chi_mang: 2,
      bao_kich: 150,
      xuyen_giap: 0,
      toc_do: 10,
    },
    ky_nang: ["Hô hấp pháp", "Nhận biết linh khí"],
  };

  const _chep = (o) => JSON.parse(JSON.stringify(o));

  // Chỉ số khởi đầu riêng của từng xuất thân (khai ở `chi_so_dau` trong JSON).
  function chi_so_dau_cua(nhom) {
    const n = load_xuat_than().nhom.find((x) => x.ma === nhom);
    return (n && n.chi_so_dau) || CHI_SO_DAU_MAC_DINH;
  }

  function trang_thai_moi(ten_nhan_vat, xuat_than, nhom) {
    ten_nhan_vat = ten_nhan_vat || "";
    xuat_than = xuat_than || "";
    nhom = nhom || "";
    if (!xuat_than.trim()) xuat_than = "tán tu vô danh";
    const hop_le = new Set(ds_xuat_than().map((n) => n.ma));
    if (!hop_le.has(nhom)) nhom = nhan_dien_xuat_than(xuat_than);
    const dau = chi_so_dau_cua(nhom);
    return {
      ten_nhan_vat: ten_nhan_vat.trim() || "Vô Danh",
      xuat_than: xuat_than.trim(),
      nhom_xuat_than: nhom,
      canh_gioi: CANH_GIOI[0],
      tu_vi: _chep(dau.tu_vi),
      chi_so: Object.assign(_chep(dau.chi_so), {
        tan_cong_phep: _zero_he(),
        khang_phep: _zero_he(),
      }),
      bac: dau.bac,
      tui_do: [
        { ten: "Bạc vụn", so: dau.bac, mo_ta: "Tiền tệ nơi phàm trần." },
      ],
      ky_nang: dau.ky_nang.slice(),
      co_su_kien: [],
      npc: {},
      nhat_ky: [],
      tu_luyen: tl_moi(),
      trong_dong: false,
      chuong: 1,
      doan_hien_tai: null,
      da_qua: [],
      ket_thuc: false,
      tao_luc: _now(),
    };
  }

  // ---------------------------------------------------------------- nạp chương
  function load_chuong(so) {
    if (!_chuong[so]) throw new Error("Chưa nạp chương " + so);
    return _chuong[so];
  }

  // Chương đã nạp trong trình duyệt chưa (bản Pages nạp lười chương 2 trở đi).
  function co_chuong(so) {
    return !!_chuong[so];
  }

  function kiem_chuong(data) {
    const loi = [];
    const ids = (data.doan || []).map((d) => d.id);
    const co = new Set(ids);
    const trung = [...new Set(ids.filter((i, k) => ids.indexOf(i) !== k))];
    if (trung.length) loi.push(`mã đoạn trùng: ${trung.join(", ")}`);
    for (const d of data.doan || []) {
      for (const lc of d.lua_chon || []) {
        if (lc.den !== "__ket_thuc__" && !co.has(lc.den)) {
          loi.push(`${d.id} → '${lc.den}' không có đoạn này`);
        }
      }
    }
    for (const [nhom, did] of Object.entries(data.doan_dau_theo_nhom || {})) {
      if (!co.has(did)) loi.push(`doan_dau_theo_nhom[${nhom}] → '${did}' không có đoạn này`);
    }
    return loi;
  }

  function _doan(state) {
    const ch = load_chuong(state.chuong);
    let did = state.doan_hien_tai;
    if (did === null || did === undefined) {
      const nhom = state.nhom_xuat_than || "tan_tu";
      did = doan_dau_cua(nhom, state.chuong) || ch.doan[0].id;
      if (!ch._theo_id[did]) {
        // Đoán bừa sẽ ném người chơi về đoạn 1 mà không ai biết vì sao.
        throw new Error(
          `Chương ${state.chuong} không có đoạn mở đầu '${did}' cho nhóm '${nhom}' ` +
          `— kiểm doan_dau_theo_nhom trong chuong${state.chuong}.json`
        );
      }
      state.doan_hien_tai = did;
    }
    if (!ch._theo_id[did]) {
      throw new Error(
        `Chương ${state.chuong} không có đoạn '${did}' — bản lưu trỏ tới đoạn không tồn tại`
      );
    }
    const d = ch._theo_id[did];
    _ap_hieu_ung_vao(state, d);
    return d;
  }

  // Hiệu ứng của chính đoạn, áp đúng một lần khi người chơi bước vào — dùng cho
  // thứ phải có mặt NGAY lúc mở đoạn (bạn đồng hành trong sổ NPC, cờ sự kiện),
  // chứ không đợi bấm lựa chọn đầu tiên.
  function _ap_hieu_ung_vao(state, d) {
    const hu = d.hieu_ung_vao;
    if (!hu) return;
    if (!state.da_ap_vao) state.da_ap_vao = [];
    if (state.da_ap_vao.includes(d.id)) return;
    state.da_ap_vao.push(d.id);
    _ap_hieu_ung(state, hu);
  }

  // ---------------------------------------------------------------- tiện ích
  function _dieu_kien_hop(state, dk) {
    if (!dk) return true;
    if ("nhom" in dk) {
      let ds = dk.nhom;
      if (typeof ds === "string") ds = [ds];
      if (!ds.includes(state.nhom_xuat_than || "")) return false;
    }
    const tien = dk.bac !== undefined ? dk.bac : dk.linh_thach;
    if (tien !== undefined && tien !== null && state.bac < tien) return false;
    if ("co_su_kien" in dk) {
      if (!dk.co_su_kien.every((f) => state.co_su_kien.includes(f))) return false;
    }
    if ("co_vat" in dk) {
      const co = new Set(state.tui_do.filter((v) => (v.so || 0) > 0).map((v) => v.ten));
      if (!co.has(dk.co_vat)) return false;
    }
    if ("hao_cam" in dk) {
      for (const [ten, toi_thieu] of Object.entries(dk.hao_cam)) {
        const hc = (state.npc[ten] || {}).hao_cam || 0;
        if (hc < toi_thieu) return false;
      }
    }
    if ("hao_cam_max" in dk) {
      for (const [ten, toi_da] of Object.entries(dk.hao_cam_max)) {
        const hc = (state.npc[ten] || {}).hao_cam || 0;
        if (hc > toi_da) return false;
      }
    }
    if ("canh_gioi" in dk) {
      // Cổng boss: so theo bậc trong CANH_GIOI, không so chuỗi.
      const can = dk.canh_gioi;
      if (!CANH_GIOI.includes(state.canh_gioi) || !CANH_GIOI.includes(can)) return false;
      if (CANH_GIOI.indexOf(state.canh_gioi) < CANH_GIOI.indexOf(can)) return false;
    }
    if ("tin" in dk) {
      if (!_tl(state).tin_da_biet.includes(dk.tin)) return false;
    }
    if ("co_tin" in dk) {
      const da = _tl(state).tin_da_biet;
      if (!dk.co_tin.every((t) => da.includes(t))) return false;
    }
    return true;
  }

  function _gap_npc(state, ten, info) {
    const moi = !(ten in state.npc);
    if (moi) state.npc[ten] = { hao_cam: 0, thai_do: "người dưng" };
    if (info) {
      for (const [k, v] of Object.entries(info)) {
        if (k === "hao_cam") {
          if (moi) state.npc[ten].hao_cam = Math.max(-100, Math.min(100, v));
        } else {
          state.npc[ten][k] = v;
        }
      }
    }
    state.npc[ten].thai_do = muc_hao_cam(state.npc[ten].hao_cam);
  }

  function _doi_hao_cam(state, ten, delta) {
    if (!(ten in state.npc)) state.npc[ten] = { hao_cam: 0, thai_do: "người dưng" };
    const cu = state.npc[ten].hao_cam;
    const moi = Math.max(-100, Math.min(100, cu + delta));
    state.npc[ten].hao_cam = moi;
    state.npc[ten].thai_do = muc_hao_cam(moi);
    const dau = delta > 0 ? "+" : "";
    return `Hảo cảm ${ten} ${dau}${delta} (${muc_hao_cam(moi)})`;
  }

  function _ap_hieu_ung(state, hu) {
    if (!hu) return [];
    const tb = [];
    const tien = hu.bac !== undefined ? hu.bac : hu.linh_thach;
    if (tien !== undefined && tien !== null) {
      state.bac = Math.max(0, state.bac + tien);
      tb.push(`Bạc ${tien > 0 ? "+" : ""}${tien}`);
    }
    if ("tu_vi" in hu) {
      const tv = state.tu_vi;
      tv.hien = Math.min(tv.max, tv.hien + hu.tu_vi);
      tb.push(`Tu vi +${hu.tu_vi}`);
      _thang_cap(state, tb);
    }
    if ("sinh_luc" in hu) {
      const sl = state.chi_so.sinh_luc;
      sl.hien = Math.max(0, Math.min(sl.max, sl.hien + hu.sinh_luc));
      tb.push(`Sinh lực ${hu.sinh_luc > 0 ? "+" : ""}${hu.sinh_luc}`);
    }
    if ("than_niem" in hu) {
      state.chi_so.than_niem = Math.max(0, state.chi_so.than_niem + hu.than_niem);
      tb.push(`Thần niệm ${hu.than_niem > 0 ? "+" : ""}${hu.than_niem}`);
    }
    if ("co_su_kien" in hu) {
      for (const f of hu.co_su_kien) {
        if (!state.co_su_kien.includes(f)) state.co_su_kien.push(f);
      }
    }
    if ("gap_npc" in hu) {
      for (const [ten, info] of Object.entries(hu.gap_npc)) {
        _gap_npc(state, ten, info);
        tb.push(`Gặp: ${ten}`);
      }
    }
    if ("hao_cam" in hu) {
      for (const [ten, delta] of Object.entries(hu.hao_cam)) {
        tb.push(_doi_hao_cam(state, ten, delta));
      }
    }
    if ("them_vat" in hu) {
      // Gộp theo tên + trạng thái: hai lần nhận cùng món là một dòng "×2", không
      // phải hai dòng trùng tên trong túi.
      for (const v of hu.them_vat) {
        if (!v || typeof v !== "object" || !(v.ten || "").trim()) continue;
        const cu = state.tui_do.find((x) => x.ten === v.ten && x.trang_thai === v.trang_thai);
        if (cu) { cu.so = (cu.so || 0) + (v.so || 1); }
        else { const moi = _saoChepSau(v); if (moi.so === undefined) moi.so = 1; state.tui_do.push(moi); }
        tb.push(`Nhận: ${v.ten}`);
      }
    }
    if ("doi_trang_thai" in hu) {
      for (const [ten, ttMoi] of Object.entries(hu.doi_trang_thai)) {
        const v = state.tui_do.find((x) => x.ten === ten);
        if (v) {
          v.trang_thai = ttMoi;
          tb.push(`${ten}: ${ttMoi}`);
        }
      }
    }
    if ("ky_nang" in hu) {
      for (const k of hu.ky_nang) {
        if (!state.ky_nang.includes(k)) {
          state.ky_nang.push(k);
          tb.push(`Học được: ${k}`);
        }
      }
    }
    return tb;
  }

  function _thang_cap(state, tb) {
    const tv = state.tu_vi;
    const tran = TRAN_CANH_GIOI[state.chuong];
    while (tv.hien >= tv.max) {
      const idx = CANH_GIOI.indexOf(state.canh_gioi);
      if (idx + 1 >= CANH_GIOI.length) break;
      if (tran && idx + 1 >= CANH_GIOI.indexOf(tran) + 1) {
        // Chạm trần: giữ tu vi đầy, không lên tầng, báo để người chơi biết vì sao.
        tv.hien = tv.max;
        if (!tb.some((t) => t.includes("chạm trần"))) {
          tb.push(`⚠ Đã chạm trần chương này (${tran}) — cần cơ duyên mới vượt được`);
        }
        break;
      }
      state.canh_gioi = CANH_GIOI[idx + 1];
      tv.hien = 0;
      tv.max = Math.trunc(tv.max * 1.35);
      const cs = state.chi_so;
      cs.sinh_luc.max += 6;
      cs.sinh_luc.hien = cs.sinh_luc.max;
      cs.linh_luc.max += 4;
      cs.linh_luc.hien = cs.linh_luc.max;
      cs.than_niem += 4;
      cs.tan_cong += 2;
      cs.phong_thu += 1;
      tb.push(`⚡ ĐỘT PHÁ: ${state.canh_gioi}!`);
    }
  }

  // ---------------------------------------------------------------- API chính
  function bat_dau(state) {
    return _goi_y(state);
  }

  // Chọn biến thể đoạn kể theo mức hảo cảm. Khớp đúng thì thắng; không có khớp
  // đúng thì lấy bậc thấp hơn gần nhất, nhờ vậy một đoạn chỉ cần vài biến thể.
  function _ke_theo_hao_cam(d, state) {
    const bts = d.bien_the || [];
    if (!bts.length) return d.ke || "";
    const thu_tu = MUC_HAO_CAM.map((m) => m[2]);
    let tot_nhat = null;
    let hang_tot_nhat = -99;
    for (const bt of bts) {
      const npc = bt.npc;
      if (npc && !(npc in state.npc)) continue;
      if (!thu_tu.includes(bt.muc)) continue;
      const diem = npc ? (state.npc[npc] || {}).hao_cam || 0 : 0;
      const muc_hien = muc_hao_cam(diem);
      const hang = thu_tu.indexOf(bt.muc);
      if (hang <= thu_tu.indexOf(muc_hien) && hang > hang_tot_nhat) {
        hang_tot_nhat = hang;
        tot_nhat = bt;
      }
    }
    if (!tot_nhat) {
      // NPC không có mặt trong cảnh (chưa từng gặp) thì dùng văn bản gốc; chỉ khi
      // NPC CÓ mặt mà hảo cảm còn thấp hơn biến thể thấp nhất mới lấy biến thể
      // thấp nhất.
      const thu = bts.filter((bt) => (!bt.npc || bt.npc in state.npc)
                                   && thu_tu.includes(bt.muc));
      if (thu.length) {
        tot_nhat = thu.reduce((a, b) =>
          thu_tu.indexOf(a.muc) <= thu_tu.indexOf(b.muc) ? a : b);
      }
    }
    return tot_nhat ? tot_nhat.ke : d.ke || "";
  }

  function _man_ket_chuong(state) {
    // Lời kết nằm trong chính file chương (`ket`), không viết cứng ở đây — nếu không,
    // sang chương 2 sẽ vẫn hiện lời kết của chương 1.
    const ch = load_chuong(state.chuong);
    const ket = ch.ket || {};
    const sau = ket.chuong_sau || state.chuong + 1;
    return {
      doan_id: "__ket_thuc__",
      hoi: "Kết",
      boi_canh: ket.boi_canh || `Chương ${state.chuong} — hết`,
      chuong: state.chuong,
      ten_chuong: ch.ten,
      ke: ket.ke || `Chương ${state.chuong} khép lại.`,
      hinh_anh: ket.hinh_anh || null,
      video: null,
      lua_chon: [],
      cho_phep_tu_do: false,
      ket_thuc: true,
      chuong_sau: sau,
      chuong_sau_mo: co_chuong(sau),
      thong_bao: [],
      trang_thai: _trang_thai_gon(state),
    };
  }

  function sang_chuong(state, so) {
    // Mang nguyên nhân vật sang chương sau: chỉ đổi `chuong` + `doan_hien_tai`.
    // Cảnh giới, bạc, túi đồ, hảo cảm, cờ sự kiện giữ nguyên.
    if (so === undefined || so === null) {
      so = (load_chuong(state.chuong).ket || {}).chuong_sau || state.chuong + 1;
    }
    if (!co_chuong(so)) return { loi: `Chương ${so} chưa mở` };
    state.chuong = so;
    state.doan_hien_tai = null;
    state.ket_thuc = false;
    // Mỗi chương một ngân sách ngày riêng. Giữ `ngay_da_dung` để dãy ngẫu nhiên
    // không lặp lại y nguyên ở chương sau; tin đã biết cũng mang theo.
    const tl = _tl(state);
    tl.ngay_con = NGAY_MOI_CHUONG;
    tl.nhat_ky.push(`— Chương ${so}: ngày mới, ${NGAY_MOI_CHUONG} ngày —`);
    _ghi_nhat_ky(state, `Sang chương ${so}`);
    const kq = _goi_y(state);
    kq.thong_bao = [`— Chương ${so}: ${load_chuong(so).ten} —`];
    return kq;
  }

  // NPC của đoạn kèm mức hảo cảm hiện tại. Nguồn: `npc` khai báo ở đoạn, cộng mọi
  // NPC mà `bien_the` nhắm tới — đoạn có biến thể giọng mà quên khai `npc` vẫn phải
  // báo đúng thái độ cho AI kể.
  function _npc_trong_canh(d, state) {
    const ten = [];
    (d.npc || []).forEach((t) => { if (!ten.includes(t)) ten.push(t); });
    (d.bien_the || []).forEach((bt) => {
      if (bt.npc && !ten.includes(bt.npc)) ten.push(bt.npc);
    });
    const ra = [];
    for (const t of ten) {
      const info = state.npc[t];
      // Chưa gặp thì chưa có thái độ — đừng bịa mức "người dưng".
      if (!info) continue;
      ra.push({
        ten: t,
        hao_cam: info.hao_cam || 0,
        thai_do: info.thai_do || muc_hao_cam(info.hao_cam || 0),
      });
    }
    return ra;
  }

  function _doan_thua(state) {
    // Đoạn kết thua là đoạn có `ket_thuc: true` + `thua: true` nằm trong chương,
    // khác màn khép chương. Trả null khi đang ở màn khép chương bình thường.
    if (!state.ket_thuc) return null;
    const ch = load_chuong(state.chuong);
    const d = ch._theo_id ? ch._theo_id[state.doan_hien_tai] : null;
    return d && d.ket_thuc && d.thua ? d : null;
  }

  function _man_ket_thua(state, d) {
    // Không có nút sang chương: người chơi lùi lại đánh khác, hoặc chơi lại từ đầu.
    return {
      doan_id: d.id,
      hoi: d.hoi || "Kết",
      boi_canh: d.boi_canh,
      chuong: state.chuong,
      ten_chuong: load_chuong(state.chuong).ten,
      ke: d.ke || "",
      hinh_anh: d.hinh_anh || null,
      video: d.video || null,
      lua_chon: [],
      cho_phep_tu_do: false,
      ket_thuc: true,
      thua: true,
      chuong_sau: null,
      chuong_sau_mo: false,
      thong_bao: [],
      trang_thai: _trang_thai_gon(state),
    };
  }

  function _goi_y(state) {
    if (state.ket_thuc) {
      const dThua = _doan_thua(state);
      if (dThua) return _man_ket_thua(state, dThua);
      return _man_ket_chuong(state);
    }
    const d = _doan(state);
    if (d.thua && d.ket_thuc) {
      // Đặt cờ để bản lưu và payload khớp nhau; `_doan_thua` dựa vào cờ này.
      state.ket_thuc = true;
      return _man_ket_thua(state, d);
    }

    const lua_chon = [];
    (d.lua_chon || []).forEach((lc, i) => {
      const hop = _dieu_kien_hop(state, lc.dieu_kien);
      lua_chon.push({
        chi_so: i,
        chu: lc.chu,
        khoa: !hop,
        ly_do_khoa: !hop ? lc.ly_do_khoa || "Chưa đủ điều kiện" : null,
      });
    });
    return {
      doan_id: d.id,
      hoi: d.hoi,
      boi_canh: d.boi_canh,
      chuong: state.chuong,
      ten_chuong: load_chuong(state.chuong).ten,
      ke: _ke_theo_hao_cam(d, state),
      npc_trong_canh: _npc_trong_canh(d, state),
      hinh_anh: d.hinh_anh,
      video: d.video,
      lua_chon: lua_chon,
      cho_phep_tu_do: d.cho_phep_tu_do !== undefined ? d.cho_phep_tu_do : true,
      ket_thuc: d.ket_thuc || false,
      thong_bao: [],
      trang_thai: _trang_thai_gon(state),
    };
  }

  function goi_y_hien_tai(state) {
    return _goi_y(state);
  }

  function _trang_thai_gon(state) {
    const cs = state.chi_so;
    return {
      ten_nhan_vat: state.ten_nhan_vat,
      xuat_than: state.xuat_than,
      nhom_xuat_than: state.nhom_xuat_than || "",
      canh_gioi: state.canh_gioi,
      tu_vi: Object.assign({}, state.tu_vi),
      sinh_luc: Object.assign({}, cs.sinh_luc),
      linh_luc: Object.assign({}, cs.linh_luc),
      than_niem: cs.than_niem,
      tan_cong: cs.tan_cong,
      phong_thu: cs.phong_thu,
      toc_do: cs.toc_do,
      bac: state.bac,
      linh_thach: state.bac,
      tui_do: state.tui_do.map((v) => Object.assign({}, v)),
      ky_nang: state.ky_nang.slice(),
      npc: Object.fromEntries(Object.entries(state.npc).map(([k, v]) => [k, Object.assign({}, v)])),
      co_su_kien: state.co_su_kien.slice(),
      chuong: state.chuong,
    };
  }

  function chon(state, chi_so) {
    if (state.ket_thuc) return _goi_y(state);
    chi_so = parseInt(chi_so, 10);
    if (Number.isNaN(chi_so)) return { loi: "Lựa chọn không hợp lệ" };
    const d = _doan(state);
    const lcs = d.lua_chon || [];
    if (!(chi_so >= 0 && chi_so < lcs.length)) return { loi: "Lựa chọn không hợp lệ" };
    const lc = lcs[chi_so];
    if (!_dieu_kien_hop(state, lc.dieu_kien)) {
      return { loi: lc.ly_do_khoa || "Chưa đủ điều kiện" };
    }
    const tb = _ap_hieu_ung(state, lc.hieu_ung);
    _ghi_nhat_ky(state, `Chọn: ${lc.chu}`);
    _chuyen_doan(state, lc.den);
    const ket_qua = _goi_y(state);
    ket_qua.thong_bao = tb;
    return ket_qua;
  }

  function _boi_canh(state) {
    if (state.ket_thuc) return "Chương đã khép lại.";
    const d = _doan(state);
    const npc = Object.entries(state.npc)
      .map(([ten, v]) => `${ten} (hảo cảm ${v.hao_cam})`)
      .join(", ");
    return (
      `Xuất thân người chơi: ${state.xuat_than || ""}. ` +
      `Đoạn: ${d.boi_canh || ""}. Cảnh giới: ${state.canh_gioi}. ` +
      `Sinh lực ${state.chi_so.sinh_luc.hien}/${state.chi_so.sinh_luc.max}. ` +
      `NPC đã gặp: ${npc || "chưa gặp ai"}.`
    );
  }

  function _so_nguyen(v) {
    if (typeof v === "boolean" || typeof v !== "number" || !Number.isFinite(v)) return null;
    return Math.trunc(v);
  }

  function _loc_y_dinh(state, y) {
    const hu = {};
    for (const [khoa, [lo, hi]] of [
      ["sinh_luc", [-15, 10]], ["tu_vi", [0, 8]], ["bac", [-10, 10]], ["than_niem", [0, 2]],
    ]) {
      const n = _so_nguyen(y[khoa]);
      if (n !== null) hu[khoa] = Math.max(lo, Math.min(hi, n));
    }
    const hc = {};
    let hc_in = y.hao_cam;
    if (typeof hc_in !== "object" || hc_in === null || Array.isArray(hc_in)) hc_in = {};
    for (const [ten, delta] of Object.entries(hc_in)) {
      const n = _so_nguyen(delta);
      if (n !== null && ten in state.npc) hc[ten] = Math.max(-10, Math.min(10, n));
    }
    if (Object.keys(hc).length) hu.hao_cam = hc;
    return hu;
  }

  async function hanh_dong_tu_do(state, van_ban, AI) {
    van_ban = typeof van_ban === "string" ? van_ban.trim() : "";
    if (!van_ban) return { loi: "Hãy nhập hành động" };
    if (state.ket_thuc) return { loi: "Chương đã khép lại" };
    const d = _doan(state);
    _ghi_nhat_ky(state, `Tự do: ${van_ban}`);
    const hien_thi = van_ban.toLowerCase().startsWith("ta ") ? van_ban.slice(3) : van_ban;
    const tb = [`(tự do) Ta ${hien_thi}…`];
    let y_dinh = {};
    if (AI) {
      try {
        if (AI.san_sang()) y_dinh = await AI.nhan_dien(van_ban, _boi_canh(state));
      } catch (e) {
        y_dinh = {};
      }
    }
    if (typeof y_dinh !== "object" || y_dinh === null) y_dinh = {};
    const hu = _loc_y_dinh(state, y_dinh);
    if (Object.keys(hu).length) tb.push(..._ap_hieu_ung(state, hu));
    if (y_dinh.nhan_xet) tb.push(`⟡ ${y_dinh.nhan_xet}`);

    const ket_qua = _goi_y(state);
    ket_qua.thong_bao = tb;
    if (AI) {
      try {
        if (AI.san_sang()) {
          const thay_doi = tb.slice(1).join("; ") || "không đổi chỉ số";
          const ke_moi = await AI.ke_lai(d.ke || "", van_ban, thay_doi);
          if (ke_moi) {
            ket_qua.ke = ke_moi;
            tb.push("AI kể: kết quả có thể khác mỗi lần");
            return ket_qua;
          }
        }
      } catch (e) {
        /* AI lỗi → rơi về chế độ viết sẵn */
      }
    }
    ket_qua.ke =
      `Ta ${van_ban}. Chưa có gì đổi khác rõ rệt, nhưng ta cảm thấy ` +
      `thời cơ đang tới gần.\n\n` + (d.ke || "");
    return ket_qua;
  }

  function _chuyen_doan(state, den) {
    if (!state.da_qua.includes(state.doan_hien_tai)) state.da_qua.push(state.doan_hien_tai);
    state.doan_hien_tai = den;
    const ch = load_chuong(state.chuong);
    if (!ch._theo_id[den]) state.ket_thuc = true;
  }

  function _ghi_nhat_ky(state, viec) {
    state.nhat_ky.push({ luc: _now(), viec: viec });
    if (state.nhat_ky.length > 60) state.nhat_ky = state.nhat_ky.slice(-60);
  }

  // ---------------------------------------------------------------- lưu / nạp
  function _safe_name(ten) {
    const s = String(ten || "").replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 40);
    return s || "khach";
  }

  function luu(state, slot) {
    const key = KHOA_LUU + _safe_name(slot);
    goc.localStorage.setItem(key, JSON.stringify(state));
    return key;
  }

  function nap(slot) {
    const key = KHOA_LUU + _safe_name(slot);
    const raw = goc.localStorage.getItem(key);
    if (raw === null) return null;
    const state = JSON.parse(raw);
    if (!("bac" in state)) {
      state.bac = state.linh_thach !== undefined ? state.linh_thach : 0;
      delete state.linh_thach;
    }
    return state;
  }

  function ds_luu() {
    const ds = [];
    for (let i = 0; i < goc.localStorage.length; i++) {
      const k = goc.localStorage.key(i);
      if (k && k.startsWith(KHOA_LUU)) ds.push(k.slice(KHOA_LUU.length));
    }
    return ds;
  }

  function xoa_luu(slot) {
    goc.localStorage.removeItem(KHOA_LUU + _safe_name(slot));
  }

  function tom_tat(state) {
    if (state.ket_thuc) return `Chương ${state.chuong} đã khép lại.`;
    const d = _doan(state);
    const npcs = Object.entries(state.npc)
      .map(([ten, v]) => `${ten} (${v.hao_cam >= 0 ? "+" : ""}${v.hao_cam || 0})`)
      .join(", ") || "chưa gặp ai";
    return (
      `Chương ${state.chuong}: ${load_chuong(state.chuong).ten}. ` +
      `Đoạn ${d.id} (${d.boi_canh}). ` +
      `Cảnh giới ${state.canh_gioi}, bạc ${state.bac}. ` +
      `Nhân vật đã gặp: ${npcs}. ` +
      `Sự kiện: ${state.co_su_kien.join(", ") || "chưa có"}.`
    );
  }

  const Engine = {
    HE_PHAP, CANH_GIOI, MUC_HAO_CAM,
    muc_hao_cam, _zero_he,
    napXuatThan, napChuong,
    load_xuat_than, ds_xuat_than, nhan_dien_xuat_than, doan_dau_cua, chi_so_dau_cua,
    trang_thai_moi, load_chuong,
    bat_dau, goi_y_hien_tai, chon, sang_chuong, hanh_dong_tu_do,
    tl_moi, tl_trang_thai, tl_da_toa, tl_san, tl_dau, tl_danh, tl_cong_thuc,
    tl_luyen_dan, tl_cho, tl_mua, tl_do_la, tl_nghi, vao_dong, ra_dong,
    TL_VIEC, TL_YEU_THU, TL_CONG_THUC, TL_TIN, TL_CHO_HANG, TRAN_CANH_GIOI,
    NGAY_MOI_CHUONG, _hat_giong, _ngau_nhien,
    co_chuong, kiem_chuong,
    luu, nap, ds_luu, xoa_luu, tom_tat,
    _khong_dau, _trang_thai_gon, _boi_canh, _thang_cap, _dieu_kien_hop,
  };

  goc.Engine = Engine;
  if (typeof module !== "undefined" && module.exports) module.exports = Engine;
})(typeof globalThis !== "undefined" ? globalThis : this);
