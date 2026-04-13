## Problem
 
Folders `Day1` and `Day2` were renamed via the OS file explorer to `Day1-basic` and `Day2-ifelse`.
 
Git did **not detect this as a rename**. Instead, it treated the operation as:
- Old folders (`Day1`, `Day2`) → **deleted**
- New folders (`Day1-basic`, `Day2-ifelse`) → **untracked / new**
 
On the next `git push`, both old and new folders were pushed to the remote, resulting in **4 directories instead of 2**.
 
---

Fix Applied
        Removed old folders from Git tracking using --cached flag (no local files deleted), then pushed the cleanup commit.
        git rm -r --cached Day1
        git rm -r --cached Day2
        git commit -m "Remove stale folders"
        git push origin <branch>

Future Remediation
    Always rename tracked folders using git mv so Git registers it as a rename event, not a delete + new add.
    git mv Day1 Day1-basic
    git mv Day2 Day2-ifelse
    git commit -m "Rename folders"
    git push origin <branch>

Root Cause
    OS-level rename is invisible to Git. Git tracks content by path — a path change without git mv registers as two separate operations: delete + add. This causes duplicate entries on remote when both the old (deleted but not staged) and new (added) folders are pushed.
