# these correspond to views defined in urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^get_explanation$', 'adaptive_engine_app.views.get_explanation', name='get_explanation'), # http://localhost:8000/adaptive_engine_app/get_explanation
    url(r'^submit_result_of_explanation$', 'adaptive_engine_app.views.submit_result_of_explanation', name='submit_result_of_explanation')
)
