from models import Mooclet, Version
import random

def uniform_random(versions):
	return random.choice(versions)

def weighted_random(versions, weights):
	pass

def thompson_sampling(versions, results):
	pass

# class ThompsonPolicy(models.Model):
# 	name
# 	priorvariables 
# 	evidencevariables 
	
# 	alpha-successes
# 	beta-failures
# 	probabilityofactions
	
	


# list of lists, each inner list is a different user variable
# [()]

# rows: versions
# columns: variable types
