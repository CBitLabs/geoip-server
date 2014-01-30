from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
                       url(r'^add/$', 'add'),
                       url(r'^dnsadd/$', 'dns_add'),
                       url(r'^history/(?P<uuid>.+)', 'history'),
                       )
