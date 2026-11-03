#!/usr/bin/env python3
"""Build the 'Persepolis: Book Club' series (B2/C1, four meetings) from content files.

  tools/piranesi_bc_content/NN_<slug>.json  ->  piranesi_bc_<slug>.html   (one meeting each)
  (all lessons)                            ->  piranesi_bookclub_dashboard.html

Reuses the Think Inside the Box engine (build_tib.py): same five tabs
(Key Words, The Story, The Tool, Grammar, Speak), same diagrams, recoloured navy.
Usage: python3 tools/build_end.py     (always rebuilds everything)
"""
import json, os, re, glob, itertools, html

import build_tib as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "piranesi_bc_content")
SERIES = "Piranesi Book Club"
SCENES = {"house": (1, "An etching of a long hall of marble statues in niches, with tide water on the floor and clouds in the galleries above"),
          "journals": (2, "An etching of a stone alcove with a table, a stack of numbered notebooks, a candle and an open journal, with a flooded hall beyond the window"),
          "other": (3, "An etching of a flooded corridor at dusk, with one distant figure in a dark coat standing at the far end"),
          "meaning": (4, "An etching of a great staircase rising into clouds and a starry doorway and descending into dark water")}
DASH = "piranesi_bookclub_dashboard.html"
E = html.escape

INK_PAL = {"#0e7490": "#8a6a2c", "#0f766e": "#16263d", "#115e59": "#16263d", "#134e4a": "#0b1626",
        "#7cc4bb": "#8a8478", "#99d5cc": "#a8a296", "#c5e6e1": "#d3cec2", "#e2f4f1": "#ece8de",
        "#cdeae5": "#ddd8cc", "#f1f9f8": "#f6f3ea", "#eaf6f4": "#f1ede2", "#e3f2ef": "#ece7dc",
        "#cfe7e3": "#dbd6ca", "#f5fbfa": "#f8f5ee", "#1f3d3a": "#16263d", "#eef7f6": "#f3efe6",
        "#f7fbfa": "#faf7f0", "rgba(14,116,144,": "rgba(138,106,44,"}
NAVY = INK_PAL


def navy(s):
    for a, b in NAVY.items():
        s = s.replace(a, b)
    return s


# diagrams are drawn by build_tib with its module-level colours
T.INK, T.TEAL, T.LIGHT = "#16263d", "#16263d", "#ece8de"
T.TONES.update({"g": "#dfe6d4", "y": "#f0e3b8", "r": "#f0cbc9", "t": "#ddd8cc", "b": "#d9dce3", "n": "#ece8de"})
PANEL_CSS = """
body { background:#faf7f0; }
header { border:1px solid #cfc6b0; border-radius:6px !important; box-shadow:0 6px 22px rgba(22,38,61,.14); background:linear-gradient(135deg,#2f5f86 0%,#16263d 82%) !important; }
header::after { content:""; position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,.10) 1.2px, transparent 1.4px); background-size:9px 9px; pointer-events:none; }
header { position:relative; overflow:hidden; }
header h1 { text-transform:uppercase; letter-spacing:1px; }
.card { border:1px solid #cfc6b0 !important; border-radius:6px !important; box-shadow:0 6px 22px rgba(22,38,61,.14) !important; background:#fff; }
.tab-btn { border:2px solid #16263d !important; border-radius:4px !important; background:#fff !important; color:#16263d !important; }
.tab-btn.active { background:#8a6a2c !important; color:#fff !important; }
.intention { border-left:5px solid #8a6a2c !important; background:#f6f3ea !important; }
.story-chunk { border-left:5px solid #16263d !important; background:#f6f3ea !important; border-radius:0 6px 6px 0 !important; }
h2, h3 { color:#16263d !important; }
.check, .gap-fill, .discuss, .note, .speak-prompt { border-radius:6px !important; }
.check-btn, .reveal-btn, .timer-btn { border-radius:4px !important; background:#16263d !important; color:#ffffff !important; border:2px solid #16263d !important; font-weight:700 !important; }
.check-btn:hover, .reveal-btn:hover, .timer-btn:hover { background:#8a6a2c !important; }
.series-strip a { color:#8a6a2c !important; }
.cousin a { color:#8a6a2c !important; }
.scene { margin:0 0 18px; } .scene img { display:block; width:100%; height:auto; max-height:420px; object-fit:cover; border-radius:10px; box-shadow:0 6px 22px rgba(22,38,61,.18); }
"""
CSS = navy(T.CSS) + PANEL_CSS
JS = T.JS


def lesson(d, lessons):
    i = [x["slug"] for x in lessons].index(d["slug"])
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    strip = [f'<a href="{DASH}">The whole series</a>']
    if prev:
        strip.insert(0, f'<a href="piranesi_bc_{prev["slug"]}.html">&larr; {prev["title"]}</a>')
    if nxt:
        strip.append(f'<a href="piranesi_bc_{nxt["slug"]}.html">{nxt["title"]} &rarr;</a>')
    body = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{d["title"]} · Piranesi Book Club · C1 English</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">PIRANESI · BOOK CLUB · MEETING {d["num"]} OF 4 · C1 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <figure class="scene"><img src="piranesi_scene_{SCENES[d["slug"]][0]}.jpg" alt="{SCENES[d["slug"]][1]}"></figure>

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
        Piranesi · Book Club · {d["title"]} · C1
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''
    return body


def map_svg(lessons):
    pos = {1: (200, 140), 2: (900, 140), 3: (200, 400), 4: (900, 400)}
    out = ['<svg viewBox="0 0 1100 540" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Map of the Piranesi book club: four halls around the House">']
    for i, d in enumerate(lessons, 1):
        x, y = pos[i]
        out.append(f'<line x1="550" y1="270" x2="{x}" y2="{y}" stroke="#8a6a2c" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/>')
    out.append('<ellipse cx="550" cy="270" rx="150" ry="72" fill="#16263d"/><ellipse cx="550" cy="270" rx="140" ry="63" fill="none" stroke="#c9b27c" stroke-width="2"/>')
    out.append('<text x="550" y="268" text-anchor="middle" font-size="30" font-weight="700" fill="#faf7f0" letter-spacing="3">PIRANESI</text>')
    out.append('<text x="550" y="296" text-anchor="middle" font-size="14" fill="#d9cfb4">book club</text>')
    for i, d in enumerate(lessons, 1):
        x, y = pos[i]
        words = d["title"].split(); half = (len(words) + 1) // 2
        l1, l2 = " ".join(words[:half]), " ".join(words[half:])
        out.append(f'<a href="piranesi_bc_{d["slug"]}.html"><title>Meeting {i}: {d["title"]}</title>'
                   f'<rect x="{x-140}" y="{y-60}" width="280" height="120" rx="14" fill="#faf7f0" stroke="#16263d" stroke-width="2"/>'
                   f'<circle cx="{x-104}" cy="{y-24}" r="19" fill="#8a6a2c"/><text x="{x-104}" y="{y-17}" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">{i}</text>'
                   f'<text x="{x-76}" y="{y-22}" font-size="19" font-weight="700" fill="#16263d">{l1}</text>'
                   f'<text x="{x-76}" y="{y}" font-size="19" font-weight="700" fill="#16263d">{l2}</text>'
                   f'<text x="{x-124}" y="{y+34}" font-size="13" fill="#555">{d["tool"]}</text></a>')
    out.append('</svg>')
    return "".join(out)


def dashboard(lessons):
    cards = []
    for d in lessons:
        c = d["card"]
        cards.append(f'''        <a class="pcard" href="piranesi_bc_{d["slug"]}.html">
            <img class="pthumb" src="piranesi_scene_{SCENES[d["slug"]][0]}.jpg" alt="" loading="lazy">
            <div class="pnum">MEETING {d["num"]} &middot; {c["shape"]}</div>
            <div class="ptitle">{d["title"]}</div>
            <div class="pwho">{c["who"]}</div>
            <div class="pess">{c["essence"]}</div>
            <div class="ptool"><span>The tool:</span> {d["tool"]}</div>
            <div class="pfoot"><span class="ptag">{d["grammar"]["name"]}</span><span class="go">Open &rarr;</span></div>
        </a>''')
    hot = [(1, 2.0, 1.0, 35.5, 28.3), (2, 61.8, 1.0, 36.8, 28.3), (3, 1.3, 52.7, 35.2, 25.4), (4, 65.1, 52.7, 33.9, 25.4)]
    hots = "".join(f'<a class="hot" href="piranesi_bc_{lessons[i-1]["slug"]}.html" title="{lessons[i-1]["title"]}" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%"><span>{lessons[i-1]["title"]}</span></a>' for i, l, t, w, h in hot)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>Piranesi Book Club · C1</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif; background:#faf7f0; color:#1a1a1a; line-height:1.6; }}
.container {{ max-width:1040px; margin:0 auto; padding:20px 16px 60px; }}
header {{ position:relative; overflow:hidden; text-align:center; color:#fff; padding:54px 26px 48px; margin-bottom:26px; border:1px solid #cfc6b0; border-radius:6px; box-shadow:0 6px 22px rgba(22,38,61,.14); background:linear-gradient(135deg,#2f5f86 0%,#16263d 82%); }}
header::after {{ content:""; position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,.10) 1.2px,transparent 1.4px); background-size:9px 9px; pointer-events:none; }}
header * {{ position:relative; z-index:1; }}
.tag {{ display:inline-block; padding:5px 15px; background:rgba(255,255,255,.18); border-radius:4px; font-size:.78rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }}
h1 {{ font-size:3rem; line-height:1.05; margin-bottom:12px; text-transform:uppercase; letter-spacing:2px; }}
.subtitle {{ font-size:1.12rem; max-width:680px; margin:0 auto; opacity:.96; }}
.intro, .who, .how {{ background:#fff; border:1px solid #cfc6b0; border-radius:6px; box-shadow:0 6px 22px rgba(22,38,61,.14); padding:22px 26px; margin-bottom:26px; }}
.intro p {{ margin-bottom:12px; color:#2d2d2d; }} .intro p:last-child {{ margin-bottom:0; }}
.who h2, .how h2 {{ font-size:1.2rem; margin-bottom:8px; }} .who p {{ color:#2d2d2d; }}
.section-label {{ font-size:.82rem; letter-spacing:.16em; text-transform:uppercase; color:#8a6a2c; font-weight:800; margin:10px 0 12px 2px; }}
.map {{ background:#fff; border:1px solid #cfc6b0; border-radius:6px; box-shadow:0 6px 22px rgba(22,38,61,.14); padding:10px; margin-bottom:8px; }}
.map-frame {{ position:relative; }} .map-frame img {{ display:block; width:100%; height:auto; border-radius:3px; }}
.map-frame svg {{ display:block; width:100%; height:auto; font-family:inherit; }}
.hot {{ position:absolute; display:block; border-radius:8px; }}
.hot span {{ position:absolute; left:50%; bottom:100%; transform:translateX(-50%); white-space:nowrap; background:#16263d; color:#fff; font-size:.8rem; font-weight:600; padding:3px 10px; border-radius:6px; opacity:0; pointer-events:none; transition:opacity .15s; }}
.hot:hover {{ box-shadow:0 0 0 3px #8a6a2c; }} .hot:hover span {{ opacity:1; }}
.map a {{ cursor:pointer; }}
.map-note {{ text-align:center; font-size:.92rem; color:#555; margin-bottom:26px; }}
.flow {{ display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:10px; margin:6px 0 26px; }}
.flow .step {{ background:#fff; border:2px solid #16263d; border-radius:4px; padding:10px 18px; text-align:center; min-width:150px; }}
.flow .step b {{ display:block; color:#8a6a2c; font-size:1.05rem; }} .flow .step span {{ font-size:.85rem; color:#555; }}
.flow .arrow {{ font-size:1.4rem; color:#16263d; }}
.pgrid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:22px; margin-bottom:30px; }}
.pcard {{ display:flex; flex-direction:column; text-decoration:none; color:inherit; background:#fff; border:1px solid #cfc6b0; border-radius:6px; box-shadow:0 6px 22px rgba(22,38,61,.14); padding:20px 22px; transition:transform .15s, box-shadow .15s; }}
.pcard:hover {{ transform:translate(-2px,-2px); box-shadow:0 10px 26px rgba(22,38,61,.22); }}
.pthumb {{ display:block; width:calc(100% + 44px); margin:-20px -22px 14px; height:150px; object-fit:cover; border-radius:9px 9px 0 0; }}
.pnum {{ font-size:.74rem; font-weight:800; letter-spacing:.12em; color:#8a6a2c; margin-bottom:6px; }}
.ptitle {{ font-size:1.5rem; font-weight:800; line-height:1.15; margin-bottom:4px; }}
.pwho {{ font-size:.85rem; color:#666; margin-bottom:10px; }}
.pess {{ color:#2d2d2d; margin-bottom:12px; flex:1; }}
.ptool {{ font-size:.92rem; margin-bottom:12px; }} .ptool span {{ font-weight:700; color:#8a6a2c; }}
.pfoot {{ display:flex; flex-wrap:wrap; gap:8px; justify-content:space-between; align-items:center; }}
.ptag {{ background:#16263d; color:#fff; font-size:.74rem; font-weight:700; padding:3px 11px; border-radius:4px; }}
.go {{ font-weight:800; color:#8a6a2c; }}
.how-steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; }}
.how-step .n {{ font-weight:800; color:#8a6a2c; margin-bottom:2px; }} .how-step p {{ font-size:.92rem; color:#2d2d2d; }}
footer {{ text-align:center; color:#666; font-size:.9rem; margin-top:30px; }}
@media (max-width:720px) {{ h1 {{ font-size:2.1rem; }} .map-frame {{ overflow-x:auto; }} .map-frame svg {{ min-width:720px; }} }}
</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">Book club &middot; a novel &middot; C1</span>
        <h1>Piranesi<br><span style="font-size:.5em;letter-spacing:6px;">Book Club</span></h1>
        <p class="subtitle">Four meetings around a strange, short and beautiful novel: a man, an endless house and a sea that comes and goes. Read it alone, in pairs or round a table.</p>
    </header>

    <div class="intro">
        <p>Susanna Clarke's <em>Piranesi</em> (2020) is a short, strange novel about a man who lives alone in a House of endless halls, with statues in every one and the tide moving through the lower floors. It is calm, mysterious and beautifully written, and readers argue about what it means, which makes it ideal for a book club.</p>
        <p>Each of the four meetings takes one part of the book and gives you a summary to read, a simple tool for talking about it, the language you need, and plenty of speaking. Use them one-to-one, in pairs or with a group. <strong>The meetings discuss the whole book, including the ending, so finish reading before the last one.</strong> The summaries are written in our own words, and the book itself is not quoted at length.</p>
    </div>

    <p class="section-label">The map &mdash; click a meeting</p>
    <div class="map">
        <div class="map-frame" id="mapframe">
            <img src="piranesi_bookclub_map.jpg" alt="A map of the House: four halls, one for each meeting of the Piranesi book club" onerror="document.getElementById('mapframe').innerHTML=document.getElementById('mapsvg').innerHTML">
            {hots}
        </div>
        <template id="mapsvg">{map_svg(lessons)}</template>
    </div>
    <p class="map-note">Four meetings, one book. Prefer another book? See <a href="persepolis_bookclub_dashboard.html" style="color:#8a6a2c;font-weight:700;">Persepolis Book Club</a>.</p>

    <div class="who">
        <h2>Who it is for</h2>
        <p>Adults who read for pleasure and want to talk about what they read: members of book clubs, one-to-one readers and anyone who wants a real conversation in English about a real book. The language level is C1, and the book itself is easy to read but subtle. You need no knowledge of fantasy or literary terms; each meeting explains what you need.</p>
    </div>

    <p class="section-label">The series</p>
    <div class="flow">
        <div class="step"><b>The House</b><span>look &middot; name &middot; compare &middot; wonder</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>The Journals</b><span>written, remembered, doubted</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>The Other</b><span>listen &middot; watch &middot; test</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>What does it mean?</b><span>text &middot; clue &middot; reading</span></div>
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

    <footer>Piranesi &middot; Book Club &middot; C1</footer>
</div>
</body>
</html>
'''


def check(d):
    n_items = sum(len(s["items"]) for s in d["vocab"])
    assert n_items == 10, f'{d["slug"]}: {n_items} vocab items, want 10'
    vb, vc = d["vocab"][1], d["vocab"][2]
    assert vb["heading"].startswith("B · Which term means") and vb["intro"].count("·") >= 2, f'{d["slug"]}: vocab B must list its terms'
    assert vc["heading"].startswith("C · Which word completes all three phrases") and all(it["sent"].count("___") == 3 for it in vc["items"]), f'{d["slug"]}: vocab C must be the collocation gap-fill'
    sort = d["tool_tab"]["sort"]
    ans = [it["answer"] for it in sort["items"]]
    assert all(a in sort["options"] for a in ans), f'{d["slug"]}: sort answer not in options'
    assert max(len(list(g)) for _, g in itertools.groupby(ans)) < 3, f'{d["slug"]}: same sort answer 3 in a row'
    for c in d["tool_tab"]["cousins"]:
        if c.get("lesson") and not (c["lesson"].startswith("piranesi_") or c["lesson"] == DASH):
            assert os.path.exists(os.path.join(ROOT, c["lesson"])), f'missing link target {c["lesson"]}'
    blob = json.dumps(d)
    for bad in ("Malcolm", "Jane", " IB ", "Paper 1", "Paper 2", "your teacher", "Your teacher", "The teacher will", "I Do", "We Do", "You Do", "TEEP", "Pause:"):
        assert bad not in blob, f'{d["slug"]}: forbidden word {bad!r}'


def main():
    lessons = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for d in lessons:
        check(d)
        out = os.path.join(ROOT, f'piranesi_bc_{d["slug"]}.html')
        open(out, "w").write(lesson(d, lessons))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")
    open(os.path.join(ROOT, DASH), "w").write(dashboard(lessons))
    print(f"  wrote {DASH}")


if __name__ == "__main__":
    main()
