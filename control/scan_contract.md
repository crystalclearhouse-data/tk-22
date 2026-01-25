# TK-22 Scan Contract (v1)

TK-22 is a gatekeeper. It scans reality, decides readiness, then executes.

## Required (Hard Fail if missing)
- control/
- control/memory/
- control/proofs/
- control/runtime/
- control/runtime/tk22_execute.py
- .github/workflows/

## Soft Requirements
- README.md
- .gitignore
- .env.example
- .github/workflows/tk22_execute.yml

## Forbidden
- .env committed to repo
- .env.* files except .env.example

## Outputs
- control/proofs/tk22_scan_latest.json
- control/proofs/tk22_scan_<timestamp>.json

Exit Codes:
- 0 = PASS
- 10 = FAIL_HARD
- 20 = FAIL_SOFT
- 30 = ERROR
