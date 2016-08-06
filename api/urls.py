from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'quizzes', views.QuizViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),

	# custom endpoints
	url(r'^get_question$', views.get_question, name='get_question'),
	url(r'^get_explanation_for_student$', views.get_explanation_for_student, name='get_explanation_for_student'),
	url(r'^submit_result_of_explanation$', views.submit_result_of_explanation, name='submit_result_of_explanation'),
	url(r'^submit_quiz_grade$', views.submit_quiz_grade, name='submit_quiz_grade'),
	url(r'^submit_user_variable$', views.submit_value, name='submit_user_variable'),
]

