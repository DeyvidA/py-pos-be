#!/bin/bash

# Configure AWS CLI for LocalStack
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack

# Set up S3 bucket
echo "Creating S3 bucket..."
awslocal s3 mb s3://product-images

# Verify S3 bucket
echo "Listing S3 buckets..."
awslocal s3 ls

# Set up SES
echo "Setting up SES..."
# Verify email identity for SES
awslocal ses verify-email-identity --email-address test@example.com
awslocal ses verify-email-identity --email-address no-reply@example.com
awslocal ses list-identities

echo "SES setup complete!"

# Define the AWS endpoint for LocalStack
export AWS_ENDPOINT="http://localhost:4566"

# Create Lambda function (without .zip file)
echo "Creating Lambda function..."
# aws lambda create-function \
#     --function-name CheckProductStock \
#     --runtime python3.9 \
#     --handler app.services/ses.lambda_handler \
#     --role arn:aws:iam::000000000000:role/lambda-role \
#     --function-code "fileb://app/services/ses.py" \
#     --endpoint-url $AWS_ENDPOINT

# Create Lambda Function with correct ZIP file
aws lambda create-function \
    --function-name CheckProductStock \
    --runtime python3.9 \
    --handler ses.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --zip-file fileb://app/services/ses.zip \
    --endpoint-url $AWS_ENDPOINT


# Create EventBridge Rule for scheduling Lambda execution every minute
echo "Creating EventBridge Rule..."
aws events put-rule \
    --schedule-expression "rate(1 minute)" \
    --name CheckProductStockSchedule \
    --endpoint-url $AWS_ENDPOINT

# Add Lambda as a target for the EventBridge Rule
echo "Adding Lambda target to EventBridge Rule..."
aws events put-targets \
    --rule CheckProductStockSchedule \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:000000000000:function:CheckProductStock" \
    --endpoint-url $AWS_ENDPOINT

# Grant EventBridge permission to invoke Lambda
echo "Granting permissions to EventBridge to invoke Lambda..."
aws lambda add-permission \
    --function-name CheckProductStock \
    --statement-id AllowEventBridgeInvocation \
    --action "lambda:InvokeFunction" \
    --principal events.amazonaws.com \
    --source-arn "arn:aws:events:us-east-1:000000000000:rule/CheckProductStockSchedule" \
    --endpoint-url $AWS_ENDPOINT

# Verify SES Email identity (to receive low stock notifications)
echo "Verifying SES Email Identity..."
aws ses verify-email-identity \
    --email-address no-reply@example.com \
    --endpoint-url $AWS_ENDPOINT

echo "LocalStack setup and Lambda function deployment complete!"
