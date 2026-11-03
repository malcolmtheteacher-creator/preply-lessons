#!/usr/bin/env python3
"""Remove a flat (any colour) background: colour is read from the corners, only background
connected to the image edge is removed, edges are feathered and de-fringed.
Usage: python3 tools/key_flat.py in.png out.png [tolerance]"""
import sys
from collections import deque
from PIL import Image, ImageFilter

def key(im, tol=60):
    im = im.convert('RGB'); w, h = im.size; px = im.load()
    pts = [px[x, y] for x in list(range(12)) + list(range(w - 12, w)) for y in list(range(12)) + list(range(h - 12, h))]
    bg = tuple(sorted(p[i] for p in pts)[len(pts) // 2] for i in range(3))
    def dist(p): return ((p[0] - bg[0]) ** 2 + (p[1] - bg[1]) ** 2 + (p[2] - bg[2]) ** 2) ** .5
    hard = tol; seen = bytearray(w * h); q = deque()
    for x in range(w):
        for y in (0, h - 1): q.append((x, y))
    for y in range(h):
        for x in (0, w - 1): q.append((x, y))
    while q:
        x, y = q.popleft(); i = y * w + x
        if seen[i]: continue
        if dist(px[x, y]) >= hard: continue
        seen[i] = 1
        if x: q.append((x - 1, y))
        if y: q.append((x, y - 1))
        if x < w - 1: q.append((x + 1, y))
        if y < h - 1: q.append((x, y + 1))
    m = Image.new('L', (w, h)); m.putdata([255 if s else 0 for s in seen])      # 255 = background
    grow = m.filter(ImageFilter.MaxFilter(7))                                     # band around background
    out = Image.new('RGBA', (w, h)); op = out.load(); mp = m.load(); gp = grow.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if mp[x, y]: op[x, y] = (r, g, b, 0); continue
            if gp[x, y]:
                d = dist((r, g, b)); a = max(0.0, min(1.0, (d - tol * .55) / (tol * .9)))
                f = (1 - a) * .7
                r, g, b = [max(0, min(255, int((c - bgc * f) / (1 - f)))) for c, bgc in zip((r, g, b), bg)]
                op[x, y] = (r, g, b, int(255 * a))
            else: op[x, y] = (r, g, b, 255)
    return out, bg

if __name__ == '__main__':
    o, bg = key(Image.open(sys.argv[1]), float(sys.argv[3]) if len(sys.argv) > 3 else 60)
    o.save(sys.argv[2]); print(sys.argv[1], 'bg', bg)
