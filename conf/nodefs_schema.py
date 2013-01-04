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
                        Controle.objects.extra(where=["mes = strftime('%%m', date('now')) and ano = strftime('%%Y', date('now'))"])
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
                            "mes = strftime('%%m', date('now','start of month','-1 month')) and ano = strftime('%%Y', date('now','start of month','-1 month'))"
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
                            '%(mes)s-%(month_name)s',
                            Controle.objects.extra(where=["mes < strftime('%%m', date('now')) - 1 and ano = strftime('%%Y', date('now'))"])
                        ), [
                            absnode(
                                ModelSelector('%(nome)s (%(status)s)', Conta), [
                                    absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                                ]
                            ),
                        ]
                    ),
                ]),

                absnode(StaticSelector('outros_anos'), [
                    absnode(QuerySetSelector('%(ano)s', Controle.objects.extra(where=["ano < strftime('%%Y', date('now'))"]).order_by('-ano')), [
                        absnode(ModelSelector('%(mes)s-%(month_name)s', Controle), [
                            absnode(
                                ModelSelector('%(nome)s (%(status)s)', Conta), [
                                    absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                                ]
                            ),
                        ]),
                    ]),
                ]),

                absnode(StaticSelector('separadas por tipo'), [
                    absnode(
                        QuerySetSelector('%(nome)s', Conta.objects.order_by('nome')), [
                            absnode(QuerySetSelector('%(ano)s %(mes)s-%(month_name)s', Controle.objects.order_by('-ano')), [

                                absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo')),

                            ]),
                        ]
                    ),
                ])


            #]),
        #]),

    ]),
}

