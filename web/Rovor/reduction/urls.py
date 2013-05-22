from django.conf.urls import patterns, url

from reduction import views

urlpatterns = patterns('',
    url(r'^$',views.index),
    url(r'^zero-dark$',views.zeroDark),
    url(r'^flatSelectForm$',views.flatSelectForm),
    url(r'^astrometry$',views.astrometry),
    url(r'^renameAll', views.renameAll),
    url(r'^makeZero',views.makeZero),
    url(r'^makeDark',views.makeDark),
    url(r'^makeFlats',views.makeFlats),
    url(r'^subZeroDark',views.subZeroDark),
    url(r'^firstPass',views.firstPass),
    url(r'^applyFlats',views.applyFlats),
    url(r'^applyWCS',views.appplyWCS),
    )
