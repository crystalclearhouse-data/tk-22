#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone
import sys
import os

ROOT = Path(__file__).resolve().parents[2]
PROOFS = ROOT / "control/proofs"

def ts():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def git(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None

def scan():
    checks = []
    hard = soft = 0

    required_dirs = [
        "control",
        "control/memory",
        "control/proofs",
        "control/runtime",
        ".github/workflows",
    ]

    for d in required_dirs:
        if (ROOT / d).is_dir():
            checks.append({"id": d, "status": "PASS"})
        else:
            checks.append({"id": d, "status": "FAIL_HARD"})
            hard += 1

    if not (ROOT / "control/runtime/tk22_execute.py").is_file():
        checks.append({"id": "tk22_execute.py", "status": "FAIL_HARD"})
        hard += 1

    if (ROOT / ".env").exists():
        checks.append({"id": ".env", "status": "FAIL_HARD"})
        hard += 1

    for f in ["README.md", ".gitignore", ".env.example"]:
        if not (ROOT / f).exists():
            checks.append({"id": f, "status": "FAIL_SOFT"})
            soft += 1

    status = "PASS" if hard == 0 and soft == 0 else "FAIL_HARD" if hard else "FAIL_SOFT"
    code = 0 if status == "PASS" else 10 if hard else 20

    PROOFS.mkdir(parents=True, exist_ok=True)
    proof = {
        "timestamp": ts(),
        "status": status,
        "exit_code": code,
        "checks": checks,
        "git": {
            "branch": git(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
            "commit": git(["git", "rev-parse", "HEAD"]),
        },
    }

    (PROOFS / "tk22_scan_latest.json").write_text(json.dumps(proof, indent=2))
    (PROOFS / f"tk22_scan_{ts()}.json").write_text(json.dumps(proof, indent=2))

    return code

# Ensure we can import from backend
sys.path.append(str(ROOT))

try:
    from backend import api_wrapper
except ImportError as e:
    print(f"CRITICAL: Could not import backend api_wrapper. {e}")
    exit(30)

def execute():
    # Gather context
    api_key = os.environ.get("TK22_API_KEY")

    context = {
        "trigger": "manual_scan",
        "timestamp": ts(),
        "api_key": api_key
    }

    try:
        # Call the Brain via Auth Wrapper
        result = api_wrapper.scan_with_auth(context)

        # Enriched proof
        proof = {
            "meta": {
                "type": "execution_proof",
                "timestamp": ts(),
                "status": "EXECUTED"
            },
            "payload": result
        }

        # Write to proofs
        (PROOFS / f"tk22_execute_{ts()}.json").write_text(json.dumps(proof, indent=2))
        return 0

    except PermissionError as e:
        print(f"AUTH FAILURE: {e}")
        return 401
    except Exception as e:
        print(f"EXECUTION FAILURE: {e}")
        return 30

if __name__ == "__main__":
    scan_code = scan()
    if scan_code == 0:
        exec_code = execute()
        exit(exec_code)
    else:
        print(f"Scan failed with code {scan_code}. Execution aborted.")
        exit(scan_code)
