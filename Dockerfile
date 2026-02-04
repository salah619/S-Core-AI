# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies (ffmpeg for pydub/whisper, build-essential for some pip packages)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (optional, can be passed during run)
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
