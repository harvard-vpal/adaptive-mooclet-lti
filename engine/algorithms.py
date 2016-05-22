import numpy as np

# Thompson sampling
def computeExplanation_Thompson (student, allExplanations, allExplanationResults):
	# Sample from posterior distribution P(\theta | D) for each explanation
	probabilities = np.zeros(len(allExplanationResults))
	means = np.zeros(len(allExplanationResults))
	for i in range(len(allExplanationResults)):
		#print allExplanationResults
		sumValues = np.sum(allExplanationResults[i])
		a = 1 + sumValues
		b = 1 + len(allExplanationResults[i]) - sumValues
		#print a,b
		means[i] = float(a) / (a + b)
		probabilities[i] = np.random.beta(a, b)
	#print means
	idx = np.argmax(probabilities)
	return allExplanations[idx], means[idx]

