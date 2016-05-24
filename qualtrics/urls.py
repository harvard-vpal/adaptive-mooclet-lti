from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^create_qualtrics_quiz_from_url$', 'qualtrics.views.create_qualtrics_quiz_from_url', name='create_qualtrics_quiz_from_url'),
	url(r'^qsf_for_quiz/(?P<quiz_id>[0-9]+)$', 'qualtrics.views.qsf_for_quiz', name='qsf_for_quiz'),
)