import os
import logging
import yaml

from logging.handlers import RotatingFileHandler

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['c57f4652f7a2.ngrok.io', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'santapp.apps.SantappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'secret_santa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'secret_santa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, '../static/')

CONFIG_PATH = os.path.join(BASE_DIR, '../config.yaml')

with open(CONFIG_PATH, 'r') as f:
    config_yaml = yaml.safe_load(f.read())

API_KEY = config_yaml['vk']['token']
VK_CONFIRMATION_CODE = config_yaml['vk']['confirmation_code']

SECRET_KEY = config_yaml['django']['secret']
MESSAGE_TIMEOUT = config_yaml['server']['message_timeout']

LOG_FILE = config_yaml['server']['log_file']

HOST = config_yaml['server']['host']
PORT = config_yaml['server']['port']

LOG_FORMAT = '%(name)s - %(levelname)s - %(asctime)s # %(message)s'

logger = logging.getLogger()

log_handler = RotatingFileHandler(LOG_FILE,
                                  maxBytes=50 * 2**20,
                                  backupCount=50)

log_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%I:%M:%S'))

logger.addHandler(log_handler)
logger.setLevel(logging.INFO)