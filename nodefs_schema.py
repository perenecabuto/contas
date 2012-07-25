# -*- coding: utf-8 -*-

from nodefs.lib.shortcuts import profile, absnode
from controle.models import Conta, Controle

from nodefs.lib.selectors import StaticSelector
from django_nodefs.selectors import ModelSelector, ModelFileSelector, QuerySetSelector
from datetime import datetime


schema = {
    'default': profile([

        absnode(StaticSelector('contas_deste_mes'), [
            absnode(QuerySetSelector(projection='%(nome)s (%(status)s)', query_set=Conta.objects.filter(controle__mes=datetime.now().month)), [
                absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
            ]),
        ]),

    ]),
}

#absnode(StaticSelector('pre_filtered_things'), [
    #absnode(StaticSelector('first_things'), [
        #absnode(
            #QuerySetSelector('%(label)s', query_set=Thing.objects.filter(label__icontains='First')), [
                #absnode(ModelSelector('%(serial_number)s', model_class=BoxOfThings), [
                    ## TODO pegar as OUTRAS COISAS da CAIXA desta coisa
                    #absnode(QuerySetSelector('%(label)s', query_set=Thing.objects.filter(label__icontains='%%')), [
                    #]),
                #]),
            #]
        #),
    #])
#]),
