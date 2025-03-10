import pathlib

import configurations

from . import env


class Settings(configurations.Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-h&!9=4=^-4lce7g*$!w9d@9!6wy!0_k*cj2fg_kwzt2!i4lfbv"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

    # ----------
    # Application definition
    # ----------

    @property
    def INSTALLED_APPS(self) -> list[str]:
        return [
            # Django
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            # Local
            "nutrimise.data.pgvector",
            "nutrimise.data.ingredients",
            "nutrimise.data.menus",
            "nutrimise.data.recipes",
            "nutrimise.interfaces.admin.apps.AdminConfig",
            "nutrimise.interfaces.management.apps.ManagementConfig",
        ]

    MIDDLEWARE = [
        # Django
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "nutrimise.config.urls"

    WSGI_APPLICATION = "nutrimise.config.wsgi.application"

    # ----------
    # Media settings
    # ----------

    MEDIA_ROOT: pathlib.Path = BASE_DIR / "media"
    MEDIA_URL: str = "/media/"
    MEDIA_BASE_URL: str = "http://localhost:8000/media"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                BASE_DIR / "interfaces" / "admin" / "templates",
                BASE_DIR / "domain" / "embeddings" / "_prompts" / "templates",
            ],
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

    FIXTURE_DIRS = [BASE_DIR.parents[1] / "fixtures"]

    # ----------
    # Database
    # ----------

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.as_str("DB_NAME"),
            "USER": env.as_str("DB_USER"),
            "PASSWORD": env.as_str("DB_PASSWORD"),
            "HOST": env.as_str("DB_HOST"),
            "PORT": env.as_int("DB_PORT", default=5432),
        }
    }

    # Default primary key field type
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # ----------
    # Password validation
    # ----------

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

    # ----------
    # Internationalization
    # ----------

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = False

    # ----------
    # Static files (CSS, JavaScript, Images)
    # ----------

    STATIC_URL = "static/"
    STATIC_ROOT = "static/"

    # ----------
    # Embeddings
    # ----------

    OPENAI_API_KEY = env.as_str("OPENAI_API_KEY")

    EMBEDDING_VENDOR = env.as_str("EMBEDDING_VENDOR", default="FAKE")

    DATA_EXTRACTION_VENDOR = env.as_str("DATA_EXTRACTION_VENDOR", default="FAKE")


class DevSettings(Settings):
    @property
    def INSTALLED_APPS(self) -> list[str]:
        installed_apps = [
            # Third party
            "django_extensions",
            *super().INSTALLED_APPS,
        ]
        return installed_apps
