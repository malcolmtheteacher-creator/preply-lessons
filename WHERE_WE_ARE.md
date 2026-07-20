# Role plays — where we are

**Last updated: 20 July 2026, end of the big audit session.** Read this first when picking the work back up.

---

## BUILDING NEW ROLE PLAYS — the current checklist (follow exactly)

When Malcolm says "build N new role plays", this is the whole process:

1. **Read first:** `FUNCTIONAL_SPEC.md` (the build rule) and `ATTESTED_PHRASES.md` (the phrase bank).
2. **Check for duplicates** before proposing anything: the three dashboards
   (`everyday_echoes_dashboard.html`, `modern_life_dashboard.html`,
   `english_at_work_dashboard.html` — 40 + 15 + 30 live situations) AND
   `BUILD_QUEUE.json` (the ~60 off-site situations awaiting rebuild — their
   situations are reserved).
3. **Propose situations + phrase lists to Malcolm BEFORE building** — his rule.
   Phrases come from `ATTESTED_PHRASES.md` or new research (2–3 sources, added
   to the bank first). NEVER invent phrases: COLLECT, don't COMPOSE. If he says
   "go" without wanting the approval round, build — but the phrases still come
   from the bank.
4. **Numbering — next free:** `rp_41`, `ml_35`, `wk_41`.
5. **Build by hand, one at a time** (never agent fan-outs), via
   `content/<name>.py` → `python3 make_lesson.py content/<name>.py`.
   Five panels: Scene · Conversation · Useful Phrases · Your Turn · Echo.
   - Your Turn: BOTH rounds scripted — partner lines as bubbles, cued gaps,
     chairs swapped with changed details in Round 2. Never "use your own
     situation".
   - Echo: tie to a real `short_history_*.html` (104) or `techniques_*.html`
     (41) — VERIFY the file exists. Check the echo isn't already used by
     another lesson if a fresh one is available.
6. **Wire up:** add cards to the right dashboard (short plain descriptions,
   ≤8 words, what the student will DO). New EE lessons have no A2/B1 twin →
   card gets `data-nolevel="1"` placed AFTER the href (the finder's regex
   requires href immediately after class). Add titles to the PLANS dict in
   `group_dashboards.py`, then run `python3 group_dashboards.py` and
   `python3 build_roleplay_finder.py`.
7. **Fix the counts:** EE dashboard header/footer text (currently "forty
   conversations"), and the homepage repo
   (`../malcolmtheteacher-creator.github.io/index.html`) cards — currently
   40 / 15 / 30. The homepage is a separate repo with its own push.
8. **Commit and push** (straight to main; the token can't open PRs), then
   confirm live with curl against `malcolmhyndman.com/preply-lessons/…`.

## Current state (20 July)

- **Live and phrase-audited: 98 role-play situations** — Everyday Echoes 40
  (30 with A2/B1 twins), Modern Life 15, English at Work 30. All 1,231 taught
  lines audited against the attested bank; Malcolm's five flagged fixes in the
  originals applied.
- `ATTESTED_PHRASES.md` — the phrase bank (British Council B2 + B1 speaking
  units, plus three ESL collections). Grows one researched function at a time.
- `EXISTING_COVERAGE.md` is STALE (lists 60) — use the dashboards + queue for
  dupe-checking instead.

## Open items

1. **The 30 EE A2/B1 twins have never been phrase-checked** — the one
   remaining audit gap.
2. New EE lessons rp_31–40 have no A2/B1 twins (toggle skips them safely).
3. The off-site rebuild queue (~60 lessons in `BUILD_QUEUE.json`): remaining
   wk (Your Younger Boss, The Reference, Promoted Over a Friend, The Colleague
   Who Cries, The Truce, Not Coping at Work, The Joke, Chairing the Meeting,
   Asking to Work From Home, The Changing Brief — some may since be done),
   then ml_07–25, then the Life in English (lf_) series decision.
4. **Mia's English images: 73 of 100 missing** — copy-paste prompt list live at
   `mia_missing_prompts.html`; generation method (ChatGPT via Chrome) in
   Malcolm's memory notes.

## What Malcolm has said, that must not be forgotten

- **Functional English at the heart.** Situations are the vehicle; the
  function is the cargo.
- **Functions expand per domain.** A doctor breaking bad news and a
  salesperson handling a brush-off share almost nothing. Do not build a canon
  of 30 generic functions and recycle them.
- **Every phrase must survive its nouns being swapped.** If it only works in
  this scene, it is not a phrase.
- **One student, one teacher.** Your Turn is always two-handed. A third voice
  may appear in the model dialogue only, never as a role to play.
- **Multiple exponents per function are good** — the original `wk_` lessons do
  this ("Let me take that in order." / "Give me a second to do that justice.")
  and it is better than one phrase per function.
- **The summaries on cards must be short and plain** — max ~8 words, saying
  what the student will *do*. Not clever.
- Malcolm is a teacher of thirty years, not a coder. Talk about the
  student-facing content. Do not report structural metrics as if they were
  quality.

---

## Open questions for when you're back

1. **The 30 A2/B1 twins in Everyday Echoes have not been checked** for the
   phrase fault. They were simplified from sound originals, so they may be
   fine — but nobody has looked.
2. **Order of the remaining 61.** Suggestion: finish English at Work (the
   professional ones, closest to real students), then Modern Life, then decide
   whether "Life in English" comes back as a series or gets folded in.
3. **New professional domains.** The clinical pair (`wk_26`, `wk_27`) opened
   this up. A first sales call in English is designed and unbuilt — the phrase
   list is in the conversation. Law, teaching, hospitality, engineering all
   untouched.
4. **Cost.** The agent fan-out approach burned the usage limit twice and
   produced nothing usable. Build these by hand, one at a time.

---

## Files that matter

| File | What it does |
|---|---|
| `FUNCTIONAL_SPEC.md` | The build rule. Read first. |
| `BUILD_QUEUE.json` | The 90 designed situations + their old phrase spines |
| `make_lesson.py` | Assembles a lesson from `content/*.py`, checks hard rules |
| `group_dashboards.py` | Groups the dashboards into sections |
| `build_roleplay_finder.py` | Rebuilds the searchable finder |
| `content/*.py` | Source for every rebuilt lesson |
| `① Update Lesson Index.command` | Runs everything and pushes both repos |
