# Everyday Echoes — Project File

**Read this first. Everything you need to keep building the role-play series.**

A speaking series: **everyday conversations as story role plays**, each tied (loosely, charmingly) to one lesson from the Short History / Short Stories library. **Level B2/C1. 50 minutes. One level only — no A2/B1 twins.**

Status: **all 30 built, verified and live.** Lessons 31+ would be new work.

---

## 1. Where everything is

| What | Path |
|---|---|
| Working dir (repo `preply-lessons`) | `/Users/malcolmtheteacher/Documents/01_Work/gitsite/` |
| **Template — clone this** | `rp_01_at_the_museum.html` |
| **Full spec** | `ROLEPLAY_SPEC.md` (§5 = the 30 lessons + their history ties) |
| The 30 lessons | `rp_01_*.html` … `rp_30_*.html` |
| Series dashboard | `everyday_echoes_dashboard.html` |
| Tied history lessons | `short_history_*.html` |
| Tied story lessons | `techniques_*.html` |
| Homepage repo | `/Users/malcolmtheteacher/Documents/01_Work/malcolmtheteacher-creator.github.io/index.html` |

Live at `https://malcolmtheteacher-creator.github.io/preply-lessons/<file>.html`

---

## 2. The lesson shape — five tabs

🎬 **The Scene** → 💬 **The Conversation** → 🧰 **Useful Phrases** → 🎭 **Your Turn** → 🕰️ **The Echo**

- **Header tag:** `Everyday Echoes · Role Play · B2/C1 · 50 min`. Meta: `<meta name="series" content="Everyday Echoes">`. Footer: `Everyday Echoes · <Title> · B2/C1`.
- **🎬 The Scene** — 3–4 warm lines setting the situation; 2 warm-up discussion questions; a "who's who" card for the two roles.
- **💬 The Conversation** — 12–16 turn model dialogue, natural B2/C1 with real softeners and hedges. Then 3 **from-memory** comprehension questions with a hidden Reveal.
- **🧰 Useful Phrases** — the 10 key phrases, grouped by move (Opening · Asking · Problems · Closing), each taught **guess-first**. Mix **at least 3 techniques**: which-is-more-polite MCQ / complete-the-chunk / reorder-the-jumble / what-would-you-say.
- **🎭 Your Turn** — the role play twice: Round 1 student plays Role A, Round 2 they swap. All student lines are **empty textareas with placeholders only**. Then ONE twist card for improvisation. Click-to-start timer.
- **🕰️ The Echo** — the history tie in 3–4 delightful lines, a `.morelink` card to the tied lesson, and 2 bigger discussion questions bridging the everyday and the historical.

**Register:** sophisticated functional language, not survival phrases. e.g. *"I don't suppose there are any places left…?"* · *"Failing that, is there a later tour we could fall back on?"* · *"Would there be any chance of putting two names down…?"*

---

## 3. HARD RULES — non-negotiable

1. **4th wall.** The student sees the HTML. No teacher notes, no pedagogy labels ("I Do", "Retrieval", TEEP phases), no "Malcolm", never the word "Simplified".
2. **All inputs empty.** No `value=` anywhere. Answers live only in hidden reveals (`.rev`, never `.rev open`).
3. **Never give the answer away in the stimulus above it.** A phrase must never be printed before the student has to produce it. An example must never reuse an exercise sentence.
4. **Exercises must actually test.** Ask of every task: *can the student get it right without knowing the answer?* If yes, it's broken.
5. **No untaught idiom in an answer key.** *(Added after the "belt and braces" fault — an untaught British idiom appeared in a comprehension answer, where the student goes to feel certain. Colour in the dialogue is fine only if the surrounding lines make it clear.)*
6. **Verify the tied lesson file EXISTS** before linking. Use the fallback listed in `ROLEPLAY_SPEC.md` if missing.

---

## 4. How to build a new one (rp_31+)

1. Copy `rp_01_at_the_museum.html`. Keep its `<style>` and `<script>` **verbatim** — change content only.
2. Structural bits that must survive: 5 `.panel` divs (`id="p0"`–`p4`, one `class="panel active"`), 5 `.tab-btn` (one `.active`), `showTab()`, `toggleRev()`, `startTimer()/resetTimer()/setDuration()`.
3. Content classes: `.say.say-a` / `.say.say-b` (speech bubbles), `.q` (question card), `.jumble`, `.choice`, `.rev` + `.rev-btn`, `.twist`, `.timer`, `.echo-card`, `.morelink`, `ol.bigq`.
4. Pick a tied lesson, confirm the file exists, write the Echo.
5. Add a card to `everyday_echoes_dashboard.html` (`.lcard` / `.lnum` / `.lbody` `.lt` `.ld` `.lg` / `.lgo`).

**Verify before reporting:** 5 panels · 0 `value=` inputs · reveals hidden by default · Echo link resolves to a real file · ≥3 phrase techniques · no untaught idiom in answers.

Fast check from `gitsite/`:
```bash
for f in rp_*.html; do
  echo "$f panels=$(grep -o 'class="panel' $f | wc -l) value=$(grep -c 'value=' $f)"
done
```
(The 4th-wall grep throws false positives on natural speech — "I **do** appreciate", "I **don't** suppose" — so read hits before trusting them.)

---

## 5. Where it's wired into the site

- `everyday_echoes_dashboard.html` — 30 cards, each showing which history it echoes.
- `short_history_dashboard.html` and `short_stories_long_shadows_dashboard.html` — each carries a teal/amber "🎭 Now go and speak it — Everyday Echoes" banner below the intro, so the link is made in both directions.
- Homepage `index.html` — an Everyday Echoes card in the "Speaking-led series" grid.

---

## 6. Deploying

```bash
cd /Users/malcolmtheteacher/Documents/01_Work/gitsite
git add <files> && git commit -m "..." && git push origin main
```
GitHub Pages rebuilds in a minute or two. The homepage is a **separate repo** — push it separately.

⚠️ The stored token can **push** but **cannot open pull requests** (403), and `gh` is not installed. Push straight to `main`; don't try to open a PR.

---

## 7. Open items

- **Quality read (offered, not yet done):** re-read all 30 lessons' comprehension answers and dialogue for the rule-5 fault — idioms or slang used but never explained. Needs a human-style read, not a grep. Malcolm decides what's a genuine problem before anything is changed.
- Lessons 31+ if the series is extended.

---

## 8. Working with Malcolm

He is an English teacher of 30 years, **not a coder**. Talk about the student-facing content in plain English; keep the tooling invisible. Don't over-engineer. When he flags a problem, **open the file and look** before theorising — and if he says you've misdiagnosed it, you probably have.
