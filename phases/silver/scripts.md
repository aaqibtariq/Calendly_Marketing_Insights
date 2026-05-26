### silver_marketing_spend

```
import sys
from pyspark.context import SparkContext
from pyspark.sql.functions import col, lower, to_date, trim
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

bronze_path = "s3://calendly-marketing-datalake/bronze/spend/"
silver_output_path = "s3://calendly-marketing-datalake/silver/marketing_spend/"

df = spark.read.option("multiline", "true").json(bronze_path)

silver_df = (
    df.select(
        to_date(col("date")).alias("spend_date"),
        lower(trim(col("channel"))).alias("channel"),
        col("spend").cast("double").alias("spend"),
        col("source_file_name"),
        col("source_system"),
        to_date(col("ingestion_date")).alias("ingestion_date")
    )
    .filter(
        col("spend_date").isNotNull()
        & col("channel").isNotNull()
        & col("spend").isNotNull()
    )
    .dropDuplicates(["spend_date", "channel", "source_file_name"])
)

silver_df.write.mode("overwrite").partitionBy("ingestion_date").parquet(silver_output_path)

print("Silver marketing spend created successfully")
print(f"Output path: {silver_output_path}")

job.commit()


```



### silver_calendly_transform

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, hour, dayofweek, when

spark = SparkSession.builder.appName("glue_silver_calendly_transform").getOrCreate()

bronze_path = "s3://calendly-marketing-datalake/bronze/calendly/"
silver_path = "s3://calendly-marketing-datalake/silver/calendly_events_clean/"

df = spark.read.option("multiline", "true").json(bronze_path)

silver_df = (
    df
    .filter(col("event_name") == "invitee.created")
    .select(
        col("event_id"),
        col("event_name"),
        col("invitee_uri"),
        col("scheduled_event_uri"),
        col("raw_payload.payload.email").alias("invitee_email"),
        col("raw_payload.payload.name").alias("invitee_name"),
        col("raw_payload.payload.status").alias("invitee_status"),
        col("raw_payload.payload.timezone").alias("invitee_timezone"),
        col("raw_payload.payload.created_at").alias("booking_created_at"),
        col("raw_payload.payload.scheduled_event.start_time").alias("meeting_start_time"),
        col("raw_payload.payload.scheduled_event.end_time").alias("meeting_end_time"),
        col("raw_payload.payload.scheduled_event.name").alias("meeting_name"),
        col("raw_payload.payload.scheduled_event.event_type").alias("event_type_uri"),
        col("raw_payload.payload.scheduled_event.event_memberships")[0]["user_email"].alias("employee_email"),
        col("raw_payload.payload.scheduled_event.event_memberships")[0]["user_name"].alias("employee_name"),
        col("raw_payload.payload.tracking.utm_source").alias("utm_source"),
        col("raw_payload.payload.tracking.utm_campaign").alias("utm_campaign"),
        col("ingestion_timestamp"),
        col("ingestion_date")
    )
)

silver_df = (
    silver_df
    .withColumn(
        "channel",
        when(col("event_type_uri") == "https://api.calendly.com/event_types/d639ecd3-8718-4068-955a-436b10d72c78", "facebook_paid_ads")
        .when(col("event_type_uri") == "https://api.calendly.com/event_types/dbb4ec50-38cd-4bcd-bbff-efb7b5a6f098", "youtube_paid_ads")
        .when(col("event_type_uri") == "https://api.calendly.com/event_types/bb339e98-7a67-4af2-b584-8dbf95564312", "tiktok_paid_ads")
        .otherwise("unknown")
    )
    .withColumn("booking_date", to_date(col("booking_created_at")))
    .withColumn("meeting_date", to_date(col("meeting_start_time")))
    .withColumn("meeting_hour", hour(col("meeting_start_time")))
    .withColumn("meeting_day_of_week", dayofweek(col("meeting_start_time")))
)

silver_df = silver_df.filter(col("channel") != "unknown")

silver_df.write.format("delta").mode("overwrite").save(silver_path)

print("Glue Silver Calendly transformation completed successfully")
print(f"Output path: {silver_path}")
```
