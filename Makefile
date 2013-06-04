#location to install the rovorweb web application to
web_prefix=/var/www

#the module to use for the settings, this assumes that there is a module called settings.production.py
# in the rovorweb/rovorweb folder (i.e. where the setting.py file should be, which in our case is simply a symlink)
settings_module=settings.production.py     

settings_module_path=$(web_prefix)/rovorweb/rovorweb/$(settings_module)
settings_path=$(web_prefix)/rovorweb/rovorweb/settings.py

#any aptions to pass to python when compiling
#for example to optimize use -O or -OO
pcompile_options=



none:


install: install_redrovor install_rovorweb


install_redrovor: 
	./setup.py install

install_rovorweb:
	cp -r rovorweb $(web_prefix)
	#detele any static and media files we might have
	rm -rf $(web_prefix)/rovorweb/static/*
	rm -rf $(web_prefix)/rovorweb/media/*
	#set read and write permission for everyone in the media folder
	chmod 777 $(web_prefix)/rovorweb/media
	#collect static files for use in the website
	$(web_prefix)/rovorweb/manage.py collectstatic -l --noinput
	$(web_prefix)/rovorweb/manage.py syncdb
ifneq ($(wildcard $(settings_module_path)),)
	#make link for settings
	ln -sf  $(settings_module_path)   $(settings_path)
	#delete compiled settings if they exist
	rm -f $(web_prefix)/rovorweb/rovorweb/settings.pyc
endif
	#compile pyc files for rovorweb
	python $(pcompile_options) -m compileall $(web_prefix)/rovorweb >/dev/null




# we do not currently have an uninstall, because I don't know how to do that with the distutils version I have available
# and it isn't that hard for the user to simply delete the folders

.PHONY: install install_redrovor install_rovorweb
	
