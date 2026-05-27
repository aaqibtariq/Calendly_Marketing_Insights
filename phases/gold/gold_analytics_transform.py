from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    min,
    max,
    sum as spark_sum,
    round,
    coalesce,
    lit,
    when
)

spark = (
    SparkSession.builder
    .appName("gold_analytics_transform")
    .getOrCreate()
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

silver_calendly_path = "s3://calendly-marketing-datalake/silver/calendly_events_clean/"
silver_spend_path = "s3://calendly-marketing-datalake/silver/marketing_spend/"

gold_campaign_path = "s3://calendly-marketing-datalake/gold/campaign_performance/"
gold_daily_path = "s3://calendly-marketing-datalake/gold/daily_booking_trends/"
gold_employee_path = "s3://calendly-marketing-datalake/gold/employee_performance/"
gold_cpb_path = "s3://calendly-marketing-datalake/gold/channel_cpb/"

# --------------------------------------------------
# Read Silver Delta Tables
# --------------------------------------------------

silver_df = spark.read.format("delta").load(silver_calendly_path)
spend_df = spark.read.format("delta").load(silver_spend_path)

# --------------------------------------------------
# GOLD 1: Campaign Performance
# --------------------------------------------------

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

gold_campaign_df.write.format("delta").mode("overwrite").save(gold_campaign_path)

# --------------------------------------------------
# GOLD 2: Daily Booking Trends
# --------------------------------------------------

gold_daily_df = (
    silver_df
    .groupBy("meeting_date", "meeting_day_of_week", "meeting_hour", "channel")
    .agg(
        count("*").alias("total_bookings"),
        countDistinct("invitee_email").alias("unique_leads")
    )
)

gold_daily_df.write.format("delta").mode("overwrite").save(gold_daily_path)

# --------------------------------------------------
# GOLD 3: Employee Performance
# --------------------------------------------------

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

gold_employee_df.write.format("delta").mode("overwrite").save(gold_employee_path)

# --------------------------------------------------
# GOLD 4: Channel CPB / Attribution
# --------------------------------------------------

spend_agg_df = (
    spend_df
    .groupBy("spend_date", "channel")
    .agg(
        spark_sum("spend").alias("total_spend")
    )
)

gold_cpb_df = (
    gold_campaign_df.alias("c")
    .join(
        spend_agg_df.alias("s"),
        (col("c.booking_date") == col("s.spend_date")) &
        (col("c.channel") == col("s.channel")),
        "full_outer"
    )
    .select(
        coalesce(col("c.booking_date"), col("s.spend_date")).alias("report_date"),
        coalesce(col("c.channel"), col("s.channel")).alias("channel"),
        coalesce(col("c.total_bookings"), lit(0)).alias("total_bookings"),
        coalesce(col("c.unique_leads"), lit(0)).alias("unique_leads"),
        coalesce(col("c.unique_events"), lit(0)).alias("unique_events"),
        round(coalesce(col("s.total_spend"), lit(0.0)), 2).alias("total_spend"),
        when(
            coalesce(col("c.total_bookings"), lit(0)) == 0,
            None
        ).otherwise(
            round(coalesce(col("s.total_spend"), lit(0.0)) / col("c.total_bookings"), 2)
        ).alias("cpb")
    )
)

gold_cpb_df.write.format("delta").mode("overwrite").save(gold_cpb_path)

print("Gold analytics transformation completed successfully")
print(f"Campaign Performance: {gold_campaign_path}")
print(f"Daily Booking Trends: {gold_daily_path}")
print(f"Employee Performance: {gold_employee_path}")
print(f"Channel CPB: {gold_cpb_path}")
