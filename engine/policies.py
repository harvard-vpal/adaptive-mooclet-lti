from numpy.random import choice, beta
from django.core.urlresolvers import reverse
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

# arguments to policies:

# variables: list of variable objects, can be used to retrieve related data
# context: dict passed from view, contains current user, course, quiz, question context


def uniform_random(variables,context):
	return choice(context['mooclet'].version_set.all())

def weighted_random(variables,context):
	Weight = variables.get(name='version_weight')
	weight_data = Weight.get_data(context)

	versions = [weight.version for weight in weight_data]
	weights = [weight.value for weight in weight_data]
	return choice(versions, p=weights)

def thompson_sampling_placeholder(variables,context):
	return choice(context['mooclet'].version_set.all())

def thompson_sampling(variables,context):
	versions = context['versions']
	#import models individually to avoid circular dependency
	Variable = apps.get_model('engine', 'Variable')
	Value = apps.get_model('engine', 'Value')
	Version = apps.get_model('engine', 'Version')
	version_content_type = ContentType.objects.get_for_model(Version)
	#priors we set by hand - will use instructor rating and confidence in future
	prior_success = 19
	prior_failure = 1
	#max value of version rating, from qualtrics
	max_rating = 10

	version_to_show = None
	max_beta = 0

	for version in versions:
		student_ratings = Variable.objects.get(name='student_rating').get_data({'version': version}).all()
		rating_count = student_ratings.count()
		rating_average = student_ratings.aggregate(Avg('value'))
		rating_average = rating_average['value__avg']
		if rating_average is None:
			rating_average = 0


		#get instructor conf and use for priors later
		#add priors to db
		prior_success_db, created = Variable.objects.get_or_create(name='thompson_prior_success', content_type=version_content_type)
		prior_success_db_value = Value.objects.filter(variable=prior_success_db, object_id=version.id).last()
		if prior_success_db_value:
			#there is already a value, so update it
			prior_success_db_value.value = prior_success
			prior_success_db_value.save()
		else:
			#no db value
			prior_success_db_value = Value.objects.create(variable=prior_success_db, object_id=version.id, value=prior_success)

		prior_failure_db, created = Variable.objects.get_or_create(name='thompson_prior_failure', content_type=version_content_type)
		prior_failure_db_value = Value.objects.filter(variable=prior_failure_db, object_id=version.id).last()
		if prior_failure_db_value:
			#there is already a value, so update it
			prior_failure_db_value.value = prior_failure
			prior_failure_db_value.save()
		else:
			#no db value
			prior_failure_db_value = Value.objects.create(variable=prior_failure_db, object_id=version.id, value=prior_failure)
	

		#TODO - log to db later?
		successes = (rating_average * rating_count) + prior_success
		failures = (max_rating * rating_count) - (rating_average * rating_count) + prior_failure

		version_beta = beta(successes, failures)

		if version_beta > max_beta:
			max_beta = version_beta
			version_to_show = version

	return version_to_show



