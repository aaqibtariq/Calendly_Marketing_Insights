
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

