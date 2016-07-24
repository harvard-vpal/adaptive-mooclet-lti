from numpy.random import choice

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

def thompson_sampling(data):
	pass
