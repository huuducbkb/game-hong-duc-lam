#!/usr/bin/env python3
"""Sinh tài liệu đối chiếu giọng kể NPC theo 6 mức hảo cảm từ dữ liệu chương.

Tài liệu sinh ra luôn khớp với game/chapters/*.json — không sửa tay bản .md.
"""
import io
import json
import os

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THU_TU_MUC = ['tử địch', 'thù địch', 'người dưng', 'quen biết', 'thân thiết', 'tri kỷ']
MO_TA_MUC = {
    'tử địch': 'coi ngươi là mối nguy phải giết, không chia sẻ gì',
    'thù địch': 'khinh, không giúp, cắt liên lạc',
    'người dưng': 'không quen, không nợ, đường ai nấy đi',
    'quen biết': 'bắt đầu trao đổi, còn tính toán',
    'thân thiết': 'chủ động giúp, không đòi lại',
    'tri kỷ': 'nói thật chỗ yếu nhất của mình, cho không tính lời',
}
NPC = [
    ('Hàn Lập', 'HÀN LẬP'),
    ('Tuyết Cơ', 'TUYẾT CƠ'),
    ('Hồng Trần', 'KIẾM LINH HỒNG TRẦN'),
]


def doc_doan():
    doan = {}
    for so in (1, 2):
        duong = os.path.join(GOC, 'game', 'chapters', f'chuong{so}.json')
        with io.open(duong, encoding='utf-8') as f:
            for x in json.load(f)['doan']:
                doan[x['id']] = (so, x)
    return doan


def sinh():
    doan = doc_doan()
    ra = []
    ra.append('# HỒNG ĐỨC TU TIÊN LỘ — GIỌNG KỂ NPC THEO 6 MỨC HẢO CẢM\n')
    ra.append('Tài liệu sinh tự động từ `game/chapters/chuong1.json` và `chuong2.json` '
              'bằng `tools/tao_tai_lieu_giong_npc.py`. Sửa truyện thì chạy lại tool, '
              'đừng sửa tay file này.\n')
    ra.append('Mỗi mức hảo cảm là một cách đối xử khác nhau, không chỉ là lời miêu tả khác nhau.\n')
    ra.append('| Mức | Khoảng điểm | Cách NPC đối xử |')
    ra.append('|---|---|---|')
    for ten, khoang in zip(THU_TU_MUC, ['−100 … −60', '−59 … −20', '−19 … 19',
                                       '20 … 49', '50 … 79', '80 … 100']):
        ra.append(f'| **{ten}** | {khoang} | {MO_TA_MUC[ten]} |')
    ra.append('')

    for npc, tieu_de in NPC:
        ds = [(k, v) for k, v in doan.items()
              if any(b['npc'] == npc for b in (v[1].get('bien_the') or []))]
        if not ds:
            continue
        ds.sort(key=lambda kv: (kv[1][0], kv[0]))
        ra.append(f'\n---\n\n# {tieu_de}\n')
        for so_thu_tu, (ma, (chuong, x)) in enumerate(ds, 1):
            cac_muc = {b['muc']: b['ke'] for b in x['bien_the'] if b['npc'] == npc}
            co = [m for m in THU_TU_MUC if m in cac_muc]
            thieu = [m for m in THU_TU_MUC if m not in cac_muc]
            ra.append(f'## {so_thu_tu}. `[{ma}]` · Chương {chuong} — {x.get("boi_canh") or "?"}\n')
            ra.append(f'Có {len(co)}/6 mức: {", ".join(co)}.')
            if thieu:
                ra.append(f' **Còn thiếu:** {", ".join(thieu)}.')
            ra.append('')
            ra.append('<details><summary>Bản gốc (dùng khi chưa có biến thể)</summary>\n')
            ra.append(x['ke'].strip())
            ra.append('\n</details>\n')
            for muc in co:
                ra.append(f'### Mức “{muc}”\n')
                ra.append(cac_muc[muc].strip())
                ra.append('')
            for lc in (x.get('lua_chon') or []):
                pass
    return '\n'.join(ra) + '\n'


if __name__ == '__main__':
    noi_dung = sinh()
    for ten in os.listdir(GOC):
        if ten.endswith('.md') and 'Tu_Tie' in ten:
            os.remove(os.path.join(GOC, ten))
    duong = os.path.join(GOC, 'TAI_LIEU_GIONG_NPC_6_MUC.md')
    with io.open(duong, 'w', encoding='utf-8') as f:
        f.write(noi_dung)
    print(f'da ghi {duong} ({len(noi_dung)} ky tu)')
