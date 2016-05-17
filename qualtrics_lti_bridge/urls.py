from django.conf.urls import patterns, include, url
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^$', 'qualtrics_lti_bridge.views.home', name='home'),
    url(r'^auth_error/', 'qualtrics_lti_bridge.views.lti_auth_error', name='lti_auth_error'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^qlb/', include('qlb.urls', namespace="qlb")),
    url(r'^adaptive_engine/', include('adaptive_engine_app.urls', namespace="adaptive_engine")),

)
