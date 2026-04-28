## Problem
 
Folders `Day1` and `Day2` were renamed via the OS file explorer to `Day1-basic` and `Day2-ifelse`.
 
Git did **not detect this as a rename**. Instead, it treated the operation as:
- Old folders (`Day1`, `Day2`) → **deleted**
- New folders (`Day1-basic`, `Day2-ifelse`) → **untracked / new**
 
On the next `git push`, both old and new folders were pushed to the remote, resulting in **4 directories instead of 2**.
 
---

## Root Cause
 
OS-level rename is **invisible to Git**. Git tracks content by file path — a path change made outside of Git registers as two separate operations: **delete + add**.
 
Since the old folders were never staged for deletion, Git pushed the new folders as additions while the old ones remained untouched on the remote.
 
---
 
## Fix Applied
 
Remove the old folders from Git tracking using the `--cached` flag.
> `--cached` removes files from Git index only — **local files are not deleted**.
 
```bash
git rm -r --cached Day1
git rm -r --cached Day2
 
git commit -m "Remove stale Day1 and Day2 folders (renamed to Day1-basic and Day2-ifelse)"
 
git push origin <your-branch-name>
```
 
---
 
## Future Remediation
 
Always rename tracked folders using `git mv` so Git registers it as a **rename event** — not a delete + add.
 
```bash
git mv Day1 Day1-basic
git mv Day2 Day2-ifelse
 
git commit -m "Rename Day1 → Day1-basic, Day2 → Day2-ifelse"
 
git push origin <your-branch-name>
```
 
---
 
## Summary
 
| | OS Rename | `git mv` |
|---|---|---|
| Git awareness | None | Full |
| Remote behaviour | Duplicate folders | Clean rename |
| Fix needed? | Yes — manual cleanup | No |
 
---