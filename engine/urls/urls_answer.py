from django.conf.urls import url, include
from .. import views

urlpatterns = [

    url(r'^$', views.answer_detail, name='answer_detail'),
    url(r'^modify$', views.answer_modify, name='answer_modify'),

    # url(r'^mooclet/create/(?P<type>\w+)$', views.mooclet_create, name='mooclet_create'),
    url(r'^mooclet/', include('engine.urls.urls_mooclet')),

]