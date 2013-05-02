from django.conf.urls import patterns, url

from dirmanage import views

urlpatterns = patterns('',
        url(r'^$',views.index),
        url(r'json/(?P<filesystem_name>.*?)/(?P<path>.*)$',views.getJson),
        url(r'testChoose',views.testChoose),
        url(r'chooseFrame/(?P<filesystem_name>.*?)/(?P<path>.*)$',views.chooseFrame),
        url(r'(?P<filesystem_name>.*?)/(?P<path>.*)$',views.directory),
        )
