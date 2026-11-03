"""The IELTS Route — the single source of truth for the order of the course.

Edit here, then run:  python3 tools/build_ielts_route.py
Every `f` (file) is checked to exist when the page is built.
star=True marks a Band 7+ stretch step (core steps are for everyone).
"""

STAGES = [
 {
  "id": "s1", "num": 1, "name": "Start here", "weeks": "Week 1",
  "short": "Start",
  "blurb": "Know exactly what the test asks, and find your starting point. Everything after this is chosen from what you learn here.",
  "groups": [
   {"id": "g-start", "title": "Know the test · find your starting point", "steps": [
     {"t": "Start here: the test, the criteria and your diagnostic", "f": "ielts_start_here.html",
      "d": "How the four parts work, what the examiners score, and three timed tasks that give you a starting band for each skill."},
   ]},
  ],
 },
 {
  "id": "s2", "num": 2, "name": "Foundations", "weeks": "Weeks 1–3",
  "short": "Foundations",
  "blurb": "The habits every band depends on: what examiners count, how a paragraph works, and how the Reading and Speaking tests are built.",
  "groups": [
   {"id": "g-found-w", "title": "Writing foundations", "steps": [
     {"t": "What examiners count", "f": "ielts_lesson_2_marking_criteria.html", "d": "The four marking criteria in plain English, with weak and strong paragraphs side by side."},
     {"t": "Funnel introductions", "f": "ielts_lesson_1_academic_paragraphs.html", "d": "A three-sentence introduction that states your position clearly."},
     {"t": "Body paragraphs", "f": "ielts_lesson_3_body_paragraphs.html", "d": "The five-part paragraph: point, explanation, example, link."},
     {"t": "Sentence architecture", "f": "sentence_architecture.html", "d": "How English sentences are built — the base for every complex sentence later."},
   ]},
   {"id": "g-found-rsl", "title": "Reading, Speaking and Listening foundations", "steps": [
     {"t": "Understanding the Reading test", "f": "ielts_reading_lesson_1_test_overview.html", "d": "The question types and how the 60 minutes work."},
     {"t": "Essential reading skills", "f": "ielts_reading_lesson_2_reading_skills.html", "d": "Skimming, scanning and finding the answer in the paragraph."},
     {"t": "Speaking Part 1: your first step", "f": "ielts_speaking_part1.html", "d": "The opening questions — build confident, natural answers."},
     {"t": "Listening practice: warm-up set", "f": "listening-lessons.html", "d": "Interactive listening lessons from B1 to C1. Start with the B2 set."},
   ]},
  ],
 },
 {
  "id": "s3", "num": 3, "name": "Build the skills", "weeks": "Weeks 3–8",
  "short": "Skills",
  "blurb": "Six tracks run side by side. Each week, take the next step in two or three of them — the order inside each track matters, the order between tracks does not.",
  "groups": [
   {"id": "track-w2", "title": "Writing Task 2 — the five essay types", "steps": [
     {"t": "Opinion essays (agree / disagree)", "f": "ielts_lesson_6_opinion_essays.html", "d": "Take a clear position and keep it for the whole essay."},
     {"t": "Discussion essays (both views)", "f": "ielts_lesson_7_discussion_essays.html", "d": "Present both sides, then give your own view."},
     {"t": "Advantages and disadvantages", "f": "ielts_lesson_8_advantages_disadvantages.html", "d": "Weigh both sides and answer the exact question asked."},
     {"t": "Problem and solution", "f": "ielts_lesson_9_problem_solution.html", "d": "Causes, effects and realistic solutions."},
     {"t": "Two-part questions", "f": "ielts_lesson_10_two_part_questions.html", "d": "Answer both parts equally and recognise mixed types."},
     {"t": "Conclusions and linking", "f": "ielts_lesson_5_conclusions_linking.html", "d": "End the essay properly and link ideas smoothly."},
     {"t": "Essay practice: guided, all five types", "f": "ielts_essay_dashboard.html", "d": "A band-8 model, then your own essay paragraph by paragraph."},
   ]},
   {"id": "track-w1", "title": "Writing Task 1 — describing visuals", "steps": [
     {"t": "Task 1 overview", "f": "ielts_task_1_master_lesson.html", "d": "All the question types, the marking criteria and the structure."},
     {"t": "Line graphs", "f": "ielts_task_1_lesson_2_line_graphs.html", "d": "Describe trends and change over time."},
     {"t": "Bar charts and pie charts", "f": "ielts_task_1_lesson_3_bar_pie.html", "d": "Compare categories and describe proportions."},
     {"t": "Process diagrams and maps", "f": "ielts_task_1_lesson_4_process_maps.html", "d": "A different style of report, in the right order."},
     {"t": "Task 1 language toolkit", "f": "ielts_task1_phrase_vault_b2.html", "d": "Trends, comparisons and overviews — nine short lessons of phrases that score.", "star": True},
   ]},
   {"id": "track-sp", "title": "Speaking — Parts 1, 2 and 3", "steps": [
     {"t": "Part 1: sounding natural", "f": "ielts_speaking_part1_band7.html", "d": "Short answers that score higher: no echoing, tenses that move, the precise word."},
     {"t": "Part 1: topics in depth", "f": "ielts_speaking_part1_lesson2_topics.html", "d": "The common Part 1 topics, with ideas ready to use."},
     {"t": "Part 2: the long turn", "f": "ielts_speaking_part2.html", "d": "One minute to plan, two to talk — with cue cards and a real timer."},
     {"t": "Part 3: the discussion", "f": "ielts_speaking_part3.html", "d": "Opinions, reasons and the wider question."},
     {"t": "Speaking grammar toolkit", "f": "ielts_speaking_grammar_toolkit.html", "d": "The structures that lift a speaking score to Band 7 and above.", "star": True},
   ]},
   {"id": "track-rd", "title": "Reading — practice and training", "steps": [
     {"t": "Reading practice tests 1–3", "f": "ielts-reading-tests.html", "d": "Full tests with every question type and instant scoring. Start with tests 1 to 3."},
     {"t": "Read Your Way to Band 7", "f": "read_your_way_to_band7_dashboard.html", "d": "Reading questions built from a story, an essay and a piece of science — each carries into writing and speaking.", "star": True},
   ]},
   {"id": "track-li", "title": "Listening", "steps": [
     {"t": "Listening practice: B2 and C1 sets", "f": "listening-lessons.html", "d": "Pre-listening, vocabulary and comprehension tasks — one lesson a week keeps the ear in training."},
   ]},
   {"id": "track-lg", "title": "Language — vocabulary and accuracy", "steps": [
     {"t": "Vocabulary and collocations", "f": "ielts_lesson_11_vocabulary_collocations.html", "d": "Academic word families and the collocations examiners notice."},
     {"t": "Complex sentences", "f": "ielts_lesson_12_complex_sentences.html", "d": "Relative clauses, participles and conditionals for writing."},
     {"t": "Cohesion and coherence", "f": "ielts_lesson_13_cohesion_coherence.html", "d": "Reference words, linking and clear paragraph flow."},
     {"t": "Paraphrasing without repetition", "f": "ielts_lesson_14_paraphrasing_variety.html", "d": "Say the same thing differently — vital in every part of the test."},
     {"t": "Sentence power-ups", "f": "sentence_powerups.html", "d": "Nominalisation, inverted conditionals and cleft sentences.", "star": True},
   ]},
  ],
 },
 {
  "id": "s4", "num": 4, "name": "Under the clock", "weeks": "Weeks 8–10",
  "short": "Clock",
  "blurb": "Now everything is timed. Plan quickly, write to the clock, and keep an error log so the same mistake never costs you twice.",
  "groups": [
   {"id": "g-clock-w", "title": "Writing under time", "steps": [
     {"t": "Time management and planning", "f": "ielts_lesson_4_time_management.html", "d": "The 40-minute clock and the five-minute plan."},
     {"t": "Generating ideas under pressure", "f": "ielts_lesson_4b_generating_ideas.html", "d": "Beat the blank page when the topic is unfamiliar."},
     {"t": "Common mistakes and how to fix them", "f": "ielts_lesson_15_common_mistakes.html", "d": "Analyse your own errors and correct them."},
     {"t": "Timed essay practice 1", "f": "ielts_lesson_16_timed_practice_1.html", "d": "A complete essay in 40 minutes."},
     {"t": "Timed essay practice 2", "f": "ielts_lesson_17_timed_practice_2.html", "d": "A second timed essay, compared with the first."},
     {"t": "Exam-mode essays: all five types", "f": "ielts_essay_dashboard.html#exam", "d": "One real question, a 40-minute timer, a word counter — no frames, no help."},
   ]},
   {"id": "g-clock-rs", "title": "Reading and Speaking under time", "steps": [
     {"t": "Reading practice tests 4–7", "f": "ielts-reading-tests.html", "d": "Full 60-minute tests. Review every wrong answer."},
     {"t": "IELTS speaking simulator", "f": "tools/speaking-practice.html", "d": "A timed run through Parts 1, 2 and 3 on your own."},
   ]},
  ],
 },
 {
  "id": "s5", "num": 5, "name": "Mock and finish", "weeks": "Weeks 11–12",
  "short": "Mock",
  "blurb": "Full test conditions, then a plain look at what is still costing marks. Finish with the exam-day strategy.",
  "groups": [
   {"id": "g-mock", "title": "Mocks and last strategy", "steps": [
     {"t": "Full writing test simulation", "f": "ielts_lesson_18_exam_simulation.html", "d": "Task 1 and Task 2 together, in the real time."},
     {"t": "Reading practice tests 8–10", "f": "ielts-reading-tests.html", "d": "Three more full tests, back to back if you can."},
     {"t": "Feedback analysis and improvement plan", "f": "ielts_lesson_19_feedback_analysis.html", "d": "Find your most expensive habits and plan the last weeks."},
     {"t": "Final practice and exam strategies", "f": "ielts_lesson_20_final_strategies.html", "d": "Last-minute tips, nerves, and the day itself."},
   ]},
  ],
 },
]

# Run all the way through — not a stage
SIDE = {
 "title": "Keep these running all the way through",
 "blurb": "Ten minutes a day on any of these. They feed every stage.",
 "items": [
  {"t": "Example bank: IELTS through Stories & History", "f": "ielts_stories_history_pathway.html", "d": "True stories turned into ready Task 2 examples and Speaking material, matched to real exam questions."},
  {"t": "IELTS Word Wall", "f": "ielts_wordwall_dashboard.html", "d": "Vocabulary games across the main IELTS topic areas."},
  {"t": "IELTS Spelling Stories", "f": "ielts_spelling_stories_dashboard.html", "d": "Six short stories that teach the words candidates misspell most."},
  {"t": "The Essay Bestiary", "f": "bestiary_ielts_phrases.html", "d": "A memory system for your essay skeleton — recall it in 2 minutes."},
 ],
}

# Mind-map leaves: (stage id, label, target)  — target is a file or '#anchor'
MAP_LEAVES = {
 "s1": [("Start here: the test and your diagnostic", "ielts_start_here.html")],
 "s2": [("What examiners count", "ielts_lesson_2_marking_criteria.html"),
        ("Funnel introductions", "ielts_lesson_1_academic_paragraphs.html"),
        ("Body paragraphs", "ielts_lesson_3_body_paragraphs.html"),
        ("Reading skills", "ielts_reading_lesson_2_reading_skills.html"),
        ("Speaking Part 1", "ielts_speaking_part1.html")],
 "s3": [("Writing Task 2", "#track-w2"),
        ("Writing Task 1", "#track-w1"),
        ("Speaking", "#track-sp"),
        ("Reading", "#track-rd"),
        ("Listening", "#track-li"),
        ("Language", "#track-lg")],
 "s4": [("Time and planning", "ielts_lesson_4_time_management.html"),
        ("Timed essays", "ielts_lesson_16_timed_practice_1.html"),
        ("Exam-mode essays", "ielts_essay_dashboard.html#exam"),
        ("Reading tests 4–7", "ielts-reading-tests.html"),
        ("Speaking simulator", "tools/speaking-practice.html")],
 "s5": [("Full writing simulation", "ielts_lesson_18_exam_simulation.html"),
        ("Reading tests 8–10", "ielts-reading-tests.html"),
        ("Feedback analysis", "ielts_lesson_19_feedback_analysis.html"),
        ("Final strategies", "ielts_lesson_20_final_strategies.html")],
}
