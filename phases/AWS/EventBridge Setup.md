## Purpose
Trigger marketing spend ingestion daily.

## Schedule
-  Daily 6:00 AM EST
Target
-  marketing_spend_ingestion_lambda

## EventBridge Rule

- Name - calendly-marketing-spend-daily-schedule
- cron(0 11 * * ? *)
- Target marketing_spend_ingestion_lambda
- Retry attempts = 3
- Maximum age = 1 hour
- eventbridge_invoke_marketing_spend_lambda_role
- create
