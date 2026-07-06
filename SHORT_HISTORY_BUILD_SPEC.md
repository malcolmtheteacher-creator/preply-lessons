# Short History, Long Echoes — Lesson Pair Build Spec

You build ONE lesson **pair**: a B2/C1 base + an A2/B1 twin. Work in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.

## 1. Clone the template (do this first)
READ these two files and **replicate their exact structure, CSS and JavaScript** — change only the content:
- B2/C1 template: `short_history_houdini.html`
- A2/B1 template: `short_history_houdini_a2b1.html`
Keep the `<style>` block and the `<script>` (tab switching + timer) **identical**. Do not invent new CSS classes.

## 2. Files to create
- Base:  `short_history_<SLUG>.html`
- Twin:  `short_history_<SLUG>_a2b1.html`

## 3. Five tabs, in this order (both levels)
**Key Words → The Story → Grammar — <POINT> → Listen → Speak**

**Header:** tag `SHORT HISTORY, LONG ECHOES · B2/C1 · 50 min` (twin: `A2/B1 · 50 min`); `<meta name="series" content="Short History, Long Echoes">`; `<h1>` = topic + a one-line subtitle. Crosslink under the header — base: `Need an easier version? <a href="short_history_<SLUG>_a2b1.html">Read this lesson at A2/B1 level →</a>`; twin: `Want more detail? <a href="short_history_<SLUG>.html">Read this lesson at B2/C1 level →</a>`.

**Tab 0 — Key Words:** an `.intention` line ("Today: you'll tell the story of… and master <grammar>…"); a short **warm-up = 2–3 discussion questions** that activate what the student already knows (do NOT link to other lessons — avoids broken links); then **10 key words**, each hidden in a natural context sentence with a Reveal button + clear definition (use the `.guess-item`/`.reveal-btn`/`.meaning` pattern); end with a short "use them out loud" `.discuss`.

**Tab 1 — The Story:** 3 parts (`.story-chunk`), genuine history, tightly abridged, vivid. After each part: a from-memory **Quick check** (2 questions + a hidden Reveal-answers block), then one `.discuss` question.

**Tab 2 — Grammar — <POINT>:** clear explanation in `.note` boxes; **3 gap-fill exercises**. Inputs MUST be empty (no `value=`, no answer shown in the prompt/hint). Answers live ONLY in the hidden `.answers` reveal.

**Tab 3 — Listen:** use the Houdini `.podcast-box` pattern. Name the real episode **"Short History Of… <Topic>"**, link to the real **Spotify show** page `https://open.spotify.com/show/2mcJ0sFMn4TdKCQrxoLPgO`, and add "search 'Short History Of <Topic>' to open the episode". Do NOT invent a specific episode URL (never guess a `/episode/...` link). Then a `.discuss` "listen out for" block (2–3 prompts).

**Tab 4 — Speak:** keep the Houdini **timer** JS identical; 3 `.speak-prompt` tasks — A: retell the whole story using the grammar + 5 key words; B: an opinion/debate; C: a broader task WITH safe non-personal alternatives; then a `.final-discussion` (3–4 bigger questions + a from-memory grammar recall).

**Footer:** `Short History, Long Echoes · <Topic> · B2/C1` (twin `· A2/B1`). No byline.

## 4. The twin (A2/B1)
Same topic, **simpler retold story** (short sentences, common words), 10 easier key words, and a **simpler grammar point** tied to the topic — NOT the B2/C1 point (e.g. past simple, comparatives, there was/were, prepositions).

## 5. HARD RULES
- 4th-wall clean: no teacher notes, no pedagogy labels ("TEEP", "retrieval", "I Do/We Do"), no mode labels, no "Malcolm".
- Gap-fill inputs empty; answers only in hidden reveals.
- Story text tightly abridged. Keep all tabs and the timer working.
- Any violence/tragedy: handle it soberly and historically, never graphically.

## 6. Verify before reporting
grep to confirm, for BOTH files: `0` inputs with `value=`; `5` `tab-content` divs; crosslink present. Report: filenames + a one-line summary + "0 prefilled inputs".
