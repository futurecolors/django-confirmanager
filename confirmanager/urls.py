# coding: utf-8
from django.conf.urls import patterns, url
from .views import ConfirmEmail


urlpatterns = patterns('',
    url(r'^confirm/(?P<confirmation_key>([^/]+))/$', ConfirmEmail.as_view(), name='confirmation-view'),
)