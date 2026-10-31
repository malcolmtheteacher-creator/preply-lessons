# Hook job: one curious question per lesson (text only, no images)

You write the short line a student sees on a card, so they feel curious and open the lesson.

## Your job
1. Your name decides your batches (see the table in `BOTS_START_HERE.md`): Folio 001-010, Atlas 011-020, Vista 021-030, Muse 031-040, Lexi 041-051. Work through your own range in order. A batch is already done if `bots/queue/hooks/done/batch_NNN.tsv` exists, so skip those. Open `bots/queue/hooks/batch_NNN.json` (50 lessons). Do one batch, upload it, then start the next. Never touch a batch outside your range.
2. For each lesson, from its title (and series/level), write one line. If the title is unclear you may open `https://raw.githubusercontent.com/malcolmtheteacher-creator/preply-lessons/main/<id>.html` and read the start. Do not guess what a lesson is about.
3. Save `bots/queue/hooks/done/batch_NNN.tsv` to `main`, one line per lesson, 4 fields separated by `|`:

`id|topics|type|hook`

Example:
`ts_john_snow_b2|HLT,SCI,HIS|science|A map of a London street that stopped cholera.`

## Fields
- **id**: exactly as in the batch file. One output line per input lesson, same order, none missing.
- **topics**: 1 to 3 codes, best first, from: MND mind and behaviour, WRK work and careers, MON money and business, CRI crime and mystery, HIS history, SCI science, TEC technology and AI, HLT health, SOC society and debate, CUL culture and language, TRV travel and places, HOM home and daily life, STO stories and books, FLM film, IDE big ideas, REL relationships, FOD food, NAT nature. A lesson that is only grammar, an exam drill or a pure phrase list: use `NONE`.
- **type**: one of discuss, story, skills, roleplay, history, film, science, profile, exam, grammar.
- **hook**: one line, 6 to 16 words, in plain English the student can read at their level. Make it a specific question or a surprising fact. Good: "Why does time feel faster as we get older?" Good: "A doctor drank the bacteria to prove he was right." Bad: "Learn about travel vocabulary." Bad: "A lesson about work."

## Rules
- Never use the words: lesson, teacher, student, Malcolm, today, practise, learn about.
- No `|` inside a hook. No emoji. No quotation marks around the hook.
- Do not invent facts. If you are not sure what a lesson contains, write a hook from the title only and do not claim details.
- If a lesson has no interesting angle (drill, word list), set topics `NONE`, and write a plain hook anyway.
- Check your file has exactly 50 lines (or the number in the batch) before you upload.
- Only add the one file in `done/`. Do not edit anything else.
