import json
from datetime import datetime, timezone
from pathlib import Path

print("TK-22 EXECUTION STARTED")

BASE = Path("control")
PROOFS = BASE / "proofs"
MEMORY = BASE / "memory"

PROOFS.mkdir(parents=True, exist_ok=True)
MEMORY.mkdir(parents=True, exist_ok=True)

proof = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "status": "EXECUTED",
    "message": "TK-22 control layer execution successful"
}

with open(PROOFS / "latest_proof.json", "w") as f:
    json.dump(proof, f, indent=2)

memory_file = MEMORY / "memory.json"

if memory_file.exists():
    memory = json.loads(memory_file.read_text())
else:
    memory = []

memory.append(proof)
memory_file.write_text(json.dumps(memory, indent=2))

print("TK-22 EXECUTION COMPLETE")
