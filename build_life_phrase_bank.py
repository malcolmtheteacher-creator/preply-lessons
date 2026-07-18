#!/usr/bin/env python3
"""Build the Life in English phrase bank from the lessons themselves.

Groups every taught phrase under the life area it came from, with each lesson's
skill as the label — so a student can find "the ways to say a hard thing to a
parent" rather than hunting through lessons.

Run after adding lessons:  python3 build_life_phrase_bank.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent

GROUPS = [
    ("Family", "👨‍👩‍👧", "Saying hard things to the people you can never resign from."),
    ("Love and dating", "❤️", "The conversations that decide what you are to each other."),
    ("Friends", "🫂", "Naming the thing a friendship needs said out loud."),
    ("Home and neighbours", "🏠", "Landlords, housemates, and the people through the wall."),
    ("Health and the body", "🩺", "Being heard by the people looking after you."),
    ("Money and admin", "💷", "Bills, refunds, and the money you're owed."),
    ("Trouble, blame and repair", "🔧", "Owning it, disputing it, and putting it right."),
    ("Big moments", "🕯️", "Births, deaths, goodbyes, and the days you only get once."),
]


def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " "),
                 ("&#39;", "'"), ("&quot;", '"')):
        s = s.replace(a, b)
    return " ".join(s.split()).strip()


def phrases_and_uses(path):
    """Each taught phrase is the <b> opener of a .rev; the text after it says why it works."""
    html = path.read_text(encoding="utf-8")
    panel = re.search(r'id="p2"(.*?)id="p3"', html, re.S)
    if not panel:
        return []
    out = []
    for m in re.finditer(r'<div class="rev"><b>(.*?)</b>(.*?)</div>', panel.group(1), re.S):
        phrase = clean(m.group(1))
        phrase = re.sub(r"^[A-C]\s*[—-]\s*", "", phrase)
        phrase = re.sub(r"^e\.g\.\s*", "", phrase).strip().strip('"').strip()
        # first sentence of the explanation, as the "what it does" line
        why = clean(m.group(2))
        why = why.split(". ")[0].strip()
        if len(why) > 180:
            why = why[:177].rsplit(" ", 1)[0] + "…"
        if phrase:
            out.append((phrase, why + ("." if why and not why.endswith((".", "!", "?", "…")) else "")))
    return out


def main():
    queue = json.load(open(HERE / "BUILD_QUEUE.json"))
    lessons = [s for s in queue if s["file"].startswith("lf_") and (HERE / s["file"]).exists()]

    style_src = (HERE / "modern_life_phrase_bank.html").read_text(encoding="utf-8")
    style = style_src[style_src.index("<style>"):style_src.index("</style>") + 8]

    sections, total = [], 0
    for group, emoji, blurb in GROUPS:
        rows = sorted([s for s in lessons if s["group"] == group], key=lambda s: s["file"])
        if not rows:
            continue
        sections.append('    <div class="func">\n        <h2>%s %s</h2>\n'
                        '        <p class="what">%s</p>\n' % (emoji, group, blurb))
        for s in rows:
            for phrase, why in phrases_and_uses(HERE / s["file"]):
                total += 1
                sections.append(
                    '        <div class="phrase">\n'
                    '            <div class="p">"%s"</div>\n'
                    '            <div class="use">%s</div>\n'
                    '            <span class="from">%s</span>\n'
                    '        </div>\n' % (phrase.replace('"', "&quot;"), why, s["title"])
                )
        sections.append("    </div>\n\n")

    names = ", ".join("<b>%s</b>" % s["title"] for s in sorted(lessons, key=lambda x: x["file"]))
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="collection" content="Life in English — Phrase Bank">
<meta name="description" content="Every phrase from every Life in English role play, grouped by the part of life it belongs to.">
<title>Life in English · Phrase Bank</title>
%s
</head>
<body>
<div class="wrap">
    <div class="hero noimg">
        <div class="cap">
            <span class="tag">Phrase Bank</span>
            <h1>Your Phrase Toolkit</h1>
            <p>Every phrase from every Life in English role play, in one place — grouped by the part of life it belongs to. Read it before a hard conversation, or after one that didn't go the way you wanted.</p>
        </div>
    </div>

%s    <div class="grow">
        <b>This toolkit grows with you.</b> It holds the phrases from %s. As more lessons are added, their phrases join these shelves. Same handful of human jobs; more ways to do them well.
    </div>

    <a class="back" href="life_in_english_dashboard.html">🌍 <span>Back to all the Life in English role plays</span><span class="go">→</span></a>

    <footer>Life in English · Phrase Bank</footer>
</div>
</body>
</html>
""" % (style, "".join(sections), names)

    out = HERE / "life_in_english_phrase_bank.html"
    out.write_text(html, encoding="utf-8")
    print("%s: %d phrases from %d lessons, %d sections"
          % (out.name, total, len(lessons), html.count('class="func"')))


if __name__ == "__main__":
    main()
