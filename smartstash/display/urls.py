from django.conf.urls import patterns, url
from smartstash.display import views

urlpatterns = patterns(
    '',
    url(r'^$', views.view_results, name='items'),
)
