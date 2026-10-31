#!/usr/bin/env python3
"""Build explore_data.js for explore.html from the bot hooks (tools/interest/hooks.json)
plus the hand-checked pilot (tools/interest/pilot_clean.json). Lessons whose topics are NONE are left out.
Usage: python3 tools/build_explore.py"""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
d = json.loads(re.search(r'WBALL=(\{.*\});?', open('wordbank/all_lessons.js', encoding='utf-8').read(), re.S).group(1))
pilot = {c[0]: c for c in json.load(open('tools/interest/pilot_clean.json', encoding='utf-8'))}
hooks = json.load(open('tools/interest/hooks.json', encoding='utf-8'))
def clean(t):
    t = re.sub(r'^(Short History, Long Echoes|Short Stories, Long Shadows|Behind the Screen|Minds Worth Meeting|Curious Conversations\s*#?\d*\s*(Special)?):\s*', '', t)
    t = re.sub(r'\s*[-—]\s*(B1|B2|A2|C1)[^|]*(Lesson|English|Level|Professional English)?.*$', '', t)
    t = re.sub(r'^B[12]\s*(Lesson|\d+)?:\s*', '', t); t = re.sub(r'\s*\((A2/B1|simplified)\)$', '', t)
    return t.strip()
out = list(pilot.values())
for k, h in hooks.items():
    if k in pilot or k not in d or h['t'] == ['NONE'] or not os.path.exists(k + '.html'): continue
    t, lv, s = d[k]
    out.append([k, clean(t) or t, lv, h['t'], h['k'], h['h']])
out = [o for o in out if os.path.exists(o[0] + '.html')]
open('explore_data.js', 'w', encoding='utf-8').write('window.EXPLORE=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';')
print(len(out), 'lessons in explore_data.js')
