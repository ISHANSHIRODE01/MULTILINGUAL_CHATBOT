# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for audio libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

# Create a script to run both services
# Render listens on the PORT env var (default 10000), but we can force it.
# We will run Streamlit on port 80 (or $PORT) to be the main entry point.
# Backend will run on localhost:8080.

ENV PORT=8501

RUN echo '#!/bin/bash\n\
    python -m src.backend.app --port 8080 & \n\
    streamlit run src/frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0\n\
    wait' > /app/start.sh && chmod +x /app/start.sh

# Run the start script
CMD ["/app/start.sh"]
