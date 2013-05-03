from django.conf.urls import patterns, url

from reduction import views

urlpatterns = patterns('',
    url(r'^$',views.index),
    url(r'^zero-dark$',views.zeroDark),
    url(r'^flat-apply$',views.flatApply),
    url(r'^astrometry$',views.astrometry),
    )
