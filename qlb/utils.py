import requests
from django.conf import settings


class QSF:
    def __init__(self,template):
        with open(QSF_TEMPLATE,'rb') as f:
            self.content = json.loads(f.read())
    
    def replace_question_text(self,new_question_text):
        for element in self.content['SurveyElements']:
            if 'Payload' not in element: continue
            if type(element['Payload'])!=type({}): continue
            if element['Payload'].get('DataExportTag')=='Question':
                element['Payload']['QuestionText'] = new_question_text


def create_qualtrics_quiz():
	QSF()
	print response.t

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

