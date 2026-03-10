#!/usr/bin/env python3
# tests/webhook_integration_test.py

"""
Webhook Integration Test Script

This script tests the webhook integration by:
1. Testing against the test webhook URL
2. Validating payload format
3. Testing the full API flow with webhook notifications
"""

import sys
import os
import json
import requests
import time
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tk22.config import WebhookConfig
from tk22.adapters.webhook import WebhookClient
from tk22.services.webhook_service import WebhookService

def test_webhook_client():
    """Test the webhook client directly."""
    print("🔧 Testing WebhookClient...")
    
    config = WebhookConfig()
    client = WebhookClient(config.get_webhook_url(), timeout=10)
    
    # Test payload validation
    valid_payload = {
        "address": "123 Main St",
        "jobId": "test_job_001",
        "source": "tk22-integration-test"
    }
    
    print(f"📋 Validating payload: {json.dumps(valid_payload, indent=2)}")
    is_valid = client.validate_payload(valid_payload)
    print(f"✅ Payload validation: {'PASS' if is_valid else 'FAIL'}")
    
    if not is_valid:
        return False
    
    # Test webhook notification
    print(f"🌐 Sending test notification to: {config.get_webhook_url()}")
    result = client.send_notification(valid_payload)
    
    if result is not None:
        print(f"✅ Webhook notification: SUCCESS")
        print(f"📊 Response: {json.dumps(result, indent=2)}")
        return True
    else:
        print(f"❌ Webhook notification: FAILED")
        return False

def test_webhook_service():
    """Test the webhook service layer."""
    print("\n🔧 Testing WebhookService...")
    
    config = WebhookConfig()
    client = WebhookClient(config.get_webhook_url(), timeout=10)
    service = WebhookService(client)
    
    # Mock verdict and request data
    verdict_data = {
        "verdict": "SAFE_TO_PROCEED",
        "summary": "Test verdict for webhook integration",
        "proof_id": f"test_{int(time.time())}"
    }
    
    request_data = {
        "input": "test_token_address_123",
        "mode": "default",
        "source": "integration-test"
    }
    
    print(f"📋 Test verdict: {json.dumps(verdict_data, indent=2)}")
    print(f"📋 Test request: {json.dumps(request_data, indent=2)}")
    
    result = service.notify_verdict(verdict_data, request_data)
    
    if result is not None:
        print(f"✅ Webhook service: SUCCESS")
        print(f"📊 Service result: {json.dumps(result, indent=2)}")
        return True
    else:
        print(f"❌ Webhook service: FAILED")
        return False

def test_api_integration():
    """Test the full API integration with webhook."""
    print("\n🔧 Testing API Integration...")
    
    # Test payload for the /execute endpoint
    api_payload = {
        "input": "test_integration_address_456",
        "mode": "default",
        "source": "webhook-integration-test"
    }
    
    print(f"📋 API payload: {json.dumps(api_payload, indent=2)}")
    
    try:
        # Note: This assumes the API is running on localhost:5000
        # In a real test environment, you'd start the API or use a test server
        api_url = "http://localhost:5000/execute"
        print(f"🌐 Testing API endpoint: {api_url}")
        
        response = requests.post(
            api_url,
            json=api_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API integration: SUCCESS")
            print(f"📊 API response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ API integration: FAILED (HTTP {response.status_code})")
            print(f"📊 Error response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"⚠️  API integration: SKIPPED (API server not running)")
        print(f"💡 To test API integration, run: python control/runtime/api.py")
        return None
    except Exception as e:
        print(f"❌ API integration: ERROR - {str(e)}")
        return False

def main():
    """Run all webhook integration tests."""
    print("🚀 TK-22 Webhook Integration Test")
    print("=" * 50)
    
    # Display configuration
    config = WebhookConfig()
    print(f"📋 Configuration: {json.dumps(config.get_config_summary(), indent=2)}")
    print()
    
    results = []
    
    # Test webhook client
    results.append(test_webhook_client())
    
    # Test webhook service
    results.append(test_webhook_service())
    
    # Test API integration
    api_result = test_api_integration()
    if api_result is not None:
        results.append(api_result)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    total = len(results)
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {total}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Webhook integration is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the configuration and network connectivity.")
        return 1

if __name__ == "__main__":
    exit(main())
