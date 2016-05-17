from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=200)
    course = models.PositiveIntegerField()

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
    order = models.PositiveIntegerField('choice order')
    correct = models.BooleanField('is correct')

    def __unicode__(self):
        return self.text


class Explanation(models.Model):
    answer = models.ForeignKey(Answer)
    text = models.CharField('explanation text', max_length=500)

    # def get_answer_text(self):
    #   return self.answer.text

    def __unicode__(self):
        return self.text


class Result(models.Model):
    student = models.ForeignKey(User)
    explanation = models.ForeignKey(Explanation)
    value = models.FloatField()

    # def get_explanation_text(self):
    #   return self.explanation.text

    def __unicode__(self):
        return "{}, explanation {}".format(value, self.explanation.id)
