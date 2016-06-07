from django.conf.urls import patterns, url


urlpatterns = [

    # url(r'^$', 'lti.views.index', name='index'),
    url(r'^tool_config$', 'lti.views.tool_config', name='tool_config'),

    url(r'^launch/(?P<quiz_id>[0-9]+)$', 'lti.views.launch', name='launch'),
    url(r'^launch_resource_selection$', 'lti.views.launch_resource_selection', name='launch_resource_selection'),
    url(r'^launch_course_navigation$', 'lti.views.launch_course_navigation', name='launch_course_navigation'),

    url(r'^return_launch_url/(?P<quiz_id>[0-9]+)$', 'lti.views.return_launch_url', name='return_launch_url'),
    url(r'^return_outcome$', 'lti.views.return_outcome', name='return_outcome'),

]