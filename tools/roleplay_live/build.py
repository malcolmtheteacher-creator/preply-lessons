#!/usr/bin/env python3
"""Rebuild the Useful Phrases and Your Turn panels of an Everyday Echoes roleplay
from a config in configs.py, reorder the tabs (phrases before conversation) and
write a separate teacher sheet. Idempotent: safe to re-run.

Usage: python3 tools/roleplay_live/build.py rp_09 [rp_02 ...]
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from configs import CONFIGS, REPAIR  # noqa: E402

CSS_START, CSS_END = '/* RPLIVE-CSS-START */', '/* RPLIVE-CSS-END */'
JS_START, JS_END = '/* RPLIVE-JS-START */', '/* RPLIVE-JS-END */'

CSS = """
.shape-label{ font-size:0.78rem; letter-spacing:1.2px; text-transform:uppercase; font-weight:700; color:var(--amber-d); margin:14px 0 6px; }
.shape{ display:flex; gap:6px; flex-wrap:wrap; margin-bottom:6px; }
.shape span{ background:var(--soft); border:1px solid var(--line); border-radius:999px; padding:6px 12px; font-size:0.9rem; font-weight:700; color:var(--teal-d); }
.shape-note{ color:#6f685d; font-size:0.9rem; margin-bottom:10px; }
.moves{ margin:8px 0 6px 22px; }
.moves li{ margin-bottom:6px; }
.chips{ display:flex; gap:8px; flex-wrap:wrap; margin:10px 0; }
.chip{ border:1px solid var(--line); background:#fff; color:var(--teal-d); border-radius:999px; padding:9px 16px; font-weight:700; font-size:0.95rem; cursor:pointer; }
.chip:hover{ background:var(--soft); }
.chip.active{ background:linear-gradient(135deg,var(--teal),var(--teal-d)); color:#fff; border-color:transparent; }
.rolecard{ background:var(--warm); border:1px solid var(--line); border-radius:16px; padding:16px 18px; margin:12px 0; }
.rolecard.other{ background:var(--soft); }
.rc-tag{ font-size:0.78rem; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; color:var(--amber-d); margin-bottom:6px; }
.rolecard.other .rc-tag{ color:var(--teal-d); }
.rc-row{ display:flex; gap:12px; margin:6px 0; }
.rc-row b{ flex:0 0 120px; color:var(--teal-d); }
.winline{ font-weight:700; color:var(--teal-d); margin:8px 0 4px; }
.twist-card{ background:#fff; border:1px dashed #e0b88c; border-radius:12px; padding:14px 16px; margin-top:12px; font-size:1.08rem; font-weight:600; min-height:52px; }
.checks label{ display:block; background:var(--cream); border:1px solid var(--line); border-radius:10px; padding:10px 14px; margin:6px 0; cursor:pointer; }
.checks input{ margin-right:8px; transform:scale(1.15); }
.kit-bar{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:6px; }
.kit-note{ color:#6f685d; font-size:0.9rem; }
.tk-group{ background:var(--warm); border:1px solid var(--line); border-radius:14px; padding:12px 16px; margin:10px 0; }
.tk-group.alt{ background:var(--soft); }
.tk-move{ font-size:0.78rem; letter-spacing:1.2px; text-transform:uppercase; font-weight:700; color:var(--amber-d); margin-bottom:6px; }
.tk-phrase{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:8px 12px; margin:6px 0; font-weight:600; }
.tk-tip{ color:var(--teal-d); font-size:0.93rem; margin-top:6px; }
.cue-card{ background:#fff; border:1px dashed #e0b88c; border-radius:12px; padding:14px 16px; margin:12px 0; font-size:1.05rem; font-weight:600; min-height:52px; }
#kit.covered{ display:none; }
@media (max-width:520px){ .rc-row{ flex-direction:column; gap:0; } .rc-row b{ flex:none; } }
"""

JS_FIXED = """
function toggleKit(btn){
  var kit = document.getElementById('kit');
  var covered = kit.classList.toggle('covered');
  btn.textContent = covered ? 'Show the toolkit' : 'Cover the toolkit';
}
function pickScene(i,btn){
  document.querySelectorAll('#scn-chips .chip').forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
  var s = SCENES[i];
  document.getElementById('rc-where').textContent = s.where;
  document.getElementById('rc-happened').textContent = s.happened;
  document.getElementById('rc-have').textContent = s.have;
  document.getElementById('rc-want').textContent = s.want;
  document.getElementById('oc-name').textContent = s.name;
  document.getElementById('oc-desc').textContent = s.desc;
}
var lastTwist = -1;
function drawTwist(){
  var n; do { n = Math.floor(Math.random()*TWISTS.length); } while(n === lastTwist);
  lastTwist = n;
  var box = document.getElementById('twist-card');
  box.textContent = TWISTS[n];
  box.scrollIntoView({behavior:'smooth', block:'center'});
}
var lastCue = -1;
function drawCue(){
  var n; do { n = Math.floor(Math.random()*CUES.length); } while(n === lastCue);
  lastCue = n;
  document.getElementById('cue-card').textContent = CUES[n].cue;
  var ans = document.getElementById('cue-ans');
  ans.classList.remove('open'); ans.textContent = '';
  document.getElementById('cue-ans-btn').style.display = 'inline-block';
}
function showCueAns(){
  var ans = document.getElementById('cue-ans');
  ans.textContent = CUES[lastCue].ans;
  ans.classList.add('open');
}
pickScene(0, document.querySelector('#scn-chips .chip'));
"""

TIMER_JS = """
var timerInterval = null;
var timeRemaining = 240;
var currentDuration = 240;
function setDuration(btn, minutes){
    if(timerInterval){ clearInterval(timerInterval); timerInterval = null; }
    document.querySelectorAll('.duration-btn').forEach(function(b){ b.classList.remove('active'); });
    btn.classList.add('active');
    currentDuration = minutes * 60;
    timeRemaining = currentDuration;
    updateDisplay();
    document.querySelector('.timer').classList.remove('warning','danger');
}
function updateDisplay(){
    var m = Math.floor(timeRemaining / 60);
    var s = timeRemaining % 60;
    document.getElementById('timer-display').textContent = m + ':' + (s < 10 ? '0' : '') + s;
}
function resetTimer(){
    if(timerInterval){ clearInterval(timerInterval); timerInterval = null; }
    timeRemaining = currentDuration;
    updateDisplay();
    document.querySelector('.timer').classList.remove('warning','danger');
}
function startTimer(){
    if(timerInterval) return;
    timerInterval = setInterval(function(){
        timeRemaining--;
        updateDisplay();
        var t = document.querySelector('.timer');
        if(timeRemaining <= 10){ t.classList.add('danger'); t.classList.remove('warning'); }
        else if(timeRemaining <= 30){ t.classList.add('warning'); t.classList.remove('danger'); }
        else { t.classList.remove('warning','danger'); }
        if(timeRemaining <= 0){
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById('timer-display').textContent = "Time's up!";
        }
    }, 1000);
}
"""

def e(t):
    return html.escape(t, quote=False)

def phrases_panel(c):
    shape = ''.join('<span>%d · %s</span>' % (i + 1, e(g['move'].split(' ', 1)[1])) for i, g in enumerate(c['groups']))
    groups = ''
    for g in c['groups']:
        groups += '            <div class="tk-group"><div class="tk-move">%s</div>\n' % e(g['move'])
        for p in g['phrases']:
            groups += '                <div class="tk-phrase">"%s"</div>\n' % e(p)
        if g.get('tip'):
            groups += '                <div class="tk-tip">%s</div>\n' % e(g['tip'])
        groups += '            </div>\n'
    def alt(title, items):
        out = '            <h3>%s</h3>\n            <div class="tk-group alt">\n' % e(title)
        for p in items:
            out += '                <div class="tk-phrase">"%s"</div>\n' % e(p)
        return out + '            </div>\n'
    return f'''    <div class="panel" id="p1">
        <h2>Useful Phrases <span class="em">🧰</span></h2>
        <p class="lead">{e(c['intro'])}</p>

        <div class="shape-label">The shape of this conversation</div>
        <div class="shape">{shape}</div>
        <div class="shape-note">It's a map, not a script. Real conversations skip steps, repeat them and go off in new directions.</div>

        <div class="kit-bar">
            <button class="rev-btn" id="kit-toggle" onclick="toggleKit(this)">Cover the toolkit</button>
            <span class="kit-note">Cover it later, when you want to test yourself.</span>
        </div>

        <div id="kit">
            <h3>When you're {e(c['you_are'])}</h3>
{groups}
            {alt("When you're " + c['other_is'], c['other_phrases'])}
            {alt('When something changes', c['change_phrases'])}
            {alt('Whenever you need a moment, or you missed something', REPAIR)}
        </div>

        <h3>Speed round 🎯</h3>
        <p class="lead">Draw a card and say what you'd say, out loud, in one or two sentences. Use your own words or the toolkit. Then peek at one possible answer.</p>
        <button class="rev-btn" onclick="drawCue()">Draw a card</button>
        <div class="cue-card" id="cue-card">Press the button to start.</div>
        <button class="rev-btn" id="cue-ans-btn" style="display:none" onclick="showCueAns()">One possible answer</button>
        <div class="rev" id="cue-ans"></div>
        <p class="lead" style="margin-top:14px">Done a few rounds? Try again with the toolkit covered. When it flows, you're ready to hear them in a real conversation.</p>
    </div>
'''

def turn_panel(c):
    warm = ''.join('            <li><b>%s</b> %s</li>\n' % (e(b), e(r)) for b, r in c['warmup'])
    chips = ''.join('            <button class="chip%s" onclick="pickScene(%d,this)">%s</button>\n' % (' active' if i == 0 else '', i, e(s['chip'])) for i, s in enumerate(c['scenes']))
    swap = ''.join('            <div class="rc-row"><b>%s</b><span>%s</span></div>\n' % (e(a), e(b)) for a, b in c['swap'])
    ticks = ''.join('            <label><input type="checkbox"> %s</label>\n' % e(t) for t in c['ticks'])
    return f'''    <div class="panel" id="p3">
        <h2>Your Turn <span class="em">🎭</span></h2>
        <p class="lead">No script this time. You'll have a real conversation with a real person. They have their own mind, and you have a goal.</p>

        <h3>1 · Warm up your voice 🎤</h3>
        <p class="lead">Say each step once, out loud, in your own words. No writing, no peeking at the phrases.</p>
        <ol class="moves">
{warm}        </ol>

        <h3>2 · The scene 🎬</h3>
        <p class="lead">Pick your situation. Your partner plays the other person.</p>
        <div class="chips" id="scn-chips">
{chips}        </div>

        <div class="rolecard" id="rolecard">
            <div class="rc-tag">Your card</div>
            <div class="rc-row"><b>Where</b><span id="rc-where"></span></div>
            <div class="rc-row"><b>The situation</b><span id="rc-happened"></span></div>
            <div class="rc-row"><b>You have</b><span id="rc-have"></span></div>
            <div class="rc-row"><b>You want</b><span id="rc-want"></span></div>
            <div class="rc-row"><b>Your rule</b><span>{e(c['rule'])}</span></div>
        </div>
        <div class="rolecard other" id="othercard">
            <div class="rc-tag">Who you're talking to</div>
            <div class="rc-row"><b id="oc-name"></b><span id="oc-desc"></span></div>
        </div>
        <p class="winline">🏆 {e(c['win'])}</p>

        <div class="timer">
            <div>⏱ <span class="timer-display" id="timer-display">4:00</span></div>
            <div class="timer-controls">
                <button class="duration-btn active" onclick="setDuration(this,4)">4 min</button>
                <button class="duration-btn" onclick="setDuration(this,6)">6 min</button>
                <button class="timer-btn" onclick="startTimer()">Start</button>
                <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
            </div>
        </div>

        <div class="twist">
            <span class="t-label">Twist deck</span>
            <h3>🎲 Something changes</h3>
            <p>Start the scene first. Partway through, draw a card. Whatever it says, it just happened.</p>
            <button class="rev-btn" onclick="drawTwist()">Draw a twist</button>
            <div class="twist-card" id="twist-card">Nothing has changed yet.</div>
        </div>

        <h3>3 · Swap seats 🔁</h3>
        <p class="lead">Now you're on the other side. Your partner takes your old part.</p>
        <div class="rolecard">
            <div class="rc-tag">Your card</div>
{swap}        </div>
        <p class="lead">Draw another twist whenever you like.</p>

        <h3>4 · Afterwards ✅</h3>
        <p class="lead">Tick what you actually did, in either seat.</p>
        <div class="checks">
{ticks}        </div>
        <h3>Phrases I want to use next time</h3>
        <textarea class="blank" placeholder="Jot down two or three phrases you liked, from either side…"></textarea>

        <div class="twist">
            <span class="t-label">Go again</span>
            <h3>⚡ Same situation, harder</h3>
            <p>Run it one more time. Draw a twist before you start, and try to reach a good result faster than before.</p>
            <button class="rev-btn" onclick="drawTwist()">Draw a twist</button>
        </div>
    </div>
'''

def js_data(c):
    scenes = [{k: s[k] for k in ('where', 'happened', 'have', 'want', 'name', 'desc')} for s in c['scenes']]
    return ('var SCENES = %s;\nvar TWISTS = %s;\nvar CUES = %s;\n' % (
        json.dumps(scenes, ensure_ascii=False, indent=1),
        json.dumps(c['twists'], ensure_ascii=False, indent=1),
        json.dumps(c['cues'], ensure_ascii=False, indent=1)))

def teacher_sheet(c):
    secrets = ''.join('<div class="card"><b>%s:</b> %s</div>\n' % (e(a), e(b)) for a, b in c['secrets'])
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex">
<title>Teacher sheet · {e(c['title'])}</title>
<style>
body{{font-family:system-ui,sans-serif;background:#fbf7f0;color:#2b2b33;line-height:1.55;max-width:720px;margin:0 auto;padding:18px;font-size:16px}}
h1{{font-size:1.4rem;margin:0 0 4px}}h2{{font-size:1.05rem;color:#237884;margin:20px 0 6px}}
.card{{background:#fff;border:1px solid #e8e0d3;border-radius:12px;padding:12px 16px;margin:8px 0}}
ul,ol{{margin:4px 0 4px 20px}}li{{margin:3px 0}}.small{{color:#6f685d;font-size:.9rem}}
</style></head><body>
<h1>{e(c['title'])} — teacher sheet</h1>
<p class="small">Keep this on a second screen. Not for sharing. Conversation family: {e(c['family'])}.</p>

<h2>Flow (about 50 min)</h2>
<ol>
<li>Scene tab, then Useful Phrases: read the toolkit aloud together, then the speed round (about 15 min).</li>
<li>Conversation tab: read it aloud one role each, then the from-memory questions (about 10 min).</li>
<li>Your Turn step 1: student says the steps aloud (3 min).</li>
<li>Step 2, run 1: you play the other person (5 min). Take notes while you listen.</li>
<li>Feedback (3 min): two things that worked, two phrases to fix.</li>
<li>Step 3, swap: you take the student's part and model one or two toolkit phrases naturally (5 min).</li>
<li>Go again, harder: same situation plus a twist (5 min). Close with the Afterwards ticks.</li>
</ol>

<h2>Your three moves as the other person</h2>
<div class="card"><ul>
<li><b>Push back once.</b> Say no, or quote a rule, the first time they ask, however good the request is.</li>
<li><b>Misunderstand once.</b> Mishear or take the wrong meaning. It makes them rephrase or use a repair phrase, which is the real skill.</li>
<li><b>Give new information.</b> Offer an option they didn't ask for.</li>
</ul></div>

<h2>The other person's secrets</h2>
{secrets}
<h2>Difficulty</h2>
<ul><li><b>Easier:</b> say yes a little sooner, repeat a question slowly, hint at the next step.</li>
<li><b>Harder:</b> stay firm two extra exchanges, speak at natural speed, draw a twist right at the start.</li></ul>

<h2>While listening</h2>
<ul><li>Don't interrupt to correct. Write down 2 things that worked and 2 phrases to fix (word choice or tone, not every slip).</li>
<li>Say the corrected phrase back once, then have them use it in the next run.</li>
<li>Keep feedback mostly positive: pronunciation, tone, creativity.</li></ul>
</body></html>
'''

def split_panels(s):
    """Return (head, [panel blocks], tail). Panel marker comments are dropped."""
    starts = [m.start() for m in re.finditer(r'[ \t]*<div class="panel[^"]*" id="p\d">', s)]
    if '<footer' in s:
        foot = s.rfind('\n', 0, s.index('<footer')) + 1
    else:
        foot = s.rfind('\n</div>', 0, s.index('<script>')) + 1
    blocks = [s[starts[i]:(starts[i + 1] if i + 1 < len(starts) else foot)] for i in range(len(starts))]
    blocks = [re.sub(r'(\n[ \t]*<!--[^\n]*-->[ \t]*)+\s*$', '\n', b) for b in blocks]
    return s[:starts[0]], blocks, s[foot:]

def title_of(block):
    return re.search(r'<h2>([A-Za-z ]+)', block).group(1).strip()

def wire(path, c):
    s = open(path).read()
    head, blocks, tail = split_panels(s)
    by = {title_of(b): b for b in blocks}
    order = [by['The Scene'], phrases_panel(c), by['The Conversation'], turn_panel(c), by['The Echo']]
    order = [re.sub(r'id="p\d"', 'id="p%d"' % i, o, count=1) for i, o in enumerate(order)]
    order = [re.sub(r'class="panel( active)?"', 'class="panel active"' if i == 0 else 'class="panel"', o, count=1) for i, o in enumerate(order)]
    s = head + '\n'.join(o.rstrip('\n') + '\n' for o in order) + '\n' + tail
    s = re.sub(r'<button class="tab-btn[^"]*" onclick="showTab\(\d\)">[^<]*</button>\s*', '', s)
    tabs = ['🎬 The Scene', '🧰 Useful Phrases', '💬 The Conversation', '🎭 Your Turn', '🕰️ The Echo']
    btns = ''.join('        <button class="tab-btn%s" onclick="showTab(%d)">%s</button>\n' % (' active' if i == 0 else '', i, t) for i, t in enumerate(tabs))
    s = s.replace('<div class="tabs">\n', '<div class="tabs">\n' + btns, 1)
    s = re.sub(r'<b>First:</b> read the conversation in the next tab\.', "<b>Next:</b> pick up the phrases you'll need in the next tab, then watch them at work in a real conversation.", s)
    s = s.replace('Read it out loud, one role each — then swap. ', 'Read it out loud, one role each, then swap. Spot as many phrases from your toolkit as you can. ')
    s = re.sub(re.escape(CSS_START) + r'.*?' + re.escape(CSS_END) + r'\n?', '', s, flags=re.S)
    s = re.sub(re.escape(JS_START) + r'.*?' + re.escape(JS_END) + r'\n?', '', s, flags=re.S)
    s = s.replace('</style>', CSS_START + CSS + CSS_END + '\n</style>', 1)
    js = JS_START + js_data(c) + JS_FIXED + JS_END + '\n'
    if 'function startTimer' not in s:
        js = JS_START + TIMER_JS + js_data(c) + JS_FIXED + JS_END + '\n'
    s = s.replace('</script>\n</body>', js + '</script>\n</body>', 1)
    open(path, 'w').write(s)

def main(names):
    for n in names:
        c = CONFIGS[n]
        path = os.path.join(ROOT, c['file'])
        wire(path, c)
        os.makedirs(os.path.join(ROOT, 'teacher'), exist_ok=True)
        open(os.path.join(ROOT, 'teacher', c['file']), 'w').write(teacher_sheet(c))
        print('built', c['file'])

if __name__ == '__main__':
    main(sys.argv[1:])
