# -*- coding: utf-8 -*-

from possessions.middleware import get_current_user
from controle.models import Conta, Controle
from django.core.urlresolvers import reverse
from django_nodefs.selectors import ModelFileSelector


def get_current_user_path():
    return "/users/%s" % get_current_user().username


def get_node_url(node, nodeselector):
    url = None

    if issubclass(nodeselector.model_class, Controle):
        obj = nodeselector.get_object(node)
        url = reverse('controle.views.editar', kwargs={'mes': obj.mes, 'ano': obj.ano})

    elif issubclass(nodeselector.model_class, Conta) and isinstance(nodeselector, ModelFileSelector):
        obj = nodeselector.get_object(node)
        url = obj.arquivo.url

    return url

