#!/usr/bin/env python3
"""Match every lesson in wordbank/all_lessons.js to a My Room object (journey/objects.json map).
Keeps existing hand matches. Order: keyword rules on the title, then series pools, then a
deterministic spread across all objects. Usage: python3 tools/match_objects.py"""
import json, re, os, hashlib
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.loads(re.search(r'WBALL=(\{.*\})', open(root + '/wordbank/all_lessons.js').read(), re.S).group(1))
o = json.load(open(root + '/journey/objects.json'))
keys = [x['key'] for x in o['library']]
H = lambda s: int(hashlib.md5(s.encode()).hexdigest(), 16)
pick = lambda lst, s: lst[H(s) % len(lst)]

RULES = [
 (r'hello|getting to know|all about me|first impression|introduc|small talk|meet', ['invitation','teapot','handmirror','suitcase']),
 (r'conditional|if i|if only|wish', ['crystalball','signpost','dice']),
 (r'passive|participle', ['gears','plug','lever']),
 (r'tense|past (simple|continuous)|present (simple|continuous|perfect)|future|used to|time scramb', ['hourglass','pocketwatch','sundial','calendar','metronome']),
 (r'relative clause|who, which|cleft|inversion|sentence architecture|complex sentence', ['gears','chessking','labyrinth']),
 (r'article|preposition|in, on, at|determiner', ['signpost','ladder','ropebridge']),
 (r'compar|bigger|superlative|contrast', ['scales','balance' if False else 'scales']),
 (r'modal|deduction|speculat', ['magnifier','crystalball','questionmark']),
 (r'question|wh-', ['questionmark','magnifier']),
 (r'word|vocab|collocation|dictionary|building words|phrasal|idiom|spelling', ['dictionary','typeblocks','bookstack']),
 (r'hedg|discourse|linker|paraphras|reformulat|differently', ['quill','megaphone','typeblocks']),
 (r'leadership|leader|boardroom|management|manager|team|delegat|motivat|belbin', ['chessking','crown','scales','briefcase','ladder']),
 (r'negotiat|bargain|price|deal|soft no|saying no', ['scales','goldpouch','handcuffs' if False else 'cash','coins']),
 (r'meeting|chair|agenda|seminar|viva|lecture|presentation|pitch|public speaking|rhetoric|speaking', ['microphone','megaphone','chalkboard','clapper']),
 (r'email|writing|essay|report|proposal|thesis|article|note-taking|reading|abstract|paper|academic|research|literature|source', ['quill','typewriter','notebook','letter','bookstack','dictionary']),
 (r'grant|fund|financ|money|budget|invest|econom|tax|salary|market|startup|brand|business|commerc|sales|branding', ['coinjar','cash','briefcase','coins','abacus','goldpouch']),
 (r'interview|job|career|cv|work|employ|workplace|hiring|colleague', ['briefcase','hardhat','handshake' if False else 'briefcase','wrench','fedora']),
 (r'ai\b|artificial|robot|tech|digital|online|computer|data|algorithm|software|internet|screen|app\b|phone|social media', ['robot','chip','laptop','smartphone','brain','gears']),
 (r'climate|green|environment|energy|sustainab|nature|plastic|pollut|renewable|recycl', ['turbine','sapling','earth','blossomtree','snowflake']),
 (r'health|medic|wellbeing|stress|sleep|mental|disease|doctor|hospital|ageing|fitness|diet|food', ['pills','vial','xray','thermometer','insulinpen','apple','soupbowl']),
 (r'travel|holiday|trip|journey|airport|hotel|tourism|abroad|flight', ['suitcase','passport','ticket','streetmap','jet','taxi']),
 (r'shop|buy|clothes|fashion|retail', ['shoppingbag','hanger','scissors','coinjar','basket']),
 (r'music|song|band|k-pop|concert|sing|guitar', ['guitar','drum','goldenrecord','lyre','microphone','metronome']),
 (r'film|movie|cinema|tv|television|series|netflix|actor|theatre|drama', ['clapper','masks','reel','vhs','camera']),
 (r'book|novel|story|stories|tale|fiction|read|poet|poem|limerick|author|myth', ['bookstack','scroll','quill','diary','comic']),
 (r'art\b|paint|museum|gallery|design|creative|draw|sculpt|photograph|heist', ['palette','sketchbook','emptyframe','statuehead','camera','polaroid']),
 (r'school|educat|learn|study|student|universit|exam|test|ielts|cambridge|toefl|duolingo|diagnostic', ['chalkboard','slate','notebook','stopwatch','bookstack','dictionary']),
 (r'law|legal|court|crime|police|justice|murder|detective|prison|trial|ethic|moral|rights', ['gavel','scales','handcuffs','magnifier','padlock','fedora']),
 (r'politic|vote|election|democra|government|power|empire|revolution|republic|nation|war\b|battle|army|military|soldier|conflict', ['ballotbox','banner','crown','shield','cannon','medal','eagle']),
 (r'world war|wwii|ww2|ww1|holocaust|nazi|cold war|bomb', ['gasmask','enigma','medal','warship','biplane']),
 (r'history|ancient|roman|rome|greek|egypt|viking|medieval|renaissance|victorian|tudor|china|chinese|japan|samurai|aztec|maya|inca|persia|ottoman|byzantine', ['scroll','amphora','helmet','temple','tapestry','tablet','pyramid','longship','kabuto']),
 (r'space|moon|mars|astronaut|nasa|planet|star|galaxy|satellite|rocket', ['astronauthelmet','planet','telescope','capsule','rocket','moon']),
 (r'science|scien|experiment|chemi|physic|biolog|dna|genetic|lab\b|invent|discover|innovat|engineer', ['flask','testtubes','microscope','atom','dna','lightbulb','gears']),
 (r'ocean|sea\b|ship|sail|pirate|navy|maritime|titanic|shackleton|arctic|polar|erebus|expedition|explor', ['shipwheel','steamship','galleon','piratehat','iceaxe','telescope','lifeboat']),
 (r'cycling|bike|sport|olympic|football|game|race|speed|running|marathon|champion|win|train\b|athlet', ['runshoes','trophy','football','stopwatch','torch','rosette','boxinggloves']),
 (r'family|child|baby|parent|home|house|friend|love|marriage|wedding|relationship|couple|date|dating', ['cradle','cottage','rings','locket','dollhouse','cake','giftbox']),
 (r'philosoph|epicur|stoic|socrat|plato|aristotle|spinoza|aquinas|treatise|virtue|truth|god\b|hall of thought|lesson \d+:', ['owl','statuehead','candle','hourglass','sundial','lyre']),
 (r'god|religio|prayer|church|mosque|temple|faith|bible|islam|muslim|christian|hindu|sikh|buddh|jew|jewish|worship|trinity|ritual', ['candlestick','orthodoxcross','dome','temple','dove','scroll','candle']),
 (r'city|urban|street|town|london|new york|paris|rome|tokyo|berlin|britain|british|culture|tradition|festival|celebrat|holiday|custom|life in', ['streetlamp','clocktower','pillarbox','taxi','lanterns','fan']),
 (r'animal|pet|dog|cat\b|bird|zoo|wildlife|farm|insect', ['dog','owl','butterfly','elephant','cow','sheep','songbird']),
 (r'hot takes|debate|opinion|argument|motion|agree|discussion|conversation|talk about|big questions|curious|dilemma|decision|choice', ['dice','scales','megaphone','questionmark','pokerchips']),
 (r'dream|sleep|night|memory|remember|mind|brain|psycholog|think|habit|focus|flow|boredom|creativ', ['nightcap','brain','crystalball','candle','hourglass','lightbulb']),
 (r'ghost|haunt|horror|spooky|mystery|secret|spy|shadow|dark|vampire|plague|witch', ['skull','witchhat','plaguemask','spiderweb','candle','fedora']),
 (r'komorebi|nature|tree|forest|garden|flower|season|weather|rain|snow|wind|sun\b', ['tree','sunflowers','umbrella','snowflake','blossomtree','sapling']),
 (r'food|cook|restaurant|recipe|eat|cafe|coffee|tea\b|drink|bread|dinner|breakfast|lunch', ['teapot','espresso','pie','bagel','soupbowl','spoon','cake']),
 (r'quick fix', ['slate','chalkboard','notebook','magnifier']),
]
POOLS = {
 'Quick Fix': ['slate','chalkboard','notebook','magnifier','dictionary','scissors'],
 'WordWall Games': ['dice','pokerchips','jenga','rubik','dartboard','ninebox','puppet','kite'],
 'Religious Studies': ['candlestick','candle','orthodoxcross','dome','temple','dove','scroll','lanterns','bamboo','tree'],
 'IELTS Course': ['stopwatch','notebook','quill','microphone','bookstack','typewriter'],
 'Short History, Long Echoes': ['scroll','hourglass','tapestry','sundial','bookstack','clocktower'],
 'Speaking Pathway': ['microphone','megaphone','signpost','telescope','lightbulb'],
 'Speaking Pathway Prep': ['microphone','megaphone','signpost','telescope','lightbulb'],
 'Grammar Course': ['gears','typeblocks','lever','abacus','chalkboard'],
 'Everyday Echoes': ['teapot','pillarbox','taxi','phone','shoppingbag','basket'],
 'Cambridge Exam Prep': ['stopwatch','notebook','dictionary','chalkboard','quill'],
 'Behind the Screen': ['camera','clapper','reel','vhs','laptop'],
 'A1 Pathway': ['alarmclock','espresso','shoppingbag','suitcase','cake','teapot'],
 'English at Work': ['briefcase','hardhat','laptop','fedora','phone','typewriter'],
 'The Art of Memory': ['palace','candle','scroll','hourglass','owl'],
 'Memory Arts': ['palace','candle','scroll','hourglass','owl'],
}
GENERIC = ['notebook','lightbulb','telescope','compass' if False else 'pocketwatch','owl','bookstack','lantern' if False else 'handlamp','scroll','globe','magnifier','hourglass','teapot']
keyset = set(keys)
m = dict(o['map']); stats = {'kept': len(m), 'rule': 0, 'pool': 0, 'spread': 0}
for lid, (title, level, series) in d.items():
    if lid in m: continue
    ti = re.sub(r'\s*[-\u2014]\s*(year \d+ )?(religious studies|b\d.*|c\d.*|a\d.*|english lesson)$', '', title, flags=re.I)
    if ':' in ti and len(ti.split(':')[0].split()) <= 4: ti = ti.split(':', 1)[1]
    s = ti.lower()
    c = None
    if series == 'Religious Studies':
        lst = RULES[-3][1] if False else ['candlestick','orthodoxcross','dome','temple','dove','scroll','candle','lanterns','bamboo','tree']
        rel = [(r'\b(islam|muslim|mosque|hajj|ramadan|quran|prophet)', ['dome','moon','lanterns']),
               (r'\b(christian|jesus|church|bible|trinity|easter|christmas|resurrect|catholic|protestant)', ['orthodoxcross','candlestick','dove']),
               (r'\b(hindu|hinduism|diwali|karma|dharma|brahman)', ['lanterns','lyre','elephant']),
               (r'\b(buddh|nirvana|meditat)', ['bamboo','sapling','candle']),
               (r'\b(sikh|gurdwara)', ['sash','handlamp']),
               (r'\b(jew|jewish|judaism|torah|synagogue)', ['candle','scroll','candlestick']),
               (r'\b(suffer|evil|death|afterlife|life after|heaven|hell)', ['candle','skull','hourglass']),
               (r'\b(rights|justice|equality|prejudice|discriminat|poverty|war|peace)', ['scales','dove','banner']),
               (r'\b(creation|universe|origin|science|environment|stewardship)', ['earth','tree','planet'])]
        for rx, l in rel:
            if re.search(rx, s): c = pick(l, lid); stats['rule'] += 1; break
        if not c: c = pick(lst, lid); stats['pool'] += 1
        m[lid] = c; continue
    for rx, lst in RULES:
        if re.search(r'\b(?:' + rx + r')', s):
            c = pick([x for x in lst if x in keyset], lid); stats['rule'] += 1; break
    if not c and series in POOLS:
        c = pick([x for x in POOLS[series] if x in keyset], lid); stats['pool'] += 1
    if not c:
        c = pick(keys, lid); stats['spread'] += 1
    m[lid] = c
o['map'] = m
json.dump(o, open(root + '/journey/objects.json', 'w'), indent=1, ensure_ascii=False)
ready = sorted(k for k in keys if os.path.exists(f'{root}/journey/img/obj/{k}.png'))
open(root + '/journey/objects_ready.js', 'w').write('window.OBJ_READY=' + json.dumps({k: 1 for k in ready}) + ';window.OBJ_MAP=' + json.dumps(m, separators=(',', ':')) + ';')
print(stats, len(m))
