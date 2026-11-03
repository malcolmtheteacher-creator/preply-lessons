#!/usr/bin/env python3
"""A2/B1 mode: rebuild the Useful Phrases and Your Turn panels of the *_a2b1.html
roleplay twins from configs in cfg_a2_f1.py ... cfg_a2_f6.py. Same structure-based,
idempotent approach as build.py (reuses its CSS, JS, panel splitting and the shared
helpers), with simpler wording, sentence frames, a smaller repair set and 3 scenes.

Usage: python3 tools/roleplay_live/build_a2.py rp_09 [rp_02 ...]     (or: all)
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
from build import e, ROOT, CSS_START, CSS_END, JS_START, JS_END  # noqa: E402
from configs_a2 import CONFIGS_A2, REPAIR_A2  # noqa: E402


def phrases_panel(c):
    shape = ''.join('<span>%d · %s</span>' % (i + 1, e(g['move'].split(' ', 1)[1])) for i, g in enumerate(c['groups']))
    groups = ''
    for g in c['groups']:
        groups += '            <div class="tk-group"><div class="tk-move">%s</div>\n' % e(g['move'])
        for p in g['phrases']:
            groups += '                <div class="tk-phrase">"%s"</div>\n' % e(p)
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
        <div class="shape-note">It's a map, not a script. Real talk can skip steps or go back.</div>

        <div class="kit-bar">
            <button class="rev-btn" id="kit-toggle" onclick="toggleKit(this)">Cover the toolkit</button>
            <span class="kit-note">Cover it later, when you want to test yourself.</span>
        </div>

        <div id="kit">
            <h3>When you're {e(c['you_are'])}</h3>
{groups}
            {alt("When you're " + c['other_is'], c['other_phrases'])}
            {alt('When something changes', c['change_phrases'])}
            {alt('When you need help', REPAIR_A2)}
        </div>

        <h3>Speed round 🎯</h3>
        <p class="lead">Draw a card. Say what you would say, out loud. Then look at one answer.</p>
        <button class="rev-btn" onclick="drawCue()">Draw a card</button>
        <div class="cue-card" id="cue-card">Press the button to start.</div>
        <button class="rev-btn" id="cue-ans-btn" style="display:none" onclick="showCueAns()">One possible answer</button>
        <div class="rev" id="cue-ans"></div>
        <p class="lead" style="margin-top:14px">Try a few more rounds with the toolkit covered. When it feels easy, you are ready.</p>
    </div>
'''


def turn_panel(c):
    warm = ''.join('            <li><b>%s</b> %s</li>\n' % (e(b), e(r)) for b, r in c['warmup'])
    chips = ''.join('            <button class="chip%s" onclick="pickScene(%d,this)">%s</button>\n' % (' active' if i == 0 else '', i, e(s['chip'])) for i, s in enumerate(c['scenes']))
    swap = ''.join('            <div class="rc-row"><b>%s</b><span>%s</span></div>\n' % (e(a), e(b)) for a, b in c['swap'])
    ticks = ''.join('            <label><input type="checkbox"> %s</label>\n' % e(t) for t in c['ticks'])
    return f'''    <div class="panel" id="p3">
        <h2>Your Turn <span class="em">🎭</span></h2>
        <p class="lead">No script this time. You have a real talk with a real person. You have a goal.</p>

        <h3>1 · Warm up your voice 🎤</h3>
        <p class="lead">Say each sentence out loud. Use your own words in the gaps.</p>
        <ol class="moves">
{warm}        </ol>

        <h3>2 · The scene 🎬</h3>
        <p class="lead">Pick a situation. Your partner plays the other person.</p>
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
            <div>⏱ <span class="timer-display" id="timer-display">3:00</span></div>
            <div class="timer-controls">
                <button class="duration-btn active" onclick="setDuration(this,3)">3 min</button>
                <button class="duration-btn" onclick="setDuration(this,5)">5 min</button>
                <button class="timer-btn" onclick="startTimer()">Start</button>
                <button class="timer-btn secondary" onclick="resetTimer()">Reset</button>
            </div>
        </div>

        <div class="twist">
            <span class="t-label">Twist deck</span>
            <h3>🎲 Something changes</h3>
            <p>Start the scene. After a minute, draw a card. What it says just happened.</p>
            <button class="rev-btn" onclick="drawTwist()">Draw a twist</button>
            <div class="twist-card" id="twist-card">Nothing has changed yet.</div>
        </div>

        <h3>3 · Swap seats 🔁</h3>
        <p class="lead">Now you are the other person. Your partner takes your old part.</p>
        <div class="rolecard">
            <div class="rc-tag">Your card</div>
{swap}        </div>
        <p class="lead">Draw another twist if you like.</p>

        <h3>4 · Afterwards ✅</h3>
        <p class="lead">Tick what you did, in either seat.</p>
        <div class="checks">
{ticks}        </div>
        <h3>Phrases I want to use next time</h3>
        <textarea class="blank" placeholder="Write two or three phrases you liked…"></textarea>

        <div class="twist">
            <span class="t-label">Go again</span>
            <h3>⚡ Same situation, one more time</h3>
            <p>Do it again. Draw a twist before you start. Try to do it faster this time.</p>
            <button class="rev-btn" onclick="drawTwist()">Draw a twist</button>
        </div>
    </div>
'''


def wire(path, c):
    s = open(path).read()
    head, blocks, tail = B.split_panels(s)
    by = {B.title_of(b): b for b in blocks}
    order = [by['The Scene'], phrases_panel(c), by['The Conversation'], turn_panel(c), by['The Echo']]
    order = [re.sub(r'id="p\d"', 'id="p%d"' % i, o, count=1) for i, o in enumerate(order)]
    order = [re.sub(r'class="panel( active)?"', 'class="panel active"' if i == 0 else 'class="panel"', o, count=1) for i, o in enumerate(order)]
    s = head + '\n'.join(o.rstrip('\n') + '\n' for o in order) + '\n' + tail
    s = re.sub(r'<button class="tab-btn[^"]*" onclick="showTab\(\d\)">[^<]*</button>\s*', '', s)
    tabs = ['🎬 The Scene', '🧰 Useful Phrases', '💬 The Conversation', '🎭 Your Turn', '🕰️ The Echo']
    btns = ''.join('        <button class="tab-btn%s" onclick="showTab(%d)">%s</button>\n' % (' active' if i == 0 else '', i, t) for i, t in enumerate(tabs))
    s = s.replace('<div class="tabs">\n', '<div class="tabs">\n' + btns, 1)
    s = s.replace('<b>First:</b> read the conversation in the next tab.', "<b>Next:</b> learn the phrases you need in the next tab. Then see them in a real conversation.")
    s = s.replace('Read it out loud, one person each — then change. ', 'Read it out loud, one person each, then change. Find the phrases from your toolkit. ')
    s = re.sub(re.escape(CSS_START) + r'.*?' + re.escape(CSS_END) + r'\n?', '', s, flags=re.S)
    s = re.sub(re.escape(JS_START) + r'.*?' + re.escape(JS_END) + r'\n?', '', s, flags=re.S)
    s = s.replace('</style>', CSS_START + B.CSS + CSS_END + '\n</style>', 1)
    assert 'function startTimer' in s, path
    js = JS_START + B.js_data(c) + B.JS_FIXED + JS_END + '\n'
    s = s.replace('</script>\n</body>', js + '</script>\n</body>', 1)
    open(path, 'w').write(s)


def main(names):
    if names == ['all']:
        names = sorted(CONFIGS_A2)
    for n in names:
        c = dict(CONFIGS_A2[n])
        path = glob.glob(os.path.join(ROOT, n + '_*_a2b1.html'))[0]
        c['file'] = os.path.basename(path)
        c['title'] = re.search(r'<title>Everyday Echoes · (.*?) \(A2/B1\)', open(path).read()).group(1).replace('&amp;', '&')
        wire(path, c)
        os.makedirs(os.path.join(ROOT, 'teacher'), exist_ok=True)
        open(os.path.join(ROOT, 'teacher', c['file']), 'w').write(B.teacher_sheet(c))
        print('built', c['file'])


if __name__ == '__main__':
    main(sys.argv[1:])
