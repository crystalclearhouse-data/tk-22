# TK22 Architecture Contract (Fail-Closed by Design)

## What TK22 Is
TK22 is a **deterministic safety and verdict engine**.

It exists to answer one question only:

> **Is this asset safe to proceed with, based on hard rules and available facts?**

If required facts are missing, unclear, or unverifiable, the system **fails closed**.

There is no "probably safe."
There is no "best guess."
There is only **PASS** or **FAIL**.

---

## Core Invariant (Non-Negotiable)

**Only the Core layer may produce or influence a verdict.**

All other layers:
- supply data
- move data
- explain data
- expose data

They **never decide**.

If this invariant is broken, TK22 is broken.

---

## Layer Model (Bottom → Top)

### 1. `core/` — Verdict Authority
**The only decision-making layer.**

Responsibilities:
- Deterministic policy evaluation
- Fail-closed verdict generation
- Threshold enforcement
- Explicit PASS / FAIL outcomes

Rules:
- No network calls
- No adapters
- No agents
- No services
- No APIs
- No LLMs
- Pure, deterministic logic only

If required inputs are missing → **FAIL**.

---

### 2. `adapters/` — External Data Boundary
**Untrusted data acquisition.**

Responsibilities:
- Fetch data from external systems (Helius, RPCs, APIs)
- Normalize raw responses into known shapes

Rules:
- NEVER decide
- NEVER infer
- NEVER default missing data to "safe"
- Allowed to return `null`, `undefined`, or partial data

Adapters are allowed to be wrong.  
Core is not.

---

### 3. `models/` — Structural Definitions
**Data shape, not meaning.**

Responsibilities:
- Type definitions
- Schemas
- Structural validation

Rules:
- No business logic
- No defaults that imply safety
- No derived values that change meaning
- Validation ≠ approval

Models describe *form*, never *truth*.

---

### 4. `services/` — Wiring & Pipelines
⚠️ **High-risk layer — strictly constrained**

Responsibilities:
- Orchestrate data flow
- Combine adapter outputs
- Prepare inputs for Core

Rules:
- NO decisions
- NO retries unless Core explicitly requests
- NO conditional logic that alters outcomes
- NO fallback behavior

If a service contains logic that could change a verdict, it is violating the architecture.

Think of this layer as **plumbing, not judgment**.

---

### 5. `agent/` — Automation & Execution
**Task coordination only.**

Responsibilities:
- Sequence scans
- Trigger adapters
- Call services
- Deliver inputs to Core

Rules:
- Cannot override Core verdicts
- Cannot soften failures
- Cannot "retry until pass"
- Cannot introduce heuristics

Agents execute instructions.  
They do not reason about safety.

---

### 6. `apis/` — Transport Layer
**Exposure, not interpretation.**

Responsibilities:
- HTTP / RPC / CLI interfaces
- Input validation
- Output serialization

Rules:
- Must return Core verdicts verbatim
- No conditional branching on verdict meaning
- No UX-driven softening of FAIL
- No alternate success paths

APIs reflect reality.  
They do not reshape it.

---

### 7. `gen/` — Narrative & Explanation
**Human-facing output only.**

Responsibilities:
- Explanations
- Summaries
- LLM-generated descriptions
- UI copy

Rules:
- NEVER emit verdicts
- NEVER influence decisions
- NEVER modify inputs
- Reads verdicts, does not write them

Gen explains what happened.  
It does not change what happened.

---

### 8. `utils/` — Pure Helpers
**Danger zone if abused.**

Responsibilities:
- Small, pure helper functions
- Formatting
- Non-semantic transformations

Rules:
- No retries
- No error masking
- No default substitution
- No "safe" wrappers

If a utility changes behavior in a failure case, it does not belong here.

---

## Architectural Enforcement Rules

- Verdicts originate in **one place only**
- Missing data → **FAIL**
- FAIL cannot be downgraded
- No layer above Core may reinterpret safety
- "Uncertain" is not a valid state

If a future change violates these rules:
- It is a bug
- It is not a feature
- It must be reverted

---

## Design Philosophy (Plain English)

TK22 is not trying to be smart.

It is trying to be **correct**.

Intelligence is allowed above the verdict.  
Judgment is allowed only at the core.

This is how you build trust.
This is how you prevent silent failure.
This is how you ship something people will pay for.
