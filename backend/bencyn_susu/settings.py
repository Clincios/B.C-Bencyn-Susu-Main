"""
Django settings for bencyn_susu project.

For production deployment, ensure:
1. DEBUG is set to False
2. SECRET_KEY is set to a secure random value
3. ALLOWED_HOSTS includes your domain
4. CORS_ALLOWED_ORIGINS includes your frontend domain
5. Database is configured for production (PostgreSQL recommended)
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# In production, set SECRET_KEY in environment variables
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG=False in production via environment variable
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts - REQUIRED for production
# Set ALLOWED_HOSTS in environment variables with your domain(s)
# Example: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
ALLOWED_HOSTS_RAW = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')

# Auto-detect Render.com deployment and add domain automatically
# Render sets RENDER=true automatically, and provides RENDER_SERVICE_URL
is_render = os.environ.get('RENDER') == 'true'
render_service_url = os.environ.get('RENDER_SERVICE_URL', '')

if is_render or render_service_url:
    # Extract hostname from Render service URL
    if render_service_url:
        from urllib.parse import urlparse
        # Handle both with and without protocol
        if '://' not in render_service_url:
            render_service_url = f'https://{render_service_url}'
        parsed = urlparse(render_service_url)
        if parsed.hostname and parsed.hostname not in ALLOWED_HOSTS_RAW:
            # Add the specific Render domain to allowed hosts
            ALLOWED_HOSTS_RAW = f"{ALLOWED_HOSTS_RAW},{parsed.hostname}"

# Filter out empty strings to prevent validation errors
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_RAW.split(',') if host.strip()]

# Additional safety: If DEBUG is False and we're on Render but domain not in ALLOWED_HOSTS,
# Django will reject requests. The above should handle it, but if not, set ALLOWED_HOSTS explicitly.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bencyn_susu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bencyn_susu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# For production, use PostgreSQL. Configure via DATABASE_URL or individual settings

# Check if DATABASE_URL is set (for production with PostgreSQL)
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Production: Use PostgreSQL from DATABASE_URL
    # Format: postgresql://user:password@host:port/dbname
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
    except ImportError:
        # Fallback if dj-database-url not installed
        # Install with: pip install dj-database-url
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Check if individual PostgreSQL settings are provided
    DB_NAME = config('DB_NAME', default=None)
    if DB_NAME:
        # Use PostgreSQL with individual settings
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME,
                'USER': config('DB_USER', default='postgres'),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='5432'),
                'CONN_MAX_AGE': 600,
            }
        }
    else:
        # Development: Use SQLite (fallback)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration for serving static files in production
# WhiteNoise allows Django to serve static files efficiently without a separate web server
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB max file size
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
# Rate limiting configuration
# Increased limits to accommodate multiple API calls per page load
# A single page load can make 5-10 API calls (hero-images, testimonials, services, etc.)
# With navigation and refreshes, users need reasonable limits
if DEBUG:
    # More lenient limits for development
    THROTTLE_RATES = {
        'anon': '1000/hour',  # ~16 requests per minute - allows for development testing
        'user': '5000/hour'    # Authenticated users: 5000 requests per hour
    }
else:
    # Production limits - still generous but more controlled
    THROTTLE_RATES = {
        'anon': '500/hour',   # ~8 requests per minute - reasonable for normal usage
        'user': '2000/hour'   # Authenticated users: 2000 requests per hour
    }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Default, but individual views can override
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Rate limiting for API endpoints
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': THROTTLE_RATES
}

# CORS settings
# REQUIRED for production - set your frontend domain(s)
# Example: CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOWED_ORIGINS_RAW = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000'
)
# Filter out empty strings to prevent CORS validation errors
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_RAW.split(',') if origin.strip()]

CORS_ALLOW_CREDENTIALS = True

# Additional CORS settings for production
if not DEBUG:
    # Only allow configured origins in production
    CORS_ALLOW_ALL_ORIGINS = False
    # Allow credentials for authenticated requests
    CORS_ALLOW_CREDENTIALS = True

# Email settings (configure for production)
# For production, use SMTP backend:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourdomain.com')

# Development: Use console backend
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Security settings for production
if not DEBUG:
    # HTTPS/SSL - Force HTTPS in production
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Session and CSRF - Secure cookies only
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Additional security
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # Prevent clickjacking
    X_CONTENT_TYPE_OPTIONS = 'nosniff'

# Logging configuration
# Production: Configure file-based logging or use a logging service
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Production: Add file handler
        # 'file': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': BASE_DIR / 'logs' / 'django.log',
        #     'maxBytes': 1024 * 1024 * 10,  # 10 MB
        #     'backupCount': 5,
        #     'formatter': 'verbose',
        # },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Production: Create logs directory if it doesn't exist
if not DEBUG:
    LOG_DIR = BASE_DIR / 'logs'
    LOG_DIR.mkdir(exist_ok=True)
