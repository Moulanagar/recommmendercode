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

# Step 1: Upgrade pip and install numpy first
RUN pip install --upgrade pip && pip install numpy

# Step 2: Now install the rest of the requirements
RUN pip install -r requirements.txt

# Copy rest of the app code (after dependencies to leverage Docker cache)
COPY . .

# Optional: pre-download sentence-transformers model if needed
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
