# Frontend → Control Contract (TK-22)

This document defines the binding contract between the TK-22 frontend
and the control/runtime layer.

The frontend is authoritative on:

- User intent
- Input payload
- When execution begins

The control layer is authoritative on:

- Validation
- Agent execution
- Final closure verdict

---

## 1. Entry Point

The frontend will call a single endpoint:

POST /execute

This endpoint replaces the current mock API.

---

## 2. Input Payload (Minimum)

```json
{
  "input": "string | json",
  "mode": "default | cautious | aggressive",
  "source": "frontend"
}
```

Notes:

- input is opaque to the frontend
- Control decides how it is interpreted
- Frontend does not validate business logic

---

## 3. Execution Lifecycle

Control responds with execution state updates:

- RECEIVED
- RUNNING
- BLOCKED (if human action required)
- COMPLETE

The frontend only displays these states.

---

## 4. Closure Output (Required)

Every execution MUST end with exactly one verdict:

```json
{
  "verdict": "SAFE_TO_PROCEED | ACTION_REQUIRED | DO_NOT_PROCEED",
  "summary": "human-readable explanation",
  "proof_id": "string"
}
```

- No execution may end without a verdict
- The frontend treats this as terminal
- Human disengagement is expected after closure

---

## 5. Non-Goals (Explicit)

The frontend does NOT:

- Choose agents
- Decide risk
- Execute integrations
- Store state long-term

The control layer does NOT:

- Care about UI
- Manage layout or presentation

---

## Frontend Language as Control Constraint

Frontend copy intentionally avoids action-oriented language.

Implications:

- "Submit for Evaluation" means no execution occurs at submission.
- "Evaluation in Progress" implies analysis only.
- "Decision Complete" implies terminal state.

The control layer must respect these semantic constraints.
Any execution beyond evaluation requires an explicit future phase.
This prevents future confusion or scope creep.
