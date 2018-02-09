# deployment/production settings

import os
from settings import *
from settings_environ import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'afternoon-hollows-18869.herokuapp.com',
    DOMAIN_NAME
]

# Media File Storage on Amazon S3
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'portfolio.storage_backends.MediaStorage'
MEDIA_URL = '/assets/'
MEDIA_ROOT = 'https://s3.us-east-2.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))
