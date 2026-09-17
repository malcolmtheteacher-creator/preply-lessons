#!/usr/bin/env python3
"""Build the 'Think Inside the Box' series (B2) from content files.

  tools/tib_content/NN_<slug>.json  ->  tib_<slug>_b2.html   (one lesson each)
  tools/tib_toolbox.json            ->  think_inside_the_box_toolbox.html
  (all lessons + toolbox)           ->  think_inside_the_box_dashboard.html

Page style is copied live from ts_penicillin_b2.html (True Science Stories) and
recoloured teal.  Diagrams are drawn here from a small spec in each content file.
Usage: python3 tools/build_tib.py     (always rebuilds everything)
"""
import json, os, re, glob, html, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "tib_content")
SERIES = "Think Inside the Box"
DASH = "think_inside_the_box_dashboard.html"
TOOLBOX = "think_inside_the_box_toolbox.html"
MAP_IMG = "ThinkInsideTheBox_map.png"
HERO_IMG = "ThinkInsideTheBox.png"

TEMPLATE = open(os.path.join(ROOT, "ts_penicillin_b2.html")).read()
RECOLOUR = {"#667eea": "#0e7490", "#764ba2": "#0f766e", "#5a3aa0": "#115e59", "#4a3380": "#134e4a",
            "#b8a8d8": "#7cc4bb", "#c8bce8": "#99d5cc", "#d8d2ea": "#c5e6e1", "#ede8f9": "#e2f4f1",
            "#ddd1ed": "#cdeae5", "#f6f4fc": "#f1f9f8", "#f0ecf7": "#eaf6f4", "#ede7f6": "#e3f2ef",
            "#e0d8ee": "#cfe7e3", "#f9f7fd": "#f5fbfa", "#3a2a5a": "#1f3d3a", "#f0f0fa": "#eef7f6",
            "#fafafe": "#f7fbfa", "rgba(102,126,234,": "rgba(14,116,144,"}


def recolour(s):
    for a, b in RECOLOUR.items():
        s = s.replace(a, b)
    return s


CSS = recolour(re.search(r"<style>\n(.*?)</style>", TEMPLATE, re.S).group(1)) + """
.diagram { text-align:center; margin: 10px 0 18px; }
.diagram svg { max-width: 100%; height: auto; }
.steps { margin: 6px 0 14px 22px; color:#3a3a4a; }
.steps li { margin-bottom: 8px; }
.sort-row { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:8px 14px; background:#f1f9f8; border:1px solid #c5e6e1; border-radius:10px; padding:10px 14px; margin:8px 0; }
.sort-row .txt { flex: 1 1 320px; color:#2a3a3a; }
.sort-row select { font: inherit; padding:5px 8px; border:1px solid #99d5cc; border-radius:8px; background:white; color:#115e59; min-width: 190px; }
.sort-row .mark { width: 22px; font-weight:700; text-align:center; }
.sort-row.ok { border-color:#6fbf73; background:#eef8ee; }
.sort-row.bad { border-color:#e0a0a0; background:#fbf0f0; }
.check-btn { background: linear-gradient(135deg, #0e7490, #0f766e); color:white; border:none; padding:8px 16px; border-radius:16px; cursor:pointer; font-size:0.88rem; font-weight:600; margin: 10px 8px 0 0; }
.score { font-weight:700; color:#115e59; margin-left:6px; }
.cousins { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:12px; margin: 10px 0; }
.cousin { background:#f5fbfa; border:1px solid #cfe7e3; border-radius:10px; padding:12px 14px; font-size:0.93rem; color:#3a3a4a; }
.cousin b { color:#115e59; display:block; margin-bottom:3px; }
.cousin a { color:#0f766e; font-weight:600; }
.series-strip { text-align:center; font-size:0.86rem; margin: 0 0 16px; color:#5a6a6a; }
.series-strip a { color:#0f766e; font-weight:600; }
"""
JS = re.search(r"<script>\n(.*?)</script>", TEMPLATE, re.S).group(1) + """
function checkSort(id) {
    const box = document.getElementById(id);
    let right = 0, total = 0;
    box.querySelectorAll('.sort-row').forEach(r => {
        const sel = r.querySelector('select');
        total++;
        r.classList.remove('ok', 'bad');
        const mark = r.querySelector('.mark');
        if (!sel.value) { mark.textContent = ''; return; }
        if (sel.value === r.dataset.answer) { right++; r.classList.add('ok'); mark.textContent = '\\u2713'; }
        else { r.classList.add('bad'); mark.textContent = '\\u2717'; }
    });
    box.querySelector('.score').textContent = right + ' / ' + total;
}
"""

GAP = '<input type="text" placeholder="...">'
REVEAL = '<button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle(\'show\')">{}</button>'
E = html.escape

# ---------------------------------------------------------------- diagrams
INK, TEAL, LIGHT = "#1f3d3a", "#0f766e", "#e2f4f1"
TONES = {"g": "#cdebd3", "y": "#f7eac0", "r": "#f3cfcf", "t": "#d4eeea", "b": "#d6e4f5", "n": "#eef2f1"}


def svg_text(x, y, s, size=14, weight="400", fill=INK, anchor="middle", rotate=None):
    lines = s.split("|")
    tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    y0 = y - (len(lines) - 1) * size * 0.6
    spans = "".join(f'<tspan x="{x}" y="{y0 + i * size * 1.2:.1f}">{E(l)}</tspan>' for i, l in enumerate(lines))
    return (f'<text font-family="Segoe UI, sans-serif" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle"{tr}>{spans}</text>')


def d_grid(d):
    cols, rows = d["cols"], d["rows"]
    cw, ch = d.get("cw", 150), d.get("ch", 90)
    L, T = (70 if d.get("arrows", True) else 96), 20
    W, H = L + cols * cw + 20, T + rows * ch + 70
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    tones = d.get("tones", ["t"] * (cols * rows))
    for i, cell in enumerate(d["cells"]):
        r, c = divmod(i, cols)
        x, y = L + c * cw, T + r * ch
        out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{TONES[tones[i]]}" stroke="white" stroke-width="3" rx="6"/>')
        out.append(svg_text(x + cw / 2, y + ch / 2, cell, 13, "600"))
    gx0, gy1 = L, T + rows * ch
    mk = ' marker-end="url(#ar)"' if d.get("arrows", True) else ""
    out.append(f'<line x1="{gx0}" y1="{gy1 + 6}" x2="{L + cols * cw}" y2="{gy1 + 6}" stroke="{TEAL}" stroke-width="2"{mk}/>')
    out.append(f'<line x1="{gx0 - 6}" y1="{gy1}" x2="{gx0 - 6}" y2="{T}" stroke="{TEAL}" stroke-width="2"{mk}/>')
    out.insert(1, f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{TEAL}"/></marker></defs>')
    out.append(svg_text(L + cols * cw / 2, gy1 + 30, d["x"], 14, "700", TEAL))
    out.append(svg_text(24, T + rows * ch / 2, d["y"], 14, "700", TEAL, rotate=-90))
    if d.get("cl"):
        for c, lab in enumerate(d["cl"]):
            out.append(svg_text(L + c * cw + cw / 2, gy1 + 50, lab, 12, "600", "#556"))
    if d.get("rl"):
        for r, lab in enumerate(d["rl"]):
            out.append(svg_text(L - 22, T + r * ch + ch / 2, lab, 12, "600", "#556", rotate=-90))
    if d.get("xl"):
        out.append(svg_text(L + 4, gy1 + 50, d["xl"][0], 11, "400", "#667", "start"))
        out.append(svg_text(L + cols * cw - 4, gy1 + 50, d["xl"][1], 11, "400", "#667", "end"))
    if d.get("yl"):
        out.append(svg_text(46, gy1 - 4, d["yl"][0], 11, "400", "#667", "start", rotate=-90))
        out.append(svg_text(46, T + 4, d["yl"][1], 11, "400", "#667", "end", rotate=-90))
    out.append("</svg>")
    return "".join(out)


def d_pyramid(d):
    levels = d["levels"]  # top first
    n, W, H, T = len(levels), 560, 60 * len(levels) + 30, 10
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    tones = ["b", "t", "g", "y", "r", "n"]
    for i, lab in enumerate(levels):
        y0, y1 = T + i * 60, T + (i + 1) * 60
        w0, w1 = 40 + i * 90, 40 + (i + 1) * 90
        pts = f"{W/2 - w0/2 + (0 if i else 20)},{y0} {W/2 + w0/2 - (0 if i else 20)},{y0} {W/2 + w1/2},{y1} {W/2 - w1/2},{y1}"
        if i == 0:
            pts = f"{W/2},{y0} {W/2 + w1/2},{y1} {W/2 - w1/2},{y1}"
        out.append(f'<polygon points="{pts}" fill="{TONES[tones[i % 6]]}" stroke="white" stroke-width="3"/>')
        out.append(svg_text(W / 2, (y0 + y1) / 2 + (8 if i == 0 else 0), lab, 13 if i else 11, "600"))
    out.append("</svg>")
    return "".join(out)


def d_cycle(d):
    steps = d["steps"]
    n, W, H, R, cx, cy = len(steps), 520, 400, 130, 260, 200
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">',
           f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{TEAL}"/></marker></defs>']
    for i in range(n):
        a0 = -math.pi / 2 + (i + 0.28) * 2 * math.pi / n
        a1 = -math.pi / 2 + (i + 0.72) * 2 * math.pi / n
        out.append(f'<path d="M{cx + R*math.cos(a0):.1f},{cy + R*math.sin(a0):.1f} A{R},{R} 0 0 1 {cx + R*math.cos(a1):.1f},{cy + R*math.sin(a1):.1f}" '
                   f'fill="none" stroke="{TEAL}" stroke-width="3" marker-end="url(#ar)"/>')
    for i, s in enumerate(steps):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="52" fill="{LIGHT}" stroke="{TEAL}" stroke-width="2"/>')
        out.append(svg_text(x, y, s, 13, "700"))
    if d.get("centre"):
        out.append(svg_text(cx, cy, d["centre"], 13, "600", TEAL))
    out.append("</svg>")
    return "".join(out)


def d_fishbone(d):
    bones, W, H = d["bones"], 640, 330
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    sy = H / 2
    out.append(f'<line x1="30" y1="{sy}" x2="500" y2="{sy}" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<rect x="500" y="{sy - 34}" width="130" height="68" rx="10" fill="#f3cfcf" stroke="#b55" stroke-width="2"/>')
    out.append(svg_text(565, sy, d["head"], 13, "700"))
    half = (len(bones) + 1) // 2
    for i, b in enumerate(bones):
        top = i < half
        k = i if top else i - half
        x = 110 + k * 140
        y = 45 if top else H - 45
        out.append(f'<line x1="{x}" y1="{y + (12 if top else -12)}" x2="{x + 70}" y2="{sy}" stroke="{TEAL}" stroke-width="3"/>')
        out.append(f'<rect x="{x - 55}" y="{y - 16}" width="110" height="30" rx="8" fill="{LIGHT}" stroke="{TEAL}"/>')
        out.append(svg_text(x, y - 1, b, 13, "700"))
    out.append("</svg>")
    return "".join(out)


def d_bell(d):
    segs = d["segments"]  # [label, pct]
    W, H, B = 640, 300, 230
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    f = lambda x: B - 170 * math.exp(-((x - 320) / 105) ** 2 / 2 * 1.0)
    pts = " ".join(f"{x},{f(x):.1f}" for x in range(30, 611, 6))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3"/>')
    edges = d["edges"]  # x positions of segment boundaries
    tones = ["b", "t", "g", "y", "r"]
    for i, (lab, pct) in enumerate(segs):
        x0, x1 = edges[i], edges[i + 1]
        poly = f"{x0},{B} " + " ".join(f"{x},{f(x):.1f}" for x in range(x0, x1 + 1, 4)) + f" {x1},{B}"
        out.append(f'<polygon points="{poly}" fill="{TONES[tones[i]]}" stroke="white" stroke-width="2"/>')
        out.append(svg_text((x0 + x1) / 2, B + 22, lab, 12, "700"))
        out.append(svg_text((x0 + x1) / 2, B + 52, pct, 12, "400", "#556"))
    out.append(f'<line x1="30" y1="{B}" x2="610" y2="{B}" stroke="{INK}" stroke-width="2"/>')
    if d.get("note"):
        out.append(svg_text(320, 22, d["note"], 12, "600", TEAL))
    out.append("</svg>")
    return "".join(out)


def d_bars(d):
    bars = d["bars"]  # [label, value]
    total = sum(v for _, v in bars)
    W, H, B, L = 640, 320, 250, 50
    bw = (W - L - 30) / len(bars)
    top = max(v for _, v in bars)
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    cum, pts = 0, []
    for i, (lab, v) in enumerate(bars):
        x = L + i * bw
        h = 200 * v / top
        out.append(f'<rect x="{x + 6:.1f}" y="{B - h:.1f}" width="{bw - 12:.1f}" height="{h:.1f}" rx="4" fill="{TONES["t"] if i < d.get("vital", 2) else TONES["n"]}" stroke="{TEAL}"/>')
        out.append(svg_text(x + bw / 2, B - h - 10, str(v), 12, "700"))
        out.append(svg_text(x + bw / 2, B + 24, lab, 11, "600"))
        cum += v
        pts.append(f"{x + bw/2:.1f},{B - 200 * cum / total:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#c0504d" stroke-width="2.5"/>')
    y80 = B - 200 * 0.8
    out.append(f'<line x1="{L}" y1="{y80}" x2="{W - 20}" y2="{y80}" stroke="#c0504d" stroke-dasharray="6 5"/>')
    out.append(svg_text(W - 24, y80 - 10, "80% line", 11, "600", "#c0504d", "end"))
    out.append(f'<line x1="{L}" y1="{B}" x2="{W - 20}" y2="{B}" stroke="{INK}" stroke-width="2"/>')
    if d.get("note"):
        out.append(svg_text(W / 2, 16, d["note"], 12, "600", TEAL))
    out.append("</svg>")
    return "".join(out)


DIAGRAMS = {"grid": d_grid, "pyramid": d_pyramid, "cycle": d_cycle, "fishbone": d_fishbone, "bell": d_bell, "bars": d_bars}

# ---------------------------------------------------------------- lesson parts


def ul(items, indent="                    "):
    return "\n".join(f"{indent}<li>{x}</li>" for x in items)


def vocab(d):
    out = []
    for sec in d["vocab"]:
        out.append(f'            <h3>{sec["heading"]}</h3>')
        if sec.get("intro"):
            out.append(f'            <p>{sec["intro"]}</p>')
        for i in sec["items"]:
            out.append(f'''            <div class="guess-item">
                <div class="sent">{i["sent"]}</div>
                {REVEAL.format("Reveal")}
                <div class="meaning">{i["meaning"]}</div>
            </div>''')
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


def tool_tab(t, lessons_by_slug):
    s = t["sort"]
    opts = "".join(f'<option value="{E(o)}">{E(o)}</option>' for o in s["options"])
    rows = "\n".join(f'''                <div class="sort-row" data-answer="{E(it["answer"])}">
                    <span class="txt">{i}. {it["text"]}</span>
                    <select><option value="">choose…</option>{opts}</select>
                    <span class="mark"></span>
                </div>''' for i, it in enumerate(s["items"], 1))
    why = "\n".join(f'                    <p><strong>{i}. {E(it["answer"])}</strong> — {it["why"]}</p>'
                    for i, it in enumerate(s["items"], 1))
    cousins = []
    for c in t["cousins"]:
        link = ""
        if c.get("lesson"):
            link = f' <a href="{c["lesson"]}">Open the lesson &rarr;</a>'
        cousins.append(f'                <div class="cousin"><b>{c["name"]}</b>{c["text"]}{link}</div>')
    breaks = "\n".join(f"                <p>{x}</p>" for x in t["breaks"])
    return f'''            <h2>How the tool works</h2>
            <p>{t["lead"]}</p>
            <div class="diagram">{DIAGRAMS[t["diagram"]["type"]](t["diagram"])}</div>
            <h3>Using it, step by step</h3>
            <ol class="steps">
{ul(t["how"], "                ")}
            </ol>

            <h3>Try it yourself</h3>
            <p>{s["intro"]}</p>
            <div id="sort1">
{rows}
                <button class="check-btn" onclick="checkSort('sort1')">Check my answers</button><span class="score"></span>
                <br>{REVEAL.format("Show the reasons")}
                <div class="answers">
{why}
                </div>
            </div>

            <h3>Where the tool breaks</h3>
            <div class="note">
{breaks}
            </div>
            <div class="discuss">
                <strong>Talk it through:</strong>
                <ul>
{ul(t["discuss"])}
                </ul>
            </div>

            <h3>Its cousins</h3>
            <div class="cousins">
{chr(10).join(cousins)}
            </div>'''


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
    out.append(f'            <p style="margin-top:14px; color:#666; font-style:italic;">{g["closing"]}</p>')
    return "\n".join(out)


def speak(s):
    tasks = "\n\n".join(f'''            <div class="speak-prompt">
                <span class="speak-label">{t["label"]}</span>
{chr(10).join("                <p>" + x + "</p>" for x in t["paras"])}
            </div>''' for t in s["tasks"])
    return f'''            <h2>Speak</h2>
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
            </div>'''


def lesson(d, all_lessons):
    by_slug = {x["slug"]: x for x in all_lessons}
    i = [x["slug"] for x in all_lessons].index(d["slug"])
    prev = all_lessons[i - 1] if i > 0 else None
    nxt = all_lessons[i + 1] if i + 1 < len(all_lessons) else None
    strip = [f'<a href="{DASH}">All the tools</a>']
    if prev:
        strip.insert(0, f'<a href="tib_{prev["slug"]}_b2.html">&larr; {prev["tool"]}</a>')
    if nxt:
        strip.append(f'<a href="tib_{nxt["slug"]}_b2.html">{nxt["tool"]} &rarr;</a>')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{d["title"]} · B2</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">THINK INSIDE THE BOX · TOOL {d["num"]:02d} · B2 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <p class="series-strip">{" &nbsp;·&nbsp; ".join(strip)}</p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Story</button>
        <button class="tab-btn" onclick="showTab(2)">The Tool</button>
        <button class="tab-btn" onclick="showTab(3)">Grammar — {d["grammar"]["name"]}</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>

    <!-- TAB 0: KEY WORDS -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>
            <div class="discuss">
                <strong>Before we start — talk these through:</strong>
                <ul>
{ul(d["warmup"])}
                </ul>
            </div>

            <h2>The vocabulary of this story</h2>
            <p>Ten items. Say your answer <strong>out loud before you reveal it</strong>.</p>

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
            <h2>The story, in three parts</h2>
            <p>Read each part. After it, answer the quick check from memory, then discuss one question.</p>

{story(d)}
        </div>
    </div>

    <!-- TAB 2: THE TOOL -->
    <div class="tab-content">
        <div class="card">
{tool_tab(d["tool_tab"], by_slug)}
        </div>
    </div>

    <!-- TAB 3: GRAMMAR -->
    <div class="tab-content">
        <div class="card">
{grammar(d["grammar"])}
        </div>
    </div>

    <!-- TAB 4: SPEAK -->
    <div class="tab-content">
        <div class="card">
{speak(d["speak"])}
        </div>
    </div>

    <footer>
        {SERIES} · {d["title"]} · B2 · Malcolm Hyndman
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''

# ---------------------------------------------------------------- toolbox page


def toolbox_page(tb, lessons):
    lesson_for = {x["tool"]: f'tib_{x["slug"]}_b2.html' for x in lessons}
    fams = []
    for fam in tb["families"]:
        rows = []
        for t in fam["tools"]:
            link = t.get("link") or lesson_for.get(t["name"], "")
            name = f'<a href="{link}">{t["name"]}</a>' if link else t["name"]
            badge = ' <span class="has">lesson</span>' if link else ""
            fields = " ".join(f'<span class="fld">{f}</span>' for f in t["fields"])
            rows.append(f'''        <div class="tool" data-fields="{E("|".join(t["fields"]))}" data-q="{E((t["name"] + " " + t["what"] + " " + t["who"]).lower())}">
            <div class="tname">{name}{badge}</div>
            <div class="twho">{t["who"]}</div>
            <div class="twhat">{t["what"]}</div>
            <div class="tf">{fields}</div>
        </div>''')
        fams.append(f'''    <section class="fam" id="{fam["id"]}">
        <h2>{fam["name"]} <span class="cnt">{len(fam["tools"])}</span></h2>
        <p class="fdesc">{fam["desc"]}</p>
        <div class="tools">
{chr(10).join(rows)}
        </div>
    </section>''')
    total = sum(len(f["tools"]) for f in tb["families"])
    fields = sorted({f for fam in tb["families"] for t in fam["tools"] for f in t["fields"]})
    chips = "".join(f'<button class="chip" data-f="{E(f)}">{f}</button>' for f in fields)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>The Toolbox · {total} Thinking Tools · B2</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background:#f7fbfa; color:#2a3a3a; line-height:1.55; }}
.container {{ max-width:1080px; margin:0 auto; padding:20px 16px; }}
header {{ background:linear-gradient(135deg,#0e7490,#0f766e); color:white; border-radius:14px; padding:40px 26px; text-align:center; margin-bottom:22px; }}
header .tag {{ display:inline-block; padding:5px 14px; background:rgba(255,255,255,.18); border-radius:14px; font-size:.78rem; font-weight:600; letter-spacing:1.4px; text-transform:uppercase; margin-bottom:12px; }}
header h1 {{ font-size:2.3rem; margin-bottom:8px; }}
header p {{ max-width:700px; margin:0 auto; opacity:.95; }}
.back {{ text-align:center; margin:-8px 0 18px; font-size:.9rem; }} .back a {{ color:#0f766e; font-weight:600; }}
.intro {{ background:white; border:1px solid #cfe7e3; border-left:4px solid #0f766e; border-radius:12px; padding:20px 24px; margin-bottom:20px; }}
.intro p {{ margin-bottom:10px; }} .intro p:last-child {{ margin-bottom:0; }} .intro strong {{ color:#115e59; }}
.bar {{ position:sticky; top:0; z-index:5; background:#f7fbfa; padding:10px 0 12px; }}
.bar input {{ width:100%; font:inherit; padding:10px 14px; border:1px solid #99d5cc; border-radius:10px; margin-bottom:10px; }}
.chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
.chip {{ font:inherit; font-size:.82rem; padding:5px 12px; border-radius:14px; border:1px solid #99d5cc; background:white; color:#115e59; cursor:pointer; }}
.chip.on {{ background:#0f766e; color:white; border-color:#0f766e; }}
.jump {{ display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 20px; font-size:.86rem; }}
.jump a {{ color:#0f766e; font-weight:600; text-decoration:none; background:#e2f4f1; padding:4px 10px; border-radius:10px; }}
.fam {{ margin-bottom:26px; }}
.fam h2 {{ color:#115e59; font-size:1.35rem; }} .cnt {{ font-size:.8rem; background:#e2f4f1; color:#115e59; border-radius:10px; padding:2px 8px; vertical-align:middle; }}
.fdesc {{ color:#556; margin:2px 0 10px; }}
.tools {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:10px; }}
.tool {{ background:white; border:1px solid #cfe7e3; border-radius:10px; padding:12px 14px; }}
.tname {{ font-weight:700; color:#1f3d3a; }} .tname a {{ color:#0f766e; }}
.has {{ font-size:.7rem; background:#0f766e; color:white; border-radius:8px; padding:1px 7px; vertical-align:middle; }}
.twho {{ font-size:.8rem; color:#889; margin:1px 0 5px; }}
.twhat {{ font-size:.92rem; color:#3a4a4a; margin-bottom:6px; }}
.fld {{ display:inline-block; font-size:.72rem; background:#f1f5f4; color:#556; border-radius:8px; padding:1px 7px; margin:2px 2px 0 0; }}
.none {{ display:none; text-align:center; color:#889; padding:20px; }}
footer {{ text-align:center; color:#889; font-size:.86rem; margin:26px 0 12px; }}
</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">Think Inside the Box · The Toolbox</span>
        <h1>{total} Tools for Thinking</h1>
        <p>{tb["subtitle"]}</p>
    </header>
    <p class="back"><a href="{DASH}">&larr; Back to the lessons and the map</a></p>

    <div class="intro">
{chr(10).join("        <p>" + p + "</p>" for p in tb["intro"])}
    </div>

    <div class="bar">
        <input id="q" type="search" placeholder="Search the tools (e.g. time, team, risk, 1950s)…" oninput="filt()">
        <div class="chips">{chips}</div>
    </div>
    <div class="jump">{"".join(f'<a href="#{f["id"]}">{f["name"]}</a>' for f in tb["families"])}</div>

{chr(10).join(fams)}
    <p class="none" id="none">No tool matches — try a different word.</p>

    <footer>{SERIES} · The Toolbox · Malcolm Hyndman</footer>
</div>
<script>
const on = new Set();
document.querySelectorAll('.chip').forEach(c => c.onclick = () => {{
    c.classList.toggle('on');
    on.has(c.dataset.f) ? on.delete(c.dataset.f) : on.add(c.dataset.f);
    filt();
}});
function filt() {{
    const q = document.getElementById('q').value.trim().toLowerCase();
    let shown = 0;
    document.querySelectorAll('.fam').forEach(f => {{
        let n = 0;
        f.querySelectorAll('.tool').forEach(t => {{
            const fl = t.dataset.fields.split('|');
            const ok = (!q || t.dataset.q.includes(q)) && (!on.size || fl.some(x => on.has(x)));
            t.style.display = ok ? '' : 'none';
            if (ok) n++;
        }});
        f.style.display = n ? '' : 'none';
        shown += n;
    }});
    document.getElementById('none').style.display = shown ? 'none' : 'block';
}}
</script>
</body>
</html>
'''

# ---------------------------------------------------------------- dashboard


def mind_map_svg(tb, lessons):
    """Fallback map drawn in code (used until the painted map image exists)."""
    lesson_for = {x["tool"]: f'tib_{x["slug"]}_b2.html' for x in lessons}
    W, H, cx, cy = 1160, 640, 580, 320
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mind map of thinking tools">']
    colours = ["#0e7490", "#b45309", "#7c3aed", "#be123c", "#15803d", "#1d4ed8"]
    fams = tb["families"]
    for i, fam in enumerate(fams):
        a = -math.pi / 3 + i * 2 * math.pi / len(fams)
        fx, fy = cx + 270 * math.cos(a), cy + 215 * math.sin(a)
        right = math.cos(a) > 0
        col = colours[i % len(colours)]
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{fx:.0f}" y2="{fy:.0f}" stroke="{col}" stroke-width="6" stroke-linecap="round" opacity=".55"/>')
        stars = [t for t in fam["tools"] if t["name"] in lesson_for]
        others = [t for t in fam["tools"] if t["name"] not in lesson_for][: max(0, 4 - len(stars))]
        leaves = stars + others
        for j, t in enumerate(leaves):
            ly = fy + (j - (len(leaves) - 1) / 2) * 38
            label = t.get("short", t["name"])
            star = t["name"] in lesson_for
            wbox = 8.2 * len(label) + (40 if star else 24)
            x0 = fx + 78 if right else fx - 78 - wbox
            ex = x0 if right else x0 + wbox
            out.append(f'<path d="M{fx + (50 if right else -50):.0f},{fy:.0f} C{fx + (66 if right else -66):.0f},{fy:.0f} {ex + (-14 if right else 14):.0f},{ly:.0f} {ex:.0f},{ly:.0f}" fill="none" stroke="{col}" stroke-width="2" opacity=".6"/>')
            if star:
                out.append(f'<a href="{lesson_for[t["name"]]}"><rect x="{x0:.0f}" y="{ly - 15:.0f}" width="{wbox:.0f}" height="30" rx="15" fill="{col}"/>'
                           + svg_text(x0 + wbox / 2, ly, "★ " + label, 14, "700", "white") + "</a>")
            else:
                out.append(f'<rect x="{x0:.0f}" y="{ly - 13:.0f}" width="{wbox:.0f}" height="26" rx="13" fill="white" stroke="{col}"/>'
                           + svg_text(x0 + wbox / 2, ly, label, 13, "500", "#334"))
        out.append(f'<a href="{TOOLBOX}#{fam["id"]}"><circle cx="{fx:.0f}" cy="{fy:.0f}" r="50" fill="white" stroke="{col}" stroke-width="4"/>'
                   + svg_text(fx, fy, fam["map"], 14, "700", col) + "</a>")
    out.append(f'<a href="{TOOLBOX}"><circle cx="{cx}" cy="{cy}" r="72" fill="#0f766e"/>'
               + svg_text(cx, cy, "Tools for|Thinking", 19, "700", "white") + "</a>")
    out.append("</svg>")
    return "".join(out)


def dashboard(tb, lessons):
    cards = []
    for d in lessons:
        c = d["card"]
        cards.append(f'''        <a class="story-card" href="tib_{d["slug"]}_b2.html">
            <div class="story-num">TOOL {d["num"]:02d} &middot; {c["shape"]}</div>
            <div class="story-title">{d["tool"]}</div>
            <div class="story-author">{c["who"]}</div>
            <div class="story-essence">{c["essence"]}</div>
            <div class="story-turn"><span>The story:</span> {d["title"]}</div>
            <div class="story-foot"><span class="grammar-tag">{d["grammar"]["name"]}</span><span class="go">Open &rarr;</span></div>
        </a>''')
    hotspots = "\n".join(
        f'            <a class="hot" href="tib_{d["slug"]}_b2.html" title="{E(d["tool"])}" '
        f'style="left:{h[0]}%;top:{h[1]}%;width:{h[2]}%;height:{h[3]}%"><span>{d["tool"]}</span></a>'
        for d in lessons if (h := d["card"].get("hotspot")))
    total = sum(len(f["tools"]) for f in tb["families"])
    dash_css = recolour(re.search(r"<style>\n(.*?)</style>", open(os.path.join(ROOT, "true_science_stories_dashboard.html")).read(), re.S).group(1))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>Think Inside the Box &middot; B2</title>
<style>
{dash_css}
.map {{ background:white; border:1px solid #cfe7e3; border-radius:14px; padding:14px; margin-bottom:30px; box-shadow:0 2px 8px rgba(0,0,0,.04); }}
.map-frame {{ position:relative; }}
.map-frame img {{ display:block; width:100%; height:auto; border-radius:10px; }}
.map-frame svg {{ display:block; width:100%; height:auto; }}
.map-frame svg a {{ cursor:pointer; }}
.map-frame svg a:hover circle, .map-frame svg a:hover rect {{ filter:brightness(1.12); }}
.hot {{ position:absolute; display:block; border-radius:14px; }}
.hot span {{ position:absolute; left:50%; bottom:100%; transform:translateX(-50%); white-space:nowrap; background:#0f766e; color:white; font-size:.8rem; font-weight:600; padding:3px 10px; border-radius:10px; opacity:0; pointer-events:none; transition:opacity .15s; }}
.hot:hover {{ box-shadow:0 0 0 3px #f59e0b, 0 0 18px rgba(245,158,11,.6); }}
.hot:hover span {{ opacity:1; }}
.map-note {{ text-align:center; font-size:.88rem; color:#667; margin-top:8px; }}
.map-note a {{ color:#0f766e; font-weight:600; }}
.grammar-tag::first-letter {{ text-transform:uppercase; }}
.toolbox-cta {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:14px; background:linear-gradient(135deg,#0e7490,#0f766e); color:white; border-radius:14px; padding:22px 26px; margin-bottom:30px; text-decoration:none; }}
.toolbox-cta b {{ font-size:1.25rem; display:block; }}
.toolbox-cta .go-btn {{ background:white; color:#0f766e; font-weight:700; padding:8px 18px; border-radius:18px; }}
</style>
</head>
<body>
<div class="container">
    <header style="padding:64px 26px; background: linear-gradient(rgba(10,50,48,0.62), rgba(10,50,48,0.62)), url('{HERO_IMG}') center/cover no-repeat, linear-gradient(135deg, #0e7490 0%, #0f766e 100%);">
        <span class="tag">True stories &middot; thinking tools &middot; speaking &middot; B2</span>
        <h1>Think Inside the Box</h1>
        <p class="subtitle">The grids, pyramids, loops and diagrams the world uses to think &mdash; and the true stories of the people who drew them.</p>
    </header>

    <div class="intro">
{chr(10).join("        <p>" + p + "</p>" for p in tb["dash_intro"])}
    </div>

    <p class="section-label">The map &mdash; click a starred tool to open its lesson</p>
    <div class="map">
        <div class="map-frame" id="mapframe">
            <img src="{MAP_IMG}" alt="A mind map of the main families of thinking tools" onerror="document.getElementById('mapframe').innerHTML=document.getElementById('mapsvg').innerHTML">
{hotspots}
        </div>
        <template id="mapsvg">{mind_map_svg(tb, lessons)}</template>
        <p class="map-note">Six families of tools. The ten starred ones have a full lesson below &mdash; all {total} are in <a href="{TOOLBOX}">the Toolbox</a>.</p>
    </div>

    <p class="section-label">The ten lessons</p>
    <div class="story-grid">
{chr(10).join(cards)}
    </div>

    <a class="toolbox-cta" href="{TOOLBOX}">
        <span><b>The Toolbox: all {total} tools</b>Every tool in one list &mdash; search it, or filter by field: business, psychology, medicine, education, the military&hellip;</span>
        <span class="go-btn">Open the Toolbox &rarr;</span>
    </a>

    <div class="how">
        <h2>How each lesson works</h2>
        <div class="how-steps">
            <div class="how-step"><div class="n">1 &middot; Key Words</div><p>Ten words from the story, worked out before you read.</p></div>
            <div class="how-step"><div class="n">2 &middot; The Story</div><p>The true story of how the tool was born, in three parts, with talk after each.</p></div>
            <div class="how-step"><div class="n">3 &middot; The Tool</div><p>How it works, a chance to use it yourself, and where it breaks.</p></div>
            <div class="how-step"><div class="n">4 &middot; Grammar</div><p>One grammar point that the tool itself needs.</p></div>
            <div class="how-step"><div class="n">5 &middot; Speak</div><p>Use the tool on your own life, work and decisions &mdash; out loud.</p></div>
        </div>
    </div>

    <footer>{SERIES} &middot; B2 &middot; Malcolm Hyndman</footer>
</div>
</body>
</html>
'''


def main():
    lessons = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    tb = json.load(open(os.path.join(HERE, "tib_toolbox.json")))
    names = {t["name"] for f in tb["families"] for t in f["tools"]}
    for d in lessons:
        assert d["tool"] in names, f'{d["tool"]} is missing from the toolbox list'
        n_items = sum(len(s["items"]) for s in d["vocab"])
        assert n_items == 10, f'{d["slug"]}: {n_items} vocab items, want 10'
        ans = [it["answer"] for it in d["tool_tab"]["sort"]["items"]]
        assert all(a in d["tool_tab"]["sort"]["options"] for a in ans), f'{d["slug"]}: sort answer not in options'
        run = max(len(list(g)) for _, g in __import__("itertools").groupby(ans))
        assert run < 3, f'{d["slug"]}: same sort answer 3 times in a row'
        out = os.path.join(ROOT, f'tib_{d["slug"]}_b2.html')
        open(out, "w").write(lesson(d, lessons))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")
    open(os.path.join(ROOT, TOOLBOX), "w").write(toolbox_page(tb, lessons))
    open(os.path.join(ROOT, DASH), "w").write(dashboard(tb, lessons))
    print(f"  wrote {TOOLBOX} + {DASH}")


if __name__ == "__main__":
    main()
