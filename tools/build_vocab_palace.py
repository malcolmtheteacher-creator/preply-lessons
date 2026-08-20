import re, glob, html, json, os
os.chdir('/Users/malcolmtheteacher/Documents/01_Work/gitsite')
OUT='/private/tmp/claude-501/-Users-malcolmtheteacher/057736c5-600e-4489-a4ae-bd0984412182/scratchpad'

files = sorted(f for f in glob.glob('short_history_*.html')+glob.glob('techniques_*.html')
               if '_a2b1' not in f and 'dashboard' not in f)

SENT = re.compile(r'<div class="sent">(.*?)</div>', re.S)
MEAN = re.compile(r'<div class="meaning">(.*?)</div>', re.S)
HEAD = re.compile(r'^\s*<b>(.*?)</b>\s*(?:\(([^)]*)\))?\s*[—–-]\s*(.*)$', re.S)
FIELD = lambda c,k: (re.search(r'<div class="%s">(.*?)</div>'%k, c, re.S) or [None,''])[1]

def txt(s):
    s = re.sub(r'<br\s*/?>', ' ', s or '')
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

JUNK = re.compile(r'^\(?[a-z]\)?$|^\d+$', re.I)

def mask(cue, surface):
    if not cue or not surface: return cue
    if surface.lower() in cue.lower():
        # mask EVERY occurrence - collocation chips repeat the target and would leak it
        return re.sub(re.escape(surface), '_____', cue, flags=re.I)
    # inflected form in the example ("annihilate" -> "annihilated"): match on the stem
    core = re.sub(r'^(to|a|an|the)\s+', '', surface.lower()).strip()
    stem = core[:max(4, len(core)-3)]
    if len(stem) >= 4:
        out, n = re.subn(r'\b'+re.escape(stem)+r'\w*', '_____', cue, flags=re.I)
        if n: return out
    return cue

def drill_type(cue, masked):
    if not cue: return 'define'
    if '_____' in masked: return 'colloc' if '·' in cue else 'scene'
    return 'define'   # "(noun) ... Which word?" - a definition cue, no blank to fill

def split_items(s, cls):
    parts = s.split('<div class="%s"' % cls)[1:]
    return parts

rooms, skipped = [], []
for f in files:
    raw = open(f, encoding='utf-8', errors='replace').read()
    s = raw.replace('&mdash;','—').replace('&ndash;','–')
    body = s[s.find('<body'):]
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    title = txt(h1.group(1)) if h1 else f
    words, seen = [], set()

    for chunk in split_items(body, 'guess-item'):
        sm, mm = SENT.search(chunk), MEAN.search(chunk)
        if not (sm and mm): continue
        sent_html = sm.group(1)
        if re.search(r'—\s*from\s*<a', sent_html): continue      # review item, belongs to another room
        h = HEAD.match(mm.group(1).strip())
        if not h: continue
        word, pos, d = txt(h.group(1)), txt(h.group(2) or ''), txt(h.group(3))
        if not word or not d or word.lower() in seen: continue
        if JUNK.match(word) or len(word) < 3: continue
        surf = re.search(r'<b>(.*?)</b>', sent_html)
        surface = txt(surf.group(1)) if surf else word
        cue = re.sub(r'^\d+[.)]\s*', '', txt(sent_html))
        seen.add(word.lower())
        mk = mask(cue, surface)
        words.append(dict(w=word, pos=pos, d=d, s=surface, cue=cue, m=mk, ty=drill_type(cue, mk)))

    if not words:
        for chunk in split_items(body, 'vocab-card'):
            word, pos = txt(FIELD(chunk,'word')), txt(FIELD(chunk,'pos'))
            d, ex = txt(FIELD(chunk,'def')), txt(FIELD(chunk,'ex')).strip('"“” ')
            if not word or not d or word.lower() in seen: continue
            seen.add(word.lower())
            mk = mask(ex, word) if ex else ''
            words.append(dict(w=word, pos=pos, d=d, s=word, cue=ex, m=mk, ty=drill_type(ex, mk)))

    if not words:
        for chunk in split_items(body, 'vocab-card'):
            w = re.search(r'<span class="word">(.*?)</span>', chunk, re.S)
            dfn = re.search(r'<span class="definition">(.*?)</span>', chunk, re.S)
            if not (w and dfn): continue
            word = txt(w.group(1))
            d = re.sub(r'^\s*'+re.escape(word)+r'\s*[—–-]\s*', '', txt(dfn.group(1)), flags=re.I)
            if not word or not d or word.lower() in seen: continue
            seen.add(word.lower())
            words.append(dict(w=word, pos='', d=d, s=word, cue='', m='', ty='define'))

    if len(words) < 4:
        skipped.append((f, len(words))); continue
    rooms.append(dict(f=f, t=title, fam='history' if f.startswith('short_history_') else 'story', words=words))

print(f"rooms: {len(rooms)}   words: {sum(len(r['words']) for r in rooms)}")
print(f"still skipped: {len(skipped)} -> {skipped}")
nocue = sum(1 for r in rooms for w in r['words'] if w['m']==w['cue'])
print(f"words whose cue could not be masked: {nocue}")
json.dump(rooms, open(OUT+'/bank.json','w'), ensure_ascii=False)
