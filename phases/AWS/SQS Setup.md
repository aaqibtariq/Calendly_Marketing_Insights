## Queues Needed
-  calendly-webhook-queue
-  calendly-webhook-dlq
  
Purpose

-  Main queue stores incoming webhook events
-  DLQ stores failed events for replay

# Create DLQ First

- Go to:
  - AWS Console → SQS → Create queue
- Choose:
  - Type: Standard
  - Name: calendly-webhook-dlq
- Keep defaults, then click:
-  Create queue

# Create Main Queue

- Create another queue:
  - Type: Standard
  - Name: calendly-webhook-queue
- visivility
    - 120 sec
- Scroll to:
  -  Dead-letter queue
- Enable:
  -Use Redrive policy
- Select DLQ:
  - calendly-webhook-dlq
- Set:
  - Maximum receives: 3
- Click:
  - Create queue
 

## Test Webhook Pipeline Using SQS

- Open Queue
  - Go to:
    - SQS
        - → calendly-webhook-queue
- Click:
  - Send and receive messages
 
## Send Test Calendly Webhook

```
{
  "event": "invitee.created",
  "payload": {
    "uri": "https://api.calendly.com/invitees/test_invitee_001",
    "created_at": "2026-05-24T18:30:00Z",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "scheduled_event": {
      "uri": "https://api.calendly.com/scheduled_events/test_event_001"
    },
    "tracking": {
      "utm_source": "facebook",
      "utm_campaign": "summer_campaign"
    }
  }
}

```
- Click:
  - Send message
 
## Verify S3 Output

- Go to:
  - calendly-marketing-datalake
  - → bronze
  - → calendly
  - → ingestion_date=YYYY-MM-DD
- You should see:
  - <uuid>.json
 
- Expected Result
  - Webhook event successfully lands in:
    - bronze/calendly/

Amazon SQS – Queue Message Testing

<p align="center"> <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/SQS%20test.png" width="750"/> </p>

Sample Webhook Payload – JSON Event Structure
-  [Webhook JSON Payload Sample](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/6a5f714d-a94a-4120-853a-602dc05c1f3e.json)
