from django.conf.urls import patterns, url

from targets import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'addObject',views.addObject),
    url(r'^targetList',views.targetList),
    url(r'^uploadCoordfile',views.uploadCoordFile),
    url(r'^editTargets',views.edit_targets),
)
