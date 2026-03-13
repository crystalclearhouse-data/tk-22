import os
import json
from datetime import datetime, timezone
from backend import engine

def log_usage(api_key: str, endpoint: str):
    """
    Logs usage counts only.
    No payloads. No verdicts. No facts.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "api_key": api_key,
        "endpoint": endpoint,
        "type": "usage_metric"
    }
    # In a real system, this goes to a DB or metric service.
    # For now, we log to stdout cleanly for the operator/n8n to consume.
    print(f"METRIC: {json.dumps(entry)}")

def scan_with_auth(context: dict) -> dict:
    """
    Wrapper around engine.run_cycle.
    Enforces Authentication and Logging.
    """
    api_key = context.get("api_key")

    if not api_key:
        raise PermissionError("UNAUTHORIZED: Missing API Key")

    # Log the attempt (billed unit)
    log_usage(api_key, "scan")

    # Pass through to core (No mutation of logic) with sanitized context
    sanitized_context = dict(context)
    sanitized_context.pop("api_key", None)
    return engine.run_cycle(sanitized_context)
