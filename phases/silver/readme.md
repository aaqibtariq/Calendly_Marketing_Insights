
# S3

- Create below folder
- calendly-marketing-emr-scripts
  - → create folder scripts
  - → upload file - silver_calendly_transform.py
 
# EMR Steps

- EMR → calendly-marketing-emr-cluster → Steps → Add step
- Type: Spark application
- Name: silver_calendly_transform
- Deploy mode: Cluster
- Spark-submit options:
  - --packages io.delta:delta-spark_2.12:3.2.0
- Application location:
  - s3://calendly-marketing-emr-scripts/scripts/silver_calendly_transform.py
- Arguments: Leave Blank
- Action on failure: Continue
- Click Add step

- Expected result:
  - Status: Pending → Running → Completed

- After it completes, check S3:
- calendly-marketing-datalake
  - → silver
    - → calendly_events_clean
   
# EMR Steps

- EMR → calendly-marketing-emr-cluster → Steps → Add step
- Type: Spark application
- Name: silver_marketing_spend
- Deploy mode: Cluster
- Spark-submit options:
  - --packages io.delta:delta-spark_2.12:3.2.0
- Application location:
  - s3://calendly-marketing-emr-scripts/scripts/silver_marketing_spend.py
- Arguments: Leave Blank
- Action on failure: Continue
- Click Add step

- Expected result:
  - Status: Pending → Running → Completed

- After it completes, check S3:
- calendly-marketing-datalake
  - → silver
    - → calendly_events_clean
   
![EMR Result for Silver 1](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/EMR%20result%20for%20silver%201.png)

![EMR Result for Silver 2](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/EMR%20result%20for%20silver.png)

![Silver Marketing Spend](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/silver%20marketing%20spend.png)


# validate from Athena

- Go to:
  - Amazon Athena → Query editor
  - Data source: AwsDataCatalog
  - Workgroup: primary
- query result location is:
  - s3://calendly-marketing-athena-results/
 
## Create database

```
CREATE DATABASE IF NOT EXISTS calendly_marketing_db;
```
### Register Silver Delta table

```
CREATE EXTERNAL TABLE IF NOT EXISTS calendly_marketing_db.silver_calendly_events_clean
LOCATION 's3://calendly-marketing-datalake/silver/calendly_events_clean/'
TBLPROPERTIES (
  'table_type' = 'DELTA'
);

CREATE EXTERNAL TABLE calendly_marketing_db.silver_marketing_spend (
    spend_date DATE,
    channel STRING,
    spend DOUBLE,
    source_file_name STRING,
    source_system STRING
)
PARTITIONED BY (
    ingestion_date DATE
)
STORED AS PARQUET
LOCATION 's3://calendly-marketing-datalake/silver/marketing_spend/';

MSCK REPAIR TABLE calendly_marketing_db.silver_marketing_spend;

SELECT *
FROM calendly_marketing_db.silver_marketing_spend
LIMIT 10;

```

### Validate row count

```
SELECT COUNT(*) AS total_rows
FROM calendly_marketing_db.silver_calendly_events_clean;

SELECT COUNT(*) AS total_rows
FROM calendly_marketing_db.silver_marketing_spend;
```

### Preview data shape

```
SELECT *
FROM calendly_marketing_db.silver_calendly_events_clean
LIMIT 10;

SELECT *
FROM calendly_marketing_db.silver_marketing_spend
LIMIT 10;

```
### Validate channel mapping

```
SELECT
  channel,
  COUNT(*) AS booking_count
FROM calendly_marketing_db.silver_calendly_events_clean
GROUP BY channel
ORDER BY booking_count DESC;

SELECT
    channel,
    SUM(spend) AS total_spend
FROM calendly_marketing_db.silver_marketing_spend
GROUP BY channel;
```
### Check duplicates
```
SELECT
  event_id,
  COUNT(*) AS duplicate_count
FROM calendly_marketing_db.silver_calendly_events_clean
GROUP BY event_id
HAVING COUNT(*) > 1;

SELECT
    spend_date,
    channel,
    source_file_name,
    COUNT(*) AS duplicate_count
FROM calendly_marketing_db.silver_marketing_spend
GROUP BY spend_date, channel, source_file_name
HAVING COUNT(*) > 1;


```

![Athena Silver 1](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/athena%20silver%201.png)

![Athena Silver 2](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/athena%20silver%202.png)

-  [Validate Channel Mapping CSV](https://github.com/aaqibtariq/Calendly_Marketing_Insights/blob/main/phases/AWS/ref%20files/Athena%20silver/Validate%20channel%20mapping.csv)

