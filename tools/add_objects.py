#!/usr/bin/env python3
"""Register the objects in tools/new_objects.txt in journey/objects.json (sheets 11+, 36 per sheet)
and write their Grok prompts to JOURNEY_OBJECT_SHEETS_NEW.md. Safe to re-run."""
import json, re, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
o = json.load(open(root + '/journey/objects.json'))
lib = [x for x in o['library'] if x['sheet'] <= 10]
new = []
for ln in open(root + '/tools/new_objects.txt'):
    if ln.strip() and not ln.startswith('#'):
        k, name, _ = [x.strip() for x in ln.split(' :: ')]
        new.append((k, name))
for i, (k, name) in enumerate(new):
    lib.append({'key': k, 'name': name, 'sheet': 11 + i // 36, 'cell': i % 36})
o['library'] = lib
json.dump(o, open(root + '/journey/objects.json', 'w'), indent=1, ensure_ascii=False)
src = open(root + '/JOURNEY_OBJECT_SHEETS.md').read()
tpl = re.search(r'## Sheet 03.*?```(?:\w*)\n(.*?)```', src, re.S).group(1)
ref = 'The attached image is one of my painted rooms. Use it only as the reference for painting style, lighting and colour richness.'
tpl = re.sub(r'\[Attached[^\n]*\]', ref, tpl)
out = ''
for s in range(11, 11 + (len(new) + 35) // 36):
    objs = [x['name'] for x in lib if x['sheet'] == s]
    rows = '\n'.join('Row %d: %s.' % (r + 1, '; '.join(objs[r * 6:r * 6 + 6])) for r in range((len(objs) + 5) // 6))
    p = re.sub(r'The objects, left to right, top to bottom:\n.*?\n\n', 'The objects, left to right, top to bottom:\n' + rows + '\n\n', tpl, flags=re.S)
    p = p.replace('EXACTLY 36', 'EXACTLY %d' % len(objs))
    out += '---\n\n## Sheet %d\n\nFirst object (top-left): %s\n\n```\n%s\n```\n\n' % (s, objs[0], p.strip())
open(root + '/SHEETS_11_ON.md', 'w').write(out)
print(len(new), 'objects,', (len(new) + 35) // 36, 'sheets')
