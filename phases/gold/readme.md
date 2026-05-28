
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



