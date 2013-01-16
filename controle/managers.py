# -*- coding: utf-8 -*-

from datetime import date

from django.db import models


class ControleManager(models.Manager):

    def get_or_create_current(self):
        return self.get_or_create(data=date.today())[0]

    def by_month_and_year(self, month, year):
        return self.filter(data__month=month, data__year=year)

