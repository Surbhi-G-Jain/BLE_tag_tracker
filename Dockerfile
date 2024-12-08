# Use Python base image
FROM python:3.8-slim

# Set the working directory to /myproject
WORKDIR /myproject

# Copy the current directory contents into /myproject in the container
COPY . /myproject

# Update pip before installing dependencies
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your application
CMD ["python", "BLE_Tag_tracker.py"]
