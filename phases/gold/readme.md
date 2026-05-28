
# EMR Step

- Name: gold_analytics_transform
- Type: Spark application
- Deploy mode: Cluster
- Application location: s3://calendly-marketing-emr-scripts/scripts/gold_analytics_transform.py
- Spark-submit options: --packages io.delta:delta-spark_2.12:3.2.0
- Arguments: blank
- Action on failure: Continue

- Expected S3 output:
  - gold/booking_time_slot/
  - gold/daily_calls_by_source/
  - gold/cpb_by_channel/
  - gold/employee_meeting_load/
 
![Gold Layer S3](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Gold%20layer%20s3.png)




  # AThena

### gold_channel_cpb

```

CREATE TABLE calendly_marketing_db.gold_channel_cpb
WITH (
    format = 'PARQUET',
    external_location = 's3://calendly-marketing-datalake/gold/channel_cpb_final/'
) AS
SELECT
    COALESCE(c.booking_date, s.spend_date) AS report_date,
    COALESCE(c.channel, s.channel) AS channel,
    COALESCE(c.total_bookings, 0) AS total_bookings,
    COALESCE(c.unique_leads, 0) AS unique_leads,
    COALESCE(c.unique_events, 0) AS unique_events,
    ROUND(COALESCE(s.total_spend, 0), 2) AS total_spend,
    CASE
        WHEN COALESCE(c.total_bookings, 0) = 0 THEN NULL
        ELSE ROUND(s.total_spend / c.total_bookings, 2)
    END AS cpb
FROM calendly_marketing_db.gold_campaign_performance c
FULL OUTER JOIN (
    SELECT
        spend_date,
        channel,
        SUM(spend) AS total_spend
    FROM calendly_marketing_db.silver_marketing_spend
    GROUP BY spend_date, channel
) s
    ON c.booking_date = s.spend_date
   AND c.channel = s.channel;


SELECT *
FROM calendly_marketing_db.gold_channel_cpb
ORDER BY report_date, channel;

```
### GOLD Campaign Performance

  ```
  CREATE EXTERNAL TABLE calendly_marketing_db.gold_campaign_performance (
    booking_date DATE,
    channel STRING,
    total_bookings BIGINT,
    unique_leads BIGINT,
    unique_events BIGINT,
    first_booking_time STRING,
    last_booking_time STRING
)
STORED AS PARQUET
LOCATION 's3://calendly-marketing-datalake/gold/campaign_performance/';


Validate

SELECT *
FROM calendly_marketing_db.gold_campaign_performance
LIMIT 10;

```

### Gold Daily Booking Trends

```

CREATE EXTERNAL TABLE calendly_marketing_db.gold_daily_booking_trends (
    meeting_date DATE,
    meeting_day_of_week INT,
    meeting_hour INT,
    channel STRING,
    total_bookings BIGINT,
    unique_leads BIGINT
)
STORED AS PARQUET
LOCATION 's3://calendly-marketing-datalake/gold/daily_booking_trends/';

validate 
SELECT *
FROM calendly_marketing_db.gold_daily_booking_trends
LIMIT 10;
```


### Gold Employee Performance

```

CREATE EXTERNAL TABLE calendly_marketing_db.gold_employee_performance (
    employee_name STRING,
    employee_email STRING,
    channel STRING,
    total_meetings BIGINT,
    unique_leads BIGINT,
    first_meeting_time STRING,
    last_meeting_time STRING
)
STORED AS PARQUET
LOCATION 's3://calendly-marketing-datalake/gold/employee_performance/';

validate 


SELECT *
FROM calendly_marketing_db.gold_employee_performance
LIMIT 10;

```
![Gold Athena 1](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/athena%20gold/gold%20athena%201.png)

![Gold Athena 2](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/athena%20gold/gold%20athena%202.png)
