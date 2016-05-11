# these correspond to views defined in urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^get_explanation_for_student$', 'adaptive_engine_app.views.get_explanation_for_student', name='get_explanation_for_student'), # http://localhost:8000/adaptive_engine_app/get_explanation_for_student
    url(r'^submit_result_of_explanation$', 'adaptive_engine_app.views.submit_result_of_explanation', name='submit_result_of_explanation'),
    url(r'^add_explanation$', 'adaptive_engine_app.views.add_explanation', name='add_explanation'),
    url(r'^get_question$', 'adaptive_engine_app.views.get_question', name='get_question'),
    url(r'^change_question$', 'adaptive_engine_app.views.change_question', name='change_question'),
    url(r'^change_explanation$', 'adaptive_engine_app.views.change_explanation', name='change_explanation'),
    url(r'^get_explanations_for_question$', 'adaptive_engine_app.views.get_explanations_for_question', name='get_explanations_for_question'),
    url(r'^add_question$', 'adaptive_engine_app.views.add_question', name='add_question')
)
