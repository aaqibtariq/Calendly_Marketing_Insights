## Create EC2 IAM Role

- Go to:
  - IAM → Roles → Create role
- Trusted entity:
  - AWS service
- Use case:
  - EC2
- Role name:
  - ec2_streamlit_athena_role
- Attach inline policy:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AthenaAccess",
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults",
        "athena:StopQueryExecution",
        "athena:GetWorkGroup"
      ],
      "Resource": "*"
    },
    {
      "Sid": "GlueCatalogRead",
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetPartition",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3AthenaAndDatalakeAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::calendly-marketing-athena-results",
        "arn:aws:s3:::calendly-marketing-athena-results/*",
        "arn:aws:s3:::calendly-marketing-datalake",
        "arn:aws:s3:::calendly-marketing-datalake/*"
      ]
    }
  ]
}
```
- Policy name:
  - ec2_streamlit_athena_policy
 
## EC2 setup

- Go to:
  - EC2 → Instances → Launch instance
- Use these settings:
  - Name: calendly-streamlit-dashboard
  - AMI: Amazon Linux 2023
  - Instance type: t2.micro or t3.micro
  - Key pair: create/select one
  - Network settings
- Allow:
  - SSH 22        Your IP
  - Custom TCP 8501    0.0.0.0/0
  - HTTP 80       optional
- Port 8501 is for Streamlit.
- IAM instance profile
- Select:
  - ec2_streamlit_athena_role
- Storage
  - 8 GB gp3
- Click:
  - Launch instance

## Install Updates

```

sudo dnf update -y
sudo dnf install python3-pip -y

python3 --version
pip3 --version

pip3 install streamlit pandas plotly boto3 pyathena
sudo dnf install git -y

git clone https://github.com/aaqibtariq/Calendly_Marketing_Insights.git
cd Calendly_Marketing_Insights/phases/streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

```

