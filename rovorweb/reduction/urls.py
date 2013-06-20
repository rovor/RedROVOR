from django.conf.urls import patterns, url

from reduction import views

urlpatterns = patterns('',
    url(r'^$',views.index),
    url(r'^zero-dark$',views.zeroDark),
    url(r'^flatSelectForm$',views.flatSelectForm),
    url(r'^photometry-start',views.photometry_start),
    url(r'^phot-page$',views.phot_page),
    url(r'^phot$',views.phot_service),
    url(r'^renameAll', views.renameAll),
    url(r'^makeZero',views.makeZero),
    url(r'^makeDark',views.makeDark),
    url(r'^makeFlats',views.makeFlats),
    url(r'^subZeroDark',views.subZeroDark),
    url(r'^firstPass',views.firstPass),
    url(r'^applyFlats',views.applyFlats),
    url(r'^applyWCS',views.applyWCS),
    url(r'^secondpass',views.secondPass),
    )
