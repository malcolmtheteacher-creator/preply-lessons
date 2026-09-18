# Think Inside the Box — series spec (B2)

Thinking tools (grids, pyramids, loops, curves, diagrams, checklists) taught through the
TRUE story of who drew each one. Born 2026-09-17 from a student's mention of the 9-box grid.

## Files
- Lessons: `tib_<slug>_b2.html` (+ `tib_<slug>_a2b1.html` twins) — GENERATED, never hand-edit.
- Your-own-problem page: `think_inside_the_box_your_problem.html` from `tools/tib_chooser.json`.
- Dashboard: `think_inside_the_box_dashboard.html` (hero, clickable map, 10 cards, toolbox link).
- Toolbox: `think_inside_the_box_toolbox.html` — 63 tools in 6 families, search + field filters.
- Content: `tools/tib_content/NN_<slug>.json` (B2) and `tools/tib_content_a2b1/NN_<slug>.json` (twins, 8 key words instead of 10) + `tools/tib_toolbox.json` (the list + dashboard intro).
- Builder: `python3 tools/build_tib.py` rebuilds everything. It refuses to build if a lesson's
  tool is missing from the toolbox, a lesson doesn't have exactly 10 key words, a sort answer isn't
  one of the options, or the same sort answer appears 3 times in a row.
- Homepage: flagship card `.flag-tools` in the website repo `index.html`.

## The 5 tabs
Key Words → The Story (3 parts, check + discuss after each) → **The Tool** (diagram drawn by the
builder, step-by-step use, a “Try it yourself” sorting task with Check button, “Where the tool
breaks”, cousins with links) → Grammar (one point, unique in the series) → Speak (timer, 3 portable
prompts, harder questions).

## The ten lessons
| # | Tool | Story | Grammar |
|---|------|-------|---------|
| 01 | The 9-Box Grid | GE + McKinsey 1970 → talent reviews | comparing with much/far/slightly |
| 02 | The Eisenhower Matrix | D-Day, 1954 speech, Covey 1989 | must / have to / need to / don't have to |
| 03 | The Johari Window | Luft & Ingham 1955 | seem / appear / come across as |
| 04 | The Prisoner's Dilemma | RAND 1950, Tucker, Axelrod's tournament | unless / as long as / provided that |
| 05 | Maslow's Hierarchy of Needs | Maslow 1943; McDermid drew the pyramid 1960 | verb + -ing or to + verb |
| 06 | The Pareto Principle | Pareto 1896, Juran 1940s ("mea culpa") | quantifiers and proportions |
| 07 | The Fishbone Diagram | Ishikawa 1943, Deming 1950, quality circles | the passive |
| 08 | The OODA Loop | John Boyd, "Forty-Second Boyd" | time clauses |
| 09 | The Diffusion of Innovations | Ryan & Gross 1943 hybrid corn, Rogers 1962 | used to and would |
| 10 | SWOT Analysis | SOFT at SRI; Puyt et al. 2023 | must have / might have / can't have |
| 11 | The Risk Matrix | safety practice: likelihood × consequence | likely to / may well / bound to |
| 12 | Tuckman's Team Stages | Tuckman 1965, US Navy; Jensen 1977 | present perfect with for/since |
| 13 | Berry's Acculturation Model | John Berry, Canada, 1970s–80s | relative clauses |
| 14 | The Five Whys | Sakichi Toyoda's loom → Toyota | indirect & reported questions |

**A2/B1 twins (4):** Eisenhower (have to / don't have to), Johari (look & seem), Maslow (need & want),
Pareto (most / a few / a lot of). Same story and tool, simpler language; 8 key words; crosslinked both ways.

**Cross-links out:** IELTS stories pathway, Bet the Company dashboard (frameworks strand) and
c1_pro_28_consulting_frameworks all link in. Tools 11–14 are NOT on the map image — regenerate it
(and re-measure hotspots) if you want them starred there.

Adding lesson 11: add `11_<slug>.json` (copy any existing one), make sure the tool's `name` matches a
toolbox entry exactly, pick an unused grammar point, add a `hotspot` if it's on the map image, run the
builder. Change "ten" in the dashboard text inside `build_tib.py`.

## Hard rules (as for every series)
4th-wall clean · gap-fills empty · teach and test with different sentences · word bank in B never in
the item order · sort answers never 3 in a row and never following the option order · facts
web-checked, legends labelled as legends (Pareto's peas, Maslow's pyramid, SWOT's origin).

## The map picture (ChatGPT) and its clickable spots
Until `ThinkInsideTheBox_map.jpg` exists, the dashboard shows a map drawn in code (every ★ clickable).
When the picture is added, the page shows it instead, with invisible click-areas on the ten lesson
tools. Each lesson's `card.hotspot` = `[left%, top%, width%, height%]` of its label on the picture.
Measure them from the real image, then rebuild.

### Prompt — mind map (landscape, 3:2)
> A beautiful hand-illustrated mind map on warm cream paper, landscape format, titled "Tools for
> Thinking" in a large teal circle in the exact centre. Six thick coloured branches radiate to six
> labelled family circles arranged like a clock: upper-right "Grids & Matrices" (teal), right
> "Pyramids & Ladders" (amber), lower-right "Cycles & Loops" (purple), lower-left "Curves & Rules"
> (crimson), left "Diagrams & Maps" (green), upper-left "Checklists & Canvases" (blue).
> From each family, smaller branches lead to clearly labelled tools, each with a tiny icon of its shape.
> Grids & Matrices: "9-Box Grid" (3×3 grid), "Eisenhower Matrix" (four boxes with a clock),
> "Johari Window" (a four-pane window), "Prisoner's Dilemma" (two figures behind bars).
> Pyramids & Ladders: "Maslow's Hierarchy" (layered pyramid), "Bloom's Taxonomy", "Food Pyramid".
> Cycles & Loops: "OODA Loop" (a circular arrow around a small fighter jet), "Plan–Do–Check–Act",
> "Kolb's Learning Cycle". Curves & Rules: "80/20 Rule" (tall and short bars), "Diffusion Curve"
> (a bell curve with a corn plant), "Hype Cycle". Diagrams & Maps: "Fishbone Diagram" (a fish
> skeleton), "Venn Diagram", "Mind Map". Checklists & Canvases: "SWOT" (four boxes marked S W O T),
> "PESTLE", "Five Forces".
> Make the ten tools 9-Box Grid, Eisenhower Matrix, Johari Window, Prisoner's Dilemma, Maslow's
> Hierarchy, OODA Loop, 80/20 Rule, Diffusion Curve, Fishbone Diagram and SWOT bigger than the others,
> each inside its own rounded label with a small gold star. All text crisp, correctly spelled and
> easy to read. Clean, elegant, educational style with generous white space; no clutter.

### Prompt — dashboard hero (wide banner, 3:1 or as wide as possible)
> A wide, atmospheric banner illustration: a wooden desk seen from above, covered with hand-drawn
> thinking tools on paper and index cards — a 3×3 grid, a four-box matrix, a pyramid, a circular
> loop of arrows, a fish-skeleton diagram, a bell curve and a sheet marked S W O T — with a pencil, a
> coffee cup and a small compass. Deep teal and warm amber colours, soft morning light, slightly
> darker at the centre so white title text can sit on top. Painterly, elegant, no people.

Save as `ThinkInsideTheBox.jpg` (hero) and `ThinkInsideTheBox_map.jpg` (map) — convert ChatGPT PNGs to JPEG (sips, quality 82) so the page loads fast in gitsite.
