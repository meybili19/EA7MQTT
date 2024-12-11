# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy your application files to the container
COPY . /app

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]