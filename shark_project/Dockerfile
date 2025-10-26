FROM python:3.10-slim

WORKDIR /app

# Only copy requirements and install dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
