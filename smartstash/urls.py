from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from smartstash.core import views
from smartstash.auth import views as authviews


urlpatterns = patterns(
    '',
    url(r'^$', views.site_index, name='site-index'),
    url(r'^stash/$', views.view_items, name='view-stash'),
    url(r'^saveme/$', views.saveme, name='saveme'),
    url(r'^images/', include('smartstash.images.urls',
        namespace='image')),

    url(r'^localauth/zotero/$', authviews.zotero_oauth, name='zotero'),
#    url(r'^localauth/', include('smartstash.auth.urls', namespace='localauth')),

    # static site content pages
    url(r'^connect/', TemplateView.as_view(template_name='connect.html'),
        name='connect'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),

    # examples
    # url(r'^input/', include('smartstash.input.urls',
    #     namespace='input')
    # url(r'^$', 'smartstash.views.home', name='home'),
    # url(r'^smartstash/', include('smartstash.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
