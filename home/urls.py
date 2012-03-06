# -*- encoding : utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'home.views.index'),
)
