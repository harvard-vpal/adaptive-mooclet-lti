from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^create_qualtrics_quiz_from_url$', views.create_qualtrics_quiz_from_url, name='create_qualtrics_quiz_from_url'),
	url(r'^qsf_for_question/(?P<question_id>[0-9]+)$', views.qsf_for_question, name='qsf_for_question'),

)