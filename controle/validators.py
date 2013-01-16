from django.core.exceptions import ValidationError


def unique_controle_per_month_year(date):
    from models import Controle

    if Controle.objects.by_month_and_year(date.month, date. year).exists():
        raise ValidationError(u'Controle already exists')
