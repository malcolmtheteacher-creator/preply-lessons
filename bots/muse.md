# Muse — twelve painted poses of Mia

**Your task:** paint **12 full-body poses of Mia**, the friendly character of the beginner-English series, so the site can use a painted Mia instead of the plain photos it uses now.

**Reference pictures:** attach **both**, with every prompt:
1. Mia's character sheet (this is who Mia is, face, hair and clothes): https://malcolmhyndman.com/preply-lessons/mia_character_sheet.png
2. The painted room, **only** for the painting style and lighting: https://malcolmhyndman.com/preply-lessons/journey/img/room1_study.webp

**Mia must look exactly the same in all 12 poses:** the same face, hair, skin tone, clothes and proportions as the character sheet. Do not change her outfit or age. If she looks like a different person, regenerate.

**Every image must be:**
- **One person only, full body, head to feet**, centred, fully inside the picture with space around her.
- On a **single flat, even background colour** (pure magenta #FF00FF if the tool can do it; if not, whatever flat colour it gives, such as crimson pink): no gradient, texture, floor or shadow on the background, so Claude can cut her out cleanly. Do not use that colour in her clothes.
- Portrait, **as large as your tool allows: 864 x 1152 pixels is fine.** Do not upscale or recolour an image afterwards; upload it as the tool made it.
- Painted in the house style: near-photorealistic painterly, warm golden light from the upper left, rich oil-paint texture.
- No text, no logos, nothing else in the picture except what the pose names.

**Files:** upload each pose to `journey/incoming/muse/` with the exact names below.

**Acceptance check for each pose:** same Mia as the sheet; full body, nothing cut off; flat even background; the pose matches; no text. If any check fails, regenerate.

**Prompt template.** Use this exactly, replacing only the pose line:

```
[Attached: the Mia character sheet, and one of my painted room images for painting style.]

A masterpiece-quality painted full-body portrait of Mia, exactly as in the character sheet (same face, hair, skin tone, clothes and proportions): <POSE>. One person only, head to feet, centred with space around her, standing on nothing. The background is perfectly flat, pure magenta (#FF00FF) with no gradient, texture, floor or shadow. Do not use magenta or pink in her clothes. Near-photorealistic painterly rendering, warm golden light from the upper left, rich oil-paint texture. No text. Portrait 1024 x 1536 or larger.
```

**The 12 poses, in order:**

1. `mia_pose_01_wave.png` — POSE: Mia waving hello with one hand raised, a warm smile.
2. `mia_pose_02_think.png` — POSE: Mia one hand on her chin, looking up thoughtfully.
3. `mia_pose_03_cheer.png` — POSE: Mia arms raised in a happy celebration, mouth open in a laugh.
4. `mia_pose_04_sleep.png` — POSE: Mia asleep sitting against a cushion with her eyes closed, peaceful.
5. `mia_pose_05_read.png` — POSE: Mia reading an open book held in both hands.
6. `mia_pose_06_coffee.png` — POSE: Mia holding a steaming cup in both hands, relaxed.
7. `mia_pose_07_point.png` — POSE: Mia pointing forward with one finger, encouraging look.
8. `mia_pose_08_surprise.png` — POSE: Mia both hands to her cheeks, eyes wide with surprise.
9. `mia_pose_09_tired.png` — POSE: Mia yawning with one hand over her mouth, sleepy eyes.
10. `mia_pose_10_key.png` — POSE: Mia holding up a large old brass key in one hand, proud smile.
11. `mia_pose_11_walk.png` — POSE: Mia mid-stride walking forward carrying a small shoulder bag.
12. `mia_pose_12_write.png` — POSE: Mia sitting writing in a notebook with a pencil, concentrating.

**What Claude does next:** cuts Mia out, makes transparent versions and puts them into the lessons and My Room. You do not need to do anything else.
