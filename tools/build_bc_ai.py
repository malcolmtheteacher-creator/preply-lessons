#!/usr/bin/env python3
"""One-off Bet the Company C1 lesson on the Think-Inside-the-Box engine (navy).
tools/bc_ai_content/<slug>.json -> bc_<slug>_c1.html"""
import json, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_end as E
E.SERIES = "Bet the Company"
for p in sorted(glob.glob(os.path.join(E.HERE, "bc_ai_content", "*.json"))):
    d = json.load(open(p)); E.check(d)
    h = E.lesson(d, [d])
    h = h.replace(f'BEGIN WITH THE END · {d["num"]} OF 3 · C1 · 50 min', 'BET THE COMPANY · C1 · 50 min')
    h = h.replace(f'<a href="{E.DASH}">The whole pathway</a>', '<a href="bet_the_company_dashboard.html">All the cases</a>')
    out = os.path.join(E.ROOT, f'bc_{d["slug"]}_c1.html'); open(out, "w").write(h)
    print("wrote", out, len(h)//1024, "KB")
