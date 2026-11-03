#!/usr/bin/env python3
"""Build Part I of the Memory Arts notebook.

  -> memory_arts_part1.html            (the map: engraved palace plate, ten clickable rooms)
  -> memory_arts_p1_01.html .. _10.html (one handwritten notebook page per book)

All notes are written in our own words from the verified reading notes in
Memory_Arts_Project/notes_verified/. The book itself is not quoted.
Each page's sketch is a crop of the plate, so no further images are needed.
Usage: python3 tools/build_memory_arts_part1.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = "https://www.cambridge.org/core/books/memory-arts-in-renaissance-england/0AD357A47D715756FDFE4521C8E63F70"
PLATE = "memory_arts_part1_palace.jpg"
HUB = "memory_arts_part1.html"
E = html.escape

# room crops on the plate: left, top, width, height (percent)
ZONES = {1: (2, 8, 17.5, 29.5), 2: (20, 8, 19, 29.5), 3: (40, 8, 19.5, 29.5), 4: (60, 8, 19, 29.5), 5: (79.2, 8, 19.3, 29.5),
         6: (2, 41, 17.5, 32), 7: (20, 41, 18.5, 32), 8: (39, 41, 23, 32), 9: (62.3, 41, 16.7, 32), 10: (79.2, 41, 19.3, 32)}

INTRO = {
    "heading": "Before the ten books",
    "points": [
        "The art of memory began as a speaker's private trick: walk through a building you know and leave a vivid picture in each place, then walk it again to get your speech back in order.",
        "In the Middle Ages monks used it to compose and to meditate. Aquinas and his teacher defended it as part of prudence: pick striking images, put things in order, care about them, and think about them often.",
        "A second tradition came from Ramon Llull: letters and wheels that combine ideas to sort out all knowledge. That strand fed the Renaissance writers on magic and logic, and later Giordano Bruno.",
        "England printed very little on the art before the 1500s. Only two foreign treatises were translated (the Phoenix and the Castle of Memory); the rest were written in English, mostly for ordinary readers, and they played down magic.",
        "The editors count 217 printed works that use the phrase \"art of memory\" between 1500 and 1700. The phrase spreads like a catchphrase and peaks in the 1640s and 1650s.",
    ],
    "note": "the English story is practical and a bit humble: lawyers, merchants, preachers. not wizards.",
}

BOOKS = [
    dict(n=1, id="I.1", short="The Pastime of Pleasure", author="Stephen Hawes", year="1509", pages="39-41",
         who="Hawes was a court poet and servant of Henry VII, remembered for his wit and his memory. His long allegorical poem follows a young knight through the seven liberal arts.",
         pts=["Rhetoric has five parts. The fifth, memory, is what makes a speech come out in order.",
              "The method is simple: fix one image in your mind for each story or point. When you speak, take the images in turn and each one brings its tale and its moral.",
              "He admits it is dark and hard at first. Practice, he says, makes it work.",
              "This is the earliest English poetry to carry the art, folded into a courtly poem."],
         try_="Pick three points you want to say aloud. Give each one a picture and say them in order without notes.",
         note="the oldest voice here. short, gentle, and honest that it is difficult.", q="Pastime of Pleasure Stephen Hawes 1509"),
    dict(n=2, id="I.2", short="The Mirror of the World", author="Laurence Andrewe", year="1527", pages="41-44",
         who="A medieval French verse encyclopedia, put into English by William Caxton in 1481. Andrewe's 1527 edition added a new section on rhetoric and the art of memory.",
         pts=["Natural memory is a gift from God. Artificial memory is the craft of writing a thing in the mind.",
              "Places are like parchment and images are like the letters you write on it.",
              "Pick a big house you know well and mark posts, corners and walls one way round, up to a hundred or two hundred places, about ten to twelve feet apart.",
              "Images must be bodily and visible. Something with no body gets a stand-in: reading becomes a person looking at a book, walking becomes a pair of legs, wisdom an old man with a white head."],
         try_="Think of an idea with no shape, like patience or fairness. Give it a person doing something.",
         note="the first plain English recipe in print. ink and parchment is the whole picture.", q="Mirror of the World Caxton 1481 Laurence Andrewe 1527"),
    dict(n=3, id="I.3", short="The Phoenix", author="Peter of Ravenna", year="1548", pages="44-51",
         who="Peter was an Italian law professor whose memory book was printed in Venice in 1491 and quickly famous. The English version, by the London printer Robert Copland, is muddled, so the editors say it cannot have been the great source people once thought.",
         pts=["Four rules for places: windows, pillars and niches will do; not too close and not too far (about six feet); not in a busy place; not too high to reach.",
              "He walks a church he knows, three or four times, and fixes a place every five or six feet. He boasts of a hundred thousand places in his youth.",
              "Images should use friends who share the name of the thing, doing what they usually do. For lifeless things use things that move: a swarm of ants for one tiny ant.",
              "An alphabet of people, one for each letter, handles names and words. He says beautiful young women make the strongest images.",
              "Later chapters give tricks for lawyers: parts of the body for the cases of nouns, colour for volumes of law, fingers for hundreds."],
         try_="Walk a place you know and count ten spots, a few steps apart. Do not use anywhere crowded.",
         note="show-off and clever, and full of practical rules for lawyers. the English copy is a mess.", q="Phoenix Peter of Ravenna Copland 1548"),
    dict(n=4, id="I.4", short="The Castle of Memory", author="Guglielmo Gratarolo", year="1562", pages="51-64",
         who="Gratarolo was an Italian doctor who became a Protestant and fled to Basel. William Fulwood, a London merchant, translated his book into English and dedicated it to Robert Dudley, the queen's favourite.",
         pts=["Memory is part of the body: it sits at the back of the head, and cold and damp harm it. His cures are homely: walk before meals, rub your limbs, avoid garlic, cheese and late drinking, wash your feet in herbs.",
              "The art itself comes last. Pick a large empty house or your own town, and mark every fifth place with a sign, such as a golden hand, so you can count.",
              "Fill the places with people you know doing something odd: one friend pours a urinal over another, a man smears salve on someone's face. Five rules for images: move the feelings, use likeness or opposites, start young, repeat each group of five, join simple images into compound ones.",
              "A chickpea (cicer) in a garden (hortus) can stand for Cicero against Hortensius. A pen can stand for a word that sounds like it.",
              "Only the sluggish and idle will gain nothing, he says. The rest is practice."],
         try_="Make a silly picture for each of three names you want to keep. Make the action rude or odd, then recall them next morning.",
         note="the first full recipe in English, wrapped inside a health book. the funny images are what stick.", q="Castle of Memory Gratarolo Fulwood 1562"),
    dict(n=5, id="I.5", short="The Jewel House of Art and Nature", author="Hugh Plat", year="1594", pages="65-69",
         who="Plat collected useful tricks and recipes, and was knighted for farming advice. His memory chapter passes on a method taught in London by Alexander Dickson, a follower of Giordano Bruno.",
         pts=["Choose a big building whose rooms you know. In each room fix ten subjects, spaced out, in groups of ten. The first is a man and the fifth a woman, so you can count.",
              "Use active things: a soldier at the door, a fire at the head of the bed, a dunghill at the foot, a tub of water in the chimney, an ape on the cupboard, a ship in the window.",
              "To remember a list, make each word act on the subject in its place: a cat claws the soldier's face, a lute burns in the fire, a hand rakes the dunghill.",
              "More than ten items? Move on to the next decade of places.",
              "He is blunt about it. Dickson charged a fortune and could not fill an hour with practice. It works for ten to forty things, and some pupils used it to cheat at cards."],
         try_="Set up ten subjects in one room of your home. Ask a friend for three words and place them.",
         note="the first honest review of a memory course: useful, not magic, and too expensive.", q="Jewel House of Art and Nature Hugh Plat 1594"),
    dict(n=6, id="I.6", short="A Help to Memory and Discourse", author="William Basse", year="1620", pages="69-73",
         who="A question-and-answer miscellany of jokes, riddles and wise sayings, written to help young gentlemen shine in conversation. The author is probably the poet W.B., a household poet to a country gentleman.",
         pts=["Good talk needs a good memory, and a good memory needs knowledge to work on. Memory is untrustworthy and unstable: a lawyer once forgot more law than his colleague ever knew.",
              "He compares memory to the Tower of London, where the realm's old records were kept, and to a clerk keeping records.",
              "The art writers say places are like paper and images like letters. The Bible supports it: twelve stones from the River Jordan, the sacraments as visible signs, a thread tied round a finger.",
              "He does not practise the art himself. He leaves it to specialists and trusts a natural memory, helped by God."],
         try_="Where would you keep your most important records if you had to store them in a building?",
         note="the art in a joke book. admired from a safe distance.", q="Help to Memory and Discourse Basse 1620"),
    dict(n=7, id="I.7", short="The Art of Memory", author="John Willis", year="1621, 1661", pages="73-84",
         who="Willis invented a popular shorthand and wrote often on memory. This is the fullest English handbook, with practical examples and no heavy debt to foreign writers.",
         pts=["Writing is the best memory aid, but you cannot write everything. The art of places and images is closest to writing: places are leaves, images are letters, rehearsing is reading.",
              "The poet Simonides was called out of a banquet just before the roof fell; he later named every crushed guest by where they had sat. King Darius won a throne because his horse neighed at the right place.",
              "Seeing beats hearing. Picture each thing as if you were looking at it, like blowing an ember back into flame. Memory only stores; understanding arranges and uses.",
              "Colour code each of your imagined buildings. Dress every image in the colour of its repository: a sailor with a golden chain in the first, a silver chain in the second, and so on. If an image goes missing, its colour tells you where to look.",
              "Compound images join a picture with a written motto, like an emblem in a book.",
              "Keep a pocket notebook of striking sentences under headings, instead of repeating them endlessly."],
         try_="Choose a colour for each room of your palace. Dress every image you place there in that colour.",
         note="the most complete English guide. colour coding is a great trick.", q="Willis Art of Memory Mnemonica 1621"),
    dict(n=8, id="I.8", short="The Art of Memory Made Plain", author="Henry Herdson", year="1651", pages="84-88",
         who="Almost nothing is known about Herdson, only a story that he advertised himself as a professor at Cambridge and a famous scholar could not recall ever meeting him. His book aims at ordinary people and mostly religious uses.",
         pts=["His repository is four square rooms with five tables each, plus a central table: 21 tables and 105 imagined friends, whose hands hold images for numbers.",
              "For business, a shopkeeper pictures an acquaintance wearing the cloth, holding the yards in one hand and the price in the other.",
              "For sermons: pay attention, notice the parts, put each part in a place, and think over the images.",
              "For stories, split them into people: Genesis becomes Adam, Noah, Abraham, Isaac, Jacob and Joseph. For Bible books, give each a friend with a similar name, with chapter in the right hand and verse in the left.",
              "To fix an image, load it with the most delightful things for all five senses (paradise) or the most horrible (hell)."],
         try_="Split a story you know into five people and put them in five spots in a room.",
         note="memory for shopkeepers and churchgoers. the paradise and hell trick is the keeper.", q="Herdson Ars Memoriae Art of Memory Made Plain 1651"),
    dict(n=9, id="I.9", short="Art of Memory", author="Richard Saunders", year="1671", pages="88-94",
         who="Saunders wrote almanacs and practised medicine in the circle of an astrologer. He added this section to a big book on palm reading, translated from a French writer.",
         pts=["The art is built on ten letters, A to K, written on the hand. A sits in the middle of the palm, B under the thumb, C to E on the fingers, and the rest at points on the palm and wrist.",
              "To think about any subject, put it on A and put its definition and parts on the other letters.",
              "Each letter is a question: to know my? who? of what? why? how much? what kind? when? where? how? Each has attached ideas such as God, Angel, Heaven, Man, Wisdom, Virtue, Truth, Glory.",
              "The system comes from Ramon Llull, who tried to compress all the sciences into a few principles. Saunders claims a child of seven could be fit for all of them in ten days.",
              "Practice: learn the letters forwards and backwards, then in groups of three. A preacher can put Bible stories on the letters; a merchant can put his business on A."],
         try_="Draw your own hand. Put a question on each finger and answer them for a problem you have.",
         note="a memory palace you carry in your hand. big promises, though.", q="Saunders Physiognomie and Chiromancie Art of Memory 1671"),
    dict(n=10, id="I.10", short="The Art of Memory", author="Marius D'Assigny", year="1697", pages="94-100",
         who="D'Assigny was a teacher and translator who wrote for university students. His little book closes Part I, pulling together what the earlier writers said without naming them all.",
         pts=["Artificial memory is an imagined arrangement of sensible things, like a wax tablet with writing on it.",
              "Some use a fair building with coloured pillars. Others use beasts for the letters of the alphabet and parts of a body, to get 115 places.",
              "Better still, use a place you know: your own town, entering by the gate and walking its streets, churches and friends' houses; or a big empty house with rooms numbered by distance from the door.",
              "Make images remarkable and moving. Show a person by likeness or contrast: Galen by another physician, Ovid by a big nose, Plato by broad shoulders.",
              "Eight rules: read the thing three or four times first; choose well-known figures; give them action; stir the passions; use natural figures that fit the place; nothing too low or too grand; never reuse an image; recall them often in order, especially on lying down to sleep.",
              "He admits it is cumbersome, not for everyone, and not for speeches. It is for names, sentences and passages."],
         try_="Tonight, before sleep, walk five places in your mind and recall one thing in each.",
         note="the tidy summary. the bedtime tip is the one I'd keep.", q="D'Assigny Art of Memory 1697"),
]

THREADS = {}

CSS = r"""
:root{--paper:#f5efdf;--sheet:#fffdf5;--ink:#1b2540;--red:#b3342d;--gold:#8a6a2c;--pencil:#6c6a66;--rule:rgba(70,100,150,.17);--margin:rgba(190,70,70,.45);--hl:rgba(255,213,60,.62);--sticky:#fff0a3;--stickyink:#3b3210;--tape:rgba(214,190,120,.66);--shadow:rgba(30,25,15,.22)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:"Kalam","Caveat","Bradley Hand","Segoe Print",cursive;font-size:1.2rem;line-height:34px;color:var(--ink);background-color:var(--paper);
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .25 0 0 0 .10 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
a{color:inherit}
.hand{font-family:"Caveat","Kalam",cursive}
.sheet{position:relative;max-width:960px;margin:22px auto 60px;padding:34px 40px 40px 96px;background-color:var(--sheet);background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 33px,var(--rule) 33px,var(--rule) 34px);box-shadow:0 14px 34px var(--shadow)}
.sheet::before{content:"";position:absolute;left:72px;top:0;bottom:0;border-left:2px solid var(--margin)}
.holes i{position:absolute;left:22px;width:22px;height:22px;border-radius:50%;background:var(--paper);box-shadow:inset 1px 2px 3px rgba(0,0,0,.38)}
.tape{position:absolute;top:-13px;left:50%;width:120px;height:28px;transform:translateX(-50%) rotate(-2deg);background:var(--tape);box-shadow:0 1px 3px rgba(0,0,0,.2)}
.back{font-family:"Caveat",cursive;font-size:1.7rem;line-height:1.2;color:var(--ink);text-decoration:none;border-bottom:2px dashed var(--ink);display:inline-block;margin-bottom:6px}
.kicker{font-family:"Caveat",cursive;font-size:1.8rem;color:var(--red);line-height:1.1;margin-top:8px}
h1{font-family:"Caveat",cursive;font-size:4.2rem;line-height:1;font-weight:700;margin:2px 0 4px;transform:rotate(-.5deg)}
.uline{position:relative;display:inline-block}
.uline::after{content:"";position:absolute;left:-4px;right:-6px;bottom:-9px;height:12px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 12' preserveAspectRatio='none'%3E%3Cpath d='M2 8 C 40 2, 80 11, 130 6 S 220 3, 298 8' fill='none' stroke='%23b3342d' stroke-width='3.2' stroke-linecap='round'/%3E%3Cpath d='M20 11 C 90 7, 170 11, 270 9' fill='none' stroke='%23b3342d' stroke-width='2' stroke-linecap='round' opacity='.7'/%3E%3C/svg%3E") no-repeat center/100% 100%}
.by{font-family:"Caveat",cursive;font-size:1.8rem;color:var(--pencil);line-height:1.15;margin:12px 0 10px}
.sketch{float:right;width:36%;margin:6px 0 14px 26px;background:#fff;padding:10px 10px 12px;box-shadow:0 9px 22px var(--shadow);transform:rotate(1.6deg);position:relative;line-height:0}
.sketch::before{content:"";position:absolute;top:-12px;left:50%;width:84px;height:22px;transform:translateX(-50%) rotate(-3deg);background:var(--tape);box-shadow:0 1px 3px rgba(0,0,0,.2)}
.crop{width:100%;background-repeat:no-repeat;background-image:url(__PLATE__)}
.sketch .cap{display:block;font-family:"Caveat",cursive;font-size:1.3rem;line-height:1.1;color:#444;text-align:center;padding-top:8px}
h2{font-family:"Caveat",cursive;font-size:2.3rem;line-height:1;color:var(--red);margin:20px 0 6px;font-weight:700}
.who{margin-bottom:6px}
.pt{position:relative;padding-left:28px;margin-bottom:10px}
.pt::before{content:"\2013";position:absolute;left:6px;color:var(--red);font-weight:700}
.hl{background:linear-gradient(transparent 52%,var(--hl) 52%,var(--hl) 92%,transparent 92%)}
.sticky{clear:both;background:var(--sticky);color:var(--stickyink);padding:12px 18px 14px;margin:18px 0 8px;max-width:560px;box-shadow:3px 4px 10px rgba(0,0,0,.2);transform:rotate(-.9deg);font-family:"Caveat",cursive;font-size:1.55rem;line-height:1.25}
.note{font-family:"Caveat",cursive;font-size:1.6rem;line-height:1.2;color:var(--pencil);margin:20px 0 6px 6px;transform:rotate(.6deg)}
.note svg{vertical-align:middle;margin-right:6px}
.go{clear:both;display:flex;flex-wrap:wrap;gap:6px 26px;margin-top:22px;font-family:"Caveat",cursive;font-size:1.75rem;line-height:1.2}
.go a{text-decoration:none;color:var(--ink)}.go a span{border-bottom:2px dashed var(--ink)}.go a:hover span{background:var(--hl)}
.go a.red{color:var(--red)}
.nav2{display:flex;justify-content:space-between;gap:12px;margin-top:30px;font-family:"Caveat",cursive;font-size:1.9rem;line-height:1.1}
.nav2 a{color:var(--red);text-decoration:none;font-weight:700}.nav2 a:hover{background:var(--hl)}
/* hub */
.plate{position:relative;line-height:0;background:#fff;padding:12px 12px 14px;box-shadow:0 12px 30px var(--shadow);transform:rotate(-.4deg);margin:14px 0 8px}
.plate::before,.plate::after{content:"";position:absolute;top:-12px;width:100px;height:26px;background:var(--tape);box-shadow:0 1px 3px rgba(0,0,0,.2);z-index:4}
.plate::before{left:-22px;transform:rotate(-38deg)}.plate::after{right:-22px;transform:rotate(38deg)}
.plate img{display:block;width:100%;height:auto}
.zone{position:absolute;display:block;border-radius:6px;transition:box-shadow .2s}
.zone:hover,.zone:focus-visible{outline:none;box-shadow:inset 0 0 0 3px var(--hl),0 0 20px rgba(255,213,60,.8)}
.znum{position:absolute;left:8px;top:8px;min-width:40px;height:40px;padding:0 6px;font-family:"Caveat",cursive;font-weight:700;font-size:1.6rem;line-height:36px;text-align:center;color:var(--red);background:rgba(255,253,245,.86);border:2.5px solid var(--red);border-radius:52% 48% 55% 45%/48% 55% 45% 52%;transform:rotate(-6deg)}
.ztag{position:absolute;left:50%;bottom:8px;transform:translateX(-50%) rotate(-1.5deg);font-family:"Caveat",cursive;font-size:1.4rem;line-height:1.05;background:var(--sticky);color:var(--stickyink);padding:3px 12px 4px;box-shadow:2px 3px 8px rgba(0,0,0,.4);opacity:0;transition:opacity .15s;text-align:center;width:max-content;max-width:92%;pointer-events:none}
.zone:hover .ztag,.zone:focus-visible .ztag{opacity:1}
.toc{list-style:none;margin:6px 0 4px}
.toc li{display:flex;align-items:baseline;gap:8px;line-height:36px}
.toc a{text-decoration:none;display:flex;align-items:baseline;gap:10px;width:100%}
.toc .no{font-family:"Caveat",cursive;font-size:1.8rem;color:var(--red);font-weight:700;min-width:48px}
.toc .t{font-family:"Caveat",cursive;font-size:1.8rem;font-weight:700}
.toc .d{flex:1;border-bottom:2px dotted rgba(70,100,150,.45);transform:translateY(-6px)}
.toc .a{font-size:.95rem;color:var(--pencil);white-space:nowrap}
.toc a:hover .t{background:var(--hl)}
@media(max-width:820px){
 body{font-size:1.1rem;line-height:31px}
 .sheet{margin:0;padding:24px 16px 30px 52px;box-shadow:none}.sheet::before{left:36px}.holes i{left:8px;width:18px;height:18px}
 h1{font-size:2.9rem}.sketch{float:none;width:78%;margin:6px auto 22px;transform:rotate(1deg)}
 .zone .znum{min-width:26px;height:26px;line-height:22px;font-size:1.05rem;left:3px;top:3px;border-width:2px}.ztag{font-size:1rem;bottom:3px}
 .toc .a{display:none}.toc .t,.toc .no{font-size:1.5rem}
}
"""


def crop_style(n):
    x, y, w, h = ZONES[n]
    size = 10000.0 / w
    px = x / (100.0 - w) * 100.0
    py = y / (100.0 - h) * 100.0
    ratio = (w * 1536.0) / (h * 1024.0)
    return f"aspect-ratio:{ratio:.4f};background-size:{size:.1f}% auto;background-position:{px:.2f}% {py:.2f}%"


def holes():
    return '<div class="holes" aria-hidden="true"><i style="top:80px"></i><i style="top:50%"></i><i style="bottom:80px"></i></div>'


def head(title):
    css = CSS.replace("__PLATE__", PLATE)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Memory Arts">
<title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@300;400;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></svg>
'''


ARROW = '<svg width="46" height="26" viewBox="0 0 46 26" aria-hidden="true"><path d="M44 4 C 30 2, 14 8, 5 20 M5 20 L13 17 M5 20 L7 11" fill="none" stroke="#b3342d" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def page(b, prev, nxt):
    n = b["n"]
    pts = "".join(f'<p class="pt">{E(p)}</p>' for p in b["pts"])
    pn = f'<a href="memory_arts_p1_{prev["n"]:02d}.html">&larr; {E(prev["id"])}</a>' if prev else '<a href="memory_arts_part1.html">&larr; the map</a>'
    nx = f'<a href="memory_arts_p1_{nxt["n"]:02d}.html">{E(nxt["id"])} &rarr;</a>' if nxt else '<a href="memory_arts_part1.html">back to the map &rarr;</a>'
    arch = f"https://archive.org/search?query={b['q'].replace(' ', '+')}"
    body = f'''<main class="sheet">
<div class="tape"></div>{holes()}
<a class="back" href="memory_arts_part1.html">&larr; part I &middot; the ten rooms</a>
<div class="kicker">{E(b["id"])} &middot; printed {E(b["year"])}</div>
<h1><span class="uline">{E(b["short"])}</span></h1>
<div class="by">{E(b["author"])}</div>
<div class="sketch"><div class="crop" style="{crop_style(n)}" role="img" aria-label="A room from the engraved palace: {E(b["short"])}"></div><span class="cap">room {n}</span></div>
<p class="who">{E(b["who"])}</p>
<h2>what it teaches</h2>
{pts}
<div class="sticky"><b>try it:</b> {E(b["try_"])}</div>
<div class="note">{ARROW}{E(b["note"])}</div>
<h2>go to the book</h2>
<div class="go"><a href="{BOOK}" target="_blank" rel="noopener"><span>read it in the anthology</span></a><a href="{arch}" target="_blank" rel="noopener"><span>look for the original</span></a></div>
<div class="nav2">{pn}{nx}</div>
</main>
</body></html>'''
    return head(f"{b['id']} {b['short']} · Memory Arts notebook") + body


def hub():
    zones = ""
    for b in BOOKS:
        x, y, w, h = ZONES[b["n"]]
        zones += (f'<a class="zone" href="memory_arts_p1_{b["n"]:02d}.html" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%" aria-label="{E(b["id"])} {E(b["short"])}">'
                  f'<span class="znum">{b["n"]}</span><span class="ztag">{E(b["id"])} &middot; {E(b["short"])}</span></a>')
    toc = "".join(f'<li><a href="memory_arts_p1_{b["n"]:02d}.html"><span class="no">{E(b["id"])}</span><span class="t">{E(b["short"])}</span><span class="d"></span><span class="a">{E(b["author"])}, {E(b["year"])}</span></a></li>' for b in BOOKS)
    ipts = "".join(f'<p class="pt">{E(p)}</p>' for p in INTRO["points"])
    body = f'''<main class="sheet">
<div class="tape"></div>{holes()}
<div class="kicker">notes from a very large project &middot; england, 1500&ndash;1700</div>
<h1>The Memory Arts in <span class="uline">Renaissance England</span></h1>
<div class="by">part I &mdash; the art of memory: ten guides, ten rooms</div>
<p>In Shakespeare's England people trained their memories with imagined buildings, strange pictures and even their own hands. These are my notes on the ten English guides in Part I of one Cambridge anthology of old sources. Tap a room to open the notes.</p>
<div class="plate"><img src="{PLATE}" alt="An engraved cutaway of a Renaissance palace with ten rooms: a garden, a mirror, a phoenix, a castle, a jewel house, a tower of books, a theatre, four chambers, an open hand and a walled town.">{zones}</div>
<div class="note">{ARROW}the gold thread is the walk through the palace, in order</div>
<h2>the ten, in order</h2>
<ul class="toc">{toc}</ul>
<h2>{E(INTRO["heading"])}</h2>
{ipts}
<div class="sticky">{E(INTRO["note"])}</div>
<h2>go to the book</h2>
<div class="go"><a href="{BOOK}" target="_blank" rel="noopener"><span>the anthology, Cambridge University Press</span></a></div>
<div class="note">parts II to VI (rhetoric, education and science, history, religion, literature) are still being written up.</div>
</main>
</body></html>'''
    return head("The Memory Arts in Renaissance England · Part I notebook") + body


def main():
    out = os.path.join(ROOT, HUB)
    open(out, "w", encoding="utf-8").write(hub())
    for i, b in enumerate(BOOKS):
        prev = BOOKS[i - 1] if i else None
        nxt = BOOKS[i + 1] if i + 1 < len(BOOKS) else None
        open(os.path.join(ROOT, f"memory_arts_p1_{b['n']:02d}.html"), "w", encoding="utf-8").write(page(b, prev, nxt))
    print("wrote hub + %d pages" % len(BOOKS))


if __name__ == "__main__":
    main()
