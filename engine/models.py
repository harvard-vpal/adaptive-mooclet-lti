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
    url = models.CharField(max_length=500, default='')
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
        pass

    def getDisplayUrl(self):
        '''
        gets the appropriate url to display the quiz
        based on whether questions exist and whether custom urls are present
        ''' 
        if self.url:
            return redirect(self.url)
        elif self.question_set.all().exists():
            first_question = self.question_set.first()
            if first_question.url:
                return redirect(first_question.url)
            else:
                return reverse('quiz:question',kwargs={'question_id':self.id})
        else:
            return reverse('quiz:placeholder')


class Question(OrderedModel):
    quiz = models.ForeignKey(Quiz)
    text = models.CharField('question text', max_length=500)
    # template = models.ForeignKey(Template)
    url = models.CharField(max_length=500, default='')
    # settings for django-ordered-model
    order_with_respect_to = 'quiz'
    
    def __unicode__(self):
        return self.text


class Answer(OrderedModel):
    question = models.ForeignKey(Question)
    text = models.CharField('answer choice text', max_length=500)
    correct = models.BooleanField('is correct')
    # order = models.PositiveIntegerField('choice order')

    # settings for django-ordered-model
    order_with_respect_to = 'question'

    def __unicode__(self):
        return self.text


class Explanation(models.Model):
    answer = models.ForeignKey(Answer)
    text = models.CharField('explanation text', max_length=500)

    def __unicode__(self):
        return "{}: {}".format(self.id,self.text)


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
    description = models.CharField(max_length=200,default='')

class CourseUserState(models.Model):
    courseuser = models.ForeignKey(CourseUser)
    variable = models.ForeignKey(CourseUserVariable)
    




