# Role-Play Series — Project File

**Read this first. It is self-contained: everything needed to keep building conversation role plays, at two levels, with echoes — with paths, so nothing has to be rediscovered.**

Working directory (repo `preply-lessons`): `/Users/malcolmtheteacher/Documents/01_Work/gitsite/`
Live at `https://malcolmhyndman.com/preply-lessons/<file>.html` (the `malcolmtheteacher-creator.github.io` address just redirects there).

---

## 1. What this is

A family of **speaking lessons built as two-person conversation role plays**. Each lesson drops a learner into one real situation, teaches the exact phrases that make it work, then has them play both sides. Three series share one house style:

| Series | Prefix | What it covers | 5th tab | Levels |
|---|---|---|---|---|
| **Everyday Echoes** | `rp_NN_slug` | Everyday situations tied to a history/story lesson | 🕰️ **The Echo** (history tie) | **B2/C1 + A2/B1** |
| **Modern Life** | `ml_NN_slug` | Contemporary / digital / social life | 🔭 **The Bigger Picture** (reflection) | B2/C1 (A2/B1 not yet) |
| **English at Work** | `wk_NN_slug` | Professional / working life | 🔭 **The Bigger Picture** (reflection) | B2/C1 (A2/B1 not yet) |

**Current inventory (all built, verified, live, on the homepage):**
- **Everyday Echoes — 30 situations × 2 levels = 60 lessons.** Every `rp_NN_slug.html` (B2/C1) has an `rp_NN_slug_a2b1.html` (A2/B1) twin, cross-linked.
- **Modern Life — 6 lessons** (`ml_01`–`ml_06`): The Group Chat, The Screen-Time Talk, The Honest Review, Back in Touch, A Photo of You, The Collab.
- **English at Work — 6 lessons** (`wk_01`–`wk_06`): Speaking Up in the Meeting, Working the Room, The Presentation, The Difficult Conversation, Negotiating, The Interview.

Each series has a dashboard, a phrase bank (Modern Life & Work) and a homepage card. Everyday Echoes has a **B2/C1 ↔ A2/B1 level toggle** on its dashboard.

**What students respond to (confirmed):** the **Useful Phrases** — real, transferable chunks they carry out of the lesson and reuse. That is the heart. Protect it.

---

## 2. Where everything is

| What | Path |
|---|---|
| **B2/C1 template (Everyday Echoes)** | `rp_04_checking_into_a_hotel.html` |
| **A2/B1 template (the twin format)** | `rp_04_checking_into_a_hotel_a2b1.html` (also `rp_03_at_the_doctors_a2b1.html`) |
| **Modern Life template** | `ml_01_the_group_chat.html` |
| **English at Work template** | `wk_01_speaking_up_in_the_meeting.html` (has a 3rd-speaker `.say-c` style) |
| **B2/C1 build spec (Everyday Echoes)** | `ROLEPLAY_SPEC.md` (§5 lists all 30 situations + their history/story ties + fallbacks) |
| **A2/B1 twin build spec** | `A2B1_ROLEPLAY_SPEC.md` |
| Dashboards | `everyday_echoes_dashboard.html`, `modern_life_dashboard.html`, `english_at_work_dashboard.html` |
| Phrase banks | `modern_life_phrase_bank.html`, `english_at_work_phrase_bank.html` |
| Dashboard hero images | `modern_life_hero.png`, `english_at_work_hero.png` (Everyday Echoes has none) |
| Homepage (separate repo) | `/Users/malcolmtheteacher/Documents/01_Work/malcolmtheteacher-creator.github.io/index.html` |
| Tied history/story lessons | `short_history_*.html`, `techniques_*.html` (many have `_a2b1` twins — 136 exist) |

---

## 3. The lesson shape — five tabs

🎬 **The Scene** → 💬 **The Conversation** → 🧰 **Useful Phrases** → 🎭 **Your Turn** → (🕰️ **The Echo** *or* 🔭 **The Bigger Picture**)

Panels `id="p0"`–`p4` (one `class="panel active"`); 5 `.tab-btn` (one `.active`). The `<style>` and `<script>` are copied **verbatim** from the template — only body content changes.

- **🎬 The Scene** — vivid setup, 2 warm-up discussion questions (`ol.bigq`), a "who's who" with two `.who` cards, a closing `.tip` telling the student to watch *how*, not just *what*.
- **💬 The Conversation** — 12–16 turn model dialogue (`.say.say-a` = the other voice, `.say.say-b` = You). Then 3 **from-memory** comprehension questions with a hidden `.rev` (answers not visible before reveal, not copyable from the lines above).
- **🧰 Useful Phrases** — the **10 key phrases** (8 at A2/B1), grouped by move, each taught **guess-first**. Mix **≥3 techniques**: which-is-more-X MCQ (`.choice`) / complete-the-chunk (`___`) / reorder-the-jumble (`.jumble`) / say-it-yourself. Plus the four scaffolding blocks below.
- **🎭 Your Turn** — the `.timer` block (verbatim), Round 1 (student is role A) and Round 2 (swap), all inputs **empty** `textarea.blank` with guiding placeholders, one `.twist` card, then the `.check` self-check.
- **🕰️ The Echo** (Everyday Echoes) — history/story tie in 3–4 lines + a `.morelink` to the tied lesson + 2 bigger questions. **🔭 The Bigger Picture** (Modern Life / Work) — a reflective `.echo-card` + 2 bigger questions, no history link.

### The four scaffolding blocks (in every lesson)
1. **`.deliver`** — a "Say it like you mean it" delivery/intonation cue at the top of Useful Phrases.
2. **`.keep`** — "🔑 Make them yours": 3 cues, each with an empty `textarea.blank`, porting phrases to the student's own life.
3. **`.check`** — "Before you close the tab…": 5 student-facing success criteria after the twist.
4. **Phrase-bank `.morelink`** — links to the series phrase bank (Modern Life / Work only; Everyday Echoes has no phrase bank).

---

## 4. The two-level system (echoes at two levels)

Everyday Echoes is fully two-level; the goal is to extend this to Modern Life and Work.

- **B2/C1 = base** (`rp_NN_slug.html`). **A2/B1 = twin** (`rp_NN_slug_a2b1.html`) — same situation, simple high-frequency English: shorter dialogue, **8** survival phrases, more support (sentence-starters in the boxes), simpler twist. Full rules in `A2B1_ROLEPLAY_SPEC.md`.
- **Cross-link both ways.** The A2/B1 file has a `.levelnote` bar under the header linking up to the B2/C1 version; the B2/C1 file has a small "New to English? Try the easier A2/B1 version →" bar right after `</header>` linking down. (Exact markup is in `A2B1_ROLEPLAY_SPEC.md`.)
- **Echo at the right level.** An A2/B1 twin's Echo links to the `_a2b1` version of its history/story lesson **if that file exists** (check the folder), otherwise the base file. This keeps the whole thing inside the site's existing two-level system.
- **Dashboard toggle.** `everyday_echoes_dashboard.html` has a B2/C1 ↔ A2/B1 toggle (`setLevel()` JS) that rewrites every card's href by adding/removing `_a2b1`. Replicate this on any dashboard once its series is two-level.

---

## 5. HARD RULES — non-negotiable

1. **The 4th wall.** The student sees the HTML. No teacher notes, no pedagogy labels ("I Do", "Retrieval", TEEP phases), no reference to Malcolm, never the word "Simplified".
2. **All inputs empty.** No `value=` anywhere. Answers live only in hidden `.rev` (never add class `open`).
3. **Never give the answer away in the stimulus above it.** A phrase must never be printed before the student produces it; teaching examples must differ from exercise sentences.
4. **Exercises must actually test.** Could a student get it right without the knowledge it claims to test (copying from above, or several answers fitting)? If yes, it's broken.
5. **Never introduce anything new in an answer key.** A reveal is where a student goes to feel certain — no untaught idiom, no fresh vocabulary. *(This rule exists because "belt and braces" once appeared, untaught, in an answer. Malcolm caught it.)*
6. **Verify the tied lesson file EXISTS** before linking an Echo.

---

## 6. How to build (the workflow that works)

**One builder agent per lesson**, fanned out in parallel (this is how the 30 A2/B1 twins and the 8 new B2/C1 lessons were built). Each agent:
1. Reads the relevant **spec** (`A2B1_ROLEPLAY_SPEC.md` for twins; `ROLEPLAY_SPEC.md` for Everyday Echoes) and the **template** to clone.
2. Clones the template (CSS/JS verbatim), writes the new body.
3. For a twin: reads the B2/C1 source, simplifies, links the Echo to the `_a2b1` history twin (or base), and adds the reverse link into the B2/C1 source.
4. Self-verifies and reports the filename + the phrases.

Keep agent prompts compact by pointing them at the spec. Pre-design each lesson's scenario, two roles, and phrase-spine so the set is coherent and non-overlapping — don't let agents invent scenarios freely.

**After the agents land**, do this yourself:
- Verify all: `for f in <files>; do echo "$f panels=$(grep -o 'class="panel' $f|wc -l) value=$(grep -c 'value=' $f)"; done` (want 5 panels, 0 value=). Check Echo links resolve and reverse links were added. (The crude 4th-wall grep for "I Do"/"You Do" throws false positives on natural speech — read hits before trusting them.)
- **Wire the dashboard** (add `.lcard` cards; update the "more coming" note; if the series is going two-level, add/keep the level toggle).
- **Update the phrase bank** (Modern Life / Work): add a function-grouped section from the new lessons; update the "grows with you" note.
- **Update the homepage card** count/description (separate repo — see §7).

---

## 7. Deploying (two repos)

```bash
cd /Users/malcolmtheteacher/Documents/01_Work/gitsite
git add <files> && git commit -m "..." && git push origin main
```
GitHub Pages rebuilds in a minute or two. The **homepage is a separate repo** — push it separately:
```bash
cd /Users/malcolmtheteacher/Documents/01_Work/malcolmtheteacher-creator.github.io
git add index.html && git commit -m "..." && git push origin main
```
Homepage cards live in the **"Speaking-led series"** section (search `everyday_echoes_dashboard`). Card markup: `<a class="card" href="https://malcolmtheteacher-creator.github.io/preply-lessons/<dash>.html"><span class="lvl">…</span><span class="cnt">…</span><h4>… Title</h4><p>…</p></a>`.

⚠️ The stored token can **push** but **cannot open pull requests** (403), and `gh` is not installed. Push straight to `main`; don't try to open a PR.

To preview locally: `python3 -m http.server 8731 --directory <gitsite>` then open `http://localhost:8731/<file>.html` (the in-app browser can't open `file://`).

---

## 8. Open items / where to go next

- **Extend the two-level system to Modern Life and English at Work** — build `ml_*_a2b1.html` and `wk_*_a2b1.html` twins (following `A2B1_ROLEPLAY_SPEC.md`), cross-link, and add a level toggle to those two dashboards. *(Note: some Work topics — full negotiation, a fast meeting — are a stretch to simplify honestly; the everyday/social ones twin most naturally.)*
- **Grow Modern Life & English at Work** — each has 6; more are sketched in their dashboard "more coming" notes (working from home, the delivery gone wrong, the comparison trap; chairing a meeting, the performance review).
- **Two more series still just proposed** — *Around the World* (travel/culture) and *Social English* (small talk / the social glue).
- **Optional quality read** — re-read the original 30 Everyday Echoes for the rule-5 fault (untaught idioms in answer keys); needs a human-style read, not a grep.

---

## 9. Working with Malcolm

He is an English teacher of thirty years, **not a coder**. Talk about the student-facing content in plain English; keep the tooling invisible. Don't over-engineer. He builds bespoke lessons for real 1-to-1 students, so scenario and level matter — when a request is ambiguous (which situation? which level?), ask briefly before fanning out a big build. When he flags a problem, **open the file and look** before theorising — and if he says you've misdiagnosed it, you have. He catches real pedagogical faults automated checks miss (answers visible above the exercise, gap-fills with several right answers, untaught idioms in answers). Fix the *class* of problem, not just the instance. He loves the illustration prompts — write them richly.
