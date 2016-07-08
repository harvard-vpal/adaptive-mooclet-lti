from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',

    url(r'^question/(?P<question_id>[0-9]+)$', views.question, name='question'),
	url(r'^explanation/(?P<explanation_id>[0-9]+)$', views.explanation, name='explanation'),
	url(r'^placeholder$', views.placeholder, name='placeholder'),
	url(r'^complete$', views.complete, name='complete'),

)