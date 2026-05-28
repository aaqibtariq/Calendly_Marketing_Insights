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

# Technologies Used

## AWS Services
- Amazon S3
- Amazon API Gateway
- AWS Lambda
- Amazon EMR
- Amazon Athena
- AWS IAM
- Amazon CloudWatch
- Amazon SNS
- Amazon SQS
- Amazon EventBridge

---

## Analytics & Visualization
- Apache Spark
- PySpark
- Delta Lake
- Streamlit
- Plotly
- Pandas
- PyAthena

# AWS Infrastructure Setup

## IAM Setup
- IAM Roles
- IAM Policies
- EMR Permissions
- Lambda Permissions
- Athena Permissions
- S3 Access Policies

Reference:
- [IAM Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/IAM%20Setup.md)

---

## S3 Data Lake Setup
- Bronze Layer Structure
- Silver Layer Structure
- Gold Layer Structure
- Athena Results Bucket
- Partition Strategy
- Delta Lake Storage Structure

Reference:
- [S3 Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/S3.md)

---

## API Gateway Setup
- REST API Creation
- Calendly Webhook Endpoint
- POST Method Configuration
- Lambda Integration
- Endpoint Testing

Reference:
- [API Gateway Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/API%20Gateway%20Setup.md)

---

## Calendly Webhook Ingestion Lambda
- Webhook Event Processing
- JSON Parsing
- Metadata Enrichment
- Bronze Layer Storage
- Error Handling
- Logging

Reference:
- [Calendly Webhook Lambda](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/calendly_webhook_ingestion_lambda.md)

---

## Marketing Spend Ingestion Lambda
- Public S3 Spend File Retrieval
- Dynamic File Detection
- Spend Data Processing
- Bronze Layer Storage
- Incremental Ingestion Logic

Reference:
- [Marketing Spend Lambda](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/marketing_spend_ingestion_lambda.md)

---

## SQS Setup
- Queue Creation
- Dead Letter Queue
- Message Handling
- Retry Mechanism

Reference:
- [SQS Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/SQS%20Setup.md)

---

## EventBridge Setup
- Scheduled Trigger Configuration
- EMR Workflow Scheduling
- Automation Strategy

Reference:
- [EventBridge Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/EventBridge%20Setup.md)

---

## CloudWatch + SNS Setup
- EMR Monitoring
- Lambda Monitoring
- Athena Monitoring
- Error Alerts
- SNS Notifications

Reference:
- [CloudWatch + SNS Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/CloudWatch%20%2B%20SNS%20Setup.md)

---

## EC2 Setup
- Streamlit Server Setup
- Security Group Configuration
- SSH Configuration
- Python Environment Setup
- Streamlit Deployment

Reference:
- [EC2 Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/EC2%20setup.md)

---

## EMR Setup
- EMR Cluster Creation
- Spark Configuration
- Delta Lake Configuration
- PySpark Environment
- Cluster Scaling
- EMR Execution Flow

Reference:
- [EMR Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/EMR%20Setup.md)

---

## Glue Data Catalog Setup
- Athena Metadata Management
- Delta Table Registration
- External Table Configuration

Reference:
- [Glue Data Catalog Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/Glue%20Data%20Catalog%20Setup%2Cmd)

---

# Silver Layer Processing

## Silver Layer Overview
- Silver Layer Objective
- Data Cleaning Strategy
- Delta Lake Processing
- Schema Standardization

Reference:
- [Silver Layer Overview](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/silver/readme.md)

---

## Silver Calendly Transformation
- Flatten Nested JSON
- Event Type Mapping
- Channel Attribution Logic
- Date & Timestamp Standardization
- Duplicate Removal
- Delta Table Creation

Reference:
- [Silver Calendly Transform](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/silver/silver_calendly_transform.py)

---

## Silver Marketing Spend Transformation
- Spend Data Cleaning
- Channel Standardization
- Spend Validation
- Delta Table Creation

Reference:
- [Silver Marketing Spend](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/silver/silver_marketing_spend.py)

---

# Gold Layer Processing

## Gold Layer Overview
- Business Aggregation Layer
- KPI Computation
- Analytics Data Modeling
- Dashboard Consumption Layer

Reference:
- [Gold Layer Overview](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/gold/readme.md)

---

## Gold Analytics Transformation
- Daily Calls by Source
- Cost Per Booking (CPB)
- Booking Time Slot Analytics
- Employee Meeting Load
- Delta Gold Tables

Reference:
- [Gold Analytics Transform](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/gold/gold_analytics_transform.py)

---

# Athena Analytics Layer

## Athena Setup
- Athena Database Creation
- Delta Table Configuration
- External Table Creation
- Query Validation
- Athena Optimization

Reference:
- [Athena Setup](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/Athena%20Setup.md)
- [Athena Queries Folder](https://github.com/aaqibtariq/Calendly_Marketing_Insights/tree/main/phases/athena)

---

# Streamlit Dashboard

## Streamlit Application
- Athena Integration
- KPI Cards
- Interactive Filters
- Plotly Visualizations
- Dashboard Layout
- Real-Time Analytics

Reference:
- [Streamlit app.py](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/streamlit/app.py)

---

# Dashboard Results

## Final Dashboard Screenshots
- KPI Dashboard
- CPB Analytics
- Booking Trend Analytics
- Booking Heatmaps
- Employee Analytics

Reference:
- [Dashboard Results](https://github.com/aaqibtariq/Calendly_Marketing_Insights/tree/main/phases/Results)

---

# Final Validation

## End-to-End Pipeline Validation
- Bronze Validation
- Silver Validation
- Gold Validation
- Athena Query Validation
- Dashboard Validation

---

# Business Metrics

## Metrics Implemented
- Daily Calls Booked by Source
- Cost Per Booking (CPB)
- Booking Trends Over Time
- Channel Attribution
- Booking Volume by Time Slot
- Employee Meeting Load


# Project Outcome

## Final Deliverables
- End-to-End Marketing Analytics Pipeline
- Delta Lake Medallion Architecture
- Athena Analytics Layer
- Interactive Streamlit Dashboard
- Real-Time Marketing Insights Platform

