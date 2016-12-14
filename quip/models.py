from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

#################################
#### Quiz application models ####
#################################


class Mooclet(models.Model):
    engine_id = models.PositiveIntegerField()


class Course(models.Model):
    context = models.CharField(max_length=100,default='')
    instance = models.CharField(max_length=200,default='')
    name = models.CharField(max_length=200,default='')

    def __unicode__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User, null=True)
    # url of a custom qualtrics survey
    url = models.URLField(default='',blank=True)
    # context = models.CharField(max_length=100,default='')
    # TODO consider removing course field
    course = models.ForeignKey(Course, blank=True,null=True)
    # mooclet_next_question = models.ForeignKey(Mooclet,null=True,blank=True)

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

    def get_mooclets(self):
        '''
        Get all associated mooclets for this quiz
        '''
        # explanation mooclets
        explanations = [answer.mooclet_explanation for answer in self.answer_set.all()]
        next_question = self.mooclet_next_question
        mooclets = {
            'explanations': explanations,
            'next_question': next_question,
        }
        return mooclets


class Question(models.Model):
    name = models.CharField('question name', max_length=100)
    quiz = models.ManyToManyField(Quiz)
    text = models.TextField('question text')
    # template = models.ForeignKey(Template)
    url = models.URLField(default='',blank=True)
    
    def __unicode__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField('answer text',default='')
    correct = models.BooleanField()
    mooclet_explanation = models.ForeignKey(Mooclet,blank=True,null=True) # explanation mooclet

    class Meta:
        order_with_respect_to = 'question'

    def __unicode__(self):
        return self.text


class Explanation(models.Model):
    text = models.TextField('explanation text')
    mooclet = models.ForeignKey(Mooclet)

    def __unicode__(self):
        return self.text


class Response(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    grade = models.FloatField()
    timestamp = models.DateTimeField(null=True,auto_now=True)


class Collaborator(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.user.__unicode__()

    class Meta:
        unique_together = ('user', 'course',)



