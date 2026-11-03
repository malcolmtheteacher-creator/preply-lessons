#!/usr/bin/env python3
"""Build the six 'IELTS Spelling Stories' chapters (Maya) from content files.

Content: tools/spelling_story_content/chN.json
Style + script are taken from the design model (the chapter 4 page as first built),
kept in tools/spelling_story_template.html, so every chapter looks and works the same.
Usage: python3 tools/build_spelling_stories.py        (builds all chapters)
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "spelling_story_content")
TEMPLATE = open(os.path.join(HERE, "spelling_story_template.html")).read()
CSS = re.search(r"<style>\n(.*?)</style>", TEMPLATE, re.S).group(1)
JS = re.search(r"<script>\n(.*?)</script>", TEMPLATE, re.S).group(1)
# everything after the ITEMS list is the shared engine
ENGINE = JS[JS.index("\n];") + 3:]
ENGINE = ENGINE.replace("const GROUPS = 4;", "const GROUPS = Math.ceil(ITEMS.length / 4);")
ENGINE = ENGINE.replace(
    'const names = ["Words 1–4", "Words 5–8", "Words 9–12", "Words 13–16"];',
    'const names = Array.from({ length: GROUPS }, (_, i) => "Words " + (i * 4 + 1) + "–" + Math.min(ITEMS.length, i * 4 + 4));')
assert "Math.ceil(ITEMS.length / 4)" in ENGINE and "Array.from({ length: GROUPS }" in ENGINE

EXTRA_CSS = """
.chapters { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin:0 0 16px; font-size:0.8rem; letter-spacing:0; word-spacing:0; }
.chapters a, .chapters span { padding:4px 11px; border-radius:14px; border:1px solid #d9d2c3; background:#fff; color:#4a2f86; text-decoration:none; font-weight:600; }
.chapters span.now { background:#4a2f86; color:#fff; border-color:#4a2f86; }
.chapters a.all { background:#f3ecdc; }
"""
NUMWORDS = {16: "Sixteen", 24: "Twenty-four"}


def chapter_nav(chapters, n):
    bits = []
    for c in chapters:
        if c["n"] == n:
            bits.append(f'<span class="now">{c["n"]} · {c["title"]}</span>')
        else:
            bits.append(f'<a href="{c["file"]}">{c["n"]} · {c["title"]}</a>')
    bits.append('<a class="all" href="ielts_spelling_stories_dashboard.html">All chapters →</a>')
    return '    <nav class="chapters" aria-label="Chapters">' + "".join(bits) + "</nav>"


def build(d, chapters):
    n = d["n"]
    count = len(d["items"])
    paras = "\n".join(
        f'''            <div class="para" data-n="{i}">
                <p>{p}</p>
                <button class="say" onclick="readPara(this)">🔊 Read to me</button>
            </div>''' for i, p in enumerate(d["paras"], 1))
    form = "\n".join(
        f'''                <p>{i}. {before} <button class="hear" onclick="say('{word}')">🔊</button> ______ {after}</p>'''
        for i, (before, word, after) in enumerate(d["form"], 1))
    form_ans = " · ".join(f"{i}. {w}" for i, (_, w, _a) in enumerate(d["form"], 1))
    items_js = "const ITEMS = [\n" + ",\n".join("  " + json.dumps(it, ensure_ascii=False) for it in d["items"]) + "\n];"
    think = d.get("think") or ("Which helped you most today: hearing the word, seeing it in parts, or the memory trick? "
                               "Which word is still the hardest for you — and what trick could you invent for it?")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="IELTS Spelling Stories">
<title>IELTS Spelling Story {n}: {d["title"]} · B2</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap" rel="stylesheet">
<style>
{CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
    <header>
        <span class="tag">IELTS Spelling Story · Chapter {n} of 6 · B2 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]} {NUMWORDS.get(count, str(count))} words that IELTS candidates often spell wrong — learned four at a time.</p>
    </header>

{chapter_nav(chapters, n)}

    <nav>
        <button class="tab-btn active" onclick="show(0)">1 · The Story</button>
        <button class="tab-btn" onclick="show(1)">2 · Meet the Words</button>
        <button class="tab-btn" onclick="show(2)">3 · Spell Them</button>
        <button class="tab-btn" onclick="show(3)">4 · Use Them</button>
    </nav>

    <!-- 1 STORY -->
    <div class="tab active">
        <div class="card">
            <h2>Read the story</h2>
            <p class="lead">Let's start with the story. The <b style="background:#efe8fb;color:#3b2275;padding:0 3px;border-radius:4px;">highlighted</b> words are the ones to learn. Read slowly. Press 🔊 to hear a part read aloud.</p>

            <div class="tools">
                <span>Reading tools:</span>
                <button class="tool" onclick="textSize(-1)">A−</button>
                <button class="tool" onclick="textSize(1)">A+</button>
                <button class="tool" id="spacingBtn" onclick="toggleSpacing()">More space</button>
                <button class="tool" id="focusBtn" onclick="toggleFocus()">One part at a time</button>
            </div>
            <div class="focus-nav">
                <button class="btn ghost" onclick="stepFocus(-1)">← Back</button>
                <button class="btn" onclick="stepFocus(1)">Next part →</button>
            </div>

{paras}

            <h3>Talk about it</h3>
            <p>{d["discuss"]}</p>
        </div>
    </div>

    <!-- 2 MEET THE WORDS -->
    <div class="tab">
        <div class="card">
            <h2>Meet the words — four at a time</h2>
            <p class="lead">Each word is split into small parts. The <mark style="background:#ffe28a;border-radius:4px;padding:0 2px;">yellow</mark> part is where people make mistakes. For each word: <strong>hear it → say it in parts → read the trick</strong>. Then press <strong>Hide the words</strong> and try to spell all four out loud.</p>

            <div class="groups" id="groupBtns"></div>
            <div id="wordArea" class="wcards"></div>
            <div class="bar">
                <button class="btn" id="hideBtn" onclick="toggleHide()">Hide the words</button>
                <button class="btn ghost" onclick="hearGroup()">🔊 Hear these four</button>
                <button class="btn ghost" onclick="nextGroup()">Next four →</button>
            </div>
        </div>
    </div>

    <!-- 3 SPELL THEM -->
    <div class="tab">
        <div class="card">
            <h2>Spell them — one word at a time</h2>
            <p class="lead">Press 🔊, listen, read the clue, then type the word. If a letter is wrong, you will see <strong>which letters are already right</strong>. You get a second try before the answer appears.</p>

            <div class="quiz">
                <div class="progress" id="progress"></div>
                <button class="hear" style="width:56px;height:56px;font-size:1.5rem;" onclick="say(ITEMS[qi].w)" title="Hear the word">🔊</button>
                <div class="qclue" id="qclue"></div>
                <div class="qpos" id="qpos"></div>
                <input class="qinput" id="qinput" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="type here" onkeydown="if(event.key==='Enter')checkWord()">
                <div class="letters" id="letters"></div>
                <div class="qmsg" id="qmsg"></div>
                <div class="reveal" id="reveal"></div>
                <div class="bar" style="justify-content:center;">
                    <button class="btn" id="checkBtn" onclick="checkWord()">Check</button>
                    <button class="btn ghost" onclick="nextWord()">Next word →</button>
                </div>
                <div class="final" id="final"></div>
            </div>
            <p style="margin-top:14px;font-size:0.9rem;color:#6b5a3a;">In IELTS Listening, a correct word that is spelled wrongly scores <strong>zero</strong>. British and American spellings are both accepted — just be consistent.</p>
        </div>
    </div>

    <!-- 4 USE THEM -->
    <div class="tab">
        <div class="card">
            <h2>Use the words</h2>

            <div class="task">
                <span class="lbl">Speaking</span>
                <p>{d["speaking"]}</p>
            </div>

            <div class="task">
                <span class="lbl">Listening practice — form filling</span>
                <p>{d["form_intro"]}</p>
{form}
                <p><button class="btn ghost" onclick="document.getElementById('formAns').classList.toggle('show')">Check the answers</button></p>
                <p class="answers" id="formAns">{form_ans}</p>
            </div>

            <div class="task">
                <span class="lbl">Writing (IELTS practice)</span>
                <p>Write four or five sentences: <em>"{d["writing_q"]}"</em> Use and spell correctly: <strong>{d["writing_words"]}.</strong></p>
                <textarea aria-label="Your sentences" placeholder="Write here..."></textarea>
            </div>

            <div class="task">
                <span class="lbl">Think back</span>
                <p>{think}</p>
            </div>
        </div>
    </div>

    <footer>IELTS Spelling Stories · Chapter {n}: {d["title"]} · B2</footer>
</div>

<script>
// w = word, c = the word in parts (the tricky part inside [ ]), clue must NOT spell the word
{items_js}{ENGINE}</script>
</body>
</html>
'''


def check(d):
    problems = []
    story = " ".join(d["paras"]).lower()
    bold = {b.lower() for b in re.findall(r"<b>([^<]+)</b>", " ".join(d["paras"]))}
    for it in d["items"]:
        if re.sub(r"[\[\]|]", "", it["c"]) != it["w"]:
            problems.append(f'chunks do not spell {it["w"]}: {it["c"]}')
        if it["w"].lower() not in bold:
            problems.append(f'{it["w"]} is not highlighted in the story')
        if it["w"].lower() in it["clue"].lower():
            problems.append(f'clue gives away {it["w"]}')
    extra = bold - {it["w"].lower() for it in d["items"]}
    if extra:
        problems.append(f"highlighted but not taught: {sorted(extra)}")
    return problems


CARD_ICON = {1: "✈️", 2: "💼", 3: "🏠", 4: "🎤", 5: "🤒", 6: "🎓"}


def build_dashboard(chapters):
    total = sum(len(c["items"]) for c in chapters)
    cards = []
    for c in chapters:
        sample = " · ".join(it["w"] for it in c["items"][:4])
        cards.append(f"""        <a class="ch" href="{c["file"]}">
            <div class="ch-top"><span class="ch-num">Chapter {c["n"]}</span><span class="ch-icon">{CARD_ICON.get(c["n"], "📖")}</span></div>
            <h3>{c["title"]}</h3>
            <p>{c["subtitle"]}</p>
            <div class="ch-words"><b>{len(c["items"])} words</b> · {sample} …</div>
            <span class="go">Open chapter →</span>
        </a>""")
    cards = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="IELTS Spelling Stories">
<title>IELTS Spelling Stories · B2 · Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Lexend", Verdana, Tahoma, sans-serif; background:#fbf7ee; color:#2b2b2b; font-size:17px; line-height:1.7; }}
.wrap {{ max-width:1000px; margin:0 auto; padding:20px 20px 60px; }}
header {{ background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:#fff; padding:44px 28px 38px; text-align:center; border-radius:16px; box-shadow:0 10px 30px rgba(102,126,234,0.22); margin-bottom:22px; }}
header .tag {{ display:inline-block; padding:4px 14px; background:rgba(255,255,255,0.2); border-radius:14px; font-size:0.75rem; font-weight:600; letter-spacing:0.06em; margin-bottom:12px; }}
header h1 {{ font-size:2.3rem; line-height:1.2; margin-bottom:10px; }}
header p {{ max-width:640px; margin:0 auto; opacity:0.95; }}
.back {{ display:inline-block; margin:0 0 16px; color:#4a2f86; font-weight:600; font-size:0.9rem; text-decoration:none; }}
.intro {{ background:#fffdf8; border:1px solid #e8e0cf; border-radius:14px; padding:22px 26px; margin-bottom:22px; }}
.intro p {{ margin-bottom:10px; }}
.intro p:last-child {{ margin-bottom:0; }}
.stats {{ display:flex; flex-wrap:wrap; gap:12px; margin:14px 0 4px; }}
.stat {{ background:#f3ecdc; border-radius:10px; padding:10px 16px; font-size:0.9rem; }}
.stat b {{ display:block; font-size:1.4rem; color:#4a2f86; line-height:1.2; }}
h2 {{ color:#4a2f86; font-size:1.35rem; margin:26px 0 12px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); gap:16px; }}
.ch {{ display:flex; flex-direction:column; background:#fff; border:1px solid #e3dccb; border-top:5px solid #764ba2; border-radius:12px; padding:18px 20px; text-decoration:none; color:inherit; transition:transform .15s, box-shadow .15s; }}
.ch:hover {{ transform:translateY(-3px); box-shadow:0 8px 20px rgba(74,47,134,0.12); }}
.ch-top {{ display:flex; justify-content:space-between; align-items:center; }}
.ch-num {{ font-size:0.75rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#8a7d62; }}
.ch-icon {{ font-size:1.6rem; }}
.ch h3 {{ font-size:1.25rem; color:#3b2275; margin:4px 0 4px; }}
.ch p {{ font-size:0.95rem; color:#4a4a3a; margin-bottom:10px; }}
.ch-words {{ font-size:0.85rem; color:#6b5a3a; background:#f7f2e6; border-radius:8px; padding:7px 10px; margin-top:auto; }}
.ch-words b {{ color:#4a2f86; }}
.go {{ margin-top:12px; font-weight:700; color:#764ba2; font-size:0.9rem; }}
.steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; }}
.step {{ background:#fffdf8; border:1px solid #e8e0cf; border-radius:12px; padding:14px 16px; }}
.step .n {{ font-weight:700; color:#4a2f86; margin-bottom:4px; }}
.step p {{ font-size:0.9rem; color:#4a4a3a; }}
.more {{ display:flex; flex-wrap:wrap; gap:10px; }}
.more a {{ background:#fff; border:1px solid #d9d2c3; border-radius:20px; padding:7px 15px; color:#4a2f86; text-decoration:none; font-weight:600; font-size:0.9rem; }}
.more a:hover {{ background:#f3ecdc; }}
footer {{ text-align:center; color:#8a7d62; font-size:0.8rem; margin-top:34px; }}
@media (max-width:768px) {{ header h1 {{ font-size:1.7rem; }} .intro {{ padding:18px; }} }}
</style>
</head>
<body>
<div class="wrap">
    <a class="back" href="https://malcolmhyndman.com/#cat-ielts">← IELTS lessons</a>
    <header>
        <span class="tag">IELTS · Listening, Reading &amp; Writing · B2</span>
        <h1>IELTS Spelling Stories</h1>
        <p>Follow Maya through six chapters of her life abroad — and learn to spell the {total} words IELTS candidates get wrong most often.</p>
    </header>

    <div class="intro">
        <p><strong>Why spelling matters in IELTS.</strong> In the Listening and Reading tests, a correct answer that is spelled wrongly scores <strong>zero</strong>. In Writing, spelling mistakes pull down your vocabulary score. A few dozen common words cause most of the damage.</p>
        <p>Each chapter is a short story with the key words highlighted. The words are taught a few at a time, split into small parts, with a memory trick for each — then you spell them one by one, with help that shows which letters you already have right.</p>
        <div class="stats">
            <div class="stat"><b>6</b>chapters</div>
            <div class="stat"><b>{total}</b>words, no repeats</div>
            <div class="stat"><b>B2</b>level</div>
            <div class="stat"><b>50 min</b>per chapter</div>
        </div>
    </div>

    <h2>The chapters — read them in order</h2>
    <div class="grid">
{cards}
    </div>

    <h2>How each chapter works</h2>
    <div class="steps">
        <div class="step"><div class="n">1 · The Story</div><p>Read Maya's story. Every highlighted word is one to learn. Press 🔊 to hear any part read aloud.</p></div>
        <div class="step"><div class="n">2 · Meet the Words</div><p>Four words at a time, split into parts, the tricky letters in yellow, and a memory trick for each.</p></div>
        <div class="step"><div class="n">3 · Spell Them</div><p>One word at a time: hear it, read the clue, type it. See which letters are right before the answer appears.</p></div>
        <div class="step"><div class="n">4 · Use Them</div><p>Speak with the words, fill in an IELTS-style listening form, and write a short Task 2 answer.</p></div>
    </div>

    <h2>More spelling practice</h2>
    <div class="more">
        <a href="ielts-spelling-diagnostic.html">🩺 Spelling Diagnostic</a>
        <a href="ielts-spelling-gym.html">🏋️ Spelling Gym</a>
        <a href="ielts_spelling_master.html">🏆 Spelling Master</a>
        <a href="qf_spelling_accommodate.html">Quick Fix: accommodate</a>
        <a href="qf_spelling_necessary.html">Quick Fix: necessary</a>
        <a href="qf_spelling_their_they_re.html">Quick Fix: their / they're</a>
        <a href="ielts_ww_anagram_spelling.html">🔀 Spelling Anagrams</a>
    </div>

    <footer>IELTS Spelling Stories · B2</footer>
</div>
</body>
</html>
"""


def main():
    chapters = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(CONTENT, "ch*.json")))]
    chapters.sort(key=lambda c: c["n"])
    seen = {}
    ok = True
    for d in chapters:
        for it in d["items"]:
            w = it["w"].lower()
            if w in seen:
                print(f'  ✗ "{it["w"]}" is in chapter {seen[w]} and chapter {d["n"]}'); ok = False
            seen[w] = d["n"]
        for pr in check(d):
            print(f'  ✗ chapter {d["n"]}: {pr}'); ok = False
    if not ok:
        raise SystemExit("Fix the content before building.")
    for d in chapters:
        out = os.path.join(ROOT, d["file"])
        open(out, "w").write(build(d, chapters))
        print(f'  wrote {d["file"]}  (chapter {d["n"]}, {len(d["items"])} words)')
    open(os.path.join(ROOT, "ielts_spelling_stories_dashboard.html"), "w").write(build_dashboard(chapters))
    print("  wrote ielts_spelling_stories_dashboard.html")
    print(f"  {len(seen)} words across {len(chapters)} chapters")


if __name__ == "__main__":
    main()
