# Rule: Self-Locating Interaction Protocol

## The Protocol
Antigravity must never search for files or paths manually if they are mapped in `SYSTEM_MAP.json`.

## Resolution
When a component name is referenced (e.g. `dispatch_to_n8n`), Antigravity MUST:
1. Read `SYSTEM_MAP.json`.
2. Resolve the path via the map.
3. Perform the requested action at that path.

## The Rule
**Antigravity never guesses paths. It resolves organs.**

## Formatting
All shell commands must still be presented in a block prefixed with:
**ANTIGRAVITY → EXECUTE**
