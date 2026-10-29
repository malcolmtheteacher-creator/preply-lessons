#!/usr/bin/env python3
"""Build wordbank/words.js from lesson HTML files.

Reads every `<div class="meaning"><b>word</b> (pos) — definition</div>` entry
(plus the sentence just before it, for a context example) and writes one
registry the Word Bank page loads.

Usage:
  python3 tools/build_wordbank.py                 # default lesson globs below
  python3 tools/build_wordbank.py 'bc_*.html'     # add more lessons by glob
  python3 tools/build_wordbank.py --auto          # every lesson that uses the meaning markup
  python3 tools/build_wordbank.py --inject        # also add the tiny
                                                   # "lesson opened" hook to each lesson
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "wordbank", "words.js")
DEFAULT_GLOBS = ["psy_*_a2b1.html", "psy_*_b2c1.html", "psyp_*_a2b1.html", "psyp_*_b2c1.html"]
HOOK = '<script src="wordbank/hook.js"></script>'

MEANING = re.compile(r'<div class="meaning">(.*?)</div>', re.S)
ENTRY = re.compile(r'^<b>(.+?)</b>\s*(?:\(([^)]{1,12})\))?\s*(?:—|-|–)?\s*(.*)$', re.S)
SENT = re.compile(r'<div class="sent">(.*?)</div>', re.S)


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def level_of(stem):
    return "B2/C1" if stem.endswith("b2c1") else "A2/B1" if stem.endswith("a2b1") else "A1" if stem.startswith("a1s_") else ""


POS = {"noun": "n", "verb": "v", "adjective": "adj", "adverb": "adv", "phrasal verb": "phr v", "phrase": "phr"}
CARD_FIELD = {k: re.compile(r'<div class="%s"[^>]*>(.*?)</div>' % k, re.S) for k in ("word", "pos", "def", "ex")}


def norm_word(word):
    w = re.sub(r"^(\([a-z]\)\s*)?(to|a|an|the) ", r"\1", word.lower())
    w = re.sub(r"^\([a-z]\)\s*", "", w).strip()
    w = re.split(r"\s+[/(]", w)[0].strip(" \u201c\u201d\"'")
    if w in ("did", "for", "false", "true") or re.search(r"[.?!:,;]$", w) or len(w.split()) > 4:
        return ""
    if len(w) < 2 or not re.search(r"[a-z]{2}", w):
        return ""
    return w


def entries(text):
    """Yield (word, pos, definition, example) from either lesson markup."""
    for m in MEANING.finditer(text):
        e = ENTRY.match(m.group(1).strip())
        if not e:
            continue
        word, pos, rest = clean(e.group(1)), (e.group(2) or "").strip(), clean(e.group(3))
        example = ""
        ex = re.search(r'Example:\s*["\u201c](.+?)["\u201d]', rest)
        if ex:
            example = ex.group(1).strip()
            rest = (rest[: ex.start()] + rest[ex.end():]).strip(" .\u2014-")
        elif rest.lower().startswith("example"):
            rest = ""
        if not example:
            before = text[max(0, m.start() - 700): m.start()]
            sents = SENT.findall(before)
            if sents and re.search(r"<b>\s*" + re.escape(word) + r"\s*</b>", sents[-1], re.I):
                cand = re.sub(r"^\d+\.\s*", "", clean(sents[-1]))
                if "?" not in cand and "_" not in cand:
                    example = cand
        yield word, pos, rest, example
    # series lessons keep their items in `var LESSON=[['id','front','meaning','emoji'], ...]`
    ls = re.search(r"var LESSON\s*=\s*\[(.*?)\n\s*\];", text, re.S)
    if ls:
        for r in re.finditer(r"\[\s*(['\"])(.*?)\1\s*,\s*(['\"])(.*?)\3\s*,\s*(['\"])(.*?)\5", ls.group(1)):
            front = re.split(r"\s+/\s+", r.group(4))[0].replace("\u2026", "").replace("...", "").strip(" ?!.")
            yield front, "", clean(r.group(6)), ""
    for chunk in text.split('class="vocab-card')[1:]:
        f = {k: (clean(r.search(chunk).group(1)) if r.search(chunk) else "") for k, r in CARD_FIELD.items()}
        if f["word"]:
            yield f["word"], POS.get(f["pos"].lower(), f["pos"]), f["def"], f["ex"].strip("\"\u201c\u201d ")


def parse_lesson(path):
    stem = os.path.basename(path)[:-5]
    text = open(path, encoding="utf-8").read()
    t = re.search(r"<title>([^<]*)", text)
    title = clean(t.group(1)).split("\u00b7")[0].strip() if t else stem
    ln = re.search(r'var LESSON_NAME\s*=\s*["\'](.+?)["\']', text)
    if ln and stem.startswith("a1s_"):
        title = "Mia \u2014 " + clean(ln.group(1))
    words, seen = [], set()
    for word, pos, rest, example in entries(text):
        w = norm_word(word)
        if re.match(r"^(is the odd one out|/)", rest) or not w or w in seen or not (rest or example):
            continue
        seen.add(w)
        words.append({"w": w, "pos": pos, "def": rest.rstrip(), "ex": example})
    return {"id": stem, "title": title, "level": level_of(stem), "words": words}


def inject_dashboards(registered):
    """Add the 'Open My Words' bar to dashboards that link to registered lessons."""
    n = 0
    for f in glob.glob(os.path.join(ROOT, "*dashboard*.html")):
        t = open(f, encoding="utf-8").read()
        tag = '<script src="wordbank/hook.js" data-page="dashboard"></script>'
        if tag in t or "</body>" not in t:
            continue
        ids = {l[:-5] for l in re.findall(r'href="([^"#?]+\.html)', t) if not l.startswith("http")}
        if ids & registered:
            open(f, "w", encoding="utf-8").write(t.replace("</body>", tag + "\n</body>", 1))
            n += 1
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    inject = "--inject" in sys.argv
    globs = args or DEFAULT_GLOBS
    if "--auto" in sys.argv:
        files = sorted(f for f in glob.glob(os.path.join(ROOT, "*.html"))
                       if any(k in open(f, encoding="utf-8", errors="ignore").read() for k in ('class="meaning"', 'class="vocab-card', 'var LESSON=[')))
    else:
        files = sorted({f for g in globs for f in glob.glob(os.path.join(ROOT, g))})
    files = [f for f in files if "dashboard" not in f and not re.search(r" \(\d+\)\.html$", f)]
    lessons, bank = [], {}
    for f in files:
        les = parse_lesson(f)
        if len(les["words"]) < 3:
            continue
        ids = []
        for x in les["words"]:
            cur = bank.get(x["w"])
            if cur is None:
                bank[x["w"]] = {**x, "lessons": [les["id"]]}
            else:
                if les["id"] not in cur["lessons"]:
                    cur["lessons"].append(les["id"])
                for k in ("pos", "def", "ex"):
                    if len(x[k]) > len(cur[k]) and (k != "def" or not cur[k]):
                        cur[k] = x[k]
            if x["w"] not in ids:
                ids.append(x["w"])
        lessons.append({"id": les["id"], "title": les["title"], "level": les["level"], "words": ids})
        if inject:
            s = open(f, encoding="utf-8").read()
            if HOOK not in s and "</body>" in s:
                open(f, "w", encoding="utf-8").write(s.replace("</body>", HOOK + "\n</body>", 1))
    if inject:
        print(inject_dashboards({l["id"] for l in lessons}), "dashboards given the My Words bar")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    data = {"lessons": lessons, "words": bank}
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("window.WORDBANK=" + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    with open(os.path.join(os.path.dirname(OUT), "lessons.js"), "w", encoding="utf-8") as fh:
        fh.write("window.WBLESSONS=" + json.dumps({l["id"]: len(l["words"]) for l in lessons}, separators=(",", ":")) + ";\n")
    print(f"{len(lessons)} lessons, {len(bank)} unique words -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
