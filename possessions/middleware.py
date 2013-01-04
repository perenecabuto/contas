# -*- coding: utf-8 -*-

from re import compile
from django.http import HttpResponseRedirect
from django.conf import settings
from threading import local

thread_locals = local()

EXEMPT_URLS = [compile(settings.LOGIN_URL)]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


def get_current_user():
    return getattr(thread_locals, 'user', None)


class AuthRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), """
            The Login Required middleware
            requires authentication middleware to be installed. Edit your
            MIDDLEWARE_CLASSES setting to insert\
            'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't
            work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes
            'django.core.context_processors.auth'.
        """

        thread_locals.user = request.user

        if not request.user.is_authenticated():
            path = request.path_info

            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)
