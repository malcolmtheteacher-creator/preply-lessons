"""Build psychology_questions_dashboard.html: six psychology questions, each at A2/B1 and B2/C1."""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LESSONS = [
 dict(n=1, slug='psy_01_marshmallow', title='The Marshmallow Test', q='Can a child who waits for a sweet predict the adult they will become?', idea='Delayed gratification', who='Mischel · Watts', color='#0e7490', emoji='🍬', a='If + will', b='unless · provided that · as long as'),
 dict(n=2, slug='psy_02_invisible_gorilla', title='The Invisible Gorilla', q='If half of us can look straight at a gorilla and not see it, what else are we missing?', idea='Inattentional blindness', who='Simons · Chabris', color='#2563eb', emoji='🦍', a='Past continuous + past simple', b='Participle clauses'),
 dict(n=3, slug='psy_03_follow_the_crowd', title='Follow the Crowd?', q='When a whole room says something you can see is wrong, how long do you hold out?', idea='Conformity', who='Asch', color='#7c3aed', emoji='👥', a='should · have to · don\'t have to', b='Reporting verbs'),
 dict(n=4, slug='psy_04_can_you_trust_memory', title='Can You Trust Your Memory?', q='If one word in a question can change what you remember, what is a memory worth?', idea='The misinformation effect', who='Loftus · Palmer', color='#dc2626', emoji='🧠', a='Past simple', b='Speculating about the past'),
 dict(n=5, slug='psy_05_born_or_made', title='Born or Made?', q='Identical twins raised apart can be uncannily alike. What does that say about who we are?', idea='Nature and nurture', who='Bouchard · twin studies', color='#d97706', emoji='🧬', a='Comparing things', b='whereas · although · despite'),
 dict(n=6, slug='psy_06_does_money_buy_happiness', title='Does Money Buy Happiness?', q='A lottery win should change everything. Does it?', idea='The hedonic treadmill', who='Brickman · Kahneman · Killingsworth', color='#059669', emoji='💷', a='Present perfect (experience)', b='Describing data and hedging'),
]
def card(L):
    return f'''<div class="story-card" style="--c:{L["color"]}">
  <div class="card-img" style="background:linear-gradient(135deg,{L["color"]},#2a2a3a)"><span class="num">{L["n"]}</span><span class="emoji">{L["emoji"]}</span></div>
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
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #fafafe; color: #2a2a3a; line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
header { color: white; text-align: center; margin-bottom: 28px; border-radius: 14px; box-shadow: 0 10px 30px rgba(102,126,234,0.22); padding: 56px 26px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
header .tag { display: inline-block; padding: 5px 15px; background: rgba(255,255,255,0.18); border-radius: 14px; font-size: 0.78rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px; }
header h1 { font-size: 2.6rem; line-height: 1.15; margin-bottom: 12px; }
header .subtitle { font-size: 1.1rem; max-width: 720px; margin: 0 auto; opacity: 0.95; }
.intro { background: white; border: 1px solid #e0e0ee; border-left: 4px solid #764ba2; border-radius: 12px; padding: 22px 28px; margin-bottom: 28px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.intro p { color: #3a3a4a; margin-bottom: 10px; } .intro p:last-child { margin-bottom: 0; } .intro strong { color: #5a3aa0; }
.section-label { font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: #5a3aa0; font-weight: 700; margin: 0 0 16px 4px; }
.story-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-bottom: 8px; }
.story-card { display: flex; flex-direction: column; background: white; border: 1px solid #e0e0ee; border-radius: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden; }
.card-img { position: relative; height: 120px; display: flex; align-items: center; justify-content: center; }
.card-img .emoji { font-size: 3.4rem; }
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
  <p class="subtitle">Six famous experiments about how the mind works: waiting, attention, the crowd, memory, nature and nurture, and money. Each one comes at two levels, so the same story can be told at A2/B1 or argued at B2/C1.</p>
</header>

<div class="intro">
  <p>A child is left alone with a sweet. A gorilla walks through a basketball game. A whole room gives the wrong answer. <strong>Each of these is a real experiment</strong> that changed what people thought about the mind.</p>
  <p>Each lesson starts from one of them. You meet the <strong>key words</strong>, read the <strong>story</strong> in three short parts, practise <strong>one grammar structure</strong> the story needs, test your thinking on five cases, and then <strong>speak</strong>. Pick a question, then pick your level.</p>
</div>

<p class="section-label">The questions</p>
<div class="story-grid">
CARDS
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
<footer>Psychology Questions · A2/B1 and B2/C1</footer>
</div>
</body>
</html>
'''
open(os.path.join(ROOT, 'psychology_questions_dashboard.html'), 'w').write(PAGE.replace('CARDS', '\n'.join(card(L) for L in LESSONS)))
print('ok')
