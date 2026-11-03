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
    t = re.sub(r'\s+', ' ', html.unescape(t)).strip(); 
    if len(t) <= n: return t
    c = t[:n - 1]; c = c[:c.rfind(' ')] if ' ' in c[n // 2:] else c
    return c.rstrip(' ,;:-—') + '…'
def leaf(id_, title, level='', sub=''):
    return {'t': trim(title, 70), 's': sub, 'i': '', 'h': id_ + '.html', 'l': level, 'k': []}
def lesson(id_):
    if 'index' in id_ or id_.startswith(('journey', 'wordbank', 'explore', 'malcolm')): return None
    a = ALL.get(id_)
    return leaf(id_, a[0] if a else id_.replace('_', ' '), a[1] if a else '') if os.path.exists(os.path.join(ROOT, id_ + '.html')) else None
def count(n): return 1 if not n['k'] else sum(count(c) for c in n['k'])
def short(t, n=20):
    t = re.sub(r'[^\w\s&\'’?!.,:;/()\-—–·]+', '', html.unescape(t)).strip()
    t = re.sub(r'^\d+\s*[·.:)-]\s*', '', t).strip()
    if ':' in t: t = t.split(':', 1)[1].strip() or t
    parts = re.split(r' [-—] ', t)
    t = (parts[1] if len(parts) > 1 and re.match(r'^(Lesson|Part|Module|Unit|Week)\s*\d+$', parts[0].strip(), re.I) else parts[0]).strip()
    t = re.sub(r'^(The|A|An) ', '', t) if len(t) > n else t
    return t if len(t) <= n else t[:n - 1].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
def names(g, cap=96):
    out = ''
    for x in g:
        n = short(x['t'], 22); nxt = (out + ' · ' + n) if out else n
        if len(nxt) > cap: return out + ' …'
        out = nxt
    return out
def chunk(kids, cap=8, off=0):
    if len(kids) <= cap: return kids
    if len(kids) <= 2 * cap:
        rest = kids[cap - 1:]
        what = 'lessons' if all(not x['k'] for x in rest) else 'scenarios' if all(x.get('s') == 'two levels' for x in rest) else 'collections'
        return kids[:cap - 1] + [{'t': '%s %d\u2060–\u2060%d' % (what.capitalize(), off + cap, off + len(kids)), 's': names(rest), 'i': '', 'h': '', 'l': '', 'k': rest}]
    size = math.ceil(len(kids) / cap); out = []
    for i in range(0, len(kids), size):
        g = kids[i:i + size]
        if len(g) == 1: out.append(g[0]); continue
        what = 'Lessons' if all(not x['k'] for x in g) else 'Scenarios' if all(x.get('s') == 'two levels' for x in g) else 'Collections'
        out.append({'t': '%s %d\u2060–\u2060%d' % (what, off + i + 1, off + i + len(g)), 's': names(g), 'i': g[0].get('i', ''), 'h': '', 'l': '', 'k': chunk(g, cap, off + i)})
    return out
def slug(t): return re.sub(r'[^a-z0-9]+', '_', html.unescape(t).lower()).strip('_')[:50]
def mapimg(t):
    for e in ('jpg', 'png'):
        if os.path.exists(os.path.join(ROOT, 'journey/map/%s.%s' % (slug(t), e))): return 'journey/map/%s.%s' % (slug(t), e)
    return ''
def merge_levels(kids):
    hs = {k['h']: k for k in kids if not k['k']}; drop = set()
    for h, lo in hs.items():
        if not h.endswith('_a2b1.html'): continue
        base = h[:-len('_a2b1.html')]
        for hi in (base + '.html', base + '_b2c1.html', base + '_c1.html'):
            if hi in hs and h in rd(hi):   # the higher page links to its A2/B1 version, so one box is enough
                hs[hi]['l'] = 'A2/B1 · B2/C1'; drop.add(h); break
    return [k for k in kids if k['h'] not in drop or k['k']]
def group(t, s, img, kids, page=''):
    t = html.unescape(t)
    img = mapimg(t) or img
    kids = merge_levels(list(kids))
    return {'t': t, 's': s, 'i': img, 'h': '', 'l': '', 'k': chunk(kids, 8)}
def lessons_of_page(p):
    if not os.path.exists(os.path.join(ROOT, p)): return []
    d = rd(p); ids = []
    for x in re.findall(r'href="([^"#?]+)\.html', d):
        if x.startswith('http') or 'dashboard' in x.lower() or x in ids or 'index' in x or '/' in x or x.startswith(('journey', 'wordbank', 'explore', 'malcolm')): continue
        ids.append(x)
    if len(ids) < 3:   # dashboards that keep their lesson list in script data, not links
        for x in re.findall(r'[A-Za-z0-9][A-Za-z0-9_\-]*_[A-Za-z0-9_\-]+', d):
            if x not in ids and 'dashboard' not in x.lower() and os.path.exists(os.path.join(ROOT, x + '.html')) and x + '.html' != p: ids.append(x)
    return [l for l in (lesson(x) for x in ids) if l]

REG = {'professional': ('Professional English', 'English for work', 'journey/world/region_professional.jpg'),
       'academic': ('Academic English & exams', 'IELTS, Cambridge, scholarship', 'journey/world/region_academic.jpg'),
       'general': ('General English', 'from first words to mastery', 'journey/world/region_general.jpg'),
       'explore': ('Explore by interest', 'follow your curiosity', 'journey/world/region_explore.jpg'),
       'palace': ('The Palace of Subjects', 'every subject, shelf by shelf', 'journey/world/region_palace.jpg'),
       'comics': ('Comics & guides', 'stories in pictures', 'journey/world/region_comics.jpg'),
       'words': ('My Words & My Room', 'your progress', 'journey/world/region_words.jpg'),
       'library': ('The Library', 'every lesson, 79 collections', 'journey/world/region_library.jpg')}
def ielts_route():
    d = rd('ielts_route.html'); stages = []
    def steps(b):
        out = []
        for h, t in re.findall(r'<a class="step-body" href="([^"#?]+)\.html"><span class="step-t">(.*?)</span>', b, re.S):
            if os.path.exists(os.path.join(ROOT, h + '.html')) and not any(x['h'] == h + '.html' for x in out): out.append(leaf(h, re.sub(r'\s*★.*$', '', re.sub(r'<[^>]+>', '', html.unescape(t))).strip()))
        return out
    for m in re.finditer(r'<section class="stage-sec" id="s(\d)".*?</section>', d, re.S):
        b = m.group(0); n = m.group(1)
        name = html.unescape(re.search(r'<h2>(.*?)</h2>', b).group(1)); wk = re.search(r'class="weeks">(.*?)<', b).group(1)
        t = '%s · %s' % (n, name)
        if '<div class="group"' in b and len(re.findall(r'<div class="group"', b)) >= 5:
            kids = [group(html.unescape(re.search(r'<h3[^>]*>(.*?)</h3>', g).group(1)), '', '', steps(g)) for g in re.split(r'<div class="group"', b)[1:]]
            kids = [k for k in kids if k['k']]
        else: kids = steps(b)
        if len(kids) == 1 and not kids[0]['k']: kids[0].update(t=t, s=wk); stages.append(kids[0])
        else: stages.append(group(t, wk, '', kids))
    return group('The IELTS Route', 'one path, five stages, from diagnostic to mock', 'journey/map/ielts_route.jpg', stages)
def listening_group():
    lv = {}
    for f in sorted(os.listdir(os.path.join(ROOT, 'listening'))):
        if not f.endswith('.html'): continue
        m = re.match(r'(B1|B2|C1)_Lesson_(\d+)', f)
        if not m: continue
        tt = re.search(r'<title>([^<]*)', rd('listening/' + f)); t = html.unescape(tt.group(1)).strip() if tt else f[:-5].replace('_', ' ')
        t = re.sub(r'^.*?(Lesson \d+)\s*[:·-]\s*', '', t) if 'Lesson' in t else t
        lv.setdefault(m.group(1), []).append(leaf('listening/' + f[:-5], '%s · %s' % (m.group(2), short(t, 34)), m.group(1)))
    return group('Listening Practice', '9 lessons, B1 to C1', mapimg('Listening Practice'), [group('Level %s' % k, '3 lessons', '', v) for k, v in sorted(lv.items())])
def interview_route():
    S = raw(rd('interviews_dashboard.html'), 'var S='); stages = []
    for n, st in enumerate(S, 1):
        kids = [leaf(it['id'], '%d · %s' % (j, html.unescape(it['t']))) for j, it in enumerate(st['items'], 1) if os.path.exists(os.path.join(ROOT, it['id'] + '.html'))]
        if kids: stages.append(group('%d · %s' % (n, html.unescape(st['name'])), st.get('level', ''), '', kids))
    return group('Interview English', 'one path, from first answers to senior level', mapimg('Interview English') or 'journey/routes/route_professional_interviews.jpg', stages)
def speaking_route():
    d = rd('speaking_pathway_dashboard.html'); stages = []
    for n, part in enumerate(re.split(r'(?=<div class="level-header")', d)[1:], 1):
        nm = html.unescape(re.search(r'<h3>(.*?)</h3>', part).group(1)); lv = re.search(r'level-icon">(.*?)<', part).group(1)
        g = part.find('Grammar to feel'); pre = part[:g] if g > 0 else part
        kids = []
        for i, t in re.findall(r"location\.href='([^']+)\.html'\">.*?class=\"lesson-title\">(.*?)</", pre, re.S):
            if os.path.exists(os.path.join(ROOT, i + '.html')) and not any(k['h'] == i + '.html' for k in kids):
                kids.append(leaf(i, '%d · %s' % (len(kids) + 1, short(re.sub(r'<[^>]+>', '', html.unescape(t)).strip(), 36)), lv))
        if kids: stages.append(group('%d · %s' % (n, nm), '%s, %d lessons' % (lv, len(kids)), '', kids))
    return group('The Speaking Pathway', 'speak with confidence, from A2 to C2', mapimg('Speaking Pathway') or 'journey/routes/route_general_hero.jpg', stages)
def cambridge_route():
    d = rd('cambridge_exam_prep_dashboard.html'); stages = []
    for part in re.split(r'(?=<div class="pathway-section")', d)[1:]:
        h = re.search(r'<h2[^>]*>\s*Phase (\d+): (.*?)</h2>', part, re.S)
        if not h: continue
        kids = []
        for i, t in re.findall(r"openLesson\('([^'#?]+)\.html'\)\">.*?<h3>(.*?)</h3>", part, re.S):
            if os.path.exists(os.path.join(ROOT, i + '.html')) and not any(k['h'] == i + '.html' for k in kids):
                kids.append(leaf(i, '%d · %s' % (len(kids) + 1, re.sub(r'<[^>]+>', '', html.unescape(t)).strip())))
        if kids:
            nm = '%s · %s' % (h.group(1), html.unescape(h.group(2)).strip())
            if len(kids) == 1: kids[0].update(t=nm, s='1 lesson'); stages.append(kids[0])
            else: stages.append(group(nm, '%d lessons' % len(kids), '', kids))
    return group('The Cambridge Route', 'CAE: from orientation to the full test papers', mapimg('Cambridge Exam Prep') or 'journey/routes/route_academic_cambridge.jpg', stages)
NUM = ('interview', 'bootcamp', 'trade fair', 'storytelling', 'speaking pathway', 'pronunciation pathway', 'beyond perfect', 'commanding', 'a1 pathway', 'say it clearly', 'begin with the end', 'beginner course', 'speak first', 'spark to speech', 'stories (a1')
BEG = ['a1_can_cant_abilities','a1_my_daily_routine','a1_free_time_hobbies','a1_how_often','a1_when_do_you_do_it_part2','a1_who_do_you_do_it_with','a1_there_is_there_are','a1_present_continuous','a1_prepositions_of_place','a1_adjectives_describing_things','a1_making_suggestions','a1_simple_present_vs_present_continuous','a1_food_eating_out','a1_asking_for_directions','a1_simple_past_yesterday','a1_going_to_future_plans','a1_christmas_new_year_special','a2_lesson_tennis']
def numbered(name, ls):
    if len(ls) < 3 or not any(k in name.lower() for k in NUM): return ls
    out = []
    for n, l in enumerate(ls, 1):
        l = dict(l); l['t'] = '%d · %s' % (n, short(l['t'], 36)); out.append(l)
    return out
def series_group(name, ids, sub, mia=False):
    ls = []
    for i in sorted(ids):
        l = lesson(i)
        if not l: continue
        if mia:
            tt = re.search(r'<title>[^<]*Lesson (\d+) · ([^<]+)', rd(i + '.html'))
            if tt: l['t'] = '%d · %s' % (int(tt.group(1)), html.unescape(tt.group(2)).strip())
            m = re.match(r'a1s_(\d+)_', i); pic = 'journey/map/mia/%s.jpg' % m.group(1) if m else ''
            if pic and os.path.exists(os.path.join(ROOT, pic)): l['i'] = pic
        ls.append(l)
    if name == 'Beginner Course': ls.sort(key=lambda l: next((n for n, b in enumerate(BEG) if l['h'].startswith(b)), 99))
    ls = numbered(name, ls)
    return group(name, sub, ('journey/map/mia/01.jpg' if mia else ''), ls) if ls else None
def general_extras(key):
    A = {i: v for i, v in ALL.items()}
    by = lambda f: [i for i, v in A.items() if f(v)]
    out = []
    if key == 'first_steps':
        out.append(series_group("Mia's English", [i for i in A if i.startswith('a1s_')], 'a story in 50 lessons, A1', True))
        for nm, sub in (('Beginner Course', 'first lessons, A1'), ('Speak First', 'speaking from day one'), ('Stories (A1/A2)', 'short stories')):
            out.append(series_group(nm, by(lambda v, nm=nm: len(v) > 2 and v[2] == nm), sub))
    if key == 'finding_voice':
        out.append(series_group('Spark to Speech', by(lambda v: len(v) > 2 and v[2] == 'Spark to Speech'), 'A2 conversation starters'))
    return [x for x in out if x]
def route(r):
    R = raw(rd('journey_%s.html' % r), 'var R=')
    t, s, img = REG[r]; goals = []
    for key, gt, gd in R['goals']:
        cards = []
        for c in R['cards']:
            if c['goal'] != key: continue
            if c['name'] == 'Listening Practice': cards.append(listening_group()); continue
            if r == 'academic' and c['name'] == 'Academic Writing': continue   # leads to one lesson; removed for now
            po = lessons_of_page(c['href']); ids_ = [l for l in (lesson(i) for i in c['ids'] if 'index' not in i and not i.startswith(('journey', 'wordbank', 'explore', 'malcolm'))) if l]
            pos = {l['h']: n for n, l in enumerate(po)}
            if ids_: ls = sorted(ids_, key=lambda l: pos.get(l['h'], 9999))
            else: ls = [l for l in po if l['h'][:-5] in ALL] or po
            ls = numbered(c['name'], ls)
            cards.append(group(c['name'], c['meta'] or trim(c['desc'], 40), '', ls, c['href']) if ls else leaf(c['href'][:-5], c['name'], c['level'], c['meta']))
        if r == 'general': cards = general_extras(key) + cards
        gimg = 'journey/routes/route_%s_%s.jpg' % (r, key if os.path.exists(os.path.join(ROOT, 'journey/routes/route_%s_%s.jpg' % (r, key))) else 'hero')
        if not os.path.exists(os.path.join(ROOT, gimg)):   # keys differ (e.g. finding_voice): try prefix match
            g2 = [f for f in os.listdir(os.path.join(ROOT, 'journey/routes')) if f.startswith('route_%s_' % r) and key.split('_')[0] in f]
            gimg = 'journey/routes/' + (g2[0] if g2 else 'route_%s_hero.jpg' % r)
        if r == 'professional': cards = [interview_route() if k['t'].startswith('Interview English') else k for k in cards]
        goals.append(group(gt, trim(gd, 50), gimg, cards, 'journey_%s.html?goal=%s' % (r, key)))
    if r == 'general': goals = [speaking_route()] + goals
    if r == 'academic':
        ie = [g for g, (k, _, _) in zip(goals, R['goals']) if k.startswith('ielts_')]
        rest = [g for g, (k, _, _) in zip(goals, R['goals']) if not k.startswith('ielts_')]
        more = group('More IELTS practice', 'speaking, reading, writing and word games', 'journey/routes/route_academic_ielts_writing.jpg', [x for g in ie for x in g['k']])
        for g in rest:
            if g['t'].startswith('Cambridge'): g['k'] = [cambridge_route()] + [k for k in g['k'] if 'Cambridge' not in k['t']]
        goals = [ielts_route(), more] + rest
    return group(t, s, img, goals, 'journey_%s.html' % r)
def explore():
    t, s, img = REG['explore']; names = {}
    if OLD:
        for n in OLD['nodes']:
            if n['id'].startswith('ex_'): names[n['id'][3:]] = n['t']
    by = {}
    for e in EXP:
        if os.path.exists(os.path.join(ROOT, e[0] + '.html')): by.setdefault(e[3][0] if e[3] else 'X', []).append(leaf(e[0], e[1], e[2], trim(e[5], 60)))
    topics = [group(names.get(c, c), '%d lessons' % len(v), 'explore_img/%s.jpg' % c if os.path.exists(os.path.join(ROOT, 'explore_img/%s.jpg' % c)) else '', v) for c, v in sorted(by.items(), key=lambda x: -len(x[1])) if c in names]
    return group(t, s, img, chunk(topics), 'explore.html')
def palace():
    t, s, img = REG['palace']; kids = []
    for n in OLD['nodes']:
        if n.get('p') == 'palace':
            l = leaf(n['h_'][:-5], n['t'], '', n.get('s', '')); l['i'] = n.get('i') or ''; kids.append(l)
    return group(t, s, img, kids)
def tintin(parent):
    d = rd('../malcolmtheteacher-creator.github.io/comics/clear-line/index.html'); seen = {}
    for slug, inner in re.findall(r'<a[^>]*href="#(album-[^"]+)"[^>]*>(.*?)</a>', d, re.S):
        m = re.match(r'(\d+)\.\s*(.+)$', re.sub(r'<[^>]+>', '', inner).strip(), re.S)
        if m: seen.setdefault(slug, (int(m.group(1)), html.unescape(m.group(2)).strip()))
    eras = [('Early adventures', 'albums 1–4', 1, 4), ('Classic period', 'albums 5–12', 5, 12), ('Mature masterpieces', 'albums 13–21', 13, 21), ('Late works', 'albums 22–24', 22, 24)]
    out = []
    for t, sub, a, b in eras:
        ls = [{'t': '%d · %s' % (n, nm), 's': '', 'i': '', 'h': 'https://malcolmhyndman.com/comics/clear-line/#' + slug, 'l': '', 'k': []} for slug, (n, nm) in sorted(seen.items(), key=lambda x: x[1][0]) if a <= n <= b]
        if ls: out.append(group(t, sub, parent.get('i', ''), ls))
    return out
def small(r, p):
    t, s, img = REG[r]; kids = []
    for n in OLD['nodes']:
        if n.get('p') == p: kids.append({'t': n['t'], 's': n.get('s', ''), 'i': mapimg(n['t']) or n.get('i') or '', 'h': n['h_'], 'l': '', 'k': []})
    for k in kids:
        if k['h'].rstrip('/').endswith('clear-line'): k['h'] = ''; k['k'] = tintin(k)
    return group(t, s, img, kids)
SECT = {'Short History, Long Echoes': ('short_history_dashboard.html', r'<section class="theme"', r'<h[23][^>]*>(.*?)</h[23]>'),
        'Short Stories, Long Shadows': ('short_stories_long_shadows_dashboard.html', r'<section class="theme"', r'<h[23][^>]*>(.*?)</h[23]>'),
        'Bet the Company': ('bet_the_company_dashboard.html', r'(?=<[a-z0-9]+ [^>]*class="section-label")', r'class="section-label"[^>]*>(.*?)<')}
def sectioned(name):
    page, split, tre = SECT[name]; d = rd(page); themes = []
    for part in re.split(split, d)[1:]:
        m = re.search(tre, part, re.S)
        if not m: continue
        t = re.sub(r'<[^>]+>', '', html.unescape(m.group(1))); t = re.sub(r'[^\x00-\u024f\u2018-\u201d\u2013\u2014]', '', t).strip()
        t = re.sub(r'\s*\d+$', '', t).split('—')[0].strip(' -')
        ids = []
        for x in re.findall(r'[A-Za-z0-9][A-Za-z0-9_\-]*\.html', part):
            x = x[:-5]
            if x not in ids and 'dashboard' not in x.lower() and 'index' not in x and os.path.exists(os.path.join(ROOT, x + '.html')): ids.append(x)
        ls = [l for l in (lesson(i) for i in ids) if l]
        if ls and t and 'reading path' not in t.lower(): themes.append(group(t, '%d lessons' % len(ls), '', ls))
    return themes
THEMES = {
 'True Science Stories': [
  ('Medicine against the odds', 'doctors who proved the experts wrong', ['doctor_who_drank', 'semmelweis', 'john_snow', 'forssmann', 'penicillin', 'smallpox', 'tu_youyou']),
  ('Women who changed science', 'recognition, and who got it', ['rosalind_franklin', 'marie_curie', 'kariko', 'montessori']),
  ('How we think and decide', 'mind, mistakes and judgement', ['erikson', 'noise', 'thinking_in_bets']),
  ('Discovery and invention', 'code, puzzles and rescue', ['apollo13', 'dna_fingerprint', 'rosetta', 'rubik'])],
 'English at Work': [
  ('Getting started', 'the job, the interview, the room', ['phrase_bank', 'compliance_manager', 'the_interview', 'working_the_room', 'the_presentation']),
  ('Meetings and teamwork', 'speaking up, chairing, negotiating', ['speaking_up', 'chairing', 'negotiating', 'handover', 'the_deadline', 'consultation', 'showing_the_ropes', 'changing_brief']),
  ('Difficult conversations', 'saying no, mistakes, conflict', ['difficult_conversation', 'saying_no', 'the_mistake', 'taking_credit', 'colleague_who_cries', 'the_truce', 'not_coping', 'the_joke', 'native_speaker', 'younger_boss']),
  ('Clients and customers', 'sales, complaints, service', ['client_who_shouts', 'unpaid_invoice', 'first_sales_call', 'front_desk', 'parents_evening', 'sceptical_client', 'repair_counter', 'client_who_wont']),
  ('Career moves and leading', 'pay, promotion, leaving, managing', ['work_from_home', 'performance_review', 'resigning', 'made_redundant', 'the_reference', 'promoted_over', 'the_pay_rise', 'letting_someone_go', 'suddenly_the_boss', 'two_floors', 'breaking_the_news'])]}
def themed(name, ls):
    spec = THEMES.get(name)
    if not spec: return ls
    used = set(); out = []
    for t, sub, keys in spec:
        g = []
        for k in keys:
            for l in ls:
                hh = l['h'] or ' '.join(c['h'] for c in l['k'])
                if k in hh and hh not in used: used.add(hh); g.append(l)
        if g: out.append(group(t, sub, '', g))
    rest = [l for l in ls if (l['h'] or ' '.join(c['h'] for c in l['k'])) not in used]
    if rest and out: out.append(group('More lessons', '', '', rest))
    return out if len(out) >= 3 else ls
def pair_levels(ls):
    seen = set(); by = {}; order = []
    for l in ls:
        if l['h'] in seen: continue
        seen.add(l['h']); k = re.sub(r'\s*\((A2/B1|B2/C1|A2|B1|B2|C1)\)\s*$', '', l['t']).strip()
        if k not in by: by[k] = []; order.append(k)
        by[k].append(l)
    out = []
    for k in order:
        g = by[k]
        if len(g) < 2: out.append(g[0]); continue
        kids = []
        for l in sorted(g, key=lambda x: x.get('l', '')):
            c = dict(l); c['t'] = 'Level %s' % (l.get('l') or '?'); c['s'] = k; kids.append(c)
        out.append(group(k, 'two levels', '', kids))
    return out
def library():
    t, s, img = REG['library']; cols = []
    for b in OLD['libs']:
        ls = [l for l in (lesson(x[0]) for x in b['ls']) if l]
        if ls:
            th = sectioned(b['n']) if b['n'] in SECT else []
            if b['n'] in ('Everyday Echoes', 'English at Work'): ls = pair_levels(ls)
            ls = themed(b['n'], ls)
            cols.append(group(b['n'], '%d lessons' % len(ls), b.get('i') or '', th if len(th) >= 3 else ls))
    return group(t, s, img, chunk(cols))
top = {'t': 'English, taught through stories', 's': '', 'i': 'journey/world/region_hub.jpg', 'h': '', 'l': '',
       'k': [route('professional'), route('academic'), route('general'), explore(), palace(), small('comics', 'comics'), small('words', 'words'), library()]}
# order: clockwise-ish to match the 3x3 positions (TL,T,TR,L,R,BL,B,BR)
o = {x['t']: x for x in top['k']}
top['k'] = [o[REG[k][0]] for k in ('professional', 'academic', 'general', 'library', 'explore', 'palace', 'comics', 'words')]
def slim(n):
    for k in [k for k, v in n.items() if v in ('', [], None)]: del n[k]
    for c in n.get('k', []): slim(c)
def distinct(n, acc):
    if not n['k']: acc.add(n['h'])
    for c in n['k']: distinct(c, acc)
    return acc
print('distinct pages:', len(distinct(top, set())))
def collapse(n):
    for c in n['k']: collapse(c)
    n['k'] = [c for c in n['k'] if c['k'] or c['h'] or c.get('pg')]
    for i, c in enumerate(n['k']):
        if len(c['k']) == 1 and not c['k'][0]['k']:
            o = c['k'][0]; n['k'][i] = {'t': c['t'], 's': c['s'] or o['s'], 'i': c['i'] or o['i'], 'h': o['h'], 'l': o['l'], 'k': []}
collapse(top)
def depth(n): return 1 + max([depth(c) for c in n['k']] or [0])
nleaf = count(top); dep = depth(top)
slim(top)
tpl = rd('tools/mandalart_template.html')
out = sys.argv[1] if len(sys.argv) > 1 else 'map.html'
open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(tpl.replace('__TREE__', json.dumps(top, ensure_ascii=False, separators=(',', ':'))))
print(out, 'leaf boxes:', nleaf, 'depth:', dep)

if '--list' in sys.argv:
    need = []; seen = set()
    def w(n, par):
        if n.get('k') and not n.get('i') and not re.match(r'(Lessons|Collections|More) ', n['t']) and slug(n['t']) not in seen:
            seen.add(slug(n['t'])); need.append((par, n['t'], n.get('s', '')))
        for c in n.get('k', []): w(c, n['t'])
    w(top, '')
    json.dump([{'file': slug(t), 'title': t, 'within': p, 'note': s_} for p, t, s_ in need], open(os.path.join(ROOT, 'bots/map_pics.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(need), 'pictures listed')
