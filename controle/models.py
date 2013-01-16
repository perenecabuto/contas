# -*- encoding : utf-8 -*-

from datetime import datetime

from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import User

from .managers import ControleManager


class Controle(models.Model):
    data = models.DateField(unique_for_month=True)
    owner = models.ForeignKey(User)
    objects = ControleManager()

    def __unicode__(self):
        if not self.data:
            return ""

        return "%02d-%04d" % (self.data.month, self.data.year)

    @property
    def mes(self):
        if self.data:
            return self.data.month

    @property
    def ano(self):
        if self.data:
            return self.data.year

    @property
    def month_name(self):
        import locale
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        return self.data.strftime('%B')

    def copy_contas_from_previous(self):
        self.objects.filter()

    class Meta:
        ordering = ['-data']


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

    @property
    def foi_pago_este_mes(self):
        return self.data_pagamento and datetime.now().strftime('%Y%m') == self.data_pagamento.strftime('%Y%m')

    @property
    def foi_pago_com_atraso(self):
        return self.data_pagamento \
            and self.data_vencimento.year < self.data_pagamento.year \
            or self.data_vencimento.month < self.data_pagamento.month

    def registrar_pagamento(self):
        self.data_pagamento = date.today()
        self.save()


