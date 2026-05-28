# Athena Setup and Validation

## Objective

This phase creates the Athena analytics layer for the Calendly Marketing Insights project.

Athena is used to query Delta Lake tables stored in Amazon S3 across the Silver and Gold layers.

---

## Athena Database Creation

```sql
CREATE DATABASE IF NOT EXISTS calendly_marketing_analytics;
```

---

## Silver Layer Table Creation

### Silver Calendly Events Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.silver_calendly_events_clean
LOCATION 's3://calendly-marketing-datalake/silver/calendly_events_clean/'
TBLPROPERTIES ('table_type'='DELTA');
```

### Silver Marketing Spend Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.silver_marketing_spend_clean
LOCATION 's3://calendly-marketing-datalake/silver/marketing_spend_clean/'
TBLPROPERTIES ('table_type'='DELTA');
```

---

## Gold Layer Table Creation

### Gold Daily Calls by Source Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_daily_calls_by_source
LOCATION 's3://calendly-marketing-datalake/gold/daily_calls_by_source/'
TBLPROPERTIES ('table_type'='DELTA');
```

### Gold CPB by Channel Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_cpb_by_channel
LOCATION 's3://calendly-marketing-datalake/gold/cpb_by_channel/'
TBLPROPERTIES ('table_type'='DELTA');
```

### Gold Booking Time Slot Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_booking_time_slot
LOCATION 's3://calendly-marketing-datalake/gold/booking_time_slot/'
TBLPROPERTIES ('table_type'='DELTA');
```

### Gold Employee Meeting Load Table

```sql
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_employee_meeting_load
LOCATION 's3://calendly-marketing-datalake/gold/employee_meeting_load/'
TBLPROPERTIES ('table_type'='DELTA');
```

---

## Confirm Tables Were Created

```sql
SHOW TABLES IN calendly_marketing_analytics;
```

Expected tables:

```text
silver_calendly_events_clean
silver_marketing_spend_clean
gold_daily_calls_by_source
gold_cpb_by_channel
gold_booking_time_slot
gold_employee_meeting_load
```

---

## Silver Layer Validation Queries

### Check Silver Calendly Events

```sql
SELECT *
FROM calendly_marketing_analytics.silver_calendly_events_clean
LIMIT 10;
```

### Count Silver Calendly Events

```sql
SELECT COUNT(*) AS total_calendly_events
FROM calendly_marketing_analytics.silver_calendly_events_clean;
```

### Check Bookings by Channel

```sql
SELECT
    channel,
    COUNT(*) AS total_bookings
FROM calendly_marketing_analytics.silver_calendly_events_clean
GROUP BY channel
ORDER BY total_bookings DESC;
```

### Check Silver Marketing Spend

```sql
SELECT *
FROM calendly_marketing_analytics.silver_marketing_spend_clean
LIMIT 10;
```

### Check Spend by Channel

```sql
SELECT
    channel,
    ROUND(SUM(spend), 2) AS total_spend
FROM calendly_marketing_analytics.silver_marketing_spend_clean
GROUP BY channel
ORDER BY total_spend DESC;
```

---

## Gold Layer Validation Queries

### Daily Calls by Source

```sql
SELECT *
FROM calendly_marketing_analytics.gold_daily_calls_by_source
LIMIT 10;
```

### CPB by Channel

```sql
SELECT *
FROM calendly_marketing_analytics.gold_cpb_by_channel
LIMIT 10;
```

### Booking Time Slot

```sql
SELECT *
FROM calendly_marketing_analytics.gold_booking_time_slot
LIMIT 10;
```

### Employee Meeting Load

```sql
SELECT *
FROM calendly_marketing_analytics.gold_employee_meeting_load
LIMIT 10;
```

---

## Business Metric Validation Queries

### Total Bookings

```sql
SELECT
    SUM(total_bookings) AS total_bookings
FROM calendly_marketing_analytics.gold_daily_calls_by_source;
```

### Total Bookings by Channel

```sql
SELECT
    channel,
    SUM(total_bookings) AS total_bookings
FROM calendly_marketing_analytics.gold_daily_calls_by_source
GROUP BY channel
ORDER BY total_bookings DESC;
```

### Cost Per Booking by Channel

```sql
SELECT
    channel,
    SUM(total_bookings) AS total_bookings,
    ROUND(SUM(total_spend), 2) AS total_spend,
    ROUND(SUM(total_spend) / NULLIF(SUM(total_bookings), 0), 2) AS cpb
FROM calendly_marketing_analytics.gold_cpb_by_channel
WHERE total_bookings > 0
GROUP BY channel
ORDER BY cpb ASC;
```

### Daily Booking Trend

```sql
SELECT
    booking_date,
    channel,
    SUM(total_bookings) AS total_bookings
FROM calendly_marketing_analytics.gold_daily_calls_by_source
GROUP BY booking_date, channel
ORDER BY booking_date, channel;
```

### Booking Volume by Hour

```sql
SELECT
    meeting_hour,
    SUM(total_bookings) AS total_bookings
FROM calendly_marketing_analytics.gold_booking_time_slot
GROUP BY meeting_hour
ORDER BY meeting_hour;
```

### Booking Volume by Day of Week

```sql
SELECT
    meeting_day_of_week,
    SUM(total_bookings) AS total_bookings
FROM calendly_marketing_analytics.gold_booking_time_slot
GROUP BY meeting_day_of_week
ORDER BY meeting_day_of_week;
```

### Employee Meeting Load

```sql
SELECT
    employee_name,
    employee_email,
    SUM(total_meetings) AS total_meetings,
    SUM(unique_leads) AS unique_leads
FROM calendly_marketing_analytics.gold_employee_meeting_load
GROUP BY employee_name, employee_email
ORDER BY total_meetings DESC;
```

---

## Data Quality Checks

### Check for Null Channels

```sql
SELECT COUNT(*) AS null_channel_count
FROM calendly_marketing_analytics.silver_calendly_events_clean
WHERE channel IS NULL;
```

### Check for Duplicate Bookings

```sql
SELECT
    event_id,
    COUNT(*) AS duplicate_count
FROM calendly_marketing_analytics.silver_calendly_events_clean
GROUP BY event_id
HAVING COUNT(*) > 1;
```

### Check for Missing Spend Values

```sql
SELECT COUNT(*) AS missing_spend_count
FROM calendly_marketing_analytics.silver_marketing_spend_clean
WHERE spend IS NULL;
```

### Check CPB Rows with Spend but No Bookings

```sql
SELECT *
FROM calendly_marketing_analytics.gold_cpb_by_channel
WHERE total_spend > 0
  AND total_bookings = 0
ORDER BY report_date, channel;
```

---

## Athena Output Location

Athena query results are stored in:

```text
s3://calendly-marketing-datalake/athena-results/
```

---

## Tables Created

| Layer | Table Name | Purpose |
|---|---|---|
| Silver | `silver_calendly_events_clean` | Cleaned Calendly booking events |
| Silver | `silver_marketing_spend_clean` | Cleaned marketing spend data |
| Gold | `gold_daily_calls_by_source` | Daily booking volume by channel |
| Gold | `gold_cpb_by_channel` | Cost per booking by channel |
| Gold | `gold_booking_time_slot` | Booking volume by hour and day |
| Gold | `gold_employee_meeting_load` | Employee meeting workload |

---

## Final Validation Checklist

- Athena database created successfully
- Silver Delta tables registered successfully
- Gold Delta tables registered successfully
- Athena query results stored in S3 results bucket
- Silver tables returned cleaned data
- Gold tables returned business-level metrics
- Streamlit connected to Athena successfully
- Dashboard displayed KPIs and visualizations successfully

![Athena Results](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/athena-results.png)
