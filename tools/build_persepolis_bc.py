#!/usr/bin/env python3
"""Build the 'Persepolis: Book Club' series (B2/C1, four meetings) from content files.

  tools/persepolis_bc_content/NN_<slug>.json  ->  persepolis_bc_<slug>.html   (one meeting each)
  (all lessons)                            ->  persepolis_bookclub_dashboard.html

Reuses the Think Inside the Box engine (build_tib.py): same five tabs
(Key Words, The Story, The Tool, Grammar, Speak), same diagrams, recoloured navy.
Usage: python3 tools/build_end.py     (always rebuilds everything)
"""
import json, os, re, glob, itertools, html

import build_tib as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "persepolis_bc_content")
SERIES = "Persepolis Book Club"
DASH = "persepolis_bookclub_dashboard.html"
E = html.escape

INK_PAL = {"#0e7490": "#b3202a", "#0f766e": "#141414", "#115e59": "#141414", "#134e4a": "#000000",
        "#7cc4bb": "#8a8478", "#99d5cc": "#a8a296", "#c5e6e1": "#d3cec2", "#e2f4f1": "#ece8de",
        "#cdeae5": "#ddd8cc", "#f1f9f8": "#f6f3ea", "#eaf6f4": "#f1ede2", "#e3f2ef": "#ece7dc",
        "#cfe7e3": "#dbd6ca", "#f5fbfa": "#f8f5ee", "#1f3d3a": "#141414", "#eef7f6": "#f3efe6",
        "#f7fbfa": "#faf7f0", "rgba(14,116,144,": "rgba(179,32,42,"}
NAVY = INK_PAL


def navy(s):
    for a, b in NAVY.items():
        s = s.replace(a, b)
    return s


# diagrams are drawn by build_tib with its module-level colours
T.INK, T.TEAL, T.LIGHT = "#141414", "#141414", "#ece8de"
T.TONES.update({"g": "#dfe6d4", "y": "#f0e3b8", "r": "#f0cbc9", "t": "#ddd8cc", "b": "#d9dce3", "n": "#ece8de"})
PANEL_CSS = """
body { background:#faf7f0; }
header { border:3px solid #141414; border-radius:6px !important; box-shadow:8px 8px 0 #141414; background:linear-gradient(135deg,#b3202a 0%,#141414 82%) !important; }
header::after { content:""; position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,.10) 1.2px, transparent 1.4px); background-size:9px 9px; pointer-events:none; }
header { position:relative; overflow:hidden; }
header h1 { text-transform:uppercase; letter-spacing:1px; }
.card { border:3px solid #141414 !important; border-radius:6px !important; box-shadow:7px 7px 0 #141414 !important; background:#fff; }
.tab-btn { border:2px solid #141414 !important; border-radius:4px !important; background:#fff !important; color:#141414 !important; }
.tab-btn.active { background:#b3202a !important; color:#fff !important; }
.intention { border-left:5px solid #b3202a !important; background:#f6f3ea !important; }
.story-chunk { border-left:5px solid #141414 !important; background:#f6f3ea !important; border-radius:0 6px 6px 0 !important; }
h2, h3 { color:#141414 !important; }
.check, .gap-fill, .discuss, .note, .speak-prompt { border-radius:6px !important; }
.check-btn, .reveal-btn, .timer-btn { border-radius:4px !important; background:#141414 !important; color:#ffffff !important; border:2px solid #141414 !important; font-weight:700 !important; }
.check-btn:hover, .reveal-btn:hover, .timer-btn:hover { background:#b3202a !important; }
.series-strip a { color:#b3202a !important; }
.cousin a { color:#b3202a !important; }
"""
CSS = navy(T.CSS) + PANEL_CSS
JS = T.JS


def lesson(d, lessons):
    i = [x["slug"] for x in lessons].index(d["slug"])
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    strip = [f'<a href="{DASH}">The whole series</a>']
    if prev:
        strip.insert(0, f'<a href="persepolis_bc_{prev["slug"]}.html">&larr; {prev["title"]}</a>')
    if nxt:
        strip.append(f'<a href="persepolis_bc_{nxt["slug"]}.html">{nxt["title"]} &rarr;</a>')
    body = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{d["title"]} · Persepolis Book Club · B2/C1 English</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">PERSEPOLIS · BOOK CLUB · MEETING {d["num"]} OF 4 · B2/C1 · 50 min</span>
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
        Persepolis · Book Club · {d["title"]} · B2/C1
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''
    return body


def map_svg(lessons):
    pos = {1: (210, 150), 2: (890, 150), 3: (210, 395), 4: (890, 395)}
    chips = {1: ["stark · poignant · candid", "notice · react · ask"], 2: ["revolution · regime · war", "what · why · so what"],
             3: ["homesick · outsider", "wishes and regrets"], 4: ["memoir · testimony", "facts · feelings · voice"]}
    out = ['<svg viewBox="0 0 1100 640" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Map of the Persepolis book club: four meetings around the book, with a timeline of 1979 to 1994">']
    for i, d in enumerate(lessons, 1):
        x, y = pos[i]
        out.append(f'<line x1="550" y1="290" x2="{x}" y2="{y}" stroke="#141414" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>')
    out.append('<circle cx="550" cy="290" r="96" fill="#141414"/><circle cx="550" cy="290" r="86" fill="none" stroke="#faf7f0" stroke-width="2"/>')
    out.append('<text x="550" y="282" text-anchor="middle" font-size="25" font-weight="800" fill="#faf7f0" letter-spacing="1">PERSEPOLIS</text>')
    out.append('<text x="550" y="310" text-anchor="middle" font-size="14" fill="#d9d3c4">book club</text>')
    for i, d in enumerate(lessons, 1):
        x, y = pos[i]
        words = d["title"].split()
        half = (len(words) + 1) // 2
        l1, l2 = " ".join(words[:half]), " ".join(words[half:])
        out.append(f'<a href="persepolis_bc_{d["slug"]}.html"><title>Meeting {i}: {d["title"]}</title>'
                   f'<rect x="{x-135}" y="{y-62}" width="270" height="124" rx="6" fill="#faf7f0" stroke="#141414" stroke-width="4"/>'
                   f'<rect x="{x-131}" y="{y-58}" width="262" height="116" rx="4" fill="none" stroke="#b3202a" stroke-width="1.5"/>'
                   f'<circle cx="{x-98}" cy="{y-26}" r="19" fill="#b3202a"/><text x="{x-98}" y="{y-19}" text-anchor="middle" font-size="22" font-weight="800" fill="#fff">{i}</text>'
                   f'<text x="{x-70}" y="{y-24}" font-size="19" font-weight="800" fill="#141414">{l1}</text>'
                   f'<text x="{x-70}" y="{y-2}" font-size="19" font-weight="800" fill="#141414">{l2}</text>'
                   f'<text x="{x-118}" y="{y+26}" font-size="13" fill="#555">{chips[i][0]}</text>'
                   f'<text x="{x-118}" y="{y+44}" font-size="13" fill="#555">{chips[i][1]}</text></a>')
    # timeline
    out.append('<text x="550" y="520" text-anchor="middle" font-size="13" font-weight="700" fill="#b3202a" letter-spacing="2">THE YEARS THE BOOK COVERS</text>')
    out.append('<line x1="110" y1="570" x2="990" y2="570" stroke="#141414" stroke-width="4"/>')
    events = [(110, "1979", "the Shah leaves;|revolution"), (330, "1980", "war with Iraq begins;|the veil in schools"),
              (550, "1984", "sent to|Vienna, aged 14"), (770, "1989", "returns|to Tehran"), (990, "1994", "leaves Iran|again")]
    for x, yr, lab in events:
        out.append(f'<circle cx="{x}" cy="570" r="9" fill="#b3202a" stroke="#141414" stroke-width="3"/>')
        out.append(f'<text x="{x}" y="552" text-anchor="middle" font-size="16" font-weight="800" fill="#141414">{yr}</text>')
        for k, line in enumerate(lab.split("|")):
            out.append(f'<text x="{x}" y="{596 + k*16}" text-anchor="middle" font-size="12.5" fill="#444">{line}</text>')
    out.append('</svg>')
    return "".join(out)


def dashboard(lessons):
    cards = []
    for d in lessons:
        c = d["card"]
        cards.append(f'''        <a class="pcard" href="persepolis_bc_{d["slug"]}.html">
            <div class="pnum">MEETING {d["num"]} &middot; {c["shape"]}</div>
            <div class="ptitle">{d["title"]}</div>
            <div class="pwho">{c["who"]}</div>
            <div class="pess">{c["essence"]}</div>
            <div class="ptool"><span>The tool:</span> {d["tool"]}</div>
            <div class="pfoot"><span class="ptag">{d["grammar"]["name"]}</span><span class="go">Open &rarr;</span></div>
        </a>''')
    hot = [(1, 1.7, 1.7, 34.1, 38.9), (2, 63.0, 1.5, 35.3, 39.6), (3, 1.7, 44.1, 34.1, 37.2), (4, 65.4, 43.9, 32.9, 37.5)]
    hots = "".join(f'<a class="hot" href="persepolis_bc_{lessons[i-1]["slug"]}.html" title="{lessons[i-1]["title"]}" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%"><span>{lessons[i-1]["title"]}</span></a>' for i, l, t, w, h in hot)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>Persepolis Book Club · B2/C1</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif; background:#faf7f0; color:#1a1a1a; line-height:1.6; }}
.container {{ max-width:1040px; margin:0 auto; padding:20px 16px 60px; }}
header {{ position:relative; overflow:hidden; text-align:center; color:#fff; padding:54px 26px 48px; margin-bottom:26px; border:3px solid #141414; border-radius:6px; box-shadow:8px 8px 0 #141414; background:linear-gradient(135deg,#b3202a 0%,#141414 82%); }}
header::after {{ content:""; position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,.10) 1.2px,transparent 1.4px); background-size:9px 9px; pointer-events:none; }}
header * {{ position:relative; z-index:1; }}
.tag {{ display:inline-block; padding:5px 15px; background:rgba(255,255,255,.18); border-radius:4px; font-size:.78rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }}
h1 {{ font-size:3rem; line-height:1.05; margin-bottom:12px; text-transform:uppercase; letter-spacing:2px; }}
.subtitle {{ font-size:1.12rem; max-width:680px; margin:0 auto; opacity:.96; }}
.intro, .who, .how {{ background:#fff; border:3px solid #141414; border-radius:6px; box-shadow:6px 6px 0 #141414; padding:22px 26px; margin-bottom:26px; }}
.intro p {{ margin-bottom:12px; color:#2d2d2d; }} .intro p:last-child {{ margin-bottom:0; }}
.who h2, .how h2 {{ font-size:1.2rem; margin-bottom:8px; }} .who p {{ color:#2d2d2d; }}
.section-label {{ font-size:.82rem; letter-spacing:.16em; text-transform:uppercase; color:#b3202a; font-weight:800; margin:10px 0 12px 2px; }}
.map {{ background:#fff; border:3px solid #141414; border-radius:6px; box-shadow:6px 6px 0 #141414; padding:10px; margin-bottom:8px; }}
.map-frame {{ position:relative; }} .map-frame img {{ display:block; width:100%; height:auto; border-radius:3px; }}
.map-frame svg {{ display:block; width:100%; height:auto; font-family:inherit; }}
.hot {{ position:absolute; display:block; border-radius:8px; }}
.hot span {{ position:absolute; left:50%; bottom:100%; transform:translateX(-50%); white-space:nowrap; background:#141414; color:#fff; font-size:.8rem; font-weight:600; padding:3px 10px; border-radius:6px; opacity:0; pointer-events:none; transition:opacity .15s; }}
.hot:hover {{ box-shadow:0 0 0 3px #b3202a; }} .hot:hover span {{ opacity:1; }}
.map a {{ cursor:pointer; }}
.map-note {{ text-align:center; font-size:.92rem; color:#555; margin-bottom:26px; }}
.flow {{ display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:10px; margin:6px 0 26px; }}
.flow .step {{ background:#fff; border:2px solid #141414; border-radius:4px; padding:10px 18px; text-align:center; min-width:150px; }}
.flow .step b {{ display:block; color:#b3202a; font-size:1.05rem; }} .flow .step span {{ font-size:.85rem; color:#555; }}
.flow .arrow {{ font-size:1.4rem; color:#141414; }}
.pgrid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:22px; margin-bottom:30px; }}
.pcard {{ display:flex; flex-direction:column; text-decoration:none; color:inherit; background:#fff; border:3px solid #141414; border-radius:6px; box-shadow:6px 6px 0 #141414; padding:20px 22px; transition:transform .15s, box-shadow .15s; }}
.pcard:hover {{ transform:translate(-2px,-2px); box-shadow:9px 9px 0 #b3202a; }}
.pnum {{ font-size:.74rem; font-weight:800; letter-spacing:.12em; color:#b3202a; margin-bottom:6px; }}
.ptitle {{ font-size:1.5rem; font-weight:800; line-height:1.15; margin-bottom:4px; }}
.pwho {{ font-size:.85rem; color:#666; margin-bottom:10px; }}
.pess {{ color:#2d2d2d; margin-bottom:12px; flex:1; }}
.ptool {{ font-size:.92rem; margin-bottom:12px; }} .ptool span {{ font-weight:700; color:#b3202a; }}
.pfoot {{ display:flex; justify-content:space-between; align-items:center; }}
.ptag {{ background:#141414; color:#fff; font-size:.74rem; font-weight:700; padding:3px 11px; border-radius:4px; }}
.go {{ font-weight:800; color:#b3202a; }}
.how-steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; }}
.how-step .n {{ font-weight:800; color:#b3202a; margin-bottom:2px; }} .how-step p {{ font-size:.92rem; color:#2d2d2d; }}
footer {{ text-align:center; color:#666; font-size:.9rem; margin-top:30px; }}
@media (max-width:720px) {{ h1 {{ font-size:2.1rem; }} .map-frame {{ overflow-x:auto; }} .map-frame svg {{ min-width:720px; }} }}
</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">Book club &middot; a graphic memoir &middot; B2/C1</span>
        <h1>Persepolis<br><span style="font-size:.5em;letter-spacing:6px;">Book Club</span></h1>
        <p class="subtitle">Four meetings around one remarkable book: a girl, a revolution and a life drawn in black ink. Read it alone, in pairs or round a table.</p>
    </header>

    <div class="intro">
        <p>Marjane Satrapi's <em>Persepolis</em> is a true story told as a comic: a girl in Tehran, a revolution, a war, and years of living between two worlds. It is short, funny, sad and easy to start talking about, which makes it ideal for a book club.</p>
        <p>Each of the four meetings takes one part of the book and gives you a story to read, a simple tool for talking about it, the language you need, and plenty of speaking. You can use them one-to-one, in pairs or with a group: take turns, respond to each other and bring your own opinions. You do not need to have finished the book, though reading along will make every meeting richer.</p>
    </div>

    <p class="section-label">The map &mdash; click a meeting</p>
    <div class="map">
        <div class="map-frame" id="mapframe">
            <img src="persepolis_bookclub_map.jpg" alt="A mind map of the Persepolis book club: four meetings around the book and a timeline from 1979 to 1994" onerror="document.getElementById('mapframe').innerHTML=document.getElementById('mapsvg').innerHTML">
            {hots}
        </div>
        <template id="mapsvg">{map_svg(lessons)}</template>
    </div>
    <p class="map-note">Four meetings, one book, and the years it covers. Prefer an exam-style, analytical approach? See <a href="persepolis_dashboard.html" style="color:#b3202a;font-weight:700;">Persepolis: Close Reading</a>.</p>

    <div class="who">
        <h2>Who it is for</h2>
        <p>Adults who read for pleasure and want to talk about what they read: members of book clubs, one-to-one readers and anyone who wants a real conversation in English about a real book. The language level is B2 to C1. You need no knowledge of Iran, comics or literary terms &mdash; each meeting explains what you need.</p>
    </div>

    <p class="section-label">The series</p>
    <div class="flow">
        <div class="step"><b>First reactions</b><span>notice &middot; react &middot; ask &middot; connect</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>The history</b><span>what happened, why, so what</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Home and away</b><span>roots, outsiders, strangers</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Whose story?</b><span>facts, feelings, voice</span></div>
    </div>

    <p class="section-label">The four meetings</p>
    <div class="pgrid">
{chr(10).join(cards)}
    </div>

    <div class="how">
        <h2>How each meeting works</h2>
        <div class="how-steps">
            <div class="how-step"><div class="n">1 &middot; Key Words</div><p>Ten words, worked out before you read.</p></div>
            <div class="how-step"><div class="n">2 &middot; The Story</div><p>The part of the book and its background, in three parts, with a talking point after each.</p></div>
            <div class="how-step"><div class="n">3 &middot; The Tool</div><p>A simple way to talk about the book, a chance to try it, and where it breaks.</p></div>
            <div class="how-step"><div class="n">4 &middot; Language</div><p>The grammar and phrases you need to write and talk about it.</p></div>
            <div class="how-step"><div class="n">5 &middot; Speak</div><p>Timed speaking tasks, then harder questions.</p></div>
        </div>
    </div>

    <footer>Persepolis &middot; Book Club &middot; B2/C1</footer>
</div>
</body>
</html>
'''


def check(d):
    n_items = sum(len(s["items"]) for s in d["vocab"])
    assert n_items == 10, f'{d["slug"]}: {n_items} vocab items, want 10'
    sort = d["tool_tab"]["sort"]
    ans = [it["answer"] for it in sort["items"]]
    assert all(a in sort["options"] for a in ans), f'{d["slug"]}: sort answer not in options'
    assert max(len(list(g)) for _, g in itertools.groupby(ans)) < 3, f'{d["slug"]}: same sort answer 3 in a row'
    for c in d["tool_tab"]["cousins"]:
        if c.get("lesson") and not (c["lesson"].startswith("persepolis_") or c["lesson"] == DASH):
            assert os.path.exists(os.path.join(ROOT, c["lesson"])), f'missing link target {c["lesson"]}'
    blob = json.dumps(d)
    for bad in ("Malcolm", "Jane", " IB ", "Paper 1", "Paper 2", "your teacher", "Your teacher", "The teacher will", "I Do", "We Do", "You Do", "TEEP", "Pause:"):
        assert bad not in blob, f'{d["slug"]}: forbidden word {bad!r}'


def main():
    lessons = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for d in lessons:
        check(d)
        out = os.path.join(ROOT, f'persepolis_bc_{d["slug"]}.html')
        open(out, "w").write(lesson(d, lessons))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")
    open(os.path.join(ROOT, DASH), "w").write(dashboard(lessons))
    print(f"  wrote {DASH}")


if __name__ == "__main__":
    main()
