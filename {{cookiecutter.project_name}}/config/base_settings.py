{% if cookiecutter.celery == 'y' %}
import datetime
{% endif %}

import os
import environ

root = environ.Path(__file__) - 2  # get root of the project
env = environ.Env()
environ.Env.read_env()  # reading .env file

SITE_ROOT = root()

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = []

SITE_ID = 1

DEBUG = env.bool("DEBUG", default=False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

SITE_ID = 1


# Application definition


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csrf",
                "django.template.context_processors.static",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("DB_NAME", default="djangocms_demo_local"),
        "HOST": env.str("DB_HOST", default="localhost"),
        "USER": env.str("DB_USER", default="postgres"),
        "PASSWORD": env.str("DB_PASSWORD", default=""),
        "PORT": env.str("DB_PORT", default=""),
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "de"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = root.path("collected_static")
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static"),)

MEDIA_ROOT = root.path("media")
MEDIA_URL = "/media/"

LANGUAGES = [
    ("de", "German"),
]

AUTH_USER_MODEL = "custom_user.CustomUser"

{% if cookiecutter.celery == 'y' %}
GRAPHENE = {
    "SCHEMA": "config.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware",],
}
GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(minutes=10),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
}
{% endif %}

PROTOCOL = "http"