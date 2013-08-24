from django.conf.urls import patterns, url
from smartstash.auth import views


urlpatterns = patterns(
    '',
    # url(r'^zotero/$', views.zotero_oauth, name='zotero'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^logged-in/$', views.logged_in, name='logged-in'),
    url(r'^login-error/$', views.login_error, name='login-error'),
)
