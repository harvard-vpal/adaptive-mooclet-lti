from numpy.random import choice, beta
from django.core.urlresolvers import reverse
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

# arguments to policies:

# variables: list of variable objects, can be used to retrieve related data
# context: dict passed from view, contains current user, course, quiz, question context
# iterations: a number of iterations of policy to run (for simulations) 
# return a dict ov versions mapped to of probabilities

def uniform_random(variables,context,iterations=100):
	probabilities = {version: 1.0 / len(context['versions']) for version in context['versions']}
	return probabilities


def weighted_random(variables,context,iterations=100):
	Weight = variables.get(name='version_weight')
	weight_data = Weight.get_data(context)

	probabilities = {weight.version: weight.value for weight in weight_data}
	return probabilities


def thompson_sampling(variables,context,iterations=100):
	versions = context['versions']
	#import models individually to avoid circular dependency
	Variable = apps.get_model('engine', 'Variable')
	Value = apps.get_model('engine', 'Value')
	Version = apps.get_model('engine', 'Version')
	version_content_type = ContentType.objects.get_for_model(Version)
	#priors we set by hand - will use instructor rating and confidence in future
	prior_success = 1.9
	prior_failure = 0.1
	#max value of version rating, from qualtrics
	max_rating = 1
	
	student_ratings_data = Variable.objects.get(name='student_rating').get_data(context)

	# set up aggregate data we only need once
	versions_data = {}
	for version in versions:
		student_ratings = student_ratings_data.filter(object_id=version.pk)
		versions_data[version] = {}
		version_data = versions_data[version]
		version_data['count'] = student_ratings.count()

		rating_average = student_ratings.aggregate(Avg('value'))
		rating_average = rating_average['value__avg']
		if rating_average is None:
			rating_average = 0
		else:
			rating_average = rating_average * 0.1
		 
		version_data['avg'] = rating_average



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
	


	version_counts = {version: 0 for version in context['versions']}

	#beta sample versions
	for i in range(1, iterations):
		version_to_show = None
		max_beta = 0
	
		for version in versions:
			version_data = versions_data[version]
			rating_count = version_data['count']
			rating_average = version_data['avg']
			

			
			#TODO - log to db later?
			successes = (rating_average * rating_count) + prior_success
			failures = (max_rating * rating_count) - (rating_average * rating_count) + prior_failure

			version_beta = beta(successes, failures)

			if version_beta > max_beta:
				max_beta = version_beta
				version_to_show = version

		version_counts[version_to_show] = version_counts[version_to_show] + 1

	probabilities = {version: float(version_counts[version]) / sum(version_counts.values()) for version in versions}
	#probabilities = [float(version_counts[version]) / sum(version_counts.values()) for version in versions]
	return probabilities