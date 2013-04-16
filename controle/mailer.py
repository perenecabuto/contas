# -*- coding: utf-8 -*-

from django.conf import settings
from django import template
from django.core.mail import EmailMessage

DEFAULT_SENDER_EMAIL = getattr(settings, 'DEFAULT_SENDER_EMAIL', "example@domain.com")


def send_mail(subject, message, from_email, recipient_list):
    msg = EmailMessage(subject, message, from_email, recipient_list)
    msg.content_subtype = "html"
    msg.send()


def notifica_vencimento(conta, target_user, sender_email=DEFAULT_SENDER_EMAIL):
    subject = 'Conta %s venceu' % conta
    ctx = template.Context({'conta': conta, 'user': target_user})
    tpl = template.loader.get_template('controle/mailer/notifica_vencimento.html')

    send_mail(subject, tpl.render(ctx), sender_email, (target_user.email,))
