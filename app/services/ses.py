from app.config.aws import ses_client
import json

SENDER_EMAIL = "no-reply@example.com"

def send_low_stock_email(product_name):
    subject = "Low Stock Alert"
    body = f"The stock for {product_name} is critically low!"
    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": ["admin@example.com"]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )

def lambda_handler(event, context):

    # retrieve products with low stock from the database
    # Mock database or data source of products
    products = [
        {"id": 1, "name": "Product 1", "stock_quantity": 5, "price": 20.0},
        {"id": 2, "name": "Product 2", "stock_quantity": 2, "price": 10.0},
        {"id": 3, "name": "Product 3", "stock_quantity": 0, "price": 15.0},
        {"id": 4, "name": "Product 4", "stock_quantity": 3, "price": 50.0},
    ]

    for product in products:
        if product["stock_quantity"] <= 3:
            subject = f"Low stock alert for {product['name']}"
            body = f"The stock for {product['name']} has dropped to {product['stock_quantity']}. Please restock soon."
            to_address = "test@example.com"  # Replace with actual recipient
            send_low_stock_email(subject, body, to_address)
    
    return {
        "statusCode": 200,
        "body": json.dumps("Stock check completed and emails sent if necessary."),
    }