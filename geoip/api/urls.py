from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
                       url(r'^wifi_report$', 'wifi_report'),
                       url(r'^scan_report$', 'scan_report'),
                       url(r'^dnsadd$', 'dns_add'),
                       url(r'^history/(?P<uuid>.+)', 'history'),
                       url(r'^pref_report', 'pref_report'),
                       )
