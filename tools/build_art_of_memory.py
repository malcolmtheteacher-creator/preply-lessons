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
FONTS = ""

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
    size = round(size * 0.84)
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
    out.append(f'<div class="intention"><b>In this lesson:</b> {d["goal"]}</div>')
    if d.get("left_off"):
        qa = "".join(f'<div class="qa"><div class="q">{x["q"]}</div><button class="reveal-btn">Check</button><div class="reveal">{x["a"]}</div></div>' for x in d["left_off"])
        out.append(f'<div class="left-off"><span class="lbl">{d.get("left_off_label", "Where we left off")}</span>{qa}</div>')
    out.append(f'<h2>{s["heading"]}</h2>')
    for i, p in enumerate(s["parts"]):
        paras = "".join(f"<p>{x}</p>" for x in p["text"])
        chk = f'<div class="qa"><div class="q">{p["check"]["q"]}</div><button class="reveal-btn">Check from memory</button><div class="reveal">{p["check"]["a"]}</div></div>' if p.get("check") else ""
        talk = f'<div class="talk"><b class="t">Talk about it.</b> {p["talk"]}</div>' if p.get("talk") else ""
        out.append(f'<div class="story-part"><div class="story-chunk">{paras}</div><div class="after">{chk}{talk}</div></div>')
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
        parts.append(f'<div class="qa"><div class="q"><span class="red">Lesson {x["from"]} · {t}.</span> {x["q"]}</div><button class="reveal-btn">Check</button><div class="reveal">{x["a"]}</div></div>')
    parts.append('<h3>What I can do now</h3><ul class="canlist">')
    for i, c in enumerate(d["can_do"]):
        parts.append(f'<li><label><input type="checkbox" data-save="can{i}"> <span>I can {c}</span></label></li>')
    parts.append("</ul>")
    parts.append(f'<h3>A thought to keep</h3><p>{d["reflect"]}</p><div class="ref"><textarea rows="3" data-save="reflect" placeholder="Your thoughts…"></textarea><div class="savednote">Saved on this device as you type.</div></div>')
    parts.append('<p><button class="btn primary" data-act="done">Mark this room as done</button></p>')
    return "".join(parts)


PICS = {1: "images", 2: "images", 3: "threshold", 4: "banquet", 5: "images", 6: "wheel", 7: "wheel", 8: "allegory", 9: "images", 10: "wheel",
        11: "allegory", 12: "images", 13: "banquet", 14: "wheel", 15: "images", 16: "allegory", 17: "allegory", 18: "wheel", 19: "wheel", 20: "allegory",
        21: "images", 22: "banquet", 23: "wheel", 24: "wheel", 25: "allegory", 26: "banquet", 27: "threshold", 28: "images", 29: "threshold", 30: "banquet"}
PIC_INFO = {
    "threshold": ("memory_arts_notes_threshold.jpg", "An engraved view into an empty grand house at dawn, with small gold markers along the doorway, a window, a hearth and a table."),
    "images": ("memory_arts_notes_images.jpg", "An engraving of a grand room full of strange, vivid pictures: a cat attacking a soldier, a burning lute, a monkey on a cabinet, a loaf of bread with a sleeping face."),
    "banquet": ("memory_arts_notes_banquet.jpg", "An engraving of a banquet hall just after the roof has fallen in, with small gold stars marking where each guest sat."),
    "wheel": ("memory_arts_notes_wheel.jpg", "An engraving of three huge turning wheels covered in small pictures, between statues and globes."),
    "allegory": ("memory_arts_notes_allegory.jpg", "An engraving of seven women in a columned hall, each holding a symbol such as a book, scales, compasses, a counting frame, a lute and a globe."),
}


def lesson_page(d, hub, lessons):
    titles = {x["num"]: x["title"] for x in lessons}
    w = wing_of(d["num"], hub)
    prev = next((x for x in lessons if x["num"] == d["num"] - 1), None)
    nxt = next((x for x in lessons if x["num"] == d["num"] + 1), None)
    strip = [f'<a href="{HUB}">The whole course</a>']
    if prev: strip.insert(0, f'<a href="{fname(prev)}">&larr; {prev["title"]}</a>')
    if nxt: strip.append(f'<a href="{fname(nxt)}">{nxt["title"]} &rarr;</a>')
    nav = '<div class="nav-end">' + (f'<a href="{fname(prev)}">&larr; {prev["title"]}</a>' if prev else f'<a href="{HUB}">&larr; The course</a>') + f'<a href="{HUB}">All 30 lessons</a>' + (f'<a href="{fname(nxt)}">{nxt["title"]} &rarr;</a>' if nxt else f'<a href="{HUB}">Back to the course</a>') + "</div>"
    tabs = "".join(f'<button class="tab-btn{" active" if i == 0 else ""}" role="tab" onclick="showTab({i})">{n}</button>' for i, n in enumerate(TABS))
    panels = [story_tab(d, titles), method_tab(d), try_tab(d), drill_tab(d, titles), back_tab(d, titles, prev, nxt)]
    pages = "".join(f'<div class="tab-content{" active" if i == 0 else ""}" id="tab{i}"><section class="page">{p}</section></div>' for i, p in enumerate(panels))
    src, alt = PIC_INFO[PICS[d["num"]]]
    strip_html = " &nbsp;\u00b7&nbsp; ".join(strip)
    desc = E(d["tagline"], quote=True)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<meta name="description" content="{desc}">
<title>{E(d["title"])} \u00b7 {SERIES} \u00b7 Lesson {d["num"]}</title>
<style>
{CSS}</style>
</head>
<body data-lesson="{d["num"]:02d}">
<div class="container">
  <header>
    <span class="tag">THE ART OF MEMORY \u00b7 LESSON {d["num"]} OF 30 \u00b7 PART {w["roman"]}: {w["name"].upper()}</span>
    <h1>{d["title"]}</h1>
    <p>{d["tagline"]}</p>
  </header>
  <figure class="scene"><img src="{src}" alt="{E(alt)}" onerror="this.closest('figure').style.display='none'"></figure>
  <p class="series-strip">{strip_html}</p>
  <nav class="tab-nav" role="tablist">{tabs}</nav>
{pages}
  {nav}
  <footer>The Art of Memory \u00b7 Lesson {d["num"]} \u00b7 {d["title"]}</footer>
</div>
<script>
{JS}</script>
</body>
</html>
'''


# ---------------------------------------------------------------- hub
HUB_CSS = """
.intro, .how, .side { background:#fff; border:1px solid var(--line); border-radius:6px; box-shadow:0 6px 22px var(--shadow); padding:22px 26px; margin-bottom:26px; }
.intro p { margin-bottom:12px; color:#2d2d2d; } .intro p:last-child { margin-bottom:0; }
.section-label { font-size:.82rem; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); font-weight:800; margin:10px 0 12px 2px; }
.how h2, .side h3 { font-size:1.2rem; margin-bottom:8px; color:var(--ink); border:0; }
.how-steps { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; }
.how-step .n { font-weight:800; color:var(--gold); margin-bottom:2px; } .how-step p { font-size:.92rem; color:#2d2d2d; margin:0; }
.part { margin:0 0 26px; }
.part h2 { font-size:1.5rem; color:var(--ink); margin:0 0 2px; }
.part .blurb { color:var(--muted); margin:0 0 12px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr)); gap:14px; }
.lcard { position:relative; display:block; text-decoration:none; color:inherit; background:#fff; border:1px solid var(--line); border-radius:6px; box-shadow:0 6px 22px var(--shadow); padding:14px 18px 12px 62px; overflow:hidden; transition:transform .15s, box-shadow .15s; }
.lcard:hover { transform:translate(-2px,-2px); box-shadow:0 10px 26px rgba(22,38,61,.22); }
.lcard .thumb { display:block; width:calc(100% + 80px); margin:-14px -18px 10px -62px; height:120px; object-fit:cover; border-radius:5px 5px 0 0; }
.lcard .num { position:absolute; left:14px; top:134px; width:36px; height:36px; line-height:36px; text-align:center; border-radius:50%; background:var(--gold); color:#fff; font-weight:800; }
.lcard .t { display:block; font-weight:800; color:var(--ink); font-size:1.08rem; line-height:1.2; margin-bottom:2px; }
.lcard .e { display:block; font-size:.9rem; color:#33405a; }
.lcard.done::after { content:"\\2713 done"; position:absolute; right:10px; top:8px; font-size:.78rem; color:#2f7a36; font-weight:800; }
.cta { text-align:center; margin:18px 0 0; }
.cta a { display:inline-block; font-weight:800; text-decoration:none; color:#fff; background:var(--gold); padding:10px 28px; border-radius:4px; border:2px solid #fff; }
.cta a:hover { background:#fff; color:var(--gold); border-color:var(--gold); }
.side ul { margin:0 0 6px 20px; } .side li { margin-bottom:3px; }
.progress { text-align:center; color:var(--muted); margin:0 0 12px; min-height:1.4rem; font-weight:600; }
.gallery { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin:0 0 22px; }
.gallery figure { margin:0; } .gallery img { display:block; width:100%; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--line); box-shadow:0 6px 22px var(--shadow); }
.gallery figcaption { font-size:.82rem; color:var(--muted); text-align:center; margin-top:4px; font-style:italic; }
.stripmap { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin:0 0 26px; }
.stripmap a { text-decoration:none; background:#fff; border:2px solid var(--ink); color:var(--ink); border-radius:4px; padding:4px 14px; font-weight:700; font-size:.9rem; }
.stripmap a:hover { background:var(--ink); color:#fff; }
"""


def hub_page(hub, lessons):
    parts = []
    for w in hub["wings"]:
        cards = []
        for num in w["rooms"]:
            d = next(l for l in lessons if l["num"] == num)
            cards.append(f'<a class="lcard" href="{fname(d)}" data-room="{num:02d}"><img class="thumb" src="{PIC_INFO[PICS[num]][0]}" alt="" loading="lazy" onerror="this.style.display=\'none\'"><span class="num">{num}</span><span class="t">{d["title"]}</span><span class="e">{hub["short"][str(num)]}</span></a>')
        parts.append(f'<section class="part" id="part{w["roman"]}"><div class="section-label">Part {w["roman"]}</div><h2>{w["name"]}</h2><p class="blurb">{w["blurb"]}</p><div class="grid">' + "".join(cards) + "</div></section>")
    jump = "".join(f'<a href="#part{w["roman"]}">{w["roman"]} \u00b7 {w["name"]}</a>' for w in hub["wings"])
    how = "".join(f'<div class="how-step"><div class="n">{n}</div><p>{x}</p></div>' for n, x in hub["how"])
    side = "".join(f'<div class="side"><h3>{x["h"]}</h3>{x["x"]}</div>' for x in hub["sidebars"])
    first = fname(next(l for l in lessons if l["num"] == 1))
    caps = {"threshold": "The threshold", "images": "Pictures that stick", "banquet": "The banquet hall", "wheel": "The wheel of images", "allegory": "Ideas with faces"}
    gallery = "".join(f'<figure><img src="{PIC_INFO[k][0]}" alt="{E(PIC_INFO[k][1])}" loading="lazy"><figcaption>{caps[k]}</figcaption></figure>' for k in ["threshold", "images", "banquet", "wheel", "allegory"])
    src, alt = PIC_INFO["threshold"]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<meta name="description" content="{E(hub["tagline"], quote=True)}">
<title>The Art of Memory \u00b7 30 Lessons</title>
<style>
{CSS}{HUB_CSS}</style>
</head>
<body>
<div class="container">
  <header>
    <span class="tag">A course \u00b7 30 lessons \u00b7 B2 English</span>
    <h1>The Art of Memory</h1>
    <p>{hub["tagline"]}</p>
    <div class="cta"><a href="{first}">Start with lesson 1 &rarr;</a></div>
  </header>
  <figure class="scene"><img src="{src}" alt="{E(alt)}" onerror="this.closest('figure').style.display='none'"></figure>
  <div class="gallery">{gallery}</div>
  <div class="progress" id="progress"></div>
  <div class="intro">{"".join(f"<p>{p}</p>" for p in hub["intro"])}</div>
  <div class="stripmap">{jump}</div>
  <p class="section-label">How every lesson works</p>
  <div class="how"><div class="how-steps">{how}</div></div>
{"".join(parts)}
{side}
  <footer>The Art of Memory \u00b7 30 lessons</footer>
</div>
<script>
{JS}
(function(){{ try {{ var n = document.querySelectorAll('.lcard.done').length, p = document.getElementById('progress'); if (n && p) p.textContent = 'You have finished ' + n + ' of 30 lessons.'; }} catch(e) {{}} }})();
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
