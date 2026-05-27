from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, to_date, trim

# --------------------------------------------------
# Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("silver_marketing_spend_transform")
    .getOrCreate()
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

bronze_path = "s3://calendly-marketing-datalake/bronze/spend/"
silver_output_path = "s3://calendly-marketing-datalake/silver/marketing_spend/"

# --------------------------------------------------
# Read Bronze Spend JSON
# --------------------------------------------------

df = spark.read.option("multiline", "true").json(bronze_path)

# --------------------------------------------------
# Clean and Transform Spend Data
# --------------------------------------------------

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

# --------------------------------------------------
# Write Silver Spend as Delta
# --------------------------------------------------

(
    silver_df
    .write
    .format("delta")
    .mode("overwrite")
    .partitionBy("ingestion_date")
    .save(silver_output_path)
)

print("Silver marketing spend transformation completed successfully")
print(f"Output path: {silver_output_path}")
