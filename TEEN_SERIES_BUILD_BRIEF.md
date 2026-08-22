# Teen Series Build Brief — Short Stories, Long Shadows

Non-graphic ESL lesson pages built from public-domain classic stories, for
general teenage learners (about 15) at B1/B2. Six lessons, same house format
as the rest of the series.

## Model file and spec
- Clone the structure of `techniques_the_garden_party.html` (built 2026-08-22).
- Spec: `SS_HISTSTYLE_SPEC.md` (five tabs, no podcast content anywhere).
- Level tag in header: `SHORT STORIES, LONG SHADOWS · B1/B2 · 50 min`.
- No A2/B1 twin for these six: the audience is B1/B2, so one file each.
  Therefore no crosslink paragraph under the header.

## The five tabs (identical CSS/JS to the model file — change content only)
0. Key Words — intention line, 3 warm-up discussion questions, 10 words in
   3-4 DIFFERENT activity types (infer-from-context / which-word-means /
   a-b-c multiple choice / word-building + collocation), each with a Reveal
   button. Never put the definition inside the word's own context sentence.
1. The Story — abridged into 3 parts, each followed by a 2-question quick
   check with hidden answers, then one discussion question.
2. Grammar — one point, explained in .note boxes, then 3 gap-fill exercises.
   Inputs EMPTY. Answers only in hidden .answers reveals. Teaching examples
   must use different sentences from the exercises.
3. Going Deeper — a short note on the theme and why the story lasts, then
   3-4 discussion questions.
4. Speak — timer JS unchanged; Task A retell, Task B debate the story's
   dilemma, Task C a wider task with 6 safe non-personal alternatives;
   then a final-discussion block of 4 questions, the last one a from-memory
   grammar recall.

## The six lessons
| File | Story | Author, year | Grammar |
|---|---|---|---|
| techniques_the_open_window.html | The Open Window | Saki, 1914 | narrative tenses (past simple / continuous / perfect) |
| techniques_the_lumber_room.html | The Lumber Room | Saki, 1914 | -ing & -ed adjectives + intensifiers |
| techniques_the_remarkable_rocket.html | The Remarkable Rocket | Oscar Wilde, 1888 | superlatives & exaggeration |
| techniques_a_white_heron.html | A White Heron | Sarah Orne Jewett, 1886 | first & second conditional |
| techniques_after_twenty_years.html | After Twenty Years | O. Henry, 1906 | present perfect vs past simple |
| techniques_the_last_class.html | The Last Class | Alphonse Daudet, 1873 | wish & regret |

Build order: the first three are comic/gentle — do those first. The last two
carry heavier context (an arrest; a school under occupation in 1871); if
either cannot be built, substitute one of: The Devoted Friend (Wilde),
The Story-Teller (Saki), The Million Pound Bank-Note (Twain) — and say so.

Connecting thread (do not label it on the page): each story turns on a young
person deciding who they are going to be. Every lesson stands alone.

## Hard rules
- 4th wall: nothing teacher-facing on the page. No pedagogy labels, no
  "Malcolm", no teacher notes.
- Gap-fill inputs empty; answers only behind Reveal.
- No podcast / Spotify / "Listen" content anywhere.
- Age-appropriate and gender-inclusive throughout; speaking tasks always
  offer non-personal alternatives.

## Dashboard
`short_stories_long_shadows_dashboard.html` — add a DISTINCT, clearly
labelled Teens section: its own `.section-label` ("For teenage learners ·
B1/B2"), a one-line intro, and its own `.story-grid` holding the six cards,
numbered TEENS 01-06. Place it directly ABOVE the existing
"The fifty-nine stories" label. Leave the existing list, counts, banners and
design untouched.

## Build note
Write each lesson in 2-3 small chunks and assemble on disk; long single
generations of story prose have tripped API safety guardrails in bulk builds.

## Deploy
Never push. Malcolm runs (1) Update.
