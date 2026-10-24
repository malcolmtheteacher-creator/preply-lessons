#!/usr/bin/env python3
"""Build the 'Say It Clearly' lessons (C1, 50 min each) from content files.

  tools/say_content/NN_<slug>.json  ->  say_<slug>_c1.html   (one lesson each)
  (all lessons)                     ->  say_it_clearly_dashboard.html

Reuses the Begin With the End builder (build_end.py), which itself sits on the
Think Inside the Box engine: same six tabs (Key Words, The Story, The Tool,
Language, Speak, Practice), same navy colours, so the two series sit together.
Only writes say_* files. Never touches end_* or the Begin With the End dashboard.
Usage: python3 tools/build_say.py
"""
import copy, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_end as BE  # noqa: E402
import build_tib as T  # noqa: E402

ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "say_content")
SERIES = "Say It Clearly"
DASH = "say_it_clearly_dashboard.html"

BE.SERIES, BE.DASH = SERIES, DASH


def lesson(d, lessons):
    h = BE.lesson(d, lessons)
    slugs = "|".join(x["slug"] for x in lessons)
    h = re.sub(rf'href="end_({slugs})_c1\.html"', r'href="say_\1_c1.html"', h)
    h = h.replace(f'BEGIN WITH THE END · {d["num"]} OF 3 · C1 · 50 min', f'SAY IT CLEARLY · LESSON {d["num"]} · C1 · 50 min')
    return h


def dashboard(lessons):
    cards = "\n".join(f'''        <a class="story-card" href="say_{d["slug"]}_c1.html">
            <div class="story-num">LESSON {d["num"]} &middot; {d["card"]["shape"]}</div>
            <div class="story-title">{d["title"]}</div>
            <div class="story-author">{d["card"]["who"]}</div>
            <div class="story-essence">{d["card"]["essence"]}</div>
            <div class="story-turn"><span>The tool:</span> {d["tool"]}</div>
            <div class="story-foot"><span class="grammar-tag">{d["grammar"]["name"]}</span><span class="go">Open &rarr;</span></div>
        </a>''' for d in lessons)
    css = BE.navy(T.recolour(re.search(r"<style>\n(.*?)</style>", open(os.path.join(ROOT, "true_science_stories_dashboard.html")).read(), re.S).group(1)))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="{SERIES}">
<title>Say It Clearly &middot; C1</title>
<style>
{css}
.flow {{ display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin: 6px 0 26px; }}
.flow .step {{ background:white; border:1px solid #cbdaee; border-radius:14px; padding:12px 18px; text-align:center; min-width:150px; box-shadow:0 2px 8px rgba(0,0,0,.04); }}
.flow .step b {{ display:block; color:#1b3a6b; font-size:1.05rem; }}
.flow .step span {{ font-size:.85rem; color:#556; }}
.flow .arrow {{ align-self:center; color:#1e4e8c; font-size:1.4rem; }}
.who {{ background:#f2f6fb; border-left:4px solid #1e4e8c; border-radius:0 12px 12px 0; padding:16px 22px; margin-bottom:26px; }}
.who h2 {{ font-size:1.1rem; color:#1b3a6b; margin-bottom:6px; }}
.who p {{ color:#3a3a4a; line-height:1.7; margin:0; }}
.nq-cta {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:14px; background:linear-gradient(135deg,#1e4e8c,#12284a); color:white; border-radius:14px; padding:20px 26px; margin-bottom:26px; text-decoration:none; }}
.nq-cta b {{ font-size:1.2rem; display:block; margin-bottom:2px; }}
.nq-cta span:first-child {{ flex:1 1 420px; line-height:1.5; }}
.nq-cta .nq-go {{ background:white; color:#1b3a6b; font-weight:700; padding:8px 18px; border-radius:18px; }}
</style>
</head>
<body>
<div class="container">
    <header style="padding:56px 26px; background: linear-gradient(135deg, #1e4e8c 0%, #12284a 100%);">
        <span class="tag">True stories &middot; professional speaking &middot; C1</span>
        <h1>Say It Clearly</h1>
        <p class="subtitle">Three moves that make what you say easy to hear: give the meaning, answer honestly, and say numbers so they stick.</p>
    </header>

    <div class="intro">
        <p>Clear speaking is mostly a matter of choosing what the listener needs to hear first. Each lesson here takes one real story, one tool, and a lot of speaking practice. The tools are small enough to use the same day: a one-sentence summary of what your data means, a three-part reply to a difficult question, and a way to say a figure so that it is remembered.</p>
        <p>The lessons stand alone, so take them in any order. They work best after <em>Begin With the End</em>, which teaches the habit of landing your point first.</p>
    </div>

    <div class="flow">
        <div class="step"><b>Mean it</b><span>finding &middot; so what &middot; now what</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Answer it</b><span>answer &middot; bridge &middot; message</span></div>
        <div class="arrow">&rarr;</div>
        <div class="step"><b>Count it</b><span>round &middot; compare &middot; mean</span></div>
    </div>

    <div class="who">
        <h2>Who it is for</h2>
        <p>Anyone who speaks English at work and already speaks it well: managers, specialists, people who present results, answer questions and are asked for numbers. No grammar from scratch; the language here is the language of clarity.</p>
    </div>

    <a class="nq-cta" href="begin_with_the_end_dashboard.html">
        <span><b>Start with the habit underneath</b>Before you can say it clearly, you need to know where you will land. Three lessons on landing a point, pausing instead of filling, and holding your position.</span>
        <span class="nq-go">Begin With the End &rarr;</span>
    </a>

    <p class="section-label">The lessons</p>
    <div class="story-grid">
{cards}
    </div>

    <div class="how">
        <h2>How each lesson works</h2>
        <div class="how-steps">
            <div class="how-step"><div class="n">1 &middot; Key Words</div><p>Ten words from the story, worked out before you read.</p></div>
            <div class="how-step"><div class="n">2 &middot; The Story</div><p>A true story in three parts, with a check and a talking point after each.</p></div>
            <div class="how-step"><div class="n">3 &middot; The Tool</div><p>A simple method, a chance to try it, and where it breaks.</p></div>
            <div class="how-step"><div class="n">4 &middot; Language</div><p>The grammar and phrases the tool needs.</p></div>
            <div class="how-step"><div class="n">5 &middot; Speak</div><p>Timed speaking tasks, then harder questions.</p></div>
            <div class="how-step"><div class="n">6 &middot; Practice</div><p>Question banks and worked examples to use again and again.</p></div>
        </div>
    </div>

    <footer>{SERIES} &middot; C1</footer>
</div>
</body>
</html>
'''


def check(d):
    c = copy.deepcopy(d)
    for x in c["tool_tab"]["cousins"]:
        if x.get("lesson", "").startswith("say_"):
            x.pop("lesson")  # built in the same run, so it may not exist yet
    BE.check(c)
    blob = json.dumps(d)
    for bad in ("Malcolm", "teacher", "Teacher", "student", "TEEP"):
        assert bad not in blob, f'{d["slug"]}: forbidden word {bad!r}'


def main():
    lessons = [json.load(open(p, encoding="utf8")) for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for d in lessons:
        check(d)
        out = os.path.join(ROOT, f'say_{d["slug"]}_c1.html')
        open(out, "w", encoding="utf8").write(lesson(d, lessons))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")
    open(os.path.join(ROOT, DASH), "w", encoding="utf8").write(dashboard(lessons))
    print(f"  wrote {DASH}")
    for d in lessons:
        for x in d["tool_tab"]["cousins"]:
            if x.get("lesson", "").startswith("say_"):
                assert os.path.exists(os.path.join(ROOT, x["lesson"])), x["lesson"]


if __name__ == "__main__":
    main()
