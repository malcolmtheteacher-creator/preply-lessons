# Everyday Echoes — Conversation Families

Most everyday conversations follow one of six shapes. Each roleplay belongs to one family, so the toolkit, shape strip and Your Turn scenes can be planned once per family and reused. The shape is a **map, not a script**: real conversations skip steps, repeat them and branch. Students see it as "the shape of this conversation" on the Useful Phrases tab.

**Piloted so far:** `rp_09` (family 2) and `rp_02` (family 1). Everything below the pilots is proposed and not built.

## The six families

| # | Family | Typical moves |
|---|---|---|
| 1 | **Getting a service** | Order lightly → ask for a steer → make it yours → change your mind → flag a mix-up → pay and close |
| 2 | **Fixing a problem** | Open gently → take them off the hook → say what's wrong → push, politely → ask for what you want → make a deal and close |
| 3 | **Getting information or help** | Get attention → ask → check you understood → clarify → say what you'll do next → thank |
| 4 | **Being questioned or consulted** | Answer → add a detail → ask a question back → check the advice or next step → close |
| 5 | **Negotiating** | Ask → give a reason → offer → counter → compromise → agree |
| 6 | **Social talk** | Open → find a shared topic → add something and ask something → react → exit gracefully |

Every lesson also teaches the same **repair set** (in `tools/roleplay_live/configs.py`, `REPAIR`): "Sorry, I didn't quite catch that…", "Do you mean…?", "Just so I've got this right, you're saying…", "Could you go a bit slower?", "Give me a second to think.", "How do you say that in English?". These work in every conversation and were missing from most lessons.

## Mapping (40 lessons)

**1 · Getting a service (13):** rp_01 museum · rp_02 café · rp_04 hotel check-in · rp_05 airport · rp_07 bank · rp_08 clothes · rp_12 restaurant · rp_18 gym · rp_21 taxi · rp_23 show tickets · rp_28 hairdresser · rp_31 post office · rp_33 car hire

**2 · Fixing a problem (4):** rp_09 complaint · rp_16 lost property · rp_24 noisy neighbour · rp_27 car trouble

**3 · Getting information or help (6):** rp_06 directions · rp_10 train station · rp_20 library · rp_34 town hall · rp_37 consulate · rp_38 school office

**4 · Being questioned or consulted (8):** rp_03 doctor · rp_11 job interview · rp_14 pharmacy · rp_25 vet · rp_32 passport control · rp_36 giving a statement · rp_39 optician · rp_40 ticket inspector

**5 · Negotiating (4):** rp_15 renting a flat · rp_17 market haggling · rp_19 planning a holiday · rp_35 house viewing

**6 · Social talk (5):** rp_13 weather · rp_22 sport · rp_26 wedding invitation · rp_29 leaving party · rp_30 first day at work

Some lessons straddle two families (hotel check-in also has a "fix a problem" half; ticket inspector can turn into a problem). They sit under the family of their main shape. Check the mapping lesson by lesson when building.

## How a lesson is built now

Tab order: **Scene → Useful Phrases → Conversation → Your Turn → Echo**. Students meet the phrases first, then see them in the dialogue.

- **Useful Phrases:** the shape strip, then an open toolkit (2–3 ways to say each move), then the other person's phrases, "when something changes" phrases, and the repair set. A speed round of situation cards follows, with a "Cover the toolkit" button for later self-testing.
- **Your Turn:** a spoken warm-up, a role card with a goal and a limit, a card for the other person, a timer, a twist deck, swap seats, an afterwards tick-list, and a "go again, harder" step. A separate teacher sheet lives in `teacher/<lesson file>`.
- **No printed answer rule:** the old spec forbade printing a phrase before the student has to produce it. That rule is lifted for the toolkit, because students could not recall phrases they had just read. Retrieval practice now comes after exposure, through the speed round with the toolkit covered.

## Building a lesson

1. Add an entry to `tools/roleplay_live/configs.py` (copy `rp_09` or `rp_02`).
2. Run `python3 tools/roleplay_live/build.py rp_NN`.
3. It rewrites the Useful Phrases and Your Turn panels, reorders the tabs, injects the CSS and JS once (between `RPLIVE` markers, so re-running is safe), and writes the teacher sheet.
4. The Scene, Conversation and Echo panels are never touched.

## Known issues

- The original series template defined timer JavaScript but had no timer on the page. The rebuilt Your Turn panel includes one. `rp_02` had the same gap, so the other lessons built from that template probably do too (not checked one by one).
- A2/B1 twins (`*_a2b1.html`) are not rebuilt yet. They would need shorter toolkits, simpler role cards and sentence frames.
