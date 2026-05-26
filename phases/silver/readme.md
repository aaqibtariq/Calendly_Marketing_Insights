
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

```

### Validate row count

```
SELECT COUNT(*) AS total_rows
FROM calendly_marketing_db.silver_calendly_events_clean;
```

### Preview data shape

```
SELECT *
FROM calendly_marketing_db.silver_calendly_events_clean
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
```
### Check duplicates
```
SELECT
  event_id,
  COUNT(*) AS duplicate_count
FROM calendly_marketing_db.silver_calendly_events_clean
GROUP BY event_id
HAVING COUNT(*) > 1;

```

