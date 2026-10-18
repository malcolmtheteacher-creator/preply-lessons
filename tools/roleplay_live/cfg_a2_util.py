"""Helpers for the A2/B1 configs: 4 groups of 2 short phrases, sentence frames, 3 scenes."""
from cfg_util import S, C  # noqa: F401  (re-exported)

REPAIR_A2 = [
    "Sorry, can you say that again, please?",
    "Can you speak more slowly, please?",
    "Do you mean…?",
    "How do you say … in English?",
]

INTRO_A2 = ("Here are the phrases for this conversation. Read each one and say it out loud once. "
            "Choose the ones you like. Keep this page open when you practise.")


def G2(move, do, frame, a, b):
    """One move: a label (emoji + words), what it does, a sentence frame, two phrases."""
    return {'move': move, 'do': do, 'frame': frame, 'phrases': [a, b]}


def lesson_a2(family, you_are, groups, other_is, other_phrases, change_phrases, cues, scenes,
              swap, twists, ticks, secrets, rule, win, own_where='Somewhere you choose'):
    own = S('⭐ My own', own_where,
            'Think of a real situation like this one. Tell your partner the basics.',
            'What you really have.', 'What you really want.', 'Your partner',
            'Plays the other person. Agree the details together first.')
    warm = [(g['move'].split(' ', 1)[1].rstrip('.') + '.', g['frame']) for g in groups]
    cues = list(cues) + [C("You did not understand. Ask them to say it again.", REPAIR_A2[0])]
    ticks = list(ticks) + ['I asked again when I did not understand.']
    return {
        'family': family, 'intro': INTRO_A2, 'you_are': you_are, 'groups': groups,
        'other_is': other_is, 'other_phrases': other_phrases, 'change_phrases': change_phrases,
        'cues': cues, 'warmup': warm, 'scenes': list(scenes) + [own], 'rule': rule, 'win': win,
        'swap': swap, 'twists': twists, 'ticks': ticks,
        'secrets': list(secrets) + [('Their own situation', 'agree the details together in 30 seconds, then use the same four steps.')],
    }
