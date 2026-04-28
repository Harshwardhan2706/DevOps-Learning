## Problem
 
`git push -u origin main` was rejected with a **non-fast-forward error**.
`git pull origin main` then failed with a **divergent branches error** — Git didn't know how to reconcile the two histories.
 
---
 
## Root Cause
 
Local `main` and remote `main` had **independent commits** — neither was an ancestor of the other.
Git requires an explicit strategy (`merge`, `rebase`, or `fast-forward`) to proceed.
 
---
 
## Fix Applied
 
```bash
git pull origin main --no-rebase   # merge diverged histories
# Vim opened → save with :wq
# Resolved red diff block in VS Code
git push -u origin main            # push succeeded ✅
```
 
---
 
## Future Remediation
 
```bash
# Set merge as default pull strategy globally
git config --global pull.rebase false
 
# Set VS Code as Git editor (avoid Vim)
git config --global core.editor "code --wait"
 
# Always pull before starting work
git pull origin main
```
 
---
 
## Summary
 
| | Issue | Fix |
|---|---|---|
| Push rejected | Non-fast-forward | `git pull` first |
| Pull failed | Divergent branches | `--no-rebase` flag |
| Vim opened | Merge commit prompt | `:wq` to save & exit |
| Diff conflict | Red block in VS Code | Resolved manually |
 
---