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
