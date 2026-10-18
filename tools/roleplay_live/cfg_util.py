"""Helpers for writing lesson configs compactly."""
from configs_repair import REPAIR

INTRO = ("Here's your toolkit. You don't need to memorise it. Read each phrase, say it out loud once, "
         "and pick the ones that sound like you. You'll have it open while you practise.")

def G(move, do, *phrases, tip=None):
    g = {'move': move, 'do': do, 'phrases': list(phrases)}
    if tip:
        g['tip'] = tip
    return g

def S(chip, where, happened, have, want, name, desc):
    return {'chip': chip, 'where': where, 'happened': happened, 'have': have, 'want': want, 'name': name, 'desc': desc}

def C(cue, ans):
    return {'cue': cue, 'ans': '"%s"' % ans}

def lesson(file, title, family, you_are, groups, other_is, other_phrases, change_phrases, cues, scenes,
           swap, twists, ticks, secrets, rule, win, own_where='Somewhere you choose'):
    own = S('⭐ My own', own_where,
            'Think of a real situation like this one that you have been in, or expect to be in. Tell your partner the basics.',
            'Whatever you really would have.', 'The result you would honestly want.', 'Your partner',
            'Plays the other person. Agree the details together first.')
    warm = [(g['move'].split(' ', 1)[1].rstrip('.') + '.', g['do']) for g in groups]
    cues = list(cues) + [C("The other person talks so fast you lose the thread.", REPAIR[0])]
    ticks = list(ticks) + ['I asked again, or checked, when I missed something.']
    return {
        'file': file, 'title': title, 'family': family, 'intro': INTRO, 'you_are': you_are,
        'groups': groups, 'other_is': other_is, 'other_phrases': other_phrases,
        'change_phrases': change_phrases, 'cues': cues, 'warmup': warm,
        'scenes': list(scenes) + [own], 'rule': rule, 'win': win, 'swap': swap,
        'twists': twists, 'ticks': ticks, 'secrets': list(secrets) + [('Their own situation', 'agree the details together in 30 seconds, then use the three moves.')],
    }
