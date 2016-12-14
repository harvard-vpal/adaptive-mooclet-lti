from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import policies
from django.http import Http404


class Mooclet(models.Model):
    name = models.CharField(max_length=100,default='')
    policy = models.ForeignKey('Policy',blank=True,null=True)

    def __unicode__(self):
        return "Mooclet {}: {}".format(self.pk, self.name)

    def run(self, policy=None, context={}):
        context['mooclet'] = self
        if not self.version_set.exists():
            raise Http404('mooclet has no versions')
        if not policy:
            if self.policy:
                policy = self.policy
            else:
                # print 'no policy found'
                raise Http404('no policy found')

        version = policy.run_policy(context)

        return version


class Version(models.Model):
    '''
    Mooclet version
    '''
    name = models.CharField(max_length=200,default='')
    mooclet = models.ForeignKey(Mooclet, null=True)

    def __unicode__(self):
        return "Version {}: {}".format(self.pk, self.name)


# class MoocletPolicyState(models.Model):
# 	pass


class Variable(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200, blank=True, default='')
    description = models.CharField(max_length=500, blank=True, default='')

    def __unicode__(self):
        return self.name

    def get_data(self,context=None):
        '''
        return relevant value objects for the variable type
        '''
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
    variable = models.ForeignKey(Variable)

    user = models.PositiveIntegerField(null=True,blank=True)
    mooclet = models.ForeignKey(Mooclet,null=True,blank=True)
    version = models.ForeignKey(Version,null=True,blank=True)
    policy = models.ForeignKey('Policy',null=True,blank=True)

    value = models.FloatField(blank=True,null=True)
    text = models.TextField(blank=True,default='')
    timestamp = models.DateTimeField(null=True,auto_now=True)



class Policy(models.Model):
    name = models.CharField(max_length=100)
    # variables = models.ManyToManyField('Variable') # might use this for persistent "state variables"?

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
        # return self.variables.all()
        return Variable.objects.all()

    def run_policy(self, context):
        # insert all version ids here?
        policy_function = self.get_policy_function()
        variables = self.get_variables()
        version_id = policy_function(variables,context)
        return version_id



