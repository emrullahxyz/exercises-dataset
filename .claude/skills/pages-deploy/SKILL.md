---
name: pages-deploy
description: Commit and publish changes to GitHub Pages for this repo, handling the two known gotchas — browser cache-busting and the Windows credential-manager push hang. Use when asked to deploy, publish, push, or ship changes to the live site.
disable-model-invocation: true
---

# Deploy to GitHub Pages

The repo (`emrullahxyz/exercises-dataset`, `origin/main`) is served directly by GitHub Pages
at https://emrullahxyz.github.io/exercises-dataset/ . There is no build step — pushing to
`main` publishes. Two recurring gotchas (documented in context.md) are handled here.

## Procedure

1. **Validate the dataset first** (cheap insurance before publishing):
   `python .claude/scripts/validate_dataset.py`

2. **Cache-bust changed asset references.** After visual/design changes, Pages takes 1–2 min
   to publish and browsers cache for ~10 min. If a change touches how an HTML page loads a
   stylesheet/script/asset, bump a `?v=N` query param on that reference so users get the new
   version. Tell the user the exact URL (with `?v=N`) to hard-check.

3. **Commit** with a clear conventional message (`feat:` / `fix:` / `chore:` …). Never commit
   `images/`/`videos/` deletions unless explicitly intended.

4. **Push — with the credential-hang fallback.** A plain `git push` on Windows can freeze on a
   Windows Credential Manager prompt (especially after a reboot). If it stalls, push via token:
   ```
   git push https://emrullahxyz:$(gh auth token)@github.com/emrullahxyz/exercises-dataset.git HEAD:main
   ```

5. **Report:** give the user the live URL, note the ~1–2 min publish delay, and the `?v=N`
   buster if one was added.

## Notes
- Confirm with the user before pushing — a push publishes to the live site.
- `origin` is the user's fork; `upstream` is the original repo (hasaneyldrm) — never push there.
