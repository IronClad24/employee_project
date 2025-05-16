# Base Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic without input (safe if DEBUG=True)
RUN python manage.py collectstatic --noinput || true

# Expose Django dev port
EXPOSE 8000

# Run migrations, seed data, then start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput && gunicorn employee_project.wsgi:application --bind 0.0.0.0:8000"]
