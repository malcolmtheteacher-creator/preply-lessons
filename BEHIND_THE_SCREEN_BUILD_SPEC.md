# Behind the Screen — Lesson Pair Build Spec

A speaking series that uses a famous film as the doorway into the **real** history, science, philosophy or myth underneath it. You build ONE lesson **pair**: a B2/C1 base + an A2/B1 twin. Work in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.

## 1. Clone the exemplar (do this FIRST)
READ these two files and **replicate their exact structure, CSS and JavaScript** — change only the content:
- B2/C1 exemplar: `behind_the_screen_interstellar.html`
- A2/B1 exemplar: `behind_the_screen_interstellar_a2b1.html`
Keep the `<style>` block and the `<script>` (tab switching + timer) **byte-identical**. Do not invent CSS classes.

## 2. Files to create
- Base:  `behind_the_screen_<SLUG>.html`
- Twin:  `behind_the_screen_<SLUG>_a2b1.html`

## 3. Five tabs, in this order (both levels)
**Key Words → The Film → Grammar — <POINT> → The Real Story → Speak**

**Header:** `<meta name="series" content="Behind the Screen">`; tag `BEHIND THE SCREEN · B2/C1 · 50 min` (twin `· A2/B1 · 50 min`); `<h1>` = the film title; a one-line subtitle that names the hook (the real thing underneath). Crosslink under the header (base → `_a2b1`, twin → base), exactly as in the exemplar.

**Tab 0 — Key Words:** an `.intention` line ("Today: you'll tell the story of <film>… discover how much is true… and master <grammar>…"); a short **warm-up = 2–3 discussion questions** (a `.note` box) that activate the theme — do NOT link to other lessons; then pre-teach **10 key words** in 3–4 small labelled activities using **varied techniques** (infer-from-context, closest-in-meaning, which-meaning-fits MCQ) — see §3a; end with a "use them out loud" `.discuss`.

### 3a. Unblocking the key words — VARIETY, self-contained, never gloss the answer
- Every word is **shown** (in bold in a natural sentence, or given for a synonym/MCQ choice). **Never ask the student to produce a word they haven't seen.**
- Every context is **self-contained**: the meaning is inferable from the situation ALONE — the student does NOT need to know the film yet. (No "the hero's defining trait is…" clues.)
- **No inline gloss:** never put the definition/synonym inside the word's own sentence; the answer appears only on Reveal.
- Words must be genuinely **B2/C1** (lower-frequency, abstract, precise) in the base; **simple/common** in the twin (twin uses an 8-item match-grid, like the exemplar).
- Use ≥3 distinct techniques across the 10 words.

**Tab 1 — The Film:** 3 parts (`.story-chunk`), the film's story told vividly and accurately, tightly abridged. **Spoilers are fine and expected** — say so once at the top ("we're here to talk about it"). Handle any violence/tragedy soberly. After each part: a from-memory **Quick check** (2 questions + hidden Reveal), then one `.discuss` question. Do NOT quote film dialogue at length (a few words max); describe, don't reproduce.

**Tab 2 — Grammar — <POINT>:** clear `.note` explanations + **3 gap-fill exercises**. Inputs MUST be empty (no `value=`, no answer in the prompt/hint). Teach with DIFFERENT example sentences from the ones you test. Answers live only in the hidden `.answers` reveals. Use the film's own situations to make the grammar vivid.

**Tab 3 — The Real Story:** the payoff of the series. Use the `.realstory-box` + `.story-chunk` + `.discuss` pattern from the exemplar. Lay out the **true** history / science / philosophy / myth the film draws on — **researched and accurate** (see §4). Be honest about where the film leaves the facts for drama. End with a `.discuss` block ("what's real, what's invented, does it matter?").

**Tab 4 — Speak:** keep the timer JS identical. 3 `.speak-prompt` tasks — A: retell the film using the grammar + 5 key words; B: a debate rooted in the film's central dilemma; C: a broader task WITH a 5–6 item idea menu (safe, non-personal options included); then a `.final-discussion` (3–4 bigger questions + a from-memory grammar recall).

**Footer:** `Behind the Screen · <Film> · B2/C1` (twin `· A2/B1`).

## 4. ACCURACY — non-negotiable
The whole point of the series is that the "Real Story" is TRUE. **Research every factual claim with WebSearch before writing it**, and do not invent people, dates, papers or quotes. If the film distorts history (e.g. Gladiator, Troy, The Imitation Game), say so plainly — "myth vs history" is often the best discussion. Get names and facts right.

## 5. The twin (A2/B1)
Same film, **simpler retold story** (short sentences, common words), 10 easy key words in the **8-item match-grid** format from the exemplar, and a **simpler grammar point** tied to the film — NOT the B2/C1 point. **The match-grid MUST be genuinely scrambled: list the meanings in a DIFFERENT order from the words, so the answer key is NEVER 1=A, 2=B, 3=C… (that pre-matches everything and tests nothing). Word N's meaning must sit under a different-position letter.** Same self-contained, no-inline-gloss vocab rule. A simpler "Real Story" tab (2 short chunks). 50 min.

## 6. HARD RULES (both levels)
- **4th-wall clean:** no teacher notes, no pedagogy/TEEP/mode labels, no "Malcolm", no "Simplified".
- Gap-fill inputs EMPTY; answers only in hidden reveals.
- Never reveal an exercise's answer in the example above it.
- Keep all 5 tabs and the timer working; end the file with `</html>`.

## 7. Verify before reporting
For BOTH files confirm: `0` inputs with `value=`; `5` `tab-content` divs; crosslink present; ends with `</html>`; JS still valid. Report: filenames + one-line summary + "0 prefilled inputs" + the grammar point + the vocab techniques used + a note on which facts you verified.

## 8. The launch line-up (film · grammar point · real-world hook)
- Interstellar · future perfect & continuous · relativity/time dilation, Dust Bowl **(exemplar — done)**
- The Matrix · 2nd & 3rd conditionals (unreal) · Plato's Cave, Descartes, simulation argument
- The Lord of the Rings · past perfect & narrative layering · Tolkien's WWI (the Somme), Norse & Anglo-Saxon myth, industrialisation
- Gladiator · modals of deduction about the past (must/might/can't have) · real Rome vs the film's invented Maximus; the real Commodus
- The Imitation Game · cleft sentences & emphasis (It was Turing who…) · Alan Turing, Enigma, Bletchley Park — and what the film changed
- Arrival · future-in-the-past (would; a foreseen future) · language & thought (the Sapir–Whorf hypothesis), linguistics
- Oppenheimer · modal perfects of regret (should/could/needn't have) · the Manhattan Project, Trinity, the moral reckoning
- Troy · passive & impersonal reporting (it is said / is thought to have) · Homer, the archaeology of Troy (Schliemann/Hisarlik), myth vs history — cross-links to `short_history_homers_epics.html`
