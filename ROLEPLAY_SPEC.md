# Everyday Echoes — Role-Play Lesson Build Spec

A 30-lesson speaking series: **everyday conversations as story role plays**, each tied (loosely, charmingly) to one lesson from the Short History / Short Stories library. Level: **B2/C1** — the same level as the Short History / Short Stories library these lessons tie into; one level only, no twins. Warm Mia-style look and feel; student-facing only (4th-wall clean).

## 1. Template
The prototype is `rp_01_at_the_museum.html`. Every other lesson CLONES it: copy its `<style>` and `<script>` verbatim; change only content. (The prototype itself borrows the warm palette and panel/tab structure of `a1s_03_where.html` — cream background, teal/amber accents, rounded cards — but has its own five tabs and NO spaced-repetition engine and NO images.)

## 2. The five tabs
🎬 **The Scene** → 💬 **The Conversation** → 🧰 **Useful Phrases** → 🎭 **Your Turn** → 🕰️ **The Echo**

- **Header:** tag `EVERYDAY ECHOES · ROLE PLAY · B2/C1 · 50 min`; `<meta name="series" content="Everyday Echoes">`; `h1` = the situation (e.g. "At the Museum"); one-line subtitle. Footer: `Everyday Echoes · <Title> · B2/C1`. No byline.
- **🎬 The Scene:** set the situation in 3–4 warm lines (who you are, where you are, what you need). 2 quick warm-up discussion questions. A "who's who" card for the two roles (e.g. YOU = the visitor · THE OTHER VOICE = the ticket clerk).
- **💬 The Conversation:** the model dialogue, 12–16 turns, natural, native-feeling everyday English at B2/C1 — real speech rhythms, softeners, idiomatic turns ("I don't suppose…", "to be honest…", "you wouldn't happen to…"), using `.say` speech-bubble lines labelled by role. After it: 3 from-memory comprehension questions with a hidden Reveal answers block (answers must NOT be visible on screen before Reveal, and must not be copy-able from the two lines above them).
- **🧰 Useful Phrases:** the 10 key phrases of this situation at genuine B2/C1 register — sophisticated functional language (hedging, softening, persuading, complaining firmly-but-politely, negotiating), NOT beginner survival phrases — grouped by move (e.g. *Opening · Asking · Problems · Closing*), each taught guess-first: a situation stimulus → Reveal the phrase (same reveal mechanic as the rest of the site — never print the answer in the stimulus). Mix at least 3 techniques (what would you say here? / complete the chunk / which phrase is more polite? / reorder the jumbled phrase).
- **🎭 Your Turn:** the role play itself, twice. Round 1: student plays Role A against the page's Role B prompt lines (student's lines = EMPTY `input`/`textarea` with placeholders only). Round 2: swap — student plays Role B. Then ONE twist card ("this time the tickets are sold out — what now?") for improvisation. Include the click-to-start timer JS from the history template if present in prototype.
- **🕰️ The Echo:** the loose, delightful history tie in 3–4 lines ("People have been queuing for wonders for 4,500 years…"), then a link-card to the tied lesson: `Want the full story? → <a href="short_history_x.html">`, and 2 bigger discussion questions bridging the everyday situation and the history.

## 3. HARD RULES
- 4th-wall clean: no teacher notes, no pedagogy labels, no "Malcolm". Never the word "Simplified".
- ALL inputs empty (no `value=`); every answer only in hidden reveals.
- **Never give an answer away in the stimulus/example above it** — a phrase must never be printed before the student has to produce it.
- Verify the tied lesson file EXISTS in the folder before linking; if missing, use the listed fallback.
- Everyday English, warm tone, real usable phrases — the situation is the star; the history tie is a light, witty bow on top.

## 4. Verify before reporting
5 tab panels; 0 inputs with `value=`; the Echo link resolves to a real file; reveals hidden by default; ≥3 phrase-teaching techniques. Report: filename + the 10 phrases + the Echo target.

## 5. The 30 lessons (file → situation → tied lesson [fallback])
1. rp_01_at_the_museum — Buying tickets & asking questions at a museum — short_history_tutankhamun.html
2. rp_02_ordering_at_a_cafe — Ordering, changing an order, paying — short_history_agatha_christie.html
3. rp_03_at_the_doctors — Describing symptoms, understanding advice — short_history_the_spanish_flu.html
4. rp_04_checking_into_a_hotel — Check-in, requests, a problem with the room — short_history_the_titanic.html
5. rp_05_at_the_airport — Check-in, security questions, a delay — short_history_amelia_earhart.html
6. rp_06_asking_for_directions — Lost in a new city — short_history_marco_polo.html
7. rp_07_at_the_bank — Opening an account, explaining a problem — short_history_the_medici.html
8. rp_08_buying_clothes — Sizes, trying on, returning an item — short_history_the_tudors.html
9. rp_09_making_a_complaint — Complaining politely and firmly — short_history_the_boston_tea_party.html
10. rp_10_at_the_train_station — Tickets, platforms, a missed train — short_history_the_christmas_truce.html
11. rp_11_a_job_interview — Talking about yourself, strengths, questions — short_history_the_manhattan_project.html
12. rp_12_at_the_restaurant — Booking, ordering, the bill — short_history_pompeii.html
13. rp_13_talking_about_the_weather — Small talk that opens doors — short_history_krakatoa.html
14. rp_14_at_the_pharmacy — Asking for remedies, understanding instructions — short_history_the_black_death.html
15. rp_15_renting_a_flat — Viewing, questions, negotiating — short_history_great_fire_of_london.html
16. rp_16_reporting_something_lost — At the lost property office — short_history_the_mary_celeste.html
17. rp_17_haggling_at_a_market — Prices, bargaining, walking away — short_history_the_silk_road.html
18. rp_18_joining_a_gym — Membership, goals, the tour — short_history_sparta.html
19. rp_19_planning_a_holiday — At the travel agent: wishes, budgets, choices — short_history_the_seven_wonders.html
20. rp_20_at_the_library — Joining, asking for help, finding a book — short_history_the_library_of_alexandria.html
21. rp_21_taking_a_taxi — Destinations, small talk, the fare — short_history_the_wild_west.html
22. rp_22_talking_about_sport — Opinions, agreeing & disagreeing — short_history_the_world_cup.html [fallback short_history_the_olympic_games.html]
23. rp_23_buying_tickets_for_a_show — The box office: seats, times, sold out — short_history_houdini.html
24. rp_24_a_noisy_neighbour — Raising a problem without a war — short_history_emperor_nero.html
25. rp_25_at_the_vet — A worried pet owner — techniques_rikki_tikki_tavi.html [fallback short_history_the_dancing_plague.html]
26. rp_26_a_wedding_invitation — Invitations, congratulations, polite refusals — short_history_queen_victoria.html
27. rp_27_car_trouble — At the garage: explaining what's wrong — short_history_the_wright_brothers.html
28. rp_28_at_the_hairdressers — Explaining what you want (and fixing what you got) — short_history_the_samurai.html
29. rp_29_a_leaving_party — Toasts, thanks, goodbyes — short_history_shackleton.html
30. rp_30_first_day_at_work — Introductions, asking for help, fitting in — short_history_the_terracotta_army.html
