ROVOR-reduction
===============

Pyraf, Python, etc. scripts for the Data reduction pipline for ROVOR (Remote Observatory for Variable Object Research)


This has been tested on RHEL with Python 2.6.6, Pyfits 2.3.1, numpy 1.4.1 and Django 1.4.5, getting it to run on another configuration
may require some tweaking. Django is only required for the web part, pyfits is required for the reduction.

Dependencies
------------

* Python  (>=2.6 and < 3.0)
* Pyfits 
* numpy  
* Django 
* pywcs 
* IRAF
* PyRaf
* astrometry.net


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

Before installing, however, you need to update the ``credentials.py'' file. The distribution contains a sample file called ``credentials.sample.py,'' which contains the format
of the credentials file, but does not contain actual usernames or passwords. The Usernames and passwords should be entered, and then the file should be renamed as credentials.py. Once this is done the system be able to properly log in to the database and remote Observation Database

Deployment
----------

#### Django Settings ####

Although the django website comes with some default settings for development purposes, and can be run with ``./manage.py runserver'' (after syncing the database and setting up the Raw and Processed paths in the database at minimum), deployment into a production environment requires more work for the user.

To simplify setting up the settings for production we have made settings.py a symbolic link which points to settings.development.py by default. When running make install, make will look at the settings_module variable, which defaults to settings.production.py, if the file exists (this would be in the rovorweb/rovorweb directory) it will move the symbolic link of settings.py to that file on installation. This allows you to put all of your production settings into settings.production.py and have them automatically take effect.

At the very least your production settings should include the following:
* Set DEBUG = False
* Set CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE to True (so that SSL is used when secret cookies are transmitted)
* Set DATABASES to use your production database
* Set SECRET_KEY to a random secret key which you DO NOT SHARE! Please DO NOT USE SAME SECRET_KEY AS IN settings.development.py
* Set ALLOWED_HOSTS to the hosts that you will accept requests to

You may also want to set up your email system in the settings

This repository included a settings.production.py that we used for our system. It may require tweaking on other systems, and requires the credentials module to be set up properly.

#### Apache Settings ####

You should configure your server to use SSL, and to run a django site, probably using WSGI. Please see documentatin for your server
and Django deployment for more information.

For Apache a sample configuration (assuming SSL and WSGI are loaded and configured) is:
```apache
#configuration for the rovorweb site

ServerName localhost

WSGISocketPrefix run/wsgi

WSGIDaemonProcess localhost python-path=/var/www/rovorweb 
WSGIProcessGroup localhost

WSGIScriptAlias / /var/www/rovorweb/rovorweb/wsgi.py

Alias /static/ /var/www/rovorweb/static/
Alias /media/ /var/www/rovorweb/media/

<Directory /var/www/rovorweb/static>
Order deny,allow
Allow from all
</Directory>

<Directory /var/www/rovorweb/media>
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
```

Note that WSGISocketPrefix must be in the global context, and that we have set
up an alias for /static to /var/www/rovorweb/static, which is necessary in order to access static files such as css, javascript, and images. 

This assumes that your web directory is /var/www.

You can either put this code directly in httpd.conf (usually at /etc/httpd/conf/httpd.conf) or in a file that is included in the configuration
(such as a custom file in /etc/httpd/conf.d/ or /etc/httpd/conf/extra depending on the distro).

For more information see https://github.com/rovor/RedROVOR/wiki/Apache-Setup

Observatory Setup
-----------------

When setting up RedROVOR for a different observatory, you need to create an Observatory object for your observatory which contains paramaters
specific to your observatory, and make sure that that Observatory object is used instead of the default ROVOR object. Eventually we might add in
a way to switch between observatories at runtime, or at least make the configuration more simple, but for now it isn't a very high priority.

Also, in order for photometry to work with setting the HJD, you need to set up your observatory in IRAF's observatory database, and it must have the same
name as the name attribute of the Observatory object. If you do not want to use HJD, or already have the HJD in your header, then comment out the line that 
calls setjd in `daophot.py`.

The entry for ROVOR is:
```
observatory = "rovor"
    name = "Remote Observatory for Variable Object Research"
    longitude = 112:43:01.00
    latitude = 39:27:17.10
    altitude = 4579
    timezone = 7
```

For more information see https://github.com/rovor/RedROVOR/wiki/Adding-Observatory.

Special Issues
-------------

##### Some issues we ran into on our system #####

* We had a lot of issues with working with SELinux. You either need to make a lot of changes in your SELinux configuration
and security contexts, or disable SELinux. See https://github.com/rovor/RedROVOR/wiki/Disabling-SELinux
* We also needed to update iptables to allow traffic on ports 443 and 80 (https and http respectevely)
* We needed to add the apache user to the iraf group so he has write access to the iraf home folder, where the login.cl, uparm and pyraf folders are



