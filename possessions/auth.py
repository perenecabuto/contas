 # -*- coding: utf-8 -*-

import re
from django.contrib.auth.models import User
from openid.consumer.consumer import SUCCESS
#from django.core.mail import mail_admins


class OpenIDBackend:
    def authenticate(self, openid_response):
        if openid_response is None:
            return None

        if openid_response.status != SUCCESS:
            return None

        email = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.email')
        first_name = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.firstname')
        last_name = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.lastname')
        username = re.findall(r'^(.+?)@', email)[0]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            user = User.objects.create_user(username, email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
