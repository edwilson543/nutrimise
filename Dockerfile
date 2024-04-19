# Pull official base image.
FROM python:3.11-slim-buster

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=nutrimise.config.settings
ENV DJANGO_CONFIGURATION=Settings

# Copy over files.
WORKDIR /app
COPY ./requirements/app-requirements.txt requirements.txt
COPY deployment/entrypoint.sh ./entrypoint.sh
COPY pyproject.toml manage.py .env ./
COPY src ./src

# Install dependencies.
RUN pip install --upgrade pip
RUN pip install -e .

# Add a non-root 'app' user to group 'app'.
RUN groupadd app
RUN useradd app -g app

# Transfer ownership of all files to the non-root user.
RUN chmod +x ./entrypoint.sh
RUN chown -R app:app .

# Change user to the app user.
USER app

# Run WSGI server using Gunicorn.
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
