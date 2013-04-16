# -*- encoding : utf-8 -*-

from django.contrib import admin
from models import Conta, Controle


class ContaAdmin(admin.ModelAdmin):
    class Meta:
        model = Conta


class ControleAdmin(admin.ModelAdmin):
    class Meta:
        model = Controle


admin.site.register(Conta, ContaAdmin)
admin.site.register(Controle, ControleAdmin)
