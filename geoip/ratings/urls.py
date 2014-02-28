from django.conf.urls import patterns, url

urlpatterns = patterns('ratings.views',
                       url(r'^get_rating$', 'get_rating'),
                       url(r'^scan_ratings$', 'scan_ratings'),
                       )
