import numpy as np

# Thompson sampling
def computeVersionOfComponent_Thompson (student, allVersions, allVersionResults):
	# Sample from posterior distribution P(\theta | D) for each version
	probabilities = np.zeros(len(allVersionResults))
	means = np.zeros(len(allVersionResults))
	for i in range(len(allVersionResults)):
		sumValues = np.sum(allVersionResults[i])
		a = 1 + sumValues
		b = 1 + len(allVersionResults[i]) - sumValues
		means[i] = float(a) / (a + b)
		probabilities[i] = np.random.beta(a, b)
	idx = np.argmax(probabilities)
	return allVersions[idx], means[idx]
