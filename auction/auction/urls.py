from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'www.views.home', name='home'),
    url(r'^login/$', 'www.views.my_login'),
    url(r'^register/$', 'www.views.register'),
    url(r'^accounts/', include('userprofiles.urls')),
    url(r'^logout_view/$', "www.views.logout_view", name='logout_view'),
    url( r'^activate/(?P<email>[\w\.-]+@[\w\.-]+)/$', 'www.views.activate' ),

    # url(r'^auction/', include('auction.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
