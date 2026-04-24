FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/tmp

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd -M -r appuser && chown -R appuser:appuser /app
USER appuser

# No EXPOSE, no gunicorn — Lambda handles all of that
CMD ["python", "-m", "awslambdaric", "app.main.handler"]