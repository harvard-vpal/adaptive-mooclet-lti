from django.conf.urls import url, include
from .. import views

urlpatterns = [
    ### resource selection ###
    url(r'^quiz_create_options$', views.quiz_create_options, name='quiz_create_options'),
    url(r'^quiz_create_blank$', views.quiz_create_blank, name='quiz_create_blank'),
    url(r'^quiz_create_url$', views.quiz_create_url, name='quiz_create_url'),

    # shortcut for launching sandbox quiz
    url(r'^launch_sandbox$', views.launch_sandbox, name='launch_sandbox'),

    # include child urls - start with longest pattern so that mooclet patterns handling more parameters are accessed first
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/', include('engine.urls.urls_answer')),
    url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/', include('engine.urls.urls_question')),
    url(r'^(?P<quiz_id>[0-9]+)/', include('engine.urls.urls_quiz')),


    # url(r'^question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)/', include('engine.urls_mooclet')),
    # url(r'^question/(?P<question_id>[0-9]+)/mooclet/(?P<mooclet_id>[0-9]+)/', include('engine.urls_mooclet')),
    # url(r'^mooclet/(?P<mooclet_id>[0-9]+)/', include('engine.urls_mooclet')),

    ## CBVs
    # url(r'quiz_detail^$',views.QuizDetail.as_view(),name='QuizDetail'),
    # url(r'reseacher_create^$',views.ResearcherCreate.as_view(),name='ResearcherCreate'),

]

