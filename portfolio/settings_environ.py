import os

# Django Application Secret Key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Domain Name
DOMAIN_NAME = "joshuadanielcodes.com"
DOMAIN_URL = "http://joshuadanielcodes.com"

ADMINS = os.environ.get('ADMINS')

# Email Server Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
SERVER_EMAIL = EMAIL_HOST_USER
