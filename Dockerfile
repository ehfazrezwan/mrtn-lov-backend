# Base image for dev and prod stages
FROM python:3.9-alpine AS base

# Install system dependencies
RUN apk add --no-cache gcc postgresql-dev musl-dev libffi-dev openssl-dev

# Set the working directory
WORKDIR /app

# Install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the application code
COPY . .

# Set the user to run the container as a non-root user
USER 1001

# Development target
FROM base AS dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Production target
FROM base AS prod
RUN rm -rf tests/ && \
    rm -rf __pycache__/ && \
    rm -rf *.pyc && \
    rm -rf *.egg-info/

CMD ["gunicorn", "main:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
