# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . /app

# Install system dependencies for Debian-based systems (you mentioned running on WSL)
RUN apt-get update && \
    apt-get install -y python3-dev build-essential

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies from requirements.txt within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your application runs (adjust as needed)
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=src/main.py

# Initialize the database (you can adjust the command as needed)
RUN flask initdb

# Command to run your application
CMD ["python", "src/main.py"]