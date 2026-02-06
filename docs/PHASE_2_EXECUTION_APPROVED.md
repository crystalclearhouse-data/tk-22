# Phase 2 Execution Instructions

**Status**: ✅ APPROVED — Ready for manual execution  
**Date**: 2026-02-03  
**Approval**: "Approve Phase 2 — create empty repos only"

---

## Quick Summary

Create 2 empty repositories manually via GitHub web UI:

1. **thediscobass/tk-22-ui** (Private)
2. **the-steele-zone/tk-22-experiments** (Private)

**Time**: 15-30 minutes  
**Method**: Manual via GitHub UI (no automation)  
**Risk**: Minimal (empty repos, fully reversible)

---

## Repository 1: thediscobass/tk-22-ui

### Creation Steps
1. Log in to GitHub as **thediscobass**
2. Click "+" → "New repository"
3. Configure:
   - **Owner**: thediscobass
   - **Name**: `tk-22-ui`
   - **Description**: `TK-22 Frontend - User interface and presentation layer for TK-22 evaluation system`
   - **Visibility**: 🔒 Private
   - **Initialize**: ✓ Add a README file
4. Click "Create repository"
5. Verify at: https://github.com/thediscobass/tk-22-ui

### Post-Creation Configuration
1. Go to **Settings**
2. Under "Features":
   - ❌ Uncheck: Wikis, Issues, Projects
   - ✅ Keep: Pull requests
3. Under "Pull Requests":
   - ✅ Check: Automatically delete head branches
4. Under "Branches":
   - Add protection rule for `main`
   - ✅ Require pull request reviews before merging

---

## Repository 2: the-steele-zone/tk-22-experiments

### Creation Steps
1. Log in to GitHub as **the-steele-zone**
2. Click "+" → "New repository"
3. Configure:
   - **Owner**: the-steele-zone
   - **Name**: `tk-22-experiments`
   - **Description**: `TK-22 Experiments - Personal R&D and proof-of-concept implementations (Not for production use)`
   - **Visibility**: 🔒 Private
   - **Initialize**: ✓ Add a README file
4. Click "Create repository"
5. Verify at: https://github.com/the-steele-zone/tk-22-experiments

### Post-Creation Configuration
1. Go to **Settings**
2. Under "Features":
   - ❌ Uncheck: Wikis, Projects
   - ✅ Keep: Issues (for personal tracking)
3. Branch protection is optional for experiments repo

---

## Final Verification Checklist

Open these three URLs and verify:

- [ ] https://github.com/crystalclearhouse-data/tk-22 (unchanged)
- [ ] https://github.com/thediscobass/tk-22-ui (new, empty, private)
- [ ] https://github.com/the-steele-zone/tk-22-experiments (new, empty, private)

All new repos should have:
- ✅ Private visibility
- ✅ README.md file
- ✅ 1 commit (initial commit)
- ✅ Default branch: main

---

## What Phase 2 Does NOT Do

- ❌ No file moves from tk-22
- ❌ No code pushing
- ❌ No history rewriting
- ❌ No automation or scripts
- ❌ No changes to crystalclearhouse-data/tk-22

---

## After Completion

Report back with:
- "Phase 2 complete — both repos created successfully"
- Include screenshot showing all 3 repos exist

Then I will:
1. Update status tracking document
2. Mark Phase 2 as complete
3. Provide Phase 3 preview (but NOT execute)
4. Wait for next approval before any file operations

---

## Rollback (If Needed)

To delete a repository:
1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Delete this repository"
4. Type repository name to confirm
5. Confirm deletion

**No data loss** — nothing was moved from original repo.

---

## Reference Documents

- **Quick Checklist**: `docs/PHASE_2_CHECKLIST.md`
- **Detailed Guide**: `docs/PHASE_2_CREATE_EMPTY_REPOS.md`
- **Status Tracking**: `docs/REPO_SPLIT_STATUS.md`
- **Overall Plan**: `docs/MULTI_REPO_BOUNDARY_PLAN.md`

---

**Proceed when ready. No automation will run. Take your time.**
