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

## Spend Ingestion Lambda

Go to:
- AWS Console → Lambda → Create function
Choose:
- Author from scratch
Use:
  - Function name: marketing_spend_ingestion_lambda
  - Runtime: Python 3.11
  - Architecture: x86_64
Under permissions:
- Use an existing role
  - Role: lambda_spend_ingestion_role
Click Create function.
## Add Environment Variables

Go to:
- Configuration → Environment variables → Edit
Add:
- DEST_BUCKET = calendly-marketing-datalake
- DEST_PREFIX = bronze/spend/
- INDEX_URL = https://dea-data-bucket.s3.us-east-1.amazonaws.com/calendly_spend_data/file_index.json
- BASE_URL = https://dea-data-bucket.s3.us-east-1.amazonaws.com/calendly_spend_data/

## Increase Timeout
Go to:
- Configuration → General configuration → Edit
Set:
- Timeout: 1 minute
- Memory: 256 MB

## Code

```python
import json
import os
import urllib.request
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")

DEST_BUCKET = os.environ["DEST_BUCKET"]
DEST_PREFIX = os.environ["DEST_PREFIX"]
INDEX_URL = os.environ["INDEX_URL"]
BASE_URL = os.environ["BASE_URL"]


def read_json_from_url(url: str):
    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)


def lambda_handler(event, context):
    ingestion_ts = datetime.now(timezone.utc).isoformat()
    ingestion_date = ingestion_ts[:10]

    # 1. Read index file
    file_index = read_json_from_url(INDEX_URL)

    # 2. Get latest spend file
    if isinstance(file_index, dict):
        files = file_index.get("files", [])
    else:
        files = file_index

    spend_files = [
        f for f in files
        if isinstance(f, str) and f.startswith("spend_data_") and f.endswith(".json")
    ]

    if not spend_files:
        raise ValueError("No spend_data_YYYY-MM-DD.json files found in file_index.json")

    latest_file = sorted(spend_files)[-1]
    spend_url = BASE_URL + latest_file

    # 3. Download spend data
    spend_data = read_json_from_url(spend_url)

    if not isinstance(spend_data, list):
        raise ValueError("Spend data file must contain a JSON array")

    # 4. Add metadata
    output_records = []
    for record in spend_data:
        output_records.append({
            **record,
            "source_file_name": latest_file,
            "ingestion_timestamp": ingestion_ts,
            "ingestion_date": ingestion_date,
            "source_system": "public_s3_marketing_spend"
        })

    # 5. Write raw JSON to your Bronze S3
    output_key = (
        f"{DEST_PREFIX}"
        f"ingestion_date={ingestion_date}/"
        f"{latest_file}"
    )

    s3.put_object(
        Bucket=DEST_BUCKET,
        Key=output_key,
        Body=json.dumps(output_records, indent=2),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "message": "Marketing spend file ingested successfully",
        "source_file": latest_file,
        "records_loaded": len(output_records),
        "s3_path": f"s3://{DEST_BUCKET}/{output_key}"
    }

```

- Deploy and Test
- Test → Create new test event
- test_spend_ingestion
- Event Json {}
- Click Test
- Expected result:
  - statusCode: 200
  - records_loaded: 3 or more
  - s3_path: s3://calendly-marketing-datalake/bronze/spend/...
- Then check S3:
    - calendly-marketing-datalake
    - → bronze
    - → spend
    - → ingestion_date=YYYY-MM-DD
  
