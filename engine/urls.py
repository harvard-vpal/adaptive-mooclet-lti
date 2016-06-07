from django.conf.urls import patterns, url

urlpatterns = patterns('',
	# resource selection
	url(r'^quiz_creation_options$', 'engine.views.quiz_creation_options', name='quiz_creation_options'),
	url(r'^create_blank_quiz$', 'engine.views.create_blank_quiz', name='create_blank_quiz'),

	# instructor lti view
    url(r'^manage_quiz/(?P<quiz_id>[0-9]+)$', 'engine.views.manage_quiz', name='manage_quiz'),
    url(r'^modify_quiz/(?P<quiz_id>[0-9]+)$', 'engine.views.modify_quiz', name='modify_quiz'),

    # url(r'^end_of_quiz/(?P<quiz_id>[0-9]+)$', 'engine.views.end_of_quiz', name='end_of_quiz'),
    # url(r'^create_quiz$', 'engine.views.create_quiz', name='create_quiz'),   
    # url(r'^select_or_create_quiz$', 'engine.views.select_or_create_quiz', name='select_or_create_quiz'),
  
)
