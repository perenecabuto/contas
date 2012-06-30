# -*- encoding : utf-8 -*-
from django.forms import ModelForm

from models import Conta
from models import Controle


class ContaForm(ModelForm):

    class Meta:
        model = Conta
        exclude = ('controle',)


class ControleForm(ModelForm):

    class Meta:
        model = Controle
