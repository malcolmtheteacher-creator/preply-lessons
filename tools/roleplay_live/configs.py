"""Per-lesson content for build.py. Student-facing text only, except `secrets` and `family`
which go to the separate teacher sheet."""

# Shared by every roleplay: the repair set students can use in any conversation.
from configs_repair import REPAIR  # noqa: E402,F401

CONFIGS = {}

CONFIGS['rp_09'] = {
    'file': 'rp_09_making_a_complaint.html',
    'title': 'Making a Complaint',
    'family': '2 · Fixing a problem',
    'intro': "Here's your toolkit. You don't need to memorise it. Read each phrase, say it out loud once, and pick the ones that sound like you. You'll have it open while you practise.",
    'you_are': 'the customer',
    'groups': [
        {'move': '🚪 Open gently', 'phrases': [
            "I'm afraid I've got a bit of a problem with something I bought here.",
            "Sorry to bother you, but there's something I need to sort out.",
            "I wonder if you could help me with something?"]},
        {'move': '🤝 Take them off the hook', 'phrases': [
            "I'm sure this isn't your fault, but…",
            "I know you didn't make it, but…"]},
        {'move': '🔍 Say what\'s wrong', 'phrases': [
            "It's faulty.",
            "This isn't quite what I was led to expect.",
            "It stopped working after just a few days."],
         'tip': 'Say "faulty", not "I don\'t like it". It puts the responsibility on the shop.'},
        {'move': '📈 Push, politely', 'phrases': [
            "I'm sure you can appreciate how frustrating this is.",
            "I'd hate to have to take this further.",
            "Could I speak to the manager, please?"]},
        {'move': '🎯 Ask for what you want', 'phrases': [
            "What I'd really like is a refund, or a replacement if that's simpler.",
            "Is this something you'd be able to sort out for me today?"]},
        {'move': '🌟 Make a deal and close', 'phrases': [
            "Could we meet halfway on this?",
            "That's genuinely kind of you. Thank you for sorting it out."]},
    ],
    'other_is': 'behind the counter',
    'other_phrases': [
        "I'm sorry about that. Let's see if we can put it right.",
        "I'm afraid our policy is…",
        "Let me see what I can do.",
        "I can't promise anything, but…",
        "What I can offer you is…"],
    'change_phrases': [
        "I understand, but it was faulty when I bought it.",
        "I'd rather not take a voucher, if that's all right.",
        "I'm not comfortable signing that.",
        "Is there anyone else I could speak to?"],
    'cues': [
        {'cue': "You walk up to the counter. Your phone case cracked in a week. Start the conversation.", 'ans': "\"Sorry to bother you, but there's something I need to sort out. This phone case I bought last week has already cracked.\""},
        {'cue': "The assistant looks worried. Reassure them before you push.", 'ans': "\"I'm sure this isn't your fault, but…\""},
        {'cue': "The assistant says it's just wear and tear. Say what you think it really is.", 'ans': "\"I understand, but it was faulty when I bought it.\""},
        {'cue': "The assistant keeps stalling. Show you might escalate, but politely.", 'ans': "\"I'd hate to have to take this further.\""},
        {'cue': "They ask what you want. Be clear, but give them an easy option.", 'ans': "\"What I'd really like is a refund, or a replacement if that's simpler.\""},
        {'cue': "You want a firm commitment, today.", 'ans': "\"Is this something you'd be able to sort out for me today?\""},
        {'cue': "They can't refund you but offer something else. Suggest a compromise.", 'ans': "\"Could we meet halfway on this?\""},
        {'cue': "They solved it. Close the conversation warmly.", 'ans': "\"That's genuinely kind of you. Thank you for sorting it out.\""},
        {'cue': "You're the assistant. A customer is angry about a faulty toaster. Start gently.", 'ans': "\"I'm sorry about that. Let's see if we can put it right.\""},
        {'cue': "You're the assistant. The returns window has passed. Explain.", 'ans': "\"I'm afraid our policy is fourteen days, and it's been eighteen.\""},
        {'cue': "You're offered a voucher, but you want your money back.", 'ans': "\"I'd rather not take a voucher, if that's all right.\""},
        {'cue': "They ask you to sign something saying it was your fault.", 'ans': "\"I'm not comfortable signing that.\""},
        {'cue': "The assistant speaks very fast and you lose the thread.", 'ans': "\"Sorry, I didn't quite catch that. Could you say it again?\""},
    ],
    'warmup': [
        ('Open gently.', 'Flag the problem and take the pressure off the other person.'),
        ("Say what's wrong.", 'Be exact. Use the word that makes it their responsibility.'),
        ('Redirect.', "Agree it's the usual route, then explain why it's not the right one here."),
        ('Hold firm, smiling.', 'Turn the pressure up a notch without turning rude.'),
        ('Name what you want.', 'A replacement or a refund, and make it easy to say yes.'),
        ('Close warmly.', 'Reward them for helping.'),
    ],
    'scenes': [
        {'chip': '🎧 Headphones', 'where': 'A small electronics shop', 'happened': 'Your headphones have a crackle in the left ear. You bought them 18 days ago.', 'have': 'The receipt, in an email on your phone.', 'want': 'A replacement pair, or your money back.', 'name': 'Dana, shop assistant', 'desc': 'Friendly and busy. Sticks to the rules until you give a good reason not to.'},
        {'chip': '🥤 Blender', 'where': 'A kitchen shop', 'happened': 'Your new blender leaks all over the worktop. You bought it last week.', 'have': 'The blender. The receipt is somewhere at home.', 'want': 'A working blender, or a refund.', 'name': 'Sam, shop assistant', 'desc': 'Polite but cautious. Worried about getting in trouble for bending the rules.'},
        {'chip': '🏨 Hotel room', 'where': 'A hotel front desk, late evening', 'happened': 'You booked a quiet room facing the garden. Yours faces the road and the noise is awful.', 'have': 'Your booking confirmation.', 'want': 'A quiet room, tonight, with no extra charge.', 'name': 'Alex, receptionist', 'desc': 'Tired at the end of a long shift. The hotel is almost full.'},
        {'chip': '⭐ My own', 'where': 'Somewhere you choose', 'happened': 'Think of something that really annoyed you recently and tell your partner the basics.', 'have': 'Whatever you really had.', 'want': 'A fair result you would honestly be happy with.', 'name': 'Your partner', 'desc': 'Plays the person on the other side. Agree the details together first.'},
    ],
    'rule': "Stay warm. The moment you get rude, you've lost.",
    'win': 'You win when they say yes, and they still like you.',
    'swap': [
        ('Who you are', 'An assistant at a home-appliance shop. Invent your name and the shop.'),
        ('The rules', "14 days to return something you've changed your mind about. Two years if it's faulty and there's proof."),
        ('Your power', "You can bend one rule if the customer is polite and reasonable. Don't give in at the first push."),
        ('Your goal', "Be fair, stay friendly, and keep the shop's money where you can."),
    ],
    'twists': [
        'The shop computer has been down all morning, so there is no record of your purchase.',
        'A manager has just walked up and heard half of what you said.',
        'You are offered a voucher instead of a refund. You do not want a voucher.',
        'The shop closes in five minutes and there is a queue behind you.',
        'The assistant suspects the damage was your fault.',
        'The assistant is brand new and has no idea what the policy is.',
        'A replacement is possible, but it will take three weeks to arrive.',
        'The assistant is extremely friendly, but keeps saying it is simply impossible.',
        'You have just seen the same item for less in the shop window.',
        'A full refund is offered at once, but you must sign to say it was your fault.',
    ],
    'ticks': [
        'I said what was wrong in one clear sentence.',
        'I used "faulty" (or my own strong word) and stayed polite.',
        'I said exactly what I wanted.',
        'I gave the other person a graceful way to say yes.',
        'I asked again, or checked, when I missed something.',
        'I closed the conversation warmly.',
    ],
    'secrets': [
        ('Headphones (Dana)', "gives way if asked about the guarantee for faulty goods, or if the student stays warm for three exchanges. Pushes the manufacturer's helpline first."),
        ('Blender (Sam)', 'nervous. Says yes to a replacement once the student offers an easy way for Sam to justify it ("it\'s clearly faulty, so no one could blame you").'),
        ('Hotel (Alex)', 'only one quiet room is free, a smaller one. Offers a free breakfast instead first. Gives in if the student stays calm and repeats exactly what was booked.'),
        ('Their own situation', 'agree the details together in 30 seconds, then use the three moves.'),
    ],
}

CONFIGS['rp_02'] = {
    'file': 'rp_02_ordering_at_a_cafe.html',
    'title': 'Ordering at a Café',
    'family': '1 · Getting a service',
    'intro': "Here's your toolkit. You don't need to memorise it. Read each phrase, say it out loud once, and pick the ones that sound like you. You'll have it open while you practise.",
    'you_are': 'the customer',
    'groups': [
        {'move': '🚪 Order lightly', 'phrases': [
            "When you've got a sec, could I get a flat white?",
            "No rush, I can see you're swamped.",
            "Eat in, please."]},
        {'move': '🤔 Ask for a steer', 'phrases': [
            "I can never make my mind up. What would you go for?",
            "Which one would you have?",
            "Are the scones homemade today?"]},
        {'move': '🛠 Make it yours', 'phrases': [
            "Could I have the flat white with oat milk, if that's possible?",
            "Would it be possible to have it extra hot?",
            "Could I have that without cream?"]},
        {'move': '🔄 Change your mind', 'phrases': [
            "On second thoughts, could I swap the croissant for the scone?",
            "Sorry to chop and change, but could the flat white be a decaf?",
            "Actually, you know what… could I make that a large?"],
         'tip': 'Apologise for the change first, lightly and with a smile, and nobody minds.'},
        {'move': '🍽 Flag a mix-up', 'phrases': [
            "I think there might have been a bit of a mix-up.",
            "I'm not fussed, but I did order a decaf flat white.",
            "No harm done. Take your time."]},
        {'move': '💳 Pay and close', 'phrases': [
            "Do you take card?",
            "Could I settle up, please?",
            "That's really not necessary… but I won't pretend I'll say no.",
            "Let's call it a round six. Keep the change."]},
    ],
    'other_is': 'behind the counter',
    'other_phrases': [
        "Morning! What can I get you?",
        "Eat in or takeaway?",
        "Anything with that?",
        "I'm afraid we've just run out of those.",
        "That's entirely my fault. Let me start again.",
        "Tell you what, have that one on the house."],
    'change_phrases': [
        "Sorry, I'm in a bit of a rush. How long will it be?",
        "Is there anything in this with nuts? I'm allergic.",
        "Could I have something else instead, then?",
        "Could we split the bill?"],
    'cues': [
        {'cue': "The café is packed. Get the barista's attention without pushing.", 'ans': "\"No rush, I can see you're swamped. When you've got a sec, could I get a flat white?\""},
        {'cue': "You can't choose between a muffin and a brownie. Ask the barista.", 'ans': "\"I can never make my mind up. What would you go for?\""},
        {'cue': "You want your tea with oat milk. Ask politely.", 'ans': "\"Could I have the tea with oat milk, if that's possible?\""},
        {'cue': "You ordered a croissant but a scone looks better. Change it.", 'ans': "\"On second thoughts, could I swap the croissant for the scone?\""},
        {'cue': "You've already changed your order once. You want to change it again.", 'ans': "\"Sorry to chop and change, but could I make that a decaf?\""},
        {'cue': "The wrong drink arrives. Say so without blaming anyone.", 'ans': "\"I think there might have been a bit of a mix-up. I'm not fussed, but I did order a latte.\""},
        {'cue': "The barista says sorry for the mistake. Reassure them.", 'ans': "\"No harm done. Take your time.\""},
        {'cue': "You're offered a free cake for the wait. Accept graciously.", 'ans': "\"That's really not necessary… but I won't pretend I'll say no.\""},
        {'cue': "You're the barista. They ask for something you've run out of.", 'ans': "\"I'm afraid we've just run out of those. Can I get you something else?\""},
        {'cue': "You're the barista. You gave the wrong order. Apologise and fix it.", 'ans': "\"That's entirely my fault. Let me start again.\""},
        {'cue': "The card machine isn't working and you only have a little cash.", 'ans': "\"Is there any chance of paying by card? If not, I've only got a few coins.\""},
        {'cue': "The barista talks so fast you miss what they said.", 'ans': "\"Sorry, I didn't quite catch that. Could you say it again?\""},
    ],
    'warmup': [
        ('Order lightly.', 'Ask for a drink and a pastry, easy-going, with no pressure.'),
        ('Ask for a steer.', 'Hand the decision to the barista: what would they go for?'),
        ('Make it yours.', 'Ask for a small change, politely, like oat milk or extra hot.'),
        ('Change your mind.', 'Swap something, and apologise lightly for it.'),
        ('Flag a mix-up.', 'Say the wrong thing arrived without blaming anyone.'),
        ('Pay and close.', 'Settle up warmly and leave them smiling.'),
    ],
    'scenes': [
        {'chip': '☕ Saturday rush', 'where': 'A busy café, Saturday morning', 'happened': 'The counter is three deep. You know what you want, then you see the specials board and start to wobble.', 'have': 'An hour to yourself and a book.', 'want': 'A drink and a pastry, exactly right, with no fuss.', 'name': 'Jo, barista', 'desc': 'Fast, friendly, run off their feet. Happy to swap or fix an order for a pleasant customer.'},
        {'chip': '🥪 Lunch counter', 'where': 'A sandwich counter, 1 pm', 'happened': 'You have 20 minutes and you cannot eat nuts. The sandwich you like might have them.', 'have': 'A tight deadline and a bit of cash.', 'want': 'A safe lunch, quickly, and a hot drink.', 'name': 'Ravi, counter assistant', 'desc': 'Cheerful but rushed. Does not always know the ingredients and needs to check.'},
        {'chip': '🍰 Wrong order', 'where': 'A café with tables, mid-afternoon', 'happened': 'You waited ten minutes. Then they bring someone else\'s order.', 'have': 'Your receipt and a meeting in half an hour.', 'want': 'The right order, fast, with everyone still smiling.', 'name': 'Mia, waitress', 'desc': 'Slightly stressed, new on the job, quick to apologise if you stay kind.'},
        {'chip': '⭐ My own', 'where': 'Somewhere you choose', 'happened': 'Think of a café or shop you really visit and what you usually order. Agree the basics.', 'have': 'Whatever you really would.', 'want': 'What you really want to order.', 'name': 'Your partner', 'desc': 'Plays the person serving. Agree the details together first.'},
    ],
    'rule': 'Stay easy-going. Nothing is worth a bad atmosphere.',
    'win': 'You win when you get what you actually wanted, and the barista is glad you came.',
    'swap': [
        ('Who you are', 'A barista on a Saturday morning rush. Invent your name and the café.'),
        ('Your menu', 'Coffee, tea, cakes and sandwiches. Invent two specials and one thing that has just sold out.'),
        ('Your power', 'You can swap or fix an order and give one free thing if the customer is pleasant.'),
        ('Your goal', "Keep the queue moving and make sure everyone leaves happy."),
    ],
    'twists': [
        'The thing you ordered has just sold out.',
        'The card machine is not working.',
        'Your order arrives with something you cannot eat.',
        'The barista gets distracted and asks you to repeat your whole order.',
        'A friend arrives and you need to change the order for two.',
        'You are given the wrong change.',
        'You are offered a free upgrade that you do not want.',
        'Someone else has taken your table.',
        'The barista says it will take fifteen minutes. You only have ten.',
        'You change your mind a third time.',
    ],
    'ticks': [
        'I ordered lightly, with a softener.',
        'I changed my mind without making a fuss.',
        'I flagged a problem without blaming anyone.',
        'I asked again, or checked, when I missed something.',
        'I thanked them warmly at the end.',
    ],
    'secrets': [
        ('Saturday rush (Jo)', 'says "last one" for the cherry scone and sells out of oat milk halfway through. Rewards patience with a free extra.'),
        ('Lunch counter (Ravi)', "doesn't know if the sandwich has nuts and has to go and check. The student must wait and decide. Offers a safe alternative."),
        ('Wrong order (Mia)', 'apologises too much. The student can calm her down. Offers a free cake if they are gracious.'),
        ('Their own situation', 'agree the details together in 30 seconds, then use the three moves.'),
    ],
}


for _m in ('cfg_f1', 'cfg_f2', 'cfg_f3', 'cfg_f4', 'cfg_f5', 'cfg_f6'):
    try:
        __import__(_m).register(CONFIGS)
    except ImportError as _e:
        if _m not in str(_e):
            raise
