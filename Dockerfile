# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Collect static files (nếu có)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run Django server
CMD ["gunicorn", "GameArt.wsgi:application", "--bind", "0.0.0.0:8000"]