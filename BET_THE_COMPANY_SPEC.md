# Bet the Company — Build Spec (business case-study series)

Real business stories, meaningful today, taught as English lessons for
professionals. C1, single level (no A2/B1 twin — the audience is executives
and business students). One lesson = one real case.

## 1. Clone the template
The template is the first lesson of the series:
`bc_orsted_bet_the_company_c1.html` (The Company That Bet Everything —
Ørsted). Replicate the entire <style> and <script> (tabs + timer). Change
only content. Do not invent new CSS classes.

## 2. Header
Tag: `BUSINESS ENGLISH · C1 · 50 min`.
`<meta name="series" content="Bet the Company">`.
`<h1>` = an evocative title for the case (NOT just the company name), with a
one-line subtitle stating the real story plainly. No crosslink paragraph.

## 3. FIVE tabs — Key Words → The Story → Grammar → Going Deeper → Speak
Structure and JS identical to the template (show(0)–show(4), Speak = tab 4).

- **Tab 0 — Key Words:** intention line naming the case AND the language
  target; 3 warm-up discussion questions pitched at working professionals
  (decisions they have made, not abstract theory); 10 business terms in 3–4
  varied activities (infer-from-context / which-term-means / a-b-c /
  collocation + word building), each behind a Reveal. Terms must be the real
  vocabulary of the case (e.g. stranded asset, write-down, headwinds), never
  generic business-English filler. NEVER gloss the term inside its own
  context sentence. End with a "use them out loud" discuss block that also
  sorts terms by register (board paper vs conversation).
- **Tab 1 — The Story:** the case in 3 parts (.story-chunk), told as a
  STORY with dates and numbers, not a Wikipedia summary. Rounded figures;
  no invented quotes. Part 3 must land on the live, unresolved question.
  After each part: 2-question quick check (hidden answers) + one .discuss
  question that connects the case to the student's own working life.
- **Tab 2 — Grammar:** ONE C1 executive-register focus per case (see list
  in §6), explained in .note boxes with business examples, then 3 gap-fill
  exercises building to a realistic spoken artefact (a board answer, a
  press line, an all-hands opening). Inputs EMPTY; answers only in hidden
  .answers reveals; teaching examples ≠ exercise sentences.
- **Tab 3 — Going Deeper:** open with a one-line note that figures are
  rounded and the case may still be developing; then the analysis — what
  the case actually tests, the assumptions nobody wrote down, the second
  and third lessons beneath the obvious one; then 3–4 discussion questions
  that turn the analysis back on the student's organisation.
- **Tab 4 — Speak:** timer JS identical. Task A = brief the board on the
  case (arc given in the prompt). Task B = survive a hostile question
  (analyst / journalist / chair), then repeat it compressed to 90 seconds.
  Task C = "four rooms" or an equivalent multi-audience task, ALWAYS with
  listed alternatives so nobody must use their own employer. Then a
  final-discussion of 4 harder questions, the last one a from-memory
  grammar recall.

**Footer:** `Business English · <Lesson title> · C1`. No byline.

## 4. Case rules
- REAL cases only, publicly documented; no invented dialogue or figures.
- Present as genuinely contested: the lesson never announces a moral; the
  Going Deeper tab argues at least two readings.
- Still-live cases are preferred over closed ones — the unresolved ending
  is the speaking prompt.
- Sensitive cases (fraud, disasters, job losses) handled soberly: facts,
  not drama; no mockery of named individuals.
- Rounded numbers, and a stated note that they are rounded.

## 5. HARD RULES (as for all lessons)
- 4th-wall clean: no teacher notes, no pedagogy labels, no "Malcolm".
- Gap-fill inputs empty (no value=); answers only in hidden reveals.
- No podcast/Spotify/Listen content.
- File names: `bc_<slug>_c1.html`, e.g. `bc_wirecard_c1.html`.

## 6. The series plan (grammar focus per case — each focus used once)
| # | Case | Working title | Grammar focus |
|---|------|---------------|---------------|
| 01 | Ørsted (LIVE) | The Company That Bet Everything | hedging & diplomatic distance |
| 02 | Nokia loses mobile (LIVE) | The Giant That Saw It Coming | past deduction & missed alternatives (must have / could have) |
| 03 | Kodak & the digital camera (LIVE) | The Invention in the Drawer | cause & effect language (lead to, stem from, set in motion) |
| 04 | Lego 2003 turnaround (LIVE) | Saved by Fewer Bricks | mixed conditionals in post-mortems |
| 05 | Blockbuster vs Netflix (LIVE) | The $50 Million Phone Call | concession & contrast (whereas, albeit, even so) |
| 06 | VW Dieselgate (LIVE) | The Cleverest Engineers in the Room | passives & impersonal accountability language |
| 07 | Wirecard (LIVE) | The Company That Wasn't There | reporting verbs (claim, allege, concede, deny) |
| 08 | Maersk & NotPetya (LIVE) | Ten Days Without Computers | narrative tenses for incident timelines |
| 09 | WeWork (LIVE) | The Vision Premium | the language of hype vs substance (emphasis, inversion, downtoning) |
| 10 | Boeing 737 MAX (LIVE) | The Culture That Signed It Off | obligation & responsibility (be required to, be supposed to, accountability) |
| 11 | Patagonia gives itself away (LIVE) | The Exit Nobody Priced | purpose, values & mission language (so as to, with a view to, cleft purpose) |
| 12 | Novo Nordisk & Ozempic (LIVE) | The Problem of Too Much Demand | forecasting & projection (future perfect, likely to, may well) |
| 13 | Hanjin collapse / Incoterms (LIVE) | Three Letters on an Invoice | contract language (shall, provided that, in the event of) |
| 14 | Translation industry vs AI (LIVE) | The Industry That Trained Its Replacement | comparison & degree (nowhere near as, all but closed, the more… the more…) |

Extend the table when adding cases; never reuse a grammar focus within the
series without a reason.

## 7. Dashboard
`bet_the_company_dashboard.html` — same visual system as the story
dashboards: header, intro, CASE 01–NN cards (title, company · years,
essence, "The question:" instead of "The turn:", grammar tag), how-it-works
strip. Add each new lesson as a card and keep the count line accurate.
Cards link only to lessons that exist.

## 8. Verify before reporting
5 tab-content divs · 0 value= inputs · 0 podcast refs · varied vocab
techniques · figures rounded · Going Deeper argues both sides · Task C has
non-personal alternatives.

## 9. Deploy
Malcolm pushes via ① Update (or asks for it explicitly).

| 15 | Online therapy reckoning (LIVE) | A Therapist in Your Pocket | relative clauses at C1 (sentence-relative which, many of whom, reduced) |
| 16 | ERP go-live disasters (LIVE) | Go-Live | verb patterns that change meaning (stop/try/remember + -ing vs to) |
