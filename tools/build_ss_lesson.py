#!/usr/bin/env python3
"""Build a Short Stories, Long Shadows / Longer Reads lesson from a JSON content file.

Usage:  python3 tools/build_ss_lesson.py tools/ss_content/<slug>.json [...]

The <style> and <script> blocks are copied verbatim from the series template
(techniques_there_will_come_soft_rains.html) at build time, so the content file
carries CONTENT only.  Story paragraphs may be literal HTML strings or a passage
spec that extracts the author's text from a downloaded public-domain source file:

  {"src": "/path/book.txt", "from": "unique phrase on first line",
   "to": "unique phrase on last line",
   "skip": [["phrase where a cut starts", "phrase where it ends"], ...],
   "drop": ["paragraph containing this phrase is removed", ...],
   "join": true}            # optional: return as ONE paragraph

Gap-fill items write ___ for each blank; it becomes an empty <input>.
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
TEMPLATE = os.path.join(SITE, "techniques_there_will_come_soft_rains.html")


def block(text, start, end):
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[i:j]


def passage(spec):
    """Return a list of paragraph strings (HTML-escaped) from a source text file."""
    raw = open(spec["src"], encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    def find(phrase, start=0, end_of=False):
        for k in range(start, len(lines)):
            if phrase in lines[k]:
                return k
            # phrase wrapped across two lines
            if k + 1 < len(lines) and phrase in (lines[k].rstrip() + " " + lines[k + 1].lstrip()):
                return k + 1 if end_of else k
        raise SystemExit(f"passage: phrase not found: {phrase!r}")
    a = find(spec["from"])
    b = find(spec["to"], a, end_of=True)
    chunk = "\n".join(lines[a:b + 1])
    # join wrapped lines inside paragraphs so phrases can span a line break
    chunk = re.sub(r"(?<!\n)\n(?!\n)", " ", chunk)
    for s, e in spec.get("skip", []):
        if s not in chunk:
            raise SystemExit(f"skip START not found (already cut?): {s!r}")
        i = chunk.index(s)
        if e not in chunk[i:]:
            raise SystemExit(f"skip END not found after start (already cut?): {e!r}")
        j = chunk.index(e, i) + len(e)
        chunk = chunk[:i] + chunk[j:]
    for pair in spec.get("replace", []):
        chunk = chunk.replace(pair[0], pair[1])
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", chunk)]
    paras = [p for p in paras if p]
    for d in spec.get("drop", []):
        paras = [p for p in paras if d not in p]
    paras = [p for p in paras if p not in spec.get("drop_exact", [])]
    paras = [html.escape(p, quote=False) for p in paras]
    # restore simple italics marked _like this_ in Gutenberg texts
    paras = [re.sub(r"_(.+?)_", r"<em>\1</em>", p) for p in paras]
    if spec.get("join"):
        paras = [" ".join(paras)]
    return paras


def story_paras(items):
    out = []
    for it in items:
        if isinstance(it, dict):
            out.extend(passage(it))
        else:
            out.append(it)
    return out


def gap(text):
    return text.replace("___", '<input type="text" placeholder="...">')


def reveal(inner_cls="meaning", label="Reveal", body=""):
    return (f'<button class="reveal-btn" onclick="this.nextElementSibling.classList.toggle(\'show\')">{label}</button>\n'
            f'                <div class="{inner_cls}">{body}</div>')


def build(c):
    tpl = open(TEMPLATE, encoding="utf-8").read()
    style = block(tpl, "<style>", "</style>")
    script = block(tpl, "<script>", "</script>")
    lvl = c["level"]
    tag = c.get("tag") or f'{c["series_tag"]} · {lvl} · 50 min'
    title_tag = c.get("title_tag") or f'{c["title_prefix"]}: {c["title"]} · {lvl}'
    footer = c.get("footer") or f'{c["title_prefix"]} · {c["title"]} · {lvl}'

    P = []
    P.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{c["series"]}">
<title>{title_tag}</title>
{style}
</head>
<body>
<div class="container">
    <header>
        <span class="tag">{tag}</span>
        <h1>{c["title"]}</h1>
        <p>{c["subtitle"]}</p>
    </header>

    <p class="crosslink">{c["crosslink"]}</p>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">Key Words</button>
        <button class="tab-btn" onclick="showTab(1)">The Story</button>
        <button class="tab-btn" onclick="showTab(2)">{c["grammar_tab"]}</button>
        <button class="tab-btn" onclick="showTab(3)">Going Deeper</button>
        <button class="tab-btn" onclick="showTab(4)">Speak</button>
    </nav>
''')

    # ---- TAB 0 KEY WORDS
    P.append('    <!-- TAB 0: KEY WORDS -->\n    <div class="tab-content active">\n        <div class="card">\n')
    P.append(f'            <div class="intention"><strong>Today:</strong> {c["intention"]}</div>\n')
    if c.get("previously"):
        P.append(f'            <div class="note"><strong>Previously…</strong> {c["previously"]}</div>\n')
    P.append('            <div class="discuss">\n                <strong>Before we read:</strong>\n                <ul>\n')
    for q in c["warmup"]:
        P.append(f'                    <li>{q}</li>\n')
    P.append('                </ul>\n            </div>\n')
    P.append(f'            <h2>Key words — think first, then check</h2>\n            <p>{c["vocab_intro"]}</p>\n')
    n = 0
    for g in c["vocab"]:
        P.append(f'            <h3>{g["heading"]}</h3>\n')
        if g.get("instruction"):
            P.append(f'            <p>{g["instruction"]}</p>\n')
        for it in g["items"]:
            n += 1
            P.append(f'            <div class="guess-item">\n                <div class="sent">{n}. {it["sent"]}</div>\n                {reveal("meaning", "Reveal", it["meaning"])}\n            </div>\n')
    P.append('            <h3>Now use them — out loud</h3>\n            <div class="discuss">\n                <strong>Talk it through before we read:</strong>\n                <ul>\n')
    for q in c["vocab_use"]:
        P.append(f'                    <li>{q}</li>\n')
    P.append('                </ul>\n            </div>\n        </div>\n    </div>\n\n')

    # ---- TAB 1 STORY
    P.append('    <!-- TAB 1: THE STORY -->\n    <div class="tab-content">\n        <div class="card">\n')
    P.append(f'            <h2>{c.get("story_h2", "The story, in three parts")}</h2>\n            <p>{c["story_intro"]}</p>\n')
    for part in c["story"]:
        P.append(f'            <h3>{part["title"]}</h3>\n            <div class="story-chunk">\n')
        for para in story_paras(part["paras"]):
            P.append(f'                <p>{para}</p>\n')
        P.append('            </div>\n')
        P.append('            <div class="check">\n                <div class="q">Quick check — answer from memory, then reveal:</div>\n')
        for i, qa in enumerate(part["check"], 1):
            P.append(f'                <p>{i}. {qa["q"]}</p>\n')
        ans = "".join(f'<p><strong>{i}.</strong> {qa["a"]}</p>' for i, qa in enumerate(part["check"], 1))
        P.append(f'                {reveal("answers", "Reveal answers", ans)}\n            </div>\n')
        P.append(f'            <div class="discuss">\n                <strong>Discuss:</strong>\n                <ul><li>{part["discuss"]}</li></ul>\n            </div>\n')
    P.append('        </div>\n    </div>\n\n')

    # ---- TAB 2 GRAMMAR
    g = c["grammar"]
    P.append('    <!-- TAB 2: GRAMMAR -->\n    <div class="tab-content">\n        <div class="card">\n')
    P.append(f'            <h2>{g["h2"]}</h2>\n            <p>{g["intro"]}</p>\n')
    for note in g["notes"]:
        P.append(f'            <div class="note">{note}</div>\n')
    for k, ex in enumerate(g["exercises"], 1):
        eid = f"gAns{k}"
        P.append(f'            <h3>{k}. {ex["h3"]}</h3>\n')
        if ex.get("instruction"):
            P.append(f'            <p>{ex["instruction"]}</p>\n')
        P.append('            <div class="gap-fill">\n')
        for i, item in enumerate(ex["items"], 1):
            P.append(f'                <p>{i}. {gap(item)}</p>\n')
        P.append(f'                <button class="reveal-btn" onclick="document.getElementById(\'{eid}\').classList.toggle(\'show\')">Reveal answers</button>\n                <div class="answers" id="{eid}">\n')
        for i, a in enumerate(ex["answers"], 1):
            P.append(f'                    <p><strong>{i}.</strong> {a}</p>\n')
        if ex.get("note"):
            P.append(f'                    <p><em>{ex["note"]}</em></p>\n')
        P.append('                </div>\n            </div>\n')
    if g.get("outro"):
        P.append(f'            <p style="margin-top:14px; color:#666; font-style:italic;">{g["outro"]}</p>\n')
    P.append('        </div>\n    </div>\n\n')

    # ---- TAB 3 GOING DEEPER
    d = c["deeper"]
    P.append('    <!-- TAB 3: GOING DEEPER -->\n    <div class="tab-content">\n        <div class="card">\n')
    P.append(f'            <h2>{d["h2"]}</h2>\n')
    for para in d["paras"]:
        P.append(f'            <p>{para}</p>\n')
    if d.get("note"):
        P.append(f'            <div class="note">{d["note"]}</div>\n')
    P.append(f'            <h3>{d.get("discuss_title", "Go deeper — talk it through")}</h3>\n            <div class="discuss">\n                <strong>Discuss:</strong>\n                <ul>\n')
    for q in d["questions"]:
        P.append(f'                    <li>{q}</li>\n')
    P.append('                </ul>\n            </div>\n        </div>\n    </div>\n\n')

    # ---- TAB 4 SPEAK
    s = c["speak"]
    P.append('    <!-- TAB 4: SPEAK -->\n    <div class="tab-content">\n        <div class="card">\n            <h2>Speak</h2>\n')
    P.append(f'            <p>{s.get("intro", "This is the heart of the lesson — do all three out loud. The timer is there to keep you going: fill the time with detail rather than escaping it.")}</p>\n')
    P.append(f'            <div class="note"><strong>Useful language:</strong> {s["useful"]}</div>\n')
    P.append('''            <div class="timer">
                <span>Time remaining: <strong><span id="timer-display">4:00</span></strong></span>
                <div class="timer-controls">
                    <button class="duration-btn" onclick="setDuration(this, 3)">3 min</button>
                    <button class="duration-btn active" onclick="setDuration(this, 4)">4 min</button>
                    <button class="duration-btn" onclick="setDuration(this, 5)">5 min</button>
                    <button class="timer-btn" onclick="startTimer()">Start</button>
                    <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
                </div>
            </div>
''')
    for t in s["tasks"]:
        P.append(f'            <div class="speak-prompt">\n                <span class="speak-label">{t["label"]}</span>\n')
        for para in t["paras"]:
            P.append(f'                <p>{para}</p>\n')
        if t.get("menu"):
            lead = t.get("menu_lead", "Stuck for an idea? Pick one of these and run with it:" if lvl == "B2/C1" else "Not sure what to talk about? Choose one:")
            P.append(f'                <p style="margin-top:6px;"><strong>{lead}</strong></p>\n                <ul style="margin:6px 0 0 20px; color:#3a2a5a;">\n')
            for m in t["menu"]:
                P.append(f'                    <li>{m}</li>\n')
            P.append('                </ul>\n')
        P.append('            </div>\n')
    P.append(f'            <div class="final-discussion">\n                <h3>{s.get("final_title", "To finish — the bigger questions")}</h3>\n                <ol>\n')
    for q in s["final"]:
        P.append(f'                    <li>{q}</li>\n')
    P.append('                </ol>\n            </div>\n        </div>\n    </div>\n\n')

    P.append(f'    <footer>\n        {footer}\n    </footer>\n</div>\n\n{script}\n</body>\n</html>\n')
    return "".join(P)


def verify(path, text):
    probs = []
    if text.count('class="tab-content') != 5: probs.append("tab-content != 5")
    if "value=" in text: probs.append("prefilled value=")
    for bad in ("podcast", "spotify", "noiser", "Malcolm", "TEEP", "Simplified", "Teacher:"):
        if bad.lower() in text.lower(): probs.append(f"contains {bad}")
    if not text.rstrip().endswith("</html>"): probs.append("no </html>")
    if "class=\"crosslink\"" not in text: probs.append("no crosslink")
    return probs


if __name__ == "__main__":
    for jp in sys.argv[1:]:
        c = json.load(open(jp, encoding="utf-8"))
        out = build(c)
        dest = os.path.join(SITE, c["file"])
        open(dest, "w", encoding="utf-8").write(out)
        probs = verify(dest, out)
        print(f"{c['file']}: {len(out)//1024} KB", "OK" if not probs else "PROBLEMS: " + "; ".join(probs))
