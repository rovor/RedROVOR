try:
    from settings_shared import *
except ImportError:
    pass


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
# note KEY is used for development purposes only
# do not use it on your production server
SECRET_KEY = 'njsae^$*=t*)#otl3^l*u(1a-6lrv!tsqs+5+arb#ppmue7zcb'


#for development the default is a simple
#sqlite database
#change this if desired
# and you should probably use a different database
# for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'rovordb.sqlite'
    }
}
