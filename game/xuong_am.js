/* ================= tiện ích ================= */
function cpText(id, btn){
  const t = document.getElementById(id);
  if(!t) return;
  const chu = t.value;
  const xong = () => {
    const cu = btn.textContent;
    btn.textContent = '✅ Đã copy';
    setTimeout(() => btn.textContent = cu, 1600);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(chu).then(xong).catch(() => chon(t, xong));
  } else chon(t, xong);
}
function chon(t, xong){
  t.removeAttribute('readonly'); t.select(); t.setSelectionRange(0, 999999);
  try{ document.execCommand('copy'); xong(); }catch(e){}
  t.setAttribute('readonly','');
}
/* Copy một chuỗi rời (từ khoá tiếng Anh) — không có textarea để chọn. */
function cpChu(btn, chu){
  const xong = () => {
    const cu = btn.textContent;
    btn.classList.add('da');
    btn.textContent = '✅ ' + cu;
    setTimeout(() => { btn.textContent = cu; btn.classList.remove('da'); }, 1500);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(chu).then(xong).catch(() => {});
    return;
  }
  // Safari cũ: tạo vùng chọn tạm
  const t = document.createElement('textarea');
  t.value = chu; t.style.position = 'fixed'; t.style.opacity = '0';
  document.body.appendChild(t); t.select();
  try{ document.execCommand('copy'); xong(); }catch(e){}
  document.body.removeChild(t);
}
function taiTxt(id, ten){
  const t = document.getElementById(id);
  if(!t) return;
  const b = new Blob([t.value], {type:'text/plain;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b); a.download = ten; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

/* ================= GitHub ================= */
const GH_REPO = '__REPO__';
const GH_BRANCH = 'main';
const GH_LS = 'xuong_am_gh_token';
const AM_DIR = '__DIR__';
const INBOX = '__INBOX__';

function ghToken(){ return localStorage.getItem(GH_LS) || ''; }

function ghHienTT(el, loai, html){
  if(!el) return;
  el.hidden = false;
  el.innerHTML = `<span class="${loai}">${html}</span>`;
}

async function ghLuuToken(){
  const inp = document.getElementById('gh-token');
  const tt = document.getElementById('gh-tt');
  // Ô token luôn trống sau khi tải lại (trình duyệt xoá ô password), nên nếu
  // người dùng bấm Lưu mà không dán gì thì kiểm tra lại token đã lưu.
  const t = (inp.value || '').trim() || ghToken();
  if(!t){ ghHienTT(tt,'warn','⚠️ Chưa dán token.'); return; }
  ghHienTT(tt,'muted','Đang kiểm tra token…');
  try{
    const r = await fetch(`https://api.github.com/repos/${GH_REPO}`, {
      headers:{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}});
    if(!r.ok){
      ghHienTT(tt,'warn',`⚠️ Token không dùng được (HTTP ${r.status}). Kiểm tra quyền Contents: Read and write.`);
      return;
    }
    const j = await r.json();
    if(j.permissions && j.permissions.push === false){
      ghHienTT(tt,'warn','⚠️ Token chưa có quyền ghi (cần Contents: Read and write).');
      return;
    }
    localStorage.setItem(GH_LS, t);
    ghHienTT(tt,'ok',`✅ Đã kết nối <b>${j.full_name}</b>.`);
  }catch(e){ ghHienTT(tt,'warn',`⚠️ Lỗi kết nối: ${e}`); }
}

function ghQuenToken(){
  localStorage.removeItem(GH_LS);
  const i = document.getElementById('gh-token'); if(i) i.value = '';
  ghHienTT(document.getElementById('gh-tt'),'muted','Đã quên token trong trình duyệt này.');
}

function blobB64(blob){
  return new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = () => res(r.result.split(',')[1]);
    r.onerror = () => rej(new Error('đọc file lỗi'));
    r.readAsDataURL(blob);
  });
}

/* ===== trích tiếng từ video, ngay trong trình duyệt =====
   Video không bao giờ được gửi lên: trình duyệt đọc luồng tiếng, ghi ra WAV,
   rồi chỉ file WAV đó được đẩy vào inbox. Bot nén WAV thành mp3 như mọi file
   khác. Nhờ vậy repo không phải chứa video, kể cả trong lịch sử git.

   decodeAudioData đọc thẳng được tiếng trong mp4/mov — đã đo thật trên WebKit
   (nhân Safari của iPhone): cả .mp4 và .mov đều ra đúng số giây. Không cần
   thẻ <video> cũng không cần MediaRecorder. */
const DUOI_VIDEO = ['mp4','mov','m4v','webm','mkv','avi','3gp','mpg','mpeg','wmv'];
const GIAY_LAY = 12;        // phải khớp GIAY_LAY trong tools/xu_ly_am.py
const TRAN_VIDEO_MB = 5;    // video lớn hơn mức này thì giải mã trên điện thoại quá chậm

function laVideo(f){
  const ten = (f.name || '').toLowerCase();
  const duoi = ten.split('.').pop();
  if(DUOI_VIDEO.includes(duoi)) return true;
  // MIME trên iPhone hay để trống hoặc "application/octet-stream", nên đuôi
  // file là dấu hiệu đáng tin hơn.
  return /^video\//.test(f.type || '');
}

/* Ghi AudioBuffer thành WAV 16-bit. Tự viết thay vì dùng lamejs: không phải
   nạp thêm thư viện ngoài, và bot đằng nào cũng nén lại nên chất lượng không
   mất thêm. */
function wavTuBuffer(buf){
  const kenh = Math.min(2, buf.numberOfChannels);
  const n = buf.length;
  const dai = 44 + n * kenh * 2;
  const dv = new DataView(new ArrayBuffer(dai));
  const ghi = (o, s) => { for(let i=0;i<s.length;i++) dv.setUint8(o+i, s.charCodeAt(i)); };
  ghi(0,'RIFF'); dv.setUint32(4, dai-8, true); ghi(8,'WAVE');
  ghi(12,'fmt '); dv.setUint32(16,16,true); dv.setUint16(20,1,true);
  dv.setUint16(22,kenh,true); dv.setUint32(24,buf.sampleRate,true);
  dv.setUint32(28,buf.sampleRate*kenh*2,true); dv.setUint16(32,kenh*2,true);
  dv.setUint16(34,16,true); ghi(36,'data'); dv.setUint32(40,n*kenh*2,true);
  const duLieu = [];
  for(let c=0;c<kenh;c++) duLieu.push(buf.getChannelData(c));
  let o = 44;
  for(let i=0;i<n;i++){
    for(let c=0;c<kenh;c++){
      let v = Math.max(-1, Math.min(1, duLieu[c][i]));
      dv.setInt16(o, v < 0 ? v*0x8000 : v*0x7fff, true);
      o += 2;
    }
  }
  return new Blob([dv], {type:'audio/wav'});
}

/* Trả về {blob, ten, giay}. Chỉ lấy GIAY_LAY giây đầu, đúng như bot vẫn làm. */
async function tiengTuVideo(f, giayLay){
  const ab = await f.arrayBuffer();
  const Ctx = window.AudioContext || window.webkitAudioContext;
  if(!Ctx) throw new Error('Trình duyệt này không đọc được tiếng trong video.');
  const ctx = new Ctx();
  let buf;
  try{
    buf = await new Promise((res, rej) => ctx.decodeAudioData(ab, res, rej));
  }catch(e){
    throw new Error('Không đọc được tiếng trong video này. Video có thể không '
      + 'có tiếng, hoặc dùng định dạng máy này không hỗ trợ.');
  }
  if(!buf || !buf.length) throw new Error('Video này không có luồng tiếng.');
  const can = Math.min(buf.length, Math.round(buf.sampleRate * giayLay));
  const cat = ctx.createBuffer(buf.numberOfChannels, can, buf.sampleRate);
  for(let c=0;c<buf.numberOfChannels;c++){
    cat.copyToChannel(buf.getChannelData(c).subarray(0, can), c);
  }
  const ten = (f.name || 'video').replace(/\.[^.]+$/, '') + '.wav';
  return {blob: wavTuBuffer(cat), ten, giay: can / buf.sampleRate};
}

async function ghLaySha(duong){
  const r = await fetch(
    `https://api.github.com/repos/${GH_REPO}/contents/${duong}?ref=${GH_BRANCH}`,
    {headers:{'Authorization':`Bearer ${ghToken()}`,'Accept':'application/vnd.github+json'}});
  if(r.status === 200){ const j = await r.json(); return j.sha || null; }
  return null;
}

/* Đẩy file lên xuong-am-inbox/<ma>/<file> — thư mục con = mã nhóm, nên workflow
   gán thẳng không cần đoán. Đặt ở inbox (không phải docs/assets/am) là cố ý:
   chỉ push vào inbox mới kích hoạt workflow nén + cập nhật trạng thái. */
async function ghPutFile(duong, b64){
  const body = {message:`Xưởng âm thanh: thêm ${duong.split('/').slice(-2)[0]}`,
                 content:b64, branch:GH_BRANCH};
  const sha = await ghLaySha(duong);
  if(sha) body.sha = sha;
  const r = await fetch(`https://api.github.com/repos/${GH_REPO}/contents/${duong}`, {
    method:'PUT',
    headers:{'Authorization':`Bearer ${ghToken()}`,'Accept':'application/vnd.github+json',
             'Content-Type':'application/json'},
    body:JSON.stringify(body)});
  if(!r.ok){
    let loi = '';
    try{ const j = await r.json(); loi = j.message || ''; }catch(e){}
    throw new Error(`HTTP ${r.status}${loi?' — '+loi:''}`);
  }
  return true;
}

/* ================= kiểm tra / gửi ================= */
async function kiemTraMot(hop){
  const file = hop.dataset.file;
  const ma = hop.dataset.ma;
  const tt = hop.querySelector('[data-tt]');
  const nut = hop.querySelector('[data-kiem]');
  const oNghe = hop.closest('article').querySelector('[data-nghe]');
  const audio = oNghe.querySelector('[data-audio]');
  const chua = oNghe.querySelector('[data-chua]');
  if(nut) nut.classList.add('dang');
  try{
    const t = ghToken();
    const r = await fetch(
      `https://api.github.com/repos/${GH_REPO}/commits?path=${AM_DIR}${file}&per_page=1`,
      {headers:t ? {'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}
                  : {'Accept':'application/vnd.github+json'}});
    if(r.status === 403 || r.status === 429)
      throw new Error('GitHub tạm giới hạn lượt gọi — chờ chút rồi thử lại');
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const ds = await r.json();
    if(!Array.isArray(ds) || !ds.length){
      audio.hidden = true; audio.removeAttribute('src');
      chua.hidden = false;
      ghHienTT(tt,'muted','⬜ Chưa có trên trang. Gửi file rồi bấm 🔄 Kiểm tra lại (bot cần ~1–2 phút).');
      return {co:false};
    }
    const sha = ds[0].sha;
    audio.src = `https://raw.githubusercontent.com/${GH_REPO}/${sha}/${AM_DIR}${file}`;
    audio.hidden = false;
    chua.hidden = true;
    const the = hop.closest('article');
    if(the){
      the.classList.add('done');
      const nh = the.querySelector('[data-badge]');
      if(nh){ nh.className = 'badge chac'; nh.textContent = '✅ đã có'; }
    }
    const khi = new Date(ds[0].commit.author.date);
    const gio = isNaN(khi) ? ds[0].commit.author.date
      : khi.toLocaleString('vi-VN',{hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'});
    ghHienTT(tt,'ok',`✅ Đã lên trang · ${gio} · <code>${sha.slice(0,7)}</code>`);
    return {co:true};
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Không kiểm tra được: ${e}`);
    return {co:null};
  }finally{
    if(nut) nut.classList.remove('dang');
  }
}

async function theoDoi(hop){
  const tt = hop.querySelector('[data-tt]');
  for(let lan = 1; lan <= 10; lan++){
    await new Promise(r => setTimeout(r, 15000));
    const kq = await kiemTraMot(hop);
    if(kq.co){ ghHienTT(tt,'ok','🎉 Tiếng đã lên trang!'); return; }
    if(kq.co === null) return;
    if(lan < 10) ghHienTT(tt,'muted',
      `⏳ Bot đang xử lý… tự kiểm tra lại sau 15 giây (lần ${lan}/10). Cứ để trang mở.`);
  }
  ghHienTT(tt,'muted','⏳ Lâu hơn thường lệ. Bấm 🔄 Kiểm tra để thử lại.');
}

async function guiMot(hop){
  const file = hop.dataset.file;
  const ma = hop.dataset.ma;
  const inp = hop.querySelector('[data-chon]');
  const tt = hop.querySelector('[data-tt]');
  const nut = hop.querySelector('[data-gui-kt]');
  if(!ghToken()){
    ghHienTT(tt,'warn','⚠️ Chưa kết nối GitHub. Dán token ở mục 🔑 phía trên rồi thử lại.');
    return;
  }
  if(!inp.files || !inp.files.length){
    ghHienTT(tt,'warn','⚠️ Chưa chọn file. Bấm ô chọn file phía trên.');
    return;
  }
  const f = inp.files[0];
  nut.disabled = true;
  let gui = f;
  let tenGui = file;      // tên trong inbox; bot lấy mã cảnh từ tên thư mục
  try{
    if(laVideo(f)){
      const mbVid = f.size / 1024 / 1024;
      if(mbVid > TRAN_VIDEO_MB){
        ghHienTT(tt,'warn',`⚠️ Video ${mbVid.toFixed(1)} MB, quá trần ${TRAN_VIDEO_MB} MB. `
          + 'Cắt bớt video trên điện thoại rồi chọn lại.');
        return;
      }
      ghHienTT(tt,'muted',`Đang trích tiếng từ <b>${f.name}</b>… Video không được tải lên, `
        + 'chỉ đoạn tiếng được gửi đi.');
      const t = await tiengTuVideo(f, GIAY_LAY);
      gui = new File([t.blob], t.ten, {type:'audio/wav'});
      tenGui = `${ma}.wav`;
      ghHienTT(tt,'muted',`Đã trích ${t.giay.toFixed(1)} giây tiếng. Đang gửi…`);
    }
    const mb = gui.size / 1024 / 1024;
    if(mb > 24){
      ghHienTT(tt,'warn',`⚠️ File ${mb.toFixed(1)} MB quá lớn để gửi thẳng (trần 24 MB). `
        + 'Nén lại thành mp3 96 kbps rồi gửi lại — 12 giây ở mức đó chỉ khoảng 0.2 MB.');
      return;
    }
    ghHienTT(tt,'muted',`Đang gửi <b>${gui.name}</b> — ${mb.toFixed(1)} MB… Đừng đóng tab.`);
    const b64 = await blobB64(gui);
    await ghPutFile(`${INBOX}/${ma}/${tenGui}`, b64);
    ghHienTT(tt,'ok','📤 Đã gửi. Bot sẽ nén và cập nhật trong 1–2 phút — tự kiểm tra nhé.');
    theoDoi(hop);
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Gửi lỗi: ${e}`);
  }finally{
    nut.disabled = false;
  }
}

/* ================= nối sự kiện + kiểm lúc mở ================= */
function chonFile(hop, f){
  const tt = hop.querySelector('[data-tt]');
  const nut = hop.querySelector('[data-gui-kt]');
  const vung = hop.querySelector('.tha-am');
  const chu = hop.querySelector('.tha-am-chu');
  const thanh = hop.querySelector('[data-thanh]');
  const ruot = hop.querySelector('[data-ruot]');
  if(!f){
    if(nut) nut.disabled = true;
    if(vung) vung.classList.remove('co-file');
    if(chu) chu.innerHTML = 'Chạm để chọn file tiếng<small>hoặc kéo file vào đây</small>';
    if(thanh) thanh.hidden = true;
    return;
  }
  const mb = f.size / 1024 / 1024;
  if(nut) nut.disabled = false;
  if(vung) vung.classList.add('co-file');
  const vid = laVideo(f);
  if(chu) chu.innerHTML = `${f.name}<small>${mb.toFixed(1)} MB${vid ? ' — video, sẽ chỉ lấy tiếng' : ''} — bấm 📤 Gửi tiếng này</small>`;
  if(thanh){ thanh.hidden = true; if(ruot) ruot.style.width = '0%'; }
  if(tt){
    if(vid && mb > TRAN_VIDEO_MB){
      ghHienTT(tt,'warn',`⚠️ Video ${mb.toFixed(1)} MB, quá trần ${TRAN_VIDEO_MB} MB. `
        + 'Cắt bớt video rồi chọn lại.');
    }else if(vid){
      ghHienTT(tt,'muted',`Đã chọn video ${mb.toFixed(1)} MB. Bấm 📤 Gửi tiếng này — `
        + `trình duyệt sẽ tự trích ${GIAY_LAY} giây tiếng, video không tải lên.`);
    }else{
      ghHienTT(tt,'muted','Đã chọn file. Bấm 📤 Gửi tiếng này.');
    }
  }
}

// Khôi phục trạng thái kết nối sau khi tải lại trang. Không có hàm này thì
// token vẫn nằm trong localStorage và việc gửi file vẫn chạy, nhưng ô token
// trống trơn nên người dùng tưởng đã mất và dán lại mỗi lần.
async function ghKhoiPhuc(){
  const inp = document.getElementById('gh-token');
  const tt = document.getElementById('gh-tt');
  const t = ghToken();
  if(!t) return;
  if(inp) inp.placeholder = 'Đã lưu token — để trống nếu không đổi';
  ghHienTT(tt,'muted','Đang kiểm tra token đã lưu…');
  try{
    const r = await fetch(`https://api.github.com/repos/${GH_REPO}`, {
      headers:{'Authorization':`Bearer ${t}`,'Accept':'application/vnd.github+json'}});
    if(!r.ok){
      ghHienTT(tt,'warn',`⚠️ Token đã lưu nhưng không dùng được (HTTP ${r.status}). `
        + 'Dán token mới rồi bấm Lưu, hoặc bấm Quên token.');
      return;
    }
    const j = await r.json();
    if(j.permissions && j.permissions.push === false){
      ghHienTT(tt,'warn','⚠️ Token đã lưu nhưng thiếu quyền ghi (cần Contents: Read and write).');
      return;
    }
    ghHienTT(tt,'ok',`✅ Đã kết nối <b>${j.full_name}</b> — token lưu trong trình duyệt này, không cần dán lại.`);
  }catch(e){
    // Mất mạng hoặc GitHub bị chặn: không xoá token, vì nó vẫn có thể dùng được.
    ghHienTT(tt,'warn','⚠️ Token vẫn đang lưu trong trình duyệt này, nhưng chưa '
      + 'kiểm tra được vì không gọi được GitHub. Cứ thử gửi file; nếu lỗi thì '
      + 'kiểm tra mạng rồi tải lại trang.');
  }
}

document.querySelectorAll('[data-gui]').forEach(hop => {
  const nut = hop.querySelector('[data-gui-kt]');
  const kiem = hop.querySelector('[data-kiem]');
  const inp = hop.querySelector('[data-chon]');
  if(nut) nut.addEventListener('click', () => guiMot(hop));
  if(kiem) kiem.addEventListener('click', () => kiemTraMot(hop));
  if(inp){
    inp.addEventListener('change', () => chonFile(hop, inp.files && inp.files[0]));
    // kéo-thả chỉ có ý nghĩa trên máy tính, nhưng thêm cũng không hại
    const vung = hop.querySelector('.tha-am');
    if(vung){
      vung.addEventListener('dragover', e => { e.preventDefault(); vung.classList.add('co-file'); });
      vung.addEventListener('dragleave', () => {
        if(!inp.files || !inp.files.length) vung.classList.remove('co-file'); });
      vung.addEventListener('drop', e => {
        e.preventDefault();
        if(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length){
          inp.files = e.dataTransfer.files;
          chonFile(hop, e.dataTransfer.files[0]);
        }
      });
    }
  }
  kiemTraMot(hop);
});

ghKhoiPhuc();
