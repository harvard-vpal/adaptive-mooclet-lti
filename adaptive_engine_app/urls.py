# these correspond to views defined in urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'adaptive_engine_app.views.index', name='index'), # http://localhost:8000/adaptive_engine_app/   
    url(r'^get_version_of_component$', 'adaptive_engine_app.views.get_version_of_component', name='get_version_of_component'), # http://localhost:8000/adaptive_engine_app/get_version_of_component
    url(r'^submit_result_of_version$', 'adaptive_engine_app.views.submit_result_of_version', name='submit_result_of_version')
)
