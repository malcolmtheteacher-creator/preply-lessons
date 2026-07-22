# Grammar Rebuild — Builder Brief (v2, 2026-07-21)

You are building ONE English-grammar lesson HTML file in `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`.
Your coordinator's prompt gives you: FILE (path to write), TITLE, LEVEL, SCOPE, and any SPLIT NOTES.

## Step 1 — Read completely, in this order
1. `GRAMMAR_LESSON_SPEC.md` (the rulebook — every rule in it is binding)
2. `grammar_b1_07_passive_voice_intermediate.html` (the gold-standard exemplar)

Clone the exemplar's CSS and its entire JS architecture verbatim in structure: `openTab`, `toggleReveal`, `normalize`, `EX` data object, `checkEx`, `showFb`, `MCQ` data object, `checkMCQ`, `checkMessage`, timer functions. Extend `normalize()` only if your lesson's contractions need it. Remove CSS classes your lesson genuinely never uses.

## Step 2 — Build the lesson (overwrite/create FILE)
- 7 tabs: **Warm-up** (invitational retrieval, one-line "Today: X so you can Y" intention, tiny everyday dialogue hook) / **2–3 content tabs** with natural names describing what you DO with the grammar / **Your Turn to Talk** (1-minute speaking task with the WORKING timer + a 3–5 sentence writing task checked by a `checkMessage`-style pattern scanner adapted to this lesson's target forms, reporting found/missing forms) / **Mix It Up** (3–4 error-correction full-sentence rewrites + 2–3 choose-the-form MCQs, all checked) / **What Do You Remember?** (1–2 recall items from more basic grammar typed+checked or revealed, then 3 FRESH checked sentences on today's grammar, one reflection question, "I can..." checkboxes tied to the intention).
- Each content tab: 3 real sentences → student spots the pattern BEFORE the rule is revealed → structure box → 2–3 CHECKED gap/transformation exercises with FRESH sentences → one SPEAK task (speak-chip box).
- Everyday-conversation register throughout (repairs, plans, food, family, travel, work small-talk — never corporate reports). Every sentence must pass "would a native speaker say this?" Every stated fact must be TRUE. No invented citations.
- Match instruction language to LEVEL (A1/A2: tiny simple words, short sentences; B1/B2: plain but natural; C1/C2: sophisticated but clear).
- If SPLIT NOTES name a sibling lesson, link to it ONCE in the final tab as "Next lesson" — do not open or duplicate it.
- Do NOT reuse sentences from the old version of the file. Do not open other grammar_ files.

## Hard rules (violations are failures)
- Every typed exercise has an `EX` entry: `accept[]` (all correct variants — remember `normalize()` lowercases, strips punctuation, expands contractions, so write accept strings and error regexes against the EXPANDED lowercase form), `errors[]` (2–4 regexes matching REALISTIC learner mistakes at this level, each with feedback that teaches the rule), `good` (explains WHY it's right), `hint` (structure reminder). One defensible right answer per gap — context must force it.
- No answer may appear anywhere earlier in the file — not in examples, reveals, placeholders or prompts. Teach with one sentence set, test with a different one. Final-recall sentences are fresh.
- MCQ options all different and plausible; per-option feedback explains the specific error.
- Feedback targets the task; never bare praise; never praises empty/wrong work.
- Banned strings anywhere (comments and <title> included): I Do, We Do, You Do, Teacher Models, Hook, Retrieval, Activate, Demonstrate, Consolidate, Interleav-, Metacogni-, Spaced Repetition, TEEP, Preply, Adult, Malcolm. (Natural-English substrings like "you don't" are fine — inspect grep hits and reword avoidable ones.)
- Tab button count == tab panel count. No `value=` on inputs. No dead CSS/JS. Timer must genuinely count down.

## Step 3 — Self-verify with Bash; fix every failure before reporting
1. `sed -n '/<script>/,/<\/script>/p' FILE | sed '1d;$d' > /tmp/chk_$$.js && node --check /tmp/chk_$$.js`
2. Banned-strings grep on the whole file; inspect every hit.
3. `grep -cE 'input[^>]*value='` must be 0.
4. Count `<button class="tab-btn` == count `<div id="tab` panels.
5. Every `checkEx('id')` call has a matching input id, `EX` key, and `id-fb` div — no orphans in either direction. Same for MCQs.
6. Recommended: simulate normalize()+EX matching in node for each correct answer and each planted error regex — no false accepts, no unreachable error messages.

## Step 4 — Report
Short report: file written, checklist results (each item), forms taught. Your final message is data for a coordinator, not prose for a human.
