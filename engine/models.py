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
# from django.db.models import Q

####################################
#### Generalized mooclet models ####
####################################

# TODO: is this useful to have? leaving in for now
class MoocletType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Mooclet(models.Model):
    name = models.CharField(max_length=100,default='')
    policy = models.ForeignKey('Policy',blank=True,null=True)

    def __unicode__(self):
        return "Mooclet: {}".format(self.id)

    def get_version_ids(self):
        return self.version_set.values_list('id',flat=True)
        # return [version_id for version in self.version_set.all()]

    def get_version(self, context={}):
        context['versions'] = self.version_set.all()
        # context['version_ids'] = self.get_version_ids()
        version = self.policy.run_policy(context)
        # version = self.version_set.get(pk=version_id)
        return version


class Version(models.Model):
    '''
    Mooclet version
    '''
    mooclet = models.ForeignKey(Mooclet)
    #
    class Meta:
        order_with_respect_to = 'mooclet'

    def __unicode__(self):
        try:
            return getattr(self, 'explanation').__unicode__()
        except:
            return "Version: {}".format(self.name)


class Policy(models.Model):
    # TODO should name be the primary key?
    name = models.CharField(max_length=100)
    variables = models.ManyToManyField('Variable')

    class Meta:
        verbose_name_plural = 'policies'

    def __unicode__(self):
        return self.name

    def get_policy_function(self):
        try:
            return getattr(policies, self.name)
        except:
            print "policy function matching specified name not found"
            # TODO look through custom user-provided functions
            return None

    def get_variables(self):
        # TODO implement returning all, subsets, etc.
        return self.variables.all()

    def run_policy(self, context):
        # insert all version ids here?
        policy_function = self.get_policy_function()
        variables = self.get_variables()
        version_id = policy_function(variables,context)
        return version_id


class Variable(models.Model):
    name = models.CharField(max_length=100)
    is_user_variable = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType,null=True) # Lets you reference a table.  e.g. if content_type = Version, it's associated with a Version. Can have multiple values associated with it.
    description = models.TextField(default='')
    # TODO variable type "classes"
    # policy_relevance = [vpal_researcher, harvard_researcher, course_team, external_researcher]
    # policy_relevance2 = [student_judgements, instructor_judgements]

    def __unicode__(self):
        return self.name

    def get_data(self,context=None):
        '''
        return relevant value objects for the variable type
        '''
        # context is a dictionary that contains model objects user, course, quiz, mooclet, version
        if context:
            ct_name = self.content_type.__unicode__() # str: 'course','user','mooclet', or 'version'

            query = {}
            # if user variable and user info in context, filter by user
            if 'user' in context and self.is_user_variable:
                query['user'] = context['user']

            # if context is at the mooclet-level but variable is version-related, pass related version ids to the query
            if 'versions' in context and ct_name=='version':
                query['object_id__in'] = context['mooclet'].version_set.values_list('id',flat=True)
            else:
                query['object_id'] = context[ct_name].id # pk of related content object instance
            return self.value_set.filter(**query)
        else:
            return self.value_set.all()

    def get_data_dicts(self,context=None):
        '''
        return relevant values for the variable type, as a list of dicts
        '''
        return self.get_data(context).values()


class Value(models.Model):
    '''
    user variable observation, can be associated with either course, mooclet, or mooclet version
    examples of user variables:
        course-level: general student characteristics
        quiz-level: number of attempts
        mooclet: ?
        version: student rating of an explanation, instructors prior judgement
    '''
    user = models.ForeignKey(User,null=True,blank=True)
    variable = models.ForeignKey(Variable)
    object_id = models.PositiveIntegerField(null=True) # This can just be the integer primary key of the table specified in Variable as content_type
    value = models.FloatField()
    timestamp = models.DateTimeField(null=True,auto_now=True)

    def get_object_content(self,content_object_name):
        '''
        retrieve the related content object associated with the Value
        takes as input the name of the content object
        '''
        ct = self.variable.content_type
        if ct.__unicode__() != content_object_name:
            return None
        return ct.get_object_for_this_type(pk=self.object_id)

    # enables use of "value.course", etc. syntax
    @property
    def course(self):
        return self.get_object_content('course')

    @property
    def quiz(self):
        return self.get_object_content('quiz')

    @property
    def mooclet(self):
        return self.get_object_content('mooclet')

    @property
    def version(self):
        return self.get_object_content('version')


#################################
#### Quiz application models ####
#################################

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

    def get_mooclets(self):
        '''
        Get all associated mooclets for this quiz
        '''
        # explanation mooclets
        return [answer.mooclet for answer in self.answer_set.all()]


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
    mooclet = models.ForeignKey(Mooclet,null=True) # explanation mooclet

    class Meta:
        order_with_respect_to = 'question'

    def __unicode__(self):
        return self.text


class Collaborator(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.user.__unicode__()

    class Meta:
        unique_together = ('user', 'course',)


# TODO does it make sense to move this to lti app models?
class QuizLtiParameters(models.Model):
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
    #TODO canvas id

    class Meta:
        unique_together = ('user','quiz')
        verbose_name = 'LTI Parameters'
        verbose_name_plural = 'LTI Parameters'


########################################
#### Specific mooclet version types ####
########################################

class Explanation(Version):
    text = models.TextField('explanation text')

    def __unicode__(self):
        return self.text



# TODO replace with generic variable
# class Outcome(models.Model):
#     user = models.ForeignKey(User)
#     quiz = models.ForeignKey(Quiz)
#     grade = models.FloatField()

## TODO use for policies that need persistent storage (e.g. priors)
# class VersionPolicyState(models.Model):
#     version = models.ForeignKey(Version)
#     policy = models.ForeignKey(Policy)
#     state = models.FloatField()

