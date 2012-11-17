# -*- encoding : utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', redirect_to, {'url': '/controle'}, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^controle/', include('controle.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
