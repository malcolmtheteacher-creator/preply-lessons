# IELTS Writing through Stories — Lesson Build Spec

You build ONE "learn the essay shape through a story" lesson. Work in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.

## 1. Clone the template EXACTLY
READ `ielts_writing_opinion_essay.html` (the approved prototype). **Copy its entire `<style>` block and `<script>` block verbatim** — do not change any CSS or JS. Keep the same 5 tabs, the same 4-colour "part" system (`.part.intro` purple, `.part.b1` teal, `.part.b2` blue, `.part.concl` amber; and the `.map-cell` mi/mb1/mb2/mc classes). Change ONLY the visible content.

## 2. The 5 tabs (identical order, identical structure)
1. **The Story** — a bespoke mini-narrative (~180–230 words) whose four beats map 1:1 onto the four essay parts. Vivid, simple, memorable. End with a `.note` pointing to "The Shape".
2. **The Shape** — 4 `.map-row`s (story beat ↔ essay part, colour-coded via mi/mb1/mb2/mc), then 3 numbered rules (`.rule`) that name the golden rules of THIS essay type.
3. **The Model Essay** — a real IELTS question in a `.q-box`, then 4 `.part` blocks (intro/b1/b2/concl) each with its `.role` label, forming a Band-8-level model. Use a REAL example drawn from Malcolm's history/story lessons where possible. End with a `.note`.
4. **The Language** — 5 `.lang-group`s of `.chip` sentence stems, one group per move for THIS type.
5. **Your Turn** — a DIFFERENT real IELTS question in a `.q-box`, a colour-matched skeleton of empty `input.blank` fields (one per part), one full `textarea.blank`, an examiner `.checklist`, and a hidden "one possible plan" reveal (`#plan` with 4 `.part` blocks) toggled by the existing `togglePlan()`.

## 3. HARD RULES
- **Authentic IELTS questions only.** Every question in a `.q-box` must be a genuine, standard IELTS Task 2 question in its real wording for this exact type. Never paraphrase or invent a non-standard format.
- 4th-wall clean: no teacher notes, no "TEEP"/mode labels, no "Malcolm" in the body. Essay terms (Introduction, Thesis, Body Paragraph, Conclusion) are fine — that IS the subject.
- All `input`/`textarea` EMPTY (placeholders only, no real answers pre-filled). The only worked content is inside the hidden `#plan` reveal.
- Never use the word "Simplified".
- Keep the header gradient, the tab JS, and `togglePlan()` working.

## 4. Verify before reporting
Confirm: 5 `.panel` divs; 5 `.tab-btn`; the `<style>`/`<script>` match the template; the two `.q-box` questions are authentic standard IELTS wording; all inputs empty. Report: filename + one-line summary + the two questions you used.
