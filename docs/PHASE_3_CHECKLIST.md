# Phase 3 Quick Checklist

**Goal**: Copy frontend files to thediscobass/tk-22-ui repository

---

## Pre-Flight Verification

Before starting Phase 3:

- [ ] Phase 2 complete (verify repos exist)
- [ ] https://github.com/thediscobass/tk-22-ui is accessible
- [ ] https://github.com/the-steele-zone/tk-22-experiments is accessible
- [ ] You have write access to thediscobass/tk-22-ui
- [ ] Approval received: "Approve Phase 3 — copy frontend files"

---

## Step 1: Prepare Working Directory

```bash
mkdir -p /tmp/tk-22-ui-migration
cd /tmp/tk-22-ui-migration
git clone https://github.com/thediscobass/tk-22-ui.git
cd tk-22-ui
```

- [ ] Temporary directory created
- [ ] Frontend repo cloned successfully

---

## Step 2: Copy Files

```bash
# Copy frontend files
cp -r /home/runner/work/tk-22/tk-22/frontend /tmp/tk-22-ui-migration/tk-22-ui/src

# Copy legal files
cp -r /home/runner/work/tk-22/tk-22/legal /tmp/tk-22-ui-migration/tk-22-ui/

# Copy contract
mkdir -p /tmp/tk-22-ui-migration/tk-22-ui/docs
cp /home/runner/work/tk-22/tk-22/docs/FRONTEND_CONTROL_CONTRACT.md /tmp/tk-22-ui-migration/tk-22-ui/docs/contract.md
```

- [ ] Frontend files copied to src/
- [ ] Legal files copied to legal/
- [ ] Contract copied to docs/contract.md

---

## Step 3: Create README.md

Create `/tmp/tk-22-ui-migration/tk-22-ui/README.md` with content from Phase 3 guide.

- [ ] README.md created
- [ ] Contains proper description and links

---

## Step 4: Create .gitignore

Create `/tmp/tk-22-ui-migration/tk-22-ui/.gitignore` with standard frontend ignores.

- [ ] .gitignore created

---

## Step 5: Commit and Push

```bash
cd /tmp/tk-22-ui-migration/tk-22-ui
git add .
git commit -m "Initial frontend migration from tk-22 control plane"
git push origin main
```

- [ ] All files added
- [ ] Commit created
- [ ] Pushed to main branch

---

## Step 6: Verify on GitHub

Visit https://github.com/thediscobass/tk-22-ui and check:

- [ ] README.md present
- [ ] src/ directory with frontend files
- [ ] legal/ directory present
- [ ] docs/contract.md present
- [ ] .gitignore present
- [ ] Commit history shows migration commit

---

## Step 7: Verify Original Unchanged

```bash
cd /home/runner/work/tk-22/tk-22
git status
```

- [ ] No uncommitted changes
- [ ] frontend/ directory still exists
- [ ] legal/ directory still exists
- [ ] Working tree clean

---

## Final Verification

- [ ] thediscobass/tk-22-ui has all required files
- [ ] crystalclearhouse-data/tk-22 unchanged
- [ ] No errors encountered
- [ ] All commits pushed successfully

---

## Cleanup (Optional)

```bash
rm -rf /tmp/tk-22-ui-migration
```

- [ ] Temporary directory cleaned up

---

## Report Completion

When done, report back:

**"Phase 3 complete — frontend copied successfully"**

Include:
- URL to migrated repo: https://github.com/thediscobass/tk-22-ui
- Any issues encountered: None / [describe]

---

## If Something Goes Wrong

**Rollback Steps:**
1. Delete content from thediscobass/tk-22-ui
2. Delete /tmp/tk-22-ui-migration
3. Start over from Step 1

**Original repo is NEVER modified, so rollback is safe.**

---

## Next Steps After Phase 3

After successful completion:
1. Update docs/REPO_SPLIT_STATUS.md
2. Review Phase 4 plan (removal from control plane)
3. Wait for Phase 4 approval (HIGH RISK phase)

**Do NOT proceed to Phase 4 without explicit approval.**

---

**Reference**: See `docs/PHASE_3_COPY_FRONTEND.md` for detailed instructions
