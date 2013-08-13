try:
    from settings_shared import *
except ImportError:
    pass

from redrovor import credentials


DEBUG = False
TEMPLATE_DEBUG = DEBUG

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': credentials.users['database-name'],                      # Or path to database file if using sqlite3.
        'USER': credentials.users['database-user'],                      # Not used with sqlite3.
        'PASSWORD': credentials.passwords['rovor-database'],                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#secret key for the production server, DO NOT DISTRIBUTE
SECRET_KEY = credentials.passwords['secret_key']

#set allowed hosts, once we know what our ip address is we should change this to match
ALLOWED_HOSTS = ['*']

ADMINS += (
    ('thayne','astrothayne@gmail.com'),
    ('rovor', 'rovor.byu@gmail.com'),
    ('j moody', 'jmoody@physics.byu.edu'),
)

MANAGERS = ADMINS

#set up email for production

#gmail settings for rovor.byu@gmail.com
#doesn't seem to work, so we will set up a file instead
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'rovor.byu@gmail.com'
#EMAIL_HOST_PASSWORD = 'outhouse'
#EMAIL_PORT = "465"
#EMAIL_USE_TLS = True


#set up logging so that we can log to a file
LOG_DIR = '/var/log/django'

LOGGING_FILE = os.path.join(LOG_DIR,'rovorweb.log')
REQUEST_LOG_FILE = os.path.join(LOG_DIR,'requests.log')

#add logfile handler
LOGGING['handlers']['logfile'] = {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'formatter':'standard',
    'filename':LOGGING_FILE,
    'maxBytes': 2048,
    'backupCount':5,
}

LOGGING['handlers']['requestlog'] = {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'formatter':'standard',
    'filename':REQUEST_LOG_FILE,
    'maxBytes': 2048,
    'backupCount':5,
}

# set loggers to use logfiles
LOGGING['loggers']['Rovor']['handlers'].append('logfile')
LOGGING['loggers']['django.request']['handlers'].append('requestlog')


#file to store emails, since we can't get smtp to work
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/var/log/django/rovorweb-messages'



