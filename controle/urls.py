# -*- encoding : utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'controle.views',

    url(r'^$', 'mes_corrente'),
    url(r'^novo$', 'novo'),
    url(r'^salvar$', 'salvar'),

    url(r'^(?P<ano>\d{4})/(?P<mes>\d{1,2})/?$', 'editar'),
    url(r'^(?P<ano>\d{4})/(?P<mes>\d{1,2})/salvar_conta/(?P<nome>[\w -]+)?/?$', 'salvar_conta'),
    url(r'^(?P<ano>\d{4})/(?P<mes>\d{1,2})/registrar_pagamento/(?P<nome>[\w  -]+)?/?$', 'registrar_pagamento'),
    url(r'^(?P<ano>\d{4})/(?P<mes>\d{1,2})/upload_conta/(?P<nome>[\w -]+)?/?$', 'upload_conta'),
)
