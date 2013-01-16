# -*- coding: utf-8 -*-

from django.core.signals import request_finished
from django.dispatch import receiver
from django.core.handlers.wsgi import WSGIRequest

from .models import Conta, Controle


@receiver(request_finished, dispatch_uid="ovo")
def terminou(sender, **kwargs):
    print "-" * 100
    print "finished"
    print "-" * 100

