from django.conf.urls import patterns, url

from obs_database import views

urlpatterns = patterns('',
    url(r'^$', views.upload_form),
    )
