# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    libavcodec-extra \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/main.py .

# Create model directory and copy model files from project root
RUN mkdir -p /app/model
COPY model/best_model.pth /app/model/
COPY model/scaler.pkl /app/model/
COPY model/label_encoder.pkl /app/model/

# Expose port (Cloud Run uses PORT env variable)
EXPOSE 8080
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application with Cloud Run port
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
