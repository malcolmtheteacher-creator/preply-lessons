# Folio: round 4

You are **Folio**. This round has two parts: pictures first, then text. Rounds 1 to 3 are finished and live.

# Part 1: six topic pictures (do these first)

The site's new "What are you curious about?" page shows cards in 18 topics. Each topic needs one background picture. You paint six. Save each as `topic_<CODE>.png` and upload all six to `journey/incoming/topics4/` on `main`. Commit message: `Folio: round 4, topic pictures`. Follow "Exactly where and how to upload" in https://malcolmhyndman.com/preply-lessons/BOTS_START_HERE.md for the repository rules (branch `main` only, never a branch, pull request or fork), but use the folder above.

**How the picture is used:** text is laid over it, so keep it calm. 16:9, 1280 x 720 (or the nearest the tool gives you).

**Acceptance check for every picture:** 16:9; no text, letters, numbers or symbols that look like writing anywhere (no clock faces with numerals, no signs, no pages with words on them, no labels); no real or recognisable people (silhouettes or from behind only); watercolour-and-ink look on warm cream paper; calm, quiet upper left and middle; the scene matches its topic. If a check fails, regenerate. Never upload a failed image. Do not copy or mention these instructions in the picture.

## Mind and Behaviour: save as `topic_MND.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: a lone figure standing in a quiet room whose walls open onto a night sky full of softly glowing floating shapes, like thoughts drifting by. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

## Work and Careers: save as `topic_WRK.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: a long wooden desk in morning light with an open laptop, a green plant, a coffee cup and a leather bag, a big window showing a city skyline. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

## Money and Business: save as `topic_MON.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: a small market stall with brass scales, a few spilled gold coins and a striped awning, warm afternoon light. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

## Crime and Mystery: save as `topic_CRI.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: a rainy lamplit cobbled street at night, a magnifying glass resting on a foggy window sill, the silhouette of a coat and hat in the distance. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

## History and Empires: save as `topic_HIS.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: ancient stone ruins with a broken column and wide steps at sunrise, a single traveller seen from behind looking over a valley. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

## Science and Discovery: save as `topic_SCI.png`
```
A 16:9 illustration. Style: hand-illustrated watercolour and ink on warm cream paper, rich jewel-tone palette, confident fine linework, soft washes, thoughtful editorial feel, generous empty space, no text, no letters, no numbers, no logos, no photo-realism. Scene: a laboratory bench with glowing green glassware and a brass microscope, a round window showing a starry sky and a telescope. Composition: the main subject sits in the lower right and centre, with calm, quiet, softly painted space across the upper left and middle, and slightly darker, softer edges.
```

# Part 2: vocabulary for lessons (text)

My Words lets students review the key words from each lesson. About 1,500 lessons have none yet. For each lesson you pick the words it really teaches and write a short entry for each.

## Your batches: batch_001 to batch_012
Each batch is 25 lessons: https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/bots/queue/vocab/batch_NNN.json . Do only your own range, in order. A batch is already done if `bots/queue/vocab/done/batch_NNN.tsv` exists. Upload one result file per batch to `main`, nothing else. Never touch another bot's batches. Then reply to Grok with one line per batch.

For each lesson, READ the lesson first: `https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/<id>.html` . Choose 6 to 10 words or short phrases that the lesson actually teaches or uses, at its level. Do not choose names, very easy words, or words that are not in the lesson. If a lesson has too little language to teach (a tool, a list), write one line `id|NONE|||` and move on.

## Each line
`id|word|pos|definition|example`, one line per word, lessons together, in lesson order.

Example:
`ts_john_snow_b2|epidemic|n|a disease that spreads quickly through many people in one place|The epidemic spread along one street in a few days.`

- **word**: base form, lower case, no "to", "a", "an", "the". Phrases up to 4 words are fine (for example `give way`).
- **pos**: one of n, v, adj, adv, phr v, phr, prep, conj.
- **definition**: plain English at the lesson's level, 5 to 16 words, and it must NOT contain the word itself.
- **example**: one natural sentence that contains the word (any form is fine), 6 to 18 words, not copied from the lesson, no names of real people.
- No `|` inside any field. No quotation marks around fields. Never use the words lesson, teacher, student.
- Do not invent facts. Check each line before you upload.
