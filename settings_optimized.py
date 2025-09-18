# settings_optimized.py - Configuración optimizada para producción y desarrollo

import os
from pathlib import Path
from decouple import config, Csv
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-h$lbw0usy3k$o49bn1t5xvm%l@_!rsz=lgr+41^1^sc7mx0y$y')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Configuración de hosts permitidos más robusta
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='localhost,127.0.0.1',
    cast=Csv()
)

# Configuración CORS optimizada
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:4200,https://liveplan-frontend.web.app',
    cast=Csv()
)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Headers de seguridad adicionales
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    'livePlan',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware optimizado
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Debe estar primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livePlan.middleware.RequestLoggingMiddleware',  # Nuestro middleware personalizado
]

ROOT_URLCONF = 'liveplanBackend.urls'

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

WSGI_APPLICATION = 'liveplanBackend.wsgi.application'

# Configuración de base de datos optimizada
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Usar dj-database-url para parsing automático
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Configuración manual para desarrollo/producción
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='postgres'),
            'USER': config('DB_USER', default='postgres.zdvtuqfxcrhxdmoffntq'),
            'PASSWORD': config('DB_PASSWORD', default='1411'),
            'HOST': config('DB_HOST', default='aws-0-us-west-1.pooler.supabase.com'),
            'PORT': config('DB_PORT', default='6543'),
            # Optimizaciones de conexión
            'OPTIONS': {
                'MAX_CONNS': 20,
                'connect_timeout': 10,
                'options': '-c default_transaction_isolation=read_committed'
            },
            'CONN_MAX_AGE': 600,  # Reutilizar conexiones por 10 minutos
        }
    }

# Optimizaciones de base de datos adicionales
if not DEBUG:
    DATABASES['default']['OPTIONS'].update({
        'ATOMIC_REQUESTS': True,  # Wrappear cada request en transacción
        'AUTOCOMMIT': True,
    })

# Configuración de caché optimizada
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 100,
                    'retry_on_timeout': True,
                },
                'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            },
            'KEY_PREFIX': config('CACHE_KEY_PREFIX', default='liveplan'),
            'TIMEOUT': 60 * 15,  # 15 minutos por defecto
        }
    }
else:
    # Fallback a caché en memoria
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'liveplan-cache',
            'TIMEOUT': 60 * 15,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
                'CULL_FREQUENCY': 3,
            }
        }
    }

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 días
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Password validation
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
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'livePlan.pagination_utils.OptimizedPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': config('THROTTLE_ANON', default='100/hour'),
        'user': config('THROTTLE_USER', default='1000/hour'),
    },
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Configuración de logging optimizada
LOGGING_DIR = BASE_DIR / 'logs'
LOGGING_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '[{asctime}] {levelname} {name}: {message} | {pathname}:{lineno}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed' if DEBUG else 'json',
            'level': 'DEBUG' if DEBUG else 'INFO'
        },
        'file_app': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'app.log',
            'maxBytes': 50 * 1024 * 1024,  # 50MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'INFO'
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'error.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'detailed',
            'level': 'ERROR'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_app'],
            'level': 'INFO',
            'propagate': False
        },
        'livePlan': {
            'handlers': ['console', 'file_app', 'file_error'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    }
}

# Configuración de seguridad para producción
if not DEBUG:
    # HTTPS settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Session security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF security
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Lax'
    
    # Additional security headers
    X_FRAME_OPTIONS = 'DENY'
    
    # Logging más estricto en producción
    LOGGING['loggers']['django.security'] = {
        'handlers': ['file_error'],
        'level': 'WARNING',
        'propagate': False
    }

# Configuraciones de performance
if not DEBUG:
    # Optimizaciones de templates
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    
    # Compresión de respuestas
    MIDDLEWARE.insert(1, 'django.middleware.gzip.GZipMiddleware')
    
    # Optimizaciones de archivos estáticos
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Configuración de email (opcional)
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
)

if not DEBUG:
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@liveplan.com')

# Configuración de archivos de media en producción
if not DEBUG:
    # Usar servicios de almacenamiento en la nube
    DEFAULT_FILE_STORAGE = config(
        'DEFAULT_FILE_STORAGE',
        default='django.core.files.storage.FileSystemStorage'
    )
    
    # AWS S3 settings (si se usa)
    if 'storages.backends.s3boto3' in DEFAULT_FILE_STORAGE:
        AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
        AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
        AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
        AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
        AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
        AWS_DEFAULT_ACL = None
        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
        }

# Configuración de monitoreo (Sentry, etc.)
SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN and not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=True,
            ),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,  # Ajustar según necesidades
        send_default_pii=False,
        environment=config('ENVIRONMENT', default='production'),
    )

# Configuraciones personalizadas del sistema financiero
FINANCIAL_CALCULATION_TIMEOUT = config('FINANCIAL_CALCULATION_TIMEOUT', default=300, cast=int)  # 5 minutos
MAX_YEARS_PROJECTION = config('MAX_YEARS_PROJECTION', default=10, cast=int)
DEFAULT_CURRENCY = config('DEFAULT_CURRENCY', default='MXN')
DEFAULT_TIMEZONE = TIME_ZONE

# Configuración de tareas asíncronas (Celery - opcional)
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default=REDIS_URL)
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default=REDIS_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Configuraciones de desarrollo
if DEBUG:
    # Django Debug Toolbar
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
        }
    except ImportError:
        pass
    
    # Django Extensions
    try:
        import django_extensions
        INSTALLED_APPS.append('django_extensions')
    except ImportError:
        pass

# Validación de configuración crítica
def validate_critical_settings():
    """Valida configuraciones críticas al iniciar"""
    errors = []
    
    if not SECRET_KEY or SECRET_KEY == 'django-insecure-h$lbw0usy3k$o49bn1t5xvm%l@_!rsz=lgr+41^1^sc7mx0y$y':
        errors.append("SECRET_KEY must be set to a secure value in production")
    
    if not DEBUG and not ALLOWED_HOSTS:
        errors.append("ALLOWED_HOSTS must be configured for production")
    
    if not DATABASE_URL and not all([
        config('DB_NAME', default=None),
        config('DB_USER', default=None),
        config('DB_PASSWORD', default=None),
        config('DB_HOST', default=None),
    ]):
        errors.append("Database configuration is incomplete")
    
    if errors:
        raise Exception(f"Critical configuration errors: {', '.join(errors)}")

# Ejecutar validación solo en producción
if not DEBUG:
    validate_critical_settings()