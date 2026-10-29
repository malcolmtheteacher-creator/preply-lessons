# Where things live (read first)

- **"My website" / "the homepage"** = `~/Documents/01_Work/malcolmtheteacher-creator.github.io/index.html` (a separate repo, served at malcolmhyndman.com). Edit and push THAT repo for any homepage request.
- `malcolm_lesson_index.html` in this folder is only the searchable lesson index. It is not the website. Only change it if asked for "the lesson index".
- This folder is the `preply-lessons` repo: lessons, dashboards and `wordbank/`.

# Word Bank (My Words) — required for every new lesson

Students review lesson vocabulary in `wordbank/index.html`. Lessons feed it automatically, but only if they follow this.

**When building any lesson that teaches vocabulary:**

1. Write each target word in the lesson's Key Words / vocabulary section as
   `<div class="meaning"><b>word</b> (pos) — short definition. Example: "A sentence using it."</div>`
   (or the existing card style: `<div class="vocab-card">` containing `.word`, `.pos`, `.def`, `.ex` divs — both are read).
   - Base form only: `generalise`, not `to generalise` or `(a) generalise`; no `a`/`an`/`the` before nouns.
   - Include a definition that does not contain the word itself, and an example sentence where possible.
   - Keep to the target words (aim for 6–12), not every word in the text.
2. Save the lesson as a top-level `*.html` file in this folder (not a subfolder).
3. After saving, run:
   ```
   python3 tools/build_wordbank.py --auto --inject
   ```
   This (re)builds `wordbank/words.js` and `wordbank/lessons.js` and adds the bottom bar (`<script src="wordbank/hook.js">`) to every lesson that has registered words. It is safe to run repeatedly.
4. Commit `wordbank/words.js`, `wordbank/lessons.js` and the lesson together, so the live bar and word list stay in step.

The bar is student-facing and contains no teacher notes, so it respects the 4th wall rule. Do not add teacher guidance to the lesson HTML to explain it.

Dashboards that link to registered lessons get an "Open My Words" bar from the same command. Lessons with fewer than 3 registered words, dashboards, and files named `* (1).html` are skipped.
