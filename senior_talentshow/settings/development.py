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
