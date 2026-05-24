# Calendly Marketing Insights Pipeline

## Objective

Build an end-to-end AWS data engineering pipeline that ingests Calendly booking events and marketing spend data, stores the data in Delta Lake on Amazon S3, 
transforms it through Bronze, Silver, and Gold layers, and delivers business insights through Athena and Streamlit.

## Business Problem

The organization wants to understand how marketing campaigns are performing and how many leads are generated from each paid channel. 
Marketing spend is spread across Facebook, YouTube, and TikTok paid ads, but the business needs a centralized pipeline to connect campaign spend with Calendly bookings.

This project helps answer:

- Which marketing channels generate the most bookings?
- Which channels have the lowest cost per booking?
- How do bookings trend over time?
- What days and times do leads prefer to book meetings?
- Which employees are handling the highest meeting load?

## Business Value

The pipeline enables the business to optimize marketing spend, improve campaign attribution, monitor lead generation performance, and support better calendar planning for employees.


## Core Flow
```
Calendly Webhook → API Gateway → SQS → Lambda → S3 Bronze Delta
Marketing Spend S3 → EventBridge → Lambda → S3 Bronze Delta
Bronze → EMR Spark → Silver → Gold → Athena → Streamlit
```
## Source Systems

This project uses two main data sources:

### 1. Calendly Webhook Events

Calendly sends real-time booking events when a new invitee schedules a meeting.

Event type:

```text
invitee.created
```

### 2. Marketing Spend Data

Marketing spend data is available as daily JSON files from a public S3 path.

- Actual spend file:
    - spend_data_YYYY-MM-DD.json
- Index/helper file:
    - file_index.json

### Ingestion Strategy

**Calendly Webhook Ingestion**

Calendly uses a push-based ingestion pattern.

```Calendly → API Gateway → SQS → Lambda → S3 Bronze Delta```

This is used because booking events arrive in real time.

**Marketing Spend Ingestion**

Marketing spend uses a pull-based scheduled ingestion pattern.

```EventBridge → Lambda → Public S3 Spend File → S3 Bronze Delta```

This is used because spend data arrives once per day at 6:00 AM EST.
The Lambda function reads file_index.json, identifies the available spend file, downloads the correct spend_data_YYYY-MM-DD.json, and stores it in the Bronze layer.

## Architecture Components

1. Calendly Webhook
2. Amazon API Gateway
3. Amazon SQS
4. AWS Lambda — Webhook Ingestion
5. Amazon EventBridge
6. AWS Lambda — Spend Ingestion
7. Amazon S3 Delta Lake
8. Amazon EMR Spark
9. AWS Glue Data Catalog
10. Amazon Athena
11. Streamlit Dashboard
12. CloudWatch + SNS
13. IAM + KMS
14. GitHub CI/CD

