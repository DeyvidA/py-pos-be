# Check if any existing files should be removed before proceeding
# Remove any existing lambda ZIP file if it exists to avoid conflicts
if [ -f lambda_function.zip ]; then
    echo "Removing existing lambda_function.zip file..."
    rm lambda_function.zip
fi

# Generate the folder for the Lambda function
# Install the required Python packages into the Lambda folder
# Required packages: boto3, requests, sqlalchemy, psycopg2, psycopg2-binary
mkdir -p lambda
echo "Installing required packages into the lambda folder..."
pip install -t lambda boto3 requests sqlalchemy psycopg2 psycopg2-binary

# Copy the necessary files into the Lambda folder
# Files: app/services/ses.py and app/config/aws.py
echo "Copying SES service file and AWS config file into the lambda folder..."
mkdir -p lambda/app/services lambda/app/config
cp app/services/ses.py lambda/app/services
cp app/config/aws.py lambda/app/config

# Create a ZIP file with the Lambda folder's contents for deployment
echo "Creating a ZIP file of the lambda folder for deployment..."
cd lambda
zip -r ../lambda_function.zip .
cd ..

# remove the lambda folder
rm -rf lambda

# Ensure necessary permissions for the project folder
echo "Setting permissions for the project directory..."
sudo chmod -R 777 /home/deyvida/Projects/study/python/fastapi/postgres_data

