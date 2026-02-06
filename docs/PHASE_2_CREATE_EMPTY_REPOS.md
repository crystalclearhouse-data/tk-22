# Phase 2: Create Empty Target Repositories

**Date**: 2026-02-03  
**Status**: Ready for Approval  
**Purpose**: Create empty repository shells on GitHub for the multi-repo split

---

## Executive Summary

Phase 2 creates **empty repository shells only** on GitHub. No files are moved, no code is pushed, and no changes are made to the existing tk-22 repository.

**What Phase 2 Does:**
- ✅ Creates empty repositories on GitHub
- ✅ Sets repository visibility (public/private)
- ✅ Adds basic README.md to each new repo
- ✅ Configures repository settings

**What Phase 2 Does NOT Do:**
- ❌ No file moves from tk-22
- ❌ No code pushing
- ❌ No history rewriting
- ❌ No git operations in existing repo
- ❌ No MCP write access needed
- ❌ No automation scripts
- ❌ No secrets management

**Risk Level**: Minimal (can delete empty repos if needed)

---

## Repository Specifications

### Repo 1: crystalclearhouse-data/tk-22
**Status**: ✅ Already Exists  
**Action**: No changes needed  
**Purpose**: Control plane (current repo)

---

### Repo 2: thediscobass/tk-22-ui
**Status**: 🆕 Create New  
**Owner**: thediscobass GitHub account  
**Name**: `tk-22-ui`  
**Visibility**: Private (can change to Public later)  
**Description**: TK-22 Frontend - User interface and presentation layer for TK-22 evaluation system  

**Initial Files:**
- `README.md` — Basic description
- `.gitignore` — Standard frontend ignores
- `LICENSE` — Copy from parent (if desired)

**Branch Protection:**
- Default branch: `main`
- Protect `main` branch after creation
- Require PR reviews for merges

**Settings:**
- Disable: Wiki, Issues (use parent repo instead)
- Enable: Pull requests
- Delete head branches automatically after merge

---

### Repo 3: the-steele-zone/tk-22-experiments
**Status**: 🆕 Create New  
**Owner**: the-steele-zone GitHub account  
**Name**: `tk-22-experiments`  
**Visibility**: Private  
**Description**: TK-22 Experiments - Personal R&D and proof-of-concept implementations  

**Initial Files:**
- `README.md` — Basic description with "Not for production use" warning
- `.gitignore` — Standard ignores

**Branch Protection:**
- Default branch: `main`
- Optional: Less strict than production repos

**Settings:**
- Disable: Wiki, Projects
- Enable: Issues (for personal tracking)
- Pull requests optional (personal repo)

---

## Step-by-Step Creation Process

### Pre-Flight Checklist

Before creating any repositories, verify:

- [ ] Access to thediscobass GitHub account confirmed
- [ ] Access to the-steele-zone GitHub account confirmed
- [ ] Current tk-22 repo is in clean state (no uncommitted changes)
- [ ] Phase 1 dry-run report reviewed and approved
- [ ] Team members notified of Phase 2 start

---

### Step 1: Create thediscobass/tk-22-ui

**Manual Steps (via GitHub Web UI):**

1. Log in to GitHub as **thediscobass** account
2. Click "+" → "New repository"
3. Configure:
   - Owner: `thediscobass`
   - Repository name: `tk-22-ui`
   - Description: `TK-22 Frontend - User interface and presentation layer for TK-22 evaluation system`
   - Visibility: ⚫ Private
   - ✅ Initialize with README
   - Add .gitignore: None (will add custom later)
   - License: None (will add later if needed)
4. Click "Create repository"

**Post-Creation:**

5. Go to Settings → Branches
6. Add branch protection rule for `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
7. Go to Settings → Options
8. Disable:
   - ❌ Wikis
   - ❌ Issues (use parent repo)
   - ❌ Projects
9. Enable:
   - ✅ Pull requests
   - ✅ Automatically delete head branches

**Verification:**

10. Visit `https://github.com/thediscobass/tk-22-ui`
11. Confirm:
    - ✅ Repository exists
    - ✅ Is private
    - ✅ Has README.md
    - ✅ Default branch is `main`

**Record Details:**
```
Repository URL: https://github.com/thediscobass/tk-22-ui
Created: [DATE]
Initial commit: [COMMIT SHA]
```

---

### Step 2: Create the-steele-zone/tk-22-experiments

**Manual Steps (via GitHub Web UI):**

1. Log in to GitHub as **the-steele-zone** account
2. Click "+" → "New repository"
3. Configure:
   - Owner: `the-steele-zone`
   - Repository name: `tk-22-experiments`
   - Description: `TK-22 Experiments - Personal R&D and proof-of-concept implementations (Not for production use)`
   - Visibility: ⚫ Private
   - ✅ Initialize with README
   - Add .gitignore: None (will add custom later)
   - License: None
4. Click "Create repository"

**Post-Creation:**

5. Go to Settings → Branches (optional for experiments)
6. Add branch protection rule for `main` (optional):
   - ✅ Require pull request reviews (optional)
7. Go to Settings → Options
8. Disable:
   - ❌ Wikis
   - ❌ Projects
9. Enable:
   - ✅ Issues (for personal tracking)

**Verification:**

10. Visit `https://github.com/the-steele-zone/tk-22-experiments`
11. Confirm:
    - ✅ Repository exists
    - ✅ Is private
    - ✅ Has README.md
    - ✅ Default branch is `main`

**Record Details:**
```
Repository URL: https://github.com/the-steele-zone/tk-22-experiments
Created: [DATE]
Initial commit: [COMMIT SHA]
```

---

### Step 3: Verify All Repositories

**Verification Checklist:**

- [ ] crystalclearhouse-data/tk-22 — Exists (unchanged)
- [ ] thediscobass/tk-22-ui — Created and accessible
- [ ] the-steele-zone/tk-22-experiments — Created and accessible
- [ ] All repos are private
- [ ] All repos have README.md
- [ ] All repos have `main` as default branch
- [ ] No files moved from original repo
- [ ] Original repo is unchanged

**Document Repository URLs:**
```
Control Plane: https://github.com/crystalclearhouse-data/tk-22
Frontend:      https://github.com/thediscobass/tk-22-ui
Experiments:   https://github.com/the-steele-zone/tk-22-experiments
```

---

## Initial README.md Templates

### For thediscobass/tk-22-ui

```markdown
# TK-22 Frontend

User interface and presentation layer for the TK-22 evaluation system.

## Status

🚧 **Repository initialized** — Content migration pending

## Purpose

This repository contains the public-facing frontend for TK-22:
- User onboarding interface
- Evaluation request submission
- Results presentation
- Legal documentation

## Integration

Frontend integrates with the TK-22 control plane via API:
- Control Plane: [crystalclearhouse-data/tk-22](https://github.com/crystalclearhouse-data/tk-22)
- API Endpoint: `POST /execute`
- Contract: See `docs/contract.md` (after migration)

## Development

Setup instructions will be added after content migration from the control plane repository.

## Owner

Maintained by: thediscobass
```

### For the-steele-zone/tk-22-experiments

```markdown
# TK-22 Experiments

Personal R&D and proof-of-concept implementations for TK-22 system.

⚠️ **Not for production use**

## Purpose

This repository is for:
- Experimental features
- Proof-of-concept implementations
- Personal consulting work
- Research and exploration

## Relationship to Production

- Control Plane: [crystalclearhouse-data/tk-22](https://github.com/crystalclearhouse-data/tk-22)
- Frontend: [thediscobass/tk-22-ui](https://github.com/thediscobass/tk-22-ui)

This repo may read from production APIs but has no write access to production systems.

## Owner

Maintained by: the-steele-zone
```

---

## Safety Measures

### What Makes Phase 2 Safe

1. **No Code Loss**: Original repo unchanged
2. **Reversible**: Empty repos can be deleted
3. **No Automation**: Manual creation via web UI
4. **No Secrets**: No credentials or keys involved
5. **No File Moves**: All content stays in tk-22
6. **No History Rewriting**: No git operations

### If Something Goes Wrong

**Problem**: Wrong repository name
**Solution**: Delete and recreate (no data loss)

**Problem**: Wrong visibility setting
**Solution**: Change in Settings → Options → Danger Zone

**Problem**: Wrong owner account
**Solution**: Delete repo and create under correct account

**Problem**: Uncertainty about settings
**Solution**: Pause and review this document again

### Rollback Procedure

If Phase 2 needs to be rolled back:

1. Delete `thediscobass/tk-22-ui` (if created)
2. Delete `the-steele-zone/tk-22-experiments` (if created)
3. Original `crystalclearhouse-data/tk-22` remains unchanged
4. No data is lost (nothing was moved)

**To delete a repository:**
1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Delete this repository"
4. Type repository name to confirm
5. Confirm deletion

---

## Post-Phase 2 State

**After Phase 2 Completion:**

✅ Three repositories exist on GitHub:
- crystalclearhouse-data/tk-22 (unchanged, contains all code)
- thediscobass/tk-22-ui (empty except README)
- the-steele-zone/tk-22-experiments (empty except README)

✅ All repositories are:
- Private
- Protected (main branch)
- Properly named
- Owned by correct accounts

❌ No code has moved yet
❌ No file operations performed
❌ No git operations in original repo

---

## Next Phase Preview

**Phase 3** (not started yet) will:
- Copy (not move) frontend files to thediscobass/tk-22-ui
- Verify copied files work independently
- Prepare removal from control plane (but not remove yet)

Phase 3 will only start after Phase 2 is complete and verified.

---

## Approval Gates

Before proceeding to Phase 3:

- [ ] Phase 2 completion verified
- [ ] All three repos accessible
- [ ] Repository settings confirmed correct
- [ ] URLs documented
- [ ] Team notified of completion
- [ ] Phase 3 plan reviewed

---

## Success Criteria

Phase 2 is successful when:

1. ✅ `thediscobass/tk-22-ui` exists and is accessible
2. ✅ `the-steele-zone/tk-22-experiments` exists and is accessible
3. ✅ Both new repos are private
4. ✅ Both new repos have basic README.md
5. ✅ Original `crystalclearhouse-data/tk-22` is unchanged
6. ✅ All repository URLs documented
7. ✅ No errors or issues during creation
8. ✅ All three accounts can access their respective repos

---

## Timeline Estimate

**Phase 2 Duration**: 15-30 minutes

Breakdown:
- Repository creation: 5 minutes per repo
- Settings configuration: 5 minutes per repo
- Verification: 5 minutes total
- Documentation: 5 minutes total

**No automation** — all steps are manual and deliberate.

---

## Notes

- This phase requires access to three separate GitHub accounts
- No GitHub API or automation tools are used
- All actions are performed via GitHub web interface
- This is the safest possible next step
- Completely reversible with no data loss risk

---

## Contact Points

If issues arise during Phase 2:

1. **Repository Creation Issues**: Check GitHub account access
2. **Permission Issues**: Verify account ownership
3. **Settings Issues**: Review this guide's specifications
4. **Uncertainty**: Stop and review the plan again

---

**Status**: Ready for execution after approval

**Approval Required**: "Approve Phase 2 — create empty repos only"
