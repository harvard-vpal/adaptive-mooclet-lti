from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    ### resource selection ###
    url(r'^quiz_create_options$', views.quiz_create_options, name='quiz_create_options'),
    url(r'^quiz_create_blank$', views.quiz_create_blank, name='quiz_create_blank'),
    url(r'^quiz_create_url$', views.quiz_create_url, name='quiz_create_url'),
 
    ### instructor management views ###

    url(r'^quiz_display/(?P<quiz_id>[0-9]+)$', views.quiz_display, name='quiz_display'),
    url(r'^quiz_detail/(?P<quiz_id>[0-9]+)$', views.quiz_detail, name='quiz_detail'),
    url(r'^quiz_update/(?P<quiz_id>[0-9]+)$', views.quiz_update, name='quiz_update'),

    url(r'^explanation_list/(?P<quiz_id>[0-9]+)$', views.explanation_list, name='explanation_list'),
    url(r'^explanation_create/(?P<mooclet_id>[0-9]+)$', views.explanation_create, name='explanation_create'),
    url(r'^explanation_modify/(?P<explanation_id>[0-9]+)$', views.explanation_modify, name='explanation_modify'),

    # "list mooclets"
    url(r'^answer_list/(?P<question_id>[0-9]+)$', views.answer_list, name='answer_list'),
    # "interact with mooclet"
    url(r'^mooclet_detail/(?P<mooclet_id>[0-9]+)$', views.mooclet_detail, name='mooclet_detail'),

    url(r'^collaborator_request', views.collaborator_request, name='collaborator_request'),
    url(r'^collaborator_create/(?P<quiz_id>[0-9]+)$', views.collaborator_create, name='collaborator_create'),


    ## CBVs
    # url(r'quiz_detail^$',views.QuizDetail.as_view(),name='QuizDetail'),
    # url(r'reseacher_create^$',views.ResearcherCreate.as_view(),name='ResearcherCreate'),

]

