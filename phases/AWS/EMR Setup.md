## Purpose

Run Spark jobs to transform data.

### Jobs
- bronze_to_silver_calendly.py
- bronze_to_silver_spend.py
- silver_to_gold_metrics.py
Reads From
- s3://calendly-marketing-datalake/bronze/
Writes To
- s3://calendly-marketing-datalake/silver/
- s3://calendly-marketing-datalake/gold/
