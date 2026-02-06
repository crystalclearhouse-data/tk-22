# Phase 2 Quick Checklist

**Goal**: Create two new empty repositories on GitHub

---

## Pre-Flight

- [ ] Have access to `thediscobass` GitHub account
- [ ] Have access to `the-steele-zone` GitHub account
- [ ] Phase 1 dry-run completed and reviewed
- [ ] Approval received: "Approve Phase 2 — create empty repos only"

---

## Repository 1: thediscobass/tk-22-ui

### Creation
- [ ] Log in to GitHub as **thediscobass**
- [ ] Create new repository: `tk-22-ui`
- [ ] Description: `TK-22 Frontend - User interface and presentation layer for TK-22 evaluation system`
- [ ] Set to **Private**
- [ ] Initialize with README
- [ ] Create repository

### Configuration
- [ ] Settings → Branches → Add protection for `main`
- [ ] Settings → Options → Disable: Wikis, Issues, Projects
- [ ] Settings → Options → Enable: Pull requests, Auto-delete branches
- [ ] Verify repository is accessible

### Record
```
URL: https://github.com/thediscobass/tk-22-ui
Created: ___________
Status: ✅ Complete
```

---

## Repository 2: the-steele-zone/tk-22-experiments

### Creation
- [ ] Log in to GitHub as **the-steele-zone**
- [ ] Create new repository: `tk-22-experiments`
- [ ] Description: `TK-22 Experiments - Personal R&D and proof-of-concept implementations (Not for production use)`
- [ ] Set to **Private**
- [ ] Initialize with README
- [ ] Create repository

### Configuration
- [ ] Settings → Options → Disable: Wikis, Projects
- [ ] Settings → Options → Enable: Issues (for personal tracking)
- [ ] Verify repository is accessible

### Record
```
URL: https://github.com/the-steele-zone/tk-22-experiments
Created: ___________
Status: ✅ Complete
```

---

## Final Verification

- [ ] All three repos exist:
  - [ ] crystalclearhouse-data/tk-22 (unchanged)
  - [ ] thediscobass/tk-22-ui (new, empty)
  - [ ] the-steele-zone/tk-22-experiments (new, empty)
- [ ] All new repos are private
- [ ] All new repos have README.md
- [ ] Original tk-22 repo is unchanged (no commits, no file moves)
- [ ] No errors or issues during creation

---

## Summary

```
Control Plane: https://github.com/crystalclearhouse-data/tk-22
Frontend:      https://github.com/thediscobass/tk-22-ui
Experiments:   https://github.com/the-steele-zone/tk-22-experiments
```

**Phase 2 Complete**: ✅ / ⏳

**Time to Complete**: _______ minutes

**Issues Encountered**: None / [Describe]

**Next Step**: Review Phase 3 plan (file migration)

---

## If Something Goes Wrong

**Rollback Steps:**
1. Go to repository Settings → Danger Zone
2. Click "Delete this repository"
3. Type repository name to confirm
4. Delete repository
5. No data is lost (nothing was moved from original repo)

**Need Help?**
- Review: `docs/PHASE_2_CREATE_EMPTY_REPOS.md` (detailed guide)
- Review: `docs/MULTI_REPO_BOUNDARY_PLAN.md` (overall plan)
