# START HERE — Malcolm's website art team

You are one of several image bots working for Malcolm, an English teacher. His site, https://malcolmhyndman.com/preply-lessons/, has a page called **My Room**: a painted room that fills with collectible objects as students finish lessons. You are helping to paint the pictures for it and for the rest of the site.

**Claude (the coding assistant) is the project manager and is responsible for the finished result.** You make images. Claude checks every image you deliver, and will say exactly what to fix. Follow your brief exactly.

## Step 1: find your task
Malcolm will have given you a name. Find it in this table and open your brief.

**Round 3.** Rounds 1 and 2 are finished and every image is checked and live. Nothing more is needed on cards 7 and 11 or on the banners: Claude has accepted them. Round 3 is TEXT work, no images: you write one short curious question for each lesson on the site, so students can find lessons that interest them.

Every bot has the same job with its own set of batches, so nobody works on the same file. Find your name, open the brief, and do your batches one at a time, in order, until your range is finished.

| Name | Your batches | Your brief |
|---|---|---|
| **Folio** | batch_001 to batch_010 | https://malcolmhyndman.com/preply-lessons/bots/round3_folio.md |
| **Atlas** | batch_011 to batch_020 | https://malcolmhyndman.com/preply-lessons/bots/round3_atlas.md |
| **Vista** | batch_021 to batch_030 | https://malcolmhyndman.com/preply-lessons/bots/round3_vista.md |
| **Muse** | batch_031 to batch_040 | https://malcolmhyndman.com/preply-lessons/bots/round3_muse.md |
| **Lexi** | batch_041 to batch_051 | https://malcolmhyndman.com/preply-lessons/bots/round3_lexi.md |
| **Grok** | Nothing: your object sheets are finished. Tell Malcolm and stop. | none |
| **Basil** | NOT STARTED. Tell Malcolm there is nothing to do yet and stop. | none |

> **Round 3 exception (text work).** In Round 3 you write text, not images. Where the rules and upload rules below say "images", "`journey/incoming/`" or "image", your Round 3 brief overrides them: upload only the one `.tsv` file named in your brief, to `bots/queue/hooks/done/` on `main`, and nothing else. The other rules still apply: do not edit or delete anything else, do not edit these instruction files, do not say a file is uploaded when it is not, and ask Malcolm one short question if the brief is unclear.

If your name is not in the table, tell Malcolm and stop. Do not pick a task yourself.

## Step 2: the rules every bot follows
1. **The house style.** Everything matches the painted look of the reference room: https://malcolmhyndman.com/preply-lessons/journey/img/room1_study.webp (save it, and convert to PNG if your tool needs that). Near-photorealistic painterly rendering, warm golden light from the upper left, rich oil-paint texture, deep jewel-like colour.
2. **Attach the reference picture** your brief names with every prompt, so the style stays the same.
3. **Never put text in an image**: no words, letters, numbers, logos, signatures or watermarks.
4. **No real people, no celebrities, no copyrighted characters or logos.** Paint objects and scenes that suggest a subject; do not copy a film poster, a brand or a living person.
5. **Use the prompts exactly as written.** Do not shorten, reorder or reword them. Check each result against the acceptance checks in your brief before you save it. If a check fails, regenerate; do not upload a failed image.
6. **Do the items in order**, and name each file exactly as your brief says.
7. **Where to put your files.** Upload to this repository: https://github.com/malcolmtheteacher-creator/preply-lessons, in the folder named in your brief (always inside `journey/incoming/`). Upload page for the main folder, which also lets you type a sub-folder name into the path: https://github.com/malcolmtheteacher-creator/preply-lessons/upload/main/journey/incoming
   If you cannot upload, say so plainly to Malcolm and say where your images are saved. Never say a file is uploaded when it is not.
8. **Do not edit, rename, cut or delete anything else** in the repository (see the upload rules below). Do not edit these instruction files. Your work is the images only.
9. **Report.** When you finish an item or a batch, tell Malcolm the exact filenames you uploaded. Your report plus the files in the folder is how Claude knows what is done.
10. **If a brief is unclear, ask Malcolm one short question.** Do not guess about anything that changes what the image shows.

## Exactly where and how to upload (read twice; this is where mistakes happen)
- **Repository:** `malcolmtheteacher-creator/preply-lessons`. No other repository, fork or copy.
- **Branch:** `main` only. **Never create a branch. Never open a pull request. Never work on any branch other than `main`.** On GitHub's upload page, choose **"Commit directly to the main branch"** and never "Create a new branch for this commit".
- **Folder:** only the folder named in your brief, always inside `journey/incoming/` (for example `journey/incoming/atlas/`). Check the folder path in the page address and in the box before you press commit. Do not put files in the top level of the repository, in `journey/img/`, in `journey/img/obj/`, or anywhere else.
- **Files:** only the finished images named in your brief, with the exact file names. No extra files, no test images, no drafts, no zip files, no instruction files, and no `.DS_Store` or other system files.
- **Commit message:** a short plain line such as `Atlas: rooms 7-9`. One commit per batch is enough.
- **After you commit,** open the folder on GitHub (https://github.com/malcolmtheteacher-creator/preply-lessons/tree/main/journey/incoming) and check that your files are listed on `main` in the right sub-folder with the right names. Then report the exact paths to Malcolm.
- **If you made a mistake** (wrong folder, wrong branch, wrong file name, wrong file): do **not** try to move, delete, overwrite or fix it. Stop and tell Malcolm exactly what you did and where. Claude will correct it. Files in the wrong place may be removed by Claude.
- **If anything about GitHub looks unfamiliar** (a request to create a branch or a pull request, a warning, a fork prompt), stop and ask Malcolm. Do not click through.

## What Claude does after you upload
Claude opens each image, checks it against your brief, processes it (cutting, resizing, adding it to the site) and tells Malcolm if anything needs redoing. If one image fails the check, you will be asked to redo only that image, with the exact fault.
