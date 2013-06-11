from django.conf.urls import patterns, url

from targets import views
from toolset import html_or_json
from django.views.generic.list import ListView
from models import Target

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'addObject',views.addObject),
    url(r'^targetList',html_or_json.as_view(html_view=views.targetList_html,json_view=views.targetList_json)),
    url(r'^uploadCoordfile',views.uploadCoordFile),
    url(r'^editTargets',views.edit_targets),
    url(r'^editCoords',views.edit_fieldObjects),
    url(r'^(?P<targetID>\d+?)/coordlist',views.coordlist_json),
    url(r'^fieldobject/(?P<objID>\d+?)/delete$', views.fieldObjectDelete),
    url(r'^coordlist/$',views.coordlist_json),
)
