from django.conf.urls import url, include
from .. import views

urlpatterns = [

    url(r'^launch_quiz$', views.launch_quiz, name='launch_quiz'),
    
    # instructor management views
    url(r'^$', views.quiz_detail, name='quiz_detail'),
    url(r'^modify$', views.quiz_modify, name='quiz_modify'),
    url(r'^launch_quiz_manager$', views.launch_quiz_manager, name='launch_quiz_manager'),
    
    # collaborator-related
    url(r'^collaborator_request$', views.collaborator_request, name='collaborator_request'),
    url(r'^collaborator_create$', views.collaborator_create, name='collaborator_create'),

    url(r'^question/create$', views.question_create, name='question_create'),
    # url(r'^question/(?P<question_id>[0-9]+)/', include('engine.urls_question')),


    url(r'^mooclet/', include('engine.urls.urls_mooclet')),

]