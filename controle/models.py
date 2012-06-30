# -*- encoding : utf-8 -*-
from django.db import models
from datetime import date, timedelta


class Controle(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()

    def __unicode__(self):
        return "%02d-%04d" % (self.mes, self.ano)

    @classmethod
    def get_current(self):
        return self.objects.get_or_create(ano=date.today().year, mes=date.today().month)[0]

    class Meta:
        unique_together = ('ano', 'mes')
        ordering = ['-ano', '-mes']


class Conta(models.Model):
    nome = models.CharField(max_length=128)
    dia_vencimento = models.PositiveIntegerField(choices=((i, i) for i in range(1, 32)))
    arquivo = models.FileField(upload_to='media/contas/%Y-%m-%d', blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    controle = models.ForeignKey(Controle, blank=True)

    class Meta:
        unique_together = ('nome', 'controle')

    def __unicode__(self):
        return self.nome

    def status(self):
        status = 'pagamento pendente, vence em %s' % self.data_vencimento.strftime('%d/%m/%Y')

        if self.pago():
            status = 'pago'
        elif self.venceu():
            status = 'venceu'

        return status

    @property
    def data_vencimento(self):
        delta = timedelta(days=self.dia_vencimento - 1)
        data_vencimento = date(year=self.controle.ano, month=self.controle.mes, day=1) + delta
        return data_vencimento

    def pago(self):
        return bool(self.data_pagamento)

    def venceu(self):
        return bool(date.today() > self.data_vencimento)
