from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from qualtrics.models import Template
# from ordered_model.models import OrderedModel
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import policies

# course / quiz

class Course(models.Model):
    context = models.CharField(max_length=100,default='')
    instance = models.CharField(max_length=200,default='')

class Quiz(models.Model):
    name = models.CharField('quiz name', max_length=100)
    user = models.ForeignKey(User, null=True)
    # url of a custom qualtrics survey
    url = models.URLField(default='',blank=True)
    # context = models.CharField(max_length=100,default='')
    course = models.ForeignKey(Course, blank=True,null=True)

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

# generalized mooclet models

# class MoocletType(models.Model):
#     pass


class Mooclet(models.Model):
    # name = models.CharField(max_length=100,default='')
    policy = models.ForeignKey('Policy',blank=True,null=True)
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey()

    def get_version(self):
        choice = self.policy.run_policy()
        return self.version_set.get(order=choice)


class Version(models.Model):
    '''
    Mooclet version
    '''
    mooclet = models.ForeignKey(Mooclet)
    #
    class Meta:
        order_with_respect_to = 'mooclet'


class Policy(models.Model):
    name = models.CharField(max_length=100)
    user_variable = models.ManyToManyField('UserVariable')

    def get_policy_function():
        try:
            return getattr(policies, self.name)
        except:
            print "policy function matching specified name not found"
            # TODO look through custom user-provided functions
            return None

    def run_policy(versions):
        policy_function = get_policy_function()
        policy_function()


class VariableType(models.Model):
    name = models.CharField(max_length=100)
    is_user_variable = models.BooleanField()
    content_type = models.ForeignKey(ContentType,null=True)

    # variable type "classes"
    description = models.TextField()
    # policy_relevance = [vpal_researcher, harvard_researcher, course_team, external_researcher]
    # policy_relevance2 = [student_judgements, instructor_judgements]


class VariableValue(models.Model):
    '''
    user variable observation, can be associated with either course, mooclet, or mooclet version
    examples of user variables:
        course-level: general student characteristics
        quiz-level: number of attempts
        mooclet: ?
        version: student rating of an explanation, instructors prior judgement
    '''
    user = models.ForeignKey(User)
    variable = models.ForeignKey(UserVariable)
    value = models.FloatField()

    # pick one of the following
    course = models.ForeignKey(Course,null=True)
    quiz = models.ForeignKey(Quiz,null=True)
    mooclet = models.ForeignKey(Mooclet,null=True)
    version = models.ForeignKey(Version,null=True)


### specific mooclet models

class Question(models.Model):
    name = models.CharField('question name', max_length=100)
    quiz = models.ForeignKey(Quiz)
    text = models.TextField('question text')
    # template = models.ForeignKey(Template)
    url = models.URLField(default='',blank=True)
    class Meta:
        order_with_respect_to = 'quiz'
    
    def __unicode__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField('answer text',default='')
    correct = models.BooleanField()
    mooclet = models.ForeignKey(Mooclet,null=True)

    class Meta:
        order_with_respect_to = 'question'

    def __unicode__(self):
        return self.text


class Explanation(Version):
    text = models.TextField('explanation text')

    def __unicode__(self):
        return self.text


class Collaborator(models.Model):
    user = models.ForeignKey(User)
    # like a canvas id or username; something that instructors would be able to provide
    # user_lms_id = models.CharField(max_length=50)
    # context = models.CharField(max_length=100,default='')
    course = models.ForeignKey(Course)
    # quiz = ManyToManyField(Quiz)
    def __unicode__(self):
        return self.user.__unicode__()

class Outcome(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    grade = models.FloatField()