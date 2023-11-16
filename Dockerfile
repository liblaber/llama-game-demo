# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8001
ENV UVICORN_RELOAD=true

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY api /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install 'uvicorn[standard]'

# Expose port 8000 for Uvicorn to listen on
EXPOSE 8001

# Run Uvicorn with the desired options
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
