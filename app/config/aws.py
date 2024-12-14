import boto3

AWS_REGION = "us-east-1"
LOCALSTACK_ENDPOINT = "http://localhost:4566"

# S3 Client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=LOCALSTACK_ENDPOINT,
)

# SES Client
ses_client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    endpoint_url=LOCALSTACK_ENDPOINT,
)
