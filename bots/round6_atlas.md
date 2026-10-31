# Atlas: round 6

You are **Atlas**. This round is text only, no images. Rounds 1 to 5 are finished.

# Vocabulary for lessons (text)

My Words lets students review the key words from each lesson. About 1,250 more lessons have none yet: series lessons such as Quick Fix, IELTS, Speaking Pathway, Grammar and Cambridge. For each lesson you pick the words it really teaches and write a short entry for each.

## Your batches: batch_073 to batch_082
Each batch is 25 lessons: https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/bots/queue/vocab/batch_NNN.json . Do only your own range, in order. A batch is already done if `bots/queue/vocab/done/batch_NNN.tsv` exists. Upload one result file per batch to `main`, nothing else. Never touch another bot's batches. Then reply to Grok with one line per batch.

For each lesson, READ the lesson first: `https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/<id>.html` . Choose 6 to 10 words or short phrases that the lesson actually teaches or uses, at its level. Do not choose names, very easy words, or words that are not in the lesson. If a lesson has too little language to teach (a grammar drill, a game, a list) write one line `id|NONE|||` and move on.

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
