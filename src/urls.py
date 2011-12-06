from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'core.views.homepage', {'template': 'index.html'}),
    (r'^inscricao/', include('subscriptions.urls', namespace='subscriptions')),
    (r'^', include('core.urls', namespace='core')),
)

urlpatterns += staticfiles_urlpatterns()