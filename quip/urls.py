from django.conf.urls import include, url
from rest_framework import routers
from views import api as api_views
from views import quiz as quiz_views

router = routers.DefaultRouter()
router.register(r'quiz', api_views.QuizViewSet)
router.register(r'question', api_views.QuestionViewSet)

urlpatterns = [

	# api endpoints
	url(r'^api/', include(router.urls, namespace='api')),

	# quiz views (student facing)
    url(r'^question/(?P<question_id>[0-9]+)$', quiz_views.question, name='question'),
	url(r'^answer/(?P<answer_id>[0-9]+)$', quiz_views.answer, name='answer'),
	url(r'^placeholder$', quiz_views.placeholder, name='placeholder'),
	url(r'^complete$', quiz_views.complete, name='complete'),

]