from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from smartstash.core import views
from smartstash.auth import views as authviews


urlpatterns = patterns(
    '',
    url(r'^$', views.site_index, name='site-index'),
    url(r'^stash/$', views.view_items, name='view-stash'),
    url(r'^dummy1/$', views.dummy1, name='dummy1'),
    url(r'^dummy2/$', views.dummy2, name='dummy2'),
    url(r'^dummy3/$', views.dummy3, name='dummy3'),
    url(r'^saveme/$', views.saveme, name='saveme'),


    url(r'^localauth/zotero/$', authviews.zotero_oauth, name='zotero'),
#    url(r'^localauth/', include('smartstash.auth.urls', namespace='localauth')),

    # static site content pages
    url(r'^about/', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^connect/', TemplateView.as_view(template_name='connect.html'),
        name='connect'),
    url(r'^dummy2/', TemplateView.as_view(template_name='dummy2.html'),
        name='dummy2'),
    url(r'^dummy3/', TemplateView.as_view(template_name='dummy3.html'),
        name='dummy3'),
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
