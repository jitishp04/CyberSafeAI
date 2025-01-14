FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Install system dependencies (if needed). Uncomment if required.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them first for better cache utilization
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of your code
# Make sure the backend, ai_model, and frontend directories exist locally
COPY backend /app/backend
COPY ai_model /app/ai_model
COPY frontend /app/frontend


# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Remove local databases to ensure the container doesn't use them
RUN rm -f /app/backend/db.sqlite3 /app/backend/admin_db.sqlite3

# Run Django commands to prepare the environment
WORKDIR /app/backend

# Make migrations and migrate
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Launch the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
