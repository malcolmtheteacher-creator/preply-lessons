#!/usr/bin/env python3
"""Cut Lexi's picture-word sheets (flat coloured background, 6x6) into wordbank/pics/<key>.png and
write wordbank/pics.js (word -> picture key) for every word in wordbank/words.js that matches.
Usage: python3 tools/cut_words.py"""
import os, sys, json, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, 'tools'))
from key_flat import key
from PIL import Image
items = []
for ln in open(os.path.join(root, 'tools/words_items.txt')):
    if ln.startswith('#') or '::' not in ln: continue
    k, a = ln.split('::'); items.append((k.strip(), [x.strip().lower() for x in a.split(',') if x.strip()]))
assert len(items) == 72, len(items)
od = os.path.join(root, 'wordbank/pics'); os.makedirs(od, exist_ok=True)
for n in (1, 2):
    im, bg = key(Image.open(os.path.join(root, 'journey/incoming/lexi/words_sheet_0%d.png' % n)), 70)
    W, H = im.size; cw, ch = W / 6, H / 6
    for i, (k, _) in enumerate(items[(n - 1) * 36:n * 36]):
        if k.startswith('-'): continue
        c, r = i % 6, i // 6
        cell = im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))
        bb = cell.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
        if not bb: print('EMPTY', k); continue
        cell = cell.crop(bb); s = 150 / max(cell.size)
        cell = cell.resize((max(1, round(cell.width * s)), max(1, round(cell.height * s))), Image.LANCZOS)
        can = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); can.paste(cell, ((160 - cell.width) // 2, (160 - cell.height) // 2), cell)
        can.save(os.path.join(od, k + '.png'), optimize=True)
s = open(os.path.join(root, 'wordbank/words.js')).read()
words = set(json.loads(s[s.index('{'):s.rindex('}') + 1])['words'])
m = {}
for k, al in items:
    if k.startswith('-'): continue
    for w in [k] + al:
        if w in words: m[w] = k
open(os.path.join(root, 'wordbank/pics.js'), 'w').write('window.WORD_PICS=' + json.dumps(m, sort_keys=True) + ';')
print(len(m), 'words now have a picture')
