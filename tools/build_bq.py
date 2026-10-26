"""Build the Big Questions lessons (philosophy + English, C1) from tools/bq_content/*.py.
Each content file defines L (dict). Output: bq_NN_<slug>_c1.html. Edit content, never the HTML."""
import glob, importlib.util, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = open(os.path.join(ROOT, 'short_history_houdini.html')).read()
CSS = SRC[SRC.index('<style>'):SRC.index('</style>') + 8]
JS = SRC[SRC.index('<script>'):SRC.index('</script>') + 9]
I = '<input type="text" placeholder="...">'
TOG = "this.nextElementSibling.classList.toggle('show')"

def reveal_item(sent, ans):
    return (f'            <div class="guess-item">\n                <div class="sent">{sent}</div>\n'
            f'                <button class="reveal-btn" onclick="{TOG}">Reveal</button>\n'
            f'                <div class="meaning">{ans}</div>\n            </div>\n')

def check(c):
    return ('            <div class="check">\n                <div class="q">Quick check — answer from memory, then reveal:</div>\n'
            f'                <p>1. {c[0]}</p>\n                <p>2. {c[1]}</p>\n'
            f'                <button class="reveal-btn" onclick="{TOG}">Reveal answers</button>\n'
            f'                <div class="answers">\n                    <p><strong>1.</strong> {c[2]}</p>\n                    <p><strong>2.</strong> {c[3]}</p>\n                </div>\n            </div>\n')

def discuss(t):
    return f'            <div class="discuss">\n                <strong>Discuss:</strong>\n                <ul><li>{t}</li></ul>\n            </div>\n'

def gap(gid, ex):
    out = f'            <h3>{ex["title"]}</h3>\n            <p>{ex["intro"]}</p>\n            <div class="gap-fill">\n'
    for line in ex['lines']:
        body = re.sub(r'(?<!\w)__(?!\w)', I, line)
        out += f'                <p>{body}</p>\n'
    out += (f'                <button class="reveal-btn" onclick="document.getElementById(\'{gid}\').classList.toggle(\'show\')">Reveal answers</button>\n'
            f'                <div class="answers" id="{gid}">\n')
    for a in ex['answers']:
        out += f'                    <p>{a}</p>\n'
    return out + '                </div>\n            </div>\n'

def build(L):
    h = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Big Questions">
<title>{L["title"]} · C1 English</title>
{CSS}
</head>
<body>
<div class="container">
    <header>
        <span class="tag">BIG QUESTIONS · PHILOSOPHY · C1 · 50 min</span>
        <h1>{L["title"]}</h1>
        <p>{L["subtitle"]}</p>
    </header>

    <p class="crosslink"><a href="big_questions_dashboard.html">← All the Big Questions</a></p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Ideas</button>
        <button class="tab-btn" onclick="showTab(2)">Grammar — {L["grammar_name"]}</button>
        <button class="tab-btn" onclick="showTab(3)">Think</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>

    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {L["intention"]}</div>
            <div class="note" style="border-left:4px solid #764ba2;">
                <strong>Warm up — have a go, and don't worry about mistakes.</strong> Say whatever comes to mind.
                <ul style="margin:8px 0 0 22px;">
''' + ''.join(f'                    <li>{q}</li>\n' for q in L['warmup']) + '''                </ul>
            </div>

            <h2>The words for today's reading</h2>
            <p>Ten words, four short activities. Try each one out loud before you reveal.</p>
'''
    for letter, grp in zip('ABCD', L['vocab']):
        h += f'\n            <h3>{letter} · {grp["head"]}</h3>\n            <p>{grp["intro"]}</p>\n'
        for s, a in grp['items']:
            h += reveal_item(s, a)
    h += '''
            <h3>Now use them, out loud</h3>
            <div class="discuss">
                <strong>Talk it through before we read:</strong>
                <ul>
''' + ''.join(f'                    <li>{q}</li>\n' for q in L['vocab_talk']) + '''                </ul>
            </div>
        </div>
    </div>

    <div class="tab-content">
        <div class="card">
            <h2>The ideas, in three parts</h2>
            <p>Read each part. After it, answer the quick check from memory first, then take the discussion question.</p>
'''
    for i, p in enumerate(L['parts'], 1):
        h += f'\n            <h3>Part {i} — {p["head"]}</h3>\n            <div class="story-chunk">\n'
        h += ''.join(f'                <p>{x}</p>\n' for x in p['text'])
        h += '            </div>\n' + check(p['check']) + discuss(p['discuss'])
    g = L['grammar']
    h += f'''        </div>
    </div>

    <div class="tab-content">
        <div class="card">
            <h2>Grammar — {g["title"]}</h2>
            <p>{g["intro"]}</p>
''' + ''.join(f'            <div class="note">\n                {n}\n            </div>\n' for n in g['notes'])
    for k, ex in enumerate(g['exercises'], 1):
        ex = dict(ex); ex['title'] = f'{k}. ' + ex['title']
        h += '\n' + gap(f'g{k}Ans', ex)
    h += f'''            <p style="margin-top:14px; color:#666; font-style:italic;">{g["closing"]}</p>
        </div>
    </div>

    <div class="tab-content">
        <div class="card">
            <h2>{L["think"]["title"]}</h2>
            <p>{L["think"]["intro"]}</p>
'''
    for s, a in L['think']['items']:
        h += reveal_item(s, a)
    for t in L['think']['extras']:
        h += f'\n            <h3>{t["head"]}</h3>\n            <div class="discuss">\n                <strong>{t["label"]}</strong>\n                <ul>\n' + ''.join(f'                    <li>{x}</li>\n' for x in t['items']) + '                </ul>\n            </div>\n'
    h += '''        </div>
    </div>

    <div class="tab-content">
        <div class="card">
            <h2>Speak</h2>
            <p>This is the heart of the lesson, so do all of it out loud. The timer is there to keep you going: fill the time with reasons and examples.</p>

            <div class="note">
                <strong>Useful language:</strong> ''' + L['speak']['language'] + '''
            </div>

            <div class="timer">
                <span>Time remaining: <strong><span id="timer-display">4:00</span></strong></span>
                <div class="timer-controls">
                    <button class="duration-btn" onclick="setDuration(this, 3)">3 min</button>
                    <button class="duration-btn active" onclick="setDuration(this, 4)">4 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 5)">5 min</button>
                    <button class="timer-btn" onclick="startTimer()">Start</button>
                    <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
                </div>
            </div>
'''
    for lab, body in L['speak']['tasks']:
        h += f'\n            <div class="speak-prompt">\n                <span class="speak-label">{lab}</span>\n' + ''.join(f'                <p>{x}</p>\n' for x in body) + '            </div>\n'
    h += '''
            <div class="final-discussion">
                <h3>To finish — the bigger questions</h3>
                <ol>
''' + ''.join(f'                    <li>{q}</li>\n' for q in L['speak']['final']) + f'''                </ol>
            </div>
        </div>
    </div>

    <footer>
        Big Questions · {L["title"]} · C1
    </footer>
</div>

{JS}
</body>
</html>
'''
    return h

if __name__ == '__main__':
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'bq_content', '[0-9]*.py'))):
        spec = importlib.util.spec_from_file_location('c', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        out = os.path.join(ROOT, m.L['file'])
        open(out, 'w').write(build(m.L))
        print('built', m.L['file'])
