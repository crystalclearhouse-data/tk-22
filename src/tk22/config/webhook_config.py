# src/tk22/config/webhook_config.py

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WebhookConfig:
    """
    Webhook configuration management.
    
    Handles environment-based configuration for webhook integration
    following TK-22 fail-closed principles.
    """
    
    # Default webhook URLs from task specification
    DEFAULT_PRODUCTION_URL = "https://ggggggggggggggg.app.n8n.cloud/webhook/7d0ce8ff-0d0b-4bce-9904-139c5b841865"
    DEFAULT_TEST_URL = "https://ggggggggggggggg.app.n8n.cloud/webhook-test/7d0ce8ff-0d0b-4bce-9904-139c5b841865"
    
    def __init__(self):
        """Initialize webhook configuration from environment variables."""
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables."""
        # Webhook URLs
        self.production_url = os.getenv('WEBHOOK_PRODUCTION_URL', self.DEFAULT_PRODUCTION_URL)
        self.test_url = os.getenv('WEBHOOK_TEST_URL', self.DEFAULT_TEST_URL)
        
        # Environment selection
        self.environment = os.getenv('TK22_ENVIRONMENT', 'development').lower()
        self.use_test_webhook = os.getenv('WEBHOOK_USE_TEST', 'true').lower() == 'true'
        
        # Webhook behavior settings
        self.enabled = os.getenv('WEBHOOK_ENABLED', 'true').lower() == 'true'
        self.timeout = int(os.getenv('WEBHOOK_TIMEOUT', '30'))
        self.fail_on_webhook_error = os.getenv('WEBHOOK_FAIL_ON_ERROR', 'false').lower() == 'true'
        
        # Logging configuration
        self.log_payloads = os.getenv('WEBHOOK_LOG_PAYLOADS', 'true').lower() == 'true'
        self.log_responses = os.getenv('WEBHOOK_LOG_RESPONSES', 'false').lower() == 'true'
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration values."""
        if self.timeout <= 0:
            logger.warning(f"Invalid webhook timeout {self.timeout}, using default 30 seconds")
            self.timeout = 30
        
        if self.timeout > 300:  # 5 minutes max
            logger.warning(f"Webhook timeout {self.timeout} too high, capping at 300 seconds")
            self.timeout = 300
        
        # Validate URLs
        if not self.production_url or not self.production_url.startswith('http'):
            logger.error(f"Invalid production webhook URL: {self.production_url}")
            
        if not self.test_url or not self.test_url.startswith('http'):
            logger.error(f"Invalid test webhook URL: {self.test_url}")
    
    def get_webhook_url(self) -> str:
        """
        Get the appropriate webhook URL based on environment and configuration.
        
        Returns:
            The webhook URL to use
        """
        if self.environment == 'production' and not self.use_test_webhook:
            return self.production_url
        else:
            return self.test_url
    
    def is_enabled(self) -> bool:
        """Check if webhook notifications are enabled."""
        return self.enabled
    
    def should_fail_on_error(self) -> bool:
        """Check if webhook errors should cause overall operation failure."""
        return self.fail_on_webhook_error
    
    def get_timeout(self) -> int:
        """Get webhook request timeout in seconds."""
        return self.timeout
    
    def should_log_payloads(self) -> bool:
        """Check if webhook payloads should be logged."""
        return self.log_payloads
    
    def should_log_responses(self) -> bool:
        """Check if webhook responses should be logged."""
        return self.log_responses
    
    def get_config_summary(self) -> dict:
        """Get a summary of current configuration for logging/debugging."""
        return {
            'environment': self.environment,
            'webhook_url': self.get_webhook_url(),
            'enabled': self.enabled,
            'timeout': self.timeout,
            'use_test_webhook': self.use_test_webhook,
            'fail_on_error': self.fail_on_webhook_error,
            'log_payloads': self.log_payloads,
            'log_responses': self.log_responses
        }
