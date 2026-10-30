# Folio — one painted cover for each lesson series

**Your task:** paint **24 cover pictures**, one for each lesson series on the site. They will appear at the top of each series page and on the lesson index.

**Reference picture:** attach https://malcolmhyndman.com/preply-lessons/journey/img/room1_study.webp with every prompt, **only** for the painting style, the lighting and the colour richness.

**Every cover must be:**
- A painted still life or small scene, in the house style: near-photorealistic painterly, warm golden light from the upper left, rich oil-paint texture, jewel-like colour.
- **Landscape 3:2, 1500 x 1000 pixels or larger.**
- A full painted scene with a soft, slightly darker edge, **not** a flat colour background. Keep the middle and lower third calm and uncluttered, because Claude will place the series title over it later.
- **No text, letters, numbers, logos or watermarks anywhere**, and no real people. Do not paint a title yourself.

**Files:** upload each cover to `journey/incoming/folio/` with the exact file name shown below.

**Acceptance check for each cover:** landscape 3:2; the subject matches the description; no text anywhere; calm lower third; rich painted style like the reference. If any check fails, regenerate.

**Prompt template.** For each series, use this exactly, replacing only the subject line with the one for that series:

```
[Attached: one of my painted room images. Use it only as the reference for painting style, lighting and colour richness.]

A masterpiece-quality painted cover illustration, landscape 3:2: <SUBJECT>. Near-photorealistic painterly rendering with rich oil-paint texture, warm golden light from the upper left, deep jewel-like colour, soft vignette at the edges, the lower third calm and uncluttered. No text, letters, numbers, logos or watermarks, no people.
```

**The 24 covers, in order:**

1. `cover_bet_the_company.png` — series "Bet the Company" — SUBJECT: a heavy brass-bound boardroom table with a single poker chip tower, a toppled chess king and a small ship in a bottle, dramatic light.
2. `cover_short_history.png` — series "Short History, Long Echoes" — SUBJECT: an old oak desk with a glowing hourglass, a rolled scroll, a bronze coin and a quill, with a faint ancient city skyline behind.
3. `cover_short_stories.png` — series "Short Stories, Long Shadows" — SUBJECT: a candlelit table with an open old book, a lantern, a raven feather and long, spooky shadows on a stone wall.
4. `cover_behind_the_screen.png` — series "Behind the Screen" — SUBJECT: a vintage cinema scene: a film reel, a clapperboard, a popcorn box and a glowing projector beam in a dark room.
5. `cover_topic_explorer.png` — series "Topic Explorer" — SUBJECT: a brass compass, a rolled map, a magnifying glass and a small globe on a wooden explorer table.
6. `cover_quick_fix.png` — series "Quick Fix" — SUBJECT: a neat workbench with a small wrench, a bright pencil and a notepad with a green tick-shaped sticker, tidy and crisp.
7. `cover_wordwall_games.png` — series "WordWall Games" — SUBJECT: a playful table of plain wooden skittles, a spinning top, colourful glass marbles and a blank wooden puzzle in warm light, with no dice, cards, tiles or markings of any kind.
8. `cover_ielts_course.png` — series "IELTS Course" — SUBJECT: a tidy exam desk with a sand timer, a sharpened pencil, a blank cream sheet of paper and a small trophy, with no clock face, numbers or writing.
9. `cover_speaking_pathway.png` — series "Speaking Pathway" — SUBJECT: a winding path of stepping stones leading to a brass microphone on a stand in golden light.
10. `cover_grammar_course.png` — series "Grammar Course" — SUBJECT: a brass clockwork mechanism of interlocking gears with wooden letter blocks and a small ruler.
11. `cover_everyday_echoes.png` — series "Everyday Echoes" — SUBJECT: a cosy street corner with an iron lamppost, a cafe table with two cups and a bicycle, morning light, with no signs, lettering or postbox.
12. `cover_cambridge_exam_prep.png` — series "Cambridge Exam Prep" — SUBJECT: a college desk with a dictionary, a fountain pen, a ribboned certificate and an old brass bell.
13. `cover_a1_pathway.png` — series "A1 Pathway" — SUBJECT: a friendly welcome table with a suitcase, a cup of tea, a key and a postcard, bright and simple.
14. `cover_english_at_work.png` — series "English at Work" — SUBJECT: a modern office desk with a laptop, a leather briefcase, a coffee mug and a desk lamp.
15. `cover_talk_about_it.png` — series "Talk About It" — SUBJECT: two empty armchairs facing each other beside a low table with two cups and a speech-bubble shaped lamp.
16. `cover_art_of_memory.png` — series "The Art of Memory" — SUBJECT: a candlelit memory palace corridor with an open door, a small statue, a scroll and a glowing key.
17. `cover_life_in_english.png` — series "Life in English" — SUBJECT: a bright shopfront window with a basket of fruit, a bus ticket, an open umbrella and a street lamp.
18. `cover_modern_life.png` — series "Modern Life" — SUBJECT: a small desk with a smartphone, wireless earbuds, a plant and a takeaway coffee cup, soft city light.
19. `cover_think_inside_the_box.png` — series "Think Inside the Box" — SUBJECT: a wooden box with its lid slightly open, golden light spilling out, and puzzle pieces around it.
20. `cover_big_conversations.png` — series "Big Conversations" — SUBJECT: a round table with six empty chairs, a lamp, a globe and a pot of tea, warm evening glow.
21. `cover_religious_studies.png` — series "Religious Studies" — SUBJECT: a quiet shelf with a candle, an open book, a small bell and a bowl of light, respectful and calm, no religious symbols of any single faith.
22. `cover_true_science_stories.png` — series "True Science Stories" — SUBJECT: a laboratory bench with a brass microscope, a glass flask of glowing liquid and a notebook, with a moon through the window.
23. `cover_deep_space.png` — series "Deep Space" — SUBJECT: a brass telescope in an observatory dome window with a ringed planet and a star field outside.
24. `cover_psychology_questions.png` — series "Psychology Questions" — SUBJECT: a quiet room with a mirror, a lit candle, a half-open door and a single lit lamp, dreamlike, with no clocks or watches.

**What Claude does next:** adds each cover to its series page and the lesson index, and puts the title over it. You do not need to do anything else.
