#!/usr/bin/env python3
"""
update_pathway_lessons.py
─────────────────────────
Scans every lesson HTML in the gitsite, extracts metadata, and re-injects
the LESSONS array into pathway_builder.html.

Run automatically by ① Update Lesson Index.command, or manually:
    python3 update_pathway_lessons.py

What it does:
  1. Scans all .html files in the gitsite folder
  2. Skips excluded prefixes (dashboards, games, religious studies, etc.)
  3. Extracts: filename, title, level, category, description, skill type,
     grammar point, grammar link, semantic topic tags
  4. Replaces the LESSONS array in pathway_builder.html in-place
  5. Reports a summary of what changed
"""

import os, re, json
from collections import Counter

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GITSITE_PATH = SCRIPT_DIR
PATHWAY_FILE = os.path.join(GITSITE_PATH, 'pathway_builder.html')
CACHE_FILE   = os.path.join(GITSITE_PATH, 'pathway_lessons_cache.json')

# ── Prefixes to exclude entirely ──────────────────────────────────────────────
EXCLUDED_PREFIXES = (
    'rs_',          # Religious Studies
    'ois_',         # Our Island Story (school history project)
    'ww_',          # Word Wall games
    'gr_',          # Game Room
    'lesson_',      # Old numbered lessons (superseded)
)

# ── Filename patterns to skip (dashboards, indexes, etc.) ─────────────────────
EXCLUDED_PATTERNS = (
    'dashboard', '_index', '_overview', '_course_guide',
    '_introduction', 'test_overview', 'malcolm_lesson_index',
    'topic_picker', 'pathway_builder', 'pathway_map',
    'publisher_', 'build_mindmap',
)

# ── Level inference from filename ────────────────────────────────────────────
LEVEL_FROM_FILENAME = {
    'a1p_': 'a1', 'a1_': 'a1',
    'su_a1': 'a1', 'su_a2': 'a2',
    'su_b1': 'b1', 'su_b2': 'b2',
    'bc_a2': 'a2', 'bc_b1': 'b1', 'bc_b2': 'b2', 'bc_c1': 'c1',
    'sp_b1': 'b1', 'sp_b2': 'b2', 'sp_c1': 'c1',
    'qf_':   'b1',   # Quick Fix — grammar/vocab, work at B1+
    'grammar_a2': 'a2', 'grammar_b1': 'b1', 'grammar_b2': 'b2',
    'grammar_c1': 'c1', 'grammar_c2': 'c2',
    'ielts_': 'b2',
    'acad_b1': 'b1', 'acad_b2': 'b2', 'acad_c1': 'c1',
    'prof_c1': 'c1',
    'cpe_': 'c1',
    'cpe_read_c1': 'c1', 'cpe_read_c2': 'c2',
    'cambridge_cae': 'c1',
    'cambridge_cpe': 'c2',
    'cpe_read': 'c1',
    'c2_': 'c2', '_c2_': 'c2',
    'c1_': 'c1', '_c1_': 'c1',
    'b2_': 'b2', '_b2_': 'b2',
    'b1_': 'b1', '_b1_': 'b1',
    'a2_': 'a2', '_a2_': 'a2',
}

# ── Category inference ────────────────────────────────────────────────────────
CATEGORY_MAP = {
    'food': 'food', 'restaurant': 'food', 'cooking': 'food', 'cuisine': 'food',
    'travel': 'travel', 'holiday': 'travel', 'tourism': 'travel',
    'work': 'work', 'business': 'work', 'professional': 'work', 'office': 'work',
    'meeting': 'work', 'career': 'work',
    'health': 'health', 'medical': 'health', 'wellness': 'health',
    'entertainment': 'entertainment', 'film': 'entertainment', 'music': 'entertainment',
    'art': 'entertainment', 'sport': 'entertainment', 'game': 'entertainment',
    'life': 'life', 'home': 'life', 'family': 'life', 'daily': 'life',
    'people': 'people', 'relationship': 'people', 'social': 'people', 'friend': 'people',
    'grammar': 'grammar', 'vocabulary': 'grammar', 'pronunciation': 'grammar',
    'ielts': 'ielts',
    'academic': 'skills', 'writing': 'skills', 'reading': 'skills', 'speaking': 'skills',
    'skills': 'skills',
}

# ── Skill type inference ──────────────────────────────────────────────────────
SKILL_TYPE_MAP = {
    'qf_': 'quick-fix',
    'grammar_': 'grammar',
    'ielts_': 'ielts',
    'sp_': 'speaking',
    'acad_': 'academic',
    'wp_': 'writing',
    'prof_c1': 'professional',
    'bc_': 'professional',
    'cpe_read': 'reading',
    'cambridge_cae_writing': 'writing',
    'cambridge_cae_speaking': 'speaking',
    'cambridge_cae_listening': 'listening',
    'cambridge_cae_reading': 'reading',
    'cambridge_cae': 'cambridge',
    'cambridge_cpe': 'cambridge',
    'su_': 'discussion',
}

# ── Semantic topic tagging ────────────────────────────────────────────────────
TOPIC_KEYWORDS = {
    'medicine':      ['medical','doctor','patient','health','nurse','hospital','surgery','diagnos','clinic','disease','treatment','therapy','symptom','anatomy','dental','pandemic'],
    'law':           ['legal','law','court','justice','contract','rights','crime','criminal','attorney','barrister','solicitor','judge','trial','evidence','regulation','legislation','copyright','patent'],
    'finance':       ['finance','financial','invest','budget','profit','revenue','market','stock','bank','loan','debt','interest','tax','accountant','accounting','insurance','pension','mortgage','economy','GDP','trade'],
    'technology':    ['tech','digital','software','hardware','data','AI','artificial intelligence','robot','algorithm','program','code','developer','internet','network','cyber','app','cloud','machine learning','automation','computer','smartphone'],
    'management':    ['manag','leader','leadership','team','meeting','decision','strategy','strategic','executive','CEO','director','corporate','HR','performance','objective','planning','project','delegation','mentor'],
    'negotiation':   ['negotiat','deal','persuad','compromise','bargain','mediat','dispute','resolution','agreement','concession','leverage','win-win'],
    'presentations': ['present','pitch','slide','audience','public speaking','conference','webinar','seminar','deliver','speech','storytelling','PowerPoint','engage'],
    'writing':       ['writ','essay','report','draft','edit','thesis','dissertation','paragraph','structure','argument','persuasive','analytical','narrative','proofreading','citation','bibliography','academic writing'],
    'communication': ['communicat','conversation','discuss','dialogue','listening','speak','verbal','nonverbal','body language','tone','assertive','feedback','clarity','interpersonal','email','interview','small talk'],
    'culture':       ['culture','cultural','tradition','custom','intercultural','diversity','global','international','multicultural','identity','society','norm','expat'],
    'environment':   ['environment','climate','carbon','green','sustainable','ecology','nature','wildlife','conservation','pollution','renewable','energy','solar','recycle','biodiversity','fossil fuel'],
    'politics':      ['polit','government','democra','election','vote','parliament','congress','policy','minister','diplomat','international relations','geopolit','sanction','treaty','ideology'],
    'education':     ['educat','teach','learn','student','university','school','college','academic','curriculum','degree','qualification','research','study','lecture','tutor','professor','training','exam','assessment'],
    'history':       ['history','historical','ancient','medieval','modern','century','era','war','revolution','empire','civilisation','civilization','archaeology','heritage','museum','timeline','colonial','dynasty'],
    'science':       ['science','scientific','research','experiment','hypothesis','theory','biology','chemistry','physics','mathematics','statistic','laboratory','innovation','discovery','space','astronomy','genetics','quantum'],
    'psychology':    ['psycholog','mental','emotion','behavior','behaviour','cognitive','therapy','counselling','stress','anxiety','depression','mindfulness','personality','motivation','perception','memory','intelligence','resilience','habit'],
    'business':      ['business','company','enterprise','entrepreneur','startup','commercial','brand','marketing','sales','customer','client','product','service','logistics','B2B','revenue','merger'],
    'arts':          ['art','music','film','cinema','theatre','theater','literature','poetry','painting','sculpture','design','architecture','fashion','photography','gallery','creative','performance','dance','opera'],
    'food':          ['food','cook','cuisine','restaurant','chef','recipe','ingredient','nutrition','diet','meal','dish','flavour','flavor','drink','wine','coffee','bakery','organic','vegan'],
    'travel':        ['travel','trip','destination','tourism','tourist','hotel','transport','flight','airport','visa','passport','explore','adventure','landmark','sightseeing','itinerary'],
    'sport':         ['sport','athletic','fitness','exercise','training','competition','team','player','champion','tournament','race','marathon','football','tennis','swimming','cycling','yoga','gym'],
    'ethics':        ['ethic','moral','value','principle','integrity','justice','fairness','responsibility','accountability','transparent','honest','dilemma','controversial','bias','discrimination','equality','human rights'],
    'media':         ['media','journalism','news','broadcast','podcast','social media','press','editor','reporter','headline','digital media','PR','public relations','advertising','brand','content','influencer'],
    'creativity':    ['creativ','design','innovat','imaginat','art','invent','original','brainstorm','inspiration','vision'],
}

CAT_DEFAULT_TOPICS = {
    'grammar': ['writing', 'communication'],
    'ielts':   ['writing', 'communication', 'education'],
    'skills':  ['communication', 'education'],
    'world':   ['culture', 'history', 'politics'],
    'work':    ['business', 'management', 'communication'],
    'people':  ['communication', 'psychology', 'culture'],
    'food':    ['food', 'culture'],
    'life':    ['communication', 'culture'],
    'cambridge-cae': ['education', 'writing', 'communication'],
    'cambridge-cpe': ['education', 'writing', 'communication'],
}


def get_topics(text, cat=''):
    text_l = text.lower()
    found = []
    for topic, kws in TOPIC_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in text_l:
                found.append(topic)
                break
    if not found:
        found = list(CAT_DEFAULT_TOPICS.get(cat, []))
    return found


def infer_level(filename):
    fn = filename.lower()
    # Check specific number patterns like _c2_, _b1_
    for pattern in ['_c2_','_c2.','c2_','_c1_','_c1.','c1_',
                    '_b2_','_b2.','b2_','_b1_','_b1.','b1_',
                    '_a2_','_a2.','a2_','_a1_','_a1.','a1_']:
        if pattern.rstrip('.').rstrip('_').lstrip('_') in fn:
            lv = pattern.strip('_.').lower()
            if lv in ('c2','c1','b2','b1','a2','a1'):
                return lv
    for prefix, lv in sorted(LEVEL_FROM_FILENAME.items(), key=lambda x: -len(x[0])):
        if fn.startswith(prefix) or prefix in fn:
            return lv
    # IELTS default
    if 'ielts' in fn: return 'b2'
    if 'cambridge_cae' in fn: return 'c1'
    if 'cambridge_cpe' in fn or 'cpe_' in fn: return 'c1'
    return 'b1'  # safe default


def infer_category(filename, title, content_snippet):
    fn = filename.lower()
    combo = (fn + ' ' + title + ' ' + content_snippet).lower()
    # Cambridge special categories
    if fn.startswith('cambridge_cae') or 'cae' in fn:
        return 'cambridge-cae'
    if fn.startswith('cambridge_cpe') or fn.startswith('cpe_'):
        return 'cambridge-cpe'
    if 'ielts' in fn: return 'ielts'
    if 'grammar_' in fn or fn.startswith('qf_'): return 'grammar'
    if fn.startswith('acad_') or fn.startswith('wp_'): return 'skills'
    if fn.startswith('sp_'): return 'skills'
    for kw, cat in CATEGORY_MAP.items():
        if kw in combo: return cat
    return 'world'  # default


def infer_skill(filename):
    fn = filename.lower()
    for prefix, sk in sorted(SKILL_TYPE_MAP.items(), key=lambda x: -len(x[0])):
        if fn.startswith(prefix) or prefix in fn:
            return sk
    if fn.startswith('bc_'): return 'professional'
    if 'cpe_read' in fn: return 'reading'
    if 'cambridge_cae_writing' in fn: return 'writing'
    if 'cambridge_cae_speaking' in fn: return 'speaking'
    if 'cambridge_cae_listening' in fn: return 'listening'
    return 'discussion'


def extract_lesson(filepath):
    """Extract metadata from a single lesson HTML file."""
    filename = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(8000)
    except Exception:
        return None

    # Title
    tm = re.search(r'<title>([^<]+)</title>', content, re.I)
    title = tm.group(1).strip() if tm else filename
    title = re.sub(r'\s*[|\-].*Malcolm.*$', '', title, flags=re.I).strip()
    title = re.sub(r'\s*\|\s*.*$', '', title).strip()[:80]

    # Level
    lv = infer_level(filename)

    # Category
    cat = infer_category(filename, title, content[:2000])

    # Description — meta first, then first meaningful <p>
    desc = ''
    md = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', content[:5000], re.I)
    if md:
        desc = md.group(1).strip()[:100]
    if len(desc) < 20:
        for p in re.findall(r'<p[^>]*>(.*?)</p>', content[:6000], re.S):
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 30 and not clean.startswith('©') and 'Malcolm' not in clean:
                desc = clean[:100]
                break

    # Skill type
    sk = infer_skill(filename)

    # Grammar point & link — look for data-grammar or known patterns
    g, gl = '', ''
    gm = re.search(r'data-grammar=["\']([^"\']+)["\']', content, re.I)
    if gm: g = gm.group(1).strip()[:50]
    glm = re.search(r'href=["\'](grammar_[^"\']+\.html)["\']', content, re.I)
    if glm: gl = glm.group(1)

    # Topics
    topics = get_topics(title + ' ' + desc + ' ' + cat, cat)

    entry = {'f': filename, 't': title, 'lv': lv, 'cat': cat, 'd': desc, 'sk': sk}
    if g:  entry['g']  = g
    if gl: entry['gl'] = gl
    if topics: entry['topics'] = topics
    return entry


def should_exclude(filename):
    fn = filename.lower()
    if fn.startswith(EXCLUDED_PREFIXES): return True
    for p in EXCLUDED_PATTERNS:
        if p in fn: return True
    return False


def update_pathway_builder(lessons):
    """Replace the LESSONS array in pathway_builder.html."""
    if not os.path.exists(PATHWAY_FILE):
        print(f'⚠️  pathway_builder.html not found at {PATHWAY_FILE}')
        return False

    with open(PATHWAY_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    marker = 'const LESSONS = '
    if marker not in html:
        print('⚠️  LESSONS marker not found in pathway_builder.html')
        return False

    lesson_js = marker + json.dumps(lessons, separators=(',', ':')) + ';'

    start = html.index(marker)
    depth, i = 0, start + len(marker)
    while i < len(html):
        if html[i] == '[': depth += 1
        elif html[i] == ']':
            depth -= 1
            if depth == 0: break
        i += 1
    end = i + 1
    if end < len(html) and html[end] == ';': end += 1

    html = html[:start] + lesson_js + html[end:]

    with open(PATHWAY_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    print('🔍 Scanning gitsite for lessons...')

    all_files = [f for f in os.listdir(GITSITE_PATH)
                 if f.endswith('.html') and not should_exclude(f)]
    all_files.sort()

    print(f'   {len(all_files)} candidate files found')

    # Load existing cache to track what's new/changed
    old_cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            old_cache = {l['f']: l for l in json.load(f)}

    lessons = []
    new_count = 0
    updated_count = 0

    for fname in all_files:
        filepath = os.path.join(GITSITE_PATH, fname)
        entry = extract_lesson(filepath)
        if not entry:
            continue

        if fname not in old_cache:
            new_count += 1
        else:
            # Preserve manually-curated data from cache (topics, descriptions, grammar)
            cached = old_cache[fname]
            if cached.get('topics') and len(cached['topics']) > len(entry.get('topics', [])):
                entry['topics'] = cached['topics']
            if cached.get('d') and len(cached.get('d','')) > len(entry.get('d','')):
                entry['d'] = cached['d']
            if cached.get('g') and not entry.get('g'):
                entry['g'] = cached['g']
            if cached.get('gl') and not entry.get('gl'):
                entry['gl'] = cached['gl']
            # Flag if title or level changed (genuinely new metadata)
            if cached.get('t') != entry.get('t') or cached.get('lv') != entry.get('lv'):
                updated_count += 1

        lessons.append(entry)

    # Stats
    lv_counts = Counter(l['lv'] for l in lessons)
    sk_counts = Counter(l['sk'] for l in lessons)
    with_topics = sum(1 for l in lessons if l.get('topics'))

    print(f'\n📚 Lesson summary:')
    print(f'   Total: {len(lessons)} lessons')
    print(f'   New since last run: {new_count}')
    print(f'   Updated: {updated_count}')
    print(f'   Levels: {dict(sorted(lv_counts.items()))}')
    print(f'   With topic tags: {with_topics}/{len(lessons)}')
    print(f'   Skill types: {dict(sk_counts.most_common(5))}')

    # Save cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(lessons, f, separators=(',', ':'))

    # Update pathway_builder.html
    print(f'\n✏️  Updating pathway_builder.html...')
    if update_pathway_builder(lessons):
        size_kb = os.path.getsize(PATHWAY_FILE) // 1024
        print(f'   ✅ pathway_builder.html updated ({size_kb}KB, {len(lessons)} lessons embedded)')
    else:
        print('   ❌ Failed to update pathway_builder.html')
        return

    if new_count > 0:
        print(f'\n🆕 {new_count} new lesson(s) added to the pathway builder!')


if __name__ == '__main__':
    main()
