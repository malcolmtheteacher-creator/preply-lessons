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
    # NOTE: Keep keywords SPECIFIC to the topic — avoid generic words that appear
    # in lesson instructions ("write", "discuss", "learn", "study", "structure",
    # "policy", "social media") since those flood every lesson with every tag.
    # These keywords will be matched against: filename + title + description +
    # headings + tab labels + intro paragraph only.
    'medicine':      [
        'medical','doctor','patient','nurse','hospital','surgery','diagnos','clinic',
        'disease','treatment','symptom','anatomy','dental','pandemic',
        'physician','specialist','prescription','medication','vaccine','vaccination',
        'anaesthetic','ward','triage','referral','blood test','x-ray','mri',
        'infection','antibiotic','allergy','GP','a&e','emergency room',
        'prognosis','outpatient','patholog','cardiolog','oncolog','neurolog',
        'dermatolog','radiolog','paramedic','midwife','obstetrician','geriatrician',
        'psychiatr','healthcare','pharmaceutical','physiology',
    ],
    'law':           [
        'legal','law','court','justice','contract','crime','criminal',
        'attorney','barrister','solicitor','judge','trial','evidence','legislation',
        'copyright','patent','lawsuit','liability','damages','verdict','sentence',
        'defendant','plaintiff','jury','prosecution','defence','defense',
        'employment law','human rights','tribunal','arbitration','compliance',
        'gdpr','intellectual property','trademark','fraud',
    ],
    'finance':       [
        'finance','financial','invest','budget','profit','revenue','stock market',
        'bank loan','debt','accountant','accounting','insurance','pension',
        'mortgage','GDP','cash flow','balance sheet','shareholder','dividend',
        'equity','venture capital','private equity','ipo','portfolio',
        'inflation','recession','fiscal','monetary','currency','exchange rate',
        'cryptocurrency','bitcoin','fintech','audit','payroll','profit margin',
    ],
    'technology':    [
        'technology','software','hardware','artificial intelligence',
        'robot','algorithm','coding','developer','cybersecurity','cyber','cloud',
        'machine learning','automation','smartphone','blockchain',
        'internet of things','big data','analytics','encryption','hack','malware',
        'digital transformation','virtual reality','augmented reality',
    ],
    'management':    [
        'manag','leadership','executive','director','corporate',
        'human resources','appraisal','stakeholder','delegation','coaching',
        'line manager','redundancy','restructure','change management',
        'agile','scrum','kanban','one-to-one',
    ],
    'negotiation':   [
        'negotiat','bargaining','mediator','mediation','concession','leverage','win-win',
        'counter-offer','contract negotiation','salary negotiation',
        'closing a deal','objection handling','stalemate','walk away',
    ],
    'presentations': [
        'presentation','presenting','presenter','pitch','public speaking','conference',
        'webinar','seminar','keynote','powerpoint','q&a','panel','moderator',
        'visual aid','signposting','hook','opening statement','delivery','slides',
    ],
    'writing':       [
        'essay','report','thesis','dissertation','proofreading',
        'citation','bibliography','academic writing','formal letter',
        'topic sentence','coherence','cohesion','executive summary',
        'abstract','paraphrase','footnote','annotate',
    ],
    'communication': [
        'interpersonal','small talk','body language','assertive',
        'active listening','telephone english','video call english',
        'difficult conversations','cross-cultural communication',
        'giving feedback','conflict resolution','rapport','empathy',
    ],
    'culture':       [
        'culture','cultural','tradition','custom','intercultural','diversity',
        'multicultural','expat','stereotype','culture shock','taboo',
        'cross-cultural','etiquette','manners','working abroad','living abroad',
    ],
    'environment':   [
        'environment','climate change','carbon','sustainable','ecology',
        'wildlife','conservation','pollution','renewable energy','recycle',
        'biodiversity','fossil fuel','global warming','greenhouse gas','emission',
        'net zero','carbon footprint','plastic waste','deforestation',
        'electric vehicle','wind power','paris agreement','cop26','cop30',
    ],
    'politics':      [
        'politics','political','politician','government','election','vote',
        'parliament','diplomat','treaty','ideology','campaign','referendum',
        'geopolit','sanction','foreign policy','nato','sovereignty',
        'asylum seeker','refugee','nationalism','populism','left wing','right wing',
        'prime minister','president','secretary of state','senate','congress',
    ],
    'education':     [
        'university','curriculum','degree','qualification','dissertation',
        'scholarship','tuition fees','admissions','gap year',
        'e-learning','mooc','vocational','apprenticeship','academic pressure',
        'grading system','standardised test','higher education',
    ],
    'history':       [
        'history','historical','ancient','medieval','century','era',
        'revolution','empire','civilisation','civilization','archaeology',
        'colonial','dynasty','world war','cold war','genocide','holocaust',
        'slavery','colonialism','apartheid','suffragette','reformation',
        'renaissance','enlightenment','industrial revolution',
    ],
    'science':       [
        'science','scientific','biology','chemistry','physics','genetics',
        'quantum','atom','molecule','laboratory','space exploration','astronomy',
        'nanotechnology','biotechnology','evolution','dna','peer review',
        'clinical trial','research paper','scientific method',
    ],
    'psychology':    [
        'psycholog','cognitive','counselling','anxiety','depression','mindfulness',
        'personality','trauma','self-esteem','social psychology','burnout',
        'phobia','ocd','adhd','autism','bipolar','therapist','psychotherapist',
        'unconscious bias','heuristic','attachment theory','grief',
    ],
    'business':      [
        'business','entrepreneur','startup','brand','marketing','B2B',
        'acquisition','merger','supply chain','ecommerce','retail',
        'customer service','market research','competitor analysis','pitch deck',
        'business plan','trade fair','franchise','import duties','exporting','networking',
    ],
    'arts':          [
        'film','cinema','theatre','theater','literature','poetry','painting',
        'sculpture','architecture','photography','gallery','opera','ballet',
        'novel','fiction','playwright','director','musician','composer',
        'exhibition','oscar','bafta','grammy','screenplay','animation',
    ],
    'food':          [
        'food','cuisine','restaurant','chef','recipe','nutrition','diet',
        'vegan','vegetarian','seafood','street food','fine dining','michelin',
        'breakfast','lunch','dinner','supermarket','gut health',
        'organic','allergy','intolerance','gluten-free','halal',
    ],
    'travel':        [
        'travel','tourism','tourist','hotel','flight','airport','visa','passport',
        'sightseeing','itinerary','accommodation','backpack','cruise',
        'package holiday','landmark','cultural trip','business travel',
    ],
    'sport':         [
        'sport','athletic','fitness','marathon','football','tennis','swimming',
        'cycling','rugby','cricket','basketball','triathlon','yoga',
        'tournament','champion','referee','stadium','penalty',
        'doping','transfer window','fan culture',
    ],
    'ethics':        [
        'ethic','moral','dilemma','integrity','discrimination','equality',
        'corporate social responsibility','csr','whistleblower',
        'corruption','consent','privacy','surveillance','ai ethics',
        'medical ethics','animal rights','euthanasia','capital punishment',
        'social justice','bias','privilege','inequality',
    ],
    'media':         [
        'journalism','broadcast','podcast','press freedom','fake news',
        'misinformation','propaganda','tabloid','broadsheet',
        'social media influencer','youtube','instagram','tiktok','viral',
        'press release','pr strategy','advertising campaign',
    ],
    'creativity':    [
        'creativ','brainstorm','ideation','prototype','lateral thinking',
        'design thinking','creative writing','storytelling','innovation',
    ],
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
            content = f.read()          # read entire file for rich tagging
    except Exception:
        return None

    # Working window — cap at 60 000 chars to keep speed reasonable
    working = content[:60000]

    # Title
    tm = re.search(r'<title>([^<]+)</title>', working, re.I)
    title = tm.group(1).strip() if tm else filename
    title = re.sub(r'\s*[|\-].*Malcolm.*$', '', title, flags=re.I).strip()
    title = re.sub(r'\s*\|\s*.*$', '', title).strip()[:80]

    # Level
    lv = infer_level(filename)

    # Category
    cat = infer_category(filename, title, working[:2000])

    # Description — meta first, then first meaningful <p>
    desc = ''
    md = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', working[:5000], re.I)
    if md:
        desc = md.group(1).strip()[:100]
    if len(desc) < 20:
        for p in re.findall(r'<p[^>]*>(.*?)</p>', working[:6000], re.S):
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 30 and not clean.startswith('©') and 'Malcolm' not in clean:
                desc = clean[:100]
                break

    # Skill type
    sk = infer_skill(filename)

    # Grammar point & link — look for data-grammar or known patterns
    g, gl = '', ''
    gm = re.search(r'data-grammar=["\']([^"\']+)["\']', working, re.I)
    if gm: g = gm.group(1).strip()[:50]
    glm = re.search(r'href=["\'](grammar_[^"\']+\.html)["\']', working, re.I)
    if glm: gl = glm.group(1)

    # ── Rich topic extraction ──────────────────────────────────────────────────
    # Use high-signal sources only — NOT full body text, because generic lesson
    # instructions ("write your answer", "discuss", "policy", "social media") would
    # tag almost every lesson with almost every topic, making boosts meaningless.
    #
    # High-signal sources (specific to lesson content):
    #   1. Filename words — the most descriptive signal ("bc_b2_negotiating_salary")
    #   2. Title — what the lesson is actually about
    #   3. Description — curated summary
    #   4. H1–H3 headings — section titles like "Vocabulary: Medical Terms"
    #   5. data-* attributes & aria-labels — structured metadata
    #   6. Tab/button labels — often named after the topic (e.g. "Negotiation Tips")
    #   7. Intro paragraph only — first substantive <p> after the title area

    # 1. Filename
    fname_words = re.sub(r'[_\-]', ' ', filename.replace('.html', ''))

    # 2+3. Title and desc already extracted above

    # 4. H1–H3 headings
    headings = ' '.join(re.findall(r'<h[1-3][^>]*>([^<]+)</h[1-3]>', working, re.I))

    # 5. data-* and aria-label attributes (vocabulary sets, card content labels)
    data_attrs = ' '.join(re.findall(r'(?:data-[\w-]+|aria-label)=["\']([^"\']{4,60})["\']', working, re.I))

    # 6. Tab and button text (short labels: "Negotiation", "Medical Vocabulary", etc.)
    tab_labels = ' '.join(re.findall(r'<(?:button|a|span|li)[^>]*class=["\'][^"\']*(?:tab|btn|chip|label)[^"\']*["\'][^>]*>([^<]{3,40})</(?:button|a|span|li)>', working, re.I))

    # 7. First intro paragraph — context for what the lesson is about
    intro_para = ''
    for p in re.findall(r'<p[^>]*>(.*?)</p>', working[:8000], re.S):
        clean_p = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean_p) > 40 and 'Malcolm' not in clean_p and not clean_p.startswith('©'):
            intro_para = clean_p[:300]
            break

    # Combine all high-signal sources
    rich_text = ' '.join([fname_words, title, desc, headings, tab_labels, data_attrs, intro_para])

    topics = get_topics(rich_text, cat)

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
            cached = old_cache[fname]
            # Topics: always use freshly computed (rich-text tagging is now reliable)
            # Description/grammar: keep cached if it's longer/richer
            if cached.get('d') and len(cached.get('d', '')) > len(entry.get('d', '')):
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
