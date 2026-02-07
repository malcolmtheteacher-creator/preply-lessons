---
name: english-lesson-builder
description: "Creates interactive HTML lessons using Malcolm's algorithmic system. Routes requests to the correct ARCHETYPE (Curious Conversations, Knowledge Building, Skills Training, or Exam Strategy) then applies MODIFIERS (level, audience, topic type). Use when creating lessons, courses, or teaching materials."
---

# Algorithmic Lesson Builder

**Formula:** PEDAGOGY ENGINE + ARCHETYPE (structure) + MODIFIER(s) (adaptations) = LESSON

**When to use:** When Malcolm asks to create/build/design any English lesson, course, or teaching material.

---

## THE PEDAGOGY ENGINE (Non-Negotiable Principles)

These principles govern ALL lesson creation across every archetype. Based on Dunlosky et al. (2013), Hattie's Visible Learning, and Rosenshine's Principles of Instruction.

### Core Rule: Student Output Ratio

**The student produces ~80% of the lesson's content.** The lesson provides scaffolding, prompts, models, and feedback — but the student does the thinking, writing, and speaking. Every tab must require active student production. If a tab is mostly reading/listening with no output task, it fails.

### The 9 Non-Negotiables

**1. RETRIEVAL FIRST (Active Recall)**
Every lesson opens with retrieval — students write/say what they already know BEFORE new input.
- Mechanism: Recalling a memory modifies and strengthens it (The Testing Effect).
- Implementation: Every lesson starts with a "What do you already know?" retrieval task. No notes, no hints. Students produce from memory first.
- Ban: Never open a lesson by simply presenting new information. The student's brain must search first.
- Tone: Retrieval prompts must use low-stakes, invitational language — "Let's see what comes to mind..." / "Have a go — don't worry about mistakes." Never test language. This creates a safe-to-fail tone without a dedicated "safe space" speech. The wording IS the safety net.

**2. LEARNING INTENTION (One Line, Not a Ceremony)**
Every lesson has a visible learning intention — but it's a single sentence, not a tab.
- Implementation: One line near the top of Tab 1, after retrieval: "Today we're working on [X] so you can [Y]."
- For returning students this may be implicit (they booked the lesson for this reason) — but the HTML lesson must still display it.
- The final retrieval tab links back to it: "We said you'd be able to [Y]. Can you?"
- This is accountability the student opted into, not a teacher monologue.

**3. SMALL CHUNKS + DUAL CODING (Rosenshine + Cognitive Load)**
New content delivered in small steps, always combining words with visuals.
- Mechanism: Brain processes visual and verbal info separately — two 'hooks' for retrieval.
- Implementation: Max 2-3 new items before a practice task. Every concept has BOTH a visual representation (diagram, timeline, icon, colour-coding) AND text. Never a wall of text.
- Rosenshine's rule: Guided Practice follows every chunk — "I do → We do → You do."

**4. ACTIVE RECALL OVER PASSIVE REVIEW**
Students must retrieve, not re-read.
- After learning items, students close/hide them and reproduce from memory.
- Click-to-reveal interactions show the PROMPT first, student attempts, THEN reveals the answer.
- Ban: No highlighting sections. No "read this again." No rereading. These are low-utility strategies that create an illusion of competence. Recognition is not knowing.

**5. INTERLEAVING (Mix Problem Types)**
Practice mixes different concepts/skills rather than blocking them.
- Mechanism: Forces students to choose the STRATEGY, not just execute. Requires diagnosis.
- Implementation: In practice tabs, shuffle question types. If teaching 3 expressions, don't group all Expression A questions together — interleave them.
- In longer lessons, switch topics/problems halfway through practice.

**6. ELABORATION (Student Explains)**
Students explain "why" and "how" out loud or in writing.
- Implementation: After practice, students explain the rule/pattern in their own words. Include "Explain why..." or "Write a 1-sentence rule for..." prompts.
- Self-explanation is more effective than teacher explanation for retention.

**7. CO-CONSTRUCTION (Guided Practice = Genuine Collaboration)**
The "We do" phase is genuinely collaborative — teacher and student construct meaning together, not teacher-demonstrates-then-student-copies.
- In 1-to-1 lessons: The teacher becomes the collaboration partner. "What do you think the pattern is?" → student hypothesises → teacher builds on it, challenges it, extends it.
- The teacher doesn't pretend not to know — but lets the student's thinking lead the direction.
- This replaces peer collaboration in group settings. The "We do" is where meaning is jointly constructed, not just transferred.

**8. FEEDBACK ON TASK & PROCESS, NOT SELF**
All feedback targets the work and the strategy, never the person.
- Correct feedback: "Your second sentence needs a time marker" / "Try elaborating on this argument" (TASK and PROCESS).
- Banned feedback: "Good boy" / "You are smart" / "Well done!" without specifics. Praise ≠ Learning.
- Algorithmically: feedback messages reference what the student DID, not who they ARE.

**9. METACOGNITION (Thinking About Thinking)**
Students reflect on HOW they learned, not just WHAT they learned.
- Implementation: The final retrieval tab includes one metacognitive question — "What helped you remember that?" / "Which practice felt most useful?" / "What would you do differently next time?"
- This is 30 seconds, not a stage. It turns retrieval from pure recall into recall + self-awareness.
- Over time, this builds students who can manage their own learning — especially important for adult learners between lessons.
- Links back to the learning intention: "We said you'd be able to [Y]. Can you? What got you there?"

### Anti-Patterns (What NOT to Do — Low Utility)

| Strategy | Why It Fails | What to Do Instead |
|----------|-------------|-------------------|
| Highlighting/Underlining | Passive, prevents connecting concepts | Retrieval practice — close the book, write what you remember |
| Rereading | Creates 'Illusion of Competence' — recognition ≠ knowing | Active recall — test yourself without looking |
| Matching teaching to 'Learning Styles' | MYTH — no evidence it improves results | Match method to CONTENT (e.g., Maps = Visual, Poetry = Verbal) |
| Teacher talks, students listen | Flips the output ratio wrong | Students produce, teacher scaffolds |
| Massed practice (cramming) | Forgetting curve destroys retention | Spaced repetition — distribute practice across time |

### The Ideal Lesson Flow (Based on "Best Study Hour")

Every lesson, regardless of archetype, follows this rhythm:

```
1. RETRIEVAL → Student writes/says what they remember (low-stakes tone, no input yet)
2. LEARNING INTENTION → One sentence: "Today: [X] so you can [Y]"
3. NEW CONTENT → Small chunks with dual coding (visual + text)
4. GUIDED PRACTICE → I do → We do (co-construct) → You do (Rosenshine)
5. ELABORATION → Student explains "why" out loud / in writing
6. INTERLEAVED PRACTICE → Mixed problem types, student produces output
7. RETRIEVAL + METACOGNITION → Recall from memory + "What helped you learn that?"
```

---

## STEP 1: ROUTE TO ARCHETYPE

```
START
│
├─ Is there a SPECIFIC GRAMMAR POINT to teach?
│   (second conditional, present perfect, modals, etc.)
│   └─ YES → KNOWLEDGE BUILDING (Archetype 2)
│
├─ Is there a SPECIFIC SKILL/FRAMEWORK to teach?
│   (interview technique, presentation structure, negotiation)
│   └─ YES → Is it for a SPECIFIC EXAM?
│            ├─ YES → EXAM STRATEGY (Archetype 4)
│            └─ NO → SKILLS TRAINING (Archetype 3)
│
└─ DEFAULT → CURIOUS CONVERSATIONS (Archetype 1)
            (content-driven fluency, interesting topics)
```

---

## STEP 2: SELECT MODIFIERS

| Modifier | Options | Effect |
|----------|---------|--------|
| **Level** | A1, A2, B1, B2, C1, C2 | Scaffolding, vocabulary complexity |
| **Audience** | Teen, Professional, General, Young Learner | Tone, topics, components |
| **Topic Type** | Current Events, Evergreen, Academic | Theme, urgency, aesthetic |
| **Language Focus** | Grammar, Expressions, Vocabulary, Pronunciation | Card content, MFP balance |
| **Delivery** | 1-to-1 Online, Group Class | Interaction model, pacing, collaboration style |

### +1-to-1 Online Modifier (Preply / Individual Lessons)

When applied, this modifier adjusts interaction patterns across ALL archetypes:

- **"We do" = Teacher-student co-construction.** No peer work available. The teacher is the collaboration partner — asking genuine questions, building on the student's hypotheses, not just validating. "What do you think the pattern is?" replaces "Discuss with your partner."
- **Student speaks output rather than writing it.** Most retrieval and elaboration tasks become spoken. Text input fields in the HTML become prompts the teacher asks verbally, with the student responding out loud. Writing tasks are reserved for where writing IS the skill (e.g., exam writing practice).
- **Teacher controls reveal pacing.** Click-to-reveal in the HTML is controlled by the teacher (screen-sharing) or the student has the link open and interacts directly. Either way, the teacher manages the pace — revealing only after the student has attempted.
- **Timer default: optional.** For most adult 1-to-1 students, the natural pace of conversation is the timer. BUT this is OVERRIDDEN by +ADHD modifier — see below. When +ADHD is active, timers are mandatory on every activity.
- **Metacognition becomes a steering wheel.** "What felt most useful today?" directly informs the next lesson. In 1-to-1 there's no fixed curriculum — the student's metacognitive feedback shapes the course.
- **Retrieval tone is especially important.** With no group to hide in, retrieval can feel exposing. Use invitational language: "Let's see what comes to mind" not "What do you remember?" The wording is the safety net.

### +Teen +ADHD / Low Attention Span Modifier

When applied (any student described as having ADHD, low attention span, difficulty concentrating), this modifier OVERRIDES the default layout. Study the dinosaur heist lesson in the gitsite folder as the gold standard.

**INTERACTION MODEL:**
- **Student has the HTML open on THEIR screen and shares it.** The student interacts directly — typing, clicking, solving. The teacher guides and observes via the student's screen-share. This is NOT a teacher-controlled presentation.
- **The lesson IS a game.** Not a lesson with game elements bolted on. The student should never feel like they're doing a "lesson" — they're playing a game that happens to teach English.

**GAME MECHANICS (all mandatory):**
- **Phases, not tabs.** Sequential phases that lock/unlock. Can't skip ahead. Completing a phase unlocks the next with a dramatic transition.
- **REAL timers on EVERY activity.** Countdown timers that actually tick, change colour (teal → yellow <30s → red <10s + pulse), and trigger consequences when they hit zero (auto-submit, lost points, failure state). No decorative timer labels. If it says "90 seconds" there must be 90 seconds counting down.
- **Points system with visible running score.** Sticky header showing score, phase progress. Points awarded for: words written (per-word scoring), target language used (keyword detection), speed bonuses, puzzle completion. Points animate when awarded.
- **REAL puzzles.** Ciphers, logic riddles, pattern recognition, word puzzles — genuine challenges that require thinking, not trivial A/B multiple choice. Match the difficulty to the student's level.
- **Keyword detection.** Scan student text inputs for target language keywords. Award bonus points automatically. Give specific inline feedback about what was detected vs missed.
- **Failure states with consequences.** Running out of time, too few words, missing target language — all trigger real consequences (lost points, "security alert", restart phase). Stakes make the game matter.
- **Achievement badges.** Track conditions throughout and reveal at end.
- **Maximum 30 seconds between interactions.** Something must be clickable, typeable, or solvable at all times. Walls of text are banned. Every piece of content is immediately followed by a student action.
- **No "fastest wins" or competitive language.** It's a single player game. The student competes against the clock and their own score, not imaginary opponents.
- **Phase transitions are dramatic.** Brief animation/message between phases.

**PEDAGOGY IS INVISIBLE:** All 9 non-negotiables still apply but hidden inside the game:
- Retrieval = entrance exam / security clearance test
- New content = classified briefing / intel files (short, visual, one at a time)
- Guided practice = training exercises with real consequences
- Interleaving = mixed challenge types within phases
- Elaboration = mission reports / interrogation responses
- Retrieval + metacognition = final debrief / graduation

---

## STEP 3: BUILD WITH ARCHETYPE FRAMEWORK

All archetypes MUST embed the 6 Non-Negotiables from the Pedagogy Engine. The structures below show WHERE each principle appears.

---

# ARCHETYPE 1: CURIOUS CONVERSATIONS

> **Use when:** Fluency through engaging content (DEFAULT for most requests)
> **Examples:** Polite Lies, Phone Addiction, Cancel Culture, Boredom, Enhanced Games

### Structure: 6 Tabs

| Tab | Name | Purpose | Pedagogy Principle |
|-----|------|---------|-------------------|
| 1 | Retrieval + Hook | Student recalls → THEN fascinating content | RETRIEVAL FIRST |
| 2 | Language Focus A | 2-3 items: visual + text, I do → You do | DUAL CODING + SMALL CHUNKS |
| 3 | Language Focus B | 2-3 items: same pattern, interleaved recall | INTERLEAVING |
| 4 | Your Turn | 6 discussion cards — student produces 80%+ | STUDENT OUTPUT |
| 5 | Deep Dive | Timed speaking + elaboration challenge | ELABORATION |
| 6 | Retrieval Wrap-Up | Student reproduces key items from memory | RETRIEVAL AGAIN |

### Requirements

**Tab 1 - Retrieval + Hook:**
- OPENS with retrieval: "Before we begin — write down 3 things you already know about [topic]" or "What vocabulary do you already know for [topic]?" — NO NOTES, from memory only
- THEN: Fascinating question OR surprising statistic
- 3-5 real statistics with sources
- 2-3 named people's stories (not generic)
- NO trauma disclosure required
- Creates need for the language in Tabs 2-3
- Dual coding: stats presented visually (icons, charts, infographics) not just as text

**Tabs 2-3 - Language Focus:**
- EXACTLY 5 items total (expressions, grammar, vocab — whatever the focus is)
- Presented in small chunks: max 2-3 per tab
- Each item uses DUAL CODING: visual representation (icon, colour, diagram) + text
- Guided practice sequence per item: Model example → Guided prompt → "NOW YOU TRY" (student produces a sentence without looking at the model)
- Click-to-reveal shows the PROMPT first. Student attempts. THEN reveals model answer
- After all items in a tab: quick interleaved recall — "Cover the items above. Which expression means [X]?" (retrieval, not rereading)
- Each item has: Meaning, Form, Pronunciation/Register notes
- All items MUST appear in Tab 4 discussions

**Tab 4 - Your Turn:**
- 6 discussion topic cards
- Student selects 2-3 (choice = ownership)
- 80% student speaking/writing time — teacher facilitates only
- Cards require students to USE the target language (not just discuss freely)
- Include elaboration prompt: "Explain WHY you chose that expression"

**Tab 5 - Deep Dive:**
- Working timer (3 or 5 minutes)
- 3-4 challenge options — student chooses
- Includes elaboration: student must explain their reasoning, not just answer
- Timer colours: blue → yellow (<30s) → red (<10s)

**Tab 6 - Retrieval Wrap-Up + Metacognition:**
- NOT a teacher-led summary. Student reproduces from memory
- "Cover everything. Write down the 5 items we learned and one example sentence for each"
- Then reveal to self-check (retrieval + feedback on task)
- Feedback is process-focused: "Check — did you remember the correct form?" not "Well done!"
- Metacognitive close (one question): "What helped you remember these?" or "Which activity was most useful for you today?"
- Links back to learning intention: "We said you'd be able to [Y]. Can you?"

### Modifier Effects

**+Teen:** Add expression tracker, critical thinking scaffolds, teacher notes section
**+Current Events:** Light background with bold red/black accents for urgency, date stamp, "Breaking News" feel
**+Professional:** Workplace context, formal register focus

### Quality Gate
> "Would students lose track of time because the content is too interesting AND are they producing 80% of the output?"

---

# ARCHETYPE 2: KNOWLEDGE BUILDING

> **Use when:** Teaching specific grammar point, vocabulary set, or language system
> **Examples:** Second Conditional, Present Continuous, Present Perfect vs Past Simple

### Structure: 7 Tabs

| Tab | Name | Purpose | Pedagogy Principle |
|-----|------|---------|-------------------|
| 1 | Retrieval + Context | What do you already know? → Then: why this matters | RETRIEVAL FIRST |
| 2 | Form Focus | Small-chunk presentation with dual coding | DUAL CODING + SMALL CHUNKS |
| 3 | Guided Practice | I do → We do → You do, controlled exercises | ROSENSHINE |
| 4 | Interleaved Practice | Mixed exercises shuffling this + previous knowledge | INTERLEAVING |
| 5 | Elaboration | Student explains the rule in own words + produces | ELABORATION |
| 6 | Speaking/Production | Real communication task — student output only | STUDENT OUTPUT |
| 7 | Retrieval Test | Final recall — no notes, reproduce the rule + examples | RETRIEVAL AGAIN |

### Requirements

**Tab 1 - Retrieval + Context:**
- OPENS with retrieval: "Write 3 sentences using [target structure] — don't worry about mistakes" or "What do you already know about [grammar point]?"
- THEN: Real situation where this language is needed
- Comparison (e.g., Present Simple vs Continuous) using DUAL CODING: timeline, table, or diagram — not just text
- Clear rule statement — explicit teaching (Direct Instruction: state the learning intention and success criteria clearly)

**Tab 2 - Form Focus:**
- Table showing all forms (I am, You are, He is...)
- Dual coding: colour-coded forms, visual timeline, diagram alongside text
- Small chunks: present ONE form pattern, practice it, then next
- Spelling rules if applicable
- Multiple examples in context
- Success criteria displayed: "By the end, you will be able to [specific outcome]"

**Tab 3 - Guided Practice (Rosenshine's I Do → We Do → You Do):**
- I DO: Teacher model — one completed example with think-aloud annotations
- WE DO: Partially completed example — student fills in the key parts
- YOU DO: Student produces full answers independently
- Gap-fill, matching, multiple choice — with immediate feedback on TASK ("The verb needs past participle form") not on SELF
- Designed for 80%+ success rate

**Tab 4 - Interleaved Practice:**
- Exercises that MIX the target structure with previously learned structures
- E.g., if teaching Present Perfect, include some Past Simple questions — student must DIAGNOSE which to use
- This forces strategy selection, not just execution
- Shuffled order — never group all same-type questions together

**Tab 5 - Elaboration:**
- Student explains the grammar rule in their own words (written or spoken)
- "Write a 2-sentence explanation of when to use [structure] as if explaining to a friend"
- Student creates their OWN example sentences (not from a model — original)
- Student identifies the PATTERN — "What do all correct examples have in common?"

**Tab 6 - Speaking/Production:**
- Real communication task — student produces freely using the target language
- Timer for extended speaking (optional)
- 90% student output — teacher only prompts/redirects
- No scaffolding visible — student must recall and apply independently

**Tab 7 - Retrieval Test + Metacognition:**
- Student writes the rule from memory (no looking back)
- Student produces 3 original example sentences from memory
- Self-check: reveal correct rule and compare
- Feedback: "Did you include [specific feature]?" — task-focused, not praise
- Metacognitive close: "What helped you remember the rule?" / "What would you do differently next lesson?"
- Links back to learning intention: "We said you'd be able to [Y]. Can you?"

### Modifier Effects

**+A1/A2:** Heavy scaffolding in Tabs 2-3 (sentence builders, listen buttons, emojis, colourful design), but Tabs 5-7 still require student output. Retrieval tasks simplified: "Write 2 words you know about..."
**+B1/B2:** Game mechanics in Tab 4, more complex interleaving, less scaffolding
**+C1/C2:** Nuance focus, academic register, minimal scaffolding, elaborate interleaving with multiple structures

### Quality Gate
> "Can the student PRODUCE the rule and examples from memory without notes? Are they choosing strategies, not just executing?"

---

# ARCHETYPE 3: SKILLS TRAINING

> **Use when:** Teaching performance skill with named framework
> **Examples:** Interview Prep (PARADE), Presentation Skills, Negotiation

### Structure: 7 Tabs

| Tab | Name | Purpose | Pedagogy Principle |
|-----|------|---------|-------------------|
| 1 | Retrieval + Framework | What do you already do? → Then: the framework | RETRIEVAL FIRST |
| 2 | Deep Dive | Component-by-component with dual coding | DUAL CODING + SMALL CHUNKS |
| 3 | Examples | Model answers — student analyses (not just reads) | ELABORATION |
| 4 | Guided Practice | Scaffolded I do → We do → You do | ROSENSHINE |
| 5 | Interleaved Practice | Mixed scenarios requiring strategy selection | INTERLEAVING |
| 6 | Application | Real scenario, no scaffolding, full student output | STUDENT OUTPUT |
| 7 | Retrieval Debrief | Reproduce the framework from memory + self-assess | RETRIEVAL AGAIN |

### Requirements

**Tab 1 - Retrieval + Framework:**
- OPENS with retrieval: "Think of a time you [used this skill]. What did you do? What went well/badly?" — student produces first
- THEN: Name framework clearly (PARADE, STAR, 3-30-3)
- Visual representation using dual coding (grid, flowchart, acronym + icons/colour)
- "Why this works" rationale
- Explicit success criteria: "A strong [skill output] will include [specific criteria]"

**Tab 2 - Deep Dive:**
- Each component explained in small chunks — one at a time
- Dual coding: visual for each component + text explanation
- After EACH component: student immediately tries it ("Write your version of [component] now")
- Good vs weak examples for each component (student identifies which is which — active, not passive reading)

**Tab 3 - Examples:**
- Complete model answers — but student ANALYSES them, not just reads
- "Read this model. Identify where each part of [FRAMEWORK] appears"
- Student annotates/labels the model (active task)
- "What makes this Band 8 instead of Band 6?" — student explains (elaboration)

**Tab 4 - Guided Practice (Rosenshine):**
- I DO: One complete worked example with think-aloud
- WE DO: Student completes a partial response with prompts
- YOU DO: Student produces a full response with framework visible
- Feedback on PROCESS: "Your [component] could be stronger — try adding [specific technique]"

**Tab 5 - Interleaved Practice:**
- Multiple different scenarios requiring the SAME framework but different content
- Vary the difficulty and context — student must adapt the strategy, not repeat the same answer
- Include a scenario where the framework must be modified or where two approaches could work — forces diagnosis

**Tab 6 - Application:**
- Real scenario, realistic pressure
- Timer for realistic time constraints
- NO scaffolding visible — student must recall framework from memory
- 100% student output

**Tab 7 - Retrieval Debrief + Metacognition:**
- "Draw/write the framework from memory"
- Student self-assesses their Tab 6 performance against the criteria
- Process feedback: "What strategy did you use? What would you change?"
- NOT teacher praise — student reflection
- Metacognitive close: "Which part of practice helped most?" / "What will you focus on between now and next lesson?"
- Links back to learning intention: "We said you'd be able to [Y]. Can you?"

### Language Integration
Strategic language is EMBEDDED in the skill (not separate expression cards):
- "Phrases for buying time"
- "Language for structuring answers"
- Always paired with visual cue (icon, colour-code) — dual coding

### Quality Gate
> "Could the student reproduce the framework AND apply it in a new situation from memory tomorrow?"

---

# ARCHETYPE 4: EXAM STRATEGY

> **Use when:** Teaching how to beat a specific test format
> **Examples:** IELTS Task 1, IELTS Speaking Part 2, Cambridge exams

### Structure: 7 Tabs

| Tab | Name | Purpose | Pedagogy Principle |
|-----|------|---------|-------------------|
| 1 | Retrieval + Real Challenge | What do you know about this exam? → Then: problem framing | RETRIEVAL FIRST |
| 2-5 | Decision 1-4 | One strategic decision per tab + interleaved practice | SMALL CHUNKS + INTERLEAVING |
| 6 | Full Practice | Apply ALL decisions — 100% student output | STUDENT OUTPUT |
| 7 | Retrieval Debrief | Reproduce decisions from memory + self-assess | RETRIEVAL AGAIN |

### Requirements

**Tab 1 - Retrieval + Real Challenge:**
- OPENS with retrieval: "Write down everything you know about how [exam section] is scored" or "What strategies do you already use for [exam task]?"
- THEN: What examiners actually look for
- Band 6 vs Band 8 comparison (same data, different approach) — dual coding: side-by-side visual, colour-coded differences
- "The difference is HOW you think"
- Explicit success criteria: "To score Band [X], you need to [specific behaviours]"

**Decision Tabs (2-5):**
- One clear decision per tab — small chunk
- Dual coding: each decision has a visual representation (flowchart, icon, colour) + text
- Guided practice sequence: Model → Guided attempt → Independent attempt (Rosenshine)
- Embedded "Activity: Select/Fix" practice — student produces, not just reads
- "See Analysis" reveal for answers — but student ATTEMPTS FIRST (retrieval before reveal)
- Interleaving: Decision 3-4 tabs include questions requiring Decisions 1-2 as well — mix, don't block
- Elaboration: "Explain in your own words WHY this decision matters for the score"

**Tab 6 - Full Practice:**
- Real exam task under realistic conditions
- Step-by-step application — but the student drives each step
- Timer for realistic pressure
- 100% student output — no scaffolding
- Self-assessment checklist (student checks their OWN work against criteria)
- Model answer revealed AFTER student attempt for comparison (not before)

**Tab 7 - Retrieval Debrief + Metacognition:**
- "Write down all [4] decisions from memory without looking back"
- Self-check: reveal decisions and compare
- Student analyses their own Tab 6 output: "Which decisions did I apply? Which did I miss?"
- Process feedback: "What will you do differently next time?" — not "Good job!"
- Metacognitive close: "Which decision was hardest to apply? Why?" / "What practice helped most today?"
- Links back to learning intention: "We said you'd be able to [Y]. Can you?"

### Quality Gate
> "Can the student list ALL strategic decisions from memory AND identify where they applied/missed them in their own work?"

---

## TECHNICAL STANDARDS (All Archetypes)

### Output Location
ALL completed lesson HTML files MUST be saved to Malcolm's gitsite folder:
`Documents/01_Work/gitsite/`
This is the lesson repository. No lessons should be saved to Documents root, Downloads, or anywhere else.

### Colours
ALL lessons use LIGHT backgrounds with dark text for readability. Dark themes are banned — they cause reading difficulty, especially on screens shared in online lessons.
- Default: White/light grey background (`#f8f9fa`), dark text (`#1a1a2e`), purple accent (`#667eea`)
- Professional: Light background, blue accent (`#4a90e2`)
- A1/A2: Light background, warm pink/coral accents for energy
- Teen: Light background, bold accent colours for engagement (red `#e94560`, teal `#4ecdc4`) — but NEVER dark backgrounds
- Ban: No dark mode themes. No dark backgrounds with light text. No low-contrast colour combinations.

### Timer Requirements
- Default: 3 minutes (180 seconds)
- Options: 3 min, 5 min, reset
- Colours: teal → yellow (<30s) → red (<10s) + pulse animation
- Ban: NEVER display a timer label (e.g., "90-SECOND CHALLENGE") without a WORKING countdown. Every timer must be functional — counting down, changing colour, and triggering consequences (auto-submit, lost points) when it hits zero. Decorative timers that don't actually count down are banned.
- For +ADHD: timers auto-start when the student clicks into the text area. No "start" button needed.

### Mobile Responsive
- Breakpoint: 768px
- Stack cards vertically on mobile

### Feedback Display
- Ban: NEVER use `alert()` pop-ups for feedback. Pop-ups are invisible to students when the teacher is screen-sharing.
- ALL feedback must appear INLINE on the page — styled divs that appear below the interaction.
- Correct feedback: light green background, teal border.
- Incorrect feedback: light red background, red border.
- Both use dark text for readability.

### Interaction Patterns for Retrieval
- Click-to-reveal: Always show PROMPT first → student attempts → click to reveal answer
- Hide/Show toggles: Let students cover content for self-testing
- Text input fields: Where students type their attempts before seeing models
- Timer-gated reveals: Content appears only after student has had time to attempt

### Feedback Message Standards
- Always reference the TASK or PROCESS: "Your sentence needs a time reference" / "Try using the framework's second step"
- Never reference the SELF: No "Good boy", "Well done!", "You're smart", "Great job!" without specifics
- If positive: tie to specific action: "Your use of [specific feature] strengthens the argument because [reason]"

---

## QUICK REFERENCE

| Request Contains... | Archetype |
|--------------------|-------------|
| Grammar point (conditional, tense, modal) | KNOWLEDGE BUILDING |
| Framework name (PARADE, STAR) | SKILLS TRAINING |
| Exam name (IELTS, Cambridge) | EXAM STRATEGY |
| Interesting topic, speaking practice, fluency | CURIOUS CONVERSATIONS |

Then apply modifiers: Level? Audience? Topic type? Language focus?

### Pedagogy Checklist (Every Lesson Must Pass)

- [ ] Opens with RETRIEVAL in low-stakes, invitational language?
- [ ] Learning intention visible (one sentence, not a tab)?
- [ ] New content in SMALL CHUNKS with DUAL CODING (visual + text)?
- [ ] Guided practice follows I DO → WE DO (co-construct) → YOU DO?
- [ ] Practice is INTERLEAVED (mixed types, not blocked)?
- [ ] Student EXPLAINS in own words (elaboration)?
- [ ] Ends with RETRIEVAL + one METACOGNITIVE question?
- [ ] Student output ratio ≥ 80%?
- [ ] Feedback targets TASK/PROCESS, not SELF?
- [ ] NO highlighting, rereading, or learning styles assumptions?
- [ ] If +1-to-1 Online: spoken output prioritised, teacher co-constructs in "We do"?

---

## FAILURE HISTORY (Do Not Repeat)

### Version 2.0 Failures (Abstract/Pedagogical)
- 12 expressions (cognitive overload)
- Abstract meta-linguistic topics ("Managing Conversations")
- Perfect pedagogy, zero engagement

### Version 3.0 Failures (Heavy/Traumatic)
- Heavy themes (AI fear, failure, trauma)
- Forced trauma disclosure
- Students left drained, not energized

### Version 4.0 Failures (Passive Students)
- Too much teacher-provided content, not enough student production
- Rereading/highlighting disguised as "activities"
- Summary tabs where teacher tells students what they learned (instead of students recalling)
- Feedback that praised the student ("Great job!") instead of addressing the work
- Blocked practice (all same-type questions grouped together) — no strategy selection required

### Universal Failures
- Western-centric content
- Textbook scenarios without real-world anchor
- No "Now You Try" prompts
- No student choice
- Matching teaching to "learning styles" (debunked — match method to CONTENT instead)

---

## VERSION HISTORY

- v1.0-3.0: Single Curious Conversations template (limited)
- v4.0: Algorithmic system with 4 archetypes + modifiers
- v5.0: Pedagogy Engine integration — retrieval practice, interleaving, dual coding, elaboration, Rosenshine's principles, evidence-based feedback. Student output ratio ≥ 80%. Based on Dunlosky et al. (2013), Hattie's Visible Learning, Rosenshine's Principles of Instruction.
- v5.1: TEEP integration (light-touch) — learning intention as one-liner not a tab, safe-to-fail tone embedded in retrieval wording, co-construction in "We do" phase, metacognitive close in all wrap-up tabs. Added +1-to-1 Online modifier for Preply/individual lessons. 9 Non-Negotiables (up from 6).
- Date: February 2026
