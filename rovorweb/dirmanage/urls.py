from django.conf.urls import patterns, url

from dirmanage import views

urlpatterns = patterns('',
        url(r'^$',views.index),
        url(r'^twoFrameBrowser',views.twoFrameBrowser),
        url(r'^json/$', views.jsonRoot), #get json list of root filesystems, used this way to be consistant with other paths
        url(r'json/(?P<filesystem_name>.*?)/(?P<path>.*)$',views.getJson),
        url(r'json/(?P<filesystem_name>.*?)$',views.getJson,{'path':''}),
        url(r'testChoose',views.testChoose),
        url(r'chooseFrame/(?P<filesystem_name>.*?)/(?P<path>.*)$',views.chooseFrame),
        url(r'(?P<filesystem_name>.*?)/(?P<path>.*)$',views.directory),
        )
