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

/* Nén AudioBuffer thành mp3 bằng lamejs (nhúng sẵn ở lamejs.js). Gửi mp3 thay
   vì WAV là cố ý: WAV 12 giây là 2 MB, base64 thành 2,7 MB, và mọi file đẩy
   vào inbox đều nằm vĩnh viễn trong lịch sử git. 43 cảnh như vậy là 29 MB;
   mp3 96 kbps chỉ 8 MB. Hạ xuống 22 kHz mono vì tiếng môi trường không có
   thông tin gì ở tần số cao, mà bot cũng nén về 96 kbps.
   WebKit không có MediaRecorder nên không dùng cách đó được. */
function mp3TuBuffer(buf){
  if(typeof lamejs === 'undefined'){
    throw new Error('Thiếu bộ nén mp3. Tải lại trang rồi thử lại.');
  }
  const sr = 22050;
  const kenh = Math.min(2, buf.numberOfChannels);
  // Trộn về mono: tiếng môi trường không cần stereo, mà mono rẻ hơn một nửa.
  const n = Math.max(1, Math.round(buf.length * sr / buf.sampleRate));
  const pcm = new Int16Array(n);
  const duLieu = [];
  for(let c=0;c<kenh;c++) duLieu.push(buf.getChannelData(c));
  const buoc = buf.sampleRate / sr;
  for(let i=0;i<n;i++){
    const viTri = i * buoc;
    const j = Math.floor(viTri);
    const le = viTri - j;
    let v = 0;
    for(let c=0;c<kenh;c++){
      const a = duLieu[c][j] || 0;
      const b = duLieu[c][j+1] !== undefined ? duLieu[c][j+1] : a;
      v += a + (b - a) * le;
    }
    v = Math.max(-1, Math.min(1, v / kenh));
    pcm[i] = v < 0 ? v * 0x8000 : v * 0x7fff;
  }
  const enc = new lamejs.Mp3Encoder(1, sr, 96);
  const phan = [];
  for(let i=0;i<n;i+=1152){
    const ra = enc.encodeBuffer(pcm.subarray(i, Math.min(i+1152, n)));
    if(ra.length) phan.push(new Int8Array(ra));
  }
  const cuoi = enc.flush();
  if(cuoi.length) phan.push(new Int8Array(cuoi));
  return new Blob(phan, {type:'audio/mpeg'});
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
  const ten = (f.name || 'video').replace(/\.[^.]+$/, '') + '.mp3';
  return {blob: mp3TuBuffer(cat), ten, giay: can / buf.sampleRate};
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
// Mã băm nội dung file, 8 ký tự đầu — cùng cách ghi_danh_sach_am.py tính `v`.
async function bamNoiDung(duong){
  const r = await fetch(duong, {cache:'no-store'});
  if(!r.ok) return {ok:false, status:r.status};
  const buf = await r.arrayBuffer();
  const h = await crypto.subtle.digest('SHA-256', buf);
  const hex = [...new Uint8Array(h)].map(x => x.toString(16).padStart(2,'0')).join('');
  return {ok:true, bam:hex.slice(0,8), bytes:buf.byteLength};
}

// Bản đang có trên trang lúc này, rỗng nếu chưa có file.
async function bamHienTai(hop){
  try{
    const duong = new URL('../' + AM_DIR + hop.dataset.file, location.href);
    duong.searchParams.set('v', Date.now());
    const kq = await bamNoiDung(duong.href);
    return kq.ok ? kq.bam : '';
  }catch(e){ return ''; }
}

async function kiemTraMot(hop, banTruoc){
  const file = hop.dataset.file;
  const tt = hop.querySelector('[data-tt]');
  const nut = hop.querySelector('[data-kiem]');
  const the = hop.closest('article');
  const oNghe = the.querySelector('[data-nghe]');
  const audio = oNghe.querySelector('[data-audio]');
  const chua = oNghe.querySelector('[data-chua]');
  if(nut) nut.classList.add('dang');
  try{
    // Tải thật file rồi băm nội dung. Trước đây chỉ hỏi HEAD "file có tồn tại
    // không": file cũ vẫn nằm đó nên lần nào cũng báo "đã có", kể cả khi bản
    // vừa gửi chưa hề lên trang — đúng cái làm người dùng tưởng đã xong mà
    // nghe vẫn ra tiếng cũ.
    // ?v= đổi mỗi lần: GitHub Pages giữ file 10 phút, không có mã này thì đọc
    // phải bản cũ trong bộ nhớ đệm.
    const duong = new URL('../' + AM_DIR + file, location.href);
    duong.searchParams.set('v', Date.now());
    const kq = await bamNoiDung(duong.href);
    if(!kq.ok){
      if(kq.status === 403){
        ghHienTT(tt,'warn','⚠️ Trang chưa cho xem file này. Chờ ~1–2 phút rồi bấm lại.');
        return {co:null};
      }
      audio.hidden = true; audio.removeAttribute('src');
      chua.hidden = false;
      ghHienTT(tt,'muted','⬜ Chưa thấy trên trang. Bot cần ~1–2 phút sau khi gửi; chờ rồi bấm 🔄 Kiểm tra lại.');
      return {co:false};
    }
    audio.src = duong.href;
    audio.hidden = false;
    chua.hidden = true;
    the.classList.add('done');
    the.dataset.co = '1';
    const nh = the.querySelector('[data-badge]');
    if(nh){ nh.className = 'badge chac'; nh.textContent = '✅ đã có'; }

    const kb = Math.round(kq.bytes / 1024);
    // Gửi xong thì theo dõi: chỉ báo xong khi bản trên trang KHÁC bản lúc bấm
    // gửi. Không có mốc so sánh thì không thể biết bản mới đã lên hay chưa.
    if(banTruoc){
      if(banTruoc === kq.bam){
        ghHienTT(tt,'warn',`⚠️ Vẫn là bản cũ (${kq.bam}). Bot chưa xử lý xong hoặc chưa đưa lên trang. `
          + 'Chờ ~1–2 phút rồi bấm 🔄 Kiểm tra lại.');
        return {co:true, moi:false};
      }
      ghHienTT(tt,'ok',`🎉 Bản mới đã lên trang (${banTruoc} → ${kq.bam}, ${kb} KB). Bấm ▶ để nghe.`);
      return {co:true, moi:true};
    }
    // Bấm kiểm tra tự do: nói đúng bản đang phát, không phán bừa là "đã xong".
    const laBaked = kq.bam === (the.dataset.ban || '');
    ghHienTT(tt, laBaked ? 'ok' : 'warn',
      `Đang phát bản ${kq.bam} · ${kb} KB.`
      + (laBaked ? '' : ' Khác bản ghi lúc tạo trang — tải lại trang để thấy trạng thái mới.'));
    return {co:true, moi:false, bam:kq.bam};
  }catch(e){
    ghHienTT(tt,'warn',`⚠️ Không kiểm tra được: ${e}`);
    return {co:null};
  }finally{
    if(nut) nut.classList.remove('dang');
  }
}

async function theoDoi(hop, banTruoc){
  const tt = hop.querySelector('[data-tt]');
  for(let lan = 1; lan <= 10; lan++){
    await new Promise(r => setTimeout(r, 15000));
    const kq = await kiemTraMot(hop, banTruoc);
    // Chỉ dừng khi bản trên trang THẬT SỰ khác bản trước khi gửi. Trước đây
    // dừng ngay khi thấy file tồn tại, nên báo "đã lên trang" trong khi vẫn
    // là tiếng cũ.
    if(kq.co && kq.moi) return;
    if(kq.co === null) return;
    if(lan < 10) ghHienTT(tt,'muted',
      `⏳ Bot đang xử lý… tự kiểm tra lại sau 15 giây (lần ${lan}/10). Cứ để trang mở.`);
  }
  ghHienTT(tt,'warn','⏳ Lâu hơn thường lệ. Bản mới CHƯA thấy trên trang. '
    + 'Bấm 🔄 Kiểm tra để thử lại, hoặc mở tab Xem trước để biết bot chạy tới đâu.');
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
      tenGui = `${ma}.mp3`;
      ghHienTT(tt,'muted',`Đã trích ${t.giay.toFixed(1)} giây tiếng. Đang gửi…`);
    }
    const mb = gui.size / 1024 / 1024;
    if(mb > 24){
      ghHienTT(tt,'warn',`⚠️ File ${mb.toFixed(1)} MB quá lớn để gửi thẳng (trần 24 MB). `
        + 'Nén lại thành mp3 96 kbps rồi gửi lại — 12 giây ở mức đó chỉ khoảng 0.2 MB.');
      return;
    }
    ghHienTT(tt,'muted',`Đang gửi <b>${gui.name}</b> — ${mb.toFixed(1)} MB… Đừng đóng tab.`);
    // Chốt bản đang có TRƯỚC khi gửi. Đây là mốc duy nhất để biết bản mới đã
    // lên trang hay chưa: không có nó thì mọi lần kiểm tra đều thấy "có file"
    // và báo xong trong khi tiếng vẫn là bản cũ.
    const banTruoc = await bamHienTai(hop);
    const b64 = await blobB64(gui);
    await ghPutFile(`${INBOX}/${ma}/${tenGui}`, b64);
    ghHienTT(tt,'ok','📤 Đã gửi lên GitHub. Bot sẽ nén và cập nhật trong 1–2 phút — '
      + `đang chờ bản mới${banTruoc ? ` (bản cũ ${banTruoc})` : ''}.`);
    theoDoi(hop, banTruoc);
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
  datNgheSan(hop);
});

// Cảnh đã có file thì trỏ thẳng vào file trong repo — không gọi GitHub API.
// Trước đây mỗi thẻ gọi API một lần, mở trang là 64 lượt, vượt hạn mức 60/giờ
// nên GitHub trả 403 và mọi cảnh hiện như chưa có tiếng.
function datNgheSan(hop){
  const the = hop.closest('article');
  if(!the || the.dataset.co !== '1') return;
  const oNghe = the.querySelector('[data-nghe]');
  if(!oNghe) return;
  const audio = oNghe.querySelector('[data-audio]');
  const chua = oNghe.querySelector('[data-chua]');
  if(audio){
    // ?v= đổi mỗi lần mở trang: GitHub Pages cho giữ file 10 phút, không có mã
    // này thì nghe lại bản cũ dù đã tải lên bản mới.
    const duongNghe = new URL('../' + AM_DIR + hop.dataset.file, location.href);
    duongNghe.searchParams.set('v', Date.now());
    audio.src = duongNghe.href;
    audio.hidden = false;
  }
  if(chua) chua.hidden = true;
}

ghKhoiPhuc();
