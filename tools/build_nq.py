#!/usr/bin/env python3
"""Build the 'Name the Question' lessons (C1, 50 min each) from content files.

  tools/nq_content/NN_<slug>.json  ->  nq_NN_<slug>_c1.html   (one lesson each)

Reuses the Think Inside the Box engine (build_tib.py): the same five tabs
(Key Words, The Cases, The Lens, Language, Speak), recoloured per kind of
question, plus a new 'lens' diagram (questions that lead to outcomes).
The pathway map and the kind pages are built by build_nameq.py.
Usage: python3 tools/build_nq.py     (always rebuilds everything)
"""
import json, os, re, glob, itertools, html, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_tib as T  # noqa: E402

ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "nq_content")
PATHWAY = os.path.join(HERE, "nameq_content", "pathway.json")
SERIES = "Name the Question"
DASH = "name_the_question_dashboard.html"
E = html.escape

# ---------------------------------------------------------------- colour
BASE = {  # the kind colours used on the map
    "go": "#0f9488", "which": "#d9910e", "first": "#7e57c2",
    "if": "#d2453d", "why": "#5b9a3c", "right": "#3f6fcf", "mixed": "#2f5f8a",
}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)


def mix(h, w, toward=(255, 255, 255)):
    r = _rgb(h)
    return _hex([r[i] * (1 - w) + toward[i] * w for i in range(3)])


def palette(base):
    dark = mix(base, 0.55, (10, 14, 24))
    mid = mix(base, 0.18, (10, 14, 24))
    return {
        "#0e7490": mid, "#0f766e": mid, "#115e59": dark, "#134e4a": mix(base, 0.68, (10, 14, 24)),
        "#1f3d3a": mix(base, 0.62, (10, 14, 24)),
        "#7cc4bb": mix(base, 0.45), "#99d5cc": mix(base, 0.58),
        "#c5e6e1": mix(base, 0.78), "#cdeae5": mix(base, 0.80), "#cfe7e3": mix(base, 0.78),
        "#e2f4f1": mix(base, 0.88), "#f1f9f8": mix(base, 0.93), "#eaf6f4": mix(base, 0.90),
        "#e3f2ef": mix(base, 0.89), "#f5fbfa": mix(base, 0.95), "#eef7f6": mix(base, 0.92),
        "#f7fbfa": mix(base, 0.96),
        "rgba(14,116,144,": "rgba(%d,%d,%d," % _rgb(mid),
    }


def tint(s, base):
    for a, b in palette(base).items():
        s = s.replace(a, b)
    return s


# ---------------------------------------------------------------- the lens diagram
def d_lens(d):
    steps, outs = d["steps"], d["outcomes"]
    col, tnt, ink = d["color"], d["tint"], d["ink"]
    W = 700
    n, m = len(steps), len(outs)
    gap = 34
    bw = (W - 40 - (n - 1) * gap) / n
    parts = [f'<svg viewBox="0 0 {W} 300" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">',
             f'<defs><marker id="la" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
             f'<path d="M0,0 L9,4.5 L0,9 z" fill="{col}"/></marker></defs>']
    for i, s in enumerate(steps):
        x = 20 + i * (bw + gap)
        parts.append(f'<rect x="{x:.1f}" y="18" width="{bw:.1f}" height="92" rx="14" fill="{tnt}" stroke="{col}" stroke-width="2.4"/>')
        parts.append(f'<circle cx="{x + 24:.1f}" cy="40" r="14" fill="{col}"/>')
        parts.append(T.svg_text(x + 24, 40, str(i + 1), 14, "700", "#ffffff"))
        parts.append(T.svg_text(x + bw / 2 + 8, 70, s, 15, "700", ink))
        if i < n - 1:
            parts.append(f'<line x1="{x + bw + 4:.1f}" y1="64" x2="{x + bw + gap - 4:.1f}" y2="64" stroke="{col}" stroke-width="2.4" marker-end="url(#la)"/>')
    parts.append(f'<line x1="{W / 2}" y1="114" x2="{W / 2}" y2="150" stroke="{col}" stroke-width="2.4" marker-end="url(#la)"/>')
    parts.append(T.svg_text(W / 2 + 70, 132, "it can lead to", 13, "600", col, "start"))
    ow = (W - 40 - (m - 1) * 14) / m
    for j, o in enumerate(outs):
        x = 20 + j * (ow + 14)
        parts.append(f'<rect x="{x:.1f}" y="156" width="{ow:.1f}" height="128" rx="14" fill="#ffffff" stroke="{col}" stroke-width="2.4"/>')
        parts.append(f'<rect x="{x:.1f}" y="156" width="{ow:.1f}" height="36" rx="14" fill="{col}"/>')
        parts.append(f'<rect x="{x:.1f}" y="178" width="{ow:.1f}" height="14" fill="{col}"/>')
        parts.append(T.svg_text(x + ow / 2, 174, o["w"], 14.5, "700", "#ffffff"))
        parts.append(T.svg_text(x + ow / 2, 236, o["d"], 12.5, "500", ink))
    parts.append("</svg>")
    return "".join(parts)


T.DIAGRAMS["lens"] = d_lens


# ---------------------------------------------------------------- page

def story_html(d):
    out = T.story(d)
    for part in d["story"]:
        seen = part.get("seen")
        if not seen:
            continue
        names = " and ".join(f'<a href="{x["href"]}">{E(x["title"])}</a>' for x in seen)
        note = (f'<p class="seen">You may have met this case in {names}. '
                f'This time, look at it through the lens.</p>')
        marker = f'<h3>{part["heading"]}</h3>'
        assert marker in out, part["heading"]
        out = out.replace(marker, marker + "\n            " + note, 1)
    return out

def lesson(d, lessons, pathway):
    kind = d["kind"]
    base = BASE[kind]
    css = tint(T.CSS, base) + ".seen{font-size:.9rem;color:#556;font-style:italic;margin:-2px 0 10px}.seen a{color:inherit}\n"
    ink = mix(base, 0.62, (10, 14, 24))
    T.INK, T.TEAL, T.LIGHT = ink, mix(base, 0.18, (10, 14, 24)), mix(base, 0.88)
    dg = d["tool_tab"]["diagram"]
    dg.update(color=base, tint=mix(base, 0.86), ink=ink)
    i = [x["slug"] for x in lessons].index(d["slug"])
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    fn = lambda x: f'nq_{x["slug"]}_c1.html'
    strip = [f'<a href="{DASH}">The whole pathway</a>']
    if d.get("page"):
        strip.append(f'<a href="{d["page"]}">{E(d["cue"])} — the quick guide</a>')
    if prev:
        strip.insert(0, f'<a href="{fn(prev)}">&larr; {E(prev["title"])}</a>')
    if nxt:
        strip.append(f'<a href="{fn(nxt)}">{E(nxt["title"])} &rarr;</a>')
    total = len(lessons)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{E(d["title"])} · C1 English</title>
<style>
{css}</style>
</head>
<body>
<div class="container">
    <header style="background: linear-gradient(135deg, {mix(base, 0.12, (10, 14, 24))} 0%, #12284a 100%);">
        <span class="tag">NAME THE QUESTION · {d["num"]} OF {total} · C1 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <p class="series-strip">{" &nbsp;·&nbsp; ".join(strip)}</p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Cases</button>
        <button class="tab-btn" onclick="showTab(2)">The Lens</button>
        <button class="tab-btn" onclick="showTab(3)">Language — {d["grammar"]["name"]}</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>

    <!-- TAB 0 -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>
            <div class="discuss">
                <strong>Before we start — have a go, and don't worry about mistakes:</strong>
                <ul>
{T.ul(d["warmup"])}
                </ul>
            </div>

            <h2>The vocabulary of this lesson</h2>
            <p>Ten items. Say your answer <strong>out loud before you reveal it</strong>.</p>

{T.vocab(d)}

            <h3>Now use them — out loud</h3>
            <div class="discuss">
                <ul>
{T.ul(d["vocab_use"])}
                </ul>
            </div>
        </div>
    </div>

    <!-- TAB 1 -->
    <div class="tab-content">
        <div class="card">
            <h2>The cases, in three parts</h2>
            <p>Read each part. After it, answer the quick check from memory, then discuss one question. The figures are rounded, and the facts are as the cases were reported.</p>

{story_html(d)}
        </div>
    </div>

    <!-- TAB 2 -->
    <div class="tab-content">
        <div class="card">
{T.tool_tab(d["tool_tab"]).replace("How the tool works", "How the lens works").replace("Where the tool breaks", "Where the lens breaks").replace("Its cousins", "Related lessons")}
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
        {SERIES} · {E(d["title"])} · C1
    </footer>
</div>

<script>
{T.JS}</script>
</body>
</html>
'''



def capstone(d, lessons):
    base = BASE["mixed"]
    css = tint(T.CSS, base)
    i = [x["slug"] for x in lessons].index(d["slug"])
    prev = lessons[i - 1] if i > 0 else None
    strip = [f'<a href="{DASH}">The whole pathway</a>']
    if prev:
        strip.insert(0, f'<a href="nq_{prev["slug"]}_c1.html">&larr; {E(prev["title"])}</a>')
    total = len(lessons)
    s = d["sort"]
    opts = "".join(f'<option value="{E(o)}">{E(o)}</option>' for o in s["options"])
    rows = "\n".join(f'''                <div class="sort-row" data-answer="{E(it["answer"])}">
                    <span class="txt">{n}. {it["text"]}</span>
                    <select><option value="">choose…</option>{opts}</select>
                    <span class="mark"></span>
                </div>''' for n, it in enumerate(s["items"], 1))
    why = "\n".join(f'                    <p><strong>{n}. {E(it["answer"])}</strong> — {it["why"]}</p>'
                    for n, it in enumerate(s["items"], 1))
    guess = lambda q, a: (f'<div class="guess-item"><div class="sent">{q}</div>{T.REVEAL.format("Reveal")}'
                          f'<div class="meaning">{a}</div></div>')
    lenses = "\n".join(guess(f'<b>{E(l["kind"])}</b> — {l["prompt"]}', l["answer"]) for l in d["lenses"])
    breaks = "\n".join(guess(b["q"], b["a"]) for b in d["breaks"]["items"])
    cards = "".join(f"<li>{E(c)}</li>" for c in d["cards"])
    speak = T.speak(d["speak"]).replace("<h2>Speak</h2>", "<h2>Say it</h2>")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>{E(d["title"])} · C1 English</title>
<style>
{css}</style>
</head>
<body>
<div class="container">
    <header style="background: linear-gradient(135deg, {mix(base, 0.12, (10, 14, 24))} 0%, #12284a 100%);">
        <span class="tag">NAME THE QUESTION · {d["num"]} OF {total} · C1 · 50 min</span>
        <h1>{d["title"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <p class="series-strip">{" &nbsp;·&nbsp; ".join(strip)}</p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Name it</button>
        <button class="tab-btn" onclick="showTab(1)">Think it</button>
        <button class="tab-btn" onclick="showTab(2)">Say it</button>
        <button class="tab-btn" onclick="showTab(3)">Where it breaks</button>
    </nav>

    <!-- TAB 0 -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>
            <h2>Have a go, and don’t worry about mistakes</h2>
{guess(d["recall"]["prompt"], d["recall"]["answer"])}
            <h2>Name the question</h2>
            <p>{s["intro"]}</p>
            <div id="sort1">
{rows}
                <button class="check-btn" onclick="checkSort('sort1')">Check my answers</button><span class="score"></span>
                <br>{T.REVEAL.format("Show the reasons")}
                <div class="answers">
{why}
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 1 -->
    <div class="tab-content">
        <div class="card">
            <h2>The six lenses, from memory</h2>
            <p>Say each lens out loud before you reveal it. Then say one real question of that kind, and what you would do first.</p>
{lenses}
        </div>
    </div>

    <!-- TAB 2 -->
    <div class="tab-content">
        <div class="card">
{speak}
            <h3>The question cards</h3>
            <div class="note"><ol style="margin:4px 0 0 22px">{cards}</ol></div>
        </div>
    </div>

    <!-- TAB 3 -->
    <div class="tab-content">
        <div class="card">
            <h2>Where it breaks</h2>
            <p>{d["breaks"]["intro"]}</p>
{breaks}
            <div class="discuss">
                <strong>Talk it through:</strong>
                <ul>
{T.ul(d["breaks"]["discuss"])}
                </ul>
            </div>
        </div>
    </div>

    <footer>
        {SERIES} · {E(d["title"])} · C1
    </footer>
</div>

<script>
{T.JS}</script>
</body>
</html>
'''

# ---------------------------------------------------------------- checks
FORBIDDEN = ("Malcolm", "your teacher", "Your teacher", "The teacher will", "I Do", "We Do", "You Do",
             "TEEP", "Pause:", "Exploration", "Knowledge Building", "TODO", "[Add", "[Insert")


def check_capstone(d):
    s = d["slug"]
    sort = d["sort"]
    ans = [it["answer"] for it in sort["items"]]
    assert all(a in sort["options"] for a in ans), f"{s}: sort answer not in options"
    assert max(len(list(g)) for _, g in itertools.groupby(ans)) < 3, f"{s}: same sort answer 3 in a row"
    assert set(ans) == set(sort["options"]), f"{s}: every kind should appear"
    assert len(d["lenses"]) == 6, f"{s}: six lenses"
    blob = json.dumps(d, ensure_ascii=False)
    for bad in FORBIDDEN:
        assert bad not in blob, f"{s}: forbidden text {bad!r}"


def check(d):
    if d["kind"] == "mixed":
        return check_capstone(d)
    s = d["slug"]
    n_items = sum(len(x["items"]) for x in d["vocab"])
    assert n_items == 10, f"{s}: {n_items} vocab items, want 10"
    va, vb, vc = d["vocab"]
    assert va["heading"].startswith("A · What do they mean here?"), f"{s}: vocab A heading"
    assert vb["heading"].startswith("B · Which term means"), f"{s}: vocab B must be 'Which term means…?'"
    assert vb["intro"].count("·") >= 2, f"{s}: vocab B intro must list the three terms (a · b · c)"
    assert all("<b>" in it["sent"] for it in vb["items"]), f"{s}: vocab B questions must quote a definition in bold"
    answers = [re.search(r"<b>(.*?)</b>", it["meaning"]).group(1).lower() for it in vb["items"]]
    listed = [t.strip().lower() for t in vb["intro"].split(":", 1)[1].split(".")[0].split("·")]
    assert sorted(answers) == sorted(listed), f"{s}: vocab B intro terms must match the answers {answers} vs {listed}"
    assert not any(a == l for a, l in zip(answers, listed)), f"{s}: vocab B terms listed in the same order as the answers - shuffle"
    assert vc["heading"].startswith("C · Which word completes all three phrases"), f"{s}: vocab C heading"
    assert all(it["sent"].count("___") == 3 for it in vc["items"]), f"{s}: each vocab C item needs three ___"
    assert len(d["story"]) == 3, f"{s}: story must have 3 parts"
    for p in d["story"]:
        assert len(p["checks"]) == len(p["answers"]), f"{s}: checks/answers mismatch in {p['heading']}"
    tt = d["tool_tab"]
    assert tt["diagram"]["type"] == "lens", f"{s}: tool diagram must be the lens"
    sort = tt["sort"]
    ans = [it["answer"] for it in sort["items"]]
    assert all(a in sort["options"] for a in ans), f"{s}: sort answer not in options"
    assert max(len(list(g)) for _, g in itertools.groupby(ans)) < 3, f"{s}: same sort answer 3 in a row"
    assert len(set(ans)) >= 3, f"{s}: sort uses too few outcomes"
    for ex in d["grammar"]["exercises"]:
        assert len(ex["items"]) == len(ex["answers"]), f"{s}: grammar items/answers mismatch"
        assert all(it.count("___") >= 1 for it in ex["items"]), f"{s}: grammar item without a gap"
    for c in tt["cousins"]:
        if c.get("lesson") and not c["lesson"].startswith("nq_"):
            assert os.path.exists(os.path.join(ROOT, c["lesson"])), f"missing link target {c['lesson']}"
    blob = json.dumps(d, ensure_ascii=False)
    for bad in FORBIDDEN:
        assert bad not in blob, f"{s}: forbidden text {bad!r}"
    assert "value=" not in blob, f"{s}: pre-filled input"


def main():
    lessons = [json.load(open(p, encoding="utf8")) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    pathway = json.load(open(PATHWAY, encoding="utf8"))
    kinds = {b["id"]: b for b in pathway["branches"]}
    for d in lessons:
        if d["kind"] in kinds:
            d["cue"], d["page"] = kinds[d["kind"]]["cue"], kinds[d["kind"]]["page"]
        check(d)
    for d in lessons:
        out = os.path.join(ROOT, f'nq_{d["slug"]}_c1.html')
        html_out = capstone(d, lessons) if d["kind"] == "mixed" else lesson(d, lessons, pathway)
        open(out, "w", encoding="utf8").write(html_out)
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out) // 1024}KB)")
    # every link must resolve
    bad = []
    for d in lessons:
        f = f'nq_{d["slug"]}_c1.html'
        for h in re.findall(r'href="([^"#]+)', open(os.path.join(ROOT, f), encoding="utf8").read()):
            if not h.startswith("http") and not os.path.exists(os.path.join(ROOT, h)):
                bad.append((f, h))
    assert not bad, f"broken links: {bad}"


if __name__ == "__main__":
    main()
