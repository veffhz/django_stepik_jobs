import os

import django_heroku
from configurations import Configuration, values


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ALLOWED_HOSTS = ['127.0.0.1']

    USE_THOUSAND_SEPARATOR = True

    LOGIN_URL = '/login/'

    LOGIN_REDIRECT_URL = '/'

    LOGOUT_REDIRECT_URL = '/'

    AUTH_USER_MODEL = 'vacancies.CustomUser'

    ROOT_APPS = [
        'vacancies',
    ]

    INSTALLED_APPS = [
        'dal',
        'dal_select2',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ] + ROOT_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'jobs_project.urls'

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

    WSGI_APPLICATION = 'jobs_project.wsgi.application'

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

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    LANGUAGE_CODE = 'ru-ru'

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    MEDIA_COMPANY_IMAGE_DIR = 'company_images'

    NO_LOGO_PIC = 'no_logo.png'

    MEDIA_SPECIALITY_IMAGE_DIR = 'speciality_images'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'debug.log',
            },
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        },
    }


class Dev(Common):
    DEBUG = values.BooleanValue(True)

    SECRET_KEY = 'd+nyf4sg5+ffv(gezkp=7nbbxppmx69gyj_8)(#%o8)(5+jjv%'

    INTERNAL_IPS = [
        '127.0.0.1',
    ]


class Prod(Common):
    DEBUG = os.getenv('DEBUG', '').lower() == 'true'

    EXTERNAL_URL = os.getenv('EXTERNAL_URL')

    if EXTERNAL_URL:
        Common.ALLOWED_HOSTS.append(EXTERNAL_URL)

    locals = locals()
    locals.update(Common.__dict__)
    django_heroku.settings(locals, logging=False)
