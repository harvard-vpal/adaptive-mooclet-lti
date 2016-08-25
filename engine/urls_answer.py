from django.conf.urls import url, include
from . import views

urlpatterns = [

    # url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)$', views.answer_detail, name='answer_detail'),
    url(r'^detail$', views.answer_detail, name='answer_detail'),
    url(r'^modify$', views.answer_modify, name='answer_modify'),

    url(r'^mooclet/create$', views.mooclet_create, name='mooclet_create'),    
    url(r'^mooclet/(?P<mooclet_id>[0-9]+)/', include('engine.urls_mooclet')),

]