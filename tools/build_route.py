#!/usr/bin/env python3
"""Build a picture-led route page from an existing journey_<route>.html.
Usage: python3 tools/build_route.py professional   (writes journey_professional_new.html)
Reads the path cards and chapters of the current page, adds a goal for each, and counts
lessons the student has opened (wb_v1 in localStorage) where a dashboard links to a sensible number."""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
route = sys.argv[1] if len(sys.argv) > 1 else "professional"
src = open(os.path.join(ROOT, "journey_%s.html" % route), encoding="utf-8").read()

CONF = {
    "professional": {
        "title": "Professional English",
        "line": "English for work. Meetings, presentations, negotiations — speak with authority in every room.",
        "goals": [
            ("meetings", "Meetings & conversation", "Speak up, think on your feet, keep the conversation moving."),
            ("presenting", "Presenting & storytelling", "Hold a room with a clear story and a confident voice."),
            ("negotiating", "Negotiating & deals", "Trade fairs, bargaining, persuading and closing."),
            ("career", "Career & interviews", "Interviews, professional skills and senior communication."),
            ("writing", "Writing & grammar", "Emails, reports and grammar that works at work."),
        ],
        "map": {
            "trade_fair": "negotiating", "speaking_pathway": "meetings", "CEFR_Grammar": "writing",
            "business_bootcamp": "career", "business_meetings": "meetings", "professional_skills": "career",
            "listening-lessons": "meetings", "strategic_storytelling": "presenting", "senior_interview": "career",
            "pronunciation_pathway": "presenting", "beyond_perfect": "presenting", "commanding_discourse": "negotiating",
        },
        "colours": ["#1f3a30", "#d4a437"],
    }
}[route]

cards = []
for ch in re.split(r'<div class="chapter">', src)[1:]:
    lvl = re.search(r'class="chapter-badge"[^>]*>([^<]+)<', ch).group(1).strip()
    ctitle = html.unescape(re.search(r'class="chapter-title">([^<]+)<', ch).group(1))
    for m in re.finditer(r'<a class="path-card" href="([^"]+)">(.*?)</a>', ch, re.S):
        body = m.group(2)
        g = lambda c: (re.search(r'class="%s"[^>]*>(.*?)</div>' % c, body, re.S) or [None, ""])[1]
        tag = re.search(r'class="path-tag"[^>]*>([^<]+)<', body)
        href = m.group(1)
        stem = re.sub(r"_?[Dd]ashboard\.html$|\.html$", "", href)
        ids = []
        p = os.path.join(ROOT, href)
        if os.path.exists(p):
            d = open(p, encoding="utf-8", errors="ignore").read()
            ids = sorted({x[:-5] for x in re.findall(r'href="([^"#?]+\.html)"', d)
                          if not x.startswith("http") and "dashboard" not in x.lower() and os.path.exists(os.path.join(ROOT, x))})
        cards.append({
            "href": href, "level": lvl, "chapter": ctitle, "tag": tag.group(1) if tag else "",
            "name": html.unescape(g("path-name")).strip(), "desc": html.unescape(g("path-desc")).strip(),
            "meta": html.unescape(g("path-meta")).strip(),
            "goal": CONF["map"].get(stem, CONF["goals"][0][0]),
            "ids": ids if 3 <= len(ids) <= 40 else [],
        })
levels = []
for c in cards:
    if c["level"] not in levels:
        levels.append(c["level"])

PAGE = open(os.path.join(ROOT, "tools", "route_template.html"), encoding="utf-8").read()
data = {"route": route, "title": CONF["title"], "line": CONF["line"], "goals": CONF["goals"], "levels": levels, "cards": cards}
out = PAGE.replace("/*DATA*/", "var R=" + json.dumps(data, ensure_ascii=False) + ";").replace("{{TITLE}}", CONF["title"]).replace("{{ROUTE}}", route)
open(os.path.join(ROOT, "journey_%s_new.html" % route), "w", encoding="utf-8").write(out)
print(len(cards), "cards,", len(levels), "levels ->", "journey_%s_new.html" % route)
