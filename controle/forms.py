# -*- encoding : utf-8 -*-
from django import forms
from django.forms.widgets import TextInput
from django.forms.extras.widgets import SelectDateWidget

from models import Conta
from models import Controle


class ContaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContaForm, self).__init__(*args, **kwargs)
        self.fields['data_pagamento'].widget = TextInput(attrs={'class': 'datepicker'})

    class Meta:
        model = Conta
        exclude = ('controle')


class UploadContaForm(forms.ModelForm):
    arquivo = forms.FileField()

    class Meta:
        model = Conta


class ControleForm(forms.ModelForm):
    data = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Controle
        exclude = ('owner',)
