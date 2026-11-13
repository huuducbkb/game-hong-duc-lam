#!/usr/bin/env python3
"""Xưởng tài nguyên: cung cấp prompt để copy + nhận ảnh upload (dạng base64 JSON).
Chạy: python3 tools_server.py   -> mở http://<host>:12001
Là công cụ tạm, xóa sau khi xong việc."""
import base64
import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = "/workspace/game-hong-duc-lam"
ENV_PATH = f"{ROOT}/.env"
UI_DIR = f"{ROOT}/assets/ui"
SCENE_DIR = f"{ROOT}/assets/scene"
FIELDS = ["OPENROUTER_API_KEY", "geminikey", "geminikey1", "geminikey2", "geminikey3"]

STYLE = (
    "Traditional East Asian ink wash painting (shui-mo / thủy mặc) on rough handmade mulberry (dó) paper. "
    "Monochrome black ink with subtle warm cream and pale sepia paper tones, visible paper fiber texture, "
    "wet ink bleeding edges, dry brush strokes, generous empty negative space (liubai), "
    "minimal and elegant ancient Chinese hanging-scroll aesthetic, muted and calm. "
    "IMPORTANT: absolutely no text, no letters, no numbers, no calligraphy, no signature, "
    "no watermark, no logo, no UI labels."
)

ASSETS = [
    {
        "key": "bg-main",
        "name": "1. Nền toàn màn hình",
        "ratio": "9:16 dọc (1080×1920)",
        "file": "bg-main.png",
        "use": "Nền sau tất cả (dùng background-size: cover).",
        "prompt": STYLE + " "
        "An almost empty aged-paper background for a mobile game screen, portrait orientation. "
        "Subtle paper texture with faint uneven washes of pale ink near the corners and edges, "
        "a very faint silhouette of distant misty mountains along the very top and bottom edges, "
        "a few tiny scattered ink specks and one or two faint dry-brush strokes at the margins. "
        "The whole center is left empty and light so game text can be placed on top. Low contrast, calm, quiet.",
    },
    {
        "key": "panel-character",
        "name": "2. Khung bảng nhân vật",
        "ratio": "3:4 dọc (900×1200)",
        "file": "panel-character.png",
        "use": "Khung bảng chỉ số nhân vật (cột trái). Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A vertical hanging-scroll card for a game interface, portrait orientation. "
        "The border is an irregular hand-painted black ink rectangle with dry-brush ends and slightly wobbly edges, "
        "a few small ink splashes near the corners, and a thin second inner line. "
        "The INSIDE of the panel is plain empty light paper with no decoration at all, reserved for text. "
        "One small red square seal stamp sits in the bottom-right corner of the border. "
        "Flat frontal view, centered, the frame fills almost the entire image with a small even margin.",
    },
    {
        "key": "panel-story",
        "name": "3. Khung bảng truyện",
        "ratio": "4:5 dọc (960×1200)",
        "file": "panel-story.png",
        "use": "Khung bảng nội dung câu chuyện. Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A large rectangular story panel for a game interface, portrait orientation, slightly softer and simpler than a scroll. "
        "A rough hand-painted black ink border with rounded irregular corners and light dry-brush texture, "
        "very subtle. The entire interior is plain empty light paper with nothing drawn inside, reserved for long text. "
        "No seal, no ornaments. Flat frontal view, the frame fills almost the whole image with a small even margin.",
    },
    {
        "key": "avatar-ring",
        "name": "4. Viền ảnh đại diện",
        "ratio": "1:1 vuông (1024×1024)",
        "file": "avatar-ring.png",
        "use": "Viền tròn quanh ảnh đại diện (sẽ đè lên ảnh người dùng).",
        "prompt": STYLE + " "
        "A single decorative circular ring for a game avatar frame, centered, on a plain empty light paper background. "
        "The ring is painted with bold black ink brush strokes, uneven and slightly broken, with dry-brush edges "
        "and a few tiny ink splashes. The inside of the circle and everything outside it is completely empty light paper. "
        "Only the ring itself, nothing else, no face, no figure.",
    },
    {
        "key": "btn-choice",
        "name": "5. Nền nút lựa chọn",
        "ratio": "5:1 ngang (1200×240)",
        "file": "btn-choice.png",
        "use": "Nền cho các nút chọn A/B/C. Ruột để trống cho chữ.",
        "prompt": STYLE + " "
        "A wide horizontal blank plaque / name-plate shape for a game button, very wide and short. "
        "Drawn as a simple hand-painted black ink rounded rectangle with thin dry-brush border and slightly wobbly edges. "
        "The interior is plain empty light paper, reserved for a single line of text. Minimal, one ink brush stroke along the bottom edge. "
        "Flat frontal view, the plaque fills almost the whole image.",
    },
    {
        "key": "seal",
        "name": "6. Ấn son (con dấu)",
        "ratio": "1:1 vuông (512×512)",
        "file": "seal.png",
        "use": "Con dấu đỏ trang trí (góc bảng, góc tranh).",
        "prompt": STYLE + " "
        "A single traditional red seal stamp (chop) on a plain empty light paper background, centered. "
        "A square vermilion-red stamped mark with rough uneven edges like real ink seal impression, "
        "containing a simple abstract ancient seal pattern (NOT readable characters). "
        "Faded, slightly blotchy, authentic antique look. Only the seal, nothing else.",
    },
    {
        "key": "divider-ink",
        "name": "7. Đường kẻ mực (tùy chọn)",
        "ratio": "10:1 ngang (1600×160)",
        "file": "divider-ink.png",
        "use": "Đường phân cách giữa các mục.",
        "prompt": STYLE + " "
        "A single horizontal decorative divider line for a game interface, extremely wide and short. "
        "A simple black ink brush stroke that starts thin, swells in the middle and fades to a dry broken end, "
        "with one or two small ink splashes. On a plain empty light paper background. "
        "Only the single brush stroke, nothing else.",
    },
]


def load_env():
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                env[k] = v
    return env


def save_env(pairs):
    lines = [f"{k}={v}" for k, v in pairs.items() if v]
    if "GEMINI_MODEL" not in pairs:
        lines.append("GEMINI_MODEL=gemini-2.5-flash-image")
    if "IMAGE_MODEL" not in pairs:
        lines.append("IMAGE_MODEL=google/gemini-3.1-flash-image")
    with open(ENV_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(ENV_PATH, 0o600)


def list_files(folder):
    if not os.path.isdir(folder):
        return []
    out = []
    for fn in sorted(os.listdir(folder)):
        p = os.path.join(folder, fn)
        if os.path.isfile(p):
            out.append((fn, os.path.getsize(p)))
    return out


def build_prompts_html():
    blocks = []
    for a in ASSETS:
        got = ""
        for fn, size in list_files(UI_DIR):
            if fn == a["file"]:
                got = f'<span class="got">✔ đã nhận ({size//1024} KB)</span>'
        blocks.append(f"""
<div class="card">
  <div class="head"><b>{a['name']}</b> <span class="ratio">{a['ratio']}</span> {got}</div>
  <div class="use">{a['use']} &nbsp;·&nbsp; tên file khi lưu: <code>{a['file']}</code></div>
  <textarea readonly rows="6" onclick="this.select()">{a['prompt']}</textarea>
  <button class="cp" onclick="cp(this)">📋 Copy prompt</button>
</div>""")
    return "\n".join(blocks)


def build_received_html():
    rows = []
    for folder, label in ((UI_DIR, "Giao diện"), (SCENE_DIR, "Bối cảnh")):
        for fn, size in list_files(folder):
            rows.append(f"<li>{label}: <b>{fn}</b> — {size//1024} KB</li>")
    if not rows:
        return "<p class='muted'>Chưa nhận được ảnh nào.</p>"
    return "<ul>" + "".join(rows) + "</ul>"


def page():
    env = load_env()
    keys_html = "".join(
        f'<label>{k}</label><input name="{k}" placeholder="{"sk-or-v1-..." if "OPENROUTER" in k else "AIza... / AQ..."}" '
        f'value="{env.get(k, "")[:0]}" autocomplete="off" autocapitalize="off">'
        for k in FIELDS
    )
    html = PAGE_TMPL
    html = html.replace("__PROMPTS__", build_prompts_html())
    html = html.replace("__RECEIVED__", build_received_html())
    html = html.replace("__KEYS__", keys_html)
    return html


PAGE_TMPL = """<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xưởng tài nguyên — Hồng Đức Tu Tiên Lộ</title>
<style>
 :root{--bg:#111a2b;--card:#182337;--ink:#e8e6df;--muted:#93a0b8;--gold:#ffd98a;--jade:#6fe0c0;--line:#2b3b57}
 *{box-sizing:border-box}
 body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--ink);
   margin:0;padding:18px;max-width:720px;margin:0 auto;line-height:1.55;-webkit-text-size-adjust:100%}
 h1{font-size:19px;color:var(--gold);margin:6px 0 2px}
 h2{font-size:15px;color:var(--jade);margin:26px 0 8px;border-bottom:1px solid var(--line);padding-bottom:6px}
 p,li{font-size:13.5px;color:#cbd4e4}
 .muted{color:var(--muted)}
 code{background:#0a1220;padding:1px 6px;border-radius:4px;color:var(--jade);font-size:12px}
 .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
 .head{font-size:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
 .ratio{font-size:11px;color:var(--muted);background:#0a1220;padding:2px 8px;border-radius:99px}
 .got{font-size:11px;color:#7fe0a8;background:#12351f;padding:2px 8px;border-radius:99px}
 .use{font-size:12px;color:var(--muted);margin:6px 0 8px}
 textarea{width:100%;font-size:12.5px;line-height:1.5;background:#0a1220;color:#dfe7f5;border:1px solid var(--line);
   border-radius:8px;padding:10px;resize:vertical;font-family:ui-monospace,Menlo,monospace}
 button{font-family:inherit;font-size:14px;font-weight:600;border:0;border-radius:10px;padding:11px 16px;cursor:pointer}
 .cp{margin-top:8px;background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600;width:100%}
 .cp.done{background:#2f8f5a;color:#eafff3}
 .up{background:linear-gradient(135deg,#2f8f7a,#6fe0c0);color:#04231c;width:100%;margin-top:10px}
 .ok{background:#12351f;border:1px solid #2f8f5a;padding:12px;border-radius:10px;color:#7fe0a8;font-size:13px}
 .warn{background:#3a1a10;border:1px solid #a05a2a;padding:12px;border-radius:10px;color:#ffb98a;font-size:13px}
 label{display:block;font-size:12px;color:var(--muted);margin:12px 0 4px}
 input{width:100%;padding:12px;font-size:14px;border-radius:9px;border:1px solid var(--line);
   background:#0a1220;color:var(--ink)}
 #drop{border:2px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--muted);
   font-size:13px;margin:10px 0;cursor:pointer}
 #drop.hot{border-color:var(--jade);color:var(--jade);background:#0f2230}
 ul{padding-left:18px}
 details{margin-top:22px}
 summary{cursor:pointer;color:var(--muted);font-size:13px}
 .steps li{margin:5px 0}
</style></head><body>

<h1>Xưởng tài nguyên</h1>
<p class="muted">Hồng Đức Tu Tiên Lộ · quy trình: bạn copy prompt → AI của bạn vẽ → bạn tải ảnh lên đây → tôi ghép vào game.</p>

<h2>Cách làm</h2>
<ol class="steps">
  <li>Bấm <b>Copy prompt</b> ở từng thẻ bên dưới.</li>
  <li>Dán vào AI tạo ảnh của bạn, chọn đúng <b>tỷ lệ</b> ghi trên thẻ.</li>
  <li>Tải ảnh kết quả về máy (đặt tên đúng như ghi trên thẻ, ví dụ <code>bg-main.png</code>).</li>
  <li>Kéo ảnh vào ô <b>Tải ảnh lên</b> ở cuối trang này.</li>
  <li>Nhắn trợ lý: <b>"đã gửi ảnh"</b> — tôi sẽ ghép vào giao diện.</li>
</ol>
<p class="muted">Lưu ý: prompt đã ghi rõ <b>không có chữ/ký tự</b> trong ảnh, vì chữ do AI vẽ thường sai. Chữ trong game do tôi viết bằng code.</p>

<h2>Danh sách prompt</h2>
__PROMPTS__

<h2>Ảnh đã nhận</h2>
<div class="card">__RECEIVED__</div>

<h2>Tải ảnh lên</h2>
<div class="card">
  <div id="drop">Bấm để chọn ảnh, hoặc kéo ảnh vào đây<br><span class="muted">(có thể chọn nhiều ảnh một lúc)</span></div>
  <input id="file" type="file" accept="image/*" multiple hidden>
  <button class="up" onclick="document.getElementById('file').click()">Chọn ảnh để tải lên</button>
  <div id="msg"></div>
</div>

<details>
  <summary>Cập nhật key (chỉ khi cần đổi)</summary>
  <form method="POST" action="/keys">
    __KEYS__
    <button class="up" type="submit" style="margin-top:14px">Lưu key</button>
  </form>
</details>

<script>
function cp(btn){
  const ta = btn.parentElement.querySelector('textarea');
  ta.select(); ta.setSelectionRange(0, 999999);
  const done = () => { btn.classList.add('done'); btn.textContent='✅ Đã copy'; 
    setTimeout(()=>{btn.classList.remove('done');btn.textContent='📋 Copy prompt';},1600); };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(ta.value).then(done).catch(()=>{ try{document.execCommand('copy');done();}catch(e){} });
  } else { try{document.execCommand('copy');done();}catch(e){} }
}
const drop=document.getElementById('drop'), fileInput=document.getElementById('file'), msg=document.getElementById('msg');
drop.onclick=()=>fileInput.click();
['dragenter','dragover'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.add('hot');}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.remove('hot');}));
drop.addEventListener('drop',ev=>sendFiles(ev.dataTransfer.files));
fileInput.onchange=()=>sendFiles(fileInput.files);
async function sendFiles(files){
  if(!files || !files.length) return;
  msg.innerHTML='';
  for(const f of files){
    if(!f.type.startsWith('image/')) continue;
    const b64 = await new Promise(res=>{const r=new FileReader();r.onload=()=>res(r.result.split(',')[1]);r.readAsDataURL(f);});
    msg.innerHTML += `<p class="muted">Đang tải ${f.name}…</p>`;
    try{
      const r = await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/json'},
        body: JSON.stringify({name:f.name, data:b64})});
      const j = await r.json();
      msg.innerHTML += j.ok ? `<p class="ok">✅ Đã nhận <b>${j.saved}</b></p>`
                            : `<p class="warn">⚠️ ${j.error||'lỗi'}</p>`;
    }catch(e){ msg.innerHTML += `<p class="warn">⚠️ Lỗi tải ${f.name}: ${e}</p>`; }
  }
  msg.innerHTML += '<p class="muted">Tải lại trang để xem danh sách "Ảnh đã nhận".</p>';
}
</script>
</body></html>"""


def keys_page(msg=""):
    env = load_env()
    keys_html = "".join(
        f'<label>{k}</label><input name="{k}" autocomplete="off" autocapitalize="off">' for k in FIELDS
    )
    return f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Cập nhật key</title>
<style>body{{font-family:-apple-system,sans-serif;background:#111a2b;color:#e8e6df;padding:20px;max-width:560px;margin:auto}}
label{{display:block;font-size:13px;color:#93a0b8;margin:14px 0 5px}}
input{{width:100%;padding:13px;border-radius:9px;border:1px solid #2b3b57;background:#0a1220;color:#e8e6df}}
button{{width:100%;margin-top:20px;padding:15px;border:0;border-radius:11px;font-size:16px;font-weight:600;
  background:linear-gradient(135deg,#f7b32b,#ffd166);color:#3a2600}}
.ok{{background:#12351f;border:1px solid #2f8f5a;padding:12px;border-radius:10px;color:#7fe0a8}}
a{{color:#6fe0c0}}</style></head><body>
<h1 style="font-size:18px;color:#ffd98a">Cập nhật key</h1>
{msg}
<form method="POST" action="/keys">{keys_html}<button type="submit">Lưu key</button></form>
<p><a href="/">← về Xưởng</a></p>
</body></html>"""


class H(BaseHTTPRequestHandler):
    def _send(self, body, code=200, ctype="text/html; charset=utf-8"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.startswith("/keys"):
            self._send(keys_page())
        elif self.path.startswith("/upload"):
            self._send(json.dumps({"ok": False, "error": "dùng POST"}), ctype="application/json")
        else:
            self._send(page())

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)
        if self.path.startswith("/upload"):
            try:
                j = json.loads(raw.decode())
                name = os.path.basename(j.get("name", "image.png")) or "image.png"
                if not re.search(r"\.(png|jpe?g|webp|gif)$", name, re.I):
                    name += ".png"
                data = base64.b64decode(j["data"])
                os.makedirs(UI_DIR, exist_ok=True)
                with open(os.path.join(UI_DIR, name), "wb") as f:
                    f.write(data)
                self._send(json.dumps({"ok": True, "saved": name}), ctype="application/json")
            except Exception as e:
                self._send(json.dumps({"ok": False, "error": str(e)}), ctype="application/json")
            return
        # /keys
        from urllib.parse import parse_qs
        data = parse_qs(raw.decode())
        env = load_env()
        for k in FIELDS:
            v = (data.get(k, [""])[0] or "").strip()
            if v:
                env[k] = v
        save_env(env)
        self._send(keys_page('<p class="ok">✅ Đã lưu key.</p>'))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Xưởng chạy tại http://0.0.0.0:12001")
    HTTPServer(("0.0.0.0", 12001), H).serve_forever()
