from django.conf.urls import url
from . import views

urlpatterns = [
    ### resource selection ###
    url(r'^quiz_create_options$', views.quiz_create_options, name='quiz_create_options'),
    url(r'^quiz_create_blank$', views.quiz_create_blank, name='quiz_create_blank'),
    url(r'^quiz_create_url$', views.quiz_create_url, name='quiz_create_url'),

    # shortcut for launching sandbox quiz
    url(r'^launch_sandbox$', views.launch_sandbox, name='launch_sandbox'),

    ### instructor management views ###
    url(r'^(?P<quiz_id>[0-9]+)/quiz_display$', views.quiz_display, name='quiz_display'),
    url(r'^(?P<quiz_id>[0-9]+)$', views.quiz_detail, name='quiz_detail'),
    url(r'^(?P<quiz_id>[0-9]+)/quiz_update$', views.quiz_update, name='quiz_update'),

    # collaborator-related
    url(r'^(?P<quiz_id>[0-9]+)/collaborator_request', views.collaborator_request, name='collaborator_request'),
    url(r'^(?P<quiz_id>[0-9]+)/collaborator_create', views.collaborator_create, name='collaborator_create'),

    # "list mooclets for a quiz"
    url(r'^(?P<quiz_id>[0-9]+)/quiz_mooclets$', views.quiz_mooclets, name='quiz_mooclets'),
    

    # question related
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)$', views.question_detail, name='question_detail'),
    url(r'^(?P<quiz_id>[0-9]+)/question/create$', views.question_create, name='question_create'),
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/modify$', views.question_modify, name='question_modify'),

    url(r'^(?P<quiz_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)$', views.answer_detail, name='answer_detail'),
    url(r'^(?P<quiz_id>[0-9]+)/answer/create$', views.answer_create, name='answer_create'),
    url(r'^(?P<quiz_id>[0-9]+)/answer/(?P<question_id>[0-9]+)/modify$', views.answer_modify, name='answer_modify'),


    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/explanation_list$', views.explanation_list, name='explanation_list'),
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/explanation_create/(?P<mooclet_id>[0-9]+)$', views.explanation_create, name='explanation_create'),
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/explanation_modify/(?P<explanation_id>[0-9]+)$', views.explanation_modify, name='explanation_modify'),


    # "interact with mooclet"
    url(r'^(?P<quiz_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)$', views.mooclet_detail, name='mooclet_detail'),
    url(r'^(?P<quiz_id>[0-9]+)/mooclet/create$', views.mooclet_create, name='mooclet_create'),    
    url(r'^(?P<quiz_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)/simulate_probabilities$', views.mooclet_simulate_probabilities, name='mooclet_simulate_probabilities'),
    url(r'^(?P<quiz_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)/modify_version_values$', views.mooclet_modify_version_values, name='mooclet_modify_version_values'),
    url(r'^(?P<quiz_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)/list_values$', views.mooclet_list_values, name='mooclet_list_values'),


    ## CBVs
    # url(r'quiz_detail^$',views.QuizDetail.as_view(),name='QuizDetail'),
    # url(r'reseacher_create^$',views.ResearcherCreate.as_view(),name='ResearcherCreate'),

]

