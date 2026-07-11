# Use official slim Python runtime
FROM python:3.10-slim

# Set environment properties
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy files
COPY . /app/

# Install production-ready frameworks
RUN pip install --no-cache-dir fastapi uvicorn PyJWT psycopg2-binary cryptography

# Expose API port
EXPOSE 8000

# Start Uvicorn REST API server
CMD ["uvicorn", "backend.infrastructure.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
