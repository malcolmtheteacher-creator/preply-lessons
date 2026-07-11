# Everyday Echoes — Project File

**Read this first. It is self-contained: everything needed to keep building the role-play series, with paths, so nothing has to be rediscovered.**

---

## 1. What this is

A **speaking series built around everyday conversations as story role plays.** Each lesson drops the learner into one real situation — a ticket desk, a doctor's room, a market stall, a job interview — and hands them the language that makes that situation *go well*: how to ask a favour, soften a request, take bad news, push back politely, close warmly.

Every lesson is also tied — loosely, charmingly — to one lesson from the **Short History / Short Stories** library, via a final "Echo" tab. The everyday situation is the star; the history tie is a witty bow on top.

**Level: B2/C1. Length: 50 minutes. One level — no A2/B1 twins.**

**What students actually respond to (confirmed on the hotel lesson, which went down very well):** the **Useful Phrases** — real, transferable chunks they can carry out of the lesson and use in their own life. That is the beating heart of the series. Protect it; everything else serves it.

**Status: all 30 built, verified, live** — dashboard, homepage card, and cross-link banners on the History and Stories dashboards all done. Lessons 31+ would be new work.

---

## 2. Where everything is

Working directory (repo `preply-lessons`): `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`
Served live at `https://malcolmtheteacher-creator.github.io/preply-lessons/<file>.html`

| What | Path |
|---|---|
| **Template — clone this** | `rp_01_at_the_museum.html` |
| **Full build spec** | `ROLEPLAY_SPEC.md` (§5 = the 30 lessons + their history ties + fallbacks) |
| The 30 lessons | `rp_01_at_the_museum.html` … `rp_30_first_day_at_work.html` |
| Series dashboard | `everyday_echoes_dashboard.html` |
| Tied history lessons | `short_history_*.html` |
| Tied story lessons | `techniques_*.html` |
| Homepage (separate repo) | `/Users/malcolmtheteacher/Documents/01_Work/malcolmtheteacher-creator.github.io/index.html` |

---

## 3. The lesson shape — five tabs

🎬 **The Scene** → 💬 **The Conversation** → 🧰 **Useful Phrases** → 🎭 **Your Turn** → 🕰️ **The Echo**

- **🎬 The Scene** — 3–4 warm lines: who you are, where you are, what you need, and *who's across the desk*. Then 2 warm-up discussion questions, and a "who's who" card for the two roles. Ends by telling the reader to watch *how* the model asks, not just what they ask for.
- **💬 The Conversation** — the model dialogue, **12–16 turns**, natural native-feeling B2/C1: real softeners, hedges, understatement, the moment "no" quietly becomes "well, maybe". Then **3 from-memory comprehension questions** with a hidden Reveal (answers must not be visible before Reveal, and must not be copyable from the two lines above).
- **🧰 Useful Phrases** — the **10 key phrases** of this situation, grouped by move (Opening · Asking · Problems · Closing), each taught **guess-first**: a situation stimulus → the student says their guess aloud → Reveal the phrase + a note on why it works and its cousins. **Mix at least 3 techniques:** which-is-more-polite MCQ / complete-the-chunk / reorder-the-jumble / what-would-you-say. **This is the tab students value most — write it with the most care.**
- **🎭 Your Turn** — the role play, twice. Round 1: student is Role A, the page supplies Role B's lines and empty textareas with *guiding placeholders* ("soften first, then ask…"). Round 2: swap roles. Then ONE **twist card** — no script, a harder version of the situation, for improvisation. Click-to-start timer.
- **🕰️ The Echo** — the history tie in 3–4 delightful lines, a `.morelink` card to the tied lesson, and 2 bigger discussion questions bridging the everyday situation and the history.

**Register is the whole game.** Sophisticated functional language, never survival phrases. e.g. *"I don't suppose there are any places left…?"* · *"Failing that, is there a later tour we could fall back on?"* · *"Would there be any chance of putting two names down…?"*

---

## 4. Why the formula is shaped this way

The order is a deliberate teach-then-release arc — model → guided phrase work → free production — you just never name it on the page (4th wall):

- **The Scene** builds context and need before any language appears — the learner wants the phrases before they meet them.
- **The Conversation** is the model: the phrases seen alive, in a real exchange, doing real work.
- **Useful Phrases** pulls them out and teaches each **guess-first**. The guess is the point: forcing a learner to *produce before they check* is what makes the phrase stick, and it's why students remember these. Never invert it — never show the phrase before they've tried.
- **Your Turn** removes the scaffolding in two steps: guided (placeholders nudge) → free (the twist, no script). Both roles, so the learner rehearses the whole exchange from both sides.
- **The Echo** rewards the effort with meaning and a reason to read on.

At B2/C1 this deliberately does **not** add a controlled drill between the phrases and the role play — that would over-scaffold able learners and bore them. The jump from guided phrase to production is the desirable difficulty.

### Candidate improvements — under discussion, NOT yet adopted

The 30 live lessons all use the proven formula above. These are being weighed as evolutions; do **not** implement them across the series without Malcolm's go-ahead, and pilot on ONE lesson first (the hotel lesson, `rp_04`, is the proven hit — test against it):

1. **A personalisation rung.** After the 10 phrases, a short step where the learner ports 2–3 of them to their *own* life ("Where in your real week could you use 'failing that…'? Write the situation."). Reuse is exactly what students already value — this converts "a phrase I met" into "a phrase I own". Highest leverage, cheapest to add.
2. **Cross-lesson recycling / a phrase bank.** Today each role play is an island — no review, unlike Mia's shared spaced-repetition deck. A learner who loves these phrases never systematically meets them again. Options, cheapest first: (a) a cumulative "Everyday Echoes phrase bank" page grouped by function; (b) a light "phrases from earlier situations that also fit here" callback in each lesson; (c) a real SR engine like Mia's. Even (a) alone turns 30 islands into a course. **Biggest structural gap in the series.**
3. **A visible self-check after Your Turn.** Student-facing success criteria ("Did you soften before asking? Offer a plan B? Thank them by name?") so free production isn't a void with no way to judge it.
4. **A delivery cue.** For functional politeness, intonation carries the meaning — "I don't suppose…" said flat sounds sarcastic. A one-line "say it like you mean it" prompt, or a note on the melody, at least on the trickiest phrases.

---

## 5. HARD RULES — non-negotiable

1. **The 4th wall.** The student sees the HTML. No teacher notes, no pedagogy labels ("I Do", "We Do", "Retrieval", TEEP phase names), no reference to Malcolm, never the word "Simplified".
2. **All inputs empty.** No `value=` anywhere. Answers live only in hidden reveals (`.rev`, never `.rev open`).
3. **Never give the answer away in the stimulus above it.** A phrase must never be printed before the learner has to produce it. An example must never reuse an exercise sentence.
4. **Exercises must actually test.** Ask of every task: *could the learner get the marked answer without the knowledge it claims to test?* If yes, it's broken.
5. **Never introduce anything new in an answer key.** A reveal box is where a learner goes to feel certain — no untaught idiom, no fresh vocabulary. *(This rule exists because "belt and braces" — an untaught idiom — once appeared in a comprehension answer in the museum lesson. Malcolm caught it. Colour and idiom belong in the dialogue, and only when the surrounding lines make the meaning plain.)*
6. **Verify the tied lesson file EXISTS** before linking. Use the fallback in `ROLEPLAY_SPEC.md` §5 if the first choice is missing.

---

## 6. How to build a new one (rp_31+)

1. Copy `rp_01_at_the_museum.html`. Keep its `<style>` and `<script>` **verbatim** — change content only.
2. Structure that must survive: 5 `.panel` divs (`id="p0"`–`p4`, one `class="panel active"`), 5 `.tab-btn` (one `.active`), and the JS `showTab()`, `toggleRev()`, `startTimer()/resetTimer()/setDuration()`.
3. Content classes to use: `.say.say-a` / `.say.say-b` (speech bubbles, labelled by role), `.q` (question card), `.jumble`, `.choice`, `.rev` + `.rev-btn`, `.twist`, `.timer`, `.echo-card`, `.morelink`, `ol.bigq`.
4. Pick a tied history/story lesson, confirm the file exists, write the Echo.
5. Add a `.lcard` to `everyday_echoes_dashboard.html` (`.lnum` / `.lbody` `.lt` `.ld` `.lg` / `.lgo`), showing which history it echoes.

**Verify before reporting:** 5 panels · 0 `value=` inputs · reveals hidden by default · Echo link resolves to a real file · ≥3 phrase-teaching techniques · no untaught idiom in answers.

Fast check from `gitsite/`:
```bash
for f in rp_*.html; do
  echo "$f panels=$(grep -o 'class="panel' $f | wc -l) value=$(grep -c 'value=' $f)"
done
```
(The crude 4th-wall grep for "I Do"/"You Do" throws false positives on natural speech — "I **do** appreciate", "I **don't** suppose" — so read the hits before trusting them.)

---

## 7. Where it's wired into the site

- `everyday_echoes_dashboard.html` — 30 cards, each showing which history it echoes.
- `short_history_dashboard.html` and `short_stories_long_shadows_dashboard.html` — each carries a teal/amber "🎭 Now go and speak it — Everyday Echoes" banner below its intro, so the link runs both ways.
- Homepage `index.html` — an Everyday Echoes card in the "Speaking-led series" grid.

---

## 8. Deploying

```bash
cd /Users/malcolmtheteacher/Documents/01_Work/gitsite
git add <files> && git commit -m "..." && git push origin main
```
GitHub Pages rebuilds in a minute or two. The **homepage is a separate repo** — push it separately.

⚠️ The stored token can **push** but **cannot open pull requests** (403), and `gh` is not installed. Push straight to `main`; don't waste time trying to open a PR.

---

## 9. Open items

- **Formula evolution (§4).** The personalisation rung and the phrase bank are the two worth trialling; pilot on `rp_04` (hotel) before touching all 30.
- **Quality read, offered but not yet run:** re-read all 30 lessons' comprehension answers and dialogue for the rule-5 fault — idioms or slang used but never explained. Needs a human-style read, not a grep; Malcolm decides what's a genuine problem before anything changes.
- Lessons 31+ if the series is extended.

---

## 10. Working with Malcolm

He is an English teacher of thirty years, **not a coder**. Talk about the student-facing content in plain English and keep the tooling invisible. Don't over-engineer.

When he flags a problem, **open the file and look at it** before theorising — and if he tells you you've misdiagnosed it, you have. He catches real pedagogical faults automated checks miss: answers visible above the exercise, gap-fills with several right answers, untaught idioms in answer keys. Fix the *class* of problem, not just the instance.
