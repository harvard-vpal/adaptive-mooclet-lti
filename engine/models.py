from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=2000, default='')
    context = models.CharField(max_length=100,default='')
    course = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    text = models.CharField('question text', max_length=500)

    def __unicode__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField('answer choice text', max_length=500)
    correct = models.BooleanField('is correct')
    order = models.PositiveIntegerField('choice order')

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

    def __unicode__(self):
        return "{}, explanation {}".format(self.value, self.explanation.id)

