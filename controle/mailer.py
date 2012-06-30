from django.conf import settings
from django import template
from django.core.mail import send_mail

DEFAULT_SENDER_EMAIL = getattr(settings, 'DEFAULT_SENDER_EMAIL', "example@domain.com")


def notifica_vencimento(conta, target_user, sender_email=DEFAULT_SENDER_EMAIL):
    subject = 'Conta %s venceu' % conta
    ctx = template.Context({'conta': conta, 'user': target_user})
    tpl = template.loader.get_template('controle/mailer/notifica_vencimento.html')

    send_mail(subject, tpl.render(ctx), sender_email, (target_user,))
