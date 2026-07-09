# Lesson Remediation — up to two fixes in one pass

You are given ONE Short History lesson file. Apply the fix(es) named in your instructions. Touch ONLY the tabs specified; never change the CSS or JS.

## FIX 1 — Grammar-tab "example gives away the answer" (do this on EVERY file, base AND twin)
In the Grammar tab, the `.note` boxes hold the **model/example sentences**, and the `.gap-fill` divs hold the **exercise sentences** (with `<input>` blanks) plus a hidden `.answers` reveal.

**The bug:** an example sentence in a `.note` is reproduced — whole, or with one word blanked — as a gap-fill exercise sentence. So the student just copies the answer from the box above and the exercise tests nothing.

**The fix — rewrite the EXAMPLE, never the exercise:**
- Find every `.note` example sentence that shares its wording with a gap-fill sentence.
- Rewrite THAT EXAMPLE so it illustrates the **same grammar point** with a **different scenario/sentence** — still about this lesson's history, still natural and correct. (See `short_history_great_fire_of_london*.html` for a worked example.)
- Leave the gap-fill sentences and their `.answers` reveal EXACTLY as they are. Inputs stay empty (no `value=`).
- End state: no exercise sentence appears — in whole or blanked — anywhere in the explanation above it. Teach with one sentence, test with another.

## FIX 2 — B2/C1 vocabulary lift (BASE files ONLY — do NOT do this on an `_a2b1` twin)
Only if your instructions say this is a base file. Follow `VOCAB_LIFT_SPEC.md` on the Key Words tab: keep words already at level, lift the too-easy ones to precise/lower-frequency words that fit the story; keep §3a technique variety and the no-inline-gloss rule; sync any verbatim Listen/Speak key-word list. If every key word is already at level, make no change and say so.

## Verify before reporting
- FIX 1: by eye, confirm no example sentence is reproduced in a gap-fill. Report the before→after example sentences you rewrote (or "no giveaway found").
- FIX 2 (base only): report before→after vocab (or "already at level").
- Both: 5 `tab-content` divs; 0 inputs with `value=`; Story/Listen/Speak prose and CSS/JS untouched (except syncing a verbatim key-word list per VOCAB_LIFT_SPEC).

A detector script is re-run afterwards; it must find ZERO example/exercise overlaps.
