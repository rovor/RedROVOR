from django.conf.urls import patterns, url

from reduction import views

urlpatterns = patterns('',
    url(r'^$',views.index),
    )
