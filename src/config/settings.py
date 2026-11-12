import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

if not ENV_FILE.exists():
    ENV_FILE = BASE_DIR.parent / ".env"

load_dotenv(ENV_FILE)

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    x.strip()
    for x in os.environ["ALLOWED_HOSTS"].split(",")
    if x.strip()
]
INSTALLED_APPS = [
 "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions",
 "django.contrib.messages","django.contrib.staticfiles","django.contrib.postgres",
 "rest_framework","rest_framework_simplejwt","django_filters","drf_spectacular","pgvector.django",
 "usuarios","catalogo","zeladoria",
]
MIDDLEWARE = [
 "django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
 "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
 "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,
 "OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}
AUTH_USER_MODEL="usuarios.Usuario"
LANGUAGE_CODE="pt-br"; TIME_ZONE="America/Sao_Paulo"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"
STATIC_ROOT=BASE_DIR / "staticfiles"
MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR/"media"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK={
 "DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication","rest_framework.authentication.SessionAuthentication"),
 "DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticated",),
 "DEFAULT_FILTER_BACKENDS":("django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),
 "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
 "DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":20,
}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=30),"REFRESH_TOKEN_LIFETIME":timedelta(days=1)}
SPECTACULAR_SETTINGS={"TITLE":"Portal Cidadão Seguro API","DESCRIPTION":"Catálogo e Zeladoria Urbana","VERSION":"1.0.0"}
