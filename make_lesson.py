#!/usr/bin/env python3
"""Assemble a role-play lesson from a content file.

The CSS/JS shell is taken verbatim from a built lesson, so every lesson stays
identical in style and behaviour. You write only the lesson content.

Usage:  python3 make_lesson.py content/lf_21_the_late_friend.py

The content file defines: TITLE, INTRO, and PANELS (a list of 5 HTML strings).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SHELLS = {"wk": "_shell_wk", "ml": "_shell_ml"}   # per-series: Work has a 3rd-speaker style


def shell_for(mod, out_name):
    """Work and Modern Life templates differ (.say-c). Pick by filename prefix."""
    prefix = out_name[:2]
    base = SHELLS.get(prefix, "_shell")
    return HERE / (base + "_head.html"), HERE / (base + "_tail.html")


def build(mod, out_path):
    head_path, tail_path = shell_for(mod, Path(out_path).name)
    head = head_path.read_text(encoding="utf-8")
    series = getattr(mod, "SERIES", "Life in English")

    head = re.sub(r"<title>.*?</title>", f"<title>{series} · {mod.TITLE}</title>", head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  lambda m: m.group(1) + f"{series} — {mod.TITLE}: {mod.SUMMARY}" + m.group(2),
                  head, count=1)
    head = re.sub(r'(<meta name="collection" content=")[^"]*(">)',
                  lambda m: m.group(1) + f"{series} — Conversation Role Plays" + m.group(2),
                  head, count=1)
    head = re.sub(r'(<div class="tag">)[^<]*(</div>)',
                  lambda m: m.group(1) + f"{series} · Role Play · B2/C1 · 50 min" + m.group(2),
                  head, count=1)
    head = re.sub(r"<h1>.*?</h1>", f"<h1>{mod.TITLE}</h1>", head, count=1)
    head = re.sub(r"(</h1>\s*<p>).*?(</p>)", lambda m: m.group(1) + mod.INTRO + m.group(2),
                  head, count=1, flags=re.S)

    ids = ["p0", "p1", "p2", "p3", "p4"]
    body = "\n\n".join(
        f'    <div class="panel{" active" if i == 0 else ""}" id="{ids[i]}">\n{p}\n    </div>'
        for i, p in enumerate(mod.PANELS)
    )
    html = head + body + tail_path.read_text(encoding="utf-8")
    Path(out_path).write_text(html, encoding="utf-8")
    return html


def check(html, path):
    """The hard rules, checked mechanically."""
    problems = []
    if html.count('class="panel') != 5:
        problems.append(f'{html.count(chr(34)+"class=" ) or ""}panels != 5')
    if html.count("panel active") != 1:
        problems.append("not exactly one active panel")
    if html.count('button class="tab-btn') != 5:
        problems.append("tab buttons != 5")
    if "value=" in html:
        problems.append("value= present (pre-filled input)")
    if "rev open" in html:
        problems.append("a .rev is left open")
    for word in ("I Do", "We Do", "You Do", "Retrieval", "TEEP", "Simplified", "Malcolm"):
        if re.search(r"\b" + re.escape(word) + r"\b", html):
            problems.append(f'possible 4th-wall breach: "{word}"')
    for fn in ("function showTab", "function toggleRev", "function startTimer"):
        if fn not in html:
            problems.append(f"missing JS: {fn}")
    for m in re.finditer(r'<div class="say say-[abc]">(.{0,60})', html, re.S):
        if not m.group(1).startswith('<span class="who-label">'):
            problems.append("malformed speaker tag: " + m.group(1)[:40])
    if re.search(r'<span class="who-(?!label)', html):
        problems.append("bad who- span class")
    if html.count("<textarea") != html.count("</textarea>"):
        problems.append("unbalanced textarea tags")
    return problems


if __name__ == "__main__":
    src = Path(sys.argv[1])
    sys.path.insert(0, str(src.parent))
    mod = __import__(src.stem)
    out = HERE / (mod.FILE if hasattr(mod, "FILE") else src.stem + ".html")
    html = build(mod, out)
    probs = check(html, out)
    print(f"{out.name}: {len(html)//1000}KB", "OK" if not probs else "PROBLEMS: " + "; ".join(probs))
