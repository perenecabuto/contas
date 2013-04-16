# -*- coding: utf-8 -*-

from nodefs.lib.shortcuts import profile, absnode
from controle.models import Conta, Controle, User
#from possessions.models import Possession

from nodefs.lib.selectors import StaticSelector
from django_nodefs.selectors import ModelSelector, ModelFileSelector, QuerySetSelector
from datetime import date

today = date.today()

schema = {
    'default': profile([

        #absnode(StaticSelector('users'), [
            #absnode(ModelSelector('%(username)s', User), [

                absnode(
                    QuerySetSelector(
                        'deste_mes',
                        Controle.objects.extra(where=["strftime('%%Y%%m', data) = strftime('%%Y%%m', date('now'))"])
                    ), [
                        absnode(
                            ModelSelector('%(nome)s (%(status)s)', Conta), [
                                absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                            ]
                        ),
                    ]
                ),

                absnode(
                    QuerySetSelector(
                        'mes_passado',
                        Controle.objects.extra(where=[
                            "strftime('%%Y%%m', data) = strftime('%%Y%%m', date('now', 'start of month', '-1 month'))"
                        ])
                    ), [
                        absnode(
                            ModelSelector('%(nome)s (%(status)s)', Conta), [
                                absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                            ]
                        ),
                    ]
                ),

                absnode(StaticSelector('este_ano'), [
                    absnode(
                        QuerySetSelector(
                            '%(data.month)s-%(month_name)s',
                            Controle.objects.extra(where=["strftime('%%Y', data) = strftime('%%Y', date('now'))"])
                        ), [
                            absnode(
                                ModelSelector('%(nome)s (%(status)s)', Conta), [
                                    absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                                ]
                            ),
                        ]
                    ),
                ]),

                #absnode(StaticSelector('outros_anos'), [
                    #absnode(QuerySetSelector('%(data.year)s', Controle.objects.extra(where=["strftime('%%Y', data) < strftime('%%Y', date('now'))"]).order_by('-data')), [
                        #absnode(ModelSelector('%(data.month)s-%(month_name)s', Controle), [
                            #absnode(
                                #ModelSelector('%(nome)s (%(status)s)', Conta), [
                                    #absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                                #]
                            #),
                        #]),
                    #]),
                #]),

                absnode(StaticSelector('separadas por tipo'), [
                    absnode(
                        QuerySetSelector('%(nome)s', Conta.objects.order_by('nome')), [
                            absnode(QuerySetSelector('%(data.year)s %(data.month)s-%(month_name)s', Controle.objects.order_by('-data')), [

                                absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo')),

                            ]),
                        ]
                    ),
                ])


            #]),
        #]),

    ]),
}

