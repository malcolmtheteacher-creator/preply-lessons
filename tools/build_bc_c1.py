#!/usr/bin/env python3
"""Build C1 'Bet the Company' lessons from content files.

Content lives in tools/bc_c1_content/<slug>.json.  The <style> and <script> are
copied live from the series template (bc_orsted_bet_the_company_c1.html), so
every generated lesson matches it exactly.  Writes bc_<slug>_c1.html.
Usage: python3 tools/build_bc_c1.py [slug ...]   (no args = build all)
"""
import json, os, sys, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "bc_c1_content")
TEMPLATE = open(os.path.join(ROOT, "bc_orsted_bet_the_company_c1.html")).read()
CSS = re.search(r"<style>\n(.*?)</style>", TEMPLATE, re.S).group(1)
JS = re.search(r"<script>\n(.*?)</script>", TEMPLATE, re.S).group(1)

GAP = '<input type="text" placeholder="...">'
REVEAL = '<button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle(\'show\')">{}</button>'


def ul(items, indent="                    "):
    return "\n".join(f"{indent}<li>{x}</li>" for x in items)


def guess(item):
    return f'''            <div class="guess-item">
                <div class="sent">{item["sent"]}</div>
                {REVEAL.format("Reveal")}
                <div class="meaning">{item["meaning"]}</div>
            </div>'''


def vocab(d):
    out = []
    for sec in d["vocab"]:
        out.append(f'            <h3>{sec["heading"]}</h3>')
        if sec.get("intro"):
            out.append(f'            <p>{sec["intro"]}</p>')
        out.extend(guess(i) for i in sec["items"])
    return "\n".join(out)


def story(d):
    out = []
    for p in d["story"]:
        paras = "\n".join(f"                <p>{x}</p>" for x in p["paras"])
        qs = "\n".join(f"                <p>{i}. {q}</p>" for i, q in enumerate(p["checks"], 1))
        ans = "\n".join(f"                    <p><strong>{i}.</strong> {a}</p>" for i, a in enumerate(p["answers"], 1))
        out.append(f'''            <h3>{p["heading"]}</h3>
            <div class="story-chunk">
{paras}
            </div>
            <div class="check">
                <div class="q">Quick check — from memory, then reveal:</div>
{qs}
                {REVEAL.format("Reveal answers")}
                <div class="answers">
{ans}
                </div>
            </div>
            <div class="discuss">
                <strong>Discuss:</strong>
                <ul><li>{p["discuss"]}</li></ul>
            </div>''')
    return "\n\n".join(out)


def grammar(g):
    out = [f'            <h2>Grammar — {g["name"]}</h2>', f'            <p>{g["lead"]}</p>']
    out.extend(f'            <div class="note">\n                {n}\n            </div>' for n in g["notes"])
    for n, ex in enumerate(g["exercises"], 1):
        rows = "\n".join(f"                <p>{t.replace('___', GAP)}</p>" for t in ex["items"])
        ans = "\n".join(f"                    <p>{a}</p>" for a in ex["answers"])
        out.append(f'''
            <h3>{n}. {ex["heading"]}</h3>
            <p>{ex["intro"]}</p>
            <div class="gap-fill">
{rows}
                {REVEAL.format("Reveal answers")}
                <div class="answers">
{ans}
                </div>
            </div>''')
    out.append('            <p style="margin-top:14px; color:#666; font-style:italic;">'
               f'{g["closing"]}</p>')
    return "\n".join(out)


def speak_task(t):
    ps = "\n".join(f"                <p>{x}</p>" for x in t["paras"])
    extra = ""
    if t.get("rooms"):
        extra += '\n                <ul style="margin:6px 0 0 20px; color:#3a2a5a;">\n' + ul(t["rooms"]) + "\n                </ul>"
    if t.get("alts"):
        extra += ('\n                <p style="margin-top:8px;"><strong>Prefer not to use your own organisation? '
                  'Take one of these instead:</strong></p>\n                <ul style="margin:6px 0 0 20px; color:#3a2a5a;">\n'
                  + ul(t["alts"]) + "\n                </ul>")
    return f'''            <div class="speak-prompt">
                <span class="speak-label">{t["label"]}</span>
{ps}{extra}
            </div>'''


def build(d):
    s = d["speak"]
    deeper = "<br><br>\n                ".join(d["deeper"]["note"])
    tasks = "\n\n".join(speak_task(t) for t in s["tasks"])
    cross = (f'    <p class="crosslink">Easier version: <a href="{d["a2b1"]}">read this lesson at A2/B1 level &rarr;</a></p>\n\n'
             if d.get("a2b1") else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Bet the Company">
<title>{d["title"]} · C1</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">BUSINESS ENGLISH · C1 · 50 min</span>
        <h1>{d["h1"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

{cross}
    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Story</button>
        <button class="tab-btn" onclick="showTab(2)">Grammar — {d["grammar"]["name"]}</button>
        <button class="tab-btn" onclick="showTab(3)">Going Deeper</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>

    <!-- TAB 0: KEY WORDS -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>

            <div class="note" style="border-left:4px solid #764ba2;">
                <strong>Before we start.</strong> Talk these through out loud.
            </div>
            <div class="discuss">
                <strong>Discuss:</strong>
                <ul>
{ul(d["warmup"])}
                </ul>
            </div>

            <h2>The vocabulary of this case</h2>
            <p>Ten items. Work through the four activities — say your answer <strong>out loud before you reveal it</strong>.</p>

{vocab(d)}

            <h3>Now use them — out loud</h3>
            <div class="discuss">
                <strong>Before we read:</strong>
                <ul>
{ul(d["vocab_use"])}
                </ul>
            </div>
        </div>
    </div>
    <!-- TAB 1: THE STORY -->
    <div class="tab-content">
        <div class="card">
            <h2>The case, in three parts</h2>
            <p>Read each part. After it, there's a quick check (answer from memory first), then one question to discuss.</p>

{story(d)}
        </div>
    </div>
    <!-- TAB 2: GRAMMAR -->
    <div class="tab-content">
        <div class="card">
{grammar(d["grammar"])}
        </div>
    </div>

    <!-- TAB 3: GOING DEEPER -->
    <div class="tab-content">
        <div class="card">
            <h2>Going deeper</h2>
            <p>{d["deeper"]["figures"]}</p>

            <div class="note">
                {deeper}
            </div>

            <div class="discuss">
                <strong>Talk it through:</strong>
                <ul>
{ul(d["deeper"]["discuss"])}
                </ul>
            </div>
        </div>
    </div>
    <!-- TAB 4: SPEAK -->
    <div class="tab-content">
        <div class="card">
            <h2>Speak</h2>
            <p>{s["intro"]}</p>

            <div class="note">
                <strong>Useful language:</strong> {s["useful"]}
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

{tasks}

            <div class="final-discussion">
                <h3>To finish — the harder questions</h3>
                <ol>
{ul(s["final"])}
                </ol>
            </div>
        </div>
    </div>

    <footer>
        Business English · {d["h1"]} · C1
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
        out = os.path.join(ROOT, f"bc_{slug}_c1.html")
        open(out, "w").write(build(d))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")


if __name__ == "__main__":
    main()
