#!/usr/bin/env python3
"""Build 'The Art of Memory' (30 rooms in six wings) from content files.

  tools/art_of_memory_content/hub.json          -> art-of-memory.html
  tools/art_of_memory_content/NN_<slug>.json    -> lesson-NN-<slug>.html   (one per room)
  (old duplicate file names)                    -> small redirect pages

Notebook look shared with memory_arts_map.html / memory_arts_notes_method.html.
Template CSS/JS live next to this script (art_of_memory_template.css / .js).
Usage: python3 tools/build_art_of_memory.py
"""
import glob, html, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "art_of_memory_content")
CSS = open(os.path.join(HERE, "art_of_memory_template.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "art_of_memory_template.js"), encoding="utf-8").read()
SERIES = "The Art of Memory"
HUB = "art-of-memory.html"
E = html.escape
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@400;700&display=swap" rel="stylesheet">')

OLD_STUBS = {  # old file name -> new file name (kept so old links still work)
    "lesson-01-how-memory-works-interactive.html": 1, "lesson-02-vivid-imagery-interactive.html": 2,
    "lesson-03-body-pegs-interactive.html": 3, "lesson-04-memory-palace-interactive.html": 4,
    "lesson-05-linking-story-interactive.html": 5, "lesson-06-simple-numbers.html": 6,
    "lesson-26-speeches.html": 26,
}
TABS = ["The Story", "The Method", "Try It", "Drill", "Look Back"]

INK, RED, GOLD, PAPER, MUTE = "#1d2a44", "#b4413a", "#8a6a2c", "#fffdf6", "#5d6477"


def fname(d):
    return f'lesson-{d["num"]:02d}-{d["slug"]}.html'


# ---------------------------------------------------------------- diagrams
def svg_open(w, h, label):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{E(label)}">'


def txt(x, y, s, size=22, fill=INK, anchor="middle", weight="700", extra=""):
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{E(s)}</text>'


def d_chain(data):
    nodes = data["nodes"]; per = data.get("per_row", 4)
    W = 760; cw = 148; gap = (W - 40 - per * cw) / max(per - 1, 1)
    rows = math.ceil(len(nodes) / per); H = 30 + rows * 96
    out = [svg_open(W, H, data.get("label", "A chain of linked pictures"))]
    pos = []
    for i, n in enumerate(nodes):
        r, c = divmod(i, per)
        if r % 2: c = per - 1 - c
        x = 20 + c * (cw + gap); y = 20 + r * 96
        pos.append((x, y))
    for i in range(len(nodes) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            a = x1 + cw if x2 > x1 else x1; b = x2 if x2 > x1 else x2 + cw
            out.append(f'<line x1="{a:.0f}" y1="{y1+33}" x2="{b:.0f}" y2="{y2+33}" stroke="{RED}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>')
        else:
            cx = x1 + cw / 2
            out.append(f'<line x1="{cx:.0f}" y1="{y1+66}" x2="{cx:.0f}" y2="{y2}" stroke="{RED}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>')
    for i, (n, (x, y)) in enumerate(zip(nodes, pos)):
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{cw}" height="66" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>')
        out.append(f'<circle cx="{x+16:.0f}" cy="{y+16}" r="13" fill="{GOLD}"/>' + txt(x + 16, y + 23, str(i + 1), 17, "#fff"))
        lines = n.split("\n") if "\n" in n else [n]
        for k, ln in enumerate(lines):
            out.append(txt(x + cw / 2 + 8, y + 40 + (k - (len(lines) - 1) / 2) * 24, ln, 22))
    out.append("</svg>")
    return "".join(out)


def d_plan(data):
    rooms = data["rooms"]; cols = data.get("cols", 3)
    rows = math.ceil(len(rooms) / cols); cw, ch = 220, 112
    W = cols * cw + 40; H = rows * ch + 40
    out = [svg_open(W, H, data.get("label", "A plan of a house with numbered rooms"))]
    out.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round" rx="4"/>')
    centres = []
    for i, r in enumerate(rooms):
        rr, c = divmod(i, cols)
        if rr % 2: c = cols - 1 - c
        x = 20 + c * cw; y = 20 + rr * ch
        centres.append((x + cw / 2, y + ch / 2 + 6))
        out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="1 0"/>')
    out.append('<polyline points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in centres) + f'" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (r, (cx, cy)) in enumerate(zip(rooms, centres)):
        out.append(f'<circle cx="{cx:.0f}" cy="{cy-8:.0f}" r="18" fill="{PAPER}" stroke="{GOLD}" stroke-width="4"/>' + txt(cx, cy - 1, str(i + 1), 22, INK))
        lab = r if isinstance(r, str) else r["label"]
        out.append(txt(cx, cy + 34, lab, 20, MUTE, weight="500"))
    out.append("</svg>")
    return "".join(out)


FIG_PEGS = ["Head", "Eyes", "Nose", "Mouth", "Neck", "Chest", "Stomach", "Legs", "Feet", "Toes"]


def d_figure(data):
    labels = data.get("labels", FIG_PEGS)
    pts = [(200, 34), (200, 88), (200, 118), (200, 146), (200, 198), (200, 248), (200, 312), (200, 392), (176, 468), (226, 468)]
    W, H = 560, 510
    out = [svg_open(W, H, data.get("label", "A figure with ten numbered body pegs"))]
    out.append(f'<circle cx="200" cy="100" r="62" fill="none" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<path d="M200 162 L200 340 M200 190 L120 270 M200 190 L280 270 M200 340 L160 440 L160 470 M200 340 L240 440 L240 470" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<ellipse cx="200" cy="260" rx="40" ry="72" fill="none" stroke="{INK}" stroke-width="3" opacity=".55"/>')
    for i, ((x, y), lab) in enumerate(zip(pts, labels)):
        side = 1 if i not in (8,) else -1
        lx = 330 if side == 1 else 70
        out.append(f'<line x1="{x}" y1="{y}" x2="{lx - (14 if side == 1 else -14)}" y2="{y if i != 9 else 470}" stroke="{GOLD}" stroke-width="2" stroke-dasharray="3 5"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{PAPER}" stroke="{RED}" stroke-width="3.5"/>' + txt(x, y + 7, str(i + 1), 19, INK))
        if i == 9:
            out.append(txt(lx, 477, lab, 25, INK, "start"))
        else:
            out.append(txt(lx, y + 7, lab, 25, INK, "start" if side == 1 else "end"))
    out.append("</svg>")
    return "".join(out)


def d_curve(data):
    W, H = 760, 330; x0, y0, x1, y1 = 70, 28, 730, 270
    reviews = data.get("reviews", [1, 3, 7, 14, 30]); span = data.get("days", 40)
    def X(t): return x0 + (x1 - x0) * t / span
    def Y(p): return y1 - (y1 - y0) * p
    out = [svg_open(W, H, data.get("label", "Forgetting curve with reviews"))]
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{INK}" stroke-width="3"/><line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="3"/>')
    out.append(txt(24, 150, "how much you keep", 22, MUTE, "middle", "500", 'transform="rotate(-90 24 150)"'))
    out.append(txt((x0 + x1) / 2, 312, "days", 22, MUTE, "middle", "500"))
    # no-review curve
    pts = [(X(t / 4), Y(math.exp(-(t / 4) / 1.8))) for t in range(0, span * 4 + 1)]
    out.append(f'<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="none" stroke="{MUTE}" stroke-width="3" stroke-dasharray="6 6"/>')
    # with reviews
    strength = 1.8; last = 0; path = []
    marks = [0] + reviews
    for k, rv in enumerate(marks):
        end = marks[k + 1] if k + 1 < len(marks) else span
        for t in [last + (end - last) * s / 24 for s in range(0, 25)]:
            path.append((X(t), Y(math.exp(-(t - last) / strength))))
        last = end; strength *= 2.4
    out.append(f'<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in path) + f'" fill="none" stroke="{RED}" stroke-width="4" stroke-linejoin="round"/>')
    for k, rv in enumerate(reviews):
        out.append(f'<line x1="{X(rv):.0f}" y1="{y1}" x2="{X(rv):.0f}" y2="{y1+8}" stroke="{INK}" stroke-width="3"/>' + txt(X(rv), y1 + 28, str(rv), 20, INK))
    out.append(txt(x1 - 6, 70, "with reviews", 24, RED, "end") + txt(x1 - 6, 205, "no review", 24, MUTE, "end", "500"))
    out.append("</svg>")
    return "".join(out)


def d_map(data):
    W, H = 760, 460; cx, cy = W / 2, H / 2
    br = data["branches"]; n = len(br)
    cols = [INK, RED, GOLD]
    out = [svg_open(W, H, data.get("label", "A mind map"))]
    for i, b in enumerate(br):
        ang = -math.pi / 2 + 2 * math.pi * i / n + (0.35 if n % 2 == 0 else 0)
        col = cols[i % 3]
        bx, by = cx + 190 * math.cos(ang), cy + 135 * math.sin(ang)
        out.append(f'<path d="M{cx:.0f} {cy:.0f} Q{(cx+bx)/2+10:.0f} {(cy+by)/2-10:.0f} {bx:.0f} {by:.0f}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
        anchor = "start" if math.cos(ang) > 0.25 else ("end" if math.cos(ang) < -0.25 else "middle")
        out.append(txt(bx + (8 if anchor == "start" else -8 if anchor == "end" else 0), by + (-10 if abs(math.cos(ang)) <= 0.25 and math.sin(ang) < 0 else 6), b["label"], 24, col, anchor))
        kids = b.get("kids", [])
        for j, k in enumerate(kids):
            off = (j - (len(kids) - 1) / 2) * 24
            kx = bx + (34 if anchor != "end" else -34) * (1 if math.cos(ang) >= 0 else -1)
            ky = by + off + (0 if abs(math.sin(ang)) < .8 else (24 if math.sin(ang) > 0 else -26)) + 12
            out.append(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{kx:.0f}" y2="{ky-5:.0f}" stroke="{col}" stroke-width="2"/>')
            out.append(txt(kx + (4 if math.cos(ang) >= 0 else -4), ky, k, 18, "#33405a", "start" if math.cos(ang) >= 0 else "end", "500"))
    out.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="86" ry="42" fill="{INK}"/>' + txt(cx, cy + 8, data["centre"], 24, "#fff"))
    out.append("</svg>")
    return "".join(out)


def d_network(data):
    nodes = data["nodes"]; n = len(nodes); W, H = 760, 380; cx, cy = W / 2, H / 2
    pos = []
    for i in range(n):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + 250 * math.cos(ang), cy + 125 * math.sin(ang)))
    out = [svg_open(W, H, data.get("label", "A network of palaces"))]
    for a, b, lab in data.get("links", []):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{RED}" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/>')
        out.append(txt((x1 + x2) / 2, (y1 + y2) / 2 - 6, lab, 19, RED, weight="500"))
    for (x, y), nd in zip(pos, nodes):
        lab = nd if isinstance(nd, str) else nd["label"]
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="82" ry="38" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>' + txt(x, y + 8, lab, 22, INK))
    out.append("</svg>")
    return "".join(out)


DIAGRAMS = {"chain": d_chain, "plan": d_plan, "figure": d_figure, "curve": d_curve, "map": d_map, "network": d_network}


def diagram(b):
    cap = f'<div class="cap">{b["cap"]}</div>' if b.get("cap") else ""
    return f'<div class="diagram">{DIAGRAMS[b["kind"]](b["data"])}{cap}</div>'


# ---------------------------------------------------------------- method blocks
def block(b):
    t = b["t"]
    if t == "h": return f'<h3>{b["x"]}</h3>'
    if t == "p": return f'<p>{b["x"]}</p>'
    if t == "lead": return f'<p class="lead">{b["x"]}</p>'
    if t == "sticky": return f'<div class="sticky{" r" if b.get("r") else ""}">{b["x"]}</div>'
    if t == "src": return f'<p class="src">{b["x"]}</p>'
    if t == "ul": return "<ul>" + "".join(f"<li>{i}</li>" for i in b["items"]) + "</ul>"
    if t == "steps": return '<ol class="steps">' + "".join(f'<li><b>{i["h"]}</b> {i["x"]}</li>' for i in b["items"]) + "</ol>"
    if t == "chips": return '<div class="chips">' + "".join(f"<span>{i}</span>" for i in b["items"]) + "</div>"
    if t == "table":
        head = "".join(f"<th>{h}</th>" for h in b["head"])
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b["rows"])
        return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    if t == "example":
        rows = "".join(f'<div class="row"><span class="k">{k}</span><span>{v}</span></div>' for k, v in b["lines"])
        pic = f'<div class="pic"><b>The picture:</b> {b["pic"]}</div>' if b.get("pic") else ""
        return f'<div class="example"><span class="lbl">{b.get("title", "A worked example")}</span><div class="given">{b["given"]}</div>{rows}{pic}</div>'
    if t == "diagram": return diagram(b)
    if t == "image":
        return f'<figure class="pol" style="--tilt:{b.get("tilt", "-1.2deg")}"><img src="{b["src"]}" alt="{E(b["alt"])}" loading="lazy" onerror="this.closest(\'figure\').style.display=\'none\'"><figcaption>{b["cap"]}</figcaption></figure>'
    if t == "reveal": return f'<button class="reveal-btn">{b["btn"]}</button><div class="reveal">{b["x"]}</div>'
    if t == "talk": return f'<div class="talk"><b class="t">Say it aloud.</b> {b["x"]}</div>'
    raise ValueError("unknown block " + t)


# ---------------------------------------------------------------- exercises
class Ids:
    n = 0
    @classmethod
    def next(cls):
        cls.n += 1; return f"x{cls.n}"


def ex_build(e):
    checks = "".join(f'<label><input type="checkbox"> {c}</label>' for c in e.get("checks", []))
    model = f'<button class="reveal-btn">{e.get("btn", "See a model")}</button><div class="reveal">{e["model"]}</div>' if e.get("model") else ""
    save = f' data-save="{e["id"]}"' if e.get("id") else ""
    return (f'<div class="ex"><h4>{e["title"]}</h4><div class="prompt">{e["prompt"]}</div>'
            f'<textarea rows="{e.get("rows", 3)}" placeholder="{E(e.get("ph", "Write it here…"))}"{save}></textarea>'
            f'<div class="checks">{checks}</div><div class="fb"></div>{model}</div>')


def ex_gap(e):
    out = [f'<div class="ex"><h4>{e["title"]}</h4>']
    if e.get("prompt"): out.append(f'<div class="prompt">{e["prompt"]}</div>')
    for it in e["items"]:
        parts = it["s"].split("___")
        ans = it["a"] if isinstance(it["a"], list) else [it["a"]]
        if len(parts) == 2 and len(ans) > 1:
            ans = ["|".join(ans)]
        assert len(parts) - 1 == len(ans), f'gap blanks/answers mismatch: {it["s"]}'
        s = parts[0]
        for k, a in enumerate(ans):
            iid = Ids.next()
            s += f'<input type="text" class="gapin" id="{iid}" data-ans="{E(a)}" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="answer"><span class="gapans" data-for="{iid}"></span>' + parts[k + 1]
        out.append(f'<div class="gaprow">{s}</div>')
    out.append('<button class="btn primary" data-act="gap">Check</button><div class="fb"></div></div>')
    return "".join(out)


def ex_mc(e):
    opts = "".join(f'<button class="mc-opt" data-act="mc" data-ok="{1 if i == e["ans"] else 0}"' + (f' data-hint="{E(e["hints"][str(i)])}"' if e.get("hints", {}).get(str(i)) else "") + f'>{o}</button>' for i, o in enumerate(e["opts"]))
    return f'<div class="ex" data-why="{E(e["why"])}"><div class="prompt"><b>{e["q"]}</b></div>{opts}<div class="fb"></div></div>'


def ex_match(e):
    right = sorted({r for _, r in e["pairs"]})
    rows = []
    for l, r in e["pairs"]:
        o = '<option value="">choose…</option>' + "".join(f'<option value="{E(x)}">{x}</option>' for x in right)
        rows.append(f'<div class="match-row"><span class="txt">{l}</span><select data-ans="{E(r)}" aria-label="match">{o}</select></div>')
    return f'<div class="ex"><h4>{e["title"]}</h4>' + (f'<div class="prompt">{e["prompt"]}</div>' if e.get("prompt") else "") + "".join(rows) + '<button class="btn primary" data-act="match">Check</button><div class="fb"></div></div>'


def timer_box(secs, label="Start the timer"):
    m, s = divmod(secs, 60)
    return (f'<div class="timer-box" data-secs="{secs}"><span class="timer">{m}:{s:02d}</span>'
            f'<button class="btn" data-act="timer">{label}</button><button class="btn" data-act="timer-reset">Reset</button> <span class="savednote timer-msg"></span></div>')


def ex_talk(e):
    return (f'<div class="ex"><h4>{e["title"]}</h4><div class="prompt">{e["prompt"]}</div>'
            + timer_box(e.get("secs", 60), "Start talking") + '</div>')


EX = {"build": ex_build, "gap": ex_gap, "mc": ex_mc, "match": ex_match, "talk": ex_talk}


def exercise(e):
    return EX[e["t"]](e)


def deck(cards):
    return (f'<div class="card-deck" data-i="0" data-cards="{E(json.dumps(cards, ensure_ascii=False))}">'
            '<div class="fcard" tabindex="0" role="button" aria-label="Flip the card"><div class="front"></div><div class="back"></div><div class="tap">tap to turn over</div></div>'
            '<div class="deck-ctl"><button class="btn" data-act="prev">&larr;</button><span class="cnt"></span>'
            '<button class="btn" data-act="next">&rarr;</button><button class="btn" data-act="shuffle">Shuffle</button></div></div>')


def challenge(c):
    items = c["items"]; secs = c.get("secs", 60); ordered = 1 if c.get("ordered", True) else 0
    return (f'<div class="recall" data-items="{E(json.dumps(items, ensure_ascii=False))}" data-secs="{secs}" data-ordered="{ordered}">'
            f'<h4>{c["title"]}</h4>'
            f'<div class="stage on" data-stage="start"><p>{c["intro"]}</p><button class="btn primary" data-act="rc-start">Start: {secs} seconds to study</button></div>'
            f'<div class="stage" data-stage="study"><p>{c.get("study", "Make a picture for each one and put it in place. Do not just read.")}</p>'
            '<div class="timer-box"><span class="timer">0:00</span><button class="btn" data-act="rc-ready">I’m ready</button></div><div class="items"></div></div>'
            f'<div class="stage" data-stage="recall"><p>{c.get("recall", "The list has gone. Type what you remember, one item per line.")}</p>'
            '<textarea rows="8" placeholder="One per line…"></textarea><button class="btn primary" data-act="rc-check">Check</button></div>'
            '<div class="stage" data-stage="result"><div class="score"></div><div class="res"></div><button class="btn" data-act="rc-again">Try again</button></div></div>')


# ---------------------------------------------------------------- lesson page
def wing_of(num, hub):
    for w in hub["wings"]:
        if num in w["rooms"]: return w
    raise KeyError(num)


def story_tab(d, titles):
    s = d["story"]; out = []
    out.append(f'<div class="intention"><b>In this room:</b> {d["goal"]}</div>')
    if d.get("left_off"):
        qa = "".join(f'<div class="qa"><div class="q">{x["q"]}</div><button class="reveal-btn">Check</button><div class="reveal">{x["a"]}</div></div>' for x in d["left_off"])
        out.append(f'<div class="left-off"><span class="lbl">{d.get("left_off_label", "Where we left off")}</span>{qa}</div>')
    out.append(f'<h2>{s["heading"]}</h2>')
    for i, p in enumerate(s["parts"]):
        paras = "".join(f"<p>{x}</p>" for x in p["text"])
        chk = f'<div class="qa"><div class="q">{p["check"]["q"]}</div><button class="reveal-btn">Check from memory</button><div class="reveal">{p["check"]["a"]}</div></div>' if p.get("check") else ""
        talk = f'<div class="talk"><b class="t">Talk about it.</b> {p["talk"]}</div>' if p.get("talk") else ""
        out.append(f'<div class="story-part"><div class="story-chunk">{paras}</div><div class="after">{chk}{talk}</div></div>')
        if i == 0 and d.get("image"):
            im = d["image"]
            out.append(block({"t": "image", **im}))
    out.append("<h3>Words worth knowing</h3><p>Say what you think each one means, then open it.</p><div class=\"words\">")
    for w in d["words"]:
        out.append(f'<div class="word"><button class="w" type="button">{w["w"]}</button><div class="m">{w["m"]}</div></div>')
    out.append("</div>")
    if d.get("source"): out.append(f'<p class="src">{d["source"]}</p>')
    return "".join(out)


def method_tab(d):
    return f'<h2>{d["method_heading"]}</h2>' + "".join(block(b) for b in d["method"])


def try_tab(d):
    parts = [f'<h2>{d.get("try_heading", "Now you build")}</h2>', f'<p>{d.get("try_intro", "Have a go before you open any answer. A rough attempt teaches you more than a perfect model you only read.")}</p>']
    parts += [exercise(e) for e in d["try"]]
    return "".join(parts)


def drill_tab(d, titles):
    dr = d["drill"]
    parts = ['<h2>Drill</h2>', '<h3>Flash cards</h3><p>Say the answer first, then tap the card.</p>', deck(dr["cards"]), '<h3>Quick quiz</h3>']
    parts += [exercise({"t": "mc", **q}) for q in dr["quiz"]]
    parts += ['<h3>The memory challenge</h3>', challenge(d["challenge"])]
    return "".join(parts)


def back_tab(d, titles, prev, nxt):
    parts = ['<h2>Look back</h2>', '<p>These reach back to earlier rooms. Answer in your head or out loud, then check.</p>']
    for x in d["look_back"]:
        t = titles[x["from"]]
        parts.append(f'<div class="qa"><div class="q"><span class="red">Room {x["from"]} · {t}.</span> {x["q"]}</div><button class="reveal-btn">Check</button><div class="reveal">{x["a"]}</div></div>')
    parts.append('<h3>What I can do now</h3><ul class="canlist">')
    for i, c in enumerate(d["can_do"]):
        parts.append(f'<li><label><input type="checkbox" data-save="can{i}"> <span>I can {c}</span></label></li>')
    parts.append("</ul>")
    parts.append(f'<h3>A thought to keep</h3><p>{d["reflect"]}</p><div class="ref"><textarea rows="3" data-save="reflect" placeholder="Your thoughts…"></textarea><div class="savednote">Saved on this device as you type.</div></div>')
    parts.append('<p><button class="btn primary" data-act="done">Mark this room as done</button></p>')
    return "".join(parts)


def lesson_page(d, hub, lessons):
    titles = {x["num"]: x["title"] for x in lessons}
    w = wing_of(d["num"], hub)
    prev = next((x for x in lessons if x["num"] == d["num"] - 1), None)
    nxt = next((x for x in lessons if x["num"] == d["num"] + 1), None)
    nav = []
    nav.append(f'<a href="{fname(prev)}">&larr; {prev["title"]}</a>' if prev else f'<a href="{HUB}">&larr; The house</a>')
    nav.append(f'<a href="{HUB}">The whole house</a>')
    nav.append(f'<a href="{fname(nxt)}">{nxt["title"]} &rarr;</a>' if nxt else f'<a href="{HUB}">Back to the house</a>')
    nav = '<div class="nav-end">' + "".join(nav) + "</div>"
    tabs = "".join(f'<button class="tab-btn{" active" if i == 0 else ""}" role="tab" onclick="showTab({i})">{n}</button>' for i, n in enumerate(TABS))
    panels = [story_tab(d, titles), method_tab(d), try_tab(d), drill_tab(d, titles), back_tab(d, titles, prev, nxt)]
    pages = "".join(f'<div class="tab-content{" active" if i == 0 else ""}" id="tab{i}"><section class="page"><div class="pgno">{d["num"]}</div>{p}</section></div>' for i, p in enumerate(panels))
    desc = E(d["tagline"], quote=True)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<meta name="description" content="{desc}">
<title>{E(d["title"])} · {SERIES} · Room {d["num"]}</title>
{FONTS}
<style>
{CSS}</style>
</head>
<body data-lesson="{d["num"]:02d}">
<div class="wrap">
  <div class="topnav"><a href="{HUB}">&larr; The Art of Memory</a><span class="where">Wing {w["roman"]} · {w["name"]}</span></div>
  <header class="cover">
    <span class="plaque">Room {d["num"]} of 30</span>
    <small>{w["name"]}</small>
    <h1>{d["title"]}</h1>
    <p>{d["tagline"]}</p>
  </header>
  <nav class="tab-nav" role="tablist">{tabs}</nav>
{pages}
  {nav}
  <footer>The Art of Memory · Room {d["num"]} · {d["title"]}</footer>
</div>
<script>
{JS}</script>
</body>
</html>
'''


# ---------------------------------------------------------------- hub
ICON = {
    1: '<rect x="14" y="8" width="36" height="48" rx="3" fill="none" stroke="%(c)s" stroke-width="3"/><path d="M14 56 V26 A18 18 0 0 1 50 26 V56" fill="none" stroke="%(c)s" stroke-width="3"/><circle cx="42" cy="34" r="3" fill="%(c)s"/>',
    2: '<rect x="8" y="10" width="48" height="44" rx="3" fill="none" stroke="%(c)s" stroke-width="3"/><path d="M8 24 H56 M8 38 H56" stroke="%(c)s" stroke-width="2"/><g fill="%(c)s"><circle cx="20" cy="17" r="3.5"/><circle cx="32" cy="17" r="3.5"/><circle cx="26" cy="31" r="3.5"/><circle cx="42" cy="31" r="3.5"/><circle cx="18" cy="45" r="3.5"/><circle cx="34" cy="45" r="3.5"/><circle cx="46" cy="45" r="3.5"/></g>',
    3: '<path d="M6 24 L12 8 H52 L58 24 Z" fill="none" stroke="%(c)s" stroke-width="3" stroke-linejoin="round"/><path d="M6 24 q6.5 8 13 0 q6.5 8 13 0 q6.5 8 13 0 q6.5 8 13 0" fill="none" stroke="%(c)s" stroke-width="3"/><path d="M12 32 V56 M52 32 V56 M8 56 H56" stroke="%(c)s" stroke-width="3"/>',
    4: '<g fill="none" stroke="%(c)s" stroke-width="3" stroke-linejoin="round"><rect x="10" y="12" width="10" height="44"/><rect x="22" y="8" width="10" height="48"/><rect x="34" y="14" width="10" height="42"/><path d="M47 57 L56 18 L60 19 L51 58 Z"/></g>',
    5: '<g fill="none" stroke="%(c)s" stroke-width="3" stroke-linejoin="round"><path d="M22 58 V22 H42 V58 Z"/><path d="M18 22 V14 H24 V18 H30 V14 H34 V18 H40 V14 H46 V22"/><path d="M32 14 V4 L44 8 L32 11"/><path d="M29 40 a3 3 0 0 1 6 0 V50 H29 Z"/></g>',
    6: '<g fill="none" stroke="%(c)s" stroke-width="3" stroke-linejoin="round"><path d="M6 24 L32 8 L58 24 Z"/><path d="M12 28 V54 M24 28 V54 M40 28 V54 M52 28 V54 M6 56 H58"/></g>',
}


def icon(n, c=INK):
    return f'<svg class="wicon" viewBox="0 0 64 64" width="44" height="44" aria-hidden="true">{ICON[n] % {"c": c}}</svg>'


HUB_CSS = """
.wing { margin:0 0 34px; }
.wing-h { display:flex; gap:14px; align-items:center; margin-bottom:6px; }
.wing-h h2 { font-size:2.3rem; line-height:1; color:var(--ink); }
.wing-h .num { font-family:"Caveat",cursive; font-size:1.4rem; color:var(--red); display:block; line-height:1; }
.wing > p.blurb { color:var(--muted); margin:0 0 12px; max-width:700px; }
.rooms { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }
.room { position:relative; display:flex; flex-direction:column; text-decoration:none; color:inherit; background:var(--sheet); border:1px solid var(--line); box-shadow:0 6px 18px var(--shadow); padding:16px 18px 14px 56px; transition:transform .15s, box-shadow .15s; }
.room:hover { transform:translate(-2px,-2px); box-shadow:0 10px 24px rgba(22,38,61,.24); }
.room .n { position:absolute; left:10px; top:8px; width:38px; text-align:center; font-family:"Caveat",cursive; font-size:2.4rem; font-weight:700; color:var(--red); line-height:1.1; }
.room .t { font-family:"Caveat",cursive; font-size:1.7rem; font-weight:700; color:var(--ink); line-height:1.1; margin-bottom:2px; }
.room .e { font-size:.95rem; color:#33405a; flex:1; }
.room .go { font-family:"Caveat",cursive; font-size:1.25rem; color:var(--gold); font-weight:700; margin-top:6px; }
.room.done::after { content:"\\2713 done"; position:absolute; right:10px; top:8px; font-family:"Caveat",cursive; font-size:1.2rem; color:#2f7a36; font-weight:700; }
.plan { background:var(--sheet); border:2px dashed var(--line); padding:8px; margin:0 0 30px; }
.plan svg { display:block; width:100%; height:auto; font-family:"Caveat",cursive; }
.plan a { cursor:pointer; } .plan a circle { transition:fill .15s; } .plan a:hover circle { fill:var(--gold); } .plan a:hover text { fill:#fff; }
.how { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; margin:10px 0 28px; }
.how div { background:var(--sheet); border:1px solid var(--line); padding:10px 14px; box-shadow:0 4px 12px var(--shadow); }
.how b { font-family:"Caveat",cursive; font-size:1.5rem; color:var(--red); display:block; line-height:1.1; }
.how span { font-size:.92rem; color:#33405a; }
.cta { text-align:center; margin:18px 0 6px; }
.cta a { display:inline-block; font-family:"Caveat",cursive; font-size:1.7rem; font-weight:700; text-decoration:none; color:#fff; background:var(--ink); padding:4px 30px 2px; border-radius:255px 15px 225px 15px/15px 225px 15px 255px; }
.cta a:hover { background:var(--gold); }
.side { background:var(--sheet); border:1px solid var(--line); box-shadow:0 6px 18px var(--shadow); padding:14px 20px 10px; margin:0 0 22px; }
.side h3 { font-size:1.7rem; color:var(--gold); line-height:1.1; margin-bottom:4px; }
.side ul { margin:0 0 6px 20px; } .side li { margin-bottom:3px; }
.page.intro { padding-left:28px; margin-bottom:26px; } .page.intro::before { display:none; }
.progress { font-family:"Caveat",cursive; font-size:1.4rem; color:var(--muted); text-align:center; margin:4px 0 14px; min-height:1.6rem; }
@media (max-width:640px) { .plan { display:none; } .wing-h h2 { font-size:2rem; } }
"""


def hub_plan(hub, lessons):
    W, H = 900, 560; bw, bh = 280, 230
    px = [30, 310 + 10, 600 + 10]; py = [30, 300]
    out = [svg_open(W, H, "Plan of the house of memory: six wings, thirty rooms")]
    out.append(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{INK}" stroke-width="6" rx="6"/>')
    centres = []
    for i, w in enumerate(hub["wings"]):
        r, c = divmod(i, 3)
        if r == 1: c = 2 - c
        x = 24 + c * 292; y = 24 + r * 262
        out.append(f'<rect x="{x}" y="{y}" width="280" height="250" fill="none" stroke="{INK}" stroke-width="2.5"/>')
        out.append(txt(x + 140, y + 36, f'Wing {w["roman"]}', 20, RED))
        out.append(txt(x + 140, y + 66, w["name"], 28, INK))
        n = len(w["rooms"]); gx = (280 - 40) / (n - 1)
        pts = []
        for k, num in enumerate(w["rooms"]):
            cx = x + 20 + k * gx; cy = y + 150 + (-26 if k % 2 else 26) * (1 if r == 0 else 1)
            pts.append((cx, cy))
        out.append('<polyline points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + f'" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="2 7" stroke-linecap="round"/>')
        for (cx, cy), num in zip(pts, w["rooms"]):
            t = next(l for l in lessons if l["num"] == num)
            out.append(f'<a href="{fname(t)}"><title>Room {num}: {E(t["title"])}</title><circle cx="{cx:.0f}" cy="{cy:.0f}" r="21" fill="{PAPER}" stroke="{GOLD}" stroke-width="4"/>' + txt(cx, cy + 8, str(num), 22, INK) + "</a>")
        centres.append((x, y))
    out.append("</svg>")
    return "".join(out)


def hub_page(hub, lessons):
    wings = []
    for w in hub["wings"]:
        cards = []
        for num in w["rooms"]:
            d = next(l for l in lessons if l["num"] == num)
            cards.append(f'<a class="room" href="{fname(d)}" data-room="{num:02d}"><span class="n">{num}</span><span class="t">{d["title"]}</span><span class="e">{d["card"]}</span><span class="go">Open the room &rarr;</span></a>')
        wings.append(f'<section class="wing" id="wing{w["roman"]}"><div class="wing-h">{icon(w["n"])}<div><span class="num">Wing {w["roman"]}</span><h2>{w["name"]}</h2></div></div><p class="blurb">{w["blurb"]}</p><div class="rooms">' + "".join(cards) + "</div></section>")
    how = "".join(f'<div><b>{n}</b><span>{x}</span></div>' for n, x in hub["how"])
    side = "".join(f'<div class="side"><h3>{s["h"]}</h3>{s["x"]}</div>' for s in hub["sidebars"])
    first = fname(next(l for l in lessons if l["num"] == 1))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<meta name="description" content="{E(hub["tagline"], quote=True)}">
<title>The Art of Memory · 30 Rooms in the House of Memory</title>
{FONTS}
<style>
{CSS}{HUB_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topnav"><a href="malcolm_lesson_index.html">&larr; All lessons</a><span class="where">thirty rooms · six wings</span></div>
  <header class="cover">
    <small>{hub["kicker"]}</small>
    <h1>The Art of Memory</h1>
    <p>{hub["tagline"]}</p>
    <div class="cta"><a href="{first}">Step through the door &rarr;</a></div>
  </header>

  <div class="progress" id="progress"></div>

  <div class="page intro">
    {"".join(f"<p>{p}</p>" for p in hub["intro"])}
    <figure class="pol" style="--tilt:1.4deg;margin-left:auto"><img src="memory_arts_notes_threshold.jpg" alt="An engraved view into an empty grand house at dawn, with small gold markers along the doorway, a window, a hearth and a table." loading="lazy" onerror="this.closest('figure').style.display='none'"><figcaption>an empty house, waiting for its pictures</figcaption></figure>
  </div>

  <div class="plan">{hub_plan(hub, lessons)}</div>

  <h2 class="hand" style="font-size:2.3rem;color:var(--ink);margin-bottom:6px">How every room works</h2>
  <div class="how">{how}</div>

{"".join(wings)}

{side}

  <footer>The Art of Memory · thirty rooms · start at the door</footer>
</div>
<script>
{JS}
(function(){{ try {{ var n = document.querySelectorAll('.room.done').length, p = document.getElementById('progress'); if (n && p) p.textContent = 'You have finished ' + n + ' of 30 rooms.'; }} catch(e) {{}} }})();
</script>
</body>
</html>
'''


# ---------------------------------------------------------------- stubs
def stub(target_file, title):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="0; url={target_file}"><meta name="robots" content="noindex">
<title>Moved</title></head><body style="font-family:sans-serif;padding:24px"><p>This lesson has moved: <a href="{target_file}">{E(title)}</a>.</p></body></html>
'''


# ---------------------------------------------------------------- checks
FORBIDDEN = ["Malcolm", "I Do", "We Do", "You Do", "TEEP", "Pause:", "RETRIEVAL", "Recall Zone", "Elaboration", "Teacher", "your teacher", "Your teacher",
             "Exploration", "Knowledge Building", "Demonstrate", "Consolidate", "Activate", "Watch Me", "Your Turn", "Teacher Models"]


def check(d, valid_nums):
    blob = json.dumps(d, ensure_ascii=False)
    for bad in FORBIDDEN:
        assert bad not in blob, f'{d["slug"]}: forbidden word {bad!r}'
    assert "<script" not in blob.lower(), f'{d["slug"]}: script in content'
    assert 3 <= len(d["story"]["parts"]) <= 4, f'{d["slug"]}: story needs 3 or 4 parts'
    assert 4 <= len(d["words"]) <= 8, f'{d["slug"]}: words'
    assert len(d["try"]) >= 5, f'{d["slug"]}: needs at least 5 exercises'
    assert len(d["drill"]["cards"]) >= 6 and len(d["drill"]["quiz"]) >= 4, f'{d["slug"]}: drill too thin'
    assert len(d["challenge"]["items"]) >= 5, f'{d["slug"]}: challenge'
    assert len(d["look_back"]) >= 4 and len(d["can_do"]) >= 3, f'{d["slug"]}: look back'
    for q in d["drill"]["quiz"]:
        assert 0 <= q["ans"] < len(q["opts"]), f'{d["slug"]}: quiz answer index'
    for e in d["try"]:
        if e["t"] == "mc": assert 0 <= e["ans"] < len(e["opts"])
    for x in d["look_back"]:
        assert x["from"] in valid_nums and (x["from"] < d["num"] or d["num"] == 1), f'{d["slug"]}: look_back from {x["from"]}'
    wc = len(re.sub(r"<[^>]+>", " ", " ".join(" ".join(p["text"]) for p in d["story"]["parts"])).split())
    assert 230 <= wc <= 700, f'{d["slug"]}: story is {wc} words'


def main():
    hub = json.load(open(os.path.join(CONTENT, "hub.json"), encoding="utf-8"))
    files = sorted(p for p in glob.glob(os.path.join(CONTENT, "[0-9][0-9]_*.json")))
    lessons = [json.load(open(p, encoding="utf-8")) for p in files]
    nums = [l["num"] for l in lessons]
    assert nums == sorted(set(nums)), f"duplicate or unsorted lesson numbers: {nums}"
    valid = set(nums)
    for d in lessons:
        check(d, valid)
        Ids.n = 0
        out = os.path.join(ROOT, fname(d))
        open(out, "w", encoding="utf-8").write(lesson_page(d, hub, lessons))
        print(f"  wrote {fname(d)}  ({os.path.getsize(out)//1024}KB)")
    if len(lessons) == 30:
        for old, n in OLD_STUBS.items():
            d = next(l for l in lessons if l["num"] == n)
            open(os.path.join(ROOT, old), "w", encoding="utf-8").write(stub(fname(d), d["title"]))
        open(os.path.join(ROOT, HUB), "w", encoding="utf-8").write(hub_page(hub, lessons))
        print(f"  wrote {HUB}")
    else:
        print(f"  {len(lessons)} of 30 lessons so far; hub and redirects not written")


if __name__ == "__main__":
    main()
