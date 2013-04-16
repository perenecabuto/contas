# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Conta, Controle


@receiver(post_save, sender=Controle, dispatch_uid="copy_contas_from_previous")
def copy_contas_from_previous(sender, **kwargs):
    if not kwargs.get('created'):
        return

    current = kwargs.get('instance')
    qs = Controle.objects.filter(data__lt=current.data)

    if not qs.exists():
        return

    previous = qs.order_by('-data')[0]

    for conta in previous.conta_set.all():
        new_conta = Conta(
            nome=conta.nome,
            valor=conta.valor,
            dia_vencimento=conta.dia_vencimento,
        )
        current.conta_set.add(new_conta)

    current.save()
