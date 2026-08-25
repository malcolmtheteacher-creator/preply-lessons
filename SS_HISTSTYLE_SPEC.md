# Short Stories (History-style, no podcast) — Build Spec

Build ONE short-story lesson **pair** using the Short History lesson structure, but for FICTION and with **no podcast**. Work in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.

## 1. Clone the template
READ and replicate exactly (the entire `<style>` and `<script>` — tab switching + timer): `short_history_houdini.html` (B2/C1) and `short_history_houdini_a2b1.html` (A2/B1). Change only content. Do not invent new CSS classes.

## 2. Header
Tag: `SHORT STORIES, LONG SHADOWS · B2/C1 · 50 min` (twin: `· A2/B1 · 50 min`). Add `<meta name="series" content="Short Stories, Long Shadows">`. `<h1>` = the story title + a one-line subtitle (mention the author). Crosslink under the header — base: `Need an easier version? <a href="..._a2b1.html">Read this story at A2/B1 level →</a>`; twin: `Want the fuller version? <a href="...html">Read this story at B2/C1 level →</a>`.

## 3. FIVE tabs — Key Words → The Story → Grammar — <POINT> → Going Deeper → Speak
Structure and JS are IDENTICAL to the history template (5 tabs, `show(0)`–`show(4)`, Speak = tab 4). **The only change is the 4th tab's purpose: the podcast "Listen" tab becomes a "Going Deeper" tab.** Rename the 4th nav button from "Listen" to **"Going Deeper"**.

- **Tab 0 — Key Words:** an `.intention` line; a short warm-up = 2–3 discussion questions (no links to other lessons); then pre-teach the **10 key words** with VARIETY (see **§3a** below); end with a short "use them out loud" `.discuss`.
- **Tab 1 — The Story:** the classic story, **faithfully and tightly abridged into 3 parts** (`.story-chunk`), vivid and true to the original. After each part: a from-memory **Quick check** (2 questions + hidden Reveal-answers block) + one `.discuss` question.
- **Tab 2 — Grammar — <POINT>:** clear explanation in `.note` boxes; **3 gap-fill exercises**. Inputs MUST be empty (no `value=`, no answer in the prompt/hint). Answers live ONLY in the hidden `.answers` reveal.
- **Tab 3 — Going Deeper:** **NO podcast, NO audio, NO Noiser, NO Spotify, NO "Listen".** Replace the podcast box with a literary-discussion block: a 2–3 sentence note on the story's theme / twist / why it endures, then a `.discuss` with 3–4 deeper questions (meaning, symbolism, the ending, "what would you have done?").
- **Tab 4 — Speak:** keep the timer JS identical; 3 `.speak-prompt` tasks — A: retell the story using the grammar + 5 key words; B: an opinion/debate on a theme; C: a broader task WITH safe non-personal alternatives; then a `.final-discussion` (3–4 bigger questions + a from-memory grammar recall).

**Footer:** `Short Stories, Long Shadows · <Story> · B2/C1` (twin `· A2/B1`). No byline.

### 3a. Unblocking the key words — VARIETY, and NEVER gloss the answer
Every vocab item reuses the proven mechanic — a stimulus in `.sent`, a `.reveal-btn` (`onclick="this.nextElementSibling.classList.toggle('show')"`), and the answer in `.meaning`, shown **only on Reveal**. Do **NOT** present all ten words as one identical "sentence → Reveal → definition" list.

**Group the 10 words into 3–4 small labelled activities, each a DIFFERENT technique** (at least 3, ideally 4; cover all 10 between them): **infer from context** ("What does **X** mean here?"), **meaning → word** ("Which word means '…'?"), **synonym / antonym**, **collocation / chunk** ("Complete: to **lay ___ to**…"), **odd one out / grouping**, **multiple choice in context** (a/b/c), **word building** ("You know **besiege** — what noun comes from it?").

**HARD RULE — scramble matching lists.** In any "Which term/word means…?" activity, the order of the terms in the intro list must NEVER match the order of the questions (use a derangement — no item in its own position). If the list order mirrors the question order, the student just reads down and nothing is tested. (Systemic fault found and fixed 2026-08-25.)

**HARD RULE — no inline gloss.** Never put the definition, a synonym, or a dash-appositive of the target word inside its own context sentence. ✗ "a *siege* — surrounding a city to starve it out." ✓ "For eleven days nothing got in or out. This was a *siege*." → Reveal gives the meaning. The student thinks; Reveal confirms. Apply the same variety (gentler) in the A2/B1 twin.

## 4. The twin (A2/B1)
Same story, **simpler retold version** (short sentences, common words), 10 easier key words, and a **simpler grammar point** tied to the story (e.g. past simple, comparatives, there was/were, prepositions) — NOT the B2/C1 point.

## 5. HARD RULES
- 4th-wall clean: no teacher notes, no pedagogy labels ("TEEP", "I Do/We Do"), no mode labels, no "Malcolm".
- Gap-fill inputs empty; answers only in hidden reveals.
- **Zero podcast/Listen/Noiser/Spotify content anywhere.**
- Dark themes (death, madness, poverty) handled soberly, never graphically.
- Keep all 5 tabs and the timer working.

## 6. Verify before reporting
Both files: `5` `tab-content` divs; `0` inputs with `value=`; crosslink present; **0 occurrences of "podcast", "noiser", "spotify", or "Listen"**; **Tab 0 uses ≥3 different vocab techniques and NO context sentence glosses its own target word**. Report filenames + one-line summary + "0 prefilled inputs" + the vocab techniques used.
