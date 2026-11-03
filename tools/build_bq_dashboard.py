"""Build big_questions_dashboard.html and BIG_QUESTIONS_IMAGE_PROMPTS.md (one source of truth for the 7 lessons)."""
import math, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

STYLE = ("hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, "
         "soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no logos, no photo-realism")

LESSONS = [
 dict(n=1, file='discuss_c1_why_risk_it.html', title='Why Risk It?', q='Why do people choose hard, dangerous, pointless things?',
      grammar='Conceding a point', color='#0e7490', idea="Because it's there", thinkers='Suits · Camus · flow', gram='Granted · Much as · However',
      img="a lone caver in a headlamp squeezing sideways through a narrow crack in glowing rock, a vast hidden chamber opening ahead, tiny against the stone, mist and warm light, teal and amber palette"),
 dict(n=2, file='bq_02_same_ship_c1.html', title='Is It Still the Same Ship?', q='If every part is replaced, what makes it the same thing?',
      grammar='Cleft sentences', color='#2563eb', idea="Theseus's ship", thinkers='Hobbes · Locke · Parfit', gram='What… is · It is… that',
      img="a wooden sailing ship in a quiet harbour at dawn, half of its planks old and dark, half pale and new, a faint ghost outline of the original ship behind it, blue and gold palette"),
 dict(n=3, file='bq_03_plug_in_c1.html', title='Would You Plug In?', q='Would you take a perfect life that was not real?',
      grammar='Unreal conditionals', color='#7c3aed', idea='The experience machine', thinkers='Nozick · Bentham', gram='If + past · I wish',
      img="a calm figure floating in a glass tank of soft violet light, dreamlike paradise landscapes glowing inside the glass, a real sunrise visible outside the window beyond, violet and rose palette"),
 dict(n=4, file='bq_04_trolley_c1.html', title='The Trolley and the Footbridge', q='Why does flipping a switch feel so different from pushing a man?',
      grammar='Past modals of judgement', color='#dc2626', idea='Switch versus footbridge', thinkers='Foot · Thomson · Kant', gram='should / could / needn\'t have',
      img="an old tram on a track that splits in two at a lever, a stone footbridge arching above, tiny distant figures as abstract silhouettes, dusk light, no violence shown, crimson and slate palette"),
 dict(n=5, file='bq_05_is_it_art_c1.html', title='Is It Art?', q='What, if anything, makes something a work of art?',
      grammar='Passive reporting', color='#d97706', idea='A urinal in a gallery', thinkers='Duchamp · Danto · Dickie', gram='is said to · regarded as',
      img="a bright gallery with ordinary objects displayed like treasures on plinths (a banana, a wooden chair, a bottle rack), a small crowd of puzzled and delighted silhouettes, amber and cream palette"),
 dict(n=6, file='bq_06_free_will_c1.html', title='Is Free Will an Illusion?', q='If your brain decides first, who is in charge?',
      grammar='Hedging and speculating', color='#059669', idea="Libet's clock", thinkers='Laplace · Hume · Dennett', gram='may well · would appear to',
      img="a figure at a crossroads whose shadow is drawn in gears and glowing neurons, a clock face in the sky, two paths ahead, one hand reaching out, green and silver palette"),
 dict(n=7, file='bq_07_is_luck_fair_c1.html', title='Is Luck Fair?', q='If success depends on luck, who deserves what they have?',
      grammar='Inversion for emphasis', color='#be185d', idea='The veil of ignorance', thinkers='Rawls · Nagel · Sandel', gram='Never have · Had it not been for',
      img="runners on a long track starting from very different places, a pair of dice mid-roll in the foreground, a soft veil of mist hanging over the start line, magenta and gold palette"),
]

def node_pos(i, cx=720, cy=450, rx=400, ry=270):
    a = math.radians(-90 + i * 360 / 7)
    return cx + rx * math.cos(a), cy + ry * math.sin(a), math.cos(a)

def svg_map():
    W, H = 1440, 900
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mind map of seven big questions, each with an idea, thinkers and a grammar point">']
    s.append('<style>.t{font-family:Georgia,serif}.l{font-family:"Segoe UI",sans-serif}</style>')
    for i, L in enumerate(LESSONS):
        x, y, c = node_pos(i)
        mx, my = (720 + x) / 2, (450 + y) / 2
        s.append(f'<path d="M720 450 Q{mx + (y - 450) * 0.12:.0f} {my - (x - 720) * 0.12:.0f} {x:.0f} {y:.0f}" stroke="{L["color"]}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".55"/>')
    s.append('<circle cx="720" cy="450" r="92" fill="#5a3aa0"/><text x="720" y="436" text-anchor="middle" class="t" font-size="30" font-weight="700" fill="#fff">Big</text><text x="720" y="470" text-anchor="middle" class="t" font-size="30" font-weight="700" fill="#fff">Questions</text>')
    for i, L in enumerate(LESSONS):
        x, y, c = node_pos(i)
        col = L['color']
        pw, ph = 215, 28
        px = x + 78 if c >= -0.1 else x - 78 - pw
        anchor_x = x + 62 if c >= -0.1 else x - 62
        pills = [('IDEA', L['idea']), ('THINKERS', L['thinkers']), ('GRAMMAR', L['gram'])]
        for k, (kind, text) in enumerate(pills):
            py = y - 51 + k * 34
            s.append(f'<path d="M{anchor_x:.0f} {y:.0f} L{(px if c >= -0.1 else px + pw):.0f} {py + ph / 2:.0f}" stroke="{col}" stroke-width="1.5" opacity=".5" fill="none"/>')
            fill = '#fff' if kind != 'GRAMMAR' else col + '22'
            s.append(f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph}" rx="14" fill="{fill}" stroke="{col}" stroke-width="1.5"/>')
            s.append(f'<text x="{px + 10:.0f}" y="{py + 18:.0f}" class="l" font-size="8.5" font-weight="700" fill="{col}">{kind}</text>')
            s.append(f'<text x="{px + 62:.0f}" y="{py + 18:.0f}" class="l" font-size="12" fill="#2a2a3a">{text.replace("&", "&amp;").replace(chr(39), "&#39;")}</text>')
        words = L['title'].replace('?', '').split()
        s.append(f'<a href="{L["file"]}"><circle cx="{x:.0f}" cy="{y:.0f}" r="62" fill="{col}" stroke="#fff" stroke-width="4"/>')
        lines = [' '.join(words[:len(words) // 2 + len(words) % 2]), ' '.join(words[len(words) // 2 + len(words) % 2:])] if len(words) > 2 else [' '.join(words)]
        y0 = y - (len(lines) - 1) * 9 + 4
        for k, ln in enumerate(lines):
            s.append(f'<text x="{x:.0f}" y="{y0 + k * 18:.0f}" text-anchor="middle" class="t" font-size="14" font-weight="700" fill="#fff">{ln}</text>')
        s.append('</a>')
    s.append('</svg>')
    return '\n'.join(s)

def hotspots():
    # circle centres in the painted map (pixels of the 1586x992 image), in lesson order
    centres = [(760, 150), (1135, 315), (1155, 595), (1015, 795), (545, 790), (425, 575), (445, 270)]
    out = ''
    for L, (x, y) in zip(LESSONS, centres):
        out += (f'<a class="hot" href="{L["file"]}" aria-label="{L["title"]}" title="{L["title"]}" '
                f'style="left:{(x - 95) / 15.86:.2f}%;top:{(y - 95) / 9.92:.2f}%;width:{190 / 15.86:.2f}%;height:{190 / 9.92:.2f}%"></a>')
    return out

def card(L):
    return f'''<a class="story-card" href="{L["file"]}" style="--c:{L["color"]}">
  <div class="card-img" style="background:linear-gradient(135deg,{L["color"]},#2a2a3a)"><span class="num">{L["n"]}</span><img src="BQ_card_{L["n"]:02d}.jpg" alt="" onerror="this.remove()"></div>
  <div class="card-body"><div class="story-title">{L["title"]}</div><div class="story-essence">{L["q"]}</div>
  <div class="story-foot"><span class="grammar-tag" style="background:{L["color"]}">{L["grammar"]}</span><span class="era-tag">C1 · 50 min</span></div>
  <div class="story-extra"><span class="go" style="color:{L["color"]}">Open the lesson →</span></div></div></a>'''

PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Big Questions">
<title>Big Questions · Philosophy and English · C1</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #fafafe; color: #2a2a3a; line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
header { position: relative; color: white; text-align: center; margin-bottom: 28px; border-radius: 14px; box-shadow: 0 10px 30px rgba(102,126,234,0.22); overflow: hidden; padding: 64px 26px; background: linear-gradient(rgba(30,18,70,0.55), rgba(30,18,70,0.55)), url('BigQuestions_title.jpg') center/cover no-repeat, linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
header .tag { display: inline-block; padding: 5px 15px; background: rgba(255,255,255,0.18); border-radius: 14px; font-size: 0.78rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px; }
header h1 { font-size: 2.8rem; line-height: 1.15; margin-bottom: 12px; text-shadow: 0 2px 14px rgba(20,10,50,0.7); }
header .subtitle { font-size: 1.12rem; max-width: 720px; margin: 0 auto; text-shadow: 0 1px 10px rgba(20,10,50,0.7); }
.intro { background: white; border: 1px solid #e0e0ee; border-left: 4px solid #764ba2; border-radius: 12px; padding: 24px 28px; margin-bottom: 28px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.intro p { color: #3a3a4a; margin-bottom: 12px; } .intro p:last-child { margin-bottom: 0; } .intro strong { color: #5a3aa0; }
.section-label { font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: #5a3aa0; font-weight: 700; margin: 0 0 16px 4px; }
.map { background: white; border: 1px solid #e0e0ee; border-radius: 14px; padding: 14px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.map-scroll { overflow-x: auto; } .map-frame { position: relative; min-width: 760px; }
.map-frame img { display: block; width: 100%; height: auto; border-radius: 8px; }
.map-frame svg { display: block; width: 100%; height: auto; }
.map-frame svg a { cursor: pointer; } .map-frame svg a:hover circle { stroke: #ffd36b; }
.hot { position: absolute; border-radius: 50%; } .hot:hover { box-shadow: 0 0 0 3px rgba(255,211,107,0.9); }
.map-note { text-align: center; color: #6a5a8a; font-size: 0.88rem; margin-top: 10px; }
.story-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 8px; }
.story-card { display: flex; flex-direction: column; background: white; border: 1px solid #e0e0ee; border-radius: 14px; text-decoration: none; color: inherit; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s, box-shadow 0.2s; overflow: hidden; }
.story-card:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(102,126,234,0.18); }
.card-img { position: relative; aspect-ratio: 16/9; overflow: hidden; }
.card-img img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.card-img .num { position: absolute; top: 10px; left: 12px; z-index: 2; background: rgba(255,255,255,0.92); color: #2a2a3a; font-weight: 700; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; }
.card-body { padding: 18px 22px 16px; display: flex; flex-direction: column; flex-grow: 1; }
.story-title { font-size: 1.22rem; font-weight: 700; color: #3a2a6a; line-height: 1.25; margin-bottom: 8px; }
.story-essence { font-size: 0.95rem; color: #3a3a4a; margin-bottom: 14px; flex-grow: 1; }
.story-foot { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.grammar-tag { display: inline-block; color: white; font-size: 0.74rem; font-weight: 600; padding: 5px 12px; border-radius: 14px; }
.era-tag { display: inline-block; background: #f1edfa; color: #5a3aa0; border: 1px solid #ddd4f2; font-size: 0.74rem; font-weight: 600; padding: 4px 11px; border-radius: 14px; }
.story-extra { border-top: 1px solid #efecf7; padding-top: 10px; } .go { font-size: 0.84rem; font-weight: 700; }
.how { background: white; border: 1px solid #e0e0ee; border-radius: 12px; padding: 24px 28px; margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.how h2 { color: #5a3aa0; font-size: 1.3rem; margin-bottom: 16px; }
.how-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; }
.how-step { padding: 14px 16px; background: #f6f4fc; border-radius: 10px; } .how-step .n { color: #764ba2; font-weight: 700; font-size: 0.9rem; margin-bottom: 4px; } .how-step p { font-size: 0.88rem; margin: 0; }
footer { text-align: center; color: #888; font-size: 0.86rem; margin: 24px 0 16px; }
@media (max-width: 640px) { .container { padding: 14px; } header h1 { font-size: 2rem; } }
</style>
</head>
<body>
<div class="container">
<header>
  <span class="tag">Philosophy · Professional English · C1</span>
  <h1>Big Questions</h1>
  <p class="subtitle">Seven questions that philosophers have argued about for centuries: why risk everything, what makes a thing the same, whether luck is fair. Argue them in English, with the grammar they need.</p>
</header>

<div class="intro">
  <p>A climber risks her life for a view. A museum rebuilds a ship plank by plank. A machine offers a perfect, false life. <strong>Each of these is a thought experiment</strong>, a short story that makes a hard question impossible to ignore.</p>
  <p>Each lesson starts from one of them. You meet the <strong>key words</strong>, read the <strong>ideas</strong> of the people who argued about it, learn <strong>one grammar structure</strong> that the argument needs, test your thinking on five cases, and then <strong>speak</strong>. The lessons stand alone, so start with the map or pick any card.</p>
</div>

<p class="section-label">The map &mdash; click a circle to open its lesson</p>
<div class="map"><div class="map-scroll"><div class="map-frame" id="mapframe">
<img src="BigQuestions_map.jpg" alt="A mind map of seven big questions with their ideas, thinkers and grammar points" onerror="var f=document.getElementById('mapframe');f.innerHTML=document.getElementById('mapsvg').innerHTML;">
HOTSPOTS
</div></div>
<template id="mapsvg">SVGMAP</template>
<p class="map-note">Each circle is a lesson. The small labels show the central idea, the thinkers, and the grammar point.</p></div>

<p class="section-label">The lessons</p>
<div class="story-grid">
CARDS
</div>

<div class="how">
  <h2>How each lesson works</h2>
  <div class="how-steps">
    <div class="how-step"><div class="n">1 · Key Words</div><p>Ten precise words, unlocked from context before you read.</p></div>
    <div class="how-step"><div class="n">2 · The Ideas</div><p>Three short parts, each with a recall check and a question.</p></div>
    <div class="how-step"><div class="n">3 · Grammar</div><p>One structure the argument needs, with three exercises.</p></div>
    <div class="how-step"><div class="n">4 · Think</div><p>Five cases and a thought experiment to test the ideas on.</p></div>
    <div class="how-step"><div class="n">5 · Speak</div><p>Timed tasks that bring the words, the ideas and the grammar together.</p></div>
  </div>
</div>
<footer>Big Questions · Philosophy and English · C1</footer>
</div>
</body>
</html>
'''

def prompts():
    md = ['# Big Questions: image prompts', '',
          'Generated from `tools/build_bq_dashboard.py` so labels match the page. Save each image beside the dashboard with the filename shown; the page falls back to a coloured gradient and an inline map until they exist.', '',
          f'Shared style for every image: *{STYLE}.*', '',
          '## Title image (`BigQuestions_title.jpg`, wide 3:1 banner)', '', '```',
          f'A wide panoramic banner, about 3:1. Style: {STYLE}. Scene: the inside of an enormous cave-library at dusk, with seven glowing arched doorways set into the curved wall, each lit a different colour (teal, blue, violet, crimson, amber, green, magenta). In the centre foreground a small figure stands holding a lantern, looking up at the doorways. Floating in the air above, drawn very lightly, are a wooden ship, a pair of dice, a balance scale, a clock face and a paintbrush. Keep the centre of the image calm and darker, as text will be placed over it.', '```', '',
          '## Mind map (`BigQuestions_map.jpg`, landscape 16:10)', '', '```',
          f'Create a refined hand-illustrated mind map, landscape 16:10, on warm cream paper. Style: {STYLE.replace(", no text, no letters, no logos", ", no logos")}. Typography: a classic serif for titles and a clean sans-serif for labels, perfectly spelled and easy to read. Every piece of text below must appear exactly as written.', '',
          'CENTRE: a large deep-purple circle with the title "Big Questions".', '',
          'SEVEN BRANCHES radiate from the centre as thick, flowing, tapering curves, clockwise from the top. Each ends in a medium coloured circle holding the lesson name in bold serif, and has three small rounded labels beside it: an IDEA label, a THINKERS label, and a GRAMMAR label (tinted).', '']
    for i, L in enumerate(LESSONS):
        pos = ['top', 'upper right', 'right', 'lower right', 'lower left', 'left', 'upper left'][i]
        md.append(f'{i + 1}. ({pos}, {L["color"]}) circle: "{L["title"]}". Labels: IDEA "{L["idea"]}"; THINKERS "{L["thinkers"]}"; GRAMMAR "{L["gram"]}".')
    md += ['', 'Keep generous white space, no cartoon characters, no clip-art.', '```', '',
           'If the generated circle positions do not match the clickable areas on the page, adjust the `.hot` percentages in the dashboard (the fallback map is always clickable).', '']
    for L in LESSONS:
        md += [f'## Card {L["n"]}: {L["title"]} (`BQ_card_{L["n"]:02d}.jpg`, 16:9)', '', '```',
               f'A 16:9 illustration. Style: {STYLE}. Scene: {L["img"]}. Leave the top-left corner a little quiet, as a number badge sits there.', '```', '']
    return '\n'.join(md)

html = PAGE.replace('HOTSPOTS', hotspots()).replace('SVGMAP', svg_map()).replace('CARDS', '\n'.join(card(L) for L in LESSONS))
open(os.path.join(ROOT, 'big_questions_dashboard.html'), 'w').write(html)
open(os.path.join(ROOT, 'BIG_QUESTIONS_IMAGE_PROMPTS.md'), 'w').write(prompts())
print('ok')
