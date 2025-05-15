# Base image
FROM python:3.11-slim

# Set environment variables để không tạo file .pyc và để stdout log đúng
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies trước để tránh lỗi khi cài các package như psycopg2, Pillow, v.v.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (nếu có static)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "GameArt.wsgi:application", "--bind", "0.0.0.0:8000"]