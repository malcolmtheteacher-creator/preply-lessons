#!/usr/bin/env python3
"""Build a standalone lesson (not part of the tib series) from a content file.

  tools/standalone_content/<slug>.json  ->  <slug>.html

Five tabs: Warm-up / The Story / Grammar / Going Deeper / Your Turn to Talk.
Page style comes from ts_penicillin_b2.html (the purple house style); the
section renderers are shared with build_tib.py so the checks stay identical.
Usage: python3 tools/build_standalone.py [slug ...]   (no args = build all)
"""
import json, os, re, sys, glob
import build_tib as B

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "standalone_content")

# the un-recoloured house style (purple), plus the few extras the tib CSS adds
CSS = re.search(r"<style>\n(.*?)</style>", B.TEMPLATE, re.S).group(1) + """
.steps { margin: 6px 0 14px 22px; color:#3a3a4a; }
.steps li { margin-bottom: 8px; }
.pair { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:12px; margin:12px 0; }
.pair > div { background:#f6f4fc; border:1px solid #d8d2ea; border-radius:10px; padding:12px 16px; font-size:.95rem; color:#3a3a4a; }
.pair b { color:#5a3aa0; display:block; margin-bottom:4px; }
"""
JS = re.search(r"<script>\n(.*?)</script>", B.TEMPLATE, re.S).group(1)


def deeper(d):
    out = [f'            <h2>{d["heading"]}</h2>', f'            <p>{d["lead"]}</p>']
    for blk in d["blocks"]:
        out.append(f'            <h3>{blk["heading"]}</h3>')
        out.extend(f'            <p>{p}</p>' for p in blk.get("paras", []))
        if blk.get("pairs"):
            cells = "".join(f'                <div><b>{p["a"]}</b>{p["b"]}</div>\n' for p in blk["pairs"])
            out.append(f'            <div class="pair">\n{cells}            </div>')
        if blk.get("items"):
            rows = "\n".join(f"                <p>{i}. {x['q']}</p>" for i, x in enumerate(blk["items"], 1))
            ans = "\n".join(f"                    <p><strong>{i}.</strong> {x['a']}</p>" for i, x in enumerate(blk["items"], 1))
            out.append(f'''            <div class="gap-fill">
{rows}
                {B.REVEAL.format("Reveal")}
                <div class="answers">
{ans}
                </div>
            </div>''')
    out.append(f'''            <div class="discuss">
                <strong>Talk it through:</strong>
                <ul>
{B.ul(d["discuss"])}
                </ul>
            </div>''')
    return "\n".join(out)


def build(d):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d["title"]} | {d["level"]}</title>
<style>
{CSS}</style>
</head>
<body>
<div class="container">
    <header>
        <span class="tag">{d["tag"]}</span>
        <h1>{d["h1"]}</h1>
        <p>{d["subtitle"]}</p>
    </header>

    <nav class="tab-nav">
        <button class="tab-btn active" onclick="showTab(0)">1. Warm-up</button>
        <button class="tab-btn" onclick="showTab(1)">2. The Story</button>
        <button class="tab-btn" onclick="showTab(2)">3. {d["grammar"]["name"]}</button>
        <button class="tab-btn" onclick="showTab(3)">4. Going Deeper</button>
        <button class="tab-btn" onclick="showTab(4)">5. Your Turn to Talk</button>
    </nav>

    <!-- TAB 0 -->
    <div class="tab-content active">
        <div class="card">
            <div class="intention"><strong>Today:</strong> {d["intention"]}</div>
            <div class="discuss">
                <strong>Before we start — talk these through:</strong>
                <ul>
{B.ul(d["warmup"])}
                </ul>
            </div>

            <h2>The vocabulary of this lesson</h2>
            <p>Ten items. Say your answer <strong>out loud before you reveal it</strong>.</p>

{B.vocab(d)}

            <h3>Now use them — out loud</h3>
            <div class="discuss">
                <strong>Before we read:</strong>
                <ul>
{B.ul(d["vocab_use"])}
                </ul>
            </div>
        </div>
    </div>

    <!-- TAB 1 -->
    <div class="tab-content">
        <div class="card">
            <h2>{d["story_heading"]}</h2>
            <p>Read each part. Answer the quick check from memory, then discuss.</p>

{B.story(d)}
        </div>
    </div>

    <!-- TAB 2 -->
    <div class="tab-content">
        <div class="card">
{B.grammar(d["grammar"])}
        </div>
    </div>

    <!-- TAB 3 -->
    <div class="tab-content">
        <div class="card">
{deeper(d["deeper"])}
        </div>
    </div>

    <!-- TAB 4 -->
    <div class="tab-content">
        <div class="card">
{B.speak(d["speak"])}
        </div>
    </div>

    <footer>
        {d["footer"]}
    </footer>
</div>

<script>
{JS}</script>
</body>
</html>
'''


def main():
    targets = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(CONTENT, "*.json")))]
    for slug in targets:
        d = json.load(open(os.path.join(CONTENT, slug + ".json")))
        n = sum(len(s["items"]) for s in d["vocab"])
        assert n == 10, f"{slug}: {n} vocab items, want 10"
        out = os.path.join(ROOT, d["file"])
        open(out, "w").write(build(d))
        print(f"  wrote {d['file']}  ({os.path.getsize(out)//1024}KB)")


if __name__ == "__main__":
    main()
