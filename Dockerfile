FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pre-install pip and numpy before anything else
RUN pip install --upgrade pip && pip install numpy==1.26.4

# COPY requirements early to leverage Docker layer caching
COPY requirements.txt .

# Force install numpy again and ensure it's before torch
RUN pip install --force-reinstall numpy==1.26.4 \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
