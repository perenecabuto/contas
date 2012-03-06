# -*- encoding : utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<id>\d)/edit$', 'controle.views.edit'),
    url(r'^new/$', 'controle.views.new'),
    url(r'^$', 'controle.views.index'),
    url(r'^(?P<id>\d)/save/$', 'controle.views.save'),
    url(r'^save/$', 'controle.views.save'),
)

