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

  function doan_dau_cua(nhom) {
    for (const n of load_xuat_than().nhom) {
      if (n.ma === nhom) return n.doan_dau;
    }
    return null;
  }

  function trang_thai_moi(ten_nhan_vat, xuat_than, nhom) {
    ten_nhan_vat = ten_nhan_vat || "";
    xuat_than = xuat_than || "";
    nhom = nhom || "";
    if (!xuat_than.trim()) xuat_than = "tán tu vô danh";
    const hop_le = new Set(ds_xuat_than().map((n) => n.ma));
    if (!hop_le.has(nhom)) nhom = nhan_dien_xuat_than(xuat_than);
    return {
      ten_nhan_vat: ten_nhan_vat.trim() || "Vô Danh",
      xuat_than: xuat_than.trim(),
      nhom_xuat_than: nhom,
      canh_gioi: CANH_GIOI[0],
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
        tan_cong_phep: _zero_he(),
        khang_phep: _zero_he(),
      },
      bac: 3,
      tui_do: [
        { ten: "Bạc vụn", so: 3, mo_ta: "Tiền tệ nơi phàm trần." },
      ],
      ky_nang: ["Hô hấp pháp", "Nhận biết linh khí"],
      co_su_kien: [],
      npc: {},
      nhat_ky: [],
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

  function _doan(state) {
    const ch = load_chuong(state.chuong);
    let did = state.doan_hien_tai;
    if (did === null || did === undefined) {
      did = doan_dau_cua(state.nhom_xuat_than || "tan_tu") || ch.doan[0].id;
      if (!ch._theo_id[did]) did = ch.doan[0].id;
      state.doan_hien_tai = did;
    }
    return ch._theo_id[did];
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
      for (const v of hu.them_vat) {
        state.tui_do.push(_saoChepSau(v));
        tb.push(`Nhận: ${v.ten}`);
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
    while (tv.hien >= tv.max) {
      const idx = CANH_GIOI.indexOf(state.canh_gioi);
      if (idx + 1 >= CANH_GIOI.length) break;
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

  function _ke_theo_hao_cam(d, state) {
    const bts = d.bien_the || [];
    if (!bts.length) return d.ke || "";
    const thu_tu = MUC_HAO_CAM.map((m) => m[2]);
    let tot_nhat = null;
    let hang_tot_nhat = -1;
    for (const bt of bts) {
      const npc = bt.npc;
      if (npc && !(npc in state.npc)) continue;
      const diem = npc ? (state.npc[npc] || {}).hao_cam || 0 : 0;
      const muc_hien = muc_hao_cam(diem);
      if (bt.muc !== muc_hien) continue;
      const hang = thu_tu.includes(muc_hien) ? thu_tu.indexOf(muc_hien) : 0;
      if (hang > hang_tot_nhat) {
        hang_tot_nhat = hang;
        tot_nhat = bt;
      }
    }
    return tot_nhat ? tot_nhat.ke : d.ke || "";
  }

  function _man_ket_chuong(state) {
    return {
      doan_id: "__ket_thuc__",
      hoi: "Kết",
      boi_canh: "Chương 1 — hết",
      chuong: state.chuong,
      ten_chuong: load_chuong(state.chuong).ten,
      ke:
        "Chương một khép lại. Dã Lang Bang rút lui, Thất Huyền Môn còn đứng đó, " +
        "dẫu tan hoang.\n\nTa đứng giữa buổi bình minh, biết rằng con đường phía trước " +
        "còn dài hơn cả những gì ta tưởng.\n\n*Chương sau: Huyết Sát Thí Luyện.*",
      hinh_anh: { tags: ["bình minh", "kết chương", "núi"] },
      video: null,
      lua_chon: [],
      cho_phep_tu_do: false,
      ket_thuc: true,
      thong_bao: [],
      trang_thai: _trang_thai_gon(state),
    };
  }

  function _goi_y(state) {
    if (state.ket_thuc) return _man_ket_chuong(state);
    const d = _doan(state);
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
    load_xuat_than, ds_xuat_than, nhan_dien_xuat_than, doan_dau_cua,
    trang_thai_moi, load_chuong,
    bat_dau, goi_y_hien_tai, chon, hanh_dong_tu_do,
    luu, nap, ds_luu, xoa_luu, tom_tat,
    _khong_dau, _trang_thai_gon, _boi_canh,
  };

  goc.Engine = Engine;
  if (typeof module !== "undefined" && module.exports) module.exports = Engine;
})(typeof globalThis !== "undefined" ? globalThis : this);
