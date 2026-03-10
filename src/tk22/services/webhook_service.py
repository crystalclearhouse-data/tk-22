# src/tk22/services/webhook_service.py

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ..adapters.webhook import WebhookClient

logger = logging.getLogger(__name__)

class WebhookService:
    """
    Webhook orchestration service.
    
    Follows TK-22 architecture principles:
    - NO decisions or verdict influence
    - NO retries unless explicitly requested
    - NO conditional logic that alters outcomes
    - Pure data orchestration and transformation
    """
    
    def __init__(self, webhook_client: WebhookClient):
        """
        Initialize webhook service.
        
        Args:
            webhook_client: The webhook adapter client
        """
        self.webhook_client = webhook_client
    
    def notify_verdict(self, 
                      verdict_data: Dict[str, Any], 
                      request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Orchestrate webhook notification for verdict events.
        
        Args:
            verdict_data: The verdict result from core
            request_data: The original request data
            
        Returns:
            Webhook response data if successful, None if failed
            
        Note: This service does NOT retry, mask errors, or alter outcomes.
        Webhook failures are logged but do not affect verdict processing.
        """
        try:
            # Transform TK-22 data to webhook payload format
            webhook_payload = self._transform_to_webhook_payload(verdict_data, request_data)
            
            if webhook_payload is None:
                logger.error("Failed to transform data to webhook payload")
                return None
            
            # Validate payload before sending
            if not self.webhook_client.validate_payload(webhook_payload):
                logger.error("Webhook payload validation failed")
                return None
            
            # Send notification via adapter
            result = self.webhook_client.send_notification(webhook_payload)
            
            if result is not None:
                logger.info(f"Webhook notification successful for job {webhook_payload.get('jobId')}")
            else:
                logger.warning(f"Webhook notification failed for job {webhook_payload.get('jobId')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Webhook service error: {str(e)}")
            return None
    
    def _transform_to_webhook_payload(self, 
                                    verdict_data: Dict[str, Any], 
                                    request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform TK-22 internal data to webhook payload format.
        
        Args:
            verdict_data: The verdict result from core
            request_data: The original request data
            
        Returns:
            Transformed payload or None if transformation fails
        """
        try:
            # Extract or generate required fields
            job_id = self._extract_job_id(verdict_data, request_data)
            address = self._extract_address(verdict_data, request_data)
            source = self._extract_source(request_data)
            
            if not all([job_id, address, source]):
                logger.error("Failed to extract required fields for webhook payload")
                return None
            
            # Build webhook payload according to specification
            payload = {
                "address": address,
                "jobId": job_id,
                "source": source,
                # Additional context (optional)
                "verdict": verdict_data.get("verdict"),
                "timestamp": datetime.utcnow().isoformat(),
                "proof_id": verdict_data.get("proof_id")
            }
            
            return payload
            
        except Exception as e:
            logger.error(f"Payload transformation error: {str(e)}")
            return None
    
    def _extract_job_id(self, verdict_data: Dict[str, Any], request_data: Dict[str, Any]) -> Optional[str]:
        """Extract or generate job ID from available data."""
        # Try to extract from request data first
        job_id = request_data.get('jobId') or request_data.get('job_id')
        
        if job_id:
            return str(job_id)
        
        # Try to extract from verdict data
        job_id = verdict_data.get('proof_id')
        if job_id:
            return str(job_id)
        
        # Generate a job ID based on proof_id or create new one
        proof_id = verdict_data.get('proof_id')
        if proof_id:
            return f"tk22_{proof_id}"
        
        # Last resort: generate new UUID
        return f"tk22_{str(uuid.uuid4())[:8]}"
    
    def _extract_address(self, verdict_data: Dict[str, Any], request_data: Dict[str, Any]) -> Optional[str]:
        """Extract address from available data."""
        # Try various possible address fields
        address_fields = ['address', 'target', 'input', 'mint', 'token']
        
        for field in address_fields:
            address = request_data.get(field)
            if address and isinstance(address, str) and address.strip():
                return address.strip()
        
        # Try to extract from input if it's a string that looks like an address
        input_data = request_data.get('input')
        if isinstance(input_data, str) and input_data.strip():
            return input_data.strip()
        
        # If input is a dict, try to find address-like fields
        if isinstance(input_data, dict):
            for field in address_fields:
                address = input_data.get(field)
                if address and isinstance(address, str) and address.strip():
                    return address.strip()
        
        # Default fallback
        return "unknown_address"
    
    def _extract_source(self, request_data: Dict[str, Any]) -> str:
        """Extract source from request data."""
        source = request_data.get('source', 'tk22-system')
        
        # Ensure source follows expected format
        if source == 'frontend':
            return 'tk22-frontend'
        elif source == 'api':
            return 'tk22-api'
        else:
            return f"tk22-{source}" if not source.startswith('tk22-') else source
