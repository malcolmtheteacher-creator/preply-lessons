# CEFR Grammar Lesson Spec (v2 rebuild, 2026-07-21)

The source of truth for every `grammar_*` lesson. The gold-standard template is
`grammar_b1_07_passive_voice_intermediate.html` — clone it, follow this spec, change only the content.

## Why v2 exists
The 2026-07-21 audit of all 82 v1 files found five systemic failures. Every v2 lesson must be
provably free of all five:

1. **Fake interactivity** — inputs that no JS ever read; "Check" buttons that praised anything.
2. **Tests that gave themselves away** — recall questions reusing taught sentences with answers a click away.
3. **Wrong English taught as correct** — e.g. "This shop is opened at 9 AM", "He regretted to inform us".
4. **4th-wall leaks** — "I Do / We Do / You Do", "Hook", "Metacognitive Check", "+Preply +Adult" visible to students.
5. **Overload & breakage** — 3–6 grammar points per file, broken tab wiring, half-built exercises.

## Hard rules

### Scope
- **One grammar concept per lesson.** Closely-related forms of the same concept are fine
  (e.g. passive across three tenses); unrelated points are not (prepositions + conjunctions + gerunds = 3 lessons).
- Overloaded v1 files get **split** into single-topic files; the CEFR dashboard is rewired accordingly.
- Content must fit a 50-minute 1-to-1 lesson.

### Register — everyday conversation first
- Example and exercise sentences are things people actually SAY: repairs, deliveries, plans,
  appointments, lost property, invitations, news about your town. Not corporate reports and bridges.
- A formal/written register example may appear once, labelled as such, where the grammar demands it.
- Every sentence must pass the "would a native speaker say this?" test. No invented citations
  ("from The Economist") — ever.

### Exercise integrity (the cardinal rule)
- **No exercise may be answerable by copying.** The answer must not appear anywhere earlier in the
  lesson — not in an example, a reveal, a placeholder, or a prompt.
- Teach with one set of sentences; test with a DIFFERENT set. Final-recall sentences are fresh,
  never recycled from the lesson.
- Placeholders in inputs show structure hints at most ("The road..."), never answer stems.
- Gap-fills are empty: no `value=`, no answer in the hint.
- Every gap has ONE defensible right answer (or all accepted variants are coded in).

### Real checking (mandatory)
Every typed exercise is validated by the shared checker (see template JS):
- `normalize()`: lowercase, trim, collapse spaces, strip end punctuation, expand contractions
  (it'll → it will, hasn't → has not, etc.).
- Each exercise defines `accept: []` (all correct variants incl. with/without agent, contractions),
  `errors: []` (regex → targeted feedback for the 2–4 most likely wrong answers: wrong participle,
  missing "been", active instead of passive, agreement), and `hint` (structure reminder fallback).
- Feedback is inline (no alert()), targets the TASK ("You need the past participle: *fixed*"),
  never the SELF ("Well done!" alone is banned).
- A correct answer gets specific confirmation of WHY it's right, not bare praise.
- Click-to-reveal is allowed only for open/discussion answers where free text can't be validated —
  and the reveal must show a *possible* answer clearly labelled as one option.
- MCQs: distractors must be plausible, all different, and each wrong option's feedback explains
  the error it represents.

### 4th wall (see /Users/malcolmtheteacher/CLAUDE.md)
- No pedagogy labels anywhere — not in headings, badges, tabs, OR HTML comments.
  Banned strings: I Do, We Do, You Do, Teacher Models, Hook, Retrieval, Activate, Demonstrate,
  Consolidate, Interleaving, Metacognition/Metacognitive, Spaced Repetition, TEEP, Preply, Adult, CEFR-tag headers.
- `<title>` is clean: "Passive Voice in Everyday English | B1" — no "+Preply +Adult".
- Tab names describe content in natural language, never phases.
- Speaking prompts are addressed neutrally ("Tell me about...", "SPEAK:"), never "your teacher will...".
- No student- or teacher-identifying details. Generic and reusable for any student at the level.

### Pedagogy (invisible to the student, structural for the builder)
Seven tabs following the TEEP backbone WITHOUT naming it:
1. **Warm-up** — invitational retrieval ("Have a go — what do you already know about...?"),
   one-line learning intention ("Today: X so you can Y"), a hook from everyday life.
2–4. **The content**, one small chunk per tab: notice-the-pattern first (student hypothesises
   before the rule is shown), structure box + visual, then 2–3 CHECKED production exercises per chunk
   with fresh sentences. Include one spoken task per tab ("Say three things that have been changed
   in your town").
5. **Real Task** — extended production, 70%+ student output, working timer, spoken first
   (1-minute monologue / role situation), written support second.
6. **Mix It Up** — interleaved practice: mixed forms in random order, error correction,
   choose-the-form MCQs. All checked. This is where strategy selection happens.
7. **What Do You Remember?** — recall of 2–3 points from earlier levels/lessons (real questions,
   generic if standalone), final retrieval with FRESH checked sentences, one reflection question
   ("Which practice helped most?"), and an "I can..." self-check tied to the learning intention.

### Technical
- Light background (#f8f9fa), dark text (#1a1a2e), purple accent (#667eea). No dark mode.
- Tabs centred; count of tab buttons MUST equal count of tab panels (v1 had an unreachable tab).
- Timers must actually run (teal → yellow <30s → red <10s + pulse). Never a dead timer.
- Mobile breakpoint 768px.
- No dead CSS for exercises that don't exist; no unused check functions.

### Verification checklist (run on every built file)
- [ ] Tab buttons == tab panels; every tab reachable.
- [ ] Zero `value=` on inputs; zero answers in placeholders.
- [ ] grep for banned 4th-wall strings returns nothing (including comments and <title>).
- [ ] Every input id has a checker entry; every checker entry has an input.
- [ ] No test sentence appears earlier in the file (grep each recall/exercise sentence).
- [ ] All MCQ options distinct.
- [ ] Timer(s) functional.
- [ ] Every example sentence reads as natural spoken English.
- [ ] A student alone can be told they are WRONG somewhere in every practice tab.

### File naming
Keep `grammar_<level>_<nn>_<topic>.html`. Splits take the next free numbers at that level and the
dashboard is updated in the same batch. Never the word "Simplified".
