from app.config.aws import ses_client
import json
import requests

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use the ngrok public URL for the API
API_URL = "https://4d7e-2803-2d60-1121-5f-630c-a41e-e54b-b34.ngrok-free.app/products/low-stock"

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
    print("Received event: ", event)
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
