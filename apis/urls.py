from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from . import views

# router_mooclet = routers.DefaultRouter()
# router_mooclet.register(r'mooclet', views.MoocletViewSet)
# router_mooclet.register(r'version', views.VersionViewSet)

# router_quip = routers.DefaultRouter()
# router_quip.register(r'quiz', views.QuizViewSet)
# router_quip.register(r'question', views.QuestionViewSet)

urlpatterns = [
	# url(r'^', include(router_mooclet.urls, namespace='mooclet')),

	# custom endpoints
	url(r'^get_question$', views.get_question, name='get_question'),
	url(r'^get_explanation_for_student$', views.get_explanation_for_student, name='get_explanation_for_student'),
	url(r'^submit_result_of_explanation$', views.submit_result_of_explanation, name='submit_result_of_explanation'),
	url(r'^submit_quiz_grade$', views.submit_quiz_grade, name='submit_quiz_grade'),
	url(r'^submit_user_variable$', views.submit_value, name='submit_user_variable'),
	url(r'^update_intermediates$', views.update_intermediates, name='update_intermediates'),
]

