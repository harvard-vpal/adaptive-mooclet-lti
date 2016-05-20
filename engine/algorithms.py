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

def get_explanation_for_student(answer_id=None, student_id=None,):
    allExplanations = []
    allResultsForExplanations = []
    for explanation in Explanation.objects.filter(answer=answer).iterator():
        someResults = []
        for result in Result.objects.filter(explanation=explanation).iterator():
            someResults.append(result.value)
        allResultsForExplanations.append(someResults)
        allExplanations.append(explanation)
    selectedExplanation, exp_value = computeExplanation_Thompson(student_id, allExplanations, allResultsForExplanations)

