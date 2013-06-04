from django.conf.urls import patterns, url

from targets import views
from toolset import html_or_json

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'addObject',views.addObject),
    url(r'^targetList',html_or_json.as_view(html_view=views.targetList_html,json_view=views.targetList_json)),
    url(r'^uploadCoordfile',views.uploadCoordFile),
    url(r'^editTargets',views.edit_targets),
)
