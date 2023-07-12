"""
Django settings for middlevel project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^y+9d$*3u8o8b!6tk4wn9kf36v0o1=jz#9wt8(vz(utvivz_oz'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'app',
    
    # "whitenoise.runserver_nostatic",
    'mail_templated',
    
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    # 'djoser.webauthn', # not working
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers ...',
    'allauth.socialaccount.providers.google',
    
    'corsheaders',
    
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'middlevel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'middlevel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'postgres',
        'PORT': 5432, #default port you don't need to mention in docker-compose
    },
    
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_mysql',
        'HOST': 'mysql_db',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {'sql_mode': 'STRICT_ALL_TABLES', 'charset': 'utf8mb4',},
    },
    
    # 'mongo': {'ENGINE': 'djongo','NAME': 'default_mongo',}
    # # # ---===--- # # #
    # 'mongo': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'default_mongo',
    #     'CLIENT': {
    #         'host': '127.0.0.1',
    #         'port': 27017,
    #         'authSource': 'admin',
    #     },
    #     'ENFORCE_SCHEMA': True
    # },
    # # # ---===--- # # #
    # 'mongo': {
    #     "ENGINE": "djongo",
    #     "NAME": 'mongo_db',
    #     "CLIENT": {
    #         "host": 'mongo',
    #         "port": 27017,
    #         "username": 'root',
    #         "password": 'root',
    #     },
    #     # 'TEST': {
    #     #     'MIRROR': 'default',
    #     # },
    # },
    # # # ---===--- # # #
    # 'mongo': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'student',
    #     'CLIENT': {
    #         'host': 'mongodb://mongodb:27017',
    #         'username': 'root',
    #         'password': 'mongoadmin',
    #         'authSource': 'admin',
    #         'authMechanism': 'SCRAM-SHA-1',
    #     }
    # }
}
"""
$ ./manage.py migrate
$ ./manage.py migrate --database=customers
>>> Author.objects.using("default")
>>> my_object.save(using="legacy_users")
>>> p.save(using="first")  # (statement 1)
>>> p.save(using="second")  # (statement 2)
>>> u = User.objects.using("legacy_users").get(username="fred")
"""


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC
DEBUG = True
ALLOWED_HOSTS = ['*']
#
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles'
]
#
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# STATIC

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=9),
}

# celery setting.
# REDIS_ADDRESS = 'redis:6379'
CELERY_BROKER_URL = f"redis://redis:6379/0"
# CELERY_RESULT_BACKEND = f"redis://{REDIS_ADDRESS}/0"

# ---:::--- Email Configuration ---:::---
# EMAIL_HOST = ''
# EMAIL_PORT = ''
EMAIL_HOST_USER = 'admin@admin.admin'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = ''
# EMAIL_USE_SSL = ''
# EMAIL_TIMEOUT = ''
# EMAIL_SSL_KEYFILE = ''
# EMAIL_SSL_CERTFILE = ''
#
# Email Backend Configuration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = BASE_DIR / 'EMAILS.txt'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = "smtp4dev"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 25

# whitenoise
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# STATIC_HOST = "http://127.0.0.1"
# STATIC_URL = STATIC_HOST + "/static/"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '10000/day'
    }
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
"""
from rest_framework.authtoken.models import Token
token = Token.objects.create(user=...)
print(token.key)
Authorization: Token ...TOKEN...
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
#
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
Authorization: Bearer ...JWT-Token...
"""

# djoser
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
}
"""
Available endpoints¶
/users/
/users/me/
/users/confirm/
/users/resend_activation/
/users/set_password/
/users/reset_password/
/users/reset_password_confirm/
/users/set_username/
/users/reset_username/
/users/reset_username_confirm/
/token/login/ (Token Based Authentication)
/token/logout/ (Token Based Authentication)
/jwt/create/ (JSON Web Token Authentication)
/jwt/refresh/ (JSON Web Token Authentication)
/jwt/verify/ (JSON Web Token Authentication)
"""

# allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
LOGIN_REDIRECT_URL = '/'
SITE_ID = 1
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": "426357936885-iq30inuqrbskh7d08d2mek31kghko5q6.apps.googleusercontent.com",
            "secret": "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",
            "key": "AIzaSyDEYbZtJvIsduC1n3cUcUWaYMjvi4CE2es"
        },
        # These are provider-specific settings that can only be
        # listed here:
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },
}

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://172.245.106.111",
    "http://172.245.106.111:8000",
]

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
