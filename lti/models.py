from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from engine.models import Quiz


class LtiParameters(models.Model):
    '''
    Used to store outcome service url for a particular user and quiz
    Enables asynchronous or API-triggered grade passback
    '''
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)

    lis_outcome_service_url = models.CharField(max_length=200,default='')
    lis_result_sourcedid = models.CharField(max_length=100,default='')
    oauth_consumer_key = models.CharField(max_length=100,default='')
    lti_user_id = models.CharField(max_length=100,default='') # lti user id
    lis_person_sourcedid = models.CharField(max_length=100,default='') #huid
    canvas_user_id = models.CharField(max_length=50,default='')
    canvas_course_id = models.CharField(max_length=50,default='')
    data = models.TextField(default='')


    class Meta:
        unique_together = ('user','quiz')
        verbose_name = 'LTI Parameters'
        verbose_name_plural = 'LTI Parameters'