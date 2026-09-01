#!/usr/bin/env python3
"""Build A2/B1 companion lessons for the 'Bet the Company' business-case series.

Content lives in tools/bc_a2b1_content/<slug>.json.  This script wraps it in the
series template and writes bc_<slug>_a2b1.html into the gitsite root.
Re-run any time; it overwrites its own output only.
"""
import json, os, sys, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bc_a2b1_content")

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bc_a2b1_template.css")).read()
JS  = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bc_a2b1_template.js")).read()


def esc(s):
    return s  # content files may contain intentional inline <b>/<em>


def vocab_cards(items):
    out = []
    for v in items:
        out.append(f'''                <div class="vocab-card" onclick="this.classList.toggle('revealed')">
                    <div class="word">{esc(v["word"])}</div>
                    <div class="pos">{esc(v["pos"])}</div>
                    <div class="def">{esc(v["def"])}</div>
                    <div class="ex">"{esc(v["ex"])}"</div>
                </div>''')
    return "\n".join(out)


def gapfill(items, answers, intro=None):
    rows = "\n".join(f'                <p>{i+1}. {esc(t)}</p>'.replace("___", '<input type="text">')
                     for i, t in enumerate(items))
    ans = " &nbsp;·&nbsp; ".join(f"<strong>{i+1}. {a}</strong>" for i, a in enumerate(answers))
    lead = f'            <p>{esc(intro)}</p>\n' if intro else ""
    return f'''{lead}            <div class="gap-fill">
{rows}
                <button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle('show')">Check my answers</button>
                <div class="answers">
                    <p>{ans}</p>
                </div>
            </div>'''


def tf_block(items):
    rows = []
    for i, (q, is_true) in enumerate(items, 1):
        t_arg = "true" if is_true else "false"
        f_arg = "false" if is_true else "true"
        rows.append(f'''                <p>{i}. {esc(q)}
                   <button onclick="tf(this,{t_arg})">True</button><button onclick="tf(this,{f_arg})">False</button></p>''')
    return '''            <div class="tf">
                <p class="q"><b>True or false?</b> Click your answer.</p>
''' + "\n".join(rows) + '''
            </div>'''


def discuss(title, items):
    lis = "\n".join(f"                    <li>{esc(i)}</li>" for i in items)
    return f'''            <div class="discuss">
                <strong>{esc(title)}</strong>
                <ul>
{lis}
                </ul>
            </div>'''


def story_part(p):
    paras = "\n".join(f"                <p>{esc(x)}</p>" for x in p["paras"])
    out = [f'            <h3>{esc(p["heading"])}</h3>',
           '            <div class="story-chunk">', paras, '            </div>',
           tf_block(p["tf"]), discuss("Talk about it", p["discuss"])]
    return "\n".join(out)


def speak_prompt(s):
    ps = "\n".join(f"                <p>{esc(x)}</p>" for x in s["paras"])
    helper = ""
    if s.get("helper"):
        chips = "".join(f"<span>{esc(c)}</span>" for c in s["helper"])
        helper = f'\n                <div class="helper"><strong>Use these:</strong> {chips}</div>'
    return f'''            <div class="speak-prompt">
                <span class="speak-label">{esc(s["label"])}</span>
{ps}{helper}
            </div>'''


def build(d):
    slug = d["slug"]
    vocab_gap = gapfill(d["vocab_practice"]["items"], d["vocab_practice"]["answers"],
                        "Write one word from the cards in each gap.")
    parts = "\n\n".join(story_part(p) for p in d["story"])
    g = d["grammar"]
    g_tables = ""
    if g.get("table"):
        rows = "\n".join("                <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                         for r in g["table"]["rows"])
        heads = "".join(f"<th>{c}</th>" for c in g["table"]["head"])
        g_tables = f'''            <table class="verb-table">
                <tr>{heads}</tr>
{rows}
            </table>'''
    g_expl = "\n".join(f'            <p>{esc(x)}</p>' for x in g["explain"])
    g_ex1 = gapfill(g["practice"]["items"], g["practice"]["answers"], g["practice"].get("intro"))
    g_fix = ""
    if g.get("fix"):
        rows = "\n".join(f'                <p>{i+1}. {esc(t)}</p>' for i, t in enumerate(g["fix"]["items"]))
        ans = "\n".join(f'                    <p><strong>{i+1}.</strong> {a}</p>' for i, a in enumerate(g["fix"]["answers"]))
        g_fix = f'''
            <h3>{esc(g["fix"]["heading"])}</h3>
            <p>{esc(g["fix"].get("intro", "Each sentence has one mistake. Say the correct sentence out loud, then check."))}</p>
            <div class="gap-fill">
{rows}
                <button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle('show')">Check my answers</button>
                <div class="answers">
{ans}
                </div>
            </div>'''
    speaks = "\n\n".join(speak_prompt(s) for s in d["speak"])
    finals = "\n".join(f"                    <li>{esc(x)}</li>" for x in d["final"])
    vocab_talk = discuss("Talk about it", d["vocab_discuss"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Bet the Company">
<title>{esc(d["title"])} · A2/B1</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">BUSINESS ENGLISH · A2/B1 · 50 min</span>
        <h1>{esc(d["title"])}</h1>
        <p>{esc(d["subtitle"])}</p>
    </header>

    <p class="crosslink">Harder version: <a href="{esc(d["c1"])}">read this lesson at C1 level &rarr;</a></p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Story</button>
        <button class="tab-btn" onclick="showTab(2)">Grammar — {esc(g["name"])}</button>
        <button class="tab-btn" onclick="showTab(3)">Speak</button>
    </nav>

    <!-- WORDS -->
    <div class="tab-content active">
        <div class="card">
            <h2>Ten words you need</h2>
            <p>Look at each word. Say what you think it means. Then tap the card.</p>
            <p class="tap-hint">Tap a card to see the meaning.</p>

            <div class="vocab-grid">
{vocab_cards(d["vocab"])}
            </div>

            <h3>Choose the right word</h3>
{vocab_gap}

{vocab_talk}
        </div>
    </div>

    <!-- STORY -->
    <div class="tab-content">
        <div class="card">
            <h2>The story, in three parts</h2>
            <p>Read each part. Then answer the questions before you read the next part.</p>

{parts}
        </div>
    </div>

    <!-- GRAMMAR -->
    <div class="tab-content">
        <div class="card">
            <h2>{esc(g["heading"])}</h2>
{g_expl}
{g_tables}

            <h3>{esc(g["practice"]["heading"])}</h3>
{g_ex1}
{g_fix}
        </div>
    </div>

    <!-- SPEAK -->
    <div class="tab-content">
        <div class="card">
            <h2>Speaking</h2>
            <p>Take your time. Short sentences are fine.</p>

            <div class="timer">
                <span>Time: <strong><span id="timer-display">3:00</span></strong></span>
                <div class="timer-controls">
                    <button class="duration-btn active" onclick="setDuration(this, 3)">3 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 4)">4 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 5)">5 min</button>
                    <button class="timer-btn" onclick="startTimer()">Start</button>
                    <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
                </div>
            </div>

{speaks}

            <div class="final-discussion">
                <h3>If we have time</h3>
                <ol>
{finals}
                </ol>
            </div>
        </div>
    </div>

    <footer>
        Business English · {esc(d["title"])} · A2/B1
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''


def main():
    targets = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for slug in targets:
        d = json.load(open(os.path.join(CONTENT, slug + ".json")))
        out = os.path.join(ROOT, f"bc_{slug}_a2b1.html")
        open(out, "w").write(build(d))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")


if __name__ == "__main__":
    main()
