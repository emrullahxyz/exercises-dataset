---
name: add-exercise
description: Add a new exercise to the dataset end-to-end — media files, the multilingual exercises.json record, and (if used in the workout plan) the trimmed EXERCISES_RAW copy in my_workout.html. Use when adding, inserting, or importing a new exercise. Keeps JSON, media, and the workout app in sync.
disable-model-invocation: true
---

# Add an exercise to the dataset

Adding an exercise is a multi-step ritual where any missed step silently desyncs the
dataset. This is the canonical procedure (the precedent is `cat-cow` id 5202 and
`bird dog` id 5203, added the same way).

## Inputs to collect from the user first
- **Exercise name** (lowercase, matches the dataset's style, e.g. `barbell bench press`)
- **A `.gif` animation** and **a `.jpg` thumbnail** (source path or URL). ExerciseDB-style
  square framing is expected — if the GIF isn't square, pad it to a square canvas so cards
  don't crop it (see the `bird dog` commit for the padding precedent).
- **Metadata**: `category` / `body_part`, `equipment`, `target`, `muscle_group`,
  `secondary_muscles[]`
- **Instructions in all four languages**: `en`, `es`, `it`, `tr` (full step-by-step). If the
  user gives only one, translate the rest — do not ship an incomplete record.

## Steps (do them all, in order)

1. **Pick the id and suffix.** `id` is a string. If the exercise exists in ExerciseDB, reuse
   its numeric id and media suffix; for brand-new ones use a high free id (the added
   ones use 5202/5203). Media basename = `{id}-{suffix}` (suffix is any short token; the
   originals use ExerciseDB's media id).

2. **Place the media** with the exact naming convention — the thumbnail and GIF share the
   same basename:
   - `images/{id}-{suffix}.jpg`
   - `videos/{id}-{suffix}.gif`

3. **Insert the record into `data/exercises.json`** at its **alphabetical position by name**
   (the array is name-sorted). Full schema (see README.md and any existing record):
   `id, name, category, body_part, equipment, instructions{en,es,it,tr}, muscle_group,`
   `secondary_muscles[], target, image, gif_url, created_at`. Set `image` to
   `images/{id}-{suffix}.jpg` and `gif_url` to `videos/{id}-{suffix}.gif`.
   Names must be plain Latin/ASCII+° — no mojibake (watch for `в°` instead of `°`).

4. **Only if the exercise is used in the workout plan:** add its **trimmed** copy to
   `EXERCISES_RAW` in `my_workout.html`. Trim rules (from context.md): keep only fields the
   app uses — `instruction_steps` limited to **en + tr** only; **no** `it`/`es`, **no**
   paragraph `instructions`, **no** `created_at`. Then reference it in the relevant `PLAN`
   day's `exercises` array with `{ name, sets, label, ... }`. `EXERCISES_RAW` is indexed by
   `name`, so the name must match `exercises.json` exactly.

5. **Validate:** run `python .claude/scripts/validate_dataset.py --strict` — it confirms the
   JSON parses, ids are unique, both media files exist, names are clean, and flags orphans.

6. **Ship:** invoke the `/pages-deploy` skill to commit + push + cache-bust.

## Guardrails
- Never add a record whose media files aren't actually on disk.
- Never leave `instructions` with fewer than all four languages in `exercises.json`.
- The name is the join key everywhere (JSON ↔ EXERCISES_RAW ↔ backend notes DB) — keep it
  byte-identical across all three.
