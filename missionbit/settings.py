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
load_dotenv()
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h7ti$^0sg*9vmi^2r)%t+o-%3-aa$!f+xsn5ckag@8g8osuz8n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split()


# Application definition

INSTALLED_APPS = [
    'student.apps.StudentConfig',
    'teacher.apps.TeacherConfig',
    'volunteer.apps.VolunteerConfig',
    'staff.apps.StaffConfig',
    'donor.apps.DonorConfig',
    'home.apps.HomeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django', # <- Social Django Oauth Google
    'crispy_forms', # <- Crispy forms
    'coverage', # <- for testing
    'salesforce' # <- salesforce database
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

ROOT_URLCONF = 'missionbit.urls'

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
                'social_django.context_processors.backends',  # <- Social Django Oauth Google
                'social_django.context_processors.login_redirect', # <- Social Django Oauth Google
            ],
        },
    },
]

WSGI_APPLICATION = 'missionbit.wsgi.application'


# Postgres Database Setup
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# Using DATABASE_URL for configuration
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://localhost/mbdb',
        conn_max_age=600
    ),
    'salesforce': {
        'ENGINE': 'salesforce.backend',
        'CONSUMER_KEY': os.getenv("SALESFORCE_CONSUMER_KEY"),
        'CONSUMER_SECRET': os.getenv("SALESFORCE_CONSUMER_SECRET"),
        'USER': os.getenv("SALESFORCE_USER"),
        'PASSWORD': os.getenv("SALESFORCE_PASSWORD"),
        'HOST': os.getenv("SALESFORCE_HOST"),
    }
}

DATABASE_ROUTERS = [
    "salesforce.router.ModelRouter"
]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

#Google authentication backend

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = 'home-landing_page'

LOGIN_REDIRECT_URL = 'home-home'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
