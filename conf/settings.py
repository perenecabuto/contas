# -*- encoding : utf-8 -*-
# Django settings for contas project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

WSGI_APPLICATION = 'conf.'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/contas.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'me@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'me@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = 'b&g+#fttt31h#h!8!w055!9)o-l_q6)8j)+_qnyyx%s!t@(h!v'

# Login
LOGIN_REDIRECT_URL = '/'

# NodeFs
NODEFS_PROFILE_MODULE = 'conf.nodefs_schema'
#NODEFS_TREE_DEFAULT_PATH = '/users/perenecabuto'
#NODEFS_TREE_DYNAMIC_PATH_CALLBACK = 'controle.callbacks.get_current_user_path'
NODEFS_TREE_DISCOVER_URL_CALLBACK = 'controle.callbacks.get_node_url'

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt_BR'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Media
MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Static
STATIC_ROOT = 'static/'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'possessions.middleware.AuthRequiredMiddleware',
)


# Auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'possessions.auth.OpenIDBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

LOGIN_EXEMPT_URLS = ['/login-complete/']
# EndAuth


CACHES = {
    'default': {
        'BACKEND': 'johnny.backends.memcached.MemcachedCache',
        'LOCATION': ['127.0.0.1:11211'],
        'JOHNNY_CACHE': False,
    }
}

JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_contas'

ROOT_URLCONF = 'conf.urls'

WSGI_APPLICATION = 'conf.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',

    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (
    'templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    #'registration',
    'debug_toolbar',
    'django_openid_auth',

    'controle',
    'django_nodefs',
    'possessions',

    'alert',
)


DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            #'formatter': 'brief',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },

        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            #'formatter': 'precise',
            'filename': 'log/server.log',
            'maxBytes': '5000000',
            'level': 'DEBUG',
            'backupCount': '3',
        },
    },
}

