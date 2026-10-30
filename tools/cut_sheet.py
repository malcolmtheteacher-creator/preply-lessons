#!/usr/bin/env python3
"""Cut one painted object sheet (magenta background) into journey/img/obj/<key>.png.
Usage: python3 tools/cut_sheet.py <sheet.png> <sheet number>
Objects and their order come from journey/objects.json. Rewrites journey/objects_ready.js."""
import json, os, sys
from PIL import Image, ImageFilter
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, n = sys.argv[1], int(sys.argv[2])
d = json.load(open(os.path.join(root, 'journey/objects.json')))
cols, rows = d['cols'], d['rows']
im = Image.open(src).convert('RGB'); W, H = im.size; px = im.load()
out = Image.new('RGBA', (W, H)); op = out.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]; m = min(r, b) - g
        al = 0 if m >= 110 else 255 if m <= 50 else int(255 * (110 - m) / 60)
        if 0 < al < 255:
            e = min(r, b) - g
            if e > 0: r, b = max(r - e, 0), max(b - e, 0)
        op[x, y] = (r, g, b, al)
cw, ch = W / cols, H / rows

def keep_main(cell):
    # drop slivers of neighbouring objects: keep the biggest blob (parts close together count as one blob)
    a = cell.split()[3]
    m = a.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(15))
    w, h = m.size; mp = m.load(); lab = {}; best = (0, None); k = 0
    for y0 in range(h):
        for x0 in range(w):
            if mp[x0, y0] and (x0, y0) not in lab:
                k += 1; st = [(x0, y0)]; lab[(x0, y0)] = k; cnt = 0
                while st:
                    x, y = st.pop(); cnt += 1
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and mp[nx, ny] and (nx, ny) not in lab:
                            lab[(nx, ny)] = k; st.append((nx, ny))
                if cnt > best[0]: best = (cnt, k)
    keep = Image.new('L', (w, h), 0); kp = keep.load()
    for (x, y), l in lab.items():
        if l == best[1]: kp[x, y] = 255
    cell = cell.copy(); cell.putalpha(Image.composite(a, Image.new('L', (w, h), 0), keep))
    return cell
od = os.path.join(root, 'journey/img/obj'); os.makedirs(od, exist_ok=True)
for o in d['library']:
    if o['sheet'] != n: continue
    c, rw = o['cell'] % cols, o['cell'] // cols
    cell = out.crop((int(c * cw), int(rw * ch), int((c + 1) * cw), int((rw + 1) * ch)))
    cell = keep_main(cell)
    bb = cell.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bb: print('EMPTY', o['key']); continue
    cell = cell.crop(bb); s = 224 / max(cell.size)
    cell = cell.resize((max(1, round(cell.width * s)), max(1, round(cell.height * s))), Image.LANCZOS)
    can = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    can.paste(cell, ((256 - cell.width) // 2, (256 - cell.height) // 2), cell)
    can.save(os.path.join(od, o['key'] + '.png'), optimize=True)
keys = {o['key'] for o in d['library']}
ready = sorted(k for k in keys if os.path.exists(os.path.join(od, k + '.png')))
open(os.path.join(root, 'journey/objects_ready.js'), 'w').write(
    'window.OBJ_READY=' + json.dumps({k: 1 for k in ready}) + ';window.OBJ_MAP=' + json.dumps(d['map'], separators=(',', ':')) + ';')
print(len(ready), 'objects ready')

import subprocess, sys
subprocess.run([sys.executable, os.path.join(root, 'tools/match_objects.py')])
