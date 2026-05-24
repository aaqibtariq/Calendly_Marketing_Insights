## Roles Needed

```
lambda_webhook_ingestion_role
lambda_spend_ingestion_role
emr_service_role
emr_ec2_instance_profile
athena_query_role
```

### Permissions Needed

```
S3 read/write
CloudWatch logs
SQS read/write
DLQ access
EventBridge trigger access
EMR access
Glue Catalog access
Athena query access
KMS encryption/decryption
Secrets Manager read
```
