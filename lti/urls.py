from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^$', 'lti.views.index', name='index'),
    url(r'^tool_config$', 'lti.views.tool_config', name='tool_config'),
    url(r'^quiz_list$', 'lti.views.quiz_list', name='quiz_list'),
    url(r'^select_or_create_quiz$', 'lti.views.select_or_create_quiz', name='select_or_create_quiz'),
    url(r'^create_quiz$', 'lti.views.create_quiz', name='create_quiz'),
    url(r'^create_qualtrics_quiz_from_url$', 'lti.views.create_qualtrics_quiz_from_url', name='create_qualtrics_quiz_from_url'),
    url(r'^create_quiz_from_submission$', 'lti.views.create_quiz_from_submission', name='create_quiz_from_submission'),
	url(r'^embed_quiz/(?P<quiz_id>[0-9]+)$', 'lti.views.embed_quiz', name='embed_quiz'),
	url(r'^launch_quiz/(?P<quiz_id>[0-9]+)$', 'lti.views.launch_quiz', name='launch_quiz'),
    # url(r'^manage_quiz/(?P<quiz_id>[0-9]+)$', 'lti.views.manage_quiz', name='manage_quiz'),
    url(r'^modify_quiz/(?P<quiz_id>[0-9]+)$', 'lti.views.modify_quiz', name='modify_quiz'),
    # url(r'^end_of_quiz/(?P<quiz_id>[0-9]+)$', 'lti.views.end_of_quiz', name='end_of_quiz'),
    url(r'^end_of_quiz$', 'lti.views.end_of_quiz', name='end_of_quiz'),

)