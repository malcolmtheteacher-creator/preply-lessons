#!/usr/bin/env python3
"""Register EVERY lesson in the lesson index with My Room.

Reads malcolm_lesson_index.html (the canonical lesson list), writes
wordbank/all_lessons.js (id -> [title, level, series]) and adds the small
wordbank/hook.js tag to each listed lesson page that lacks it, so opening any
lesson is recorded in the student's My Room (words optional).

Usage:  python3 tools/build_all_lessons.py            # write registry + inject
        python3 tools/build_all_lessons.py --dry-run  # just count
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = '<script src="wordbank/hook.js"></script>'
PAT = re.compile(r"\{ filename: '((?:[^'\\]|\\.)*)', title: '((?:[^'\\]|\\.)*)', level: '([^']*)', series: '((?:[^'\\]|\\.)*)', grammar: '(?:[^'\\]|\\.)*', duration: '[^']*', hub: (true|false), audience: '([^']*)'")


def unesc(s):
    return s.replace("\\'", "'").replace("\\\\", "\\")


def main():
    dry = "--dry-run" in sys.argv
    t = open(os.path.join(ROOT, "malcolm_lesson_index.html"), encoding="utf-8").read()
    reg, inj, skipped = {}, 0, 0
    for fn, title, level, series, hub, aud in PAT.findall(t):
        fn = unesc(fn)
        if hub == "true" or not fn.endswith(".html") or re.search(r" \(\d+\)\.html$", fn) or "/" in fn:
            continue
        path = os.path.join(ROOT, fn)
        if not os.path.exists(path):
            skipped += 1
            continue
        reg[fn[:-5]] = [unesc(title), level, unesc(series)]
        s = open(path, encoding="utf-8", errors="surrogateescape", newline="").read()
        if "wordbank/hook.js" in s:
            continue
        i = s.lower().rfind("</body>")
        nl = "\r\n" if "\r\n" in s else "\n"
        new = s[:i] + HOOK + nl + s[i:] if i >= 0 else s + nl + HOOK + nl
        if not dry:
            open(path, "w", encoding="utf-8", errors="surrogateescape", newline="").write(new)
        inj += 1
    if not dry:
        open(os.path.join(ROOT, "wordbank", "all_lessons.js"), "w", encoding="utf-8").write(
            "window.WBALL=" + json.dumps(reg, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print("%d lessons registered, %d pages given the hook, %d listed files missing" % (len(reg), inj, skipped))


if __name__ == "__main__":
    main()
