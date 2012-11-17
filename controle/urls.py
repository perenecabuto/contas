# -*- encoding : utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',

    url(r'^$', 'controle.views.mes_corrente'),
    url(r'^index$', 'controle.views.index'),
    url(r'^novo$', 'controle.views.novo'),
    url(r'^salvar$', 'controle.views.salvar'),
    url(r'^novo/(?P<mes>\d)/(?P<ano>\d)$', 'controle.views.novo'),

    url(r'^(?P<mes>\d{1,2})/(?P<ano>\d{4})/?$', 'controle.views.editar'),
    url(r'^(?P<mes>\d{1,2})/(?P<ano>\d{4})/salvar_conta/(?P<nome>[\w -]+)?/?$', 'controle.views.salvar_conta'),
    url(r'^(?P<mes>\d{1,2})/(?P<ano>\d{4})/registrar_pagamento/(?P<nome>[\w  -]+)?/?$', 'controle.views.registrar_pagamento'),
    url(r'^(?P<mes>\d{1,2})/(?P<ano>\d{4})/upload_conta/(?P<nome>[\w -]+)?/?$', 'controle.views.upload_conta'),
)
