"""
Django settings for missionbit project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import dj_database_url
from dotenv import load_dotenv
import sys

load_dotenv()
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "h7ti$^0sg*9vmi^2r)%t+o-%3-aa$!f+xsn5ckag@8g8osuz8n"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split()


# Application definition

INSTALLED_APPS = [
    "student.apps.StudentConfig",
    "teacher.apps.TeacherConfig",
    "volunteer.apps.VolunteerConfig",
    "staff.apps.StaffConfig",
    "donor.apps.DonorConfig",
    "attendance.apps.AttendanceConfig",
    "home.apps.HomeConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",  # <- Social Django Oauth Google
    "crispy_forms",  # <- Crispy forms
    "coverage",  # <- for testing
    "salesforce",  # <- salesforce database
    "django_q",  # <- For queueing tasks
    "storages",  # <- Storing uploaded files in Azure Storage
    "static",  # <- Accessing Static HTML templates
    "django_celery_beat", # <- Scheduled tasks
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <- Whitenoise for serving static assets
]

ROOT_URLCONF = "missionbit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "static/html"),
            os.path.join(BASE_DIR, "html/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",  # <- Social Django Oauth Google
                "social_django.context_processors.login_redirect",  # <- Social Django Oauth Google
                "context_processors.user_groups",
                "context_processors.user_classroom",
            ]
        },
    }
]

WSGI_APPLICATION = "missionbit.wsgi.application"


# Postgres/Salesforce Database Setup
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# Using DATABASE_URL for configuration
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://localhost/mbdb", conn_max_age=600
    ),
    "salesforce": {
        "ENGINE": "salesforce.backend",
        "CONSUMER_KEY": os.getenv("SALESFORCE_CONSUMER_KEY"),
        "CONSUMER_SECRET": os.getenv("SALESFORCE_CONSUMER_SECRET"),
        "USER": os.getenv("SALESFORCE_USER"),
        "PASSWORD": os.getenv("SALESFORCE_PASSWORD"),
        "HOST": os.getenv("SALESFORCE_HOST"),
    },
}

DATABASE_ROUTERS = ["salesforce.router.ModelRouter"]

"""
if 'test' in sys.argv:
    DATABASES['salesforce'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_sfdb'
    }
"""


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Google authentication backend

AUTHENTICATION_BACKENDS = (
    "social_core.backends.open_id.OpenIdAuth",
    "social_core.backends.google.GoogleOpenId",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_POSTGRES_JSONFIELD = True


# Django Q Settings

Q_CLUSTER = {
    "name": "DjangoORM",
    "timeout": 1200,
    "save_limit": 10,
    "catch_up": False,
    "orm": "default",
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "djangoq-localmem",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Gmail backend

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

LOGIN_URL = "home-landing_page"

LOGIN_REDIRECT_URL = "home-home"

CRISPY_TEMPLATE_PACK = "bootstrap4"

# Azure file storage
DEFAULT_FILE_STORAGE = "missionbit.azure_storage_backend.CustomAzureStorage"
AZURE_EMULATED_MODE = os.getenv("AZURE_EMULATED_MODE") == "true"
AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")
AZURE_CUSTOM_DOMAIN = os.getenv(
    "AZURE_CUSTOM_DOMAIN", f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
)
AZURE_PROTOCOL = "http" if AZURE_EMULATED_MODE else "https"
MEDIA_URL = os.getenv(
    "MEDIA_URL", f"{AZURE_PROTOCOL}://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"
)

INSTAUSERID = os.getenv("INSTAUSERID")
INSTATOKEN = os.getenv("INSTATOKEN")

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
"""

from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {
    'users_contacts_sync': {
        'task': 'staff.tasks.add_salesforce_contacts_to_postgres',
        'schedule': crontab()
    },
    'userprofile_sync': {
        'task': 'staff.tasks.sync_userprofile_data_with_salesforce_data',
        'schedule': crontab()
    }
}
