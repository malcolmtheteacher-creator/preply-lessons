---
name: preply-lesson-factory
description: >
  HTML lesson PRODUCTION tool — takes content (PPTX, article, text, or topic+level) and outputs
  a deployable .html file in Malcolm's exact design system (purple gradient, vocab flip cards,
  answer reveals, click-to-start timers, tabbed layout) plus registers it in the Topic Explorer
  dashboard and updates the lesson count on the website.

  This is the BUILD/DEPLOY skill, not the pedagogy skill. Use english-lesson-builder for lesson
  DESIGN decisions (TEEP structure, activity selection, learning goals). Use THIS skill when
  the output is a finished .html file for the gitsite.

  TRIGGERS: "convert this PPTX to a lesson", "turn this article into a lesson", "add a lesson
  to the Topic Explorer", "build an HTML lesson", "make a batch of lessons", any mention of
  "topic_picker", "Topic Explorer", "gitsite", or "lesson count". Also trigger when the user
  provides a PPTX file path and wants it converted, or asks for a lesson to be created AND
  deployed as HTML.
---

# Preply Lesson Factory

You are building interactive HTML lessons for Malcolm's 1-to-1 Preply teaching website. Every lesson you create will be **screen-shared with a student** — the HTML IS the student experience.

## Step 1: Clarify the Input

Before creating anything, establish what you're working with:

**Ask the user (if not already clear):**
1. **Content source** — Is there a PPTX file to convert? An article URL? Pasted text? Or should you generate from a topic?
2. **Target CEFR level** — A2, B1, B2, or C1? (This affects vocabulary complexity, scaffolding, and timer duration)
3. **Category** — For the dashboard: food, travel, life, health, entertainment, work, people, or world

If converting a PPTX, extract the content using python-pptx first. If using an article URL, fetch and read it. If generating from a topic, create authentic-feeling content appropriate to the level.

## Step 2: Analyse the Content

Read the source material and identify:
- **The topic and angle** — What's the lesson about?
- **Key vocabulary** (6-10 words/phrases appropriate to the level)
- **A grammar or language focus** — What structure naturally emerges from the content?
- **Discussion potential** — What questions does this topic raise?
- **A task/scenario** — How can the student actively use this language?

For PPTX conversions: stay **faithful to the original content**. Adapt the format for 1-to-1, but do NOT change the actual material, questions, or vocabulary. The PPTX is the source of truth.

## Step 3: Structure the Tabs

Choose 4-5 tabs based on what the content supports. The tab names should be **content-descriptive** (not pedagogical labels). Common patterns:

| Tab Position | Purpose | Example Names |
|---|---|---|
| 1 | Warm-up / Hook | "Getting Started", "First Thoughts", "Opening Questions" |
| 2 | Language input | "Key Vocabulary", "Reading the Text", "Money Language" |
| 3 | Language focus | "Grammar in Action", "Persuasion Phrases", "Verb Patterns" |
| 4 | Active task | "The Meeting", "Your Presentation", "Role Play" |
| 5 | Reflection | "Discussion", "Your Thoughts", "Looking Back" |

**Do NOT use** pedagogical labels like "Lead-in", "Language Focus 1", "Task", "I Do / We Do / You Do", or TEEP phase names as tab titles.

## Step 4: Build the HTML

Read `references/design-system.md` for the exact CSS, JS, and HTML skeleton. Every lesson MUST use this design system exactly — no deviations.

### The 4th Wall Rule (Non-Negotiable)

The student has this HTML open on their screen. It must NEVER contain:
- Teacher notes or instructions ("Teacher: do X", "Malcolm: customise this")
- Pedagogical labels ("I Do", "We Do", "Retrieval", "Activate", "Demonstrate")
- TEEP phase names anywhere — not in tabs, headings, HTML comments, or data attributes
- References to "Malcolm" by name
- "Pause:" prompts — write discussion questions naturally instead
- Group/partner/classmates language — adapt everything for 1-to-1 (teacher and student)
- Mode labels ("Exploration", "Knowledge Building", etc.)

### Content Authenticity (for PPTX conversions)

When converting a PPTX, the content IS the original material. You adapt the delivery format (tabs, interactivity, 1-to-1 framing) but you do NOT:
- Invent new vocabulary that wasn't in the PPTX
- Change questions or rewrite discussion prompts
- Add content that wasn't there
- Remove content that was there (unless it's classroom logistics like "save the Zoom chat")

### Timer Rules

Timers are **click-to-start ONLY**. They must NEVER:
- Auto-start when the page loads
- Auto-start when a tab is opened
- Start via `window.addEventListener('load', ...)`
- Start via `window.onload`

The timer always requires the user to click a "Start Timer" button. Default durations: A2 = 3 min, B1 = 5 min, B2 = 5 min, C1 = 10 min.

### JavaScript String Rule

Never use single-quoted strings in JavaScript that contain apostrophes or contractions. Use double quotes: `"Time's up"`, `"don't"`, `"you're"`, `"I'd"`, `"it's"`.

## Step 5: Choose Interactive Elements

Pick from this toolkit based on what the content needs:

| Element | When to Use | Reference |
|---|---|---|
| **Vocab flip cards** | 4-10 key terms to learn | `references/design-system.md` → Vocab Cards |
| **Answer reveal buttons** | Questions with definite answers | `references/design-system.md` → Answer Buttons |
| **Reading passage** | Text-based content to analyse | `references/design-system.md` → Reading Passages |
| **Matching exercise** | Connecting words to definitions | `references/design-system.md` → Matching |
| **Discussion box** | Open-ended questions | `references/design-system.md` → Discussion Box |
| **Task checklist** | Multi-step activities | `references/design-system.md` → Task Checklist |
| **Timer** | Timed speaking/writing tasks | `references/design-system.md` → Timer |
| **Text area** | Written responses | `references/design-system.md` → Text Areas |
| **Gap-fill** | Sentence completion | Build inline with answer reveals |

## Step 5b: Practice & Application Tab Quality (Non-Negotiable)

The practice/application tab (typically tab 4 or equivalent) is where the student actually USES the language. This is the most important tab in the lesson. It must NEVER be a set of bare scenario cards with vague instructions like "How would you respond using X strategies?"

### Every practice scenario MUST include:

1. **Rich context** (3-5 sentences minimum) — not just "You disagree with your boss." Give the student a specific situation with enough detail that they can actually inhabit it: who the people are, what's at stake, what was said, why it's complicated.

2. **Specified target language** — A `speaking-time` div that names the exact expressions/strategies to use. Format: `Target: 3-4 mins | Use: "Expression 1..." + "Expression 2..."`. The student should know WHICH tools to deploy, not just "use the strategies."

3. **A selection note** at the top telling the student to pick 2-3 scenarios and how long to spend on each.

4. **A coaching note** at the bottom (in an `insight-box`) that tells the teacher what to listen for — not just "did they use the expressions" but how naturally they integrated them, whether the expressions carried real communicative weight, etc.

### The "Try It" boxes in teaching tabs must match the lesson register

If the lesson teaches professional/academic language, the "Try It" prompts must be professional/academic scenarios — NOT casual friend conversations. A lesson on diplomatic disagreement in workplace settings should not have "Try It" prompts about arguing with friends about grammar rules or healthy eating. The "Try It" scenario should feel like a natural extension of the example above it, in the same register and domain.

### Deep Dive / Extended Practice tabs must provide scaffolding

Extended practice scenarios must include:
- **Detailed situational context** (who, what, why, what makes it hard — minimum 3-4 sentences of setup)
- **Specific expressions to deploy** with guidance on WHEN in the scenario to use each one
- **Success criteria** — what "good" looks like for this scenario (1-2 sentences)
- **Integration requirements** — if the lesson builds on previous lessons, specify which earlier strategies should be combined and how

Never write a Deep Dive challenge that just says "Disagree diplomatically" or "Navigate this situation." The student needs to know what tools to reach for and what the target performance looks like.

### CSS required for practice tabs

Practice tabs using the card-grid layout need these CSS classes (check the lesson includes them):
- `.discussion-grid` — grid container for scenario cards
- `.discussion-card` — individual clickable card
- `.card-number` — numbered badge in top-right corner
- `.speaking-time` — target time and expressions footer on each card
- `.selection-note` — instruction bar above the grid

## Step 6: Register in Dashboard

After creating the HTML file, add an entry to `topic_picker.html`. Read `references/dashboard-format.md` for the exact object structure. Then update the lesson count in the website's `index.html`.

### File Naming Convention

- A2: `su_a2_[NUMBER]_[snake_case_title].html` (check existing files for next number)
- B1: `b1_[NUMBER]_[snake_case_title].html`
- B2: `b2_[NUMBER]_[snake_case_title].html`
- C1: `bc_[topic_snake_case]_c1.html`

### Duplicate Check (Critical)

Before creating ANY lesson, grep `topic_picker.html` for:
1. The proposed filename
2. The proposed title (exact and fuzzy matches)
3. Semantically similar topics

If a duplicate or near-duplicate exists, flag it and choose a different PPTX/topic.

## Step 7: Verify

After creating the lesson:
1. Check the HTML file exists and has reasonable size (15-35KB typical)
2. Grep for any auto-starting timers (`window.addEventListener.*load.*startTimer`)
3. Grep for any 4th Wall violations (teacher notes, TEEP labels, "Malcolm")
4. Verify the dashboard entry was added correctly
5. Verify the lesson count was updated
6. **Check practice tab quality** — open the "Your Turn" or equivalent tab and verify:
   - Every scenario card has rich context (3+ sentences), not just a title and one-liner
   - Every card has a `speaking-time` div specifying target expressions
   - There's a selection note and coaching note
   - "Try It" prompts match the register of the lesson (no casual friend-chat in professional lessons)

## File Locations

- **Lesson HTML files**: `/Documents/01_Work/gitsite/`
- **Topic picker dashboard**: `/Documents/01_Work/gitsite/topic_picker.html`
- **Website index**: `/Documents/01_Work/malcolmtheteacher-creator.github.io/index.html`
- **PPTX sources (if converting)**:
  - A2: `/Documents/01_Work/Assets/British Council Lessons for Conversion/BC Preply/PreIntermediate/`
  - B1: `/Documents/01_Work/Assets/British Council Lessons for Conversion/BC Preply/Intermediate/`
  - B2: `/Documents/01_Work/Assets/British Council Lessons for Conversion/BC Preply/Upper Intermediate/`
  - C1: `/Documents/01_Work/Assets/British Council Lessons for Conversion/BC Preply/Advanced/`
