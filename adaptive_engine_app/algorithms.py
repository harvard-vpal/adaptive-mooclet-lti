import numpy as np

# Thompson sampling
def computeVersionOfComponent_Thompson (student, allVersions, allVersionResults):
	# Sample from posterior distribution P(\theta | D) for each version
	probabilities = np.zeros(len(allVersionResults))
	for i in range(len(allVersionResults)):
		a = 1 + np.sum(allVersionResults[i])
		b = 1 + len(allVersionResults[i]) - a
		probabilities[i] = np.random.beta(a, b)
	idx = np.argmax(probabilities)
	return allVersions[idx]
