"""
Flask-based webhook receiver for GitHub Actions job events.

This service receives GitHub Actions job events and forwards them to n8n
for automated processing and notifications. Useful for local testing before
deploying to production.
"""

import os
from typing import Dict, Any, Tuple
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configuration from environment variables
N8N_HOST = os.getenv('N8N_HOST', 'http://localhost:5678')
N8N_WEBHOOK_PATH = os.getenv('N8N_WEBHOOK_PATH', '/webhook/github-jobs')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '5000'))


def forward_to_n8n(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """
    Forward the GitHub job event payload to n8n webhook.
    
    Args:
        payload: The GitHub job event data as a dictionary
        
    Returns:
        Tuple of (response_data, status_code)
    """
    n8n_url = f"{N8N_HOST}{N8N_WEBHOOK_PATH}"
    
    try:
        app.logger.info(f"Forwarding payload to n8n: {n8n_url}")
        
        # Forward to n8n with proper headers
        response = requests.post(
            n8n_url,
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'TK-22-Webhook-Receiver'
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        app.logger.info(f"Successfully forwarded to n8n (status: {response.status_code})")
        
        # Return n8n's response
        return response.json() if response.content else {"status": "success"}, response.status_code
        
    except requests.exceptions.Timeout:
        app.logger.error("Timeout while forwarding to n8n")
        return {"error": "Timeout connecting to n8n"}, 504
        
    except requests.exceptions.ConnectionError as e:
        app.logger.error(f"Connection error to n8n: {str(e)}")
        return {"error": f"Cannot connect to n8n at {n8n_url}"}, 503
        
    except requests.exceptions.HTTPError as e:
        app.logger.error(f"HTTP error from n8n: {str(e)}")
        return {"error": f"n8n returned error: {e.response.status_code}"}, e.response.status_code
        
    except Exception as e:
        app.logger.error(f"Unexpected error forwarding to n8n: {str(e)}")
        return {"error": f"Internal error: {str(e)}"}, 500


@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        "status": "healthy",
        "service": "webhook-receiver",
        "n8n_host": N8N_HOST,
        "n8n_webhook_path": N8N_WEBHOOK_PATH
    }), 200


@app.route('/webhook/github-job', methods=['POST'])
def receive_webhook() -> Tuple[Dict[str, Any], int]:
    """
    Receive GitHub Actions job event webhook and forward to n8n.
    
    Expected payload structure:
    - job_id: Job identifier
    - job_name: Name of the job
    - job_status: Current status (queued, in_progress, completed)
    - job_conclusion: Final result (success, failure, cancelled, etc.)
    - workflow_name: Name of the workflow
    - repository: Repository full name
    - branch: Git branch
    - commit_sha: Commit hash
    - And more metadata fields...
    
    Returns:
        JSON response with forwarding status
    """
    try:
        # Get JSON payload from request
        payload = request.get_json(force=True)
        
        if not payload:
            app.logger.warning("Received empty payload")
            return jsonify({"error": "Empty payload"}), 400
        
        # Log received event
        job_name = payload.get('job_name', 'unknown')
        job_status = payload.get('job_status', 'unknown')
        job_conclusion = payload.get('job_conclusion', 'N/A')
        
        app.logger.info(f"Received webhook: job={job_name}, status={job_status}, conclusion={job_conclusion}")
        
        # Forward to n8n
        response_data, status_code = forward_to_n8n(payload)
        
        return jsonify(response_data), status_code
        
    except Exception as e:
        app.logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": f"Failed to process webhook: {str(e)}"}), 500


if __name__ == '__main__':
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Display startup configuration
    app.logger.info("=" * 60)
    app.logger.info("TK-22 Webhook Receiver Starting")
    app.logger.info("=" * 60)
    app.logger.info(f"N8N Host: {N8N_HOST}")
    app.logger.info(f"N8N Webhook Path: {N8N_WEBHOOK_PATH}")
    app.logger.info(f"Listening on port: {WEBHOOK_PORT}")
    app.logger.info("=" * 60)
    
    # Start Flask server
    app.run(host='0.0.0.0', port=WEBHOOK_PORT, debug=True)
