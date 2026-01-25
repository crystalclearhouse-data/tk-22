# LOCK-IN MODE (CANONICAL)

When this mode is active, the agent MUST obey the following rules:

## EXECUTION RULES
1. Once `git status` has been run successfully, the current working directory is authoritative.
2. Do NOT suggest `cd`, alternate roots, or submodule-prefixed paths.
3. Provide ONE command per step.
4. Never present fallback or alternative command blocks.
5. Never repeat steps already completed.
6. Never advance steps without explicit confirmation.

## SUBMODULE RULES
1. If a path belongs to a submodule, Antigravity MUST guide a separate commit inside that submodule directory FIRST.
2. Only after the submodule is pushed to remote can the parent repository update its pointer.
3. Never mix submodule file staging with parent repository staging.

## STAGING RULES
- Only stage files explicitly listed as canonical.
- Never stage `.env.local`, `node_modules`, or secrets.
- If a file is untracked, guide staging — do not reframe architecture.

## COMMUNICATION RULES
- Guidance is mandatory.
- Silence is allowed only after verification success.
- If ambiguity is detected, ask ONE clarifying question, then pause.

## EXIT CONDITIONS
This mode exits only when:
- `git status` shows: `nothing to commit, working tree clean`
- User explicitly confirms completion.

Violations of this protocol are errors.
