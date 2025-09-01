# Start from the official Python Alpine image
FROM python:3.11-alpine
 
# Set working directory inside the container
WORKDIR /app
 
# Install system dependencies (if needed)
# 'gcc' and 'musl-dev' are needed for packages with native extensions
RUN apk add --no-cache gcc musl-dev libffi-dev
 
# Copy requirement file and install dependencies
COPY requirements.txt .
 
RUN pip install --upgrade pip
 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy your Python app files
COPY . .
 
# Set environment variables (optional)
# ENV PYTHONUNBUFFERED=1
 
# Define the command to run your app
CMD ["streamlit", "run","app.py"]