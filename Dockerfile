# Python lightweight base image
FROM python:3.9-slim

# Working directory for the container
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install -r requirements.txt

# Copy your Flask application code
COPY . .

# Expose the port where your Flask app runs (usually 5000)
EXPOSE 5000

# Specify the command to run your Flask app
CMD ["python", "app.py"]  # Replace
