# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Possession


class PossessionAdmin(admin.ModelAdmin):
    class Meta:
        model = Possession

admin.site.register(Possession, PossessionAdmin)
