
# EMR Step

- Name: gold_analytics_transform
- Type: Spark application
- Deploy mode: Cluster
- Application location: s3://calendly-marketing-emr-scripts/scripts/gold_analytics_transform.py
- Spark-submit options: --packages io.delta:delta-spark_2.12:3.2.0
- Arguments: blank
- Action on failure: Continue

- Expected S3 output:
  - gold/campaign_performance/
  - gold/daily_booking_trends/
  - gold/employee_performance/
 


  # AThena

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
