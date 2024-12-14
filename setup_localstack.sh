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
awslocal ses verify-email-identity --email-address test@example.com

echo "LocalStack setup complete!"
