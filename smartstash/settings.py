# Django settings for smartstash project.

import os
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMAIL_SUBJECT_PREFIX = '[Serendipomatic] '

# heroku config

HEROKU = bool(os.environ.get('HEROKU', ''))


# heroku-specific configuration
if HEROKU:

    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {'default':  dj_database_url.config()}

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Static asset configuration
    # STATIC_ROOT = 'static'
    # STATIC_URL = '/static/'

    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )

    # get 'local' settings via heroku env
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

    API_KEYS = {
        'DPLA': os.environ.get('DPLA_API_KEY'),
        'Europeana': os.environ.get('EUROPEANA_API_KEY'),
        'Flickr': os.environ.get('FLICKR_API_KEY'),
        'ZOTERO_CONSUMER_KEY': os.environ.get("ZOTERO_CONSUMER_KEY"),
        'ZOTERO_CONSUMER_SECRET': os.environ.get("ZOTERO_CONSUMER_SECRET"),
        'Trove': os.environ.get("TROVE_API_KEY"),
    }


DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# NOTE: media root & url are disabled for now - not expecting to serve out
# user-uploaded content

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'sitemedia'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'smartstash.version',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smartstash.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'smartstash.wsgi.application'

#Text file to draw the starting text from
#DEFAULT_TEXT_PATHNAME = os.path.join(BASE_DIR, "default.txt")

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'social_auth',
    'smartstash.core',
    'smartstash.auth',
    'smartstash.images',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'smartstash.auth.zotero.ZoteroBackend',
)

LOGIN_URL          = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/logged-in/'
LOGIN_ERROR_URL    = '/auth/login-error/'

# directory where files with extra stopwords by language can be added
EXTRA_STOPWORDS = os.path.join(BASE_DIR, '..', 'stopwords')

# when requesting zotero oauth key, also request access to notes and groups
ZOTERO_PERMISSIONS = ['library_access', 'notes_access', 'group_read']

if not HEROKU:
    try:
        from localsettings import *
    except ImportError:
        import sys
        print >> sys.stderr, 'No local settings. Trying to start, but if ' + \
            'stuff blows up, try copying localsettings.py.dist to ' + \
            'localsettings.py and setting appropriately for your environment.'


# settings specific to travis-ci
TRAVIS = bool(os.environ.get('TRAVIS', ''))
if TRAVIS:
    SECRET_KEY = 'not really very secret is it'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'stash.db'),
        }
    }

