#!/usr/bin/env python3
"""Cut a bot's 6x6 picture sheets (journey/incoming/words7/<bot>_sheet_0N.png, list bots/queue/words/done/<bot>_0N.txt,
'-' = blank cell) into wordbank/pics/<word>.png and add them to wordbank/pics.js.
Usage: python3 tools/cut_words7.py folio [rows_sheet1 rows_sheet2]   (rows default 6)"""
import os, sys, json
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, 'tools'))
from key_flat import key
from PIL import Image
def clean(cell):
    cell, bg = key(cell, 95)                       # flood from the cell edge, so neighbours' crumbs and the shadow go
    px = cell.load(); w, h = cell.size
    for y in range(h):                             # pockets of background trapped inside the object
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and ((r - bg[0]) ** 2 + (g - bg[1]) ** 2 + (b - bg[2]) ** 2) ** .5 < 55: px[x, y] = (r, g, b, 0)
    a = cell.split()[3]                            # keep only the biggest piece
    seen = bytearray(w * h); best = []; ap = a.load()
    for sy in range(h):
        for sx in range(w):
            if seen[sy * w + sx] or ap[sx, sy] < 40: continue
            comp = [(sx, sy)]; seen[sy * w + sx] = 1; i = 0
            while i < len(comp):
                x, y = comp[i]; i += 1
                for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny*w+nx] and ap[nx, ny] >= 40:
                        seen[ny*w+nx] = 1; comp.append((nx, ny))
            if len(comp) > len(best): best = comp
    keep = set(best); out = cell.copy(); op = out.load()
    for y in range(h):
        for x in range(w):
            if (x, y) not in keep: op[x, y] = (0, 0, 0, 0)
    return out

bot = sys.argv[1]; rows = [int(x) for x in sys.argv[2:]] or [6, 6]
od = os.path.join(root, 'wordbank/pics'); os.makedirs(od, exist_ok=True)
s = open(os.path.join(root, 'wordbank/words.js')).read()
words = set(json.loads(s[s.index('{'):s.rindex('}') + 1])['words'])
ps = open(os.path.join(root, 'wordbank/pics.js')).read()
m = json.loads(ps[ps.index('{'):ps.rindex('}') + 1])
for n, nr in zip((1, 2), rows):
    names = [l.strip() for l in open(os.path.join(root, 'bots/queue/words/done/%s_0%d.txt' % (bot, n))) if l.strip()]
    raw = Image.open(os.path.join(root, 'journey/incoming/words7/%s_sheet_0%d.png' % (bot, n))).convert('RGB')
    W, H = raw.size; cw, ch = W / 6, H / 6
    for i, k in enumerate(names[:nr * 6]):
        if k.startswith('-'): continue
        c, r = i % 6, i // 6
        cell = raw.crop((int(c * cw) + 3, int(r * ch) + 3, int((c + 1) * cw) - 3, int((r + 1) * ch) - 3))
        cell = clean(cell)
        bb = cell.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
        if not bb: print('EMPTY', k); continue
        cell = cell.crop(bb); sc = 150 / max(cell.size)
        cell = cell.resize((max(1, round(cell.width * sc)), max(1, round(cell.height * sc))), Image.LANCZOS)
        can = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); can.paste(cell, ((160 - cell.width) // 2, (160 - cell.height) // 2), cell)
        can.save(os.path.join(od, k + '.png'), optimize=True)
        if k in words: m[k] = k
        else: print('not in My Words:', k)
open(os.path.join(root, 'wordbank/pics.js'), 'w').write('window.WORD_PICS=' + json.dumps(m, sort_keys=True) + ';')
print(len(m), 'words now have a picture')
