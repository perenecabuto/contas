# -*- encoding : utf-8 -*-
from django.forms import ModelForm
from django_tables2.utils import A
import django_tables2 as tables

from models import Conta

class ContaForm(ModelForm):
  class Meta:
    model = Conta
    exclude = ('controle',)

class ContaTable(tables.Table):
  nome = tables.TemplateColumn('<a href={% url controle.views.edit id=record.pk %}>{{ record.nome }}</a>')

  class Meta:
    model = Conta

