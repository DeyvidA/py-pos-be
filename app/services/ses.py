import os
import json
import logging
import requests
from app.config.aws import ses_client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV_API_URL = os.getenv("API_URL")

# Use the ngrok public URL for the API
API_URL = "https://a8d0-2803-2d60-1121-5f-340b-50c-fd3e-381d.ngrok-free.app/products/low-stock"
# API_URL = f"{ENV_API_URL}/products/low-stock"

SENDER_EMAIL = "no-reply@example.com"

def send_low_stock_email(product_name):
    subject = "Low Stock Alert"
    body = f"The stock for {product_name} is critically low!"
    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": ["test@example.com"]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event, indent=2))
    try:
        # Use requests to connect to the ngrok public URL
        response = requests.get(API_URL)

        if response.status_code == 200:
            # Parse the response (assuming it's a JSON list of products)
            products = response.json()

            # Loop through the products and send emails for each one
            for product in products:
                send_low_stock_email(product['name'])

            return {
                'statusCode': 200,
                'body': 'Success'
            }
        else:
            # Handle the case where the API request fails
            logger.error(f"Failed to retrieve low stock products: {response.status_code} - {response.text}")
            return {
                'statusCode': 500,
                'body': 'Failed to retrieve low stock products'
            }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise
