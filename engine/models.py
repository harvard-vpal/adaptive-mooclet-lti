from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from qualtrics.models import Template
from ordered_model.models import OrderedModel
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your models here.

class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User)
    # url of a custom qualtrics survey
    url = models.URLField(default='',blank=True)
    context = models.CharField(max_length=100,default='')

    class Meta:
        verbose_name_plural = 'quizzes'

    def __unicode__(self):
        return self.name

    def isValid(self):
        '''
        Check whether the quiz is student-ready:
        Checks whether quiz has questions, questions have answers, and answers have explanations
        '''
        if self.question_set.all().exists():
            return True
        # TODO: check answers of questions, explanations of answers

    def getExternalUrl(self):
        '''
        gets the external url to display the quiz, return None if not available
        '''
        if self.url:
            return self.url
        elif self.question_set.all().exists():
            first_question = self.question_set.first()
            if first_question.url:
                return first_question.url
        return None


class Question(OrderedModel):
    quiz = models.ForeignKey(Quiz)
    text = models.TextField('question text')
    # template = models.ForeignKey(Template)
    url = models.URLField(default='',blank=True)
    # settings for django-ordered-model
    order_with_respect_to = 'quiz'
    
    def __unicode__(self):
        return self.text


class Answer(OrderedModel):
    question = models.ForeignKey(Question)
    text = models.TextField('answer choice text', max_length=500)
    correct = models.BooleanField()
    # order = models.PositiveIntegerField('choice order')

    # settings for django-ordered-model
    order_with_respect_to = 'question'

    def __unicode__(self):
        return self.text


class Explanation(models.Model):
    answer = models.ForeignKey(Answer)
    text = models.TextField('explanation text')
    # policy = models.ForeignKey(Policy)

    def __unicode__(self):
        return "{}: {}".format(self.id,self.text)

# class Policy(models.Model):
#    pass


class Result(models.Model):
    user = models.ForeignKey(User)
    explanation = models.ForeignKey(Explanation)
    value = models.FloatField()
    # store lis_result_sourcedid, lis_outcome_service_url

    def __unicode__(self):
        return "{}, explanation {}".format(self.value, self.explanation.id)


# class Role(models.Model):
#     name = models.CharField(max_length=50,default='')
#     description = models.CharField(max_length=200,default='')

class Researcher(models.Model):
    user = models.ForeignKey(User)
    # like a canvas id or username; something that instructors would be able to provide
    user_lms_id = models.CharField(max_length=50)
    context = models.CharField(max_length=100,default='')

class CourseUser(models.Model):
    user = models.ForeignKey(User)
    context = models.CharField(max_length=100,default='')
    # is_researcher = models.BooleanField()
    # role = models.ForeignKey(Role)

class CourseUserVariable(models.Model):
    name = models.CharField(max_length=50,default='')
    description = models.TextField(default='')

class CourseUserState(models.Model):
    courseuser = models.ForeignKey(CourseUser)
    variable = models.ForeignKey(CourseUserVariable)
    




