## Purpose

- Expose HTTPS POST endpoint for Calendly webhook.
  - POST /calendly/webhook
- Connected To
  - API Gateway → SQS Queue

## Create API Gateway SQS Role

- Go to:
  - IAM → Roles → Create role
- Trusted entity:
  - AWS service → API Gateway
- Role name:
  - api_gateway_sqs_integration_role

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSendMessageToCalendlyWebhookQueue",
      "Effect": "Allow",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:YOUR_ACCOUNT_ID:calendly-webhook-queue"
    }
  ]
}
```

# API Gateway Setup

- Go to:
  - AWS Console → API Gateway → Create API
- Choose:
  - REST API
-  Not HTTP API, because REST API is easier for direct AWS service integration with SQS.
- Click:
  - Build

## API Details

- Choose:
  - New API
- Name:
  - calendly-webhook-api
- Endpoint type:
  - Regional
- Click:
  - Create API
 
## Create Resource

- In the left panel:
  - Resources → Actions → Create Resource
- Resource name:
  - webhook
- Resource path:
  - /webhook
- Click:
  - Create Resource
 
## Create POST Method

- Select:
  - /webhook
- Then:
  - Actions → Create Method → POST
 
## Integration Setup

- Choose:
  - Integration type: AWS Service
  - AWS Region: us-east-1
  - AWS Service: SQS
  - HTTP method: POST
  - Action Type: Use path override
  - Path override:
    - YOUR_ACCOUNT_ID/calendly-webhook-queue
   
## Method Request
For now, keep defaults.

## Integration Request Mapping Template

- Go to:
    - Integration Request → Mapping Templates
- Add content type:
    - application/json
- Template:
    - Action=SendMessage&MessageBody=$util.urlEncode($input.body)
- URL request headers parameters:
    - Content-Type
- is set to:
    - application/x-www-form-urlencoded
 
## Method Response

- Set success response:
  - 200
 
## Deploy API

- Click:
    - Actions → Deploy API
- Deployment stage:
    - New Stage
- Stage name:
    - prod
- Deploy.
- Your final URL will look like:
    - https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/webhook

## Test with Postman

- POST to your API URL with sample webhook JSON.
- Expected result:
  - API Gateway → SQS → Lambda → S3 Bronze
- After test, check:
  - S3 → bronze/calendly/ingestion_date=YYYY-MM-DD/
 
## Postman Testing Steps

### Step 1 — Open Postman

- Click:
  - New Request

### Step 2 — Set Request Type

- Select:
  - POST

### Step 3 — Paste API URL

- Use:
  - https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/webhook

### Step 4 — Add Headers

- Go to:
  - Headers
- Add:
  - KEY	VALUE
- Content-Type	application/json

###  Step 5 — Add Body

- Go to:
  - Body
  - → raw
  - → JSON
- Paste:

```
{
  "event": "invitee.created",
  "payload": {
    "uri": "https://api.calendly.com/invitees/test_invitee_001",
    "created_at": "2026-05-24T18:30:00Z",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "scheduled_event": {
      "uri": "https://api.calendly.com/scheduled_events/test_event_001"
    },
    "tracking": {
      "utm_source": "facebook",
      "utm_campaign": "summer_campaign"
    }
  }
}

```

###  Step 6 — Click Send

- Expected response:
```
{
  "message": "Webhook received successfully"
}
```
- or:
  - 200 OK

###   Step 7 — Verify End-to-End Pipeline

- Go to:
- S3
  - → calendly-marketing-datalake
  - → bronze
  - → calendly
  - → ingestion_date=YYYY-MM-DD
- You should see a NEW JSON file.

<p align="center">
  <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/POSTMAN/POSTMAN%201.png" width="750"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/POSTMAN/POSTMAN%202.png" width="750"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/POSTMAN/POSTMAN%203.png" width="750"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/aaqibtariq/Calendly_Marketing_Insights/main/phases/AWS/ref%20files/POSTMAN/POSTMAN%204.png" width="750"/>
</p>
