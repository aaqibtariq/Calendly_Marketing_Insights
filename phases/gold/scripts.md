### gold_analytics_transform

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, countDistinct, min, max

spark = SparkSession.builder.appName("glue_gold_analytics_transform").getOrCreate()

silver_path = "s3://calendly-marketing-datalake/silver/calendly_events_clean/"

gold_campaign_path = "s3://calendly-marketing-datalake/gold/campaign_performance/"
gold_daily_path = "s3://calendly-marketing-datalake/gold/daily_booking_trends/"
gold_employee_path = "s3://calendly-marketing-datalake/gold/employee_performance/"

silver_df = spark.read.format("delta").load(silver_path)

gold_campaign_df = (
    silver_df
    .groupBy("booking_date", "channel")
    .agg(
        count("*").alias("total_bookings"),
        countDistinct("invitee_email").alias("unique_leads"),
        countDistinct("event_id").alias("unique_events"),
        min("booking_created_at").alias("first_booking_time"),
        max("booking_created_at").alias("last_booking_time")
    )
)

gold_daily_df = (
    silver_df
    .groupBy("meeting_date", "meeting_day_of_week", "meeting_hour", "channel")
    .agg(
        count("*").alias("total_bookings"),
        countDistinct("invitee_email").alias("unique_leads")
    )
)

gold_employee_df = (
    silver_df
    .groupBy("employee_name", "employee_email", "channel")
    .agg(
        count("*").alias("total_meetings"),
        countDistinct("invitee_email").alias("unique_leads"),
        min("meeting_start_time").alias("first_meeting_time"),
        max("meeting_start_time").alias("last_meeting_time")
    )
)

gold_campaign_df.write.format("delta").mode("overwrite").save(gold_campaign_path)
gold_daily_df.write.format("delta").mode("overwrite").save(gold_daily_path)
gold_employee_df.write.format("delta").mode("overwrite").save(gold_employee_path)

print("Gold analytics transformation completed successfully")
```
