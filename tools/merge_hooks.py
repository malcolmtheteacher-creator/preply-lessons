#!/usr/bin/env python3
"""Check bot hook files in bots/queue/hooks/done/ and merge into tools/interest/hooks.json.
Usage: python3 tools/merge_hooks.py        (reports problems, merges only clean files)"""
import glob, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(R, 'bots/queue/hooks')
CODES = set('MND WRK MON CRI HIS SCI TEC HLT SOC CUL TRV HOM STO FLM IDE REL FOD NAT NONE'.split())
KINDS = set('discuss story skills roleplay history film science profile exam grammar'.split())
BAD = re.compile(r'\b(lesson|teacher|student|malcolm|today|practise|learn about)\b', re.I)
out_p = os.path.join(R, 'tools/interest/hooks.json')
out = json.load(open(out_p)) if os.path.exists(out_p) else {}
for f in sorted(glob.glob(Q + '/done/batch_*.tsv')):
    b = os.path.basename(f)[:-4]
    ids = [x['id'] for x in json.load(open(os.path.join(Q, b + '.json')))]
    rows, errs = {}, []
    for n, l in enumerate(open(f, encoding='utf-8').read().splitlines(), 1):
        if not l.strip(): continue
        p = l.split('|')
        if len(p) != 4: errs.append('%d: not 4 fields' % n); continue
        i, t, k, h = [x.strip() for x in p]
        tc = t.split(',')
        if i not in ids: errs.append('%d: unknown id %s' % (n, i))
        if not all(c in CODES for c in tc) or len(tc) > 3: errs.append('%d: bad topics %s' % (n, t))
        if k not in KINDS: errs.append('%d: bad type %s' % (n, k))
        w = len(h.split())
        if not 5 <= w <= 18: errs.append('%d: hook length %d' % (n, w))
        if BAD.search(h): errs.append('%d: banned word' % n)
        rows[i] = {'t': tc, 'k': k, 'h': h}
    miss = [i for i in ids if i not in rows]
    if miss: errs.append('missing %d ids, e.g. %s' % (len(miss), miss[:3]))
    if errs: print(b, 'NEEDS FIXING:', *errs[:8], sep='\n  ')
    else: out.update(rows); print(b, 'ok', len(rows))
json.dump(out, open(out_p, 'w'), ensure_ascii=False)
print(len(out), 'hooks merged')
