# TK-22 Minimal Control Runtime

## Overview

This directory contains the minimal control runtime that satisfies the TK-22 frontend contract.

The runtime performs **EVALUATION ONLY** - it does not execute integrations, trigger automations, or perform any side effects.

## Purpose

The control runtime exists to:
1. Accept input from the frontend
2. Evaluate risk based on mode (default/cautious/aggressive)
3. Return a single verdict: `SAFE_TO_PROCEED`, `ACTION_REQUIRED`, or `DO_NOT_PROCEED`
4. Respect frontend semantic constraints (evaluation ≠ execution)

## Files

### `api.py`

Flask API endpoint that implements POST /execute according to the frontend contract.

**Endpoint**: `POST /execute`

**Request**:
```json
{
  "input": "string | json",
  "mode": "default | cautious | aggressive",
  "source": "frontend"
}
```

**Response**:
```json
{
  "verdict": "SAFE_TO_PROCEED | ACTION_REQUIRED | DO_NOT_PROCEED",
  "summary": "human-readable explanation",
  "proof_id": "uuid-string"
}
```

**Current Behavior**: Returns SAFE_TO_PROCEED for all inputs (DEMO workspace mode).

### `tk22_execute.py`

Legacy execution script that writes proof records to control/proofs and control/memory.

**Note**: This script is from the earlier prototype phase. The api.py endpoint is the authoritative runtime implementation.

## Running the Runtime

### Requirements

```bash
pip install flask
```

### Start the API

```bash
python api.py
```

The API will run on `http://localhost:5000`

### Test the Endpoint

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "test payload",
    "mode": "default",
    "source": "frontend"
  }'
```

**Expected Response**:
```json
{
  "verdict": "SAFE_TO_PROCEED",
  "summary": "TK-22 found no blocking risk based on the provided input.",
  "proof_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Frontend Contract Compliance

This runtime strictly adheres to `docs/FRONTEND_CONTROL_CONTRACT.md`:

✅ **Accepts minimal input payload** (input, mode, source)  
✅ **Performs evaluation only** (no execution/integrations)  
✅ **Returns single verdict** with summary and proof_id  
✅ **Respects semantic constraints** ("Submit for Evaluation" means no execution)  
✅ **Terminal state** (every run ends with exactly one verdict)  

## Workspace State: DEMO

This runtime is configured for the DEMO workspace as defined in `docs/WORKSPACE_STATE.md`.

**DEMO mode behavior**:
- Always returns `SAFE_TO_PROCEED`
- No real risk assessment logic
- No integration with external systems
- Minimal logging (proof_id generation only)

**Promotion to LIVE** will require:
- Implementing actual risk evaluation logic
- Mode-based assessment (cautious vs aggressive)
- Integration with control/memory for state tracking
- Proper logging and audit trails

## Architecture

```
Frontend (Submit → Execute → Closure)
    ↓
    POST /execute
    ↓
control/runtime/api.py
    ↓
    Evaluation Logic (minimal)
    ↓
    {verdict, summary, proof_id}
    ↓
Frontend (displays verdict)
```

## Non-Goals (Explicit)

The control runtime does **NOT**:
- Choose agents
- Decide risk (currently hardcoded to SAFE)
- Execute integrations
- Store state long-term
- Trigger workflows
- Send notifications
- Perform any side effects

These capabilities will be added in future phases after the frontend contract is fully validated.

## Next Steps

1. Frontend integration testing with this endpoint
2. Validate three-screen flow (Submit → Execute → Closure)
3. Implement real evaluation logic (risk assessment)
4. Promote workspace from DEMO → LIVE
