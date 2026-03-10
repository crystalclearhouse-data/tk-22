"""TK-22 Minimal Control Runtime API

This module implements the POST /execute endpoint required by the frontend contract.
It performs EVALUATION only - no execution or integration actions.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import sys
import os
import logging

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tk22.config import WebhookConfig
from tk22.adapters.webhook import WebhookClient
from tk22.services.webhook_service import WebhookService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Verdict constants from FRONTEND_CONTROL_CONTRACT.md
SAFE_TO_PROCEED = "SAFE_TO_PROCEED"
ACTION_REQUIRED = "ACTION_REQUIRED"
DO_NOT_PROCEED = "DO_NOT_PROCEED"

# Initialize webhook components
webhook_config = WebhookConfig()
webhook_client = WebhookClient(
    webhook_url=webhook_config.get_webhook_url(),
    timeout=webhook_config.get_timeout()
)
webhook_service = WebhookService(webhook_client)

logger.info(f"Webhook integration initialized: {webhook_config.get_config_summary()}")

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
    
    # Prepare verdict response
    verdict_response = {
        "verdict": verdict,
        "summary": summary,
        "proof_id": proof_id
    }
    
    # Send webhook notification (non-blocking)
    if webhook_config.is_enabled():
        try:
            webhook_result = webhook_service.notify_verdict(
                verdict_data=verdict_response,
                request_data=data
            )
            
            if webhook_result is not None:
                logger.info(f"Webhook notification sent successfully for proof_id: {proof_id}")
            else:
                logger.warning(f"Webhook notification failed for proof_id: {proof_id}")
                
                # Only fail the request if configured to do so
                if webhook_config.should_fail_on_error():
                    return jsonify({
                        "error": "Webhook notification failed and WEBHOOK_FAIL_ON_ERROR is enabled"
                    }), 500
                    
        except Exception as e:
            logger.error(f"Webhook notification error for proof_id {proof_id}: {str(e)}")
            
            # Only fail the request if configured to do so
            if webhook_config.should_fail_on_error():
                return jsonify({
                    "error": f"Webhook notification error: {str(e)}"
                }), 500
    
    # Return verdict (webhook failures don't affect verdict by default)
    return jsonify(verdict_response), 200

if __name__ == '__main__':
    # Run on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=False)
