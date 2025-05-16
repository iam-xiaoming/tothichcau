# Sử dụng Python slim để nhẹ
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tạo thư mục làm việc
WORKDIR /app

# Cài đặt thư viện hệ thống (Postgres client, gcc)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy toàn bộ source code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Chạy gunicorn server
CMD ["gunicorn", "GameArt.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]