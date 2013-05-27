ROVOR-reduction
===============

Pyraf, Python, etc. scripts for the Data reduction pipline for ROVOR (Remote Observatory for Variable Object Research)


This has been tested on RHEL with Python 2.6.6, Pyfits 2.3.1, numpy 1.4.1 and Django 1.4.5, getting it to run on another configuration
may require some tweaking. Django is only required for the web part, pyfits is required for the reduction.

Installation
------------

The redrovor package uses a standard distutils script for installation
so to install into the normal site-packages directory simply run

./setup.py install

for other options for the distribution see the distutils documentation. You can
also use ``make install_redrovor'' which will run the setup script for you.

To install the rovorweb django package, which is the web interface to redrovor
you can run make install_rovorweb, this copies the folder to the webprefix folder which is an option in the Makefile, and if supplied changes the settings for django to production settings.

To install both packages simply run ``make install''.

Deployment
----------

Although the django website comes with some default settings for development purposes, and can be run with ``./manage.py runserver'' (after syncing the database and setting up the Raw and Processed paths in the database at minimum), deployment into a production environment requires more work for the user.

To simplify setting up the settings for production we have made settings.py a symbolic link which points to settings.development.py by default. When running make install, make will look at the settings_module variable, which defaults to settings.production.py, if the file exists (this would be in the rovorweb/rovorweb directory) it will move the symbolic link of settings.py to that file on installation. This allows you to put all of your production settings into settings.production.py and have them automatically take effect.

At the very least your production settings should include the following:
* Set DEBUG = False
* Set CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE to True (so that SSL is used when secret cookies are transmitted)
* Set DATABASES to use your production database
* Set SECRET_KEY to a random secret key which you DO NOT SHARE! Please DO NOT USE SAME SECRET_KEY AS IN settings.development.py
* Set ALLOWED_HOSTS to the hosts that you will accept requests to

You should configure your server to use SSL, and to run a django site, probably using WSGI. Please see documentatin for your server
and Django deployment for more information.

For Apache a sample configuration (assuming SSL and WSGI are loaded and configured) is:

WSGISocketPrefix run/wsgi

WSGIDaemonProcess localhost python-path=/var/www/rovorweb user=rovor
WSGIProcessGroup localhost

WSGIScriptAlias / /var/www/rovorweb/rovorweb/wsgi.py

Alias /static/ /var/www/rovorweb/static/

<Directory /var/www/rovorweb/static>
Order deny,allow
Allow from all
</Directory>

<Directory /var/www/rovorweb/rovorweb>
#require ssl for the rovorweb site
SSLRequireSSL  
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>

Note that WSGISocketPrefix must be in the global context, and that we have set
up an alias for /static to /var/www/rovorweb/static, which is necessary in order to access static files such as css, javascript, and images. 

This assumes that your web directory is /var/www
