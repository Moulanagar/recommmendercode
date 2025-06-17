# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies early to cache better
COPY requirements.txt .

# Pre-install sentence-transformers (to prevent model download at runtime)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of the app code (after dependencies to leverage Docker cache)
COPY . .

# Ensure model is already available in local path
# Optional: check that `models/minilm_model/config.json` etc. exist in your repo

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
