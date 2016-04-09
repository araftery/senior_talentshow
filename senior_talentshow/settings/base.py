from datetime import timedelta
import os

from path import path

############################################################
##### SETUP ################################################
############################################################

# i.e., where root urlconf is
PROJECT_ROOT = path(__file__).abspath().dirname().dirname()
os.sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))


############################################################
##### DATABASE #############################################
############################################################

ALLOWED_HOSTS = ['*']

############################################################
##### APPS #################################################
############################################################

# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'gunicorn',
    'widget_tweaks',
    'dbbackup',
    'compressor',
    'crispy_forms',
    'localflavor',
    'djrill',
    'djcelery',
    'kombu.transport.django',
)

MY_APPS = (
    'core',
    'talentshow',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + MY_APPS

############################################################
##### MIDDLEWARE ###########################################
############################################################

DEFAULT_MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

THIRD_PARTY_MIDDLEWARE = (
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

############################################################
##### INTERNATIONALIZATION #################################
############################################################

LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
INTERNAL_IPS = ['*']

############################################################
##### TEMPLATES ############################################
############################################################

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates_common').replace('\\','/'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TCP

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'core.context_processors.debug',
    'core.context_processors.site_url',
] + DEFAULT_TCP


############################################################
##### AUTHENTICATION #######################################
############################################################

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''

############################################################
##### EMAIL ################################################
############################################################

ADMINS = (
    ('Andrew Raftery', 'andrewraftery@gmail.com'),
)

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ.get('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = os.environ.get('MAILGUN_SERVER_NAME')

HARVARD_TALENT_EMAIL_ADDRESS = 'catarinamartinez@college.harvard.edu'
HARVARD_TALENT_EMAIL = 'Harvard Senior Talent Show <{}>'.format(HARVARD_TALENT_EMAIL_ADDRESS)
DEFAULT_FROM_EMAIL = HARVARD_TALENT_EMAIL_ADDRESS

############################################################
##### STATIC FILES #########################################
############################################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_common').replace('\\','/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_CSS_FILTERS = (
     'compressor.filters.cssmin.CSSMinFilter',
)


############################################################
##### OTHER ################################################
############################################################

ROOT_URLCONF = 'senior_talentshow.urls'
WSGI_APPLICATION = 'senior_talentshow.wsgi.application'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASES = {}
TIME_ZONE = 'America/New_York'
USE_TZ = True
SITE_ID = 1

############################################################
##### CRISPY FORMS  ########################################
############################################################

CRISPY_TEMPLATE_PACK = 'bootstrap3'

############################################################
##### PROJECT-SPECIFIC #####################################
############################################################

TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE

