# TK-22 Copilot Instructions

## What This Repo Is

TK-22 is a **deterministic, fail-closed verdict engine** for Solana token safety analysis.

It answers one question: *Is this on-chain asset structurally safe to proceed with?*

If required facts are missing, unclear, or unverifiable — the system **fails closed**.  
There is no "probably safe." There is no "best guess." There is only **SAFE** or **FAIL_CLOSED**.

Read `ARCHITECTURE.md` and `REPO_CONTRACT.md` before making any changes.

---

## Critical Invariant — Never Break This

**Only `src/tk22/core/` may produce or influence a verdict.**

All other layers:
- supply data (`adapters/`)
- wire pipelines (`services/`)
- sequence tasks (`agent/`)
- expose results (`apis/`)
- explain results (`gen/`)
- provide pure helpers (`utils/`)

**They never decide.** If any layer outside `core/` contains logic that changes a verdict outcome, it is a bug.

---

## Layer Boundaries

| Layer | Purpose | May Decide? |
|---|---|---|
| `core/` | Deterministic policy evaluation, verdict generation | ✅ Only layer that may |
| `adapters/` | Fetch + normalize external data (Helius RPC) | ❌ |
| `models/` | Type definitions and structural schemas | ❌ |
| `services/` | Orchestrate data flow, prepare inputs for core | ❌ |
| `agent/` | Sequence scans, trigger adapters, deliver inputs | ❌ |
| `apis/` | HTTP/RPC transport, return core verdicts verbatim | ❌ |
| `gen/` | Human-facing explanations, LLM narrative output | ❌ |
| `utils/` | Pure helper functions, formatting | ❌ |

`core/` has no imports from any other layer. ESLint enforces this via `no-restricted-imports`.

---

## Verdict Types

```typescript
type Verdict = "SAFE" | "WARNING" | "FAIL_CLOSED";
```

- **`FAIL_CLOSED`** — Any structural risk detected or any required fact is missing.
- **`SAFE`** — All required facts present and within policy thresholds.
- **`WARNING`** — Optional intermediate state; defined in `core/policies.ts`.

### Fail-Closed Rules
- Missing data → `FAIL_CLOSED` (never default missing values to safe)
- `FAIL_CLOSED` cannot be downgraded by any layer above `core/`
- No retries until a pass — run once, return result

---

## Repository Structure

```
src/tk22/
  core/          # Verdict engine (isolated, no outside imports)
    types.ts     # ChainFacts, VerdictResult, Verdict types
    policies.ts  # Numeric thresholds (TOP_HOLDER_PERCENT, etc.)
    verdictEngine.ts  # evaluateToken(facts: ChainFacts): VerdictResult
  adapters/
    helius/      # Helius RPC client, returns ChainFacts
  apis/          # HTTP transport, returns core verdicts verbatim
  agent/         # Task coordination only
  services/      # Data pipeline wiring
  gen/           # Narrative/explanation output
  utils/         # Pure helpers

backend/         # Python agent/LLM services
frontend/        # UI (lovable prompts, states, copy)
automation/      # n8n workflows
integrations/    # External API connectors
ops/             # Deployment configs
agents/          # Agent definitions
docs/            # Documentation
```

---

## Code Conventions

### TypeScript (primary language for `src/tk22/`)
- TypeScript 5.4+, strict mode
- ESLint 8 with `@typescript-eslint` — run `npm run lint`
- Jest with `ts-jest` for tests — run `npm test`
- Build with `tsc` — run `npm run build`
- Explicit types on all function signatures
- No `any` except where unavoidable (add a comment explaining why)

```typescript
// Good: explicit types, named export, no side effects in core
export function evaluateToken(facts: ChainFacts): VerdictResult {
  const reasons: string[] = [];
  if (facts.mintAuthorityActive !== false) {
    reasons.push("Mint authority active or unknown");
  }
  // ...
}
```

### Python (used in `backend/`)
- Python 3.11+ with type hints on all functions
- Prefer f-strings over `.format()`
- Use `python-dotenv` — load env vars from `.env` only
- Use `requests` for HTTP calls
- Add docstrings to all functions

```python
def fetch_token_facts(mint: str) -> dict:
    """Fetch on-chain token facts from the Helius adapter."""
    response = requests.get(f"{HELIUS_URL}/token/{mint}", timeout=10)
    response.raise_for_status()
    return response.json()
```

---

## Security Rules

**NEVER:**
- Commit `.env`, API keys, or secrets to source control
- Use `eval()` or `exec()` on untrusted input
- Use `os.system()` or `subprocess` without explicit justification
- Default missing adapter data to a "safe" value — always fail closed
- Allow any layer above `core/` to override or reinterpret a `FAIL_CLOSED` verdict

**ALWAYS:**
- Load credentials from `.env` (see `.env.example` for required keys)
- Check `.agents/automation-author.md` before implementing multi-step automations
- Log all external API calls (Helius, LLM services)
- Handle rate limits gracefully (back-off, do not retry until pass)

---

## Testing

Tests live alongside their layer:
- `src/tk22/core/__tests__/` — golden/invariant tests for the verdict engine
- `src/tk22/apis/__tests__/` — verbatim contract tests for the API layer

**Key test invariant:** The fail-closed golden test in `core/__tests__/failClosed.golden.test.ts` must always pass. If it fails, core is broken.

When adding features to `core/`, add a corresponding golden test that proves FAIL_CLOSED behavior for missing/unknown inputs.

---

## Key Files

| File | Purpose |
|---|---|
| `ARCHITECTURE.md` | Layer model, invariants, design rules |
| `REPO_CONTRACT.md` | Folder naming rules, structural constraints |
| `.env.example` | Required environment variables |
| `src/tk22/core/policies.ts` | Numeric policy thresholds |
| `src/tk22/core/types.ts` | `ChainFacts`, `VerdictResult`, `Verdict` |
| `.eslintrc.js` | Import restrictions for `core/` isolation |

---

## Branch Strategy

- `main` — stable and production-safe; only reviewed merges
- `dev` — agents, experiments, controlled work in progress
