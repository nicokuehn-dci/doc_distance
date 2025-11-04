Django Deployment Guide
This document outlines the deployment setup and configuration for our Django project, including database setup, static file handling, environment configuration, and build process.:paket: Dependencies
Install the following dependencies required for production:


pip install dj-database-url==3.0.1
pip install 'whitenoise[brotli]'
pip install gunicorn uvicorn

:zahnrad: Database Configuration
We use PostgreSQL as the production database, configured via dj-database-url.
In your settings.py:


import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/mysite',
        conn_max_age=600
    )
}

This configuration automatically parses the database URL from the environment (e.g. DATABASE_URL variable).:ziegelsteine: Creating the PostgreSQL Database
Run the following commands to create a local or remote database:


# Access PostgreSQL shell
psql -U postgres

# Inside psql:
CREATE DATABASE mysite;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mysite TO myuser;

Then set your environment variable accordingly:


export DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/mysite"

:erde_afrika: Environment Variables
Set up the following environment variables in your deployment environment:
VariableDescriptionExampleSECRET_KEYDjango secret keyexport SECRET_KEY="your-secret-key"DEBUGEnables debug mode (not for production)export DEBUG=FalseDATABASE_URLPostgreSQL connection stringexport DATABASE_URL="postgresql://user:pass@host:5432/dbname"HOSTAllowed host for the environmentexport HOST="yourdomain.com"
Example (on Linux/macOS):


export SECRET_KEY="supersecretkey"
export DEBUG=False
export HOST="yourdomain.com"
export DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/mysite"

:ziegelsteine: Static Files Configuration
Install and configure WhiteNoise for static file management.
In settings.py:


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must come right after security middleware
    ...
]

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WhiteNoise will handle compression and caching of static assets automatically.:rakete: Build Script
Create a build.sh file at the project root:


#!/usr/bin/env bash
set -o errexit  # exit on errors

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

Then make the script executable:


chmod a+x build.sh

This script will install dependencies, collect static files, and apply database migrations.:schlüssel: Security & Host Settings
Update your settings for security and environment handling:


SECRET_KEY = os.getenv('SECRET_KEY', 'some-crazy-secret')
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = []
HOST = os.environ.get('HOST')
if HOST:
    ALLOWED_HOSTS.append(HOST)

This ensures your project adapts automatically based on environment variables.:kompass: Running the Server (Gunicorn + Uvicorn)
For production, use Gunicorn as the main process manager and Uvicorn workers for ASGI support.
Example command:


gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

Screenshot 2025-11-04 at 11.49.18.png 
Screenshot 2025-11-04 at 11.49.18.png
11:50 Uhr
Note: There will always be a problem. It is important to remain patient, have grit, check logs, (turn off some settings, turn them back on, push constantly until something is fixed).Usually following instructions gets you to a destination but some times there are happy accidents.