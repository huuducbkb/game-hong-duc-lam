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
  const t = (inp.value || '').trim();
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
  const mb = f.size / 1024 / 1024;
  if(mb > 24){
    ghHienTT(tt,'warn',`⚠️ File ${mb.toFixed(1)} MB quá lớn để gửi thẳng (trần 24 MB). `
      + 'Nén lại thành mp3 96 kbps rồi gửi lại — 30 giây ở mức đó chỉ khoảng 0.4 MB.');
    return;
  }
  nut.disabled = true;
  ghHienTT(tt,'muted',`Đang gửi <b>${f.name}</b> — ${mb.toFixed(1)} MB… Đừng đóng tab.`);
  try{
    const b64 = await blobB64(f);
    await ghPutFile(`${INBOX}/${ma}/${file}`, b64);
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
  if(chu) chu.innerHTML = `${f.name}<small>${mb.toFixed(1)} MB — bấm 📤 Gửi tiếng này</small>`;
  if(thanh){ thanh.hidden = true; if(ruot) ruot.style.width = '0%'; }
  if(tt) ghHienTT(tt,'muted','Đã chọn file. Bấm 📤 Gửi tiếng này.');
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
