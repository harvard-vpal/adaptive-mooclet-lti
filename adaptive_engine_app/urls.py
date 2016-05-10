# these correspond to views defined in urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^get_explanation_for_answer$', 'adaptive_engine_app.views.get_explanation_for_answer', name='get_explanation_for_answer'), # http://localhost:8000/adaptive_engine_app/get_explanation_for_answer
    url(r'^submit_result_of_explanation$', 'adaptive_engine_app.views.submit_result_of_explanation', name='submit_result_of_explanation')
)
