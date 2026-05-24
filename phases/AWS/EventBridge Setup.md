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

 Amazon EventBridge – Pipeline Scheduling Rule

<p align="center"> <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/eventbridge.png" width="750"/> </p>

 Amazon EventBridge – Scheduled Workflow Configuration

<p align="center"> <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/eventbridge%202.png" width="750"/> </p>
