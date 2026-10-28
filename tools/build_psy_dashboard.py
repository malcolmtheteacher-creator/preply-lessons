"""Build psychology_questions_dashboard.html and PSYCHOLOGY_QUESTIONS_IMAGE_PROMPTS.md: twelve psychology questions (two sets), each at A2/B1 and B2/C1."""
import math, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
STYLE = ("hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, "
         "soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no logos, no photo-realism")
LESSONS = [
 dict(n=1, slug='psy_01_marshmallow', set=1, title='The Marshmallow Test', q='Can a child who waits for a sweet predict the adult they will become?', idea='Delayed gratification', who='Mischel · Watts', color='#0e7490', emoji='🍬', a='If + will', b='unless · provided that · as long as',
      img='a small child at a table with a single glowing marshmallow, a window behind showing a long path to a distant gate, a clock face dissolving into birds, teal and amber palette'),
 dict(n=2, slug='psy_02_invisible_gorilla', set=1, title='The Invisible Gorilla', q='If half of us can look straight at a gorilla and not see it, what else are we missing?', idea='Inattentional blindness', who='Simons · Chabris', color='#2563eb', emoji='🦍', a='Past continuous + past simple', b='Participle clauses',
      img='a crowd of figures passing glowing basketballs on a stage, a great calm gorilla silhouette walking through the middle unnoticed, a spotlight narrowed to one small circle, blue and gold palette'),
 dict(n=3, slug='psy_03_follow_the_crowd', set=1, title='Follow the Crowd?', q='When a whole room says something you can see is wrong, how long do you hold out?', idea='Conformity', who='Asch', color='#7c3aed', emoji='👥', a='should · have to · don\'t have to', b='Reporting verbs',
      img='a row of identical silhouetted figures all pointing at one line on a card, one lone figure at the end holding a lantern and looking at a different line, violet and rose palette'),
 dict(n=4, slug='psy_04_can_you_trust_memory', set=1, title='Can You Trust Your Memory?', q='If one word in a question can change what you remember, what is a memory worth?', idea='The misinformation effect', who='Loftus · Palmer', color='#dc2626', emoji='🧠', a='Past simple', b='Speculating about the past',
      img='a hand painting over an old photograph, pieces of the picture floating away and re-forming slightly differently, a road and two cars in the picture, crimson and sepia palette'),
 dict(n=5, slug='psy_05_born_or_made', set=1, title='Born or Made?', q='Identical twins raised apart can be uncannily alike. What does that say about who we are?', idea='Nature and nurture', who='Bouchard · twin studies', color='#d97706', emoji='🧬', a='Comparing things', b='whereas · although · despite',
      img='two identical figures standing in two different landscapes, one in a snowy pine forest and one by a warm sea, a glowing double helix as a rope between them, amber and green palette'),
 dict(n=6, slug='psy_06_does_money_buy_happiness', set=1, title='Does Money Buy Happiness?', q='A lottery win should change everything. Does it?', idea='The hedonic treadmill', who='Brickman · Kahneman · Killingsworth', color='#059669', emoji='💷', a='Present perfect (experience)', b='Describing data and hedging',
      img='a figure running on a giant treadmill that is made of gold coins while a small kite and a picnic blanket wait unnoticed beside it, green and gold palette'),
 dict(n=7, slug='psyp_07_replication_crisis', set=2, title='Can We Repeat the Result?', q='A field tried to reproduce its own findings. What happened?', idea='The replication crisis', who='Open Science Collaboration · Simmons', color='#1d4ed8', emoji='🔁', a='The passive', b='Nominalisation',
      img='a long laboratory shelf of glass jars each holding a glowing result, a second shelf below with the same jars much dimmer, a researcher holding a magnifying glass between them, indigo and silver palette'),
 dict(n=8, slug='psyp_08_should_this_study_run', set=2, title='Should This Study Be Allowed?', q='What would it take for a famous experiment to pass an ethics board today?', idea='Research ethics', who='Milgram · Baumrind · Belmont', color='#9f1239', emoji='⚖️', a='must · mustn\'t · be allowed to', b='Formal obligation and permission',
      img='an old balance scale with a small glowing lab beaker on one side and a pile of closed doors on the other, a quiet committee table in the background, wine-red and brass palette'),
 dict(n=9, slug='psyp_09_does_the_method_matter', set=2, title='Does the Method Matter?', q='If every therapy works about equally well, what is doing the work?', idea='The Dodo bird verdict', who='Rosenzweig · Wampold', color='#0f766e', emoji='🤝', a='Quantifiers', b='Relative clauses',
      img='a dodo bird in a waistcoat holding a bundle of different keys, two chairs facing each other in a warm room, threads of light joining the chairs, deep teal and cream palette'),
 dict(n=10, slug='psyp_10_who_decides_whats_normal', set=2, title='Who Decides What Is Normal?', q='Healthy people went to hospital and said they heard a voice. What happened?', idea='Diagnosis and labels', who='Rosenhan · Spitzer · Cahalan', color='#7e22ce', emoji='🏷️', a='Reported speech', b='Indirect and softened questions',
      img='a corridor of identical doors with luggage-tag labels hanging from each handle, one figure stepping through a door with a label half peeled off, soft violet light, purple and grey palette'),
 dict(n=11, slug='psyp_11_judgment_or_formula', set=2, title='Expert or Formula?', q='A simple list of numbers has often matched the professional. Why?', idea='Clinical vs statistical prediction', who='Meehl · Kahneman · Klein', color='#b45309', emoji='📋', a='will · going to · might', b='Prediction and likelihood',
      img='a seasoned figure with an hourglass and a crystal ball on one side, a small tidy checklist and abacus on the other, a path between them through a misty garden, ochre and slate palette'),
 dict(n=12, slug='psyp_12_whose_psychology', set=2, title='Whose Psychology Is It?', q='Most of what we know about the mind comes from a small part of the world. Does it matter?', idea='WEIRD samples', who='Henrich · Heine · Norenzayan', color='#3f6212', emoji='🌍', a='Numbers and comparisons', b='Comparative structures',
      img='a great illuminated globe with only one small region brightly lit and the rest softly glowing in many colours, tiny figures with lanterns travelling between regions, olive green and gold palette'),
]
SETNAMES = {1: 'The experiments', 2: 'Going deeper: for psychologists and professionals'}

def node_pos(i, cx=720, cy=450, rx=440, ry=330):
    a = math.radians(-75 + i * 30)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)

def svg_map():
    W, H = 1440, 900
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mind map of twelve psychology questions in two sets">']
    s.append('<style>.t{font-family:Georgia,serif}.l{font-family:"Segoe UI",sans-serif}</style>')
    for i, L in enumerate(LESSONS):
        x, y = node_pos(i)
        s.append(f'<path d="M720 450 L{x:.0f} {y:.0f}" stroke="{L["color"]}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>')
    s.append('<circle cx="720" cy="450" r="100" fill="#5a3aa0"/><text x="720" y="440" text-anchor="middle" class="t" font-size="27" font-weight="700" fill="#fff">Psychology</text><text x="720" y="474" text-anchor="middle" class="t" font-size="27" font-weight="700" fill="#fff">Questions</text>')
    s.append('<text x="1000" y="46" text-anchor="middle" class="l" font-size="14" font-weight="700" letter-spacing="2" fill="#5a3aa0">THE EXPERIMENTS</text>')
    s.append('<text x="440" y="46" text-anchor="middle" class="l" font-size="14" font-weight="700" letter-spacing="2" fill="#5a3aa0">GOING DEEPER · FOR PROFESSIONALS</text>')
    for i, L in enumerate(LESSONS):
        x, y = node_pos(i)
        col = L['color']
        pw, ph = 196, 26
        px, py = x - pw / 2, y + 66
        s.append(f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph}" rx="13" fill="#fff" stroke="{col}" stroke-width="1.5"/>')
        s.append(f'<text x="{px + 10:.0f}" y="{py + 17:.0f}" class="l" font-size="8" font-weight="700" fill="{col}">IDEA</text>')
        s.append(f'<text x="{px + 42:.0f}" y="{py + 17:.0f}" class="l" font-size="11" fill="#2a2a3a">{L["idea"].replace("&", "&amp;")}</text>')
        words = L['title'].replace('?', '').split()
        half = len(words) // 2 + len(words) % 2
        lines = [' '.join(words[:half]), ' '.join(words[half:])] if len(words) > 2 else [' '.join(words)]
        s.append(f'<a href="#q{L["n"]}"><circle cx="{x:.0f}" cy="{y:.0f}" r="58" fill="{col}" stroke="#fff" stroke-width="4"/>')
        y0 = y - (len(lines) - 1) * 9 + 4
        for k, ln in enumerate(lines):
            s.append(f'<text x="{x:.0f}" y="{y0 + k * 18:.0f}" text-anchor="middle" class="t" font-size="12" font-weight="700" fill="#fff">{ln}</text>')
        s.append('</a>')
    s.append('</svg>')
    return '\n'.join(s)

def hotspots():
    # circle centres in the painted map (pixels of the 1586x992 image), in lesson order
    centres = [(985, 155), (1280, 215), (1308, 395), (1295, 578), (1242, 765), (950, 790),
               (652, 795), (350, 770), (308, 578), (283, 392), (318, 205), (640, 160)]
    out = ''
    for L, (x, y) in zip(LESSONS, centres):
        out += (f'<a class="hot" href="#q{L["n"]}" aria-label="{L["title"]}" title="{L["title"]}" '
                f'style="left:{(x - 90) / 15.86:.2f}%;top:{(y - 90) / 9.92:.2f}%;width:{180 / 15.86:.2f}%;height:{180 / 9.92:.2f}%"></a>')
    return out

def prompts():
    md = ['# Psychology Questions: image prompts', '',
          'Generated from `tools/build_psy_dashboard.py` so labels match the page. Save each image beside the dashboard with the filename shown; the page falls back to a coloured gradient and an inline map until they exist. Paste each prompt into ChatGPT (image generation) exactly as written.', '',
          f'Shared style for every image: *{STYLE}.*', '',
          '## Title image (`PsychologyQuestions_title.jpg`, wide 3:1 banner)', '', '```',
          f'A wide panoramic banner, about 3:1. Style: {STYLE}. Scene: a great curved library-laboratory at dusk, with twelve tall arched windows, six on the right glowing warm amber and teal, six on the left glowing deeper indigo and wine-red. Through the windows, faint scenes: a sweet on a table, a gorilla, a crowd of silhouettes, a photograph, twins, coins on the right; a flask, a scale, a dodo, a hospital door, a checklist, a globe on the left. In the centre foreground a small figure with a lantern stands at a long table, looking at a softly glowing brain-shaped lamp. Keep the centre calm and darker, as text will be placed over it.', '```', '',
          '## Mind map (`PsychologyQuestions_map.jpg`, landscape 16:10)', '', '```',
          f'Create a refined hand-illustrated mind map, landscape 16:10, on warm cream paper. Style: {STYLE.replace(", no text, no letters, no logos", ", no logos")}. Typography: a classic serif for titles and a clean sans-serif for labels, perfectly spelled and easy to read. Every piece of text below must appear exactly as written.', '',
          'CENTRE: a large deep-purple circle with the title "Psychology Questions".', '',
          'TWO HALVES. The RIGHT half holds six circles for "THE EXPERIMENTS", with a small label "THE EXPERIMENTS" in spaced capitals above it near the top. The LEFT half holds six circles for "GOING DEEPER · FOR PROFESSIONALS", with that small label in spaced capitals above it near the top. Twelve thick, flowing, tapering curves radiate from the centre to the twelve circles. The circles sit on a wide oval around the centre, evenly spaced, clockwise from the upper right: the right half runs from upper right down to lower right, then the left half runs from lower left up to upper left. Each circle holds the lesson name in bold serif, and has one small rounded IDEA label directly beneath it.', '']
    pos = ['upper right', 'right, upper', 'right, lower', 'right, lowest', 'lower right', 'bottom right', 'bottom left', 'lower left', 'left, lowest', 'left, lower', 'left, upper', 'upper left']
    for i, L in enumerate(LESSONS):
        md.append(f'{i + 1}. ({pos[i]}, {L["color"]}) circle: "{L["title"]}". Label beneath: IDEA "{L["idea"]}".')
    md += ['', 'Keep generous white space, no cartoon characters, no clip-art. All twelve circles must be the same size, with equal gaps between them.', '```', '',
           'If the generated circle positions do not match the clickable areas on the page, tell Claude where the image is and the hot spots will be re-aligned (the fallback map is always clickable).', '']
    for L in LESSONS:
        md += [f'## Card {L["n"]}: {L["title"]} (`PQ_card_{L["n"]:02d}.jpg`, 16:9)', '', '```',
               f'A 16:9 illustration. Style: {STYLE}. Scene: {L["img"]}. Leave the top-left corner a little quiet, as a number badge sits there.', '```', '']
    return '\n'.join(md)

def card(L):
    return f'''<div class="story-card" id="q{L["n"]}" style="--c:{L["color"]}">
  <div class="card-img" style="background:linear-gradient(135deg,{L["color"]},#2a2a3a)"><span class="num">{L["n"]}</span><span class="emoji">{L["emoji"]}</span><img src="PQ_card_{L["n"]:02d}.jpg" alt="" onerror="this.remove()"></div>
  <div class="card-body"><div class="story-title">{L["title"]}</div><div class="story-essence">{L["q"]}</div>
  <div class="meta"><span class="pill">{L["idea"]}</span><span class="pill alt">{L["who"]}</span></div>
  <div class="levels">
    <a class="lvl" href="{L["slug"]}_a2b1.html" style="--c:{L["color"]}"><strong>A2/B1</strong><span>{L["a"]}</span></a>
    <a class="lvl" href="{L["slug"]}_b2c1.html" style="--c:{L["color"]}"><strong>B2/C1</strong><span>{L["b"]}</span></a>
  </div></div></div>'''
PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Psychology Questions">
<title>Psychology Questions · A2/B1 and B2/C1 English</title>
<style>
html { scroll-behavior: smooth; }
.story-card { scroll-margin-top: 20px; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #fafafe; color: #2a2a3a; line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
header { color: white; text-align: center; margin-bottom: 28px; border-radius: 14px; box-shadow: 0 10px 30px rgba(102,126,234,0.22); padding: 56px 26px; background: linear-gradient(rgba(30,18,70,0.55), rgba(30,18,70,0.55)), url('PsychologyQuestions_title.jpg') center/cover no-repeat, linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
header .tag { display: inline-block; padding: 5px 15px; background: rgba(255,255,255,0.18); border-radius: 14px; font-size: 0.78rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px; }
header h1 { font-size: 2.6rem; line-height: 1.15; margin-bottom: 12px; }
header .subtitle { font-size: 1.1rem; max-width: 720px; margin: 0 auto; opacity: 0.95; }
.map { background: white; border: 1px solid #e0e0ee; border-radius: 14px; padding: 14px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.map-scroll { overflow-x: auto; } .map-frame { position: relative; min-width: 760px; }
.map-frame img { display: block; width: 100%; height: auto; border-radius: 8px; } .map-frame svg { display: block; width: 100%; height: auto; }
.map-frame svg a { cursor: pointer; } .map-frame svg a:hover circle { stroke: #ffd36b; }
.hot { position: absolute; border-radius: 50%; } .hot:hover { box-shadow: 0 0 0 3px rgba(255,211,107,0.9); }
.map-note { text-align: center; color: #6a5a8a; font-size: 0.88rem; margin-top: 10px; }
.set-head { margin: 34px 0 6px; } .set-head h2 { color: #3a2a6a; font-size: 1.5rem; } .set-head p { color: #555; font-size: 0.95rem; margin-bottom: 16px; }
.intro { background: white; border: 1px solid #e0e0ee; border-left: 4px solid #764ba2; border-radius: 12px; padding: 22px 28px; margin-bottom: 28px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.intro p { color: #3a3a4a; margin-bottom: 10px; } .intro p:last-child { margin-bottom: 0; } .intro strong { color: #5a3aa0; }
.section-label { font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: #5a3aa0; font-weight: 700; margin: 0 0 16px 4px; }
.story-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-bottom: 8px; }
.story-card { display: flex; flex-direction: column; background: white; border: 1px solid #e0e0ee; border-radius: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden; }
.card-img { position: relative; height: 120px; display: flex; align-items: center; justify-content: center; }
.card-img { overflow: hidden; } .card-img img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; } .card-img .emoji { font-size: 3.4rem; } .card-img .num { z-index: 2; }
.card-img .num { position: absolute; top: 10px; left: 12px; background: rgba(255,255,255,0.92); color: #2a2a3a; font-weight: 700; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; }
.card-body { padding: 18px 22px 20px; display: flex; flex-direction: column; flex-grow: 1; }
.story-title { font-size: 1.22rem; font-weight: 700; color: #3a2a6a; line-height: 1.25; margin-bottom: 8px; }
.story-essence { font-size: 0.95rem; color: #3a3a4a; margin-bottom: 12px; flex-grow: 1; }
.meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.pill { background: #f1edfa; color: #5a3aa0; border: 1px solid #ddd4f2; font-size: 0.74rem; font-weight: 600; padding: 4px 11px; border-radius: 14px; } .pill.alt { background: #fff; color: #666; border-color: #e0e0ee; }
.levels { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.lvl { display: flex; flex-direction: column; gap: 2px; text-decoration: none; color: #2a2a3a; border: 2px solid var(--c); border-radius: 10px; padding: 10px 12px; transition: all 0.2s; }
.lvl strong { color: var(--c); font-size: 0.95rem; } .lvl span { font-size: 0.78rem; color: #555; line-height: 1.3; }
.lvl:hover { background: var(--c); } .lvl:hover strong, .lvl:hover span { color: white; }
.how { background: white; border: 1px solid #e0e0ee; border-radius: 12px; padding: 24px 28px; margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.how h2 { color: #5a3aa0; font-size: 1.3rem; margin-bottom: 16px; }
.how-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; }
.how-step { padding: 14px 16px; background: #f6f4fc; border-radius: 10px; } .how-step .n { color: #764ba2; font-weight: 700; font-size: 0.9rem; margin-bottom: 4px; } .how-step p { font-size: 0.88rem; margin: 0; }
footer { text-align: center; color: #888; font-size: 0.86rem; margin: 24px 0 16px; }
@media (max-width: 640px) { .container { padding: 14px; } header h1 { font-size: 2rem; } .story-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="container">
<header>
  <span class="tag">Psychology · English · A2/B1 and B2/C1</span>
  <h1>Psychology Questions</h1>
  <p class="subtitle">Twelve questions about how the mind works and how the field works. Six famous experiments, then six deeper questions for psychologists and other professionals. Every question comes at two levels: A2/B1 and B2/C1.</p>
</header>

<div class="intro">
  <p>A child is left alone with a sweet. A gorilla walks through a basketball game. A whole room gives the wrong answer. <strong>Each of these is a real experiment</strong> that changed what people thought about the mind.</p>
  <p>Each lesson starts from one of them. You meet the <strong>key words</strong>, read the <strong>story</strong> in three short parts, practise <strong>one grammar structure</strong> the story needs, test your thinking on five cases, and then <strong>speak</strong>. The second set, <strong>going deeper</strong>, asks how psychology checks itself: whether results repeat, what ethics allows, whether the method matters, who decides what is normal, whether experts beat formulas, and whose minds the research is about. Pick a question, then pick your level.</p>
</div>

<p class="section-label">The map &mdash; click a circle to jump to its lesson</p>
<div class="map"><div class="map-scroll"><div class="map-frame" id="mapframe">
<img src="PsychologyQuestions_map.jpg" alt="A mind map of twelve psychology questions in two sets" onerror="var f=document.getElementById('mapframe');f.innerHTML=document.getElementById('mapsvg').innerHTML;">
HOTSPOTS
</div></div>
<template id="mapsvg">SVGMAP</template>
<p class="map-note">Right: the six experiments. Left: six deeper questions for professionals.</p></div>

<div class="set-head" id="set1"><h2>The experiments</h2><p>Six studies that changed what people thought about the mind. Open a question, then choose A2/B1 or B2/C1.</p></div>
<div class="story-grid">
CARDS1
</div>

<div class="set-head" id="deeper"><h2>Going deeper: for psychologists and professionals</h2><p>How the field checks itself: replication, ethics, therapy, diagnosis, prediction and who the research is about. The content and language are pitched at people who work in psychology, mental health, education and research.</p></div>
<div class="story-grid">
CARDS2
</div>

<div class="how">
  <h2>How each lesson works</h2>
  <div class="how-steps">
    <div class="how-step"><div class="n">1 · Key Words</div><p>The words you need, unlocked from context before you read.</p></div>
    <div class="how-step"><div class="n">2 · The Story</div><p>Three short parts, each with a recall check and a question.</p></div>
    <div class="how-step"><div class="n">3 · Grammar</div><p>One structure the story needs, with three exercises.</p></div>
    <div class="how-step"><div class="n">4 · Think</div><p>Five cases and a thought experiment to test the ideas on.</p></div>
    <div class="how-step"><div class="n">5 · Speak</div><p>Timed tasks that bring words, ideas and grammar together.</p></div>
  </div>
</div>
<footer>Psychology Questions · A2/B1 and B2/C1 · 12 lessons × 2 levels</footer>
</div>
</body>
</html>
'''
html = (PAGE.replace('HOTSPOTS', hotspots()).replace('SVGMAP', svg_map())
        .replace('CARDS1', '\n'.join(card(L) for L in LESSONS if L['set'] == 1))
        .replace('CARDS2', '\n'.join(card(L) for L in LESSONS if L['set'] == 2)))
open(os.path.join(ROOT, 'psychology_questions_dashboard.html'), 'w').write(html)
open(os.path.join(ROOT, 'PSYCHOLOGY_QUESTIONS_IMAGE_PROMPTS.md'), 'w').write(prompts())
print('ok')
