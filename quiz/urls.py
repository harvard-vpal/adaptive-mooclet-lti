from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^display_quiz_question/(?P<question_id>[0-9]+)$', 'quiz.views.display_quiz_question', name='display_quiz_question'),
	url(r'^display_quiz_explanation/(?P<explanation_id>[0-9]+)$', 'quiz.views.display_quiz_explanation', name='display_quiz_explanation'),

)