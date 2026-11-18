#!/usr/bin/env python3
"""Tạo nội dung bình luận báo cáo kết quả xử lý ảnh, để đăng lại trong Issue.

Đọc báo cáo JSON từ tools/xu_ly_inbox.py, in ra Markdown.
"""

from __future__ import annotations

import json
import os
import sys

REPO = "huuducbkb/game-hong-duc-lam"
XUONG = f"https://huuducbkb.github.io/{REPO.split('/')[1]}/xuong/"


def _dong_anh(x: dict) -> str:
    key = x.get("key") or "?"
    file = x.get("file") or ""
    cach = {"ai": "AI nhận diện", "ten-file": "theo tên file", "thu-muc": "theo thư mục"}.get(
        x.get("cach", ""), x.get("cach", ""))
    tin = x.get("do_tin_cay")
    them = f" · {tin}%" if tin else ""
    return f"| `{key}` | `{file}` | {cach}{them} |"


def tao_binh_luan(bc: dict) -> str:
    da_luu = bc.get("da_luu", [])
    can = bc.get("can_xac_nhan", [])
    bo = bc.get("bo_qua", [])
    ghep = bc.get("ghep", {})

    d = ["### 🖼️ Xưởng ảnh — kết quả xử lý", ""]

    if da_luu:
        d += [f"✅ **Đã nhận và ghép {len(da_luu)} ảnh vào game:**", "",
              "| ảnh | lưu là | cách nhận |", "|---|---|---|"]
        d += [_dong_anh(x) for x in da_luu]
        d += [""]
        if ghep:
            d += ["**Vị trí đã ghép:**", ""]
            for f, doan in ghep.items():
                d.append(f"- `{f}` → {', '.join(doan)}")
            d += [""]
        d += [f"Ảnh đã lên web sau khi deploy (khoảng 1–2 phút): "
              f"[mở game](https://huuducbkb.github.io/{REPO.split('/')[1]}/game/)", ""]

    if can:
        d += [f"⚠️ **{len(can)} ảnh chưa chắc chắn** — chưa ghép, cần bạn xác nhận:", ""]
        d += ["| ảnh | đoán là | tin cậy | ghi chú |", "|---|---|---|---|"]
        for x in can:
            d.append(f"| `{x.get('name','?')}` | `{x.get('key','—')}` | "
                     f"{x.get('do_tin_cay',0)}% | {x.get('ly_do','')[:80]} |")
        d += ["", "Bạn trả lời bình luận này cho biết ảnh nào thuộc mã nào, "
                  "hoặc tải lại ảnh vào đúng thư mục `xuong-inbox/<mã>/`.", ""]

    if bo:
        d += [f"❌ **{len(bo)} ảnh bị bỏ qua:**", ""]
        for x in bo:
            d.append(f"- `{x.get('name','?')}`: {x.get('ly_do','')}")
        d += [""]

    if not (da_luu or can or bo):
        d += ["Không tìm thấy ảnh nào trong nội dung này. "
              "Hãy kéo ảnh trực tiếp vào ô bình luận rồi gửi lại.", ""]

    d += ["---", "", f"📋 Danh sách prompt còn thiếu: [Xưởng ảnh]({XUONG})", "",
          "_Bình luận này do AI agent (OpenHands) tạo tự động._"]
    return "\n".join(d)


def main() -> int:
    if len(sys.argv) < 2:
        print("Dùng: bao_cao_issue.py <bao-cao.json>", file=sys.stderr)
        return 1
    with open(sys.argv[1], encoding="utf-8") as f:
        bc = json.load(f)
    print(tao_binh_luan(bc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
