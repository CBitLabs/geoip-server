from django.conf.urls import patterns, include, url
from django.shortcuts import HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^robots\.txt$', lambda r: HttpResponse(
                           "User-agent: *\nDisallow: /",
                           mimetype="text/plain")),
                       url(r'', include("api.urls")),
                       url(r'ratings/', include("ratings.urls")),
                       )
