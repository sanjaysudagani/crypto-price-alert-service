# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (Docker cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY config/ ./config/
# Set environment variables (optional defaults)
ENV PYTHONUNBUFFERED=1

# Run the service
CMD ["python", "-m", "app.main"]
