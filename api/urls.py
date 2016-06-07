from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'quizzes', views.QuizViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),

	# custom endpoints
	url(r'^get_question$', 'api.views.get_question', name='get_question'),
	url(r'^get_explanation_for_student$', 'api.views.get_explanation_for_student', name='get_explanation_for_student'),

]

