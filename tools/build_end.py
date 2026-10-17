#!/usr/bin/env python3
"""Build the 'Begin With the End' pathway (C1, three lessons) from content files.

  tools/end_content/NN_<slug>.json  ->  end_<slug>_c1.html   (one lesson each)
  (all lessons)                     ->  begin_with_the_end_dashboard.html

Reuses the Think Inside the Box engine (build_tib.py): same five tabs
(Key Words, The Story, The Tool, Grammar, Speak), same diagrams, recoloured navy.
Usage: python3 tools/build_end.py     (always rebuilds everything)
"""
import json, os, re, glob, itertools, html

import build_tib as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "end_content")
SERIES = "Begin With the End"
DASH = "begin_with_the_end_dashboard.html"
E = html.escape

NAVY = {"#0e7490": "#1e4e8c", "#0f766e": "#1b3a6b", "#115e59": "#17325c", "#134e4a": "#12284a",
        "#7cc4bb": "#8fb0d9", "#99d5cc": "#a9c4e6", "#c5e6e1": "#cbdaee", "#e2f4f1": "#e4edf8",
        "#cdeae5": "#d3e1f1", "#f1f9f8": "#f2f6fb", "#eaf6f4": "#ecf2f9", "#e3f2ef": "#e6eef8",
        "#cfe7e3": "#d6e3f2", "#f5fbfa": "#f6f9fd", "#1f3d3a": "#1d2f4d", "#eef7f6": "#eef3fa",
        "#f7fbfa": "#f7f9fd", "rgba(14,116,144,": "rgba(30,78,140,"}


def navy(s):
    for a, b in NAVY.items():
        s = s.replace(a, b)
    return s


# diagrams are drawn by build_tib with its module-level colours
T.INK, T.TEAL, T.LIGHT = "#1d2f4d", "#1b3a6b", "#e4edf8"
T.TONES.update({"t": "#d3e1f1", "b": "#d6e4f5", "n": "#eef2f7"})
CSS = navy(T.CSS)
JS = T.JS


def practice_tab(pr):
    groups = "".join(
        f'<h3>{E(g["title"])}</h3><p class="pr-intro">{g["intro"]}</p><ol class="pr-q">' + "".join(f"<li>{q}</li>" for q in g["questions"]) + "</ol>"
        for g in pr["groups"])
    models = "".join(
        f'<details class="pr-model"><summary>{m["q"]}</summary><p><strong>Point:</strong> {m["point"]}</p><p><strong>Reason:</strong> {m["reason"]}</p><p><strong>Stop:</strong> {m["stop"]}</p></details>'
        for m in pr["models"])
    steps = "".join(f"<li>{x}</li>" for x in pr["steps"])
    harder = "".join(f"<li>{x}</li>" for x in pr["harder"])
    return f'''    <!-- TAB 5 -->
    <div class="tab-content">
        <div class="card">
            <style>
            .pr-intro{{color:#555;margin:2px 0 8px}} .pr-q{{margin:0 0 14px 22px}} .pr-q li{{margin:5px 0}}
            .pr-model{{background:#f2f6fb;border:1px solid #d3e1f1;border-radius:8px;padding:10px 16px;margin:8px 0}}
            .pr-model summary{{cursor:pointer;font-weight:600;color:#1b3a6b}} .pr-model p{{margin:8px 0 0}}
            </style>
            <h2>Practice</h2>
            <p>{pr["intro"]}</p>
            <div class="note"><strong>Each time:</strong><ol style="margin:8px 0 0 22px">{steps}</ol></div>
            <h2>The questions</h2>
            {groups}
            <h2>How it sounds</h2>
            <p>Six examples of the shape. Try the question first, then open the answer.</p>
            {models}
            <h2>Make it harder</h2>
            <ul style="margin:6px 0 0 22px">{harder}</ul>
        </div>
    </div>

'''


def lesson(d, lessons):
    i = [x["slug"] for x in lessons].index(d["slug"])
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    strip = [f'<a href="{DASH}">The whole pathway</a>']
    if prev:
        strip.insert(0, f'<a href="end_{prev["slug"]}_c1.html">&larr; {prev["title"]}</a>')
    if nxt:
        strip.append(f'<a href="end_{nxt["slug"]}_c1.html">{nxt["title"]} &rarr;</a>')
    body = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{d["title"]} · C1 English</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">BEGIN WITH THE END · {d["num"]} OF 3 · C1 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <p class="series-strip">{" &nbsp;·&nbsp; ".join(strip)}</p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Story</button>
        <button class="tab-btn" onclick="showTab(2)">The Tool</button>
        <button class="tab-btn" onclick="showTab(3)">Language — {d["grammar"]["name"]}</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>

    <!-- TAB 0 -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>
            <div class="discuss">
                <strong>Before we start — talk these through:</strong>
                <ul>
{T.ul(d["warmup"])}
                </ul>
            </div>

            <h2>The vocabulary of this story</h2>
            <p>Ten items. Say your answer <strong>out loud before you reveal it</strong>.</p>

{T.vocab(d)}

            <h3>Now use them — out loud</h3>
            <div class="discuss">
                <strong>Before we read:</strong>
                <ul>
{T.ul(d["vocab_use"])}
                </ul>
            </div>
        </div>
    </div>

    <!-- TAB 1 -->
    <div class="tab-content">
        <div class="card">
            <h2>The story, in three parts</h2>
            <p>Read each part. After it, answer the quick check from memory, then discuss one question.</p>

{T.story(d)}
        </div>
    </div>

    <!-- TAB 2 -->
    <div class="tab-content">
        <div class="card">
{T.tool_tab(d["tool_tab"])}
        </div>
    </div>

    <!-- TAB 3 -->
    <div class="tab-content">
        <div class="card">
{T.grammar(d["grammar"]).replace("Grammar — ", "Language — ")}
        </div>
    </div>

    <!-- TAB 4 -->
    <div class="tab-content">
        <div class="card">
{T.speak(d["speak"])}
        </div>
    </div>

    <footer>
        {SERIES} · {d["title"]} · C1
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''
    if d.get("practice"):
        body = body.replace('        <button class="tab-btn" onclick="showTab(4)">Speak</button>',
            '        <button class="tab-btn" onclick="showTab(4)">Speak</button>\n        <button class="tab-btn" onclick="showTab(5)">Practice</button>', 1)
        body = body.replace('    <footer>', practice_tab(d["practice"]) + '    <footer>', 1)
    return body


def dashboard(lessons):
    cards = []
    for d in lessons:
        c = d["card"]
        cards.append(f'''        <a class="story-card" href="end_{d["slug"]}_c1.html">
            <div class="story-num">LESSON {d["num"]} &middot; {c["shape"]}</div>
            <div class="story-title">{d["title"]}</div>
            <div class="story-author">{c["who"]}</div>
            <div class="story-essence">{c["essence"]}</div>
            <div class="story-turn"><span>The tool:</span> {d["tool"]}</div>
            <div class="story-foot"><span class="grammar-tag">{d["grammar"]["name"]}</span><span class="go">Open &rarr;</span></div>
        </a>''')
    dash_css = navy(T.recolour(re.search(r"<style>\n(.*?)</style>", open(os.path.join(ROOT, "true_science_stories_dashboard.html")).read(), re.S).group(1)))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>Begin With the End · C1</title>
<style>
{dash_css}
.flow {{ display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin: 6px 0 26px; }}
.flow .step {{ background:white; border:1px solid #cbdaee; border-radius:14px; padding:12px 18px; text-align:center; min-width:150px; box-shadow:0 2px 8px rgba(0,0,0,.04); }}
.flow .step b {{ display:block; color:#1b3a6b; font-size:1.05rem; }}
.flow .step span {{ font-size:.85rem; color:#556; }}
.idea {{ background:white; border:1px solid #cbdaee; border-radius:14px; padding:18px 14px 10px; margin-bottom:26px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,.04); }}
.idea svg {{ max-width:100%; height:auto; }}
.idea-cap {{ color:#1d2f4d; font-weight:600; margin:2px 0 8px; }}
.who {{ background:#f2f6fb; border-left:4px solid #1e4e8c; border-radius:0 12px 12px 0; padding:16px 22px; margin-bottom:26px; }}
.who h2 {{ font-size:1.1rem; color:#1b3a6b; margin-bottom:6px; }}
.who p {{ color:#3a3a4a; line-height:1.7; margin:0; }}
.flow .arrow {{ align-self:center; color:#1e4e8c; font-size:1.4rem; }}
</style>
</head>
<body>
<div class="container">
    <header style="padding:56px 26px; background: linear-gradient(135deg, #1e4e8c 0%, #12284a 100%);">
        <span class="tag">True stories &middot; professional speaking &middot; C1</span>
        <h1>Begin With the End</h1>
        <p class="subtitle">Know where you will land before you open your mouth. Three lessons on speaking like someone who is in control of the room.</p>
    </header>

    <div class="intro">
        <p>Most speaking problems that sound like <em>fillers</em>, <em>long answers</em> and <em>lost sentences</em> have one cause: starting to talk before you know where the sentence is going. The cure is the oldest advice about communication &mdash; <strong>begin with the end in mind</strong>.</p>
        <p>Each lesson tells a true story, teaches one tool you can use the same day, practises the language it needs, and ends with a lot of speaking. They build on each other, so take them in order.</p>
    </div>

    <div class="idea">
        <svg viewBox="0 0 900 230" width="900" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A dashed path rising from a small circle on the left and landing exactly on a target on the right, with the labels point, reason and stop">
            <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#1b3a6b"/></marker></defs>
            <circle cx="60" cy="170" r="14" fill="#cbdaee" stroke="#1b3a6b" stroke-width="2"/>
            <text x="60" y="206" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="13" fill="#556">before you speak</text>
            <path d="M74,166 C250,30 520,30 760,150" fill="none" stroke="#1b3a6b" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round" marker-end="url(#ah)"/>
            <circle cx="800" cy="170" r="46" fill="#e4edf8" stroke="#1b3a6b" stroke-width="2"/>
            <circle cx="800" cy="170" r="30" fill="#cbdaee" stroke="#1b3a6b" stroke-width="2"/>
            <circle cx="800" cy="170" r="13" fill="#1b3a6b"/>
            <text x="800" y="236" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="13" fill="#556">the landing</text>
            <g font-family="Segoe UI, sans-serif" font-size="15" font-weight="700" fill="#1b3a6b" text-anchor="middle">
                <text x="250" y="62">1 &middot; POINT first</text>
                <text x="450" y="38">2 &middot; one REASON</text>
                <text x="650" y="62">3 &middot; STOP</text>
            </g>
        </svg>
        <p class="idea-cap">Decide where you will land. Then say it first, give one reason, and stop.</p>
    </div>

    <div class="who">
        <h2>Who it is for</h2>
        <p>Anyone who speaks English at work and already speaks it well &mdash; managers, specialists, presenters, people who sit in meetings where seniority is judged in seconds. If you talk too long, lose your sentence, fill silences, or give way too fast when challenged, this is the pathway. No grammar from scratch: the language here is the language of control.</p>
    </div>

    <p class="section-label">The pathway</p>
    <div class="flow">
        <div class="step"><b>Land it</b><span>point &middot; reason &middot; stop</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Pause it</b><span>a beat instead of &ldquo;um&rdquo;</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Hold it</b><span>stay calm under pushback</span></div>
    </div>

    <p class="section-label">The three lessons</p>
    <div class="story-grid">
{chr(10).join(cards)}
    </div>

    <div class="how">
        <h2>How each lesson works</h2>
        <div class="how-steps">
            <div class="how-step"><div class="n">1 &middot; Key Words</div><p>Ten words from the story, worked out before you read.</p></div>
            <div class="how-step"><div class="n">2 &middot; The Story</div><p>A true story in three parts, with a check and a talking point after each.</p></div>
            <div class="how-step"><div class="n">3 &middot; The Tool</div><p>A simple method, a chance to try it, and where it breaks.</p></div>
            <div class="how-step"><div class="n">4 &middot; Language</div><p>The grammar and phrases the tool needs.</p></div>
            <div class="how-step"><div class="n">5 &middot; Speak</div><p>Timed speaking tasks, then harder questions.</p></div>
        </div>
    </div>

    <footer>{SERIES} &middot; C1</footer>
</div>
</body>
</html>
'''


def check(d):
    n_items = sum(len(s["items"]) for s in d["vocab"])
    assert n_items == 10, f'{d["slug"]}: {n_items} vocab items, want 10'
    # vocab-activity guard (2026-10-15): B must give the student a pool of terms, C must be real collocation gaps
    vb, vc = d["vocab"][1], d["vocab"][2]
    assert vb["heading"].startswith(("B · Which term means", "B · Which word matches")), f'{d["slug"]}: vocab B must be "Which term means…?" with the terms listed'
    assert vb["intro"].count("·") >= 2, f'{d["slug"]}: vocab B intro must list the three terms (a · b · c)'
    assert all("<b>" in it["sent"] for it in vb["items"]), f'{d["slug"]}: vocab B questions must quote a definition in bold'
    answers = [re.search(r"<b>(.*?)</b>", it["meaning"]).group(1).lower() for it in vb["items"]]
    listed = [t.strip().lower() for t in vb["intro"].split(":", 1)[1].split(".")[0].split("·")]
    assert sorted(answers) == sorted(listed), f'{d["slug"]}: vocab B intro terms must match the answers {answers}'
    assert not any(a == l for a, l in zip(answers, listed)), f'{d["slug"]}: vocab B terms are listed in the same order as the answers - shuffle the intro list'
    assert vc["heading"].startswith("C · Which word completes all three phrases"), f'{d["slug"]}: vocab C must be the collocation gap-fill'
    assert all(it["sent"].count("___") == 3 for it in vc["items"]), f'{d["slug"]}: each vocab C item needs three phrases with ___'
    assert "Which expression fits" not in json.dumps(d), f'{d["slug"]}: vague "Which expression fits" activity is banned'
    sort = d["tool_tab"]["sort"]
    ans = [it["answer"] for it in sort["items"]]
    assert all(a in sort["options"] for a in ans), f'{d["slug"]}: sort answer not in options'
    assert max(len(list(g)) for _, g in itertools.groupby(ans)) < 3, f'{d["slug"]}: same sort answer 3 in a row'
    for c in d["tool_tab"]["cousins"]:
        if c.get("lesson") and not c["lesson"].startswith(("end_", "bc_ai_")):
            assert os.path.exists(os.path.join(ROOT, c["lesson"])), f'missing link target {c["lesson"]}'
    blob = json.dumps(d)
    for bad in ("Malcolm", "your teacher", "Your teacher", "The teacher will", "I Do", "We Do", "You Do", "TEEP", "Pause:"):
        assert bad not in blob, f'{d["slug"]}: forbidden word {bad!r}'


def main():
    lessons = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for d in lessons:
        check(d)
        out = os.path.join(ROOT, f'end_{d["slug"]}_c1.html')
        open(out, "w").write(lesson(d, lessons))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")
    open(os.path.join(ROOT, DASH), "w").write(dashboard(lessons))
    print(f"  wrote {DASH}")


if __name__ == "__main__":
    main()
