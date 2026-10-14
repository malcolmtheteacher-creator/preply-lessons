#!/usr/bin/env python3
"""Build the IELTS Route page (ielts_route.html) and the Start-here page
(ielts_start_here.html) from tools/ielts_route_data.py.

Usage: python3 tools/build_ielts_route.py
"""
import math, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ielts_route_data as D

COLORS = {"s1": "#0e7490", "s2": "#2563eb", "s3": "#7c3aed", "s4": "#d97706", "s5": "#dc2626"}
NAVY = "#1f3a5f"
E = html.escape


def check_files():
    missing = []
    def chk(f):
        p = f.split("#")[0]
        if p in ("ielts_start_here.html", "ielts_route.html"):
            return
        if p and not p.startswith("#") and not os.path.exists(os.path.join(ROOT, p)):
            missing.append(p)
    for s in D.STAGES:
        for g in s["groups"]:
            for st in g["steps"]:
                chk(st["f"])
    for it in D.SIDE["items"]:
        chk(it["f"])
    for leaves in D.MAP_LEAVES.values():
        for _, tgt in leaves:
            if not tgt.startswith("#"):
                chk(tgt)
    if missing:
        raise SystemExit("MISSING FILES: " + ", ".join(sorted(set(missing))))


# ---------------------------------------------------------------- mind map
def pill(x, y, w, label, target, color):
    h = 30
    return (f'<a class="leaf" href="{E(target)}"><title>{E(label)}</title>'
            f'<rect x="{x}" y="{y - h/2}" width="{w}" height="{h}" rx="15" fill="#ffffff" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x + w/2}" y="{y + 4.5}" text-anchor="middle" font-size="13" font-weight="600" fill="#1c2b3a">{E(label)}</text></a>')


def mind_map():
    cx, cy, R = 600, 440, 215
    angles = {"s1": -90, "s2": -18, "s3": 54, "s4": 126, "s5": 198}
    pos = {k: (cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for k, a in angles.items()}
    out = []
    out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker></defs>')
    # ring arrows (clockwise) between consecutive stages
    keys = list(angles)
    for i, k in enumerate(keys[:-1]):
        a1 = math.radians(angles[k] + 25)
        a2 = math.radians(angles[keys[i + 1]] - 25)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        x2, y2 = cx + R * math.cos(a2), cy + R * math.sin(a2)
        out.append(f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="#64748b" stroke-width="3" marker-end="url(#arr)"/>')
    # spokes hub -> stage
    for k, (x, y) in pos.items():
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4 6"/>')
    # leaves
    placement = {}
    placement["s1"] = [(450, 92, 300)]
    n = len(D.MAP_LEAVES["s2"]); placement["s2"] = [(935, pos["s2"][1] + (i - (n - 1) / 2) * 38, 235) for i in range(n)]
    n = len(D.MAP_LEAVES["s3"]); placement["s3"] = [(935, 530 + i * 38, 235) for i in range(n)]
    n = len(D.MAP_LEAVES["s4"]); placement["s4"] = [(30, pos["s4"][1] + (i - (n - 1) / 2) * 38 + 20, 235) for i in range(n)]
    n = len(D.MAP_LEAVES["s5"]); placement["s5"] = [(30, pos["s5"][1] + (i - (n - 1) / 2) * 38 - 10, 235) for i in range(n)]
    for k, spots in placement.items():
        sx, sy = pos[k]
        col = COLORS[k]
        for (x, y, w), (label, tgt) in zip(spots, D.MAP_LEAVES[k]):
            if x > cx:
                ex, ey = x, y
            elif x + w < cx:
                ex, ey = x + w, y
            else:
                ex, ey = x + w / 2, y + 15
            out.append(f'<path d="M{sx:.1f},{sy:.1f} C{(sx+ex)/2:.1f},{sy:.1f} {(sx+ex)/2:.1f},{ey:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="{col}" stroke-width="1.6" opacity=".5"/>')
        for (x, y, w), (label, tgt) in zip(spots, D.MAP_LEAVES[k]):
            out.append(pill(x, y, w, label, tgt, col))
    # hub
    out.append(f'<circle cx="{cx}" cy="{cy}" r="72" fill="{NAVY}"/>'
               f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">IELTS</text>'
               f'<text x="{cx}" y="{cy+22}" text-anchor="middle" font-size="15" font-weight="600" fill="#cfe0f5">your route</text>')
    # stage nodes
    for s in D.STAGES:
        k = s["id"]; x, y = pos[k]; col = COLORS[k]
        out.append(f'<a class="stage" href="#{k}"><title>Stage {s["num"]}: {E(s["name"])}</title>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="52" fill="{col}"/>'
                   f'<text x="{x:.1f}" y="{y-6:.1f}" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">{s["num"]}</text>'
                   f'<text x="{x:.1f}" y="{y+16:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{E(s["short"])}</text></a>')
    # keep-running rail
    out.append(f'<text x="{cx}" y="792" text-anchor="middle" font-size="14" font-weight="700" fill="#475569">Keep these running all the way through</text>')
    side = [("Example bank", "ielts_stories_history_pathway.html"), ("Word Wall", "ielts_wordwall_dashboard.html"),
            ("Spelling Stories", "ielts_spelling_stories_dashboard.html"), ("Essay Bestiary", "bestiary_ielts_phrases.html")]
    w = 185; gap = 18; total = len(side) * w + (len(side) - 1) * gap; x0 = cx - total / 2
    for i, (lab, tgt) in enumerate(side):
        out.append(pill(x0 + i * (w + gap), 830, w, lab, tgt, "#64748b"))
    return ('<svg viewBox="0 0 1200 870" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Map of the IELTS route: five stages, each with clickable lessons">' + "".join(out) + '</svg>')


# ---------------------------------------------------------------- route page
def step_html(sid, gi, si, st):
    key = f"{sid}-{gi}-{si}"
    star = '<span class="star" title="Band 7 and above">★ Band 7+</span>' if st.get("star") else ""
    return (f'<li class="step"><label class="tick"><input type="checkbox" data-k="{key}" aria-label="Done: {E(st["t"])}"><span></span></label>'
            f'<a class="step-body" href="{E(st["f"])}"><span class="step-t">{E(st["t"])} {star}</span>'
            f'<span class="step-d">{E(st["d"])}</span></a></li>')


def route_page():
    stages = []
    for s in D.STAGES:
        col = COLORS[s["id"]]
        groups = []
        for gi, g in enumerate(s["groups"]):
            steps = "\n".join(step_html(s["id"], gi, si, st) for si, st in enumerate(g["steps"]))
            groups.append(f'<div class="group" id="{g["id"]}"><h3>{E(g["title"])}</h3><ol class="steps">\n{steps}\n</ol></div>')
        stages.append(f'''<section class="stage-sec" id="{s["id"]}" style="--c:{col}">
  <div class="stage-head"><span class="num">{s["num"]}</span><div><h2>{E(s["name"])}</h2><div class="weeks">{E(s["weeks"])}</div></div></div>
  <p class="blurb">{E(s["blurb"])}</p>
  {"".join(groups)}
</section>''')
    side_items = "\n".join(
        f'<a class="side-card" href="{E(it["f"])}"><b>{E(it["t"])}</b><span>{E(it["d"])}</span></a>' for it in D.SIDE["items"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="IELTS Route">
<title>The IELTS Route · B2–C1 English</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background:#f6f8fb; color:#1c2b3a; line-height:1.6; }}
.container {{ max-width: 1040px; margin: 0 auto; padding: 20px 16px 60px; }}
header {{ background: linear-gradient(135deg, {NAVY}, #2f5d8f); color:#fff; border-radius:14px; text-align:center; padding:44px 24px 38px; margin-bottom:24px; box-shadow:0 10px 30px rgba(31,58,95,.25); }}
header .tag {{ display:inline-block; padding:5px 15px; background:rgba(255,255,255,.18); border-radius:14px; font-size:.78rem; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }}
header h1 {{ font-size:2.6rem; line-height:1.15; margin-bottom:12px; }}
header p {{ font-size:1.1rem; max-width:680px; margin:0 auto; opacity:.96; }}
.back {{ display:inline-block; margin-bottom:12px; color:{NAVY}; font-weight:600; text-decoration:none; font-size:.92rem; }}
.intro {{ background:#fff; border:1px solid #dde4ee; border-left:4px solid {NAVY}; border-radius:12px; padding:22px 26px; margin-bottom:24px; }}
.intro p {{ margin-bottom:10px; color:#33445a; }} .intro p:last-child {{ margin-bottom:0; }}
.cta {{ display:flex; align-items:center; justify-content:space-between; gap:14px; background:linear-gradient(135deg,#0e7490,#155e75); color:#fff; text-decoration:none; border-radius:12px; padding:18px 24px; margin-bottom:28px; box-shadow:0 6px 18px rgba(14,116,144,.25); }}
.cta b {{ font-size:1.15rem; display:block; }} .cta span {{ font-size:.95rem; opacity:.95; }} .cta i {{ font-style:normal; font-size:1.4rem; font-weight:700; }}
.section-label {{ font-size:.82rem; letter-spacing:.14em; text-transform:uppercase; color:{NAVY}; font-weight:800; margin:8px 0 12px 4px; }}
.map {{ background:#fff; border:1px solid #dde4ee; border-radius:14px; padding:12px; margin-bottom:10px; box-shadow:0 2px 10px rgba(0,0,0,.04); }}
.map svg {{ display:block; width:100%; height:auto; font-family:inherit; }}
.map a {{ cursor:pointer; }} .map .leaf:hover rect {{ fill:#fff3d6; }} .map .stage:hover circle {{ filter:brightness(1.12); }}
.map-note {{ text-align:center; font-size:.92rem; color:#51637a; margin-bottom:26px; }}
.map-narrow {{ display:none; }}
.stage-sec {{ background:#fff; border:1px solid #dde4ee; border-top:6px solid var(--c); border-radius:14px; padding:22px 26px 14px; margin-bottom:22px; scroll-margin-top:12px; }}
.stage-head {{ display:flex; align-items:center; gap:16px; margin-bottom:8px; }}
.stage-head .num {{ width:48px; height:48px; border-radius:50%; background:var(--c); color:#fff; font-size:1.5rem; font-weight:800; display:flex; align-items:center; justify-content:center; flex:0 0 auto; }}
.stage-head h2 {{ font-size:1.6rem; line-height:1.15; color:#12202f; }} .weeks {{ color:var(--c); font-weight:700; font-size:.92rem; }}
.blurb {{ color:#44566c; margin-bottom:14px; }}
.group {{ margin-bottom:18px; scroll-margin-top:12px; }}
.group h3 {{ font-size:1rem; color:var(--c); margin:6px 0 8px; text-transform:uppercase; letter-spacing:.06em; }}
.steps {{ list-style:none; }}
.step {{ display:flex; align-items:stretch; gap:10px; margin-bottom:8px; }}
.tick {{ flex:0 0 auto; display:flex; align-items:center; padding-left:2px; cursor:pointer; }}
.tick input {{ position:absolute; opacity:0; }}
.tick span {{ width:24px; height:24px; border:2px solid #b8c4d4; border-radius:50%; display:block; background:#fff; }}
.tick input:checked + span {{ background:var(--c); border-color:var(--c); box-shadow:inset 0 0 0 4px #fff; }}
.tick input:focus-visible + span {{ outline:3px solid #f59e0b; outline-offset:2px; }}
.step-body {{ flex:1; display:block; text-decoration:none; color:inherit; background:#f6f8fb; border:1px solid #e3e9f1; border-radius:10px; padding:10px 16px; }}
.step-body:hover {{ border-color:var(--c); background:#fff; box-shadow:0 2px 10px rgba(0,0,0,.06); }}
.step-t {{ display:block; font-weight:700; color:#12202f; }}
.step-d {{ display:block; font-size:.93rem; color:#52647a; }}
.star {{ display:inline-block; margin-left:6px; font-size:.72rem; font-weight:700; color:#92400e; background:#fef3c7; border:1px solid #fcd34d; border-radius:10px; padding:1px 8px; vertical-align:middle; }}
.side {{ background:#fff; border:1px solid #dde4ee; border-top:6px solid #64748b; border-radius:14px; padding:22px 26px; margin-bottom:22px; }}
.side h2 {{ font-size:1.4rem; margin-bottom:4px; }} .side p {{ color:#44566c; margin-bottom:14px; }}
.side-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
.side-card {{ display:block; text-decoration:none; color:inherit; background:#f6f8fb; border:1px solid #e3e9f1; border-radius:10px; padding:12px 16px; }}
.side-card:hover {{ border-color:#64748b; background:#fff; }} .side-card b {{ display:block; color:#12202f; }} .side-card span {{ font-size:.9rem; color:#52647a; }}
.all {{ text-align:center; margin:22px 0; font-size:.95rem; color:#51637a; }} .all a {{ color:{NAVY}; font-weight:700; }}
.progress {{ text-align:center; color:#51637a; font-size:.92rem; margin:-4px 0 16px; }}
footer {{ text-align:center; color:#6b7c93; font-size:.9rem; margin-top:30px; }}
@media (max-width: 720px) {{
  header h1 {{ font-size:2rem; }}
  .map-wide {{ display:none; }} .map-narrow {{ display:block; text-align:center; color:#51637a; padding:12px; }}
  .stage-sec {{ padding:18px 16px 10px; }}
}}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="malcolm_lesson_index.html">&larr; All lessons</a>
  <header>
    <span class="tag">IELTS &middot; Academic &middot; Bands 6 to 7.5+</span>
    <h1>The IELTS Route</h1>
    <p>One path from your first diagnostic to your last mock. Follow the stages in order — every lesson is chosen and placed for you.</p>
  </header>

  <div class="intro">
    <p><strong>How it works.</strong> The route has five stages. Stage 1 finds your starting point. Stages 2 to 5 build, test and finish your skills, with a different mix each week. Every step below is a lesson or practice page — click it, do it, tick it off.</p>
    <p><strong>A good week</strong> is one writing step, one speaking step, one reading or listening step, and ten minutes on the side lessons at the bottom. Steps marked <span class="star">★ Band 7+</span> are for stretching beyond the core; everything else is for every student.</p>
    <p>The whole route fits twelve weeks, but it moves at your pace. If your test is sooner, do Stage 1, then spend your time on the skills where your diagnostic was lowest.</p>
  </div>

  <a class="cta" href="ielts_start_here.html"><div><b>Not sure where to begin? Start here.</b><span>The test at a glance, the marking criteria in plain English, and a diagnostic to find your starting band.</span></div><i>&rarr;</i></a>

  <p class="section-label">The route map &mdash; click any stage or lesson</p>
  <div class="map">
    <div class="map-wide">{mind_map()}</div>
    <div class="map-narrow">The route map is best on a larger screen. On a phone, follow the stages below.</div>
  </div>
  <p class="map-note">Five stages, clockwise from the top. Stage 3 opens into six tracks — click a track to jump to its lessons.</p>
  <p class="progress" id="progress"></p>

{chr(10).join(stages)}

  <section class="side" id="side">
    <h2>{E(D.SIDE["title"])}</h2>
    <p>{E(D.SIDE["blurb"])}</p>
    <div class="side-grid">
{side_items}
    </div>
  </section>

  <p class="all">Looking for something specific? <a href="malcolm_lesson_index.html">Search the whole library</a> &middot; <a href="ielts_start_here.html">Start here</a></p>
  <footer>The IELTS Route &middot; Academic</footer>
</div>
<script>
(function() {{
  var boxes = document.querySelectorAll('.tick input');
  var saved = {{}};
  try {{ saved = JSON.parse(localStorage.getItem('ielts_route_done') || '{{}}'); }} catch (e) {{ saved = {{}}; }}
  function save() {{ try {{ localStorage.setItem('ielts_route_done', JSON.stringify(saved)); }} catch (e) {{}} }}
  function count() {{
    var n = 0; boxes.forEach(function(b) {{ if (b.checked) n++; }});
    document.getElementById('progress').textContent = n ? ('Steps done on this device: ' + n + ' of ' + boxes.length) : '';
  }}
  boxes.forEach(function(b) {{
    if (saved[b.dataset.k]) b.checked = true;
    b.addEventListener('change', function() {{ if (b.checked) saved[b.dataset.k] = 1; else delete saved[b.dataset.k]; save(); count(); }});
  }});
  count();
}})();
</script>
</body>
</html>
'''


# ---------------------------------------------------------------- start-here page
def start_page():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="IELTS Route">
<title>Start Here: The Test and Your Diagnostic · B2–C1 English</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background:#f6f8fb; color:#1c2b3a; line-height:1.6; }}
.container {{ max-width: 920px; margin: 0 auto; padding: 20px 16px 60px; }}
header {{ background: linear-gradient(135deg, #0e7490, #155e75); color:#fff; border-radius:14px; text-align:center; padding:40px 24px 34px; margin-bottom:24px; }}
header .tag {{ display:inline-block; padding:5px 15px; background:rgba(255,255,255,.18); border-radius:14px; font-size:.78rem; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }}
header h1 {{ font-size:2.4rem; line-height:1.15; margin-bottom:10px; }} header p {{ font-size:1.08rem; max-width:640px; margin:0 auto; opacity:.96; }}
.back {{ display:inline-block; margin-bottom:12px; color:{NAVY}; font-weight:600; text-decoration:none; font-size:.92rem; }}
.card {{ background:#fff; border:1px solid #dde4ee; border-radius:14px; padding:24px 28px; margin-bottom:22px; }}
.card h2 {{ font-size:1.5rem; color:#12202f; margin-bottom:10px; }} .card h3 {{ font-size:1.05rem; color:#155e75; margin:14px 0 6px; }}
.card p {{ color:#33445a; margin-bottom:10px; }} .card ul {{ margin:0 0 10px 22px; color:#33445a; }} .card li {{ margin-bottom:5px; }}
table {{ width:100%; border-collapse:collapse; margin:8px 0 12px; font-size:.97rem; }}
th, td {{ text-align:left; padding:9px 12px; border-bottom:1px solid #e3e9f1; vertical-align:top; }}
th {{ background:#eef4f8; color:#12202f; }}
.step {{ display:flex; gap:14px; align-items:flex-start; margin-bottom:14px; }}
.step .n {{ flex:0 0 34px; height:34px; border-radius:50%; background:#0e7490; color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; }}
.btn {{ display:inline-block; margin-top:4px; background:#0e7490; color:#fff; text-decoration:none; font-weight:700; padding:8px 18px; border-radius:10px; }}
.btn:hover {{ background:#155e75; }}
.who {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; margin:12px 0; }}
.who label {{ display:block; font-weight:700; color:#12202f; font-size:.95rem; }}
.who select {{ width:100%; margin-top:4px; padding:9px 10px; border:1px solid #b8c4d4; border-radius:8px; font-size:1rem; background:#fff; }}
.result {{ display:none; margin-top:14px; background:#ecfeff; border:1px solid #67e8f9; border-left:5px solid #0e7490; border-radius:10px; padding:14px 18px; }}
.result.show {{ display:block; }} .result a {{ color:#155e75; font-weight:700; }}
.logtbl td {{ font-size:.94rem; }}
.go {{ display:block; text-align:center; text-decoration:none; background:{NAVY}; color:#fff; font-weight:700; font-size:1.1rem; padding:16px; border-radius:12px; margin-bottom:22px; }}
.go:hover {{ background:#2f5d8f; }}
footer {{ text-align:center; color:#6b7c93; font-size:.9rem; margin-top:26px; }}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="ielts_route.html">&larr; The IELTS Route</a>
  <header>
    <span class="tag">IELTS &middot; Stage 1</span>
    <h1>Start Here</h1>
    <p>What the test asks of you, what the examiners score, and three tasks that show you where you stand today.</p>
  </header>

  <div class="card">
    <h2>The test at a glance</h2>
    <table>
      <tr><th>Part</th><th>Time</th><th>What you do</th></tr>
      <tr><td><b>Listening</b></td><td>About 30 minutes</td><td>Four recordings, 40 questions. You hear each recording once.</td></tr>
      <tr><td><b>Reading</b></td><td>60 minutes</td><td>Three long texts, 40 questions. No extra time to copy answers.</td></tr>
      <tr><td><b>Writing</b></td><td>60 minutes</td><td>Task 1: describe a graph, chart, map or process (at least 150 words, about 20 minutes). Task 2: an essay (at least 250 words, about 40 minutes). <b>Task 2 counts for twice as much as Task 1.</b></td></tr>
      <tr><td><b>Speaking</b></td><td>11 to 14 minutes</td><td>A live conversation with an examiner: Part 1 (familiar topics), Part 2 (a two-minute talk), Part 3 (a deeper discussion).</td></tr>
    </table>
    <p>Each part gets a band from 0 to 9. Your overall band is the average of the four, rounded to the nearest half band. This route is for the <b>Academic</b> test, where Reading and Writing use academic texts and tasks; Listening and Speaking are the same in both versions. Check with your test centre whether you will sit the test on paper or on a computer.</p>
  </div>

  <div class="card">
    <h2>What the examiners score</h2>
    <p>Listening and Reading are marked by counting correct answers. Writing and Speaking are marked by an examiner on four criteria each. If you know them, you know what to practise.</p>
    <h3>Writing — four criteria, each worth a quarter</h3>
    <ul>
      <li><b>Task Achievement / Task Response</b> — did you answer the question that was asked, fully, with a clear position and developed ideas?</li>
      <li><b>Coherence and Cohesion</b> — is it organised into clear paragraphs, with ideas that connect?</li>
      <li><b>Lexical Resource</b> — a wide range of accurate vocabulary, used naturally, spelled correctly.</li>
      <li><b>Grammatical Range and Accuracy</b> — a mix of simple and complex sentences, mostly accurate.</li>
    </ul>
    <h3>Speaking — four criteria, each worth a quarter</h3>
    <ul>
      <li><b>Fluency and Coherence</b> — speaking at length without long pauses, and organising what you say.</li>
      <li><b>Lexical Resource</b> — a range of vocabulary and the ability to paraphrase.</li>
      <li><b>Grammatical Range and Accuracy</b> — a mix of structures, with few errors that block meaning.</li>
      <li><b>Pronunciation</b> — clear sounds, stress and intonation that a listener can follow easily.</li>
    </ul>
    <p>Want these in detail, with weak and strong paragraphs side by side? Do <a href="ielts_lesson_2_marking_criteria.html" style="color:#155e75;font-weight:700;">What Examiners Count</a> next.</p>
  </div>

  <div class="card">
    <h2>Your diagnostic: three timed tasks</h2>
    <p>Do these in one sitting if you can, or across two days. Be strict with the clock — an untimed attempt hides the real problem. Do not look anything up. Afterwards, note your estimate for each part in the box below.</p>
    <div class="step"><div class="n">1</div><div><b>Reading — a full test, 60 minutes, no pausing.</b><br>Mark it, then count your correct answers out of 40.<br><a class="btn" href="IELTS-Reading-Practice-Test-1.html">Open Reading Test 1</a></div></div>
    <div class="step"><div class="n">2</div><div><b>Writing — one Task 2 essay, 40 minutes.</b><br>Use the exam-mode page: one real question, a timer and a word counter, with no help on screen.<br><a class="btn" href="essay_practice_opinion_3.html">Open the essay task</a></div></div>
    <div class="step"><div class="n">3</div><div><b>Speaking — record yourself.</b><br>Run a mock test on the simulator: record Parts 1, 2 and 3 on your phone, then listen back. Where did you stop, repeat or run out of ideas?<br><a class="btn" href="tools/speaking-practice.html">Open the speaking simulator</a></div></div>
    <p><b>Listening:</b> try one lesson from the <a href="listening-lessons.html" style="color:#155e75;font-weight:700;">listening set</a> and count how many questions you answer correctly.</p>
  </div>

  <div class="card">
    <h2>Where should you focus?</h2>
    <p>Choose your honest estimate for each part (half bands are fine to round). If you are not sure, choose the lower band.</p>
    <div class="who">
      <div><label for="b-li">Listening</label><select id="b-li"></select></div>
      <div><label for="b-rd">Reading</label><select id="b-rd"></select></div>
      <div><label for="b-wr">Writing</label><select id="b-wr"></select></div>
      <div><label for="b-sp">Speaking</label><select id="b-sp"></select></div>
      <div><label for="b-tg">Your target overall</label><select id="b-tg"></select></div>
    </div>
    <button class="btn" id="go" style="border:0;cursor:pointer;font-size:1rem;">Show me where to start</button>
    <div class="result" id="result" aria-live="polite"></div>
  </div>

  <div class="card">
    <h2>Keep an error log</h2>
    <p>A correct answer does not prove you have learned something; a repeated mistake does prove you have not. From today, every time you get something wrong, write one line:</p>
    <table class="logtbl">
      <tr><th>The mistake</th><th>Why it happened</th><th>The fix</th></tr>
      <tr><td>The graph <i>show</i> a rise</td><td>Forgot the &ndash;s with a singular subject</td><td>The graph <b>shows</b> a rise</td></tr>
      <tr><td>Wrote 190 words in Task 2</td><td>Spent 15 minutes planning</td><td>Plan for 5 minutes; write for 30</td></tr>
      <tr><td>Missed a True/False/Not Given answer</td><td>Used my own opinion, not the text</td><td>Find the exact sentence first</td></tr>
    </table>
    <p>Read your log before every practice session. By the time you reach the mock tests, it will be the most useful page you own.</p>
  </div>

  <div class="card">
    <h2>A good week</h2>
    <ul>
      <li>One <b>writing</b> step (a Task 2 essay type or a Task 1 lesson)</li>
      <li>One <b>speaking</b> step, with a recording you listen to</li>
      <li>One <b>reading or listening</b> step, timed</li>
      <li>Ten minutes of vocabulary or spelling — the side lessons at the end of the route</li>
      <li>Five minutes with your error log</li>
    </ul>
  </div>

  <a class="go" href="ielts_route.html">Go to the IELTS Route &rarr;</a>
  <footer>The IELTS Route &middot; Stage 1</footer>
</div>
<script>
(function() {{
  var bands = ['4','4.5','5','5.5','6','6.5','7','7.5','8','8.5','9'];
  ['b-li','b-rd','b-wr','b-sp','b-tg'].forEach(function(id) {{
    var s = document.getElementById(id);
    var first = document.createElement('option'); first.value = ''; first.textContent = 'Choose…'; s.appendChild(first);
    bands.forEach(function(b) {{ var o = document.createElement('option'); o.value = b; o.textContent = b; s.appendChild(o); }});
  }});
  var tracks = {{
    li: ['Listening', 'ielts_route.html#track-li'],
    rd: ['Reading', 'ielts_route.html#track-rd'],
    wr: ['Writing', 'ielts_route.html#track-w2'],
    sp: ['Speaking', 'ielts_route.html#track-sp']
  }};
  document.getElementById('go').addEventListener('click', function() {{
    var res = document.getElementById('result');
    var vals = [], missing = false;
    ['li','rd','wr','sp'].forEach(function(k) {{
      var v = document.getElementById('b-' + k).value;
      if (!v) missing = true; else vals.push([k, parseFloat(v)]);
    }});
    if (missing) {{ res.className = 'result show'; res.innerHTML = 'Choose an estimate for all four parts first — a guess is fine.'; return; }}
    var sum = 0; vals.forEach(function(p) {{ sum += p[1]; }});
    var avg = Math.floor((sum / 4) * 2 + 0.5 + 1e-9) / 2;
    vals.sort(function(a, b) {{ return a[1] - b[1]; }});
    var lowest = vals.filter(function(p) {{ return p[1] === vals[0][1]; }});
    var tg = document.getElementById('b-tg').value;
    var html = 'Your estimated overall band is about <b>' + avg + '</b>';
    if (tg) html += ' and your target is <b>' + tg + '</b>' + (parseFloat(tg) > avg ? ' — a gap of ' + (parseFloat(tg) - avg) + ' to close.' : ' — you are already there on paper; the work now is making it reliable.');
    else html += '.';
    html += '<br><br>Your lowest part' + (lowest.length > 1 ? 's are ' : ' is ');
    html += lowest.map(function(p) {{ return '<a href="' + tracks[p[0]][1] + '">' + tracks[p[0]][0] + '</a>'; }}).join(' and ');
    html += '. Do Stage 2 (Foundations) first, then give ' + (lowest.length > 1 ? 'those tracks' : 'that track') + ' an extra step each week in Stage 3.';
    html += '<br><br><a href="ielts_route.html#s2">Start Stage 2: Foundations &rarr;</a>';
    res.className = 'result show'; res.innerHTML = html;
  }});
}})();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    check_files()
    open(os.path.join(ROOT, "ielts_route.html"), "w").write(route_page())
    open(os.path.join(ROOT, "ielts_start_here.html"), "w").write(start_page())
    print("wrote ielts_route.html, ielts_start_here.html")
