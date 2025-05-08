FROM python:3.11-slim-buster

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV AGENT_PORT=50052

# Expose the gRPC port
EXPOSE 50052

# Command to run the application
CMD ["python", "main.py"]
