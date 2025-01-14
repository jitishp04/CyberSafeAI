# Import necessary modules and classes
import os
import sys
from pathlib import Path

# Adjust BASE_DIR to point to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(os.path.join(BASE_DIR, "../../ai_model"))

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-rzx(y(ac&9#^6+79z3ehz0a-v1v^8deye24-qdf!##y0@%vhku'

DEBUG = True

ALLOWED_HOSTS = ['*'] #To allow easier connecion when testing deployment

# Application definition
INSTALLED_APPS = [
    # Default Django apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app',
    'CSA_AdminApp',
    'frontend',
]

MIDDLEWARE = [
    # Default middleware...
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Ensure the ROOT_URLCONF points to the correct urls.py in config
ROOT_URLCONF = 'config.urls'

# Templates directory configuration
TEMPLATES_DIR = BASE_DIR / 'frontend' / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],  # Include your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Default context processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ensure WSGI_APPLICATION points to the correct wsgi.py in config
WSGI_APPLICATION = 'config.wsgi.application'

TESTING = 'test' in sys.argv
print(f"Is testing: {TESTING}")

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('USER_DB_PATH', BASE_DIR / 'backend' / 'db.sqlite3'),
    },
    'admin_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('ADMIN_DB_PATH', BASE_DIR / 'backend' / 'admin_db.sqlite3'),
    },
}


DATABASE_ROUTERS = ['CSA_AdminApp.db_router.AdminDbRouter']



# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'