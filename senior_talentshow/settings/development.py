from base import *


############################################################
##### DATABASE #############################################
############################################################

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'senior_talentshow',
        'USER': 'senior_talentshow',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


############################################################
##### OTHER ################################################
############################################################

DEBUG = True
TEMPLATE_DEBUG = True

SETTINGS_MODULE = 'senior_talentshow.settings.development'

CELERY_RESULT_DBURI = "postgresql://senior_talentshow:password@localhost/senior_talentshow"
BROKER_URL = 'django://'

# put these two lines at the very bottom of the settings file
import djcelery
djcelery.setup_loader()
