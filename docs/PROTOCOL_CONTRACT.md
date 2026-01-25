# Rule: Antigravity Interaction Protocol (Tell, Don't Run)

## Context
To ensure transparency, safety, and user control, Antigravity must never execute shell commands directly. Instead, it must provide them to the user for manual execution.

## The Rule
**Antigravity never runs commands directly.**

## Implementation
Whenever a shell command is needed:
1. Identify the exact command required.
2. Present the command in a dedicated code block.
3. Prefix the block with the header: **ANTIGRAVITY → EXECUTE**.

## Example
**ANTIGRAVITY → EXECUTE**
```bash
ls -la
```

## Exceptions
Non-destructive read-only commands (like `ls`, `cat`, `grep`) may be executed by Antigravity via its internal tools to gather context, but any command that modifies the file system, installs dependencies, or triggers external effects MUST follow this protocol.
