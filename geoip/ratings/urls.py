from django.conf.urls import patterns, url

urlpatterns = patterns('ratings.views',
                       url(r'^get_rating$', 'get_rating'),
                       )
