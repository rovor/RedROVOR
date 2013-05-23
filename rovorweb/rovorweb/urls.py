from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from root import views

urlpatterns = patterns('',
    url(r'$^', views.index, name='top_index'),
    url(r'^files/', include('dirmanage.urls')),
    url(r'^reduce/',include('reduction.urls')),
    url(r'^odb/',include('obs_database.urls')), #observation database
    url(r'^accounts/',include('accounts.urls')),
    # Examples:
    # url(r'^$', 'Rovor.views.home', name='home'),
    # url(r'^Rovor/', include('Rovor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
