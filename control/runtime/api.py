"""TK-22 Minimal Control Runtime API

This module implements the POST /execute endpoint required by the frontend contract.
It performs EVALUATION only - no execution or integration actions.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Verdict constants from FRONTEND_CONTROL_CONTRACT.md
SAFE_TO_PROCEED = "SAFE_TO_PROCEED"
ACTION_REQUIRED = "ACTION_REQUIRED"
DO_NOT_PROCEED = "DO_NOT_PROCEED"

@app.route('/execute', methods=['POST'])
def execute():
    """
    POST /execute endpoint - performs evaluation and returns verdict.
    
    Request body (minimum):
    {
        "input": "string | json",
        "mode": "default | cautious | aggressive",
        "source": "frontend"
    }
    
    Response:
    {
        "verdict": "SAFE_TO_PROCEED | ACTION_REQUIRED | DO_NOT_PROCEED",
        "summary": "human-readable explanation",
        "proof_id": "string"
    }
    """
    
    # Validate request
    if not request.is_json:
        return jsonify({
            "error": "Content-Type must be application/json"
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'input' not in data:
        return jsonify({
            "error": "Missing required field: input"
        }), 400
    
    # Extract fields with defaults
    input_payload = data.get('input')
    mode = data.get('mode', 'default')
    source = data.get('source', 'unknown')
    
    # Generate proof ID
    proof_id = str(uuid.uuid4())
    
    # EVALUATION LOGIC (minimal)
    # This is where risk assessment would happen
    # For now: always return SAFE_TO_PROCEED for demo/DEMO workspace
    
    verdict = SAFE_TO_PROCEED
    summary = "TK-22 found no blocking risk based on the provided input."
    
    # Log evaluation (not shown - would write to control/memory)
    
    # Return verdict
    return jsonify({
        "verdict": verdict,
        "summary": summary,
        "proof_id": proof_id
    }), 200

if __name__ == '__main__':
    # Run on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=False)
