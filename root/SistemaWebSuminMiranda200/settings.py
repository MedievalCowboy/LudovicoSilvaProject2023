"""
Django settings for SistemaWebSuminMiranda200 project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
import os
from django.contrib import messages
import environ
from datetime import timedelta


import pymysql
pymysql.install_as_MySQLdb()

env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

#DEBUG_PROPAGATE_EXCEPTIONS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    "crispy_bootstrap4",
    "tempus_dominus",
    'django_filters',
    'widget_tweaks',
    #apps
    'mainwebsite'
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    ##
    'mainwebsite.middleware.AuditMiddleware',
    'mainwebsite.middleware.UpdateLastActivityMiddleware',
]

ROOT_URLCONF = 'SistemaWebSuminMiranda200.urls'

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
                
                ##
                
                'mainwebsite.context_processors.theme_context',
                'mainwebsite.context_processors.user_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'SistemaWebSuminMiranda200.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        'OPTIONS':{
            'sql_mode':'traditional'
        }
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



LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'

DATE_INPUT_FORMATS = ['%Y-%m-%d']  # Formato ISO para inputs
DATE_FORMAT = 'd/m/Y'  # Formato para mostrar en templates

USE_I18N = True
USE_L10N = False
USE_TZ = True

#CONFIGURACION DE SESIONES
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/ordenes/'
LOGOUT_REDIRECT_URL=''
AUTO_LOGOUT = {'IDLE_TIME':timedelta(minutes=10), 'MESSAGE':'Tu sesión de usuario a expirado. Inicie sesión nuevamente para continuar.'}

# Tiempo de inactividad en segundos (20 minutos = 20 * 60)
SESSION_COOKIE_AGE = 1200

# Renovar la sesión en cada solicitud (actualiza el contador de inactividad)
SESSION_SAVE_EVERY_REQUEST = True

# Opcional: Forzar a que la sesión expire al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # (False para usar SESSION_COOKIE_AGE)

# Asegura usar base de datos para las sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.db" 

#CONFIGURACION DE MENSAJES
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}



STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "mainwebsite", "static"),
    ]


MEDIA_URL = '/media/'
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')




# CONFIGURACION DE EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'   
EMAIL_PORT = 587       # gmail smtp server port
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # Use your email account
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD") # For gmail use app password
EMAIL_USE_TLS = True     # for SSL communication use EMAIL_USE_SSL
EMAUL_USE_SSL = False


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
