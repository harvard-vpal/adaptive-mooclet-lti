from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',

    url(r'^question/(?P<question_id>[0-9]+)$', views.question, name='question'),
	url(r'^answer/(?P<answer_id>[0-9]+)$', views.answer, name='answer'),
	url(r'^placeholder$', views.placeholder, name='placeholder'),
	url(r'^complete$', views.complete, name='complete'),

)