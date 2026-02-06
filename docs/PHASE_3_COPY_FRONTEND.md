# Phase 3: Copy Frontend Files to thediscobass/tk-22-ui

**Date**: 2026-02-06  
**Status**: Ready for Execution (Requires Phase 2 Completion)  
**Purpose**: Copy frontend files to the new frontend repository without modifying the control plane

---

## Prerequisites - What You Need

### ✅ Phase 2 Must Be Complete

Before starting Phase 3, verify:

- [ ] Repository `thediscobass/tk-22-ui` exists on GitHub
- [ ] Repository `the-steele-zone/tk-22-experiments` exists on GitHub
- [ ] Both repositories are private
- [ ] Both repositories have been initialized (have at least README.md)
- [ ] You have write access to `thediscobass/tk-22-ui`

**How to Verify:**
1. Visit https://github.com/thediscobass/tk-22-ui
2. Visit https://github.com/the-steele-zone/tk-22-experiments
3. Confirm both are accessible

### ✅ Git Access Requirements

You will need ONE of the following:

**Option A: Manual Execution (Recommended for Safety)**
- Access to thediscobass GitHub account via browser
- Ability to clone/push to thediscobass/tk-22-ui

**Option B: Automated Execution (Advanced)**
- GitHub Personal Access Token for thediscobass account with `repo` permissions
- Git configured with appropriate credentials

---

## Executive Summary

Phase 3 **copies** (does not move) frontend files from the control plane to the new frontend repository.

**What Phase 3 Does:**
- ✅ Copies `/frontend/` directory to new repo
- ✅ Copies `/legal/` directory to new repo
- ✅ Copies `docs/FRONTEND_CONTROL_CONTRACT.md` to new repo
- ✅ Creates appropriate README.md for frontend repo
- ✅ Initializes git and pushes to thediscobass/tk-22-ui
- ✅ Verifies files are accessible in new repo

**What Phase 3 Does NOT Do:**
- ❌ No files removed from crystalclearhouse-data/tk-22
- ❌ No modifications to control plane repository
- ❌ No deletion of any existing content
- ❌ Original files remain untouched

**Risk Level**: Medium (creates duplicates, but safe)  
**Reversibility**: 100% (can delete copied files, original unchanged)  
**Timeline**: 20-40 minutes

---

## Files to Copy

### From crystalclearhouse-data/tk-22

```
Source Repository: crystalclearhouse-data/tk-22
├── frontend/
│   ├── lovable_prompt.md
│   ├── ui_copy.md
│   └── states.md
├── legal/
│   ├── privacy.md
│   ├── terms.md
│   └── disclaimer.md
└── docs/
    └── FRONTEND_CONTROL_CONTRACT.md
```

### To thediscobass/tk-22-ui

```
Target Repository: thediscobass/tk-22-ui
├── README.md (new, to be created)
├── src/ (or root)
│   ├── lovable_prompt.md
│   ├── ui_copy.md
│   └── states.md
├── legal/
│   ├── privacy.md
│   ├── terms.md
│   └── disclaimer.md
└── docs/
    └── contract.md (was FRONTEND_CONTROL_CONTRACT.md)
```

---

## Step-by-Step Execution Guide

### Option A: Manual Execution (Safer, Recommended)

#### Step 1: Prepare Temporary Directory

```bash
# Create temporary working directory
mkdir -p /tmp/tk-22-ui-migration
cd /tmp/tk-22-ui-migration

# Clone the new frontend repo
git clone https://github.com/thediscobass/tk-22-ui.git
cd tk-22-ui
```

#### Step 2: Copy Files from Control Plane

```bash
# Navigate to control plane repo
cd /home/runner/work/tk-22/tk-22

# Copy frontend files
cp -r frontend /tmp/tk-22-ui-migration/tk-22-ui/src

# Copy legal files
cp -r legal /tmp/tk-22-ui-migration/tk-22-ui/

# Copy contract document
mkdir -p /tmp/tk-22-ui-migration/tk-22-ui/docs
cp docs/FRONTEND_CONTROL_CONTRACT.md /tmp/tk-22-ui-migration/tk-22-ui/docs/contract.md
```

#### Step 3: Create Frontend README

Create `/tmp/tk-22-ui-migration/tk-22-ui/README.md`:

```markdown
# TK-22 Frontend

User interface and presentation layer for the TK-22 evaluation system.

## Status

🚀 **Repository initialized** — Migrated from control plane

## Purpose

This repository contains the public-facing frontend for TK-22:
- User onboarding interface
- Evaluation request submission
- Results presentation
- Legal documentation

## Architecture

Frontend integrates with the TK-22 control plane via API:
- **Control Plane**: [crystalclearhouse-data/tk-22](https://github.com/crystalclearhouse-data/tk-22)
- **API Endpoint**: `POST /execute`
- **Contract**: See `docs/contract.md`

## Integration Contract

The frontend follows strict separation of concerns:
- Displays verdicts (never interprets them)
- Submits user input to control plane
- Shows execution state (RECEIVED, RUNNING, BLOCKED, COMPLETE)
- Renders verdict responses (SAFE_TO_PROCEED, ACTION_REQUIRED, DO_NOT_PROCEED)

See `docs/contract.md` for full API contract.

## Repository Contents

- `/src/` — Frontend source files
- `/legal/` — Privacy policy, terms of service, disclaimers
- `/docs/` — Contract and documentation

## Development

Setup instructions will be added as development progresses.

## Owner

**Maintained by**: thediscobass  
**Control Plane**: crystalclearhouse-data/tk-22  
**Experiments**: the-steele-zone/tk-22-experiments
```

#### Step 4: Create .gitignore

Create `/tmp/tk-22-ui-migration/tk-22-ui/.gitignore`:

```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
.next/
out/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/

# Temporary files
*.tmp
*.log
```

#### Step 5: Commit and Push

```bash
cd /tmp/tk-22-ui-migration/tk-22-ui

# Add all files
git add .

# Commit
git commit -m "Initial frontend migration from tk-22 control plane

Migrated files:
- Frontend UI files (lovable_prompt.md, ui_copy.md, states.md)
- Legal documentation (privacy, terms, disclaimer)
- Frontend-control contract

Source: crystalclearhouse-data/tk-22
Date: 2026-02-06
Phase: 3 of multi-repo split"

# Push to main branch
git push origin main
```

#### Step 6: Verify on GitHub

1. Visit https://github.com/thediscobass/tk-22-ui
2. Verify files are present:
   - [ ] README.md
   - [ ] src/ directory with frontend files
   - [ ] legal/ directory
   - [ ] docs/contract.md
3. Check commit history shows the migration commit

---

### Option B: Automated Script (Advanced)

If you prefer automated execution, I can create a script. This requires:
- GitHub Personal Access Token
- Git credentials configured
- Confirmation of repo access

**Script would:**
1. Clone thediscobass/tk-22-ui
2. Copy all required files
3. Create README and .gitignore
4. Commit and push automatically

⚠️ **Note**: Manual execution is safer for first-time migration.

---

## Verification Checklist

After completing the migration, verify:

### Repository Structure
- [ ] `thediscobass/tk-22-ui` has README.md
- [ ] Frontend files present in `/src/` or root
- [ ] Legal files present in `/legal/`
- [ ] Contract present in `/docs/contract.md`
- [ ] .gitignore is configured

### Git Status
- [ ] All files committed
- [ ] Pushed to main branch
- [ ] No uncommitted changes
- [ ] Repository is up to date with remote

### Original Repository Unchanged
- [ ] `crystalclearhouse-data/tk-22` still has `/frontend/` directory
- [ ] `crystalclearhouse-data/tk-22` still has `/legal/` directory
- [ ] No commits made to control plane during Phase 3
- [ ] Working tree clean in control plane

### Access and Visibility
- [ ] `thediscobass/tk-22-ui` is private (or desired visibility)
- [ ] Repository is accessible to thediscobass account
- [ ] All team members can access (if needed)

---

## Safety Measures

### What Makes Phase 3 Safe

1. **No Deletion**: Original files remain in control plane
2. **Copy Only**: Creating duplicates, not moving
3. **Reversible**: Can delete new repo and start over
4. **No Production Impact**: Control plane unchanged
5. **Verification Steps**: Multiple checkpoints

### If Something Goes Wrong

**Problem**: Files didn't copy correctly  
**Solution**: Delete `/tmp/tk-22-ui-migration`, start over

**Problem**: Push failed  
**Solution**: Check credentials, verify repo access, try again

**Problem**: Missing files in target repo  
**Solution**: Re-run copy commands, verify source files exist

**Problem**: Wrong repository structure  
**Solution**: Delete target repo content, reorganize, push again

### Rollback Procedure

If Phase 3 needs to be rolled back:

1. Delete all content from `thediscobass/tk-22-ui` (or delete entire repo)
2. Original files are still in `crystalclearhouse-data/tk-22`
3. No data loss — everything can be re-attempted
4. Clean up `/tmp/tk-22-ui-migration` directory

**To reset target repository:**
```bash
# In thediscobass/tk-22-ui
git rm -rf .
git commit -m "Reset repository for re-migration"
git push origin main
```

---

## Post-Phase 3 State

**After Phase 3 Completion:**

✅ Files exist in both repositories:
- crystalclearhouse-data/tk-22 (original, unchanged)
- thediscobass/tk-22-ui (new copy)

✅ Both repositories are independent:
- Each has own git history
- Each can be modified independently
- No shared commit history

❌ Duplicates exist temporarily:
- Same files in both repos
- Will be cleaned up in Phase 4

---

## Next Phase Preview

**Phase 4** (not started yet) will:
- Remove frontend files from crystalclearhouse-data/tk-22
- Update control plane README to reference frontend repo
- Verify control plane works without frontend files
- Only starts after Phase 3 complete and verified

Phase 4 is HIGH RISK and requires explicit approval.

---

## Approval Gates

Before proceeding:

- [ ] Phase 2 verified complete (repos exist)
- [ ] Prerequisites checked (access confirmed)
- [ ] Execution method chosen (manual vs automated)
- [ ] Team notified of Phase 3 start
- [ ] Approval received: "Approve Phase 3 — copy frontend files"

After completion:

- [ ] All verification steps passed
- [ ] Files confirmed in target repo
- [ ] Original repo confirmed unchanged
- [ ] Team notified of Phase 3 completion
- [ ] Phase 4 approval NOT granted yet

---

## Success Criteria

Phase 3 is successful when:

1. ✅ `thediscobass/tk-22-ui` contains all frontend files
2. ✅ `thediscobass/tk-22-ui` has proper README.md
3. ✅ All commits pushed to main branch
4. ✅ Repository is accessible and functional
5. ✅ Original `crystalclearhouse-data/tk-22` unchanged
6. ✅ No errors during migration
7. ✅ All files present and correctly organized
8. ✅ Git history is clean

---

## Timeline Estimate

**Phase 3 Duration**: 20-40 minutes

Breakdown:
- Preparation and setup: 5 minutes
- File copying: 5 minutes
- README and .gitignore creation: 5 minutes
- Commit and push: 5 minutes
- Verification: 10 minutes
- Documentation update: 5-10 minutes

---

## What You Need to Tell Me

To proceed with Phase 3, please provide:

### Required Information

1. **Phase 2 Status Confirmation**:
   - "Phase 2 complete — repos created successfully"
   - OR URLs to both created repositories

2. **Execution Preference**:
   - "Use manual execution" (recommended)
   - OR "Create automation script" (provide token)

3. **Approval Statement**:
   - "Approve Phase 3 — copy frontend files"

### Optional Information

- GitHub Personal Access Token (if automation desired)
- Any specific file organization preferences
- Any additional files to include/exclude

---

## Notes

- Phase 3 can be executed multiple times safely (idempotent)
- Original repository is never modified in Phase 3
- Can pause at any checkpoint for review
- Full rollback available at every step
- No production systems affected

---

**Status**: Awaiting Phase 2 confirmation and Phase 3 approval

**Next Action**: User to confirm Phase 2 complete and approve Phase 3
