# Phase 1 Dry Run — Quick Start Guide

This guide explains how to run the Phase 1 dry-run task for the repository split.

## What This Does

The Phase 1 dry-run task:
- ✅ Reads the planning document at `docs/MULTI_REPO_BOUNDARY_PLAN.md`
- ✅ Lists all detected top-level folders in the repository
- ✅ Shows proposed ownership simulation (no actual changes)
- ✅ Confirms safety checks (no files moved, no git changes, no remotes touched)
- ✅ Generates a report at `reports/repo-split-dry-run.md`

**Zero Risk**: Nothing changes on disk or in Git.

## How to Run It

### Option 1: VS Code Task Runner (Recommended)

1. Open Command Palette: `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows/Linux)
2. Type: `Run Task`
3. Select: `🧱 Repo Split — Phase 1 (Dry Run)`
4. View the output in the integrated terminal

### Option 2: Command Line

```bash
bash scripts/prepare-repo-split-dry-run.sh
```

## Output

After running, check the generated report:

```bash
cat reports/repo-split-dry-run.md
```

## What's Next

After reviewing the dry-run report, you can:

1. **"Approve Phase 1 — create empty repos"** — Proceed to Phase 2
2. **"Adjust ownership map"** — Modify the proposed ownership structure
3. **"Explain the report like I'm 10"** — Get a simpler explanation
4. **"Pause here"** — Stop and review before proceeding

## Files Created

- `.vscode/tasks.json` — VS Code task definition
- `scripts/prepare-repo-split-dry-run.sh` — Dry-run execution script
- `reports/repo-split-dry-run.md` — Generated report (excluded from git)

## Safety Guarantees

- ✅ No files are moved or deleted
- ✅ No git commits are made by the script
- ✅ No remote repositories are touched
- ✅ The generated report is excluded from version control
- ✅ The original repository structure remains intact
