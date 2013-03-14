# coding: utf-8
from django.conf.urls import patterns, include, url
from django.http import HttpResponse


urlpatterns = patterns('',
    url(r'', include('confirmanager.urls')),
    url(r'LOGIN_URL/', lambda _: HttpResponse()),
    url(r'REDIRECT_URL/', lambda _: HttpResponse()),
)