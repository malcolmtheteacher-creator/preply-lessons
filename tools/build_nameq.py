#!/usr/bin/env python3
"""Build the Name the Question pages from tools/nameq_content/pathway.json:
  name_the_question_dashboard.html (the map), nq_<kind>.html (six branch pages), nq_quick_test.html.

Run from anywhere:  python3 tools/build_nameq.py
Refuses to build if a linked lesson file is missing, a quiz answer is out of
range, or the same quiz answer appears three times in a row.
"""
import html
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, "nameq_content", "pathway.json")
OUT = os.path.join(ROOT, "name_the_question_dashboard.html")
GENERATED = set()  # filled in main(): the pages this builder writes

W, H = 1800, 1080
HUB = (900, 470)
HUB_R = 138
BR_R = 80
LEAF_W, LEAF_H, LEAF_GAP = 250, 64, 74
LEAF_OFFSET = 140  # hub centre to the near edge of the leaf column


def esc(s):
    return html.escape(s, quote=True)


def check(d):
    problems = []
    hrefs = [l["href"] for b in d["branches"] for l in b["leaves"]]
    hrefs += [x["href"] for x in d["delivery"]]
    hrefs += [x["href"] for x in d["medicine"]["items"]]
    hrefs += [x["href"] for x in d["further"]]
    hrefs += [b["lesson"]["href"] for b in d["branches"]] + [l["href"] for l in d["lessons"]]
    for h in sorted(set(hrefs)):
        h = h.split("#")[0]
        if h in GENERATED:
            continue
        if not os.path.exists(os.path.join(ROOT, h)):
            problems.append("missing file: " + h)
    for b in d["branches"]:
        for k in ("lens", "leads", "example", "map_out", "talk", "page"):
            if not b.get(k):
                problems.append("branch %s has no %s" % (b["id"], k))
        if len(b.get("map_out", [])) != 2:
            problems.append("branch %s: map_out needs exactly two short lines" % b["id"])
        if any(len(x) > 22 for x in b.get("map_out", [])):
            problems.append("branch %s: map_out line too long for the circle (max 22)" % b["id"])
    items = d["quiz"]["items"]
    n = len(d["quiz"]["options"])
    for i, it in enumerate(items):
        if not 0 <= it["a"] < n:
            problems.append("quiz item %d: answer out of range" % (i + 1))
    for i in range(2, len(items)):
        if items[i]["a"] == items[i - 1]["a"] == items[i - 2]["a"]:
            problems.append("quiz: same answer three times in a row at item %d" % (i + 1))
    return problems


# ---------- icons (drawn around 0,0, roughly 34px square) ----------
def icon(kind, c):
    s = 'fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"' % c
    if kind == "fork":
        return '<g %s><path d="M0 16 V2 M0 2 L-12 -10 M0 2 L12 -10 M-12 -10 l-1 7 M-12 -10 l7 1 M12 -10 l1 7 M12 -10 l-7 1"/></g>' % s
    if kind == "pair":
        return '<g %s><rect x="-17" y="-10" width="13" height="20" rx="3"/><rect x="4" y="-10" width="13" height="20" rx="3"/><path d="M7 0 l3 4 l6 -8"/></g>' % s
    if kind == "bars":
        return '<g %s><path d="M-15 -9 H15 M-15 0 H6 M-15 9 H-4"/></g>' % s
    if kind == "umbrella":
        return '<g %s><path d="M-16 2 A16 14 0 0 1 16 2 Z M0 2 V13 q0 4 -5 4"/></g>' % s
    if kind == "magnifier":
        return '<g %s><circle cx="-3" cy="-3" r="10"/><path d="M5 5 L15 15"/></g>' % s
    if kind == "scales":
        return '<g %s><path d="M0 -14 V14 M-8 14 H8 M-14 -8 H14 M-14 -8 l-5 12 h10 z M14 -8 l-5 12 h10 z"/></g>' % s
    return ""


def wrap_name(name, limit=24):
    return name if len(name) <= limit else name[: limit - 1] + "…"


def leaf_svg(x, y, leaf, color, tint):
    tool = leaf["kind"] == "tool"
    fill = "#ffffff" if tool else tint
    tag = "TOOL" if tool else "CASE"
    return (
        '<a class="leaf" href="%s" aria-label="%s — %s">'
        '<rect class="pill" x="%d" y="%d" width="%d" height="%d" rx="28" fill="%s" stroke="%s" stroke-width="2.6"/>'
        '<text x="%d" y="%d" class="tag" fill="%s">%s</text>'
        '<text x="%d" y="%d" class="nm">%s</text>'
        '<text x="%d" y="%d" class="ds">%s</text></a>'
        % (esc(leaf["href"]), esc(leaf["name"]), esc(leaf["desc"]),
           x, y, LEAF_W, LEAF_H, fill, color,
           x + 22, y + 16, color, tag,
           x + 22, y + 37, esc(wrap_name(leaf["name"])),
           x + 22, y + 55, esc(leaf["desc"]))
    )


def unit(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    d = math.hypot(dx, dy) or 1
    return dx / d, dy / d


def build_map(d):
    cx, cy = HUB
    back, front = [], []
    for i, b in enumerate(d["branches"]):
        bx, by, col, tint = b["x"], b["y"], b["color"], b["tint"]
        ux, uy = unit(cx, cy, bx, by)
        sx, sy = cx + ux * (HUB_R - 6), cy + uy * (HUB_R - 6)
        ex, ey = bx - ux * (BR_R - 6), by - uy * (BR_R - 6)
        length = math.hypot(ex - sx, ey - sy)
        off = 46 if i % 2 == 0 else -46
        px, py = -uy, ux
        c1 = (sx + ux * length * 0.33 + px * off, sy + uy * length * 0.33 + py * off)
        c2 = (ex - ux * length * 0.33 + px * off, ey - uy * length * 0.33 + py * off)
        back.append(
            '<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" stroke-width="20" '
            'fill="none" stroke-linecap="round" opacity=".92"/>'
            % (sx, sy, c1[0], c1[1], c2[0], c2[1], ex, ey, col)
        )
        # leaves
        n = len(b["leaves"])
        side = 1 if b["side"] == "r" else -1
        lx = bx + LEAF_OFFSET if side == 1 else bx - LEAF_OFFSET - LEAF_W
        for j, leaf in enumerate(b["leaves"]):
            ly_c = by + (j - (n - 1) / 2) * LEAF_GAP
            ly = ly_c - LEAF_H / 2
            tx = lx if side == 1 else lx + LEAF_W
            ux2, uy2 = unit(bx, by, tx, ly_c)
            s2x, s2y = bx + ux2 * (BR_R - 4), by + uy2 * (BR_R - 4)
            dx = tx - s2x
            back.append(
                '<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" stroke-width="6.5" '
                'fill="none" stroke-linecap="round" opacity=".85"/>'
                % (s2x, s2y, s2x + dx * 0.55, s2y, tx - dx * 0.45, ly_c, tx, ly_c, col)
            )
            front.append(leaf_svg(int(lx), int(ly), leaf, col, tint))
        # branch hub
        front.append(
            '<a class="hubbtn" href="%s" aria-label="%s — %s">'
            '<circle cx="%d" cy="%d" r="%d" fill="url(#g-%s)" stroke="%s" stroke-width="5.5"/>'
            '<g transform="translate(%d %d)">%s</g>'
            '<text x="%d" y="%d" class="cue">%s</text>'
            '<text x="%d" y="%d" class="sub">%s</text><text x="%d" y="%d" class="sub">%s</text></a>'
            % (esc(b["page"]), esc(b["cue"]), esc(b["sub"]), bx, by, BR_R, b["id"], col,
               bx, by - 40, icon(b["icon"], col),
               bx, by + 6, esc(b["cue"]),
               bx, by + 30, esc(b["map_out"][0]), bx, by + 47, esc(b["map_out"][1]))
        )

    # delivery ribbon
    st_y = 988
    xs = [670, 900, 1130]
    rib = []
    rib.append(
        '<path d="M900 %d C900 760 670 790 670 %d" stroke="#c9a227" stroke-width="12" fill="none" '
        'stroke-linecap="round" stroke-dasharray="2 20" opacity=".95"/>' % (cy + HUB_R - 6, st_y - 38)
    )
    rib.append('<text x="900" y="918" class="script" text-anchor="middle">then say it</text>')
    for k in range(2):
        rib.append(
            '<path d="M%d %d H%d" stroke="#c9a227" stroke-width="5" stroke-linecap="round" '
            'marker-end="url(#arrow)"/>' % (xs[k] + 112, st_y, xs[k + 1] - 118)
        )
    for k, st in enumerate(d["delivery"]):
        x = xs[k] - 110
        rib.append(
            '<a class="leaf" href="%s" aria-label="%s — %s">'
            '<rect class="pill" x="%d" y="%d" width="220" height="64" rx="32" fill="#fff8e1" stroke="#c9a227" stroke-width="3"/>'
            '<circle cx="%d" cy="%d" r="15" fill="#c9a227"/><text x="%d" y="%d" class="num">%d</text>'
            '<text x="%d" y="%d" class="nm">%s</text><text x="%d" y="%d" class="ds">%s</text></a>'
            % (esc(st["href"]), esc(st["name"]), esc(st["desc"]),
               x, st_y - 32, x + 30, st_y, x + 30, st_y + 5, k + 1,
               x + 56, st_y - 2, esc(st["name"]), x + 56, st_y + 17, esc(st["desc"]))
        )

    # centre hub
    hub = (
        '<g class="centre"><circle cx="%d" cy="%d" r="%d" fill="url(#g-hub)" stroke="#0b5f5a" stroke-width="7"/>'
        '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#0b5f5a" stroke-width="1.6" stroke-dasharray="3 9" opacity=".6"/>'
        '<g transform="translate(%d %d) scale(1.15)" fill="none" stroke="#0b5f5a" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M-22 -6 a22 18 0 1 1 22 17 l-12 8 l2 -9 a22 18 0 0 1 -12 -16z"/>'
        '<path d="M-3 -12 q3 -6 9 -3 q4 4 -3 8 q-3 2 -3 5" /><circle cx="0" cy="12" r="1.2" fill="#0b5f5a"/></g>'
        '<text x="%d" y="%d" class="hub1">Name the</text><text x="%d" y="%d" class="hub1">Question</text>'
        '<text x="%d" y="%d" class="hub2">Hear it. Name it.</text><text x="%d" y="%d" class="hub2">Think it. Say it.</text></g>'
        % (cx, cy, HUB_R, cx, cy, HUB_R - 14,
           cx, cy - 78,
           cx, cy - 6, cx, cy + 36,
           cx, cy + 74, cx, cy + 96)
    )

    grads = "".join(
        '<radialGradient id="g-%s" cx="50%%" cy="38%%" r="70%%"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset="1" stop-color="%s"/></radialGradient>' % (b["id"], b["tint"])
        for b in d["branches"]
    )
    defs = (
        '<defs>%s<radialGradient id="g-hub" cx="50%%" cy="35%%" r="75%%"><stop offset="0" stop-color="#f0fbf9"/>'
        '<stop offset="1" stop-color="#b9e4de"/></radialGradient>'
        '<radialGradient id="paper" cx="50%%" cy="45%%" r="75%%"><stop offset="0" stop-color="#fffaf0"/>'
        '<stop offset="1" stop-color="#f3e9d2"/></radialGradient>'
        '<filter id="rough" x="-5%%" y="-5%%" width="110%%" height="110%%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        '<path d="M1 1 L9 5 L1 9" fill="none" stroke="#c9a227" stroke-width="2.2" stroke-linecap="round"/></marker></defs>'
        % grads
    )
    sprigs = (
        '<g fill="none" stroke="#7aa56a" stroke-width="2.4" stroke-linecap="round" opacity=".7">'
        '<path d="M70 1030 q14 -34 6 -66 M76 1000 q-18 -4 -24 -22 M78 984 q16 -2 22 -18"/>'
        '<path d="M1730 1030 q-14 -34 -6 -66 M1724 1000 q18 -4 24 -22 M1722 984 q-16 -2 -22 -18"/></g>'
        '<text x="150" y="1040" class="script" opacity=".75">Different questions. Clearer answers.</text>'
    )
    return (
        '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-label="Mind map of six kinds of question, with tools and cases for each">%s'
        '<rect width="%d" height="%d" fill="url(#paper)"/>%s'
        '<g filter="url(#rough)">%s</g>%s%s%s</svg>'
        % (W, H, defs, W, H, sprigs, "".join(back), hub, "".join(front), "".join(rib))
    )


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;background:#f7fbfa;color:#2a2a3a;line-height:1.6}
.container{max-width:1120px;margin:0 auto;padding:20px}
header{position:relative;color:#fff;text-align:center;margin-bottom:26px;border-radius:14px;overflow:hidden;
 box-shadow:0 10px 30px rgba(14,116,144,.22);padding:54px 30px 48px;
 background:radial-gradient(ellipse at 20% 0%,#1d8a82 0%,transparent 55%),radial-gradient(ellipse at 85% 100%,#3f6fcf 0%,transparent 55%),linear-gradient(135deg,#0b4f55,#123a63)}
header .tag{display:inline-block;padding:5px 15px;background:rgba(255,255,255,.18);border-radius:14px;font-size:.78rem;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px}
header h1{font-size:2.8rem;line-height:1.12;margin-bottom:14px;letter-spacing:-.5px;font-family:Georgia,"Times New Roman",serif}
header .subtitle{font-size:1.15rem;max-width:720px;margin:0 auto;opacity:.97}
.intro{background:#fff;border:1px solid #e0e0ee;border-left:4px solid #0f766e;border-radius:12px;padding:24px 28px;margin-bottom:26px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.intro p{color:#3a3a4a;margin-bottom:12px}.intro p:last-child{margin-bottom:0}.intro strong{color:#115e59}
.section-label{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:#115e59;font-weight:700;margin:0 0 14px 4px}
.wide{width:min(1380px,calc(100vw - 24px));position:relative;left:50%;transform:translateX(-50%)}
.map{background:#fff;border:1px solid #cfe7e3;border-radius:14px;padding:12px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.map-scroll{overflow-x:auto}
.map-frame{min-width:820px}
.map-frame svg{display:block;width:100%;height:auto;border-radius:10px}
svg text{font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif}
svg .cue{font-family:Georgia,"Times New Roman",serif;font-weight:700;font-size:21px;text-anchor:middle;fill:#23233a}
svg .sub{font-size:14px;font-style:italic;text-anchor:middle;fill:#55556a}
svg .hub1{font-family:Georgia,"Times New Roman",serif;font-weight:700;font-size:44px;text-anchor:middle;fill:#0b4f55}
svg .hub2{font-family:Georgia,serif;font-style:italic;font-size:19px;text-anchor:middle;fill:#2f5f5c}
svg .nm{font-size:18px;font-weight:700;fill:#23233a}
svg .ds{font-size:14px;fill:#5a5a70}
svg .tag{font-size:10.5px;font-weight:700;letter-spacing:.14em}
svg .num{font-size:15px;font-weight:700;fill:#fff;text-anchor:middle}
svg .script{font-family:"Snell Roundhand","Brush Script MT","Segoe Script",cursive;font-size:30px;fill:#8a6d0b}
svg a{cursor:pointer;outline:none}
svg a.leaf .pill{transition:filter .15s,stroke-width .15s}
svg a.leaf:hover .pill,svg a.leaf:focus-visible .pill{stroke-width:4.4;filter:drop-shadow(0 3px 6px rgba(0,0,0,.18))}
svg a.hubbtn circle{transition:filter .15s}
svg a.hubbtn:hover circle,svg a.hubbtn:focus-visible circle{filter:brightness(1.05) drop-shadow(0 4px 8px rgba(0,0,0,.2))}
.legend{display:flex;gap:22px;flex-wrap:wrap;justify-content:center;font-size:.86rem;color:#55556a;margin:10px 0 28px}
.legend span{display:inline-flex;align-items:center;gap:8px}
.chip{display:inline-block;width:34px;height:16px;border-radius:9px;border:2px solid #0f766e}
.chip.tool{background:#fff}.chip.case{background:#d7f0ec}.chip.say{background:#fff8e1;border-color:#c9a227}
.how{background:#fff;border:1px solid #e0e0ee;border-radius:12px;padding:24px 28px;margin-bottom:30px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.how h2,.quiz h2,.med h2{color:#115e59;font-size:1.3rem;margin-bottom:14px}
.how-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
.how-step{padding:14px 16px;background:#f1f9f8;border-radius:10px}
.how-step .n{color:#0f766e;font-weight:700;font-size:.92rem;margin-bottom:4px}
.how-step p{font-size:.92rem;color:#3a3a4a}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px;margin-bottom:32px}
.card{background:#fff;border:1px solid #e0e0ee;border-radius:14px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.04);position:relative;overflow:hidden;scroll-margin-top:16px}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:6px;background:var(--c)}
.card:target{box-shadow:0 0 0 3px var(--c),0 12px 28px rgba(0,0,0,.12)}
.card .kick{font-size:.76rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--c);margin-bottom:4px}
.card h3{font-family:Georgia,serif;font-size:1.5rem;color:#23233a;margin-bottom:8px}
.card .asked{font-size:.97rem;color:#3a3a4a;margin-bottom:12px}
.card h4{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:#6a6a80;margin:12px 0 6px}
.card ol.lens{padding-left:0;list-style:none;counter-reset:l;font-size:.94rem}
.card ol.lens li{counter-increment:l;position:relative;padding:6px 0 6px 34px}
.card ol.lens li::before{content:counter(l);position:absolute;left:0;top:7px;width:24px;height:24px;border-radius:50%;background:var(--c);color:#fff;font-weight:700;font-size:.8rem;display:flex;align-items:center;justify-content:center}
.card ol.lens li b{color:#23233a;display:block}.card ol.lens li span{color:#55556a;font-size:.88rem}
.card ul.leads{list-style:none;font-size:.92rem}
.card ul.leads li{background:var(--t);border-left:4px solid var(--c);border-radius:8px;padding:8px 12px;margin:6px 0}
.card ul.leads li b{color:#23233a;display:block}.card ul.leads li span{color:#3a3a4a;font-size:.88rem}
details.ex{margin-top:12px;border:1px dashed var(--c);border-radius:10px;padding:8px 12px}
details.ex summary{cursor:pointer;font-weight:700;font-size:.9rem;color:#23233a}
details.ex .exq{font-family:Georgia,serif;font-size:1.02rem;margin:10px 0 4px;color:#23233a}
details.ex ol.run{padding-left:20px;font-size:.9rem;color:#3a3a4a}
details.ex .say{background:#f6f6fb;border-radius:8px;padding:10px 12px;margin-top:8px;font-size:.93rem;font-style:italic}
details.ex .say span{display:block;font-style:normal;font-weight:700;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--c);margin-bottom:2px}
details.ex .exnote{font-size:.86rem;color:#55556a;margin-top:8px}
.lensnote{font-size:.88rem;color:#55556a;margin:-4px 4px 16px}
.card .breaks{background:var(--t);border-radius:8px;padding:10px 14px;font-size:.9rem;margin-top:12px}
.card .breaks b{color:#23233a}
.card ul.links{list-style:none;margin-top:4px}
.card ul.links li{margin:4px 0;font-size:.92rem}
.card ul.links a{color:#115e59;text-decoration:none;border-bottom:1px solid #b9e4de}
.card ul.links a:hover{border-bottom-color:var(--c)}
.card ul.links .k{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.1em;color:var(--c);width:42px}
.quiz,.med{background:#fff;border:1px solid #e0e0ee;border-radius:12px;padding:24px 28px;margin-bottom:30px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.quiz .lead,.med .lead{margin-bottom:14px;color:#3a3a4a}
.qrow{display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:10px 0;border-top:1px solid #eef0f4}
.qrow:first-of-type{border-top:none}
.qrow .qn{font-weight:700;color:#0f766e;width:22px}
.qrow .qt{flex:1 1 320px}
.qrow select{font-size:.95rem;padding:7px 10px;border-radius:8px;border:1.5px solid #b9c4d4;background:#fff;min-width:150px}
.qrow.ok select{border-color:#2e8b57;background:#eaf7ef}.qrow.no select{border-color:#c0392b;background:#fdeceb}
.qwhy{flex-basis:100%;font-size:.9rem;color:#3a3a4a;background:#f1f9f8;border-radius:8px;padding:8px 12px;display:none}
.qwhy.on{display:block}
.btnrow{margin-top:14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.b{background:linear-gradient(135deg,#0e7490,#0f766e);color:#fff;border:0;border-radius:20px;padding:9px 20px;font-weight:600;font-size:.92rem;cursor:pointer}
.b.alt{background:#fff;color:#0f766e;border:1.5px solid #0f766e}
.score{font-weight:700;color:#115e59}
.med ul{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}
.med li a{display:block;padding:12px 14px;background:#f1f9f8;border-radius:10px;text-decoration:none;color:#115e59;font-weight:600;font-size:.94rem}
.med li a small{display:block;color:#6a6a80;font-weight:400}
.further{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-bottom:30px}
.further a{display:block;background:#fff;border:1px solid #e0e0ee;border-radius:12px;padding:16px 18px;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}
.further a:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(14,116,144,.15)}
.further b{display:block;color:#115e59;margin-bottom:2px}.further span{font-size:.88rem;color:#55556a}
footer{text-align:center;color:#888;font-size:.86rem;margin:24px 0 16px}

.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.intro .lede{font-size:1.1rem;color:#115e59;font-family:Georgia,serif}
header.slim{padding:20px 28px 22px;margin-bottom:14px}
header.slim .tag{margin-bottom:8px}
header.slim h1{font-size:2.2rem;margin-bottom:6px}
header.slim .subtitle{font-size:1rem;max-width:760px}
.lessons{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin-bottom:22px}
.lessons a{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #e0e0ee;border-left:6px solid var(--c);border-radius:12px;padding:12px 14px;text-decoration:none;color:#23233a;transition:transform .2s,box-shadow .2s}
.lessons a:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(14,116,144,.15)}
.lessons i{font-style:normal;font-weight:700;color:#fff;background:var(--c);border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;flex:none}
.lessons b{font-family:Georgia,serif;font-size:.98rem;line-height:1.25}
.lessoncta{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;background:var(--c);color:#fff;border-radius:14px;padding:16px 24px;margin-bottom:18px;text-decoration:none;box-shadow:0 6px 18px rgba(0,0,0,.12)}
.lessoncta i{display:block;font-style:normal;font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;opacity:.9}
.lessoncta b{font-family:Georgia,serif;font-size:1.3rem}
.lessoncta em{font-style:normal;background:#fff;color:#23233a;font-weight:700;padding:8px 18px;border-radius:18px}
.cta{text-align:center;margin:6px 0 30px}
.cta a.b{display:inline-block;text-decoration:none;font-size:1rem;padding:12px 26px}
.how-steps{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.kinds{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;align-items:center}
.kinds a{text-decoration:none;font-family:Georgia,serif;font-weight:700;font-size:.92rem;color:var(--c,#115e59);border:2px solid var(--c,#115e59);background:#fff;border-radius:18px;padding:5px 14px}
.kinds a.on,.kinds a:hover{background:var(--c,#115e59);color:#fff}
.kinds a.home{--c:#55556a;font-family:inherit;font-weight:600;margin-right:6px}
header.bh{padding:40px 30px 36px}
header.bh h1{font-size:3rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:30px}
@media(max-width:760px){.two{grid-template-columns:1fr}}
.card{margin-bottom:18px}
.card ol.talk{padding-left:22px;font-size:.98rem}.card ol.talk li{margin:8px 0}
.card ul.links.plain li{margin:7px 0}
.pn{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:6px 0 10px}
.pn a{text-decoration:none;color:#115e59;font-weight:600;border:1.5px solid #b9e4de;border-radius:18px;padding:7px 16px;background:#fff}
.pn a:hover{background:#f1f9f8}
@media(max-width:640px){header h1{font-size:2.1rem}.container{padding:12px}}
"""

JS = """
function check(){
 var rows=document.querySelectorAll('.qrow'),ok=0,answered=0;
 rows.forEach(function(r){
  var s=r.querySelector('select'),w=r.querySelector('.qwhy');
  r.classList.remove('ok','no');
  if(s.value===''){return;}
  answered++;
  if(s.value===r.dataset.a){r.classList.add('ok');ok++;}else{r.classList.add('no');}
 });
 document.getElementById('score').textContent=answered?('You named '+ok+' of '+rows.length+' correctly.'):'Choose an answer for each question first.';
}
function reveal(){
 document.querySelectorAll('.qwhy').forEach(function(w){w.classList.toggle('on');});
}
function resetQ(){
 document.querySelectorAll('.qrow').forEach(function(r){r.classList.remove('ok','no');r.querySelector('select').value='';});
 document.querySelectorAll('.qwhy').forEach(function(w){w.classList.remove('on');});
 document.getElementById('score').textContent='';
}
"""


def example_html(ex, label, open_=False):
    run = "".join("<li>%s</li>" % esc(r) for r in ex["run"])
    note = '<p class="exnote">%s</p>' % esc(ex["note"]) if ex.get("note") else ""
    return (
        '<details class="ex"%s><summary>%s</summary><p class="exq">%s</p>'
        '<ol class="run">%s</ol><p class="say"><span>How it might sound</span>%s</p>%s</details>'
        % (" open" if open_ else "", esc(label), esc(ex["q"]), run, esc(ex["say"]), note)
    )


def shell(d, title, head_html, body, series="Name the Question"):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="%s">
<title>%s</title>
<style>%s</style>
</head>
<body>
<div class="container">
%s
%s
<footer>%s</footer>
</div>
<script>%s</script>
</body>
</html>
""" % (esc(series), esc(title), CSS, head_html, body, esc(d["footer"]), JS)


def kinds_nav(d, current=None):
    chips = []
    for b in d["branches"]:
        cls = ' class="on"' if b["id"] == current else ""
        chips.append('<a%s href="%s" style="--c:%s">%s</a>' % (cls, esc(b["page"]), b["color"], esc(b["cue"])))
    return '<nav class="kinds"><a class="home" href="name_the_question_dashboard.html">\u2190 The map</a>%s</nav>' % "".join(chips)


def lessons_row(d):
    colors = {b["id"]: b["color"] for b in d["branches"]}
    colors["mixed"] = "#2f5f8a"
    return "".join('<a href="%s" style="--c:%s"><i>%d</i><b>%s</b></a>'
                   % (esc(l["href"]), colors[l["kind"]], l["num"], esc(l["title"])) for l in d["lessons"])


def dashboard(d):
    head = ('<header class="slim"><div class="tag">%s</div><h1>%s</h1><p class="subtitle">%s</p></header>'
            % (esc(d["tag"]), esc(d["title"]), esc(d["subtitle"])))
    steps = "".join('<div class="how-step"><div class="n">%s \u00b7 %s</div><p>%s</p></div>'
                    % (s["n"], esc(s["t"]), esc(s["d"])) for s in d["steps"])
    body = (
        '<div class="wide"><div class="map"><div class="map-scroll"><div class="map-frame">%s</div></div></div></div>'
        '<div class="legend"><span><i class="chip tool"></i> a thinking tool</span>'
        '<span><i class="chip case"></i> a real case to practise on</span>'
        '<span><i class="chip say"></i> a lesson on saying it</span>'
        '<span>Click a circle to open that kind of question</span></div>'
        '<div class="intro">%s</div>'
        '<section class="how"><div class="how-steps">%s</div></section>'
        '<div class="section-label">%s</div><div class="lessons">%s</div>'
        '<div class="cta"><a class="b" href="%s">Take the quick test: which kind of question is it? \u2192</a></div>'
        '<div class="section-label">Go further</div><div class="further">%s</div>'
        % (build_map(d), "".join("<p>%s</p>" % p for p in d["intro"]), steps, esc(d["lessons_heading"]), lessons_row(d), esc(d["quiz"]["page"]),
           "".join('<a href="%s"><b>%s</b><span>%s</span></a>' % (esc(f["href"]), esc(f["name"]), esc(f["desc"]))
                   for f in d["further"]))
    )
    return shell(d, d["title"] + " \u00b7 C1", head, body)


def prac_list(leaves, kind):
    rows = "".join('<li><a href="%s">%s</a> <span style="color:#6a6a80">\u2014 %s</span></li>'
                   % (esc(l["href"]), esc(l["name"]), esc(l["desc"])) for l in leaves if l["kind"] == kind)
    return rows


def branch_page(d, b, idx):
    n = len(d["branches"])
    prev_b, next_b = d["branches"][(idx - 1) % n], d["branches"][(idx + 1) % n]
    style = "--c:%s;--t:%s" % (b["color"], b["tint"])
    head = (
        '<header class="bh" style="%s;background:linear-gradient(135deg,%s,#123a63)">'
        '<div class="tag">%s</div><h1>%s</h1><p class="subtitle">%s</p></header>'
        % (style, b["color"], esc(b["kicker"]), esc(b["cue"]), esc(b["asked"]))
    )
    lens = "".join('<li><b>%s</b> <span>%s</span></li>' % (esc(x["q"]), esc(x["g"])) for x in b["lens"])
    leads = "".join('<li><b>%s</b> <span>%s</span></li>' % (esc(x["w"]), esc(x["d"])) for x in b["leads"])
    exs = example_html(b["example"], "A worked example", True)
    if b.get("contrast"):
        exs += example_html(b["contrast"], "Same words, opposite answer", True)
    tools, cases = prac_list(b["leaves"], "tool"), prac_list(b["leaves"], "case")
    prac = ""
    if tools:
        prac += '<div><h4>Thinking tools</h4><ul class="links plain">%s</ul></div>' % tools
    if cases:
        prac += '<div><h4>Real cases</h4><ul class="links plain">%s</ul></div>' % cases
    talk = "".join("<li>%s</li>" % esc(t) for t in b["talk"])
    say = "".join('<a href="%s"><b>%s</b><span>%s</span></a>' % (esc(x["href"]), esc(x["name"]), esc(x["desc"]))
                  for x in d["delivery"])
    med = ""
    if b["id"] == "right":
        m = d["medicine"]
        med = ('<section class="med" id="medicine"><h2>%s</h2><p class="lead">%s</p><ul>%s</ul></section>'
               % (esc(m["heading"]), esc(m["lead"]),
                  "".join('<li><a href="%s">%s<small>%s</small></a></li>' % (esc(i["href"]), esc(i["name"]), esc(i["level"]))
                          for i in m["items"])))
    body = (
        kinds_nav(d, b["id"]) +
        '<a class="lessoncta" href="%s" style="--c:%s"><span><i>The lesson \u00b7 50 minutes \u00b7 C1</i><b>%s</b></span><em>Open the lesson \u2192</em></a>'
        % (esc(b["lesson"]["href"]), b["color"], esc(b["lesson"]["title"])) +
        '<section class="card" style="%s"><div class="two"><div><h4>The lens</h4><ol class="lens">%s</ol></div>'
        '<div><h4>It can lead to</h4><ul class="leads">%s</ul></div></div></section>' % (style, lens, leads) +
        '<section class="card" style="%s"><h4>The thinking, step by step</h4>%s'
        '<div class="breaks"><b>Where it breaks.</b> %s</div></section>' % (style, exs, esc(b["breaks"])) +
        '<section class="card" style="%s"><h4>Practise it</h4><div class="two">%s</div></section>' % (style, prac) +
        '<section class="card" style="%s"><h4>Talk it through</h4><ol class="talk">%s</ol></section>' % (style, talk) +
        med +
        '<div class="section-label">Then say it</div><div class="further">%s</div>' % say +
        '<nav class="pn"><a href="%s">\u2190 %s</a><a href="name_the_question_dashboard.html">The map</a><a href="%s">%s \u2192</a></nav>'
        % (esc(prev_b["page"]), esc(prev_b["cue"]), esc(next_b["page"]), esc(next_b["cue"]))
    )
    return shell(d, "%s \u00b7 Name the Question \u00b7 C1" % b["cue"], head, body)


def quiz_page(d):
    q = d["quiz"]
    by_cue = {b["cue"]: b for b in d["branches"]}
    opts = '<option value="">choose\u2026</option>' + "".join(
        '<option value="%d">%s</option>' % (i, esc(o)) for i, o in enumerate(q["options"]))
    rows = []
    for i, it in enumerate(q["items"]):
        b = by_cue[q["options"][it["a"]]]
        rows.append(
            '<div class="qrow" data-a="%d"><span class="qn">%d</span><span class="qt">%s</span>'
            '<select aria-label="Question %d">%s</select><div class="qwhy"><b>%s.</b> %s '
            '<a href="%s">Open this kind \u2192</a></div></div>'
            % (it["a"], i + 1, esc(it["q"]), i + 1, opts, esc(q["options"][it["a"]]), esc(it["why"]), esc(b["page"])))
    head = ('<header><div class="tag">%s</div><h1>%s</h1><p class="subtitle">%s</p></header>'
            % (esc(d["tag"]), esc(q["heading"]), esc(q["lead"])))
    body = (
        kinds_nav(d) +
        '<section class="quiz">%s<div class="btnrow"><button class="b" onclick="check()">Check my answers</button>'
        '<button class="b alt" onclick="reveal()">Show the reasons</button>'
        '<button class="b alt" onclick="resetQ()">Start again</button><span class="score" id="score"></span></div></section>'
        % "".join(rows)
    )
    return shell(d, "Which kind of question is it? \u00b7 Name the Question \u00b7 C1", head, body)


def main():
    with open(DATA, encoding="utf8") as f:
        d = json.load(f)
    GENERATED.update([b["page"] for b in d["branches"]] + [d["quiz"]["page"]])
    problems = check(d)
    if problems:
        print("NOT BUILT:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    outputs = {OUT: dashboard(d), os.path.join(ROOT, d["quiz"]["page"]): quiz_page(d)}
    for i, b in enumerate(d["branches"]):
        outputs[os.path.join(ROOT, b["page"])] = branch_page(d, b, i)
    for path, text in outputs.items():
        with open(path, "w", encoding="utf8") as f:
            f.write(text)
        print("built", os.path.relpath(path, ROOT), "(%d bytes)" % os.path.getsize(path))


if __name__ == "__main__":
    main()
