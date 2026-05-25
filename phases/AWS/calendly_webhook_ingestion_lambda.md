# Lambda Functions

- calendly_webhook_ingestion_lambda
- marketing_spend_ingestion_lambda

## Webhook Lambda

Triggered by:
- SQS
Writes to:
- s3://calendly-marketing-datalake/bronze/calendly/

## Spend Lambda

Triggered by:
- EventBridge
Reads:
- file_index.json
- spend_data_YYYY-MM-DD.json
Writes to:
- s3://calendly-marketing-datalake/bronze/spend/

# calendly_webhook_ingestion_lambda

- Go to:
  - AWS Console → Lambda → Create function
- Choose:
  - Author from scratch
- Use:
  - Function name: calendly_webhook_ingestion_lambda
  - Runtime: Python 3.11
  - Architecture: x86_64
- Permissions:
  - Use existing role
    - lambda_webhook_ingestion_role
- Click Create function.

## Environment variables

- Add:
  - DEST_BUCKET = calendly-marketing-datalake
  - DEST_PREFIX = bronze/calendly/
 
## Timeout

- Set:
  - Timeout: 1 minute
  - Memory: 256 MB
 
# code

```python
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")

DEST_BUCKET = os.environ["DEST_BUCKET"]
DEST_PREFIX = os.environ["DEST_PREFIX"]


def lambda_handler(event, context):
    ingestion_ts = datetime.now(timezone.utc).isoformat()
    ingestion_date = ingestion_ts[:10]

    records_loaded = 0
    output_files = []

    for record in event.get("Records", []):
        # SQS message body should contain Calendly webhook JSON
        body = record.get("body", "{}")

        try:
            webhook_event = json.loads(body)
        except json.JSONDecodeError:
            webhook_event = {
                "raw_body": body,
                "parse_error": True
            }

        event_name = webhook_event.get("event", "unknown_event")

        payload = webhook_event.get("payload", {})
        invitee_uri = payload.get("uri")
        scheduled_event_uri = payload.get("scheduled_event", {}).get("uri")

        output_record = {
            "event_id": str(uuid.uuid4()),
            "event_name": event_name,
            "invitee_uri": invitee_uri,
            "scheduled_event_uri": scheduled_event_uri,
            "raw_payload": webhook_event,
            "ingestion_timestamp": ingestion_ts,
            "ingestion_date": ingestion_date,
            "source_system": "calendly_webhook"
        }

        file_name = f"{output_record['event_id']}.json"

        output_key = (
            f"{DEST_PREFIX}"
            f"ingestion_date={ingestion_date}/"
            f"{file_name}"
        )

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=output_key,
            Body=json.dumps(output_record, indent=2),
            ContentType="application/json"
        )

        records_loaded += 1
        output_files.append(f"s3://{DEST_BUCKET}/{output_key}")

    return {
        "statusCode": 200,
        "message": "Calendly webhook events ingested successfully",
        "records_loaded": records_loaded,
        "output_files": output_files
    }

```
## Add SQS trigger

- Inside Lambda:
  - Configuration → Triggers → Add trigger
- Choose:
  - SQS
- Select:
  - calendly-webhook-queue
- Batch size:
  - 1
- Enable trigger:
  - Yes
- Click Add.
