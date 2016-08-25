from django.conf.urls import url, include
from . import views

urlpatterns = [

    # question related
    url(r'^detail$', views.question_detail, name='question_detail'),
    url(r'^modify$', views.question_modify, name='question_modify'),
    url(r'^results$', views.question_results, name='question_results'),

    url(r'^mooclet/create$', views.mooclet_create, name='mooclet_create'),
    url(r'^mooclet/(?P<mooclet_id>[0-9]+)/', include('engine.urls_mooclet')),

    url(r'^answer/create$', views.answer_create, name='answer_create'),
    url(r'^answer/(?P<answer_id>[0-9]+)/', include('engine.urls_answer')),

]