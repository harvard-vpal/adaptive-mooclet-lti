def create_qualtrics_quiz():
	pass

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
