# Data Model Design

## Bronze Layer

The Bronze layer stores raw data with minimal transformation.

### bronze_calendly_webhook

Purpose: Store raw Calendly webhook events.

Main fields:

```text
event_id
event_name
raw_payload
ingestion_timestamp
ingestion_date
source_system
```
Example S3 path:
  - s3://bucket/bronze/calendly/

### bronze_marketing_spend

Purpose: Store raw marketing spend JSON data.
```
Main fields:

spend_date
channel
spend
raw_payload
ingestion_timestamp
ingestion_date
source_file_name
```
Example S3 path:
  - s3://bucket/bronze/spend/

## Silver Layer
The Silver layer stores cleaned, flattened, and standardized data.

### silver_calendly_bookings

Purpose: Flatten Calendly webhook data into one row per booking.
```
Main fields:

booking_id
invitee_uri
invitee_name
invitee_email
booking_created_at
booking_date
scheduled_event_uri
event_name
event_type_uri
channel
timezone
status
rescheduled
utm_source
utm_campaign
utm_medium
employee_id
employee_name
employee_email

```

### silver_marketing_spend

Purpose: Clean daily marketing spend data.
```
Main fields:

spend_date
channel
spend_amount
currency
source_file_name
ingestion_timestamp

```
### silver_event_channel_map

Purpose: Map Calendly event type URI to campaign/channel.
```
Main fields:

event_type_uri
channel
campaign_name
is_active

Example values:

d639ecd3-8718-4068-955a-436b10d72c78 → facebook_paid_ads
dbb4ec50-38cd-4bcd-bbff-efb7b5a6f098 → youtube_paid_ads
bb339e98-7a67-4af2-b584-8dbf95564312 → tiktok_paid_ads
```

### silver_employees

Purpose: Store employee/member information from Calendly event memberships.
```
Main fields:

employee_id
employee_uri
employee_name
employee_email
```

## Gold Layer

The Gold layer stores business-ready aggregated metrics.

### gold_daily_bookings_by_source

Purpose: Count bookings per source/channel per day.
```
Fields:

booking_date
channel
total_bookings
```

### gold_cost_per_booking_by_channel

Purpose: Calculate CPB by channel.
```
Formula:

CPB = total_spend / total_bookings

Fields:

spend_date
channel
total_spend
total_bookings
cost_per_booking

```

### gold_bookings_trend_over_time

Purpose: Track daily/weekly booking trends.
```
Fields:

booking_date
channel
daily_bookings
weekly_bookings
cumulative_bookings
```

### gold_channel_attribution_summary

Purpose: Rank channels by spend, bookings, and CPB.
```
Fields:

channel
total_bookings
total_spend
cost_per_booking
rank_by_bookings
rank_by_cpb
```

### gold_bookings_by_time_analysis

Purpose: Analyze booking behavior by hour and weekday.
```
Fields:

booking_date
channel
booking_hour
day_of_week
total_bookings
```

###gold_employee_meeting_load

Purpose: Measure weekly employee meeting load.
```
Fields:

employee_id
employee_name
employee_email
week_start_date
total_meetings
avg_meetings_per_week
```
