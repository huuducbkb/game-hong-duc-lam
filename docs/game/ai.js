/* Gọi Gemini từ trình duyệt — bản JavaScript của game/ai.py.
 *
 * KHÁC bản Python ở một điểm: key KHÔNG nằm trên máy chủ, mà do NGƯỜI CHƠI
 * tự nhập và lưu trong localStorage của chính họ (xem docs/game/play.html).
 * Nhờ vậy key của bạn không bao giờ nằm trong code công khai.
 *
 * Nguyên tắc:
 *   - Chưa có key, hoặc key hỏng → `san_sang()` trả false.
 *   - Kết quả thử được NHỚ trong RAM (không gọi lại mỗi lượt).
 *   - Mọi lỗi mạng/API đều bị nuốt, coi như AI không sẵn sàng (game vẫn chạy).
 */
(function (goc) {
  "use strict";

  const KHOA_KEY = "hdttl_gemini_key";
  const TIMEOUT = 12000;

  const MODEL_DU_PHONG = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
  ];

  // ------------------------------------------------------------ key của người chơi
  function lay_key() {
    try {
      return (goc.localStorage.getItem(KHOA_KEY) || "").trim();
    } catch (e) {
      return "";
    }
  }

  function dat_key(key) {
    try {
      goc.localStorage.setItem(KHOA_KEY, (key || "").trim());
    } catch (e) {
      /* Safari riêng tư có thể chặn localStorage */
    }
    _trang_thai = { da_thu: false, ok: false, ly_do: "" };
  }

  function co_key() {
    return lay_key().length > 0;
  }

  let _trang_thai = { da_thu: false, ok: false, ly_do: "" };

  // ------------------------------------------------------------ gọi Gemini
  async function _goi_gemini(prompt, max_token) {
    max_token = max_token || 400;
    const key = lay_key();
    if (!key) throw new Error("Thiếu key Gemini");
    let loi_cuoi = null;
    for (const model of MODEL_DU_PHONG) {
      const url =
        "https://generativelanguage.googleapis.com/v1beta/models/" +
        model + ":generateContent?key=" + encodeURIComponent(key);
      const body = JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: Math.max(max_token, 256), temperature: 0.9 },
      });
      const ctl = new AbortController();
      const hen = setTimeout(() => ctl.abort(), TIMEOUT);
      try {
        const r = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: body,
          signal: ctl.signal,
        });
        clearTimeout(hen);
        if (r.status === 400 || r.status === 401 || r.status === 403) {
          const t = await r.text();
          throw new Error(`Key bị từ chối (HTTP ${r.status}): ${t.slice(0, 160)}`);
        }
        if (!r.ok) {
          loi_cuoi = `${model}: HTTP ${r.status}`;
          continue;
        }
        const data = await r.json();
        const cand = (data.candidates || [{}])[0];
        const parts = (cand.content || {}).parts || [];
        const txt = parts.map((p) => p.text || "").join("").trim();
        if (txt) return txt;
        loi_cuoi = `${model}: không có nội dung trả về`;
      } catch (e) {
        clearTimeout(hen);
        if (e && e.message && e.message.startsWith("Key bị từ chối")) throw e;
        loi_cuoi = `${model}: ${(e && e.name) || "lỗi"}`;
      }
    }
    throw new Error(loi_cuoi || "Không gọi được model nào");
  }

  async function thu_ket_noi(force) {
    if (_trang_thai.da_thu && !force) return _trang_thai;
    if (!co_key()) {
      _trang_thai = { da_thu: true, ok: false, ly_do: "Chưa nhập key Gemini" };
      return _trang_thai;
    }
    try {
      const txt = await _goi_gemini("Trả lời đúng một chữ: OK", 16);
      _trang_thai = { da_thu: true, ok: !!txt, ly_do: txt ? "" : "Không có phản hồi" };
    } catch (e) {
      _trang_thai = { da_thu: true, ok: false, ly_do: (e && e.message) || "Lỗi không rõ" };
    }
    return _trang_thai;
  }

  function san_sang() {
    return _trang_thai.ok;
  }

  // ------------------------------------------------------------ kể lại đoạn
  const TEN_RIENG = ["Hàn Lập", "Thất Huyền Môn", "Thất Huyền quyền", "Thất Huyền trấn",
    "Dã Lang Bang", "Lý Hổ", "Tần Báo", "Tuyết Cơ", "Mạc Đại Phu",
    "Hùng Bá", "Hợp Hoan Tông", "tân xá", "ngọc cốt", "hậu sơn",
    "hắc quáng động"];

  const _cache_ke = new Map();
  const CACHE_TOI_DA = 500;

  // -------------------------------------------------- chặn AI viết hỏng
  // Model hay "cổ phong hoá" quá tay: ghép chữ Hán nửa vời, dính chữ ("mộtỗ"),
  // sai ngữ pháp, dùng từ sai nghĩa ("mai táng" cho khối ngọc). Truyện gốc
  // sạch nên lấy chính nó làm chuẩn. Ngưỡng đo trên dữ liệu thật:
  // bản gốc 0.0% từ lạ · bản AI hỏng 12–45%.
  const NGUONG_TU_LA = 0.12;
  const NGUONG_PHINH = 1.40;
  const NGUONG_NGAN = 0.70;
  const KY_TU_RAC = "øØæÆðÐþÞß";
  const TU_RAC = [
    "khứu đại", "dị hương", "triệt ngộ", "tùng hình", "nguyệt thăng", "u lan",
    "tịch mịch", "tịch dương", "mai táng", "vị tằng", "phương tri", "hà xứ",
    "nhi lai", "đồng thời khắc", "nhất lũ", "nhất vị", "nhất đạo", "chủng hoa",
    "độc năng", "tị quan", "nhục thân chân thật", "mộc sàng", "bích quang",
    "chân quang", "ôn nhuận", "hữu mạch", "thanh sở", "ma ty", "nguyệt hoa",
    "lăng tại", "chí nghẹn", "thiên niên", "nhu như ti",
  ];

  let _kho_tu = null;
  function _khoTuChuan() {
    if (_kho_tu) return _kho_tu;
    const tu = new Set();
    const g = (typeof globalThis !== "undefined" ? globalThis : this);
    // Truyện nạp bất đồng bộ vào Engine, nên lấy qua load_chuong() khi có.
    let ds = (g.CHUONG_DU_LIEU && g.CHUONG_DU_LIEU.doan) || [];
    if (!ds.length && g.Engine && g.Engine.load_chuong) {
      try { ds = g.Engine.load_chuong(1).doan || []; } catch (e) { ds = []; }
    }
    for (const d of ds) {
      for (const truong of ["ke", "boi_canh"]) {
        for (const w of String(d[truong] || "").toLowerCase().match(/[^\W\d_]+/gu) || []) {
          tu.add(w);
        }
      }
    }
    if (tu.size) _kho_tu = tu;
    return tu;
  }

  function _tyLeTuLa(v) {
    const tu = String(v || "").toLowerCase().match(/[^\W\d_]+/gu) || [];
    if (!tu.length) return 0;
    const chuan = _khoTuChuan();
    if (!chuan.size) return 0;
    let la = 0;
    for (const w of tu) if (!chuan.has(w)) la++;
    return la / tu.length;
  }

  function _coChuDinh(v) {
    const chuan = _khoTuChuan();
    const m = String(v || "").toLowerCase().match(/[^\W\d_]{2,}ỗ\b/gu) || [];
    return m.some(w => !chuan.has(w));
  }

  function van_ban_dung(ban_ai, ban_goc) {
    if (!ban_ai || !ban_ai.trim()) return [false, "AI trả về rỗng"];
    for (const c of ban_ai) if (KY_TU_RAC.includes(c)) return [false, "có ký tự rác ngoài tiếng Việt"];
    const thap = ban_ai.toLowerCase();
    for (const tu of TU_RAC) {
      if (thap.includes(tu)) return [false, `có từ Hán-Việt rác (${tu})`];
    }
    if (_coChuDinh(ban_ai)) return [false, "có chữ dính nhau (vd 'mộtỗ')"];
    if (!/[.!?…”"*]\s*$/u.test(ban_ai)) return [false, "câu bị cắt giữa chừng"];
    if (_tyLeTuLa(ban_ai) > NGUONG_TU_LA) return [false, `quá nhiều từ lạ (${(_tyLeTuLa(ban_ai) * 100).toFixed(0)}%)`];
    if (ban_goc) {
      const mat = TEN_RIENG.filter(t => ban_goc.includes(t) && !ban_ai.includes(t));
      if (mat.length) return [false, `đổi mất tên riêng (${mat.slice(0, 3).join(", ")})`];
      const dem = s => (s.match(/\n\n/g) || []).length;
      if (dem(ban_goc) && dem(ban_ai) < dem(ban_goc) - 1) {
        return [false, "gộp mất dòng trống giữa các đoạn"];
      }
      const ti = ban_ai.length / Math.max(1, ban_goc.length);
      if (ti > NGUONG_PHINH) return [false, `dài hơn bản gốc ${(ti * 100).toFixed(0)}%`];
      if (ti < NGUONG_NGAN) return [false, `ngắn hơn bản gốc ${(ti * 100).toFixed(0)}%`];
    }
    return [true, ""];
  }

  async function ke_lai(doan_ke, hanh_dong, thay_doi) {
    thay_doi = thay_doi || "";
    const phan_thay_doi = thay_doi
      ? `\nCÁC THAY ĐỔI ĐÃ ÁP DỤNG (phải khớp với truyện): ${thay_doi}`
      : "";
    const prompt =
      "Bạn là người dẫn chuyện tiên hiệp Việt, ngôi thứ nhất 'ta'. " +
      "Viết lại đoạn sau thật sinh động, có nội tâm, 3-5 câu, KHÔNG đổi sự kiện:\n\n" +
      `ĐOẠN GỐC:\n${doan_ke}\n\n` +
      `HÀNH ĐỘNG CỦA NGƯỜI CHƠI: ${hanh_dong}${phan_thay_doi}\n\n` +
      "Dùng tiếng Việt thuần, KHÔNG chêm chữ Hán (dị hương, khứu đại, triệt ngộ…). " +
      "Chỉ trả về đoạn kể, không giải thích.";
    let moi;
    try { moi = (await _goi_gemini(prompt, 500)).trim(); }
    catch (e) { return ""; }
    const [dung] = van_ban_dung(moi, doan_ke);
    return dung ? moi : "";
  }

  async function ke_lai_tien_hiep(doan_ke, boi_canh, hanh_dong) {
    doan_ke = (doan_ke || "").trim();
    if (!doan_ke) return "";
    boi_canh = boi_canh || "";
    hanh_dong = hanh_dong || "";
    const khoa = doan_ke + "\u0000" + hanh_dong;
    if (_cache_ke.has(khoa)) return _cache_ke.get(khoa);

    const ten = TEN_RIENG.join(", ");
    const phan_boi_canh = boi_canh ? `\nBỐI CẢNH: ${boi_canh}` : "";
    const phan_hanh_dong = hanh_dong ? `\nHÀNH ĐỘNG VỪA RỒI CỦA NGƯỜI CHƠI: ${hanh_dong}` : "";
    const prompt =
      "Bạn là người kể chuyện tiếng Việt. Kể lại đoạn dưới bằng TIẾNG VIỆT HIỆN ĐẠI, " +
      "trong sáng, dễ hiểu — vẫn giữ không khí kiếm hiệp.\n\n" +
      "GIỮ NGUYÊN:\n" +
      "- Ngôi thứ nhất 'ta' (KHÔNG đổi thành 'tôi', 'mình').\n" +
      "- Mọi sự việc, nhân vật, địa điểm, thứ tự câu. Không thêm, không bớt.\n" +
      "- Độ dài tương đương bản gốc (không tóm tắt).\n" +
      "- Giữ nguyên tên riêng, thuật ngữ: " + ten + ".\n" +
      "- Nội tâm trong *…*, lời thoại trong “…” như bản gốc.\n" +
      "- Giữ đúng các đoạn: chỗ nào bản gốc có dòng trống thì giữ dòng trống.\n\n" +
      "TUYỆT ĐỐI KHÔNG dùng từ Hán-Việt cổ. Sai: 'tịch mịch', 'dị hương', 'khứu đại', " +
      "'triệt ngộ', 'nguyệt thăng', 'tùng hình', 'u lan', 'mai táng', 'vị tằng', " +
      "'phương tri', 'nhất lũ'. Đúng: 'im lặng', 'mùi lạ', 'mũi', 'hiểu ra', " +
      "'trăng lên', 'theo nàng mà tới', 'chưa từng', 'mới biết', 'một'.\n" +
      "- 'mai táng' chỉ dùng cho chôn người chết. Chôn đồ vật thì dùng 'chôn', 'vùi', 'lấp đất'.\n\n" +
      "Viết trọn câu, kết thúc bằng dấu chấm. Chỉ trả về đoạn kể, không giải thích.\n\n" +
      `ĐOẠN GỐC:\n${doan_ke}${phan_boi_canh}${phan_hanh_dong}`;
    let ket_qua;
    try {
      ket_qua = (await _goi_gemini(prompt, 1600)).trim();
    } catch (e) {
      return "";
    }
    if (!ket_qua) return "";
    const [dung, ly_do] = van_ban_dung(ket_qua, doan_ke);
    if (!dung) {
      if (typeof console !== "undefined") console.warn("Chặn AI kể:", ly_do);
      return "";
    }
    if (_cache_ke.size >= CACHE_TOI_DA) {
      const bo = Array.from(_cache_ke.keys()).slice(0, 100);
      for (const k of bo) _cache_ke.delete(k);
    }
    _cache_ke.set(khoa, ket_qua);
    return ket_qua;
  }

  // ------------------------------------------------------------ nhận diện hành động
  const HANH_DONG_HOP_LE = ["tấn công", "tặng quà", "trò chuyện", "di chuyển",
    "quan sát", "nghỉ", "khác"];

  const GIOI_HAN = {
    sinh_luc: [-15, 10],
    tu_vi: [0, 8],
    bac: [-10, 10],
    than_niem: [0, 2],
    hao_cam: [-10, 10],
  };

  function _tach_json(txt) {
    txt = (txt || "").trim();
    if (txt.startsWith("```")) {
      const phan = txt.split("```");
      txt = phan.length >= 3 ? phan[1] : txt.replace(/`/g, "");
      if (txt.trim().startsWith("json")) txt = txt.trim().slice(4);
    }
    const dau = txt.indexOf("{");
    const cuoi = txt.lastIndexOf("}");
    if (dau < 0 || cuoi < dau) throw new Error("Không thấy JSON");
    return JSON.parse(txt.slice(dau, cuoi + 1));
  }

  function _so_nguyen(v) {
    if (typeof v === "boolean" || typeof v !== "number" || !Number.isFinite(v)) return null;
    return Math.trunc(v);
  }

  async function nhan_dien(van_ban, boi_canh) {
    const prompt =
      "Bạn là bộ máy luật cho game nhập vai tu tiên. Người chơi gõ một hành động tự do.\n" +
      "Nhiệm vụ: phân loại hành động và đề xuất thay đổi chỉ số NHỎ, hợp lý. CHỈ TRẢ JSON.\n\n" +
      `BỐI CẢNH:\n${boi_canh}\n\n` +
      `HÀNH ĐỘNG NGƯỜI CHƠI: ${van_ban}\n\n` +
      "Khuôn JSON (bỏ khoá nào không áp dụng):\n" +
      '{"hanh_dong": "' + HANH_DONG_HOP_LE.join("|") + '",\n' +
      ' "sinh_luc": <số nguyên -15..10>,\n' +
      ' "tu_vi": <0..8>,\n' +
      ' "bac": <-10..10>,\n' +
      ' "than_niem": <0..2>,\n' +
      ' "hao_cam": {"<tên NPC đã gặp>": <-10..10>},\n' +
      ' "nhan_xet": "<một câu tiếng Việt ngắn>"}\n' +
      "Quy tắc: thay đổi phải NHỎ; chỉ dùng NPC đã liệt kê trong bối cảnh; " +
      "KHÔNG bịa sự kiện, KHÔNG đổi đoạn truyện. Chỉ trả JSON, không giải thích.";
    let raw;
    try {
      raw = await _goi_gemini(prompt, 400);
    } catch (e) {
      return {};
    }
    let d;
    try {
      d = _tach_json(raw);
    } catch (e) {
      return {};
    }
    if (typeof d !== "object" || d === null || Array.isArray(d)) return {};
    const y = {};
    if (HANH_DONG_HOP_LE.includes(d.hanh_dong)) y.hanh_dong = d.hanh_dong;
    for (const k of ["sinh_luc", "tu_vi", "bac", "than_niem"]) {
      const n = _so_nguyen(d[k]);
      if (n !== null && n !== 0) {
        const [lo, hi] = GIOI_HAN[k];
        y[k] = Math.max(lo, Math.min(hi, n));
      }
    }
    const hc = d.hao_cam;
    if (typeof hc === "object" && hc !== null && !Array.isArray(hc)) {
      const loc = {};
      for (const [ten, v] of Object.entries(hc)) {
        const n = _so_nguyen(v);
        if (typeof ten === "string" && n !== null && n !== 0) {
          const [lo, hi] = GIOI_HAN.hao_cam;
          loc[ten] = Math.max(lo, Math.min(hi, n));
        }
      }
      if (Object.keys(loc).length) y.hao_cam = loc;
    }
    if (typeof d.nhan_xet === "string") y.nhan_xet = d.nhan_xet.trim().slice(0, 160);
    return y;
  }

  const AI = {
    KHOA_KEY, MODEL_DU_PHONG,
    lay_key, dat_key, co_key,
    thu_ket_noi, san_sang, ke_lai, ke_lai_tien_hiep, nhan_dien, _tach_json,
    van_ban_dung,
  };

  goc.AI = AI;
  if (typeof module !== "undefined" && module.exports) module.exports = AI;
})(typeof globalThis !== "undefined" ? globalThis : this);
