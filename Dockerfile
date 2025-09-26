FROM python:3.11-slim

# set noninteractive for apt
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps required for some Python packages (and for compiling wheels)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copy Pipfile and Pipfile.lock (Pipenv will read the lockfile)
COPY Pipfile Pipfile.lock /app/

# upgrade pip, install pipenv and install pinned dependencies into system python
RUN python -m pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile

# copy project files
COPY . /app

# Create directory for staticfiles to collect into
RUN mkdir -p /app/staticfiles

# Make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port; Railway will supply $PORT at runtime so binding happens then.
EXPOSE 8000

# Default envs (overridden by Railway environment variables)
ENV DJANGO_SETTINGS_MODULE=Todolist.settings
ENV PYTHONPATH=/app

# Use the entrypoint to run migrations & collectstatic, then start gunicorn
CMD ["/app/entrypoint.sh"]
