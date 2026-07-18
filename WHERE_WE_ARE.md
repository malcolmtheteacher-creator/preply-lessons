# Role plays — where we are

**Last updated: 18 July 2026.** Read this first when picking the work back up.

---

## The short version

The role-play library was rebuilt from the wrong end. Lessons were written as
*situations*, and the "Useful Phrases" were then scraped out of the invented
dialogue — which produced set dressing (*"Mum mentioned the wing mirror."*)
rather than functional English. Malcolm caught it. Everything built that way
has been taken off the site and is being rebuilt **functions-first**.

The rule is written in **`FUNCTIONAL_SPEC.md`**. Read that before writing
anything.

---

## What is LIVE and sound

| Series | Count | Status |
|---|---|---|
| **Everyday Echoes** | 30 situations × 2 levels | Original. The model. Zero duplicate phrases across all 30. Grouped into 6 sections. |
| **Modern Life** | 6 | All sound — 5 rebuilt functions-first, `ml_01` Group Chat had 2 faults fixed. |
| **English at Work** | 12 | 6 original (2 small patches) + 6 rebuilt functions-first. |

Live at `https://malcolmhyndman.com/preply-lessons/`

### Rebuilt functions-first (11 so far)
- `wk_22` The Unpaid Invoice — chasing a client who hasn't paid
- `wk_26` The Consultation — taking a patient's history in English *(new: clinical)*
- `wk_27` Breaking the News — giving a diagnosis, checking it landed *(new: clinical)*
- `wk_13` The Mistake — telling your boss you've broken something
- `wk_11` Saying No to Your Boss — making the trade visible
- `wk_09` The Performance Review — taking criticism, still asking
- `ml_02` The Screen-Time Talk · `ml_03` The Honest Review · `ml_04` Back in Touch
- `ml_05` A Photo of You · `ml_06` The Collab

### Patched, not rebuilt
- `wk_05` Negotiating — removed a duplicated phrase
- `wk_06` The Interview — replaced an instruction masquerading as a phrase
- `ml_01` The Group Chat — removed duplicate phrase 6, made phrase 8 portable

---

## What is OFF the site, waiting

**61 lesson files** sit on disk with their dashboard cards removed, so no
student can reach them. They get **overwritten in place** — same filename, so
links, the finder and the phrase banks all just work again when each one
returns.

- `lf_*` (27) — the whole "Life in English" series. Dashboard and phrase bank
  deleted; the series is currently not on the site at all.
- `ml_07`–`ml_25` (19)
- `wk_07`–`wk_25` minus the rebuilt ones

Their situations and original phrase spines are in **`BUILD_QUEUE.json`**.
The situations are worth keeping — the phrases are not.

---

## How to build one

1. Pick a situation.
2. Write the **phrase list first** — functions named, exponents chosen.
   Show Malcolm. **Do not write HTML until he's passed it.**
3. Write the content file in `content/<name>.py` (title, intro, 5 panels).
4. `python3 make_lesson.py content/<name>.py` — assembles it using the
   verbatim CSS/JS shell and checks the hard rules.
5. Add the card to the dashboard, then `python3 group_dashboards.py`.
6. `python3 build_roleplay_finder.py`, commit, push.

Or just run **① Update Lesson Index.command**, which now does steps 5–6 and
pushes both repos.

---

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
