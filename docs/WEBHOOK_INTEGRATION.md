# TK-22 Webhook Integration

## Overview

The TK-22 webhook integration enables real-time notifications to external systems when verdicts are generated. This integration follows the TK-22 architectural principles, ensuring that webhook failures do not compromise the core verdict functionality.

## Architecture

The webhook integration is implemented across three layers following TK-22 architecture:

### 1. Adapter Layer (`src/tk22/adapters/webhook/`)
- **WebhookClient**: Handles HTTP communication with external webhook endpoints
- Follows fail-closed principles: returns `None` on any failure
- No retries, no error masking, no defaults to "safe"
- Pure external data boundary

### 2. Service Layer (`src/tk22/services/webhook_service.py`)
- **WebhookService**: Orchestrates webhook notifications
- Transforms TK-22 internal data to webhook payload format
- No decisions, no retries, no conditional logic that alters outcomes
- Pure data orchestration and transformation

### 3. API Layer (`control/runtime/api.py`)
- Integrates webhook notifications into the `/execute` endpoint
- Non-blocking: webhook failures don't affect verdict processing by default
- Configurable fail-on-error behavior for strict environments

## Configuration

Webhook behavior is controlled via environment variables:

```bash
# Webhook URLs
WEBHOOK_PRODUCTION_URL=https://ggggggggggggggg.app.n8n.cloud/webhook/7d0ce8ff-0d0b-4bce-9904-139c5b841865
WEBHOOK_TEST_URL=https://ggggggggggggggg.app.n8n.cloud/webhook-test/7d0ce8ff-0d0b-4bce-9904-139c5b841865

# Environment and behavior
TK22_ENVIRONMENT=development          # development|staging|production
WEBHOOK_ENABLED=true                  # Enable/disable webhook notifications
WEBHOOK_USE_TEST=true                 # Use test URL even in production
WEBHOOK_TIMEOUT=30                    # Request timeout in seconds
WEBHOOK_FAIL_ON_ERROR=false          # Fail entire request if webhook fails

# Logging
WEBHOOK_LOG_PAYLOADS=true            # Log webhook payloads (debug)
WEBHOOK_LOG_RESPONSES=false          # Log webhook responses (debug)
```

## Payload Format

Webhooks send the following payload structure:

```json
{
  "address": "token_address_or_input",
  "jobId": "tk22_proof_id_or_generated",
  "source": "tk22-frontend",
  "verdict": "SAFE_TO_PROCEED",
  "timestamp": "2024-03-10T04:50:41.123Z",
  "proof_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Required Fields (per n8n specification)
- `address`: Extracted from request input or generated fallback
- `jobId`: Extracted from request or generated from proof_id
- `source`: Prefixed with "tk22-" for identification

### Optional Fields (TK-22 context)
- `verdict`: The TK-22 verdict result
- `timestamp`: ISO timestamp of notification
- `proof_id`: TK-22 proof identifier

## Usage

### Basic API Usage

The webhook integration is automatically triggered when using the `/execute` endpoint:

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "token_address_123",
    "mode": "default",
    "source": "frontend"
  }'
```

Response includes verdict, and webhook notification is sent asynchronously:

```json
{
  "verdict": "SAFE_TO_PROCEED",
  "summary": "TK-22 found no blocking risk based on the provided input.",
  "proof_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Programmatic Usage

```python
from tk22.config import WebhookConfig
from tk22.adapters.webhook import WebhookClient
from tk22.services.webhook_service import WebhookService

# Initialize components
config = WebhookConfig()
client = WebhookClient(config.get_webhook_url(), timeout=30)
service = WebhookService(client)

# Send notification
verdict_data = {
    "verdict": "SAFE_TO_PROCEED",
    "summary": "Analysis complete",
    "proof_id": "test_123"
}

request_data = {
    "input": "token_address",
    "source": "api"
}

result = service.notify_verdict(verdict_data, request_data)
```

## Testing

### Integration Test Script

Run the comprehensive integration test:

```bash
python tests/webhook_integration_test.py
```

This tests:
- Webhook client functionality
- Service layer transformation
- Full API integration (if server is running)

### Unit Tests

Run adapter unit tests:

```bash
python -m unittest src.tk22.adapters.webhook.test_client
```

### Manual Testing

Test against the test webhook URL:

```bash
# Set environment to use test webhook
export WEBHOOK_USE_TEST=true
export WEBHOOK_ENABLED=true

# Start the API
python control/runtime/api.py

# In another terminal, test the endpoint
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "test_address_123",
    "mode": "default",
    "source": "manual-test"
  }'
```

## Error Handling

### Webhook Failures
- By default, webhook failures are logged but don't affect verdict processing
- Set `WEBHOOK_FAIL_ON_ERROR=true` for strict fail-closed behavior
- All errors are logged with appropriate detail levels

### Network Issues
- Connection timeouts are handled gracefully
- DNS resolution failures return `None` (no retry)
- HTTP errors (4xx, 5xx) are logged and return `None`

### Payload Issues
- Invalid payloads are rejected before sending
- Missing required fields cause validation failure
- Transformation errors are logged and return `None`

## Monitoring

### Logging
Webhook operations are logged at appropriate levels:

```
INFO: Webhook notification sent successfully for proof_id: abc123
WARNING: Webhook notification failed for proof_id: def456
ERROR: Webhook request timed out after 30 seconds
```

### Configuration Validation
On startup, the system logs current webhook configuration:

```
INFO: Webhook integration initialized: {
  "environment": "development",
  "webhook_url": "https://...webhook-test/...",
  "enabled": true,
  "timeout": 30,
  "use_test_webhook": true,
  "fail_on_error": false
}
```

## Security Considerations

### URL Protection
- Webhook URLs contain sensitive tokens
- URLs are loaded from environment variables (not hardcoded)
- Consider using secrets management in production

### Payload Sanitization
- Payloads are validated before sending
- No sensitive TK-22 internal data is exposed
- Only specified fields are included in notifications

### Network Security
- HTTPS is required for webhook endpoints
- Timeouts prevent hanging connections
- No retry logic prevents amplification attacks

## Production Deployment

### Environment Setup
1. Set `TK22_ENVIRONMENT=production`
2. Set `WEBHOOK_USE_TEST=false` to use production URL
3. Configure appropriate timeout values
4. Enable/disable based on operational requirements

### Monitoring Setup
- Monitor webhook success/failure rates
- Alert on sustained webhook failures
- Track webhook response times

### Rollback Plan
- Set `WEBHOOK_ENABLED=false` to disable notifications
- Webhook failures don't affect core functionality
- Can be toggled without service restart

## Troubleshooting

### Common Issues

**Webhook notifications not sending:**
- Check `WEBHOOK_ENABLED=true`
- Verify webhook URL is accessible
- Check network connectivity

**Payload validation failures:**
- Ensure required fields (address, jobId, source) are present
- Check for empty or null values
- Review transformation logic in WebhookService

**Timeout errors:**
- Increase `WEBHOOK_TIMEOUT` value
- Check external service performance
- Consider network latency

**API errors after webhook integration:**
- Check if `WEBHOOK_FAIL_ON_ERROR=true` is causing failures
- Review webhook error logs
- Temporarily disable with `WEBHOOK_ENABLED=false`

### Debug Mode
Enable detailed logging:

```bash
export WEBHOOK_LOG_PAYLOADS=true
export WEBHOOK_LOG_RESPONSES=true
```

This will log full request/response details for debugging.
