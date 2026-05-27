
```

CREATE DATABASE IF NOT EXISTS calendly_marketing_analytics;
CREATE EXTERNAL TABLE calendly_marketing_analytics.silver_calendly_events_clean
LOCATION 's3://calendly-marketing-datalake/silver/calendly_events_clean/'
TBLPROPERTIES ('table_type'='DELTA');
CREATE EXTERNAL TABLE calendly_marketing_analytics.silver_marketing_spend_clean
LOCATION 's3://calendly-marketing-datalake/silver/marketing_spend_clean/'
TBLPROPERTIES ('table_type'='DELTA');
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_daily_calls_by_source
LOCATION 's3://calendly-marketing-datalake/gold/daily_calls_by_source/'
TBLPROPERTIES ('table_type'='DELTA');
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_cpb_by_channel
LOCATION 's3://calendly-marketing-datalake/gold/cpb_by_channel/'
TBLPROPERTIES ('table_type'='DELTA');
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_booking_time_slot
LOCATION 's3://calendly-marketing-datalake/gold/booking_time_slot/'
TBLPROPERTIES ('table_type'='DELTA');
CREATE EXTERNAL TABLE calendly_marketing_analytics.gold_employee_meeting_load
LOCATION 's3://calendly-marketing-datalake/gold/employee_meeting_load/'
TBLPROPERTIES ('table_type'='DELTA');


SELECT * 
FROM calendly_marketing_analytics.gold_cpb_by_channel
LIMIT 10;


Daily Calls by Source
SELECT *
FROM calendly_marketing_analytics.gold_daily_calls_by_source
LIMIT 10;

Booking Time Slot
SELECT *
FROM calendly_marketing_analytics.gold_booking_time_slot
LIMIT 10;

Employee Meeting Load
SELECT *
FROM calendly_marketing_analytics.gold_employee_meeting_load
LIMIT 10;
```
