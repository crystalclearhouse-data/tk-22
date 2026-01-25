# Rule: Interaction Protocol

## The Protocol
Antigravity must never execute shell commands (`run_command`) directly. It must orchestrate them by providing copy-paste-ready blocks.

## Formatting Requirement
All shell commands must be presented in a block prefixed with:
**ANTIGRAVITY → EXECUTE**

## Rationale
This ensures user control, prevents accidental deletions, and maintains transparency.
