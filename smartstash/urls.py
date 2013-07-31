from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from smartstash.input import views as input_views
from smartstash.display import views as display_views

urlpatterns = patterns('',
    url(r'^$', input_views.site_index, name='site-index'),
    url(r'^items/', include('smartstash.display.urls',
        namespace='display')),

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
