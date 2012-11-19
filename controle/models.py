# -*- encoding : utf-8 -*-

from django.db import models
from datetime import date, timedelta

import logging
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())


class Controle(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()

    def __unicode__(self):
        return "%02d-%04d" % (self.mes, self.ano)

    def get_date(self):
        return date(self.ano, self.mes, 1)

    @property
    def month_name(self):
        import locale
        locale.setlocale(locale.LC_ALL, 'pt_BR')

        return self.get_date().strftime('%b')

    @classmethod
    def get_current(self):
        return self.objects.get_or_create(ano=date.today().year, mes=date.today().month)[0]

    class Meta:
        unique_together = ('ano', 'mes')
        ordering = ['-ano', '-mes']


class Conta(models.Model):
    nome = models.CharField(max_length=128)
    dia_vencimento = models.PositiveIntegerField(choices=((i, i) for i in range(1, 32)))
    valor = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    arquivo = models.FileField(upload_to='contas/%Y-%m-%d', blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True)
    controle = models.ForeignKey(Controle, blank=True)

    class Meta:
        unique_together = ('nome', 'controle')

    def __unicode__(self):
        return self.nome

    def status(self):
        status = 'pagamento pendente, vence em %s' % self.data_vencimento.strftime('%d/%m/%Y')

        if self.pago:
            status = 'pago'
        elif self.venceu:
            status = 'venceu'

        return status

    @property
    def data_vencimento(self):
        delta = timedelta(days=self.dia_vencimento - 1)
        data_vencimento = date(year=self.controle.ano, month=self.controle.mes, day=1) + delta
        return data_vencimento

    @property
    def pago(self):
        return bool(self.data_pagamento)

    @property
    def venceu(self):
        return bool(date.today() > self.data_vencimento)

    def registrar_pagamento(self):
        self.data_pagamento = date.today()
        self.save()
