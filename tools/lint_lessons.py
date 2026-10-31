#!/usr/bin/env python3
"""Scan every top-level lesson page for problems a student would notice.
Usage: python3 tools/lint_lessons.py            (summary + report in tools/lint_report.txt)
Checks: broken local links/images, placeholder text, teacher/pedagogy wording shown to the student."""
import glob, html, os, re, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
FILES = sorted(f for f in glob.glob('*.html'))
EXIST = set(os.listdir('.')) | {d + '/' for d in os.listdir('.') if os.path.isdir(d)}
PLACE = re.compile(r'\[(?:add|insert|todo|your)[^\]]{0,60}\]|\bTODO\b|\bLorem ipsum\b|\bPLACEHOLDER\b|\bFIXME\b', re.I)
WALL = re.compile(r'\bTeacher:|\bMalcolm\b|\b(?:I Do|We Do|You Do)\b(?! it| you| they| we)|\bPause:|\bTEEP\b|\b[Yy]our teacher will\b|\b[Tt]alk to your teacher\b')
LINK = re.compile(r'(?:href|src)=["\']([^"\'#?]+)', re.I)
SKIP_LINK = ('http', 'mailto:', 'tel:', 'data:', 'javascript:', '//', 'sms:')
problems = collections.defaultdict(list)
for f in FILES:
    t = open(f, encoding='utf-8', errors='ignore').read()
    body = re.sub(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>', '', t, flags=re.S | re.I)
    for u in set(LINK.findall(body)):
        if u.startswith(SKIP_LINK) or '{' in u or '+' in u or '$' in u: continue
        p = os.path.normpath(u)
        if not os.path.exists(p): problems['broken link'].append((f, u))
    text = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    for m in PLACE.finditer(text): problems['placeholder'].append((f, m.group(0)))
    for m in WALL.finditer(text):
        if f.startswith(('dewey_palace_architecture', 'malcolm_lesson_index', 'journey_')): continue
        problems['4th wall'].append((f, m.group(0)))
lines = []
for k, v in sorted(problems.items(), key=lambda kv: -len(kv[1])):
    files = collections.Counter(f for f, _ in v)
    lines.append('== %s: %d hits in %d files' % (k, len(v), len(files)))
    for f, n in files.most_common(): lines.append('  %s (%d) e.g. %s' % (f, n, next(x for g, x in v if g == f)))
open('tools/lint_report.txt', 'w').write('\n'.join(lines))
print(len(FILES), 'files scanned')
for k, v in problems.items(): print(k, len(v), 'hits,', len({f for f, _ in v}), 'files')
