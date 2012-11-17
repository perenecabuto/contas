# -*- encoding : utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import TextInput

from models import Conta
from models import Controle

from datetime import date


class ContaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContaForm, self).__init__(*args, **kwargs)
        today = date.today()
        self.fields['data_pagamento'].widget = TextInput(attrs={'class': 'datepicker'})

    class Meta:
        model = Conta
        exclude = ('controle', 'arquivo')


class ControleForm(ModelForm):

    class Meta:
        model = Controle
