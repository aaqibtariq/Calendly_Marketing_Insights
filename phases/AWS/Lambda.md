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
