from django.conf.urls import url, include
from .. import views

urlpatterns = [

    # # general views for mooclet
    url(r'^detail$', views.mooclet_detail, name='mooclet_detail'), 
    url(r'^simulate_probabilities$', views.mooclet_simulate_probabilities, name='mooclet_simulate_probabilities'),
    url(r'^modify_version_values$', views.mooclet_modify_version_values, name='mooclet_modify_version_values'),
    url(r'^list_values$', views.mooclet_list_values, name='mooclet_list_values'),
    url(r'^mooclet_results$', views.mooclet_results, name='mooclet_results'),

    url(r'^version/create$', views.version_create, name='version_create'),
    url(r'^version/(?P<version_id>[0-9]+)/modify$', views.version_modify, name='version_modify'),
    url(r'^explanation/create$', views.explanation_create, name='explanation_create'),
    url(r'^explanation_modify/(?P<version_id>[0-9]+)/modify$', views.explanation_modify, name='explanation_modify'),


    # url(r'^version/(?P<version_id>[0-9]+)/', include('engine.urls_version')),

    # TODO version-type specific
    # TOOD explanation create/edit

    # # explanation-mooclet specific
    # url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/explanation_mooclet/explanation_list$', views.explanation_list, name='explanation_list'),
    # url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/explanation_mooclet/explanation_create$', views.explanation_create, name='explanation_create'),
    # url(r'^(?P<quiz_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/explanation_mooclet/explanation_modify/(?P<explanation_id>[0-9]+)$', views.explanation_modify, name='explanation_modify'),

]