from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	
    url(r'^$', views.home, name='home'),
    url(r'^auth_error/', views.lti_auth_error, name='lti_auth_error'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lti/', include('lti.urls', namespace="lti")),
    url(r'^mooclet/', include('mooclet.urls', namespace="mooclet")),
    url(r'^quip/', include('quip.urls', namespace="quip")),
    url(r'^qualtrics/', include('qualtrics.urls', namespace="qualtrics")),
    url(r'^quipmanager/', include('quipmanager.urls.urls', namespace="quipmanager")),
    
    url(r'^api/', include('apis.urls', namespace="api")),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
