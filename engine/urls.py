from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    # resource selection
    url(r'^quiz_create_options$', views.quiz_create_options, name='quiz_create_options'),
    url(r'^quiz_create_blank$', views.quiz_create_blank, name='quiz_create_blank'),
    url(r'^quiz_create_url$', views.quiz_create_url, name='quiz_create_url'),
 
    # instructor lti view
    # url(r'^display_quiz/(?P<quiz_id>[0-9]+)$', views.display_quiz, name='display_quiz'),
    # url(r'^manage_quiz/(?P<quiz_id>[0-9]+)$', views.manage_quiz, name='manage_quiz'),
    # url(r'^modify_quiz/(?P<quiz_id>[0-9]+)$', views.modify_quiz, name='modify_quiz'),
    # url(r'^manage_explanations/(?P<quiz_id>[0-9]+)$', views.manage_explanations, name='manage_explanations'),
    # url(r'^create_explanation_for_answer/(?P<answer_id>[0-9]+)$', views.create_explanation_for_answer, name='create_explanation_for_answer'),

    url(r'^researcher_request$', views.researcher_request, name='researcher_request'),

    # renamed views
    url(r'^quiz_display/(?P<quiz_id>[0-9]+)$', views.quiz_display, name='quiz_display'),
    url(r'^quiz_detail/(?P<quiz_id>[0-9]+)$', views.quiz_detail, name='quiz_detail'),
    url(r'^quiz_update/(?P<quiz_id>[0-9]+)$', views.quiz_update, name='quiz_update'),

    url(r'^explanation_list/(?P<quiz_id>[0-9]+)$', views.explanation_list, name='explanation_list'),
    url(r'^explanation_create/(?P<answer_id>[0-9]+)$', views.explanation_create, name='explanation_create'),
    url(r'^explanation_modify/(?P<explanation_id>[0-9]+)$', views.explanation_modify, name='explanation_modify'),


    ## CBVs
    # url(r'quiz_detail^$',views.QuizDetail.as_view(),name='QuizDetail'),
    # url(r'reseacher_create^$',views.ResearcherCreate.as_view(),name='ResearcherCreate'),


    # url(r'^end_of_quiz/(?P<quiz_id>[0-9]+)$', 'engine.views.end_of_quiz', name='end_of_quiz'),
    # url(r'^create_quiz$', 'engine.views.create_quiz', name='create_quiz'),   
    # url(r'^select_or_create_quiz$', 'engine.views.select_or_create_quiz', name='select_or_create_quiz'),
]

