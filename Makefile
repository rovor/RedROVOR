
web_prefix=/var/www

none:


install: install_redrovor install_rovorweb


install_redrovor: 
	./setup.py install

install_rovorweb:
	cp -r rovorweb $(web_prefix)
	$(web_prefix)/rovorweb/manage.py collectstatic #collect static files for use in the website


.PHONY: install install_redrovor install_rovorweb
	
