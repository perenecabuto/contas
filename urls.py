# -*- encoding : utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='/controle'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^controle/', include('controle.urls')),

    #url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'https://accounts.google.com/Login'}, name='logout'),

    url(r'^nodefs_tree/', include('django_nodefs.urls')),
    #url(r'^notification/', include('notification.urls')),
)

from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
