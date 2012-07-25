# -*- coding: utf-8 -*-

from nodefs.lib.shortcuts import profile, absnode
from controle.models import Conta, Controle

from nodefs.lib.selectors import StaticSelector
from django_nodefs.selectors import ModelSelector, ModelFileSelector, QuerySetSelector
from datetime import date

today = date.today()

schema = {
    'default': profile([

        absnode(StaticSelector('contas_deste_mes'), [
            absnode(
                QuerySetSelector('%(nome)s (%(status)s)', Conta.objects.filter(controle__mes=today.month, controle__ano=today.year)), [
                    absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                ]
            ),
        ]),


        absnode(StaticSelector('do_mes_passado'), [
            absnode(
                QuerySetSelector('%(nome)s (%(status)s)', Conta.objects.filter(controle__mes=today.month - 1, controle__ano=today.year)), [
                    absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                ]
            ),
        ]),

        absnode(StaticSelector('este_ano'), [
            absnode(QuerySetSelector('%(mes)s', Controle.objects.filter(mes__lt=today.month - 2, ano=today.year)), [
                absnode(
                    ModelSelector('%(nome)s (%(status)s)', Conta), [
                        absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                    ]
                ),
            ]),
        ]),

        absnode(StaticSelector('outros_anos'), [
            absnode(QuerySetSelector('%(ano)s', Controle.objects.filter(ano__lt=today.year)), [
                absnode(ModelSelector('%(mes)s', Controle), [
                    absnode(
                        ModelSelector('%(nome)s (%(status)s)', Conta), [
                            absnode(ModelFileSelector(projection='%(arquivo)s', model_class=Conta, file_field_name='arquivo'), writable=True),
                        ]
                    ),
                ]),
            ]),
        ])

    ]),
}

