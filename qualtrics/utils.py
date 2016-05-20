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


def modify_qsf_template(quiz):
	'''
	given a django quiz object, modify the template qsf file to match the information
	'''
	question = quiz.question_set.first()
	answers = question.answer_set.order_by('order')

	qsf = QSF(QSF_TEMPLATE)
	qsf.replace_question_text(question.text)

	return json.dumps(qsf.content)


def upload_qsf_to_qualtrics(qsf_url, survey_name, ):
	'''
	uploads the qsf file hosted at qsf_url to qualtrics, using qualtrics API v3
	return the qualtrics id of the newly created survey
	'''
	api_url = "https://harvard.az1.qualtrics.com/API/v3/surveys"
	# qsf_url = 'https://dl.dropboxusercontent.com/u/8138074/LTI_quiz_1.qsf'
	headers = {
	    'x-api-token': settings.QUALTRICS_API_TOKEN
	}
	data = {
	    'contentType': (None, 'application/vnd.qualtrics.survey.qsf'),
	    'name': (None, survey_name),
	    'fileUrl': (None, qsf_url),
	}
	response = requests.post(url, headers=headers, files=data)

	if not response.status_code == 200:
		return None

	else:
		qualtrics_id = response.json()['result']['id']
		qualtrics_url = "{}/SE/?SID={}".format(settings.QUALTRICS_BASE_URL,qualtrics_id)
		
		return qualtrics_url