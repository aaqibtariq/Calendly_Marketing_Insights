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

## lambda_spend_ingestion_role
Use this for the Lambda that pulls marketing spend JSON and writes to Bronze S3.

Trusted entity
- Choose:
  - AWS service → Lambda


```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "WriteSpendDataToBronze",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-datalake",
        "arn:aws:s3:::calendly-marketing-datalake/bronze/spend/*"
      ]
    },
    {
      "Sid": "ReadEmrOrConfigScriptsIfNeeded",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-emr-scripts/*"
      ]
    },
    {
      "Sid": "CloudWatchLogsForLambda",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}

```

Also attach AWS managed policy:
- AWSLambdaBasicExecutionRole

## lambda_webhook_ingestion_role
Use this for Calendly webhook Lambda.
Trusted entity
- Choose:
  - AWS service → Lambda
```{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadWebhookMessagesFromSQS",
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:ChangeMessageVisibility"
      ],
      "Resource": [
        "arn:aws:sqs:us-east-1:YOUR_ACCOUNT_ID:calendly-webhook-queue",
        "arn:aws:sqs:us-east-1:YOUR_ACCOUNT_ID:calendly-webhook-dlq"
      ]
    },
    {
      "Sid": "WriteCalendlyWebhookToBronze",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-datalake",
        "arn:aws:s3:::calendly-marketing-datalake/bronze/calendly/*"
      ]
    },
    {
      "Sid": "CloudWatchLogsForLambda",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}

```

Also attach:
-  AWSLambdaBasicExecutionRole
Replace:
-  YOUR_ACCOUNT_ID with your AWS account ID.

## emr_service_role

Use this for Amazon EMR service.

Trusted entity
- Choose:
  - AWS service → EMR
  - Attach AWS managed policy
    - AmazonEMRServicePolicy_v2

That is usually enough for the EMR service role.

- attach this incline policy
- emr_service_ec2_network_policy
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEMREC2NetworkOperations",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateSecurityGroup",
        "ec2:DeleteSecurityGroup",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:RevokeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupEgress",
        "ec2:CreateTags",
        "ec2:Describe*",
        "ec2:RunInstances",
        "ec2:TerminateInstances",
        "ec2:CreateFleet",
        "ec2:ModifyInstanceAttribute",
        "ec2:ModifyNetworkInterfaceAttribute",
        "ec2:CreateLaunchTemplate",
        "ec2:CreateLaunchTemplateVersion",
        "ec2:DeleteLaunchTemplate",
        "ec2:DeleteLaunchTemplateVersions"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowPassEMREC2Role",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::****:role/emr_ec2_instance_profile"
    }
  ]
}

```

## emr_ec2_instance_profile
Use this for EC2 instances inside EMR cluster.

Trusted entity
- Choose:
  - AWS service → EC2

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadWriteDataLake",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-datalake",
        "arn:aws:s3:::calendly-marketing-datalake/*"
      ]
    },
    {
      "Sid": "ReadScriptsBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-emr-scripts",
        "arn:aws:s3:::calendly-marketing-emr-scripts/*"
      ]
    },
    {
      "Sid": "AthenaResultsAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-athena-results",
        "arn:aws:s3:::calendly-marketing-athena-results/*"
      ]
    },
    {
      "Sid": "GlueCatalogAccess",
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:CreateDatabase",
        "glue:GetTable",
        "glue:GetTables",
        "glue:CreateTable",
        "glue:UpdateTable",
        "glue:DeleteTable",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:CreatePartition",
        "glue:BatchCreatePartition",
        "glue:UpdatePartition"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchLogsForEMR",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}

```
Also attach managed policy:
- AmazonElasticMapReduceforEC2Role
