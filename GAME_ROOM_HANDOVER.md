# The Game Room — Handover Document

## What Is It?
The Game Room is a collection of 12 game-based speaking lessons for 1-to-1 Preply lessons. Each game is a different mechanic — the student plays, and the speaking happens naturally inside the game. Every lesson is ~50 minutes, reusable with any student at the target level, and follows the 4th Wall Rule (no teacher notes, no level labels, no pedagogical jargon visible to the student).

## Dashboard
- **File:** `game_room_dashboard.html`
- Dark background, rainbow header, level filter (All / A2 / B1 / B2 / C1)
- 12 game cards with icons, descriptions, and skill tags
- Links to all lesson files

## The 12 Games

### A2 (3 games)
| Game | File | Mechanic | Skills |
|------|------|----------|--------|
| **Odd One Out** | `gr_a2_odd_one_out.html` | 4 words, pick the one that doesn't belong, explain why. Multiple valid answers = discussion. | Vocabulary, justification, comparing |
| **Two Truths & A Lie** | `gr_a2_two_truths.html` | Write 3 statements (2 true, 1 lie), speak about all 3 convincingly. Listener guesses. | Past tenses, storytelling, fluency |
| **The Keyword Builder** | `gr_a2_keyword_builder.html` | Student types keywords, related words "ignite" via Datamuse API. Pick words, build a word map, speak from it. 5→7→9 ladder. | Vocabulary, word maps, fluency |

### B1 (2 games)
| Game | File | Mechanic | Skills |
|------|------|----------|--------|
| **Speed Definitions** | `gr_b1_speed_definitions.html` | Word appears, explain it without saying it (like Taboo). Timer running. How many in 2 minutes? | Paraphrasing, circumlocution, vocabulary |
| **Story Chain** | `gr_b1_story_chain.html` | 5 random words appear, tell a story using all 5 in 60 seconds. Then 5 more words — continue the story. | Improvisation, narrative tenses, coherence |

### B2 (4 games)
| Game | File | Mechanic | Skills |
|------|------|----------|--------|
| **The Keyword Builder** | `sp_b2_keyword_builder.html` | Same as A2 version but with B2-level questions (leadership, news, social media, success). | Vocabulary, word maps, fluency |
| **Bid, Fix & Flip** | `sp_b2_error_auction_flip.html` | Error auction ($500 budget, bid on sentences with errors) + debate flip (argue FOR then AGAINST). | Error correction, debate, accuracy |
| **The Ranking Game** | `gr_b2_the_ranking_game.html` | 8 items, rank 1-8, justify top 3 and bottom 3. Topics: good life, leader qualities, world threats. | Opinion, justification, comparing |
| **Alibi** | `gr_b2_alibi.html` | Build a detailed alibi story, then face cross-examination with 12 tough questions under 20-sec timers. | Narrative tenses, detail, quick thinking |
| **Fact or Bluff** | `gr_b2_fact_or_bluff.html` | 6 surprising statements (3 real, 3 invented), guess which, explain reasoning, debate the real ones. | Critical thinking, speculation, discussion |

### C1 (3 games)
| Game | File | Mechanic | Skills |
|------|------|----------|--------|
| **The Negotiator** | `gr_c1_the_negotiator.html` | Two conflicting role cards, reach a deal under time pressure. 3 scenarios: office move, contract, partnership. | Persuasion, register, diplomacy |
| **Devil's Advocate** | `gr_c1_devils_advocate.html` | State opinion → argue the opposite for 2 min → synthesise both sides. 3 topics + rapid fire. | Concession, nuance, discourse |
| **The Press Conference** | `gr_c1_the_press_conference.html` | Play a public figure in crisis. Opening statement + 6 tough questions with 30-sec answer timers. | Hedging, register control, pressure |

## Design System
- **Light background:** #f8f9fa, dark text #1a1a2e, purple accent #667eea
- **Centred tabs** — `justify-content: center`
- **Cards with shadows** — consistent rounded corners, subtle elevation
- **Timers:** teal/green → yellow (<30s) → red (<10s) + pulse animation
- **Click-reveal:** dashed border → solid green border when revealed
- **Speak prompts:** gradient background with left border accent
- **No emojis in level labels** — level badges hidden from student view

## Exceptions
- The B2 Keyword Builder (`sp_b2_keyword_builder.html`) uses the **dark background** Speaking Pathway design system (not the light Game Room style) because it was built before the Game Room existed. It still works fine.
- The B2 Bid Fix & Flip (`sp_b2_error_auction_flip.html`) uses the light Game Room style.

## Datamuse API
Used in both Keyword Builder lessons. Client-side fetch to `https://api.datamuse.com`. No API key needed. Endpoints: `rel_syn` (synonyms), `rel_ant` (antonyms), `rel_trg` (trigger/related), `rel_jjb` (adjectives). Blocked from some sandboxes but works in the browser.

## The 4th Wall Rule
Every lesson follows these rules:
- No teacher notes or instructions visible
- No pedagogical labels (TEEP phases, "I Do/We Do/You Do")
- No level labels (A2/B1/B2/C1) in student-facing content
- No student names or teacher names
- No "Talk to your teacher" or "Your teacher will..."
- Test: screen-share the HTML. If anything makes the student think "this isn't for me," it fails.

## What's Next
- Build more games at each level as ideas emerge
- Consider themed editions (e.g., Bid Fix & Flip: Business English edition, Alibi: C1 version)
- The dashboard can grow — just add cards
- All games are standalone and reusable — no sequence dependency
