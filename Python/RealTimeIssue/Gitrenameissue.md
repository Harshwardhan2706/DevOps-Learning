## Problem
 
`Day1` and `Day2` were renamed via OS file explorer to `Day1-basic` and `Day2-ifelse`.
Git saw this as **delete + add** — resulting in **4 folders on remote instead of 2**.
 
---
 
## Root Cause
 
OS-level rename is **invisible to Git**. Git tracks by file path, so renaming outside Git = old path deleted + new path untracked.
 
---
 
## Fix Applied
 
```bash
git rm -r --cached Day1 Day2   # remove stale folders from index only (local files safe)
 
git commit -m "Remove stale Day1 and Day2 folders"
git push origin <branch>
```
 
---
 
## Future Remediation
 
Always use `git mv` — Git registers it as a **rename**, not delete + add.
 
```bash
git mv Day1 Day1-basic
git mv Day2 Day2-ifelse
 
git commit -m "Rename Day1 → Day1-basic, Day2 → Day2-ifelse"
git push origin <branch>
```
 
---
 
## Summary
 
| | OS Rename | `git mv` |
|---|---|---|
| Git awareness | None | Full |
| Remote behaviour | Duplicate folders | Clean rename |
| Fix needed? | Yes | No |
 
---