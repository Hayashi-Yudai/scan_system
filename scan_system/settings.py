from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

DATA_UPLOAD_MAX_MEMORY_SIZE = None

# SASS
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "static")
SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r"^.+\.(sass|scss)$"
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = "compressed"
SASS_TEMPLATE_EXTS = [".html", ".haml"]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# '0&=py-ucs50e6=gk5(^oy#6f@h%np!=zjzd1-vv59$r(&kc^9m'
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "archive.apps.ArchiveConfig",
    "toppage.apps.ToppageConfig",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "scan_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "scan_system.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "deploy"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

CORS_ORIGIN_WHITELIST = (
    "http://localhost:8000",
    "http://127.0.0.1:8000",
)

LOG_BASE_DIR = BASE_DIR / "log"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},
    "handlers": {
        "debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_BASE_DIR / "debug.log",
            "formatter": "simple",
        },
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_BASE_DIR / "info.log",
            "formatter": "simple",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOG_BASE_DIR / "warning.log",
            "formatter": "simple",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_BASE_DIR / "error.log",
            "formatter": "simple",
        },
    },
    "root": {"handlers": ["debug", "info", "warning", "error"], "level": "DEBUG"},
}
