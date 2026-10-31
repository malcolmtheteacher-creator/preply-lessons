#!/usr/bin/env python3
"""Build world.html: one zoomable painted map of the whole site (routes, goals, pathways, interests,
guides, palace, library of every lesson). Layout is computed here; the page only draws it.
Usage: python3 tools/build_world.py"""
import glob, json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = "https://malcolmhyndman.com/"
nodes = []          # every card on the map
edges = []          # [x1, y1, x2, y2, colour, width]
libs = []           # library blocks (lessons drawn lazily by the page)


def add(id, title, x, y, w, h, kind, col, img="", href="", sub="", parent=None, lod=0, ext=False):
    n = dict(id=id, t=title, s=sub, x=round(x), y=round(y), w=w, h=h, k=kind, c=col, i=img, h_=href, p=parent, l=lod, e=ext)
    nodes.append(n)
    return n


def link(a, b, col, wd):
    edges.append([a["x"], a["y"], b["x"], b["y"], col, wd, a["id"], b["id"]])


def exists(p):
    return os.path.exists(os.path.join(ROOT, p))


def pic(p):
    return p if exists(p) else ""


COL = {"pro": "#2f6f8f", "aca": "#a8552f", "gen": "#3f7d5a", "exp": "#7a4b8f", "com": "#b04a3a", "pal": "#b08a2a", "wr": "#3f5f9a", "lib": "#1f3a30"}

# ---------- hub ----------
hub = add("hub", "English, taught through stories", 0, 0, 1100, 620, "hub", "#1f3a30", HOME + "hero_study.jpg",
          "index.html", "Malcolm Hyndman · 3,400+ free lessons · A1 to C2", None, 0, False)
book = add("book", "Book a lesson", 900, 640, 420, 170, "leaf", "#d4a437", HOME + "headshot.png", "https://preply.com/en/tutor/4383857",
           "With Malcolm on Preply", "hub", 0, True)
link(hub, book, "#d4a437", 6)


def region(id, title, sub, x, y, col, img, href, lod=0):
    r = add(id, title, x, y, 760, 430, "region", col, img, href, sub, "hub", lod, False)
    link(hub, r, col, 14)
    return r


# ---------- the three routes ----------
def route_data(r):
    s = open(os.path.join(ROOT, "journey_%s.html" % r), encoding="utf-8").read()
    return json.loads(re.search(r"var R=(\{.*?\});\n", s, re.S).group(1))


def route_block(r, side, ytop, col, title, sub):
    """side: -1 grows left, +1 grows right. Returns the next free y below the block."""
    R = route_data(r)
    goals = R["goals"]
    by = {g[0]: [] for g in goals}
    for c in R["cards"]:
        by.setdefault(c["goal"], []).append(c)
    gx = side * 3600 + side * 700          # goal column
    lx = gx + side * 470                   # pathway column
    y = ytop
    centres = []
    for gi, g in enumerate(goals):
        cs = by.get(g[0], [])
        hgt = max(240, len(cs) * 205)
        cy = y + hgt / 2
        gimg = "journey/routes/route_%s_%s.jpg" % (r, g[0])
        gn = add("%s_g%d" % (r, gi), g[1], gx, cy, 400, 230, "goal", col, pic(gimg), "%s.html?goal=%s" % ("journey_" + r, g[0]), g[2], r, 1, False)
        centres.append(gn)
        for ci, c in enumerate(cs):
            py = y + 102 + ci * 205
            cn = add("%s_c%d_%d" % (r, gi, ci), c["name"], lx, py, 320, 180, "path", col, pic(gimg), c["href"], c["level"] + (" · " + c["meta"] if c["meta"] else ""), "%s_g%d" % (r, gi), 2, True)
            link(gn, cn, col, 4)
        y += hgt + 50
    cy = (ytop + y) / 2
    rn = region(r, title, sub, side * 3600, cy, col, pic("journey/routes/route_%s_hero.jpg" % r), "journey_%s.html" % r)
    for gn in centres:
        link(rn, gn, col, 8)
    return y


y = -3400
y = route_block("professional", -1, y, COL["pro"], "Professional English", "Meetings, presenting, negotiating, interviews")
y_left = y + 120
route_block("general", 1, -3400, COL["gen"], "General English", "From first steps to mastery")
# academic grows upward
R = route_data("academic")
goals = R["goals"]
by = {g[0]: [] for g in goals}
for c in R["cards"]:
    by.setdefault(c["goal"], []).append(c)
x = -sum(max(420, 2 * 340) for _ in goals) / 2
for gi, g in enumerate(goals):
    cs = by.get(g[0], [])
    gx = x + 340
    gimg = "journey/routes/route_academic_%s.jpg" % g[0]
    gn = add("aca_g%d" % gi, g[1], gx, -2300, 400, 230, "goal", COL["aca"], pic(gimg), "journey_academic.html?goal=" + g[0], g[2], "academic", 1, False)
    for ci, c in enumerate(cs):
        cx = gx - 170 + (ci % 2) * 340
        cy = -2300 - 300 - (ci // 2) * 205
        cn = add("aca_c%d_%d" % (gi, ci), c["name"], cx, cy, 320, 180, "path", COL["aca"], pic(gimg), c["href"], c["level"] + (" · " + c["meta"] if c["meta"] else ""), "aca_g%d" % gi, 2, True)
        link(gn, cn, COL["aca"], 4)
    gnodes = gn
    x += 2 * 340 + 80
    nodes_aca = gnodes
acar = region("academic", "Academic English & exams", "IELTS, Cambridge, the language of scholarship", 0, -1600, COL["aca"], pic("journey/routes/route_academic_hero.jpg"), "journey_academic.html")
for n in [n for n in nodes if n["id"].startswith("aca_g")]:
    link(acar, n, COL["aca"], 8)

# ---------- explore by interest ----------
T = re.search(r"var T=(\{.*?\});", open(os.path.join(ROOT, "explore.html"), encoding="utf-8").read(), re.S).group(1)
T = json.loads(re.sub(r"([{,])([A-Z]{3}):", r'\1"\2":', T.replace("'", '"')))
ex_y = y_left
rows = math.ceil(len(T) / 2)
exr = region("explore", "Explore by interest", "Questions that make you curious, 18 worlds", -3600, ex_y + rows * 205 / 2, COL["exp"], pic("explore_img/IDE.jpg"), "explore.html")
for i, (code, (name, colr)) in enumerate(T.items()):
    cx = -4300 - (i % 2) * 340
    cy = ex_y + 102 + (i // 2) * 205
    cn = add("ex_" + code, name, cx, cy, 320, 180, "topic", colr, pic("explore_img/%s.jpg" % code), "explore.html?topic=" + code, "", "explore", 1, False)
    link(exr, cn, colr, 4)
y_left = ex_y + rows * 205 + 120

# ---------- the palace ----------
pal = [("dewey_palace_architecture.html", "The Palace", "Where every subject has a room")]
names = {"000": "Computer science & information", "100": "Philosophy & psychology", "200": "Religion", "300": "Social sciences", "400": "Language", "500": "Science", "600": "Technology", "700": "Arts", "800": "Literature", "900": "History"}
for f in sorted(glob.glob(os.path.join(ROOT, "dewey-*.html"))):
    b = os.path.basename(f)
    code = b.split("-")[1]
    pal.append((b, names.get(code, b), "Dewey " + code))
prow = math.ceil((len(pal) - 1) / 2)
palr = region("palace", "The Palace of Subjects", "Dewey rooms, ten worlds of knowledge", -3600, y_left + prow * 205 / 2, COL["pal"], pic("journey/img/room2_library.webp"), pal[0][0])
rooms = ["room3_gallery", "room5_observatory", "room9_musicroom", "room4_courtyard", "room6_conservatory", "room7_workshop", "room8_attic", "room10_maproom", "room11_boathouse", "room12_teahouse"]
for i, (h, t, s) in enumerate(pal[1:]):
    cn = add("pal%d" % i, t, -4300 - (i % 2) * 340, y_left + 102 + (i // 2) * 205, 320, 180, "topic", COL["pal"], pic("journey/img/%s.webp" % rooms[i % len(rooms)]), h, s, "palace", 1, False)
    link(palr, cn, COL["pal"], 4)

# ---------- comics and guides (right, below General) ----------
ry = 3400 - 3400 + max(0, 0)
gen_bottom = max([n["y"] for n in nodes if n["id"].startswith("general_c")] + [0]) + 400
cy0 = gen_bottom
comics = [("comics/clear-line/", "The Clear Line", "A companion to Tintin", HOME + "comics/clear-line/art/abdullah.jpg"),
          ("comics/star-trek-columbo/", "Star Trek and Columbo", "Every episode", HOME + "comics/art/star-trek-columbo.jpg"),
          ("comics/marvel/", "The Marvel Universe Guide", "Heroes and key stories", HOME + "comics/art/marvel.jpg"),
          ("comics/silver-surfer/", "Silver Surfer: The Sentinel's Guide", "Comics and the 1998 series", HOME + "comics/silver-surfer/images/ss1_1.webp")]
cr = region("comics", "Comics & guides", "Worlds to get lost in", 3600, cy0 + 2 * 205, COL["com"], HOME + "comics/art/comics-header.jpg", HOME + "comics/")
for i, (h, t, s, im) in enumerate(comics):
    cn = add("cm%d" % i, t, 4300, cy0 + 102 + i * 205, 320, 180, "topic", COL["com"], im, HOME + h, s, "comics", 1, True)
    link(cr, cn, COL["com"], 4)
wy0 = cy0 + 4 * 205 + 160
wr = region("words", "My Words & My Room", "Review words, grow your room", 3600, wy0 + 205, COL["wr"], pic("journey/img/room1_study.webp"), "wordbank/index.html")
for i, (h, t, s, im) in enumerate([("wordbank/index.html", "My Words", "Every word you meet, with quiz and pictures", "journey/img/room12_teahouse.webp"),
                                    ("journey/index.html", "My Room", "A room that fills as you learn", "journey/img/room4_courtyard.webp"),
                                    ("malcolm_lesson_index.html", "Search every lesson", "Find any of the 3,400 lessons", "journey/img/room10_maproom.webp")]):
    cn = add("wr%d" % i, t, 4300, wy0 + 102 + i * 205, 320, 180, "topic", COL["wr"], pic(im), h, s, "words", 1, False)
    link(wr, cn, COL["wr"], 4)

# ---------- the library: every lesson ----------
meta = json.loads(re.search(r"WBALL=(\{.*\});?", open(os.path.join(ROOT, "wordbank/all_lessons.js"), encoding="utf-8").read(), re.S).group(1))
groups = {}
for k, (t, lv, se) in meta.items():
    groups.setdefault(se or ("Lessons without a series · " + (lv or "mixed levels")), []).append([k, re.sub(r"\s+", " ", t).strip()[:70], lv])
order = sorted(groups.items(), key=lambda kv: -len(kv[1]))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


lib_y = 2100
libr = region("library", "The Library", "Every lesson, in %d collections" % len(order), 0, lib_y, COL["lib"], pic("journey/img/room10_maproom.webp"), "malcolm_lesson_index.html")
cols, colw, gap = 5, 1010, 90
top = lib_y + 700
heights = [top] * cols
for gi, (name, ls) in enumerate(order):
    ls.sort(key=lambda r: r[0])
    rowsN = math.ceil(len(ls) / 6)
    h = 300 + rowsN * 66
    c = heights.index(min(heights))
    bx = (c - (cols - 1) / 2) * (colw + gap)
    by = heights[c]
    cover = pic(slug(name) + "_cover.jpg")
    libs.append(dict(id="lib%d" % gi, n=name, x=round(bx - colw / 2), y=round(by), w=colw, h=h, i=cover, ls=ls))
    heights[c] = by + h + gap
link(hub, libr, COL["lib"], 14)

pts = [(n["x"] - n["w"] / 2, n["y"] - n["h"] / 2, n["x"] + n["w"] / 2, n["y"] + n["h"] / 2) for n in nodes]
pts += [(b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]) for b in libs]
bbox = [min(p[0] for p in pts) - 300, min(p[1] for p in pts) - 300, max(p[2] for p in pts) + 300, max(p[3] for p in pts) + 300]
data = {"nodes": nodes, "edges": edges, "libs": libs, "bbox": bbox}
tpl = open(os.path.join(ROOT, "tools", "world_template.html"), encoding="utf-8").read()
open(os.path.join(ROOT, "world.html"), "w", encoding="utf-8").write(tpl.replace("/*DATA*/", "var W=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"))
print(len(nodes), "cards,", len(libs), "library collections,", sum(len(b["ls"]) for b in libs), "lessons;", [round(v) for v in bbox])
