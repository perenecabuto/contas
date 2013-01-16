# -*- coding: utf-8 -*-

from django.forms import widgets
from django.utils.dates import MONTHS

from datetime import date


class SelectMonthYearWidget(widgets.MultiWidget):

    def __init__(self, attrs=None):
        current_year = date.today().year
        years = reversed([(current_year + i, current_year + i) for i in range(-2, 2)])
        months = MONTHS.items()

        _widgets = (
            widgets.HiddenInput(attrs=attrs),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(self.__class__, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [1, value.month, value.year]
        return [1, None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]

        try:
            d = date(day=1, month=int(datelist[1]), year=int(datelist[2]))
            return str(d)
        except ValueError:
            return ''

