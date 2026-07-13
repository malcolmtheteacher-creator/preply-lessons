# A2/B1 Role-Play Twin — Build Spec

Make the **A2/B1 twin** of an Everyday Echoes role play: the SAME situation as the B2/C1 lesson, in simple, easy English. Working dir: `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`

## Template & sources
- **Clone `rp_04_checking_into_a_hotel_a2b1.html`** — copy its `<style>` and `<script>` VERBATIM (do not change CSS/JS). It defines the A2/B1 format, including the `.levelnote` bar. (`rp_03_at_the_doctors_a2b1.html` is a second worked example.)
- **Read the B2/C1 source** (`rp_NN_slug.html`) for the situation, the two roles, and which history/story lesson its Echo links to. You are re-telling that same situation, simpler.

## Level (this is the whole point)
- Short, simple sentences. High-frequency words. Grammar around A2/B1: present simple, basic past, `can I…?`, `I would like…`, `is … possible?`, `there is a problem with…`, `… doesn't work`.
- No idioms. If one is unavoidable, gloss it in plain words. **Never** put an untaught word/idiom in an answer key.
- Header tag: `Everyday Echoes · Role Play · A2/B1 · 50 min`. Footer: `Everyday Echoes · <Title> · A2/B1`. Title = the same situation name. `<meta name="series" content="Everyday Echoes">`.
- Right under `</header>`, keep the level-note: `<div class="levelnote">This is the easier version. <a href="rp_NN_slug.html">Want the harder one? → Full B2/C1 version →</a></div>`

## The five tabs (same icons/order)
🎬 The Scene → 💬 The Conversation → 🧰 Useful Phrases → 🎭 Your Turn → 🕰️ The Echo. Panels id p0–p4 (one `panel active`); tab-btns (one `active`).

1. **🎬 The Scene** — 3 short simple paragraphs; "Warm up — talk for one minute" with 2 easy questions (`ol.bigq`); "Who's who" two `.who` cards (YOU + the other person); a closing `.tip` (a friendly, simple note — e.g. it's OK to speak slowly / ask them to repeat).
2. **💬 The Conversation** — a simple model dialogue, **10–14 short turns**, `.say.say-a` = the other person, `.say.say-b` = You. Then "From memory — don't look up!" with 3 simple questions in a `.q` + hidden `.rev` (answers not visible before reveal, not copyable from the lines above).
3. **🧰 Useful Phrases** — `.lead`; a `.deliver` box (a simple "say it nicely / it's OK to ask" tone tip); **8 phrases** in `.q` cards under ~4 `h3` move-headings. Each taught **guess-first**: a simple situation → `.rev` with the phrase + a very simple why + one or two easy cousins. **Never print the phrase in its own stimulus.** Use **≥3 techniques**: multiple-choice (`.choice` divs), complete-the-chunk (`___` gaps), reorder a short jumble (`.jumble` spans, 3–4 words only), and say-it-yourself (reveal a simple model). Then a `.keep` box "🔑 Make them yours" (short intro + 3 `.cue` lines each with an empty `textarea.blank`, porting phrases to the student's own life). Then a `.tip` "Quick test". (NO phrase-bank link — Everyday Echoes has none.)
4. **🎭 Your Turn** — `.lead`; the `.timer` block VERBATIM from the template (3-min default); "Round 1 — you are [role]" = the other person's `.say-a` lines interleaved with EMPTY `textarea.blank` (placeholders that GUIDE and give a sentence-starter, e.g. "Start: 'I would like…'"); "Round 2 — now YOU are [the other role]" swapped; a simple `.twist` card (one small complication, plainly written); then a `.check` box "Before you finish…" with 5 simple tick `<li>`.
5. **🕰️ The Echo** — an `.echo-card` with 3 short, simple paragraphs tying the situation to the history/story (plain language); a `.morelink` to that lesson — use its `_a2b1` version if that file exists in the folder, otherwise the file the B2/C1 source links to; then "Two questions to talk about" (`ol.bigq`, 2 simple questions).

## HARD RULES
- 4th wall: the student sees this. No teacher notes, no pedagogy labels, no "Malcolm", never "Simplified".
- ALL inputs empty: no `value=` anywhere; answers only in hidden `.rev` (never add class `open`).
- Never give the answer away in the stimulus above it; teaching examples ≠ exercise sentences. Every exercise must actually test.

## Also: link back from the B2/C1 lesson
In the B2/C1 source `rp_NN_slug.html`, right after `</header>` (only if it isn't already there), insert:
`<div style="display:flex; align-items:center; gap:8px; justify-content:center; background:#fff; border:1px solid var(--line); border-radius:12px; padding:10px 14px; margin-bottom:14px; font-size:0.95rem; color:#6f685d;">New to English? <a href="rp_NN_slug_a2b1.html" style="color:var(--teal-d); font-weight:700; text-decoration:none;">Try the easier A2/B1 version →</a></div>`

## Verify before reporting
5 `.panel`; 0 `value=`; 8 phrases; `.deliver`, `.keep` (3 empty textareas), `.check` (5 items) all present; Echo `.morelink` resolves to a real file; ≥3 techniques; all `.rev` hidden; the reverse link is now in the B2/C1 source. Report: the new filename and the 8 phrases.
