import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Debe setearse ANTES de que cualquier parte del código importe keras
os.environ.setdefault('KERAS_BACKEND', os.getenv('KERAS_BACKEND', 'torch'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'classifier',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'staticfiles' / 'frontend'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# No database needed — using Drive for storage
DATABASES = {}

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

# Media (temporary local storage before uploading to Drive)
MEDIA_ROOT = BASE_DIR / 'media_temp'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

# CORS — adjust in production
CORS_ALLOW_ALL_ORIGINS = DEBUG

# ── Model config ──────────────────────────────────────────────
MODEL_PATH = BASE_DIR / os.getenv('MODEL_PATH', 'model/model.keras')
MODEL_INPUT_SIZE = (224, 224)   # adjust to match your model
MODEL_CLASSES = os.getenv('MODEL_CLASSES', '').split(',')  # e.g. "plastic,metal,glass"

# ── Google Drive config ───────────────────────────────────────
GOOGLE_DRIVE_CREDENTIALS_FILE = BASE_DIR / os.getenv(
    'GOOGLE_DRIVE_CREDENTIALS_FILE', 'credentials/service_account.json'
)
GOOGLE_OAUTH_TOKEN_FILE = BASE_DIR / os.getenv(
    'GOOGLE_OAUTH_TOKEN_FILE', 'credentials/token.json'
)

# Clave para el endpoint de subida de token. Sin valor = endpoint deshabilitado.
TOKEN_UPLOAD_SECRET = os.getenv('TOKEN_UPLOAD_SECRET', '')
