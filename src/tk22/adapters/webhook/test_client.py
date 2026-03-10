# src/tk22/adapters/webhook/test_client.py

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime

from .client import WebhookClient

class TestWebhookClient(unittest.TestCase):
    """Test cases for WebhookClient adapter."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.webhook_url = "https://example.com/webhook"
        self.client = WebhookClient(self.webhook_url, timeout=10)
        
        self.valid_payload = {
            "address": "123 Main St",
            "jobId": "job_001",
            "source": "tk22-test"
        }
    
    def test_validate_payload_valid(self):
        """Test payload validation with valid payload."""
        result = self.client.validate_payload(self.valid_payload)
        self.assertTrue(result)
    
    def test_validate_payload_missing_field(self):
        """Test payload validation with missing required field."""
        invalid_payload = {
            "address": "123 Main St",
            "jobId": "job_001"
            # Missing 'source'
        }
        result = self.client.validate_payload(invalid_payload)
        self.assertFalse(result)
    
    def test_validate_payload_empty_field(self):
        """Test payload validation with empty required field."""
        invalid_payload = {
            "address": "",
            "jobId": "job_001",
            "source": "tk22-test"
        }
        result = self.client.validate_payload(invalid_payload)
        self.assertFalse(result)
    
    def test_validate_payload_not_dict(self):
        """Test payload validation with non-dict payload."""
        result = self.client.validate_payload("not a dict")
        self.assertFalse(result)
    
    @patch('requests.post')
    def test_send_notification_success(self, mock_post):
        """Test successful webhook notification."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "received"}
        mock_response.text = '{"status": "received"}'
        mock_post.return_value = mock_response
        
        result = self.client.send_notification(self.valid_payload)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['status_code'], 200)
        self.assertIn('sent_at', result)
        
        # Verify request was made correctly
        mock_post.assert_called_once_with(
            self.webhook_url,
            json=self.valid_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
    
    @patch('requests.post')
    def test_send_notification_http_error(self, mock_post):
        """Test webhook notification with HTTP error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        result = self.client.send_notification(self.valid_payload)
        
        self.assertIsNone(result)
    
    @patch('requests.post')
    def test_send_notification_timeout(self, mock_post):
        """Test webhook notification with timeout."""
        # Mock timeout exception
        mock_post.side_effect = Exception("Timeout")
        
        result = self.client.send_notification(self.valid_payload)
        
        self.assertIsNone(result)
    
    @patch('requests.post')
    def test_send_notification_connection_error(self, mock_post):
        """Test webhook notification with connection error."""
        # Mock connection error
        mock_post.side_effect = Exception("Connection failed")
        
        result = self.client.send_notification(self.valid_payload)
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
