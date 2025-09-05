# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including audio and text-to-speech support
RUN apt-get update && apt-get install -y \
    build-essential \
    flac \
    portaudio19-dev \
    libportaudio2 \
    libasound2-dev \
    espeak \
    espeak-data \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install faiss-cpu for vector store
RUN pip install faiss-cpu

# Install Python dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]