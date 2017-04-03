from django.conf.urls import url, include
from .. import views

urlpatterns = [

    # question related
    url(r'^$', views.question_detail, name='question_detail'),
    url(r'^modify$', views.question_modify, name='question_modify'),
	url(r'^question_and_answers_modify$', views.question_and_answers_modify, name='question_and_answers_modify'),
    url(r'^results$', views.question_results, name='question_results'),
    url(r'^answer/create$', views.answer_create, name='answer_create'),
    url(r'^answer/list$', views.answer_list, name='answer_list'),
    url(r'^get_question_data$', views.get_question_results, name='get_question_results'),
    url(r'^calculus_comparison$', views.calculus_comparison, name='calculus_comparison')
]