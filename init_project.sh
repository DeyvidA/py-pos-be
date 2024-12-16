#!/bin/bash

# Step 1: Create a Python virtual environment
# This creates a directory named '.venv' where the virtual environment will be stored
python3 -m venv .venv

# Step 2: Activate the virtual environment
# On Linux/MacOS, use 'source' to activate the environment; Windows users can use '.venv\\Scripts\\activate'
source .venv/bin/activate

# Step 3: Install project dependencies from requirements.txt
# This will install all the Python libraries listed in the requirements.txt file
pip install -r requirements.txt

# Step 4: Start Docker containers in the background (detached mode)
# This will start up your Docker containers defined in 'docker-compose.yml'
docker-compose up -d

# Step 5: Run database migrations with Alembic
# This ensures that the database schema is up to date
alembic upgrade head

# Step 6: Ensure that the 'generate_lambada_file.sh' script is executable
# This changes the permissions of the script to make it executable
chmod +x generate_lambada_file.sh

# Step 7: Run the FastAPI application with Uvicorn
# The '--reload' flag enables automatic reloading of the server on code changes
uvicorn app.main:app --reload

# Step 8: Ensure that the 'setup_localstack.sh' script is executable
chmod +x setup_localstack.sh

# Step 9: Run the 'setup_localstack.sh' script (if required)
# This script might be used to set up or configure LocalStack for AWS local development
./setup_localstack.sh

# End of the script
# Display a message indicating the successful completion of the project setup
echo "Project initialization completed successfully!"
