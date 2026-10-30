# START HERE — Malcolm's website art team

You are one of several image bots working for Malcolm, an English teacher. His site, https://malcolmhyndman.com/preply-lessons/, has a page called **My Room**: a painted room that fills with collectible objects as students finish lessons. You are helping to paint the pictures for it and for the rest of the site.

**Claude (the coding assistant) is the project manager and is responsible for the finished result.** You make images. Claude checks every image you deliver, and will say exactly what to fix. Follow your brief exactly.

## Step 1: find your task
Malcolm will have given you a name. Find it in this table and open your brief.

**Round 2.** Round 1 is finished. Find your name below and open your round 2 brief. Each round 2 brief says where its style differs from the shared rules below; where it does, the brief wins for that task.

| Name | Task | Your brief |
|---|---|---|
| **Folio** | Seven cards for the Big Questions page | https://malcolmhyndman.com/preply-lessons/bots/round2_folio.md |
| **Atlas** | Twelve cards for the Psychology Questions page | https://malcolmhyndman.com/preply-lessons/bots/round2_atlas.md |
| **Vista** | Three wide banners for three course pages | https://malcolmhyndman.com/preply-lessons/bots/round2_vista.md |
| **Muse** | Three missing story pictures for the Speak First course | https://malcolmhyndman.com/preply-lessons/bots/round2_muse.md |
| **Lexi** | Nothing yet. Tell Malcolm there is no round 2 task for you until Claude has checked your two sheets, then stop. | none |
| **Grok** | Object sheets 11 to 18 (finished) | https://malcolmhyndman.com/preply-lessons/GROK_START_HERE_object_sheets.md |
| Basil | NOT STARTED. If your name is Basil, tell Malcolm there is nothing to do yet and stop. | none |

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
