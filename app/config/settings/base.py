from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Path settings
CONFIG_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = CONFIG_DIR.resolve().parent
ROOT_DIR = APPS_DIR.resolve().parent
ENV_DIR = Path(ROOT_DIR / 'env').resolve()

# Load env from file
dotenv_path = Path(ENV_DIR / '.env').resolve()
load_dotenv(dotenv_path=dotenv_path)

# Base setting
DEBUG = environ['DJANGO_DEBUG']
SECRET_KEY = environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = environ['DJANGO_ALLOWED_HOSTS'].split(',')
DOMAIN_NAME = environ['DOMAIN_NAME'] if not DEBUG else 'http://127.0.0.1:8000/'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'static'
STATICFILES_DIRS = (APPS_DIR / 'static',)

MEDIA_URL = '/media/'
MEDIA_ROOT = APPS_DIR / 'media'

# Users
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
LOGIN_URL = '/users/signin/'
LOGIN_REDIRECT_URL = '/index/'
LOGOUT_REDIRECT_URL = '/users/signin/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'crispy_forms',
    'captcha',

    # My apps
    'common.apps.CommonConfig',
    'users.apps.UsersConfig',
    'code_files.apps.CodeFilesConfig',
    'code_checker.apps.CodeCheckerConfig',
    'email_sender.apps.EmailSenderConfig',
    'reports.apps.ReportsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            APPS_DIR / 'common',
            APPS_DIR / 'users',
            APPS_DIR / 'code_files',
            APPS_DIR / 'reports',
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

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

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'
