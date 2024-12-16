from app.config.aws import s3_client
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

BUCKET_NAME = "product-images"

def upload_image_to_s3(image):
    try:
        # Attempt to upload the image to S3
        s3_client.upload_fileobj(image.file, BUCKET_NAME, image.filename)
        # Return the URL after successful upload
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{image.filename}"
    except NoCredentialsError:
        logging.error("AWS credentials not found.")
        return "Error: AWS credentials not found."
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials.")
        return "Error: Incomplete AWS credentials."
    except ClientError as e:
        logging.error(f"An error occurred: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return f"Error: {str(e)}"
