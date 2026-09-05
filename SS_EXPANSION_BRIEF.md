# Short Stories, Long Shadows — Expansion Brief (September 2026)

You are building ONE lesson pair (B2/C1 base + A2/B1 twin) from the list below. Work in
`/Users/malcolmtheteacher/Documents/01_Work/gitsite/`. Non-graphic ESL lessons built on
public-domain classic fiction.

## 0. Read first, in this order
1. `SS_HISTSTYLE_SPEC.md` — the series spec. Every rule in it applies.
2. Template B2/C1: `techniques_there_will_come_soft_rains.html` — copy its `<style>` and `<script>` byte-for-byte; change only content.
3. Template A2/B1: `techniques_there_will_come_soft_rains_a2b1.html` — same rule.
4. Your entry below.

## 1. The text: the author's real words, abridged — never a flat paraphrase
The Story tab must contain the author's own prose, faithfully and tightly abridged into 3 parts
(B2/C1). A neutral retelling in your own words is a FAILED lesson (a past batch did this and
had to be rebuilt). Fetch the public-domain text from the source given (Project Gutenberg
plain text `https://www.gutenberg.org/cache/epub/<N>/pg<N>.txt`, Wikisource, Aozora Bunko).
Verify the fetched page is actually the story before using it.

- **Stories not originally in English** (Akutagawa, Quiroga, Lu Xun, Kafka): the originals are
  public domain but most English translations are NOT. Fetch the ORIGINAL and translate it
  yourself, faithfully, in the author's register. Do not copy a modern published translation.
  Tagore and Machado de Assis have public-domain 1916/1921 English translations — use those.
- The A2/B1 twin is a simple retelling in short sentences and common words (that is the one
  place a retelling is correct), with `<em class="dialogue">` for speech as in the template.
- Dialect (Hurston): keep the dialogue as written; narration is standard. Add one sentence in
  the Story intro saying the dialogue is written in the spoken English of 1920s Florida.
- Dark material (murder, suicide, madness, poverty): sober, never graphic.


### 1a. Keep your context SMALL — this matters
Large requests full of book text get blocked by an automated filter (a false positive, but it
kills the build). So:
- Download the source to disk with curl (e.g. `curl -sL https://www.gutenberg.org/cache/epub/43/pg43.txt -o /tmp/src.txt`),
  then locate your chapters with `grep -n` and read ONLY those lines with `sed -n 'A,Bp'`.
  Never cat a whole book or a whole template into your context.
- Read the template ONCE, in two pieces (the `<style>`+`<script>` block via sed ranges, and one
  sample tab), then write your files. Do not re-read it.
- Write each file in 2–3 appended chunks (heredocs with a quoted delimiter) rather than one giant write.
- The brief entry for your lesson is the only part of THE LIST you need — read it with grep/sed,
  not the whole file.

## 2. Files and header
- Filenames exactly as listed. `<meta name="series" content="...">` exactly as listed.
- `<title>Short Stories, Long Shadows: <Title> · B2/C1</title>` (twin `· A2/B1`).
  Novella episodes: `<title>Longer Reads: <Novella> — Episode n · B2/C1</title>`.
- Header tag `SHORT STORIES, LONG SHADOWS · B2/C1 · 50 min`; novellas
  `LONGER READS · EPISODE n OF N · B2/C1 · 50 min`. Twins say `A2/B1`.
- Crosslink line under the header exactly as the spec. Novella episodes ALSO add, on the same
  crosslink line, `← Episode n-1` / `Episode n+1 →` links to the neighbouring episode files
  (same level). Episode 1 has only "next"; the last episode only "previous".
- 50 min always. Never the word "Simplified". No byline. No names of real teachers or students.

## 3. Grammar
Use the grammar point assigned below (B2/C1) and the different, simpler one for the twin.
Three gap-fill exercises; inputs empty; the teaching examples in the `.note` boxes must use
DIFFERENT sentences from the exercise sentences; every gap has exactly one defensible answer;
with a/b/c options never let the same letter be right three times running.

## 4. Key Words (10) — see spec §3a
≥3 different techniques, labelled mini-activities, no inline gloss, matching lists scrambled
(derangement). B2/C1 words must be genuinely B2/C1; the twin's ten must be simple.

## 5. Going Deeper
No podcast, no audio, no Spotify. A short note on the theme/twist/why it endures + a `.discuss`
of 3–4 deeper questions. For the 1920s and non-Western stories, add ONE sentence of context
about the writer and their world (where, when, what they were writing against) — no lecture.

## 6. Speak
Timer JS identical. Task A retell (grammar + 5 key words); Task B opinion/debate; Task C
broader task with a "Stuck for an idea? Pick one of these and run with it:" menu of 5–6
springboards, at least half of them non-personal. Then `.final-discussion` (3–4 questions +
a from-memory grammar recall).

## 7. Novella episodes — extra rules
- The Story tab abridges ONLY the chapters listed for that episode, in 3 parts, author's prose.
- Episode 2+: Key Words tab opens with a `.note` headed **Previously…** (3–4 sentences) and
  the warm-up's first question is "Last time you predicted what would happen next. Were you right?"
- Every episode except the last: Speak Task C is **Predict** — "What happens next — and what
  would have to be true for it to happen?" with a menu of plausible directions (no spoilers).
  The last episode: Task C is the whole-book verdict (was the ending earned? who was to blame?).
- Going Deeper in the last episode looks back over the whole novella.

## 8. Verify before reporting (both files)
`grep -c 'tab-content'` = 5 (or 10 if the template counts nav+panels — match the template);
`grep -c 'value='` = 0; crosslink present; 0 occurrences of podcast/noiser/spotify/Listen;
0 occurrences of "Malcolm", "Teacher:", "TEEP", "I Do"; file ends `</html>`; open the file
and read the Story tab once through as a student would. Report filenames, size in KB,
the vocab techniques used, and one line on where the text came from.

---

## THE LIST

### Block A — Voices from further away  (series: `Short Stories, Long Shadows`)

**A1 · `techniques_the_cabuliwallah.html` + `_a2b1`** — Rabindranath Tagore, "The Cabuliwallah" (1892).
Source: the 1916 English translation in *The Hungry Stones and Other Stories* (Project Gutenberg, search the title; also on Wikisource). A Kabul fruit-seller befriends a Calcutta child; years later, released from prison, he finds her grown.
B2/C1 grammar: **past habits — used to / would / be used to**. A2/B1: **past simple with time expressions (every day, one morning, years later)**.

**A2 · `techniques_in_a_grove.html` + `_a2b1`** — Ryūnosuke Akutagawa, "In a Grove" (藪の中, 1922).
Source: Japanese original on Aozora Bunko (search 藪の中 芥川龍之介); translate it yourself. Seven testimonies about one death in a bamboo grove — a woodcutter, a priest, a policeman, an old woman, the bandit Tajōmaru, the wife, and the dead man through a medium — and they cannot all be true. (The Kurosawa film *Rashōmon* is based on it — mention in Going Deeper.)
B2/C1 grammar: **reported speech and reporting verbs (claim, admit, insist, deny, swear)**. A2/B1: **question words and forming questions (Who? Where? Why? What did he…?)**.

**A3 · `techniques_the_fortune_teller.html` + `_a2b1`** — Machado de Assis, "The Fortune-Teller" (A Cartomante, 1884).
Source: Isaac Goldberg's public-domain 1921 translation in *Brazilian Tales* (Project Gutenberg). Rita consults a fortune-teller about her lover Camillo; a letter from her husband Villela; the ending is one line.
B2/C1 grammar: **the future in the past — predictions reported (will → would, was going to, was to)**. A2/B1: **will / won't for predictions**.

**A4 · `techniques_the_feather_pillow.html` + `_a2b1`** — Horacio Quiroga, "The Feather Pillow" (El almohadón de plumas, 1907).
Source: Spanish original on Wikisource (es); translate it yourself. A young bride, Alicia, wastes away in a cold marble house; the pillow holds the answer. Handle the final image soberly.
B2/C1 grammar: **describing gradual change — comparatives of degree (weaker and weaker, the more… the less…, ever more)**. A2/B1: **adjectives for health and feelings (pale, weak, tired, afraid) with look / feel / seem**.

**A5 · `techniques_kong_yiji.html` + `_a2b1`** — Lu Xun, "Kong Yiji" (孔乙己, 1919).
Source: Chinese original on Chinese Wikisource (zh.wikisource.org, 孔乙己); translate it yourself. A failed scholar in a long gown, mocked in a Luzhen tavern, told by the boy who warms the wine; his last visit, on his hands.
B2/C1 grammar: **contrast and concession (although, even though, despite, yet, for all his…)**. A2/B1: **but / because / so — joining ideas**.

**A6 · `techniques_yuki_onna.html` + `_a2b1`** — Lafcadio Hearn, "Yuki-Onna" (1904, from *Kwaidan*).
Source: *Kwaidan* on Project Gutenberg (ebook 1210), written in English. Two woodcutters in a snowstorm; the snow woman spares the young one, Minokichi, on condition he never tells; years later, his wife O-Yuki.
B2/C1 grammar: **conditionals for promises, warnings and threats (if you ever…, should you…, unless), plus the mixed conditional looking back**. A2/B1: **past continuous for weather and background (it was snowing, the wind was blowing)**.

### Block B — The 1920s  (series: `Short Stories, Long Shadows`)

**B1 · `techniques_hands.html` + `_a2b1`** — Sherwood Anderson, "Hands" (1919, from *Winesburg, Ohio*).
Source: Project Gutenberg ebook 416. Wing Biddlebaum, his restless hands, the boy George Willard, and the town that drove him out on a misunderstanding.
B2/C1 grammar: **the passive for what is done TO a person (was driven out, had been beaten, is talked about)**. A2/B1: **adjectives of personality with very / quite / a little**.

**B2 · `techniques_winter_dreams.html` + `_a2b1`** — F. Scott Fitzgerald, "Winter Dreams" (1922).
Source: Project Gutenberg / Wikisource (published 1922, public domain). Dexter Green, a caddy at the golf club, and Judy Jones; success, and what is lost. Abridge hard — it is long.
B2/C1 grammar: **regret and hindsight — wish / if only / should have + past perfect**. A2/B1: **want to / would like to / hope to — talking about dreams and plans**.

**B3 · `techniques_kew_gardens.html` + `_a2b1`** — Virginia Woolf, "Kew Gardens" (1919).
Source: *Monday or Tuesday* (1921) on Project Gutenberg / Wikisource. A flowerbed, a snail, four pairs of people passing on a July afternoon; almost nothing happens and everything does.
B2/C1 grammar: **participle clauses for flowing description (-ing / -ed clauses, "walking past, she…")**. A2/B1: **present continuous — what people are doing right now**.

**B4 · `techniques_hills_like_white_elephants.html` + `_a2b1`** — Ernest Hemingway, "Hills Like White Elephants" (1927).
Source: Wikisource / Faded Page (Canada). Public domain in the USA (published 1927), not yet in the EU. A man and a girl at a Spanish station, the "awfully simple operation" that is never named. Handle the subject (an implied abortion) with tact; the A2/B1 twin keeps it as "an operation the man wants and the girl is not sure about".
B2/C1 grammar: **modals for pressure, persuasion and refusal (I'd rather, you don't have to, I'll…, would you please…)**. A2/B1: **questions and short answers (Do you want…? — Yes, I do / No, I don't)**.

**B5 · `techniques_sweat.html` + `_a2b1`** — Zora Neale Hurston, "Sweat" (1926).
Source: Wikisource (published in *Fire!!*, 1926; public domain in the USA). Delia the washerwoman, her husband Sykes, the snake. Keep the dialect dialogue; sober on the ending.
B2/C1 grammar: **cleft sentences for emphasis (What she wanted was…, It was Sykes who…)**. A2/B1: **have to / must for daily work and duties**.

### Block C — Longer Reads: novellas in episodes  (series: `Longer Reads`)
Files `techniques_<novella>_<n>.html` + `_a2b1`. Episode boundaries are fixed — do not move them.

**Dr Jekyll and Mr Hyde** — R. L. Stevenson, 1886. Source: Gutenberg ebook 43. Slug `jekyll_and_hyde`, 4 episodes.
- **C1 · `techniques_jekyll_and_hyde_1`** — "Story of the Door" + "Search for Mr Hyde". B2/C1: **modals of deduction about a person (must be, can't be, might have)**. A2/B1: **describing people (he is / he has / he looks)**.
- **C2 · `techniques_jekyll_and_hyde_2`** — "Dr Jekyll Was Quite at Ease" + "The Carew Murder Case" + "Incident of the Letter". B2/C1: **passive reporting (was seen, is believed to have, it was reported that)**. A2/B1: **past simple — irregular verbs in a crime story**.
- **C3 · `techniques_jekyll_and_hyde_3`** — "Remarkable Incident of Dr Lanyon" + "Incident at the Window" + "The Last Night". B2/C1: **reported speech and orders (Poole said that…, told him to…, asked whether…)**. A2/B1: **there was / there were + prepositions of place**.
- **C4 · `techniques_jekyll_and_hyde_4`** — "Dr Lanyon's Narrative" + "Henry Jekyll's Full Statement". B2/C1: **third and mixed conditionals of regret (If I had never…, I would not now…)**. A2/B1: **because / so — explaining reasons**. (Last episode: whole-book verdict.)

**The Metamorphosis** — Franz Kafka, 1915. Source: German original *Die Verwandlung* on de.wikisource.org / Gutenberg-DE; translate it yourself (do NOT copy a published translation). Slug `metamorphosis`, 3 episodes = the three parts.
- **C5 · `techniques_metamorphosis_1`** — Part I. B2/C1: **obligation and duty (had to, must, ought to, was supposed to)**. A2/B1: **can / can't — what Gregor can and can't do now**.
- **C6 · `techniques_metamorphosis_2`** — Part II. B2/C1: **how life changed — no longer / any more / used to vs now**. A2/B1: **comparatives — before and after**.
- **C7 · `techniques_metamorphosis_3`** — Part III. B2/C1: **concession and contrast (although, even so, despite, and yet)**. A2/B1: **too / enough + adjectives of feeling**. (Last episode.)

**The Time Machine** — H. G. Wells, 1895. Source: Gutenberg ebook 35. Slug `time_machine`, 4 episodes.
- **C8 · `techniques_time_machine_1`** — chapters I–III (the dinner, the model, the journey). B2/C1: **future forms and speculation (will, is bound to, might well, is going to)**. A2/B1: **will / won't — predicting the future**.
- **C9 · `techniques_time_machine_2`** — chapters IV–VI (the Eloi, Weena, the Morlocks). B2/C1: **defining and non-defining relative clauses to describe a world**. A2/B1: **there is / there are — describing a place**.
- **C10 · `techniques_time_machine_3`** — chapters VII–X (the Palace of Green Porcelain, the forest fire, Weena lost). B2/C1: **time linkers for tense narrative (as soon as, no sooner… than, until, by the time)**. A2/B1: **past simple with then / after that / finally**.
- **C11 · `techniques_time_machine_4`** — chapters XI–XII + Epilogue (the far future, the return, the disappearance). B2/C1: **hypothetical past and future in the past (would have, might have, was never to return)**. A2/B1: **past continuous vs past simple (what was happening when…)**. (Last episode.)

**The Call of the Wild** — Jack London, 1903. Source: Gutenberg ebook 215. Slug `call_of_the_wild`, 4 episodes.
- **C12 · `techniques_call_of_the_wild_1`** — chapters 1–2 ("Into the Primitive", "The Law of Club and Fang"). B2/C1: **the passive and the get-passive (was sold, got beaten, was taught)**. A2/B1: **past simple + animal and weather words**.
- **C13 · `techniques_call_of_the_wild_2`** — chapters 3–4 ("The Dominant Primordial Beast", "Who Has Won to Mastership"). B2/C1: **comparison — superlatives, "the more… the more", far/much + comparative**. A2/B1: **comparative adjectives (stronger than, faster than)**.
- **C14 · `techniques_call_of_the_wild_3`** — chapter 5 ("The Toil of Trace and Trail": Hal, Charles, Mercedes; Thornton). B2/C1: **modals of criticism and hindsight (should have, shouldn't have, ought to have, needn't have)**. A2/B1: **must / mustn't / should — rules and advice**.
- **C15 · `techniques_call_of_the_wild_4`** — chapters 6–7 ("For the Love of a Man", "The Sounding of the Call"). B2/C1: **gerunds and infinitives after verbs of feeling and habit (loved to, kept running, began to, couldn't help)**. A2/B1: **like / love / hate + -ing**. (Last episode.)

**Ethan Frome** — Edith Wharton, 1911. Source: Gutenberg ebook 4517. Slug `ethan_frome`, 4 episodes.
- **C16 · `techniques_ethan_frome_1`** — Prologue + chapters I–II (the narrator in Starkfield; Ethan, Zeena, Mattie; the walk home). B2/C1: **past perfect and past perfect continuous — what had been going on before**. A2/B1: **describing places and weather (it was cold; there was snow; the house was small)**.
- **C17 · `techniques_ethan_frome_2`** — chapters III–V (Zeena goes to Bettsbridge; the evening alone; the pickle dish). B2/C1: **preferences and wishes (would rather, would sooner, wish + past, if only)**. A2/B1: **want / would like / prefer**.
- **C18 · `techniques_ethan_frome_3`** — chapters VI–VIII (Zeena returns; the hired girl; Ethan's plan and the letter he cannot write). B2/C1: **second conditional and the unreal present (If I had the money… / If Zeena were…)**. A2/B1: **going to — plans (What is Ethan going to do?)**.
- **C19 · `techniques_ethan_frome_4`** — chapter IX + Epilogue (the sled; twenty years on). B2/C1: **distancing and piecing together (apparently, it seems, so I gathered, is said to)**. A2/B1: **past simple questions and short answers**. (Last episode; the ending is handled soberly.)
