# src/tk22/adapters/webhook/client.py

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WebhookClient:
    """
    Webhook adapter for external notifications.
    
    Follows TK-22 architecture principles:
    - NEVER decides or interprets data
    - NEVER defaults missing data to "safe"
    - Allowed to return null/errors on failure
    - Pure external data boundary
    """
    
    def __init__(self, webhook_url: str, timeout: int = 30):
        """
        Initialize webhook client.
        
        Args:
            webhook_url: The webhook endpoint URL
            timeout: Request timeout in seconds
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
    
    def send_notification(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send notification to webhook endpoint.
        
        Args:
            payload: The payload to send to the webhook
            
        Returns:
            Response data if successful, None if failed
            
        Note: Following TK-22 adapter principles:
        - Does not retry on failure
        - Does not mask errors
        - Returns None on any failure condition
        """
        try:
            logger.info(f"Sending webhook notification to {self.webhook_url}")
            logger.debug(f"Webhook payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            
            # Log response details
            logger.info(f"Webhook response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json() if response.text else {}
                    logger.info("Webhook notification sent successfully")
                    return {
                        'status': 'success',
                        'status_code': response.status_code,
                        'response': response_data,
                        'sent_at': datetime.utcnow().isoformat()
                    }
                except json.JSONDecodeError:
                    logger.warning("Webhook returned non-JSON response")
                    return {
                        'status': 'success',
                        'status_code': response.status_code,
                        'response': response.text,
                        'sent_at': datetime.utcnow().isoformat()
                    }
            else:
                logger.error(f"Webhook failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Webhook request timed out after {self.timeout} seconds")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Failed to connect to webhook endpoint: {self.webhook_url}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Webhook request failed: {str(e)}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error sending webhook: {str(e)}")
            return None
    
    def validate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validate webhook payload structure.
        
        Args:
            payload: The payload to validate
            
        Returns:
            True if payload is valid, False otherwise
        """
        required_fields = ['address', 'jobId', 'source']
        
        if not isinstance(payload, dict):
            logger.error("Webhook payload must be a dictionary")
            return False
        
        for field in required_fields:
            if field not in payload:
                logger.error(f"Missing required field in webhook payload: {field}")
                return False
            
            if payload[field] is None or payload[field] == "":
                logger.error(f"Required field cannot be empty: {field}")
                return False
        
        return True
