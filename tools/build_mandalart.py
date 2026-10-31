#!/usr/bin/env python3
"""Build the mandalart map (map.html): every lesson on the site in a tree of 3x3 boxes, max 8 children per box.
Usage: python3 tools/build_mandalart.py [outfile]"""
import html, json, os, re, sys, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()
def raw(s, tok):
    i = s.index(tok) + len(tok); return json.JSONDecoder().raw_decode(s[i:])[0]
ALL = raw(rd('wordbank/all_lessons.js'), 'window.WBALL=')           # id -> [title, level, series]
EXP = raw(rd('explore_data.js'), 'window.EXPLORE=')                # id,title,level,codes,type,hook
OLD = raw(open('/tmp/w_old.html', encoding='utf-8').read(), 'var W=') if os.path.exists('/tmp/w_old.html') else None

def trim(t, n=26):
    t = re.sub(r'\s+', ' ', html.unescape(t)).strip(); return t if len(t) <= n else t[:n - 1].rstrip() + '…'
def leaf(id_, title, level='', sub=''):
    return {'t': title, 's': sub, 'i': '', 'h': id_ + '.html', 'l': level, 'k': []}
def lesson(id_):
    a = ALL.get(id_)
    return leaf(id_, a[0] if a else id_.replace('_', ' '), a[1] if a else '') if os.path.exists(os.path.join(ROOT, id_ + '.html')) else None
def count(n): return 1 if not n['k'] else sum(count(c) for c in n['k'])
def chunk(kids, cap=8):
    if len(kids) <= cap: return kids
    size = math.ceil(len(kids) / cap); out = []
    for i in range(0, len(kids), size):
        g = kids[i:i + size]
        if len(g) == 1: out.append(g[0]); continue
        out.append({'t': trim(g[0]['t'], 15) + ' … ' + trim(g[-1]['t'], 15), 's': '%d lessons' % sum(count(x) for x in g), 'i': '', 'h': '', 'l': '', 'k': chunk(g, cap)})
    return out
def group(t, s, img, kids, page=''):
    t = html.unescape(t)
    kids = list(kids)
    if page: kids = [{'t': 'Open the full page', 's': t, 'i': '', 'h': page, 'l': '', 'k': [], 'pg': 1}] + kids
    return {'t': t, 's': s, 'i': img, 'h': '', 'l': '', 'k': chunk(kids, 8)}
def lessons_of_page(p):
    if not os.path.exists(os.path.join(ROOT, p)): return []
    d = rd(p); ids = []
    for x in re.findall(r'href="([^"#?]+)\.html', d):
        if x.startswith('http') or 'dashboard' in x.lower() or x in ids: continue
        ids.append(x)
    return [l for l in (lesson(x) for x in ids) if l]

REG = {'professional': ('Professional English', 'English for work', 'journey/world/region_professional.jpg'),
       'academic': ('Academic English & exams', 'IELTS, Cambridge, scholarship', 'journey/world/region_academic.jpg'),
       'general': ('General English', 'from first words to mastery', 'journey/world/region_general.jpg'),
       'explore': ('Explore by interest', 'follow your curiosity', 'journey/world/region_explore.jpg'),
       'palace': ('The Palace of Subjects', 'every subject, shelf by shelf', 'journey/world/region_palace.jpg'),
       'comics': ('Comics & guides', 'stories in pictures', 'journey/world/region_comics.jpg'),
       'words': ('My Words & My Room', 'your progress', 'journey/world/region_words.jpg'),
       'library': ('The Library', 'every lesson, 79 collections', 'journey/world/region_library.jpg')}
def route(r):
    R = raw(rd('journey_%s.html' % r), 'var R=')
    t, s, img = REG[r]; goals = []
    for key, gt, gd in R['goals']:
        cards = []
        for c in R['cards']:
            if c['goal'] != key: continue
            ls = [l for l in (lesson(i) for i in c['ids']) if l] or lessons_of_page(c['href'])
            cards.append(group(c['name'], c['meta'] or c['desc'][:40], '', ls, c['href']) if ls else leaf(c['href'][:-5], c['name'], c['level'], c['meta']))
        gimg = 'journey/routes/route_%s_%s.jpg' % (r, key if os.path.exists(os.path.join(ROOT, 'journey/routes/route_%s_%s.jpg' % (r, key))) else 'hero')
        if not os.path.exists(os.path.join(ROOT, gimg)):   # keys differ (e.g. finding_voice): try prefix match
            g2 = [f for f in os.listdir(os.path.join(ROOT, 'journey/routes')) if f.startswith('route_%s_' % r) and key.split('_')[0] in f]
            gimg = 'journey/routes/' + (g2[0] if g2 else 'route_%s_hero.jpg' % r)
        goals.append(group(gt, gd[:50], gimg, cards, 'journey_%s.html?goal=%s' % (r, key)))
    return group(t, s, img, goals, 'journey_%s.html' % r)
def explore():
    t, s, img = REG['explore']; names = {}
    if OLD:
        for n in OLD['nodes']:
            if n['id'].startswith('ex_'): names[n['id'][3:]] = n['t']
    by = {}
    for e in EXP:
        if os.path.exists(os.path.join(ROOT, e[0] + '.html')): by.setdefault(e[3][0] if e[3] else 'X', []).append(leaf(e[0], e[1], e[2], e[5][:60]))
    topics = [group(names.get(c, c), '%d lessons' % len(v), 'explore_img/%s.jpg' % c if os.path.exists(os.path.join(ROOT, 'explore_img/%s.jpg' % c)) else '', v) for c, v in sorted(by.items(), key=lambda x: -len(x[1])) if c in names]
    return group(t, s, img, chunk(topics), 'explore.html')
def palace():
    t, s, img = REG['palace']; kids = []
    for n in OLD['nodes']:
        if n.get('p') == 'palace':
            ls = lessons_of_page(n['h_']); kids.append(group(n['t'], n.get('s', ''), n.get('i') or '', ls, n['h_']) if ls else leaf(n['h_'][:-5], n['t'], '', n.get('s', '')))
    return group(t, s, img, kids)
def small(r, p):
    t, s, img = REG[r]; kids = []
    for n in OLD['nodes']:
        if n.get('p') == p: kids.append({'t': n['t'], 's': n.get('s', ''), 'i': n.get('i') or '', 'h': n['h_'], 'l': '', 'k': []})
    return group(t, s, img, kids)
def library():
    t, s, img = REG['library']; cols = []
    for b in OLD['libs']:
        ls = [l for l in (lesson(x[0]) for x in b['ls']) if l]
        if ls: cols.append(group(b['n'], '%d lessons' % len(ls), b.get('i') or '', ls))
    return group(t, s, img, chunk(cols))
top = {'t': 'English, taught through stories', 's': '', 'i': 'journey/world/region_hub.jpg', 'h': '', 'l': '',
       'k': [route('professional'), route('academic'), route('general'), explore(), palace(), small('comics', 'comics'), small('words', 'words'), library()]}
# order: clockwise-ish to match the 3x3 positions (TL,T,TR,L,R,BL,B,BR)
o = {x['t']: x for x in top['k']}
top['k'] = [o[REG[k][0]] for k in ('professional', 'academic', 'general', 'library', 'explore', 'palace', 'comics', 'words')]
def depth(n): return 1 + max([depth(c) for c in n['k']] or [0])
tpl = rd('tools/mandalart_template.html')
out = sys.argv[1] if len(sys.argv) > 1 else 'map.html'
open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(tpl.replace('__TREE__', json.dumps(top, ensure_ascii=False, separators=(',', ':'))))
print(out, 'lessons reachable:', count(top), 'depth:', depth(top))
