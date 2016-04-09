from base import *

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'senior_talentshow',
        'USER': 'senior_talentshow',
        'PASSWORD': 'senior_talentshow',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DEBUG = True
TEMPLATE_DEBUG = True
TIME_ZONE = 'America/New_York'

STATIC_ROOT = '/webapps/senior_talentshow/static/'
STATIC_URL = '/static/'

SETTINGS_MODULE = 'senior_talentshow.settings.production'

BROKER_URL = "amqp://senior_talentshow:senior_talentshow@127.0.0.1:5672/senior_talentshow"
CELERY_RESULT_DBURI = "postgresql://senior_talentshow:senior_talentshow@localhost/senior_talentshow"

# put these two lines at the very bottom of the settings file
import djcelery
djcelery.setup_loader()
