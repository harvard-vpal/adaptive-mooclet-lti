from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^question/(?P<question_id>[0-9]+)$', 'quiz.views.question', name='question'),
	url(r'^explanation/(?P<explanation_id>[0-9]+)$', 'quiz.views.explanation', name='explanation'),
	url(r'^placeholder$', 'quiz.views.placeholder', name='placeholder'),

)