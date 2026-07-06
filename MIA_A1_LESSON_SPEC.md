# Mia's English — A1 Lesson Build Spec

You build ONE lesson in Malcolm's "Mia's English" A1 story journey. Work in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.

## 1. Clone the template EXACTLY
READ `a1s_03_where.html`. **Copy its entire `<style>` block verbatim** (do not change one character). **Copy its `<script>` verbatim too — with ONE exception: the `LESSON` array**, which you replace with this lesson's 8 items.

**CRITICAL — the shared review engine:** keep `SR_KEY='miaSR_v1'`, `INTERVALS`, and every function (`loadDeck, saveDeck, addCard, dueCards, grade, refreshStats, showTab, buildCards, addAllAndReview, startReview, renderWarmUp, reviewToday`) **byte-for-byte identical** to the template. All lessons must share the same localStorage deck, so review carries across the whole course. Do NOT rename or "improve" anything in the engine.

## 2. The 5 tabs (identical structure, new content)
🔁 **Warm-up** → 📖 **The Story** → 🗂️ **Words** → 🧩 **The Pattern** → 🗣️ **Your Turn**. Keep the header block, the two stat cards, the tab buttons, and all the container IDs exactly as the template (`p0…p4`, `warmArea`, `cardGrid`, `wordsReview`, `turnReview`, etc.).

- **Header:** `.step` = "Mia's English · Lesson N"; `h1` = the lesson title; one-line subtitle. Footer = "Mia's English · A1 Story Journey · Lesson N".
- **Warm-up:** leave the panel as the template (it auto-shows due cards from earlier lessons). Its lead may mention "your words from the lessons before".
- **The Story:** ~8 short lines, **present simple, tiny A1 vocabulary**, continuing Mia's story. Recurring cast: **Mia** (hero), **Tom** (kind neighbour), **Rosa** (café owner). Use `.say` for spoken lines, `<b>` for the target words. Include **two image slots**: `<img class="scene" src="a1s_NN_keyword.png" alt="..." onerror="ph(this)">`. End with a `.tip` and a button to the Words tab.
- **Words:** the 8 new items live ONLY in the `LESSON` array (below). Keep the grid + "Add these to my reviews" exactly as template.
- **The Pattern:** ONE tiny grammar point in `.build` boxes, plus a `.tip`, then TWO `.morelink` links to existing lessons (given per lesson) — verify each file exists in the folder before linking.
- **Your Turn:** production task with **empty** `input.blank` fields (placeholders only), the `reviewToday()` button, a `.checklist`, and a closing `.tip`.

## 3. The LESSON array format
```
var LESSON=[
    ['lN_slug',"English word/phrase",'a very simple meaning or example','emoji'],
    ... 8 items, ids prefixed lN_ (l4_, l5_, …) ...
];
```
Front = the English. Back = a simple meaning or example a beginner understands (short). Emoji = one clear picture.

## 4. HARD RULES
- 4th-wall clean: no teacher notes, no TEEP/mode/pedagogy labels, no "Malcolm" in the body (title/footer keep "Mia's English"). Never use the word "Simplified".
- All `input`/`textarea` EMPTY (placeholders only, no `value=`).
- Engine byte-identical (see §1). Tabs + flip cards + review must work.
- Keep it gentle and A1: short sentences, common words, warm tone, big wins.

## 5. Verify before reporting
Confirm: 5 `.panel`, 5 `.tab-btn`, 0 prefilled inputs, `SR_KEY='miaSR_v1'` present, engine functions unchanged, the two `.morelink` targets exist. Report: filename + one-line summary + the 8 words + the two image filenames used.
