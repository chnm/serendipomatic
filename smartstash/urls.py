from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from smartstash.core import views


urlpatterns = patterns(
    '',
    url(r'^$', views.site_index, name='site-index'),
    url(r'^stash/$', views.view_items, name='view-stash'),

    # static site content pages
    url(r'^about/', TemplateView.as_view(template_name='about.html'),
        name='about'),

    # examples
    # url(r'^input/', include('smartstash.input.urls',
    #     namespace='input')
    # url(r'^$', 'smartstash.views.home', name='home'),
    # url(r'^smartstash/', include('smartstash.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
