# Data Model Design

## Overview

This project follows a Medallion Architecture using Delta Lake on Amazon S3.

The data model is organized into three layers:

```text
Bronze Layer  → Raw JSON Data
Silver Layer  → Cleaned and Flattened Delta Tables
Gold Layer    → Business-Ready Analytics Delta Tables
```

---

# Bronze Layer

The Bronze layer stores raw source data with minimal transformation.

## bronze_calendly_webhook

### Purpose

Stores raw Calendly webhook events received from API Gateway and Lambda.

### Source

Calendly webhook event:

```text
invitee.created
```

### S3 Path

```text
s3://calendly-marketing-datalake/bronze/calendly/
```

### Main Fields

```text
event_id
event_name
invitee_uri
scheduled_event_uri
raw_payload
ingestion_timestamp
ingestion_date
source_system
```

### Notes

The full Calendly webhook JSON is preserved in `raw_payload` for replay, audit, and future transformation needs.

---

## bronze_marketing_spend

### Purpose

Stores raw marketing spend JSON files from the public S3 source.

### S3 Path

```text
s3://calendly-marketing-datalake/bronze/spend/
```

### Main Fields

```text
date
channel
spend
source_file_name
ingestion_timestamp
ingestion_date
source_system
```

### Example Channels

```text
facebook_paid_ads
youtube_paid_ads
tiktok_paid_ads
```

---

# Silver Layer

The Silver layer stores cleaned, flattened, standardized Delta tables.

---

## silver_calendly_events_clean

### Purpose

Flattens Calendly webhook JSON into one clean row per booking event.

### S3 Path

```text
s3://calendly-marketing-datalake/silver/calendly_events_clean/
```

### Athena Table

```text
calendly_marketing_analytics.silver_calendly_events_clean
```

### Grain

```text
One row per Calendly booking event
```

### Main Fields

```text
event_id
booking_id
event_name
invitee_uri
scheduled_event_uri
meeting_id
invitee_email
invitee_name
invitee_status
invitee_timezone
booking_created_at
booking_date
meeting_start_time
meeting_end_time
meeting_date
meeting_hour
meeting_day_of_week
meeting_name
event_type_uri
employee_id
employee_email
employee_name
utm_source
utm_campaign
channel
ingestion_timestamp
ingestion_date
```

### Channel Mapping Logic

Calendly event type URI is mapped to marketing channel.

```text
d639ecd3-8718-4068-955a-436b10d72c78 → facebook_paid_ads
dbb4ec50-38cd-4bcd-bbff-efb7b5a6f098 → youtube_paid_ads
bb339e98-7a67-4af2-b584-8dbf95564312 → tiktok_paid_ads
```

### Data Quality Rules

```text
Only invitee.created events are included
Unknown channels are filtered out
Duplicate events are removed using event_id
Dates and timestamps are standardized
```

---

## silver_marketing_spend_clean

### Purpose

Cleans and standardizes daily marketing spend data.

### S3 Path

```text
s3://calendly-marketing-datalake/silver/marketing_spend_clean/
```

### Athena Table

```text
calendly_marketing_analytics.silver_marketing_spend_clean
```

### Grain

```text
One row per spend_date, channel, and source_file_name
```

### Main Fields

```text
spend_date
channel
spend
source_file_name
source_system
ingestion_date
```

### Data Quality Rules

```text
Spend date must not be null
Channel must not be null
Spend must not be null
Duplicate spend records are removed by spend_date, channel, and source_file_name
Channel names are lowercased and trimmed
```

---

# Gold Layer

The Gold layer stores business-ready aggregated Delta tables used by Athena and Streamlit.

---

## gold_daily_calls_by_source

### Purpose

Tracks daily Calendly bookings by marketing channel.

### S3 Path

```text
s3://calendly-marketing-datalake/gold/daily_calls_by_source/
```

### Athena Table

```text
calendly_marketing_analytics.gold_daily_calls_by_source
```

### Grain

```text
One row per booking_date and channel
```

### Main Fields

```text
booking_date
channel
total_bookings
unique_leads
unique_events
first_booking_time
last_booking_time
```

### Supports Metrics

```text
Daily Calls Booked by Source
Bookings Trend Over Time
Channel Attribution
```

---

## gold_cpb_by_channel

### Purpose

Calculates Cost Per Booking by marketing channel.

### S3 Path

```text
s3://calendly-marketing-datalake/gold/cpb_by_channel/
```

### Athena Table

```text
calendly_marketing_analytics.gold_cpb_by_channel
```

### Grain

```text
One row per report_date and channel
```

### Main Fields

```text
report_date
channel
total_bookings
unique_leads
unique_events
total_spend
cpb
```

### Formula

```text
CPB = total_spend / total_bookings
```

### Notes

If `total_bookings = 0`, CPB is returned as null to avoid division by zero.

### Supports Metrics

```text
Cost Per Booking by Channel
Channel Attribution Leaderboard
Marketing Spend Analysis
```

---

## gold_booking_time_slot

### Purpose

Analyzes booking behavior by meeting date, weekday, hour, and channel.

### S3 Path

```text
s3://calendly-marketing-datalake/gold/booking_time_slot/
```

### Athena Table

```text
calendly_marketing_analytics.gold_booking_time_slot
```

### Grain

```text
One row per meeting_date, meeting_day_of_week, meeting_hour, and channel
```

### Main Fields

```text
meeting_date
meeting_day_of_week
meeting_hour
channel
total_bookings
unique_leads
```

### Supports Metrics

```text
Booking Volume by Time Slot
Booking Volume by Day of Week
Booking Volume by Hour
Heatmap Analysis
```

---

## gold_employee_meeting_load

### Purpose

Measures meeting workload per employee.

### S3 Path

```text
s3://calendly-marketing-datalake/gold/employee_meeting_load/
```

### Athena Table

```text
calendly_marketing_analytics.gold_employee_meeting_load
```

### Grain

```text
One row per employee and channel
```

### Main Fields

```text
employee_id
employee_name
employee_email
channel
total_meetings
unique_leads
first_meeting_time
last_meeting_time
```

### Supports Metrics

```text
Employee Meeting Load
Employee Booking Distribution
Workload Monitoring
```

---

# Data Model Relationships

## Calendly Events to Marketing Spend

The main join between Calendly bookings and marketing spend is:

```text
silver_calendly_events_clean.booking_date = silver_marketing_spend_clean.spend_date
AND
silver_calendly_events_clean.channel = silver_marketing_spend_clean.channel
```

---

# Final Tables Summary

| Layer | Table Name | Grain | Purpose |
|---|---|---|---|
| Bronze | bronze_calendly_webhook | Raw event | Stores raw Calendly webhook JSON |
| Bronze | bronze_marketing_spend | Raw spend file | Stores raw marketing spend JSON |
| Silver | silver_calendly_events_clean | One row per booking | Cleaned and flattened Calendly events |
| Silver | silver_marketing_spend_clean | One row per spend date/channel/file | Cleaned marketing spend data |
| Gold | gold_daily_calls_by_source | One row per booking date/channel | Daily booking metrics |
| Gold | gold_cpb_by_channel | One row per report date/channel | Cost per booking metrics |
| Gold | gold_booking_time_slot | One row per meeting date/hour/channel | Booking time behavior |
| Gold | gold_employee_meeting_load | One row per employee/channel | Employee meeting workload |

---

# Business Metrics Covered

| Metric | Gold Table |
|---|---|
| Daily Calls Booked by Source | gold_daily_calls_by_source |
| Cost Per Booking by Channel | gold_cpb_by_channel |
| Bookings Trend Over Time | gold_daily_calls_by_source |
| Channel Attribution | gold_cpb_by_channel |
| Booking Volume by Time Slot | gold_booking_time_slot |
| Employee Meeting Load | gold_employee_meeting_load |

---

# Dashboard Consumption Layer

The Streamlit dashboard queries the Gold tables through Athena.

```text
Gold Delta Tables on S3
        ↓
Athena External Tables
        ↓
PyAthena
        ↓
Streamlit Dashboard
```

---

# Final Outcome

This data model supports a complete marketing analytics dashboard with:

```text
Total Bookings
Unique Leads
Total Marketing Spend
Average CPB
Top Channel
Daily Calls by Source
Cost Per Booking by Channel
Booking Trends
Booking Time Slot Heatmap
Employee Meeting Load
```
