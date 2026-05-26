from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_date, hour, dayofweek, when

spark = (
    SparkSession.builder
    .appName("silver_calendly_transform")
    .getOrCreate()
)

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

print("Silver Calendly Delta table created successfully")
print(f"Output path: {silver_path}")