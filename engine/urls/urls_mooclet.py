from django.conf.urls import url, include
from .. import views

urlpatterns = [
    url(r'^create/(?P<type>\w+)$', views.mooclet_create, name='mooclet_create'),    
    url(r'^(?P<mooclet_id>[0-9]+)/', include('engine.urls.urls_mooclet_detail')),
]