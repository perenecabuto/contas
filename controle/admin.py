# -*- encoding : utf-8 -*-
from django.contrib import admin
from models import Conta

class ContaAdmin(admin.ModelAdmin):
  class Meta:
    model = Conta

admin.site.register(Conta, ContaAdmin)
