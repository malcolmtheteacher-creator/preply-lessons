#!/usr/bin/env python3
"""Check bot vocabulary files in bots/queue/vocab/done/ and merge the clean ones into
wordbank/extra_words.json, which tools/build_wordbank.py adds to My Words (no lesson page is edited).
Usage: python3 tools/merge_vocab.py"""
import glob, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(R, 'bots/queue/vocab')
OUT = os.path.join(R, 'wordbank/extra_words.json')
POS = set('n v adj adv phr v prep conj phr'.split()) | {'phr v'}
BAD = re.compile(r'\b(lesson|teacher|student|malcolm)\b', re.I)
def repeats(w, d):
    dl = d.lower()
    if re.search(r'\b' + re.escape(w) + r'(s|es|ed|d|ing)?\b', dl): return True
    big = [x for x in w.split() if len(x) >= 5]
    return len(w.split()) > 1 and len(big) >= 2 and all(re.search(r'\b' + re.escape(x), dl) for x in big)


out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
for f in sorted(glob.glob(Q + '/done/batch_*.tsv')):
    b = os.path.basename(f)[:-4]
    ids = [x['id'] for x in json.load(open(os.path.join(Q, b + '.json'), encoding='utf-8'))]
    lessons, errs = {}, []
    for n, l in enumerate(open(f, encoding='utf-8').read().splitlines(), 1):
        if not l.strip(): continue
        p = [x.strip() for x in l.split('|')]
        if len(p) != 5: errs.append('%d: not 5 fields' % n); continue
        i, w, pos, d, ex = p
        if i not in ids: errs.append('%d: unknown id %s' % (n, i)); continue
        if w == 'NONE': lessons.setdefault(i, []); continue
        w = re.sub(r'^(to|a|an|the) ', '', w.lower())
        if not re.fullmatch(r"[a-zé0-9][a-zé0-9' -]{0,38}[a-zé0-9]", w) or len(w.split()) > 4: errs.append('%d: bad word %r' % (n, w)); continue
        if pos not in POS: errs.append('%d: bad pos %r' % (n, pos)); continue
        if not 4 <= len(d.split()) <= 20: errs.append('%d: definition length' % n); continue
        if repeats(w, d): errs.append('%d: definition contains the word %r' % (n, w)); continue
        if not 5 <= len(ex.split()) <= 22: errs.append('%d: example length' % n); continue
        if BAD.search(d + ' ' + ex): errs.append('%d: banned word' % n); continue
        lessons.setdefault(i, []).append({'w': w, 'pos': pos, 'def': d, 'ex': ex})
    for i in ids:
        ws = lessons.get(i)
        if ws is None: errs.append('lesson %s missing' % i)
        elif ws and not 3 <= len(ws) <= 12: errs.append('lesson %s has %d words' % (i, len(ws)))
    if errs: print(b, 'NEEDS FIXING (%d):' % len(errs), *errs[:8], sep='\n  ')
    else:
        out.update({i: ws for i, ws in lessons.items() if ws}); print(b, 'ok', sum(1 for w in lessons.values() if w), 'lessons with words')
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out), 'lessons in extra_words.json')
