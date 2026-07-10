#!/usr/bin/env python3
import re, html

PLAN = "/Users/malcolmtheteacher/Documents/01_Work/gitsite/MIA_SERIES_PLAN.md"
OUT  = "/Users/malcolmtheteacher/Documents/01_Work/gitsite/mia_image_prompts.html"

CHARS = {
    "{MIA}":  "Mia (late-20s woman, medium-brown skin, short dark wavy hair, bright teal jacket, coral-and-amber patterned scarf)",
    "{TOM}":  "Tom (kind man in his late 50s, light-brown skin, short grey beard, glasses, soft-green cardigan)",
    "{ROSA}": "Rosa (warm cafe owner in her 40s, olive skin, dark hair in a loose bun, apron over a mustard-yellow top)",
    "{ANA}":  "Ana (Mia's younger sister, early 20s, medium-brown skin, long dark curly hair, denim jacket over a sunny yellow top)",
}
STYLE = ("A scene for \"Mia's English\". {SCENE} Flat warm storybook vector illustration, "
         "cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded "
         "shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3.")

# The 4 images still missing from lessons 5-6 (prompts as in the original brief)
MISSING = [
    ("a1s_05_morning.png", "Lesson 5 · My day",
     "A scene for \"Mia's English\". Early morning: Mia (late-20s woman, medium-brown skin, short dark wavy hair) gets up and stretches by a sunny window in her cosy room, still a little sleepy but cheerful. Warm morning light. Flat warm storybook vector illustration, cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3."),
    ("a1s_05_cafe_work.png", "Lesson 5 · My day",
     "A scene for \"Mia's English\". Mia (teal jacket or apron, coral-and-amber scarf, short dark wavy hair) works happily behind the counter at Rosa's cafe, serving a coffee; Rosa (40s, olive skin, apron over a mustard-yellow top, dark hair in a bun) is nearby. Busy, warm, friendly. Flat warm storybook vector illustration, cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3."),
    ("a1s_06_evening.png", "Lesson 6 · I like it!",
     "A scene for \"Mia's English\". Mia (teal jacket, coral-and-amber scarf), Tom (late 50s, grey beard, glasses, soft-green cardigan) and Rosa (apron, dark hair in a bun) sit together at the cafe in warm evening light, chatting and laughing over drinks. Cosy, golden. Flat warm storybook vector illustration, cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3."),
    ("a1s_06_like.png", "Lesson 6 · I like it!",
     "A scene for \"Mia's English\". Mia (teal jacket, coral-and-amber scarf, short dark wavy hair) smiles warmly, surrounded by small friendly icons of things she likes - a coffee cup, a music note, an open book. Flat warm storybook vector illustration, cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3."),
]

ANA_SHEET = ("ana_character_sheet.png", "New character — make BEFORE Lesson 15",
    "Create a character reference sheet for \"Ana\", Mia's younger sister in the \"Mia's English\" beginner-English story series. Ana is a bright, energetic young woman in her early 20s, medium-brown skin, long dark curly hair, wearing a denim jacket over a sunny yellow top. Show front view, side view, and three expressions: excited, laughing, and a warm hug-ready smile. Flat warm storybook vector illustration, cream (#fbf7f0), teal (#2f8f9d), amber (#f2a65a) and soft coral palette, soft rounded shapes, clean lines, gentle shading. No text, no letters anywhere. 4:3.")

def subst(scene):
    for k, v in CHARS.items():
        scene = scene.replace(k, v)
    return STYLE.replace("{SCENE}", scene.strip())

lessons = []
for line in open(PLAN, encoding="utf-8"):
    line = line.strip()
    m = re.match(r"^(\d+)\s*\|\|", line)
    if not m:
        continue
    parts = [p.strip() for p in line.split("||")]
    n, slug, title, grammar, beat, img1, img2 = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
    f1, s1 = [x.strip() for x in img1.split("::", 1)]
    f2, s2 = [x.strip() for x in img2.split("::", 1)]
    lessons.append((int(n), title, f1 + ".png", subst(s1), f2 + ".png", subst(s2)))

cards = []
idx = 1
def card(fname, label, prompt):
    global idx
    c = f'''<div class="card" id="img{idx}">
  <div class="head"><span class="num">{idx}</span><div><div class="fname">{html.escape(fname)}</div><div class="label">{html.escape(label)}</div></div>
  <button class="copy" onclick="cp(this,'p{idx}')">Copy</button></div>
  <div class="prompt" id="p{idx}">{html.escape(prompt)}</div>
</div>'''
    idx += 1
    return c

# Section 1: the 4 missing
sec1 = [card(f, l, p) for f, l, p in MISSING]
# Sections per lesson
sec2 = []
for n, title, f1, p1, f2, p2 in lessons:
    if n == 15:
        sec2.append('<h2>Before Lesson 15 — new character: Ana</h2>')
        sec2.append(card(*ANA_SHEET))
    sec2.append(f'<h2>Lesson {n} — {html.escape(title)}</h2>')
    sec2.append(card(f1, f"Lesson {n} · picture 1", p1))
    sec2.append(card(f2, f"Lesson {n} · picture 2", p2))

total = idx - 1
page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mia's English — every picture, in order ({total} images)</title>
<style>
body{{font-family:"Segoe UI",sans-serif;background:#fbf7f0;color:#333;margin:0;padding:24px}}
.wrap{{max-width:860px;margin:0 auto}}
h1{{color:#2f8f9d}} h2{{color:#c77b2e;margin:34px 0 10px;border-bottom:2px solid #f2a65a55;padding-bottom:4px}}
.note{{background:#fff;border:1px solid #e5ddcf;border-radius:12px;padding:14px 18px;margin-bottom:18px;line-height:1.6}}
.card{{background:#fff;border:1px solid #e5ddcf;border-radius:12px;padding:14px 16px;margin:12px 0;box-shadow:0 2px 6px rgba(0,0,0,.04)}}
.head{{display:flex;align-items:center;gap:12px;margin-bottom:8px}}
.num{{background:#2f8f9d;color:#fff;border-radius:50%;min-width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:700}}
.fname{{font-weight:700;color:#2f8f9d;font-family:monospace}} .label{{font-size:.85rem;color:#999}}
.copy{{margin-left:auto;background:#f2a65a;color:#fff;border:none;border-radius:18px;padding:8px 18px;font-weight:700;cursor:pointer;font-size:.9rem}}
.copy:hover{{background:#e0954a}} .copy.ok{{background:#4a9c5f}}
.prompt{{background:#faf6ee;border-radius:8px;padding:10px 14px;font-size:.92rem;line-height:1.55;color:#555}}
</style></head><body><div class="wrap">
<h1>Mia's English — every picture, in order</h1>
<div class="note"><b>How to use:</b> work from top to bottom. Press <b>Copy</b>, paste the prompt into ChatGPT, then save the image into the <b>gitsite</b> folder with the <b>exact filename shown</b> on the card. {total} images in total: 4 missing ones from Lessons 5&ndash;6 first, then Lessons 7&ndash;50 in order (two pictures per lesson), plus one new character sheet (Ana) before Lesson 15. You already have the Mia, Tom and Rosa character sheets &mdash; keep using that same ChatGPT project so the characters stay consistent.</div>
<h2>First — the 4 missing pictures (Lessons 5 &amp; 6)</h2>
{''.join(sec1)}
{''.join(sec2)}
</div>
<script>
function cp(btn,id){{navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>{{btn.textContent='Copied ✓';btn.classList.add('ok');setTimeout(()=>{{btn.textContent='Copy';btn.classList.remove('ok');}},1500);}});}}
</script></body></html>'''

open(OUT, "w", encoding="utf-8").write(page)
print(f"wrote {OUT}: {total} image prompts ({len(lessons)} lessons x2 + 4 missing + 1 character sheet)")
