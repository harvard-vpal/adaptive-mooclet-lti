from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'qlb.views.index', name='index'),
    url(r'^tool_config$', 'qlb.views.tool_config', name='tool_config'),
    url(r'^select_qualtrics$', 'qlb.views.select_qualtrics', name='select_qualtrics'),
    url(r'^embed_qualtrics$', 'qlb.views.embed_qualtrics', name='embed_qualtrics'),
    # url(r'^display_qualtrics$', 'qlb.views.display_qualtrics', name='display_qualtrics'),
    url(r'^display_qualtrics/(?P<qualtrics_id>\w+)$', 'qlb.views.display_qualtrics', name='display_qualtrics'),
    url(r'^qualtrics_result$', 'qlb.views.qualtrics_result', name='qualtrics_result'),

)