# Multi-Repo Boundary Plan for TK-22 System

**Date**: 2026-02-03  
**Status**: Planning Only - No Changes Made  
**Purpose**: Define repository boundaries for splitting across three GitHub accounts

---

## Executive Summary

This document provides a **deterministic plan** for organizing the TK-22 system across three separate GitHub accounts, based on the repository's existing architecture and constraints.

**Three GitHub Accounts:**
1. **CrystalClearHouse** (crystalclearhouse-data) — agents, infrastructure, rules
2. **thediscobass** — public brand, website, chat widget
3. **the-steele-zone** — personal / consulting / experiments

**Key Constraint**: These accounts have **separate ownership**. No shared write access. No cross-account assumptions.

---

## 1. Repo Boundary Definitions

### 1.1 crystalclearhouse-data/tk-22 (Control Plane) ✅ CURRENT REPO

**What it is:**
- The authoritative control plane for the TK-22 system
- Deterministic safety and verdict engine
- Agent definitions and automation orchestration
- Internal infrastructure and rules

**What stays here:**
- `/src/tk22/` — Core verdict engine (adapters, agent, apis, core, gen, models, services, utils)
- `/agents/` — Agent definitions and constraints
- `/automation/` — Automation scripts and pipelines
- `/control/` — Runtime control and execution logic
- `/backend/` — LLM scoring, agent prompts, internal logic
- `/ops/` — Deployment, runbooks, environment configs
- `/reports/` — Internal reporting schemas and templates
- `/.agents/` — Agent instruction files (automation-author.md, etc.)
- `/.github/` — GitHub workflows and CI/CD for this repo
- `/.vscode/` — VS Code configurations for development
- `/docs/` — Architecture, contracts, workspace state
- `ARCHITECTURE.md` — System architecture contract
- `REPO_CONTRACT.md` — Repository rules and constraints
- `README.md` — Control plane documentation

**Repository Type**: Private  
**Authority**: Verdict generation, agent orchestration, internal automation  
**Who Can Modify**: CrystalClearHouse team only

---

### 1.2 thediscobass/tk-22-ui (Public Frontend) 🆕 NEW REPO

**What it is:**
- Public-facing brand website
- User onboarding interface
- Presentation layer for TK-22 evaluation requests
- Chat widget / demo interface

**What moves here:**
- `/frontend/` → `/src/` or root (lovable_prompt.md, ui_copy.md, states.md)
- `/legal/` → `/legal/` (privacy.md, terms.md, disclaimer.md)
- `/docs/FRONTEND_CONTROL_CONTRACT.md` → `/docs/contract.md`
- Frontend-specific README and setup instructions

**What it does NOT contain:**
- No verdict logic
- No agent definitions
- No automation scripts
- No infrastructure configurations
- No internal contracts

**Repository Type**: Public or Private (but public-facing)  
**Authority**: User interface, presentation, public brand  
**Who Can Modify**: thediscobass team

**Integration Point**:
- Frontend calls `POST /execute` to crystalclearhouse-data/tk-22 control plane
- Frontend receives verdict responses (SAFE_TO_PROCEED, ACTION_REQUIRED, DO_NOT_PROCEED)
- Frontend displays state updates (RECEIVED, RUNNING, BLOCKED, COMPLETE)

---

### 1.3 the-steele-zone/tk-22-experiments (Personal / R&D) 🆕 NEW REPO

**What it is:**
- Personal consulting work
- Experimental features
- Proof-of-concept implementations
- Non-production testing

**What could go here:**
- Experimental integrations not ready for production
- Personal automation scripts
- Research notes and exploratory documentation
- Test implementations of new features

**What it does NOT contain:**
- No production code
- No customer-facing features
- No verdict authority
- No live automation

**Repository Type**: Private  
**Authority**: Experimentation only, no production impact  
**Who Can Modify**: the-steele-zone owner only

**Integration Point**:
- May read from public APIs of tk-22 if available
- No write access to production systems
- Results may be promoted to crystalclearhouse-data/tk-22 after review

---

### 1.4 Potential Future Repo: Integration Adapters (Optional)

**What it could be:**
- Shared integration libraries (Stripe, ClickUp, blockchain adapters)
- Published as NPM/PyPI packages
- Consumed by both tk-22 and tk-22-ui

**What would move here:**
- `/integrations/` → separate package repo
- Each integration as a standalone, versioned module

**Decision**: Not required immediately. Keep in tk-22 for now until integrations stabilize.

---

## 2. What Must NEVER Cross Repo Boundaries

### 2.1 Hard Boundaries (Violations Break Security)

❌ **NEVER share these across repos:**
1. **Secrets and Credentials**
   - `.env` files
   - API keys
   - Private keys
   - Database credentials
   - Service tokens

2. **Verdict Authority**
   - Only `crystalclearhouse-data/tk-22/src/tk22/core/` may produce verdicts
   - Frontend repos cannot override or soften FAIL states
   - No heuristics or "probably safe" logic in presentation layers

3. **Agent Definitions**
   - Only `crystalclearhouse-data/tk-22/agents/` and `/.agents/` define agent capabilities
   - No agent logic in frontend repos
   - No cross-repo agent execution

4. **Infrastructure Configuration**
   - Deployment configs stay in `crystalclearhouse-data/tk-22/ops/`
   - No production configs in public repos
   - No environment-specific secrets in any repo

### 2.2 Architectural Boundaries (Violations Break Trust)

❌ **NEVER allow these patterns:**
1. **Frontend Deciding Safety**
   - Frontend displays verdicts, never interprets them
   - No conditional logic that changes PASS/FAIL meaning
   - No UX-driven softening of failures

2. **Shared State Without Contract**
   - All communication via documented APIs
   - No direct database access from frontend
   - No shared file system assumptions

3. **Cross-Account Write Access**
   - Each repo owned by one account
   - No commits from other accounts without explicit PR review
   - No automated cross-repo modifications

### 2.3 Data Flow Boundaries

✅ **Allowed flows:**
- Frontend → Control Plane: POST /execute with user input
- Control Plane → Frontend: Verdict responses and state updates
- Experiments → Control Plane: Read-only API calls (if public API exists)

❌ **Forbidden flows:**
- Frontend → Direct database access
- Experiments → Production infrastructure modifications
- Any repo → Another repo's secrets or credentials

---

## 3. Safe Execution Order for Splitting and Pushing

### Phase 1: Preparation (Zero Risk)
**Goal**: Understand current state, no changes yet

✅ **Steps:**
1. Document current file structure (this document)
2. Identify all external dependencies (package.json, requirements.txt, etc.)
3. Map all integration points between components
4. Review all existing remotes and branches
5. **Checkpoint**: Confirm plan with stakeholders

**Risk Level**: None (read-only analysis)

---

### Phase 2: Create Empty Target Repos (Low Risk)
**Goal**: Set up new repositories without moving code

✅ **Steps:**
1. Create `thediscobass/tk-22-ui` repository on GitHub (empty, with README.md only)
2. Create `the-steele-zone/tk-22-experiments` repository on GitHub (empty, with README.md only)
3. Configure repository settings:
   - Set visibility (public vs private)
   - Disable force pushes
   - Set up branch protection on `main`
4. **Checkpoint**: Confirm repos exist and are accessible

**Risk Level**: Low (no code moved yet)

---

### Phase 3: Copy Frontend to thediscobass/tk-22-ui (Medium Risk)
**Goal**: Move frontend files without breaking history

✅ **Steps:**
1. In `crystalclearhouse-data/tk-22`, create a new branch: `prepare-frontend-split`
2. Copy (not move) frontend files to a temporary directory:
   ```bash
   mkdir /tmp/tk-22-ui
   cp -r /home/runner/work/tk-22/tk-22/frontend/* /tmp/tk-22-ui/
   cp -r /home/runner/work/tk-22/tk-22/legal /tmp/tk-22-ui/
   cp /home/runner/work/tk-22/tk-22/docs/FRONTEND_CONTROL_CONTRACT.md /tmp/tk-22-ui/docs/
   ```
3. Create new README.md for frontend repo
4. Initialize git in `/tmp/tk-22-ui`:
   ```bash
   cd /tmp/tk-22-ui
   git init
   git add .
   git commit -m "Initial frontend commit from tk-22"
   ```
5. Add remote and push:
   ```bash
   git remote add origin https://github.com/thediscobass/tk-22-ui
   git branch -M main
   git push -u origin main
   ```
6. **Checkpoint**: Verify frontend repo looks correct on GitHub

**Risk Level**: Medium (creates new repo, but doesn't modify original)

---

### Phase 4: Remove Frontend from crystalclearhouse-data/tk-22 (High Risk - CAREFUL)
**Goal**: Clean up control plane repo after successful frontend move

⚠️ **Prerequisites:**
- Phase 3 completed successfully
- Frontend repo verified working
- All team members notified

✅ **Steps:**
1. In `crystalclearhouse-data/tk-22`, create branch: `remove-frontend-files`
2. Remove frontend directories:
   ```bash
   git rm -r frontend/
   git rm -r legal/
   git rm docs/FRONTEND_CONTROL_CONTRACT.md
   ```
3. Update README.md to reference the new frontend repo
4. Update ARCHITECTURE.md to note frontend is now separate
5. Commit changes:
   ```bash
   git commit -m "Move frontend to thediscobass/tk-22-ui"
   ```
6. Create PR for review
7. After approval, merge to main
8. **Checkpoint**: Confirm control plane still works without frontend

**Risk Level**: High (modifies production repo)

**Rollback Plan**: 
- Keep `prepare-frontend-split` branch until Phase 5 complete
- Can restore files from that branch if needed

---

### Phase 5: Set Up Experiments Repo (Low Risk)
**Goal**: Create personal experiments space

✅ **Steps:**
1. In `the-steele-zone/tk-22-experiments`, add README.md:
   ```markdown
   # TK-22 Experiments
   
   Personal experiments and proof-of-concept work.
   
   **Not for production use.**
   ```
2. Add basic .gitignore
3. Add LICENSE if desired
4. Commit and push:
   ```bash
   git add .
   git commit -m "Initial experiments repo setup"
   git push origin main
   ```
5. **Checkpoint**: Experiments repo ready for use

**Risk Level**: Low (doesn't affect production)

---

### Phase 6: Document Integration Points (Zero Risk)
**Goal**: Ensure teams know how to communicate

✅ **Steps:**
1. In `crystalclearhouse-data/tk-22`, update README.md with:
   - Link to frontend repo
   - API endpoints for frontend integration
   - Contact information for coordination
2. In `thediscobass/tk-22-ui`, update README.md with:
   - Link to control plane repo
   - API endpoints to call
   - Contract reference (FRONTEND_CONTROL_CONTRACT.md)
3. In `the-steele-zone/tk-22-experiments`, update README.md with:
   - Links to both production repos
   - Note: "Read-only access to production APIs"
4. **Checkpoint**: All repos have clear documentation

**Risk Level**: None (documentation only)

---

### Phase 7: Update CI/CD and Automation (Medium Risk)
**Goal**: Ensure automated systems work with new structure

✅ **Steps:**
1. In `crystalclearhouse-data/tk-22`:
   - Review `.github/workflows/` for any frontend-specific jobs
   - Remove or update those workflows
   - Ensure backend/core tests still run
2. In `thediscobass/tk-22-ui`:
   - Create new `.github/workflows/` for frontend tests
   - Set up deployment pipeline (Vercel, Netlify, etc.)
   - Configure environment variables (no secrets in repo)
3. In `the-steele-zone/tk-22-experiments`:
   - Optional: Add basic CI for linting
   - No deployment pipeline (experiments only)
4. **Checkpoint**: All CI/CD pipelines working

**Risk Level**: Medium (affects automation)

---

## 4. Folder Ownership Matrix

| Folder/File | crystalclearhouse-data/tk-22 | thediscobass/tk-22-ui | the-steele-zone/tk-22-experiments |
|-------------|------------------------------|------------------------|-----------------------------------|
| `/src/tk22/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/agents/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/automation/` | ✅ OWNS | ❌ Never | 🔄 May copy for experiments |
| `/control/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/backend/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/ops/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/reports/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/.agents/` | ✅ OWNS | ❌ Never | ❌ Never |
| `/frontend/` | 🔄 Remove after Phase 4 | ✅ OWNS (moved here) | ❌ Never |
| `/legal/` | 🔄 Remove after Phase 4 | ✅ OWNS (moved here) | ❌ Never |
| `/integrations/` | ✅ OWNS (for now) | ❌ Never | 🔄 May copy for experiments |
| `/docs/` | ✅ OWNS (internal) | ✅ OWNS (frontend-specific) | ✅ OWNS (experiments) |
| `ARCHITECTURE.md` | ✅ OWNS | ❌ Never | 📖 Reference only |
| `REPO_CONTRACT.md` | ✅ OWNS | ❌ Never | 📖 Reference only |

**Legend:**
- ✅ OWNS: This repo has write authority
- ❌ Never: Must not exist in this repo
- 🔄 May copy: Can copy for reference, not authoritative
- 📖 Reference only: May read, never modify

---

## 5. Post-Split Governance

### 5.1 Decision Authority

**Who decides what:**
1. **Verdict Logic**: CrystalClearHouse only
2. **Frontend UX**: thediscobass only
3. **Experiments**: the-steele-zone only
4. **Contracts (API between systems)**: Both CrystalClearHouse and thediscobass must agree

### 5.2 Change Approval Process

**For crystalclearhouse-data/tk-22:**
- All changes via PR
- Review required before merge to main
- No direct commits to main

**For thediscobass/tk-22-ui:**
- Owner has final say on UX decisions
- Must respect FRONTEND_CONTROL_CONTRACT.md
- Cannot violate API contract without coordination

**For the-steele-zone/tk-22-experiments:**
- Owner has full control
- No production impact
- May propose changes to production repos via PR

### 5.3 Breaking Changes Protocol

If a breaking change is needed:
1. Propose change in both affected repos
2. Update contract documentation
3. Implement in controlled order:
   - First: Update receiver (e.g., backend API)
   - Then: Update sender (e.g., frontend)
4. Never break existing integrations without migration plan

---

## 6. Risk Assessment

### Low Risk Items
- Creating new empty repos
- Copying files for reference
- Documentation updates
- Read-only analysis

### Medium Risk Items
- Moving frontend files to new repo
- Updating CI/CD configurations
- Removing files from control plane repo (with good backup)

### High Risk Items
- Deleting files without verification
- Changing core verdict logic
- Modifying secrets management
- Cross-account credential sharing

### Unacceptable Risk (NEVER DO)
- Force pushing to production branches
- Sharing secrets across repos
- Giving write access to all repos to one person
- Modifying core/ logic in frontend repos
- Auto-merging PRs that affect repo boundaries

---

## 7. Rollback Strategy

**If Phase 3 (move frontend) fails:**
- Frontend files still exist in crystalclearhouse-data/tk-22
- Delete thediscobass/tk-22-ui and start over
- No impact on production

**If Phase 4 (remove from control plane) fails:**
- Restore from `prepare-frontend-split` branch
- Frontend code available in both repos temporarily (not ideal, but safe)
- Fix issues in thediscobass/tk-22-ui, then retry Phase 4

**If CI/CD breaks:**
- Each repo has independent CI/CD
- Failure in one repo doesn't affect others
- Roll back changes to `.github/workflows/` in affected repo

---

## 8. Success Criteria

**Phase completion criteria:**
- [ ] Phase 1: This document reviewed and approved
- [ ] Phase 2: All target repos exist on GitHub
- [ ] Phase 3: Frontend code running in thediscobass/tk-22-ui
- [ ] Phase 4: Frontend removed from crystalclearhouse-data/tk-22, control plane still works
- [ ] Phase 5: Experiments repo initialized
- [ ] Phase 6: All READMEs updated with integration instructions
- [ ] Phase 7: CI/CD working in all repos

**Overall success:**
- ✅ All repos have clear ownership
- ✅ No secrets shared across repos
- ✅ No cross-account write assumptions
- ✅ Frontend can call control plane API
- ✅ Control plane produces verdicts independently
- ✅ Documentation reflects new structure
- ✅ Team understands boundaries and communication paths

---

## 9. Next Steps (After This Planning Document)

**DO NOT proceed without:**
1. Review of this document by all stakeholders
2. Confirmation of GitHub account access for all three accounts
3. Backup of current repository state
4. Communication to team about upcoming changes

**When ready to execute:**
1. Start with Phase 1 (already complete - this document)
2. Proceed to Phase 2 only after approval
3. Execute phases sequentially, validating at each checkpoint
4. Stop immediately if any phase fails validation
5. Document any deviations from this plan

---

## 10. Constraints Honored

This plan respects the following constraints from the problem statement:

✅ **Do NOT modify files** — This is a planning document only  
✅ **Do NOT create commits** — No code changes in this task  
✅ **Do NOT assume shared GitHub ownership** — Each repo owned by one account  
✅ **Output markdown only** — This entire document is markdown  

✅ **Deliverables provided:**
1. ✅ Clear repo boundary definition (Section 1)
2. ✅ Which folders belong in which repo (Section 4)
3. ✅ What must never cross repo boundaries (Section 2)
4. ✅ Safe execution order for splitting and pushing (Section 3)

---

## Conclusion

This plan provides a **deterministic, safe path** for splitting the TK-22 system across three GitHub accounts while maintaining:
- Clear ownership boundaries
- Security (no shared secrets)
- Architectural integrity (verdict authority stays in control plane)
- Rollback capability at every phase
- Team coordination and communication

**Status**: Ready for review  
**No commits made**: This document is the only output  
**No files changed**: Analysis only

---

**Ready for review and stakeholder approval.**
