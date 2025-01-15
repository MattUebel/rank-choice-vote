# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Create a working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker’s caching
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 for our app
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
