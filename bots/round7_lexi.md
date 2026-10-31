# Lexi: round 7

You are **Lexi**. Round 6 is finished and live, thank you. Round 7 has two jobs. Do **Job 1 first** (text), then **Job 2** (word pictures).

# Job 1: curious one-line hooks for lessons that have none (text)

The Explore page shows each lesson as a curious question. About 900 lessons, mostly series lessons, still have no hook. Your batches are **batch_081 to batch_088**. Each batch is 25 lessons: https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/bots/queue/hooks/batch_NNN.json . A batch is already done if `bots/queue/hooks/done/batch_NNN.tsv` exists. Do only your own range, in order. Never touch another bot's batches.

The full rules, fields and format are in the hook brief: https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/bots/queue/hooks/BRIEF.md . Follow it exactly, with two changes for this round: **your batch range is the one above** (ignore the ranges in that file), and drills, games and word lists (Quick Fix, WordWall, grammar drills) get topics `NONE` and a plain, honest hook written from the title.

Upload one `bots/queue/hooks/done/batch_NNN.tsv` per batch to `main`, nothing else.

# Job 2: two sheets of word pictures (images)

My Words shows a small picture next to a word, and the quiz uses them ("Which word matches the picture?"). Only 70 words have one. You paint **2 sheets of 36 small objects** (72 pictures).

**Your word list:** https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/bots/queue/words/candidates_lexi.txt (about 267 words, one per line). Choose **72 words** from it that can be shown as ONE clear, recognisable object, animal, food or simple thing: for example `ladder`, `umbrella`, `bridge`, `kettle`, `owl`. Skip abstract words, verbs, adjectives, people and anything that needs writing or a scene to make sense. Use each word once. If you cannot find 72, choose as many as you can and say so.

**Reference picture:** attach https://malcolmhyndman.com/preply-lessons/journey/img/room1_study.webp with each sheet, only for painting style, lighting and colour richness.

**Every sheet must be:**
- Exactly 36 objects in a clean 6 x 6 grid, each fully separate with generous empty space around it, each about the same size.
- A **flat pure magenta background (#FF00FF)**: no gradient, texture or shadows on the background. No magenta or pink inside the objects.
- No text, letters, numbers, logos, faces or people.

**Prompt template.** Use this exactly, replacing only the object rows:

```
[Attached: one of my painted room images. Use it only as the reference for painting style, lighting and colour richness.]

A masterpiece-quality painted collection sheet of EXACTLY 36 small clear objects, arranged in a perfect grid of 6 columns by 6 rows, every object fully separate with generous empty space around it. The background is perfectly flat, pure magenta (#FF00FF) with no gradient, texture or shadows. Do not use magenta or pink anywhere in the objects. Style: near-photorealistic painterly rendering like collectible museum pieces, rich oil-paint texture, warm golden light from the upper left, jewel-like colour, the same slightly raised three-quarter angle, each object centred in its cell, about the same size, fully inside its cell, crisp clean edge, simple and instantly recognisable. No text, letters, numbers or logos. The objects, left to right, top to bottom:
<ROWS>
Every object is complete and clearly separate. Square image, 2048 x 2048 or larger.
```

Write the `<ROWS>` as 6 rows of 6 object names (for example `Row 1: ladder, umbrella, kettle, owl, lantern, bucket`).

**Files (upload to `main` only):**
- Pictures: `journey/incoming/words7/lexi_sheet_01.png` and `journey/incoming/words7/lexi_sheet_02.png`
- Lists: `bots/queue/words/done/lexi_01.txt` and `bots/queue/words/done/lexi_02.txt`: exactly 36 lines each, one word per line, in the same order as the grid (left to right, top to bottom), the word exactly as it appears in your candidate list.

**Acceptance check:** exactly 36 objects in a clean 6 x 6 grid, in the order of your list file; flat magenta background; no text; clear and recognisable. If a sheet fails, regenerate. Never upload a failed sheet. If 36 will not fit in one image, tell Malcolm.

When finished, reply to Grok with one line: the hook batches done, and the four file names uploaded.
