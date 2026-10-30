# Lexi — picture-words for beginner lessons

**Your task:** paint **2 sheets of 36 small objects** (72 pictures) for the words in the beginner (A1) English lessons. A student who sees a clear picture of "key" or "bridge" learns the word faster. These are cut out and shown next to the words in the word bank.

**This is exactly the same sheet job as the object sheets Grok does.** The same format rules apply.

**Reference picture:** attach https://malcolmhyndman.com/preply-lessons/journey/img/room1_study.webp with each sheet, only for painting style, lighting and colour richness.

**Every sheet must be:**
- **One square image, 2048 x 2048 pixels or larger**, with **exactly 36 objects in a 6 columns x 6 rows grid**, in the order listed, each fully separate with empty space all round it, centred in its cell, none touching, none cut off.
- A **flat pure magenta background (#FF00FF)**: no gradient, texture or shadows on the background. No magenta or pink inside the objects.
- Painted in the house style: near-photorealistic painterly collectible pieces, warm golden light from the upper left, same slightly raised three-quarter view, all about the same size, **clear and instantly recognisable**, because these teach beginners. Keep each object simple and readable, with one main thing in it.
- No text, letters, numbers, logos or watermarks, and no people.

**Files:** upload to `journey/incoming/lexi/` as `words_sheet_01.png` and `words_sheet_02.png`.

**Acceptance check:** exactly 36 objects in a clean 6 x 6 grid, in the order listed; the **top-left object matches the "first object" line**; flat magenta background; no text; clear and recognisable. If it fails, regenerate. If 36 will not fit, make two images of 3 rows each and tell Malcolm.

**Prompt template.** Use this exactly, replacing only the object rows:

```
[Attached: one of my painted room images. Use it only as the reference for painting style, lighting and colour richness.]

A masterpiece-quality painted collection sheet of EXACTLY 36 small clear objects, arranged in a perfect grid of 6 columns by 6 rows, every object fully separate with generous empty space around it. The background is perfectly flat, pure magenta (#FF00FF) with no gradient, texture or shadows. Do not use magenta or pink anywhere in the objects. Style: near-photorealistic painterly rendering like collectible museum pieces, rich oil-paint texture, warm golden light from the upper left, jewel-like colour, the same slightly raised three-quarter angle, each object centred in its cell, about the same size, fully inside its cell, crisp clean edge, simple and instantly recognisable. No text, letters, numbers or logos. The objects, left to right, top to bottom:
<ROWS>
Every object is complete and clearly separate. Square image, 2048 x 2048 or larger.
```

## Sheet 1 (`words_sheet_01.png`)

First object (top-left): a cup of coffee

Put this in place of <ROWS>:

```
Row 1: a cup of coffee; a cup of tea; a glass of water; a sandwich; an old brass key; a handbag.
Row 2: a wooden door; a framed family photo; a plate of breakfast with egg and toast; a school lunch box; a pair of headphones with music notes; a book.
Row 3: a market stall; a bowl of fruit; a red apple; a purse with coins; a small town street; a park bench.
Row 4: a river with a stone bridge; a railway station sign; a hill with a path; a cat; a birthday cake; an egg.
Row 5: a bowl of sugar cubes; an umbrella; a blue sea wave; a sandy beach with a bucket; a red bus; an ice cream cone.
Row 6: a seashell; a party hat with balloons; a jacket on a hanger; a summer dress; a steam train; a suitcase.
```

## Sheet 2 (`words_sheet_02.png`)

First object (top-left): a bicycle

Put this in place of <ROWS>:

```
Row 1: a bicycle; a hilltop castle; a picnic blanket and basket; a folded map; a serving tray; a flight of stairs.
Row 2: a bedroom; a brick wall; a cardboard box; a patterned rug; a house plant in a pot; an open fridge.
Row 3: a bottle of milk; a loaf of bread; a block of butter; a bowl of rice; a shopping trolley; a newspaper.
Row 4: an acoustic guitar; a jar of coins; a wall calendar; a lit candle; a paper lantern; a diary with a pencil.
Row 5: a clock showing seven o'clock; a pair of running shoes; a toothbrush; a wristwatch; a wooden chair; a wooden table.
Row 6: a lamp; a bed with a pillow; a bathroom mirror; a soccer ball; a window with curtains; a mobile phone.
```

**What Claude does next:** cuts each sheet into 36 pictures and adds them to the word bank next to the words. You do not need to do anything else.
