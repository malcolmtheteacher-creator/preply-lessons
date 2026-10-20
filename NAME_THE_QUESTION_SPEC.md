# Name the Question — pathway spec (C1, B2 later)

Status: **design record, not a settled syllabus.** Born 2026-10-20 from a ChatGPT thread
("Philosophy Visualisation Map") and the handover `structured_thinking_claude_handover.md`.
What is built so far: the dashboard with its mind map and a self-checking quiz. No new
lessons yet. Everything below the "Built" section is a proposal to be approved before authoring.

## 1. What it is, in one paragraph

Teach professionals to **recognise the kind of question they have been asked, choose a fitting
way of thinking, and then say a defensible answer clearly.** Language is the medium for the
reasoning, not a wrapper around a pre-written opinion. It sits *upstream* of Begin With the End:

> **Name it** (this pathway) → **Land it** → **Pause it** → **Hold it** (Begin With the End)

North star: *teach students to recognise the question, think it through with a suitable
structure, and communicate a defensible answer with clarity and flexibility.* The course
teaches how to reason and communicate, not a set of business opinions to recite.

## 2. Audience

C1 first. Senior and specialist professionals who are questioned under pressure — executives
(the Poland MD), consultants, doctors and other clinicians, specialists in any field — not
only people in business. B2 later, via the A2/B1-twin mechanism Think Inside the Box already
uses. Case facts are always **supplied**, so no outside industry knowledge is needed.

## 3. The model: THINK, then COMMUNICATE

| Stage | Move | Where it is taught |
|---|---|---|
| Think | **Recognise** the kind of question | this pathway (new) |
| Think | **Diagnose** constraints, stakeholders, uncertainty | this pathway + the tool lessons |
| Think | **Select** a lens and produce a provisional answer | Think Inside the Box (tools) |
| Say | Point → reason → stop; signpost; hold under challenge | Begin With the End |

These are teaching stages, not a universal algorithm. They loop and overlap; some questions
need a clarifying question before any recommendation.

## 4. The taxonomy: six kinds of question

Entry point is the **audible cue** (the question word), because that is what a learner can
actually hear. The cue is a clue, not a guarantee — see "look-alikes".

| Cue | Kind | The lens (questions to run, in order) | It can lead to | Breaks when… |
|---|---|---|---|---|
| Should we…? | Go / no-go under uncertainty | Can we undo it? Can we try it small first? What does waiting cost? | **Pilot** (undoable, testable, waiting cheap) · **Stage it** (hard to undo, but can be done in steps with checkpoints) · **Decide now** (waiting costs more than a wrong move) · **Decline for now** (can't undo, can't test, weak case) | there is no time to test — a pilot is just delay |
| Which…? | Choosing between options | What matters most? How does each option do on that? What do I give up with each? What would flip my choice? | A clear pick, with its price · a conditional pick ("A, unless…") · neither yet (the real answer is an option nobody has put forward) | options cannot share one scale |
| What first…? | Priorities | What is urgent, and what is only loud? Which few things cause most of the trouble? What depends on what? | Do now · do next, with a date · hand it on · leave it, and say so | everything really is urgent; the ranking is disputed |
| What if…? | Risk and scenarios | What could happen? How likely, how bad? What would warn us early? What is our response? | Prevent · reduce · prepare (warning sign + plan B) · accept knowingly | numbers give false comfort; the real surprise was unlisted |
| Why…? | Diagnosis | What exactly happened? What could explain it? What evidence tells the causes apart (cheapest check first)? How sure am I? | A leading cause, with a confidence · two causes you can't yet separate, and the one check that would · not enough data, and which data | causes interact; there is no single root cause |
| Is it right…? | **Boundary: values and ethics** | Who is affected and who decides? Which principles pull against each other? Would I accept this rule applied to me? What can I not know? | A position with its principle · a position with a limit · "it depends on X", and say exactly what X is — never a shrug | — the tools run out; say what you weigh |

Each kind also has a **worked example** (question → running the lens → how it might sound), and
"Should we…?" has a second, contrasting one (a possible contaminated-medicine recall, where the
same lens points to *decide now*). They are examples of the thinking, not answers to learn. All
are on the dashboard cards and in `pathway.json` (`lens`, `leads`, `example`, `contrast`).
The two outcome lines inside each map circle come from `map_out` (max 22 characters per line).

Design points:
- **Problem types are not conversation situations.** "Disagree or challenge" and "explain a
  decision" (in the handover's table) are covered by Begin With the End (Hold it / Land it), so
  they are not branches here.
- **Look-alikes are the real teaching.** "Should we fix the website or the payment system
  first?" begins with *should we* but is a priorities question. Novices sort by surface
  features, experts by structure — so every recognition activity includes contrast pairs.
- The sixth kind is where the lenses deliberately run out. It carries the "when the framework
  does not fit" test the handover asks for.
- Do not present any lens as a universal answer. A lens produces a provisional recommendation.

## 5. How it connects to what already exists

The pathway adds **no new case stories and no new tools**. It is a recognition layer that routes
to material already in the site.

| Layer | Existing home | Used for |
|---|---|---|
| Lenses (tools) | Think Inside the Box (23 lessons, 63-tool toolbox, "your own problem" chooser) | Think-it |
| Cases | Bet the Company (32 cases, each ends on a one-line question), Beyond Reasonable Doubt, Tylenol, Challenger | Practise-it |
| Delivery | Begin With the End (3 lessons) | Say-it |
| Clinicians | `b2_57_medical_ethics`, `b2_99_clinical_anxious_patient`, `bc_doctor_who_drank_it_b2`, `bc_healthcare_billing_c1`, `bc_tylenol_c1` | a "Working in medicine?" strip |
| Overlap to respect | Thinking Out Loud (`skills_c1_senior_interview_4_thinking`: hypothesis, trade-off, sense-check), Argument Structure (`sp_c1_02`), Calibrated Certainty, Rhetoric of Persuasion, c1_pro_28 Consulting Frameworks | link, don't duplicate |

Tool → kind mapping used on the map: PDCA, OODA → Should we; SWOT, Five Forces → Which;
Eisenhower, Pareto → What first; Risk Matrix, PESTLE → What if; Fishbone, Five Whys → Why.

## 6. Built (as of 2026-10-20)

**Structure: a short dashboard that navigates, and one page per kind of question.** The dashboard
holds only the map, a one-line guide and a link to the quick test; each map circle opens its own
page. The branch pages are where lessons will eventually sit, so the dashboard never has to grow.

| File | What it is |
|---|---|
| `name_the_question_dashboard.html` | The map (code-drawn; each circle shows its possible outcomes), a four-step guide, a link to the quick test, and a "Go further" row. About two screens. |
| `nq_pathway_should_we.html` · `nq_pathway_which.html` · `nq_pathway_what_first.html` · `nq_pathway_what_if.html` · `nq_pathway_why.html` · `nq_pathway_is_it_right.html` | One page per kind: **the lens** (numbered questions) beside **what it can lead to**; a **worked example** (Should we… has a second, contrasting one); **where it breaks**; **practise it** (tools and cases, linked); **talk it through** (three discussion questions); the three "say it" lessons; previous/next. `nq_pathway_is_it_right.html` also carries the "Working in medicine?" strip (`#medicine`). |
| `nq_pathway_quick_test.html` | "Which kind of question is it?" — 8 self-checking questions, two of them look-alikes. Each reason links to the matching kind page. |
| `tools/nameq_content/pathway.json` | All content. **Edit this to rearrange the map or change any page.** |
| `tools/build_nameq.py` | `python3 tools/build_nameq.py` rebuilds all eight pages. It refuses to build if a linked file is missing, a branch lacks lens/leads/example/talk/map_out/page, a map line is over 22 characters, or a quiz answer is out of range or repeats three times. |

All `nq_*.html` and the dashboard are **generated — never hand-edit.**

To move a branch, change its `x`/`y` in the JSON (canvas is 1800 × 1080; `side` is which way its
leaves fan out). To add a leaf, add an object to its `leaves` list. Keep leaf names ≤ 24
characters and descriptions ≤ ~30 so they fit the pills; leave 74 px between leaf rows.
Planned lessons should be named `nq_01_should_we_c1.html` etc., to stay distinct from the kind pages.

**Linked in:** `begin_with_the_end_dashboard.html` and `think_inside_the_box_dashboard.html` each carry a card pointing to the map (inserted by hand into the committed HTML; the same block is in `build_end.py` / `build_tib.py`, but **do not regenerate those two dashboards or the `end_*` lessons** without checking the diff — their committed HTML contains hand-added cross-link sections the builders do not produce).

**Not done:** the site index and search (see publish steps). To publish: run the site's Update command so the index and search pick the new pages up (the kind pages are named `nq_pathway_*` so the index treats them as hubs). A hand-illustrated map image (like `ThinkInsideTheBox_map.jpg`) can replace
the code-drawn one later using hotspots, as TIB does. The lens steps and outcomes for every kind
except "Should we…?" are first drafts and need a subject-expert read.

## 7. The lessons (built 2026-10-20)

Seven 50-minute C1 lessons, in the house five-tab format, built by `python3 tools/build_nq.py` from
`tools/nq_content/NN_<slug>.json` on the Think Inside the Box engine (`build_tib.py`), recoloured per kind.
**Generated — never hand-edit.** Tabs: **Key Words → The Cases → The Lens → Language → Speak**
(the capstone has Name it → Think it → Say it → Where it breaks).

| # | File | Lesson | Cases (facts drawn from the existing case lessons) | Language |
|---|---|---|---|---|
| 1 | `nq_01_should_we_c1.html` | Try It Small, or Do It Now | Amazon's hiring tool (kept small, never relied on) vs Tylenol 1982 (no time to test) | conditions; conditional inversion; recommend that + base |
| 2 | `nq_02_which_c1.html` | The Price of the Pick | BCG matrix and Alphabet's Other Bets; Klarna's hybrid | comparing, conceding, naming the price |
| 3 | `nq_03_what_first_c1.html` | Ninety Days and Thirteen Thousand Bricks | Apple 1997; Lego's turnaround | sequencing and focus; negative inversion; clefts |
| 4 | `nq_04_what_if_c1.html` | The Risk Nobody Listed | Maersk and NotPetya; Novo Nordisk's forecast range | likelihood, range and consequence |
| 5 | `nq_05_why_c1.html` | Who Knew, and When? | Nokia 2007–2011; Bicester Village's visit system | cause, evidence and deduction |
| 6 | `nq_06_is_it_right_c1.html` | Where the Tools Run Out | R v Dudley and Stephens; the 2023 BetterHelp regulatory action | principles, limits, judging the past |
| 7 | `nq_07_mixed_c1.html` | Name It, Think It, Say It | — (capstone) | 12 mixed questions to name; the six lenses from memory; four speaking rounds; questions that fit no lens |

Each lesson opens with a retrieval warm-up that recalls the previous lesson's lens, has ten key words
(context inference, "which term means", collocation gap), three-part cases with checks, the lens as
a diagram, a seven-item sort that tests the lens on new situations, grammar with two gap-fill
exercises, and three timed speaking tasks plus harder questions. Facts are as told in the existing
case lessons (Amazon, Tylenol, Alphabet, Klarna, Apple, Lego, Maersk, Novo Nordisk, Nokia, Bicester,
Dudley and Stephens, online therapy); figures are rounded, as those lessons state. **No new
research was done for these lessons, so any fact that matters should be re-checked against the
case lessons before it is relied on.**

Reasoning and English objectives stay separate: the sort and the "Where the lens breaks" notes test
reasoning; the grammar and speaking tasks test expression.

## 8. How learning is evidenced (no rubric needed)

- **Recognition is auto-checked.** The sort-and-check pattern marks it, as in every lesson.
- **Reasoning is self-checked.** Each lesson ends with a model answer to compare against (Lesson 1's "How it sounds" pattern), not a graded rubric.
- **One live test for the teacher:** in a later session, ask a question the learner has not seen and notice whether they name the kind unprompted.
- Completion and the learner's own reactions remain the soft signals.

## 9. Safeguards (from the handover's objections)

1. **Fluent but hollow:** require decisions grounded in supplied facts and a stated assumption.
2. **Framework overuse:** every lesson includes a "where it breaks" case.
3. **False certainty:** teach provisional recommendations and calibrated confidence; sometimes the right move is a clarifying question.
4. **Experience can't be fully packaged:** frameworks are practice habits, not a substitute for domain knowledge.
5. **"Two reasons" is not a rule:** the number comes from the logic and the audience.
6. **Interviews:** behavioural questions often want STAR/PARADE-style narrative; don't force a recommendation structure onto them.
7. **Keep the learner-facing tool simple** even if the model behind it is richer.

## 10. Theory notes (from memory — verify before putting any in front of a student)

- **Recognition-primed decision-making** (Klein): suggestive of what the Poland MD and the consultant do. Not verified as the explanation of their behaviour; Kahneman & Klein (2009) caution that intuition is only reliable where the environment is regular and feedback is fast.
- **Novice/expert sorting** (Chi, Feltovich & Glaser, 1981): novices sort by surface features, experts by structure — the reason for contrast pairs.
- **Minto's SCQA** (situation, complication, question, answer): the front end of the Pyramid; itself a recognition step.
- **Issue trees / hypothesis-driven problem solving:** the consulting method behind Thinking Out Loud.
- **Cynefin** (Snowden): a way to teach "this tool doesn't fit".
- **Toulmin model** (claim, grounds, qualifier, rebuttal): maps onto hedging and "I'd change my view if…".

## 11. Hard rules (as for every series)

4th-wall clean — no teacher notes, no pedagogy labels, no mode labels, no "Malcolm" in any student-facing HTML ·
gap-fill inputs empty; answers only in hidden reveals · teach and test with different sentences ·
sort answers never three in a row and never following the option order · facts web-checked,
numbers rounded and labelled · real cases only, presented as contested · generated pages are never
hand-edited — change the JSON and rebuild.

## 12. Decisions and open questions

**Decided (2026-10-20):** separate pages, not a pop-up. The dashboard stays a short map; each kind of question opens its own page.

**Still open:**

1. Final name ("Name the Question" is a working title).
2. Does lesson 1 use the 4-day-week pilots, Tylenol, or both as the contrasting pair?
3. Whether a hand-illustrated map image (ChatGPT, as for TIB) is wanted on top of the code-drawn one.
4. Where the pathway is first linked from (Begin With the End dashboard is the natural place).
