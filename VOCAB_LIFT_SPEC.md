# B2/C1 Vocabulary Lift — retrofit spec

You are given ONE Short History **B2/C1 base** lesson (`short_history_<slug>.html`, NOT the `_a2b1` twin). Your ONLY job is to raise its **Key Words tab** to a genuine B2/C1 register. Touch nothing else.

## What to do
1. Read the lesson's Key Words tab (Tab 0). List the 10 pre-taught words.
2. Judge each against B2/C1 (see the register test below). **Keep the words that are already at level.** Only lift the ones that are too easy.
3. For each too-easy word, replace it with a genuinely B2/C1 word that **actually appears in, or naturally belongs to, THIS lesson's Story** — a lower-frequency, abstract, figurative, or precise topic/academic term worth teaching. Prefer a more precise/formal word for the same idea (e.g. *cannon → artillery · fort → garrison · ban → prohibition · fight → skirmish · money → finance/capital · fame → notoriety · fall → downfall · plan → conspiracy*).
4. When you swap a word, update all three parts of its item **consistently**: the bold headword, the stimulus in `.sent`, and the `.meaning` reveal (definition + part of speech). Keep the item's existing **technique** (infer-from-context / meaning→word / synonym-antonym / collocation / odd-one-out / MCQ / word-building) and its `.guess-item` → `.reveal-btn` → `.meaning` structure.
5. If a word appears in the Story only as its basic form, you may use the precise term as the taught word and note it — but do NOT rewrite the Story, Grammar, Listen or Speak tabs. If a swapped word does not occur in the story text at all, pick one that does, or that fits the topic naturally.

## The register test — is a word B2/C1?
- **Too easy (lift it):** everyday A2/B1 words an advanced learner already owns — *army, gun, king, ship, rich, wall, win, fight, mission, blast, plot, fort, boat, money, fame, plan, brave.*
- **At level (keep it):** lower-frequency / abstract / figurative / precise — *garrison, capitulate, patronage, fabricated, decisive, ruthless, besiege, notorious, entangled, coup, dynasty, annexation, conscience, valour, phalanx, infatuated, annul, shrewd, reinforcements, siege.*
- Topic-specific technical terms (*hoplite, agoge, plutonium, annul, oligarchy*) are excellent — they are exactly what an advanced learner comes for.

## Hard rules (unchanged)
- Keep **§3a variety** (3–4 different techniques across the 10 words) and the **no-inline-gloss** rule: the context sentence must never contain the target's definition/synonym; the meaning appears only on Reveal.
- All inputs stay EMPTY (no `value=`). Do not rewrite prose in the Story/Grammar/Listen/Speak tabs, or touch the CSS or JS. **ONE exception:** if the Listen or Speak tab lists the taught key words *verbatim* (a "use these words aloud" list), update those word tokens to match your lifted set — a token swap only, never a sentence rewrite. This keeps the student from being asked to reuse a word they weren't taught, and means no lesson is ever "blocked" from lifting.
- 4th-wall clean; never the word "Simplified".

## Phase 2 — reconcile the spaced-repetition review block (RUN ONLY AFTER ALL LESSONS' NEW WORDS ARE LIFTED)
Many lessons open the Key Words tab with a **review block**: 5–6 `guess-item`s of the form "*word* — from [an earlier lesson]" that re-test vocabulary taught before. These are the series' **spaced repetition**, and they must show the **lifted** words, not the old easy ones. Because a review block reviews OTHER lessons, this pass can only run once every lesson's final key-word set exists.
For each review item "WORD — from LESSON": open that source LESSON, and replace WORD with one of the genuinely-B2/C1 key words that LESSON now actually teaches (keep the "— from [LESSON]" link). Update headword + stimulus + `.meaning` consistently, keep the item's technique, no inline gloss. Never leave a review item pointing at an everyday word or at a word the source lesson no longer teaches.

## Verify before reporting
Confirm: still exactly 10 taught words; 5 `tab-content` divs; 0 inputs with `value=`; §3a variety intact; no context sentence glosses its own word. Report: the filename, the **before → after** list of words you changed (and which you left as already-at-level), and "0 prefilled inputs".
