from django.conf.urls import url, include
from .. import views

urlpatterns = [

    url(r'^launch$', views.launch, name='launch'),
    
    # instructor management views
    url(r'^$', views.quiz_detail, name='quiz_detail'),
    url(r'^modify$', views.quiz_modify, name='quiz_modify'),
    
    # collaborator-related
    url(r'^collaborator_request$', views.collaborator_request, name='collaborator_request'),
    url(r'^collaborator_create$', views.collaborator_create, name='collaborator_create'),

    url(r'^question/create$', views.question_create, name='question_create'),
    # url(r'^question/(?P<question_id>[0-9]+)/', include('engine.urls_question')),


    url(r'^mooclet/', include('engine.urls.urls_mooclet')),

]