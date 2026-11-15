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
  const TEN_RIENG = ["Hàn Lập", "Thất Huyền Môn", "Dã Lang Bang", "Lý Hổ",
    "Tần Báo", "Thất Huyền trấn", "hắc quáng động"];

  const _cache_ke = new Map();
  const CACHE_TOI_DA = 500;

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
      "Chỉ trả về đoạn kể, không giải thích.";
    return _goi_gemini(prompt, 500);
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
    const gioi_han = Math.trunc(doan_ke.length * 1.2);
    const prompt =
      "Bạn là biên tập viên văn tiên hiệp. Nhiệm vụ: ĐỔI TỪ NGỮ trong đoạn dưới " +
      "sang giọng cổ phong tiên hiệp. TUYỆT ĐỐI KHÔNG viết lại tự do.\n\n" +
      "CÁCH LÀM:\n" +
      "- Giữ nguyên TỪNG CÂU, giữ nguyên thứ tự câu, giữ nguyên số câu.\n" +
      "- Chỉ thay một số từ ngữ (thường → cổ phong). Ví dụ: 'im lặng'→'tịch mịch', " +
      "'chạy'→'phi thân', 'nghĩ'→'thầm nghĩ'.\n" +
      "- KHÔNG thêm câu mới. KHÔNG thêm sự việc mới. KHÔNG thêm nhân vật/địa danh.\n\n" +
      "VÍ DỤ:\n" +
      "GỐC: Ta ngồi xuống, im lặng hồi lâu.\n" +
      "ĐÚNG: Ta ngồi xuống, tịch mịch hồi lâu.\n" +
      "SAI: Ta ngồi xuống bên vách đá, im lặng hồi lâu, lòng dấy lên nỗi bất an.\n" +
      "(câu SAI thêm 'bên vách đá' và 'nỗi bất an' — KHÔNG được làm vậy)\n\n" +
      "QUY TẮC:\n" +
      "1. GIỮ NGUYÊN mọi sự kiện, nhân vật, địa điểm, vật phẩm, kết quả.\n" +
      "2. KHÔNG thêm bất kỳ chi tiết nào không có trong đoạn gốc.\n" +
      "3. Giữ nguyên giới tính và cách gọi nhân vật (hắn/ta/nó…).\n" +
      `4. Tối đa ${gioi_han} ký tự.\n` +
      "5. Viết đúng tên riêng: " + ten + ".\n" +
      "6. Giữ định dạng: dòng trống giữa các đoạn; nội tâm trong *…*.\n" +
      "7. Chỉ trả về đoạn đã sửa, không giải thích.\n\n" +
      `ĐOẠN GỐC:\n${doan_ke}${phan_boi_canh}${phan_hanh_dong}`;
    let ket_qua;
    try {
      ket_qua = (await _goi_gemini(prompt, 700)).trim();
    } catch (e) {
      return "";
    }
    if (!ket_qua) return "";
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
  };

  goc.AI = AI;
  if (typeof module !== "undefined" && module.exports) module.exports = AI;
})(typeof globalThis !== "undefined" ? globalThis : this);
