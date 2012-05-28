# -*- encoding : utf-8 -*-
from django.db import models
from datetime import datetime
from django.db.models import signals
from django.dispatch import receiver


# Create your models here.
class Controle(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()

    def __unicode__(self):
        return "%02d-%04d" % (self.mes, self.ano)

    @classmethod
    def get_current(self):
        return self.objects.get_or_create(ano=datetime.now().year, mes=datetime.now().month)[0]


class Conta(models.Model):
    nome = models.CharField(max_length=128)
    arquivo = models.FileField(upload_to='media/contas/%Y-%m-%d', blank=True, null=True)
    data_pagamento = models.DateField()
    pago = models.BooleanField()
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    controle = models.ForeignKey(Controle, blank=True)

    def __unicode__(self):
        return self.nome

    def status(self):
        pass


@receiver(signals.post_init, sender=Conta)
def configura_controle(sender, **kwargs):
    conta = kwargs['instance']

    if not conta.id:
        conta.controle = Controle.get_current()
