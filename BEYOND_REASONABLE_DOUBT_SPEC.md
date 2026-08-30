# Beyond Reasonable Doubt — Build Spec (landmark legal cases series)

Real cases that made the rules ordinary people live under, taught as English
lessons for professionals. C1, single level (no A2/B1 twin — the audience is
lawyers, law students, compliance and contract people, and business
professionals who meet the law through liability, contracts and process).
One lesson = one real case. Sister series to **Bet the Company**
(BET_THE_COMPANY_SPEC.md) — same template, same five tabs, same rules.

## 1. Clone the template
The template is the first lesson of the series:
`lw_donoghue_c1.html` (The Snail in the Bottle — Donoghue v Stevenson).
Its `<style>` and `<script>` are byte-identical to
`bc_orsted_bet_the_company_c1.html`. Change only content. Do not invent new
CSS classes.

## 2. Header
Tag: `LEGAL ENGLISH · C1 · 50 min`.
`<meta name="series" content="Beyond Reasonable Doubt">`.
`<h1>` = an evocative title for the case (NOT the case citation), with a
one-line subtitle stating the real story plainly. No crosslink paragraph.

## 3. FIVE tabs — Key Words → The Case → Grammar → Going Deeper → Speak
Structure and JS identical to the template (showTab(0)–showTab(4), Speak = tab 4).

- **Tab 0 — Key Words:** intention line naming the case AND the language
  target; 3 warm-up discussion questions pitched at working professionals
  (situations they have actually been in — a contract, a complaint, a
  process that went wrong — not abstract jurisprudence); 10 legal terms in
  3–4 varied activities (infer-from-context / which-term-means / a-b-c /
  collocation + word building), each behind a Reveal. Terms must be the real
  vocabulary of the case (e.g. duty of care, consideration, burden of proof),
  never generic legal filler. NEVER gloss the term inside its own context
  sentence. End with a "use them out loud" discuss block that also sorts
  terms by register (pleading vs client email vs conversation).
- **Tab 1 — The Case:** the case in 3 parts (.story-chunk), told as a STORY
  with dates, people and facts, not a textbook headnote. Part 1 = the facts
  as they happened to a person. Part 2 = the legal problem and the argument.
  Part 3 = the judgment and the rule it created, landing on what is still
  contested. After each part: 2-question quick check (hidden answers) + one
  .discuss question connecting the case to the student's own working life.
- **Tab 2 — Grammar:** ONE C1 legal-register focus per case (see §6),
  explained in .note boxes with legal examples, then 3 gap-fill exercises
  building to a realistic spoken artefact (an advice to a client, a
  submission, a summing-up). Inputs EMPTY; answers only in hidden .answers
  reveals; teaching examples ≠ exercise sentences.
- **Tab 3 — Going Deeper:** open with a one-line note that the case is
  summarised, that jurisdictions differ, and that this is teaching material
  and not legal advice; then the analysis — what the case actually tests,
  the dissent or the counter-reading, the second and third rules beneath the
  famous one; then 3–4 discussion questions turning it on the student's own
  system or organisation.
- **Tab 4 — Speak:** timer JS identical. Task A = present the case to
  someone who has never heard it (arc given in the prompt). Task B = argue
  the losing side properly, then compress to 90 seconds. Task C = "four
  rooms" or equivalent multi-audience task (client / court / regulator /
  the person affected), ALWAYS with listed alternatives so nobody must use
  their own employer or a real matter. Then a final-discussion of 4 harder
  questions, the last one a from-memory grammar recall.

**Footer:** `Legal English · <Lesson title> · C1`. No byline.

## 4. Case rules
- REAL, publicly documented cases only; no invented dialogue or evidence.
  Judicial phrases may be quoted only where they are genuinely famous and
  short (e.g. "Who, then, in law, is my neighbour?").
- Present as genuinely contested: the lesson never announces a moral; Going
  Deeper argues at least two readings, and names the dissent where there was one.
- Not legal advice, and it says so. Jurisdiction is always stated.
- Cases involving death, wrongful conviction or atrocity are handled soberly:
  facts, not drama; the people harmed are named as people, never as examples.
- No live, politically polarised litigation (abortion, elections, current
  culture-war matters) — the series teaches register, not sides.

## 5. HARD RULES (as for all lessons)
- 4th-wall clean: no teacher notes, no pedagogy labels, no "Malcolm".
- Gap-fill inputs empty (no value=); answers only in hidden reveals.
- No podcast/Spotify/Listen content.
- File names: `lw_<slug>_c1.html`, e.g. `lw_miranda_c1.html`.

## 6. The series plan (one branch of law + one grammar focus per case)
| # | Case | Working title | Branch | Grammar focus |
|---|------|---------------|--------|---------------|
| 01 | Donoghue v Stevenson (1932) | The Snail in the Bottle | Negligence / tort | Defining scope — relative clauses & legal definition |
| 02 | Carlill v Carbolic Smoke Ball (1893) | The Advert That Became a Promise | Contract | Conditional obligation (provided that, unless, in the event of) |
| 03 | R v Dudley and Stephens (1884) | Four Men in a Boat | Criminal defences | Past modals & justification (had no choice but to, should have) |
| 04 | Miranda v Arizona (1966) | The Right to Say Nothing | Rights & procedure | Modals of rights & permission (may, must, be entitled to, need not) |
| 05 | Post Office / Horizon (1999–today) | The Computer Was Never Wrong | Evidence & miscarriage | Passives & presumption (it was held that, was deemed, is presumed) |
| 06 | Nuremberg (1945–46) | A Court for a Crime With No Name | International law | Reporting verbs of allegation (contend, submit, allege, hold, find) |

Extend the table when adding cases; never reuse a grammar focus within the
series without a reason. Candidates for extension: Liebeck v McDonald's (how
a case gets retold — hedging and attribution), Sally Clark (probability
language), McLibel (free expression), Carltona/judicial review (delegation),
Rylands v Fletcher (strict liability), the Herald of Free Enterprise
(corporate manslaughter).

## 7. Dashboard
`beyond_reasonable_doubt_dashboard.html` — same visual system as the other
series dashboards: hero header (CSS background stack: dark overlay + image +
gradient fallback, so the text always sits on top and the page works before
the image lands), intro, CASE 01–NN cards (title, case · years, essence,
"The question:", grammar tag), how-it-works strip. Hero image file:
`BeyondReasonableDoubt.png`. Add each new lesson as a card and keep the
count line accurate. Cards link only to lessons that exist.

## 8. Verify before reporting
5 tab-content divs · 0 value= inputs · 0 podcast refs · varied vocab
techniques · jurisdiction stated · not-legal-advice note present · Going
Deeper argues both sides · Task C has non-personal alternatives.

## 9. Deploy
Malcolm pushes via ① Update (or asks for it explicitly).
