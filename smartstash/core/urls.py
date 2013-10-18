from django.conf.urls import patterns, url
from smartstash.core import views


urlpatterns = patterns(
    '',
    url(r'^$', views.view_items, name='view'),
    url(r'^list/$', views.save_list, name='list'),
)

