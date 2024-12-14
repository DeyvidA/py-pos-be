from app.config.aws import s3_client

BUCKET_NAME = "product-images"

def upload_image_to_s3(image):
    s3_client.upload_fileobj(image.file, BUCKET_NAME, image.filename)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{image.filename}"
