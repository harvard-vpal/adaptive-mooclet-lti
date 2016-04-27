# these correspond to views defined in urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'example_app.views.index', name='index'), # http://localhost:8000/example_app/   
    url(r'^handle_get_param$', 'example_app.views.handle_get_param', name='handle_get_param'), # http://localhost:8000/example_app/handle_get_param
    url(r'^return_json$', 'example_app.views.return_json', name='return_json'),
    url(r'^do_redirect$', 'example_app.views.do_redirect', name='do_redirect'),

)
