from django.conf.urls import url, include
from .. import views

urlpatterns = [

    # question related
    url(r'^$', views.question_detail, name='question_detail'),
    url(r'^modify$', views.question_modify, name='question_modify'),
    url(r'^results$', views.question_results, name='question_results'),

    url(r'^answer/create$', views.answer_create, name='answer_create'),

]