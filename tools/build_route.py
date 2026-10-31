#!/usr/bin/env python3
"""Build a picture-led route page from an existing journey_<route>.html.
Usage: python3 tools/build_route.py professional   (rewrites journey_professional.html; old design stays in git history)
Reads the path cards and chapters of the original page (tools/route_src/), adds a goal for each, and counts
lessons the student has opened (wb_v1 in localStorage) where a dashboard links to a sensible number."""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
route = sys.argv[1] if len(sys.argv) > 1 else "professional"
src = open(os.path.join(ROOT, "tools", "route_src", "journey_%s.html" % route), encoding="utf-8").read()

CONF = {
    "professional": {
        "title": "Professional English",
        "line": "English for work. Meetings, presentations, negotiations — speak with authority in every room.",
        "q1": "What do you want to get better at?", "sub1": "Choose one and the page shows the best places to start.",
        "goals": [
            ("meetings", "Meetings & conversation", "Speak up, think on your feet, keep the conversation moving."),
            ("presenting", "Presenting & storytelling", "Hold a room with a clear story and a confident voice."),
            ("negotiating", "Negotiating & deals", "Trade fairs, bargaining, persuading and closing."),
            ("career", "Career & interviews", "Interviews, professional skills and senior communication."),
            ("writing", "Writing & grammar", "Emails, reports and grammar that works at work."),
            ("leading", "Leading & influencing", "The language of senior people: framing, steering, commanding a room."),
        ],
        "rules": [("Trade Fair", "negotiating"), ("Speaking Pathway", "meetings"), ("Grammar", "writing"), ("Bootcamp", "career"),
                  ("Business Meetings", "meetings"), ("Professional Skills", "career"), ("Listening", "meetings"),
                  ("Storytelling", "presenting"), ("Interview", "career"), ("Pronunciation", "presenting"),
                  ("Beyond Perfect", "leading"), ("Commanding", "leading")],
    },
    "academic": {
        "title": "Academic English & exams",
        "line": "Prepare for exams, university and academic life. IELTS, Cambridge, and the language of scholarship.",
        "q1": "What are you preparing for?", "sub1": "Choose one and the page shows the best places to start.",
        "goals": [
            ("ielts_writing", "IELTS writing", "Task 1 data and diagrams, essays, and the grammar behind them."),
            ("ielts_speaking", "Speaking & pronunciation", "Speak clearly and fluently, in exams and in seminars."),
            ("ielts_reading", "IELTS reading & vocabulary", "Reading tests and the academic words that unlock them."),
            ("academic_writing", "Academic writing", "Essays, accuracy and the grammar of scholarship."),
            ("lectures", "Lectures & listening", "Follow long talks and express complex ideas."),
            ("cambridge", "Cambridge exams", "Full preparation for the Cambridge qualifications."),
            ("big_ideas", "Big ideas", "Philosophy and ideas to think and argue about."),
        ],
        "rules": [("IELTS Reading", "ielts_reading"), ("IELTS Word", "ielts_reading"), ("IELTS", "ielts_writing"), ("Quick Fix", "ielts_writing"),
                  ("Cambridge", "cambridge"), ("Philosophy", "big_ideas"), ("Listening", "lectures"), ("Commanding", "lectures"),
                  ("Speaking", "ielts_speaking"), ("Pronunciation", "ielts_speaking"), ("Grammar", "academic_writing"),
                  ("Word Wall", "academic_writing"), ("Academic Writing", "academic_writing")],
    },
    "general": {
        "title": "General English",
        "line": "Build your English from the ground up. Speak with confidence in everyday life.",
        "q1": "Where would you like to start?", "sub1": "Pick the stage that sounds like you. You can always move up or down.",
        "nolevels": True, "bychapter": True,
        "goals": [
            ("first_steps", "First steps", "Hello, numbers, everyday words. Start from the very beginning."),
            ("finding_voice", "Finding your voice", "Start speaking about your life, your day, your plans."),
            ("growing_confidence", "Growing confidence", "Talk about opinions, stories and ideas with ease."),
            ("real_fluency", "Real fluency", "Handle real conversations, fast speech and finer detail."),
            ("mastery", "Mastery", "Sound natural, precise and thoughtful at the top level."),
        ],
        "chapters": {"First Steps": "first_steps", "Finding Your Voice": "finding_voice", "Growing Confidence": "growing_confidence",
                     "Real Fluency": "real_fluency", "Mastery": "mastery"},
    },
}[route]

def goal_of(chapter, name):
    if CONF.get("bychapter"):
        return CONF["chapters"].get(chapter, CONF["goals"][0][0])
    for k, v in CONF["rules"]:
        if k.lower() in name.lower():
            return v
    return CONF["goals"][0][0]


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
            "goal": goal_of(ctitle, html.unescape(g("path-name")).strip()),
            "ids": ids if 3 <= len(ids) <= 40 else [],
        })
levels = []
for c in cards:
    if c["level"] not in levels:
        levels.append(c["level"])

PAGE = open(os.path.join(ROOT, "tools", "route_template.html"), encoding="utf-8").read()
data = {"route": route, "title": CONF["title"], "line": CONF["line"], "q1": CONF["q1"], "sub1": CONF["sub1"], "nolevels": bool(CONF.get("nolevels")), "goals": CONF["goals"], "levels": levels, "cards": cards}
out = PAGE.replace("/*DATA*/", "var R=" + json.dumps(data, ensure_ascii=False) + ";").replace("{{TITLE}}", CONF["title"]).replace("{{ROUTE}}", route)
open(os.path.join(ROOT, "journey_%s.html" % route), "w", encoding="utf-8").write(out)
print(len(cards), "cards,", len(levels), "levels ->", "journey_%s.html" % route)
