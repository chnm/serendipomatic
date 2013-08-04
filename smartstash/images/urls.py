from django.conf.urls import patterns, include, url
from smartstash.images import views

urlpatterns = patterns(
    '',
    url(r'^resize/(?P<size>[0-9]+)/$', views.resize, name='resize'),
)
