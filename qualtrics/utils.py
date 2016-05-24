import requests
from django.conf import settings
from os import path
import json

class QSF:
    '''
    class for initializing qsf from template and modifying it
    # TODO would like to initialize from a QSF at some URL
    '''
    def __init__(self, qsf_path=None, qsf_version=None):
        if not qsf_path:
            # QSF template location, assumes it is in static/qualtrics
            qsf_path = path.join(settings.STATIC_ROOT, 'qualtrics/'+settings.QUALTRICS_TEMPLATE_NAME)
        with open(qsf_path,'rb') as f:
            self.content = json.loads(f.read())


    def insert_question_id(self,question_id,to_replace=None):
        '''
        insert the question id into the qsf template
        looks for to_replace in any of the embedded data fields
        defaults to looking for 'INSERT_QUESTIONID'
        '''
        if not to_replace: 
            to_replace = 'INSERT_QUESTIONID'
        replace_with = question_id

        for element in self.content['SurveyElements']:
            if element['Element']=='FL':
                for flow_element in element['Payload']['Flow']:
                    if 'EmbeddedData' in flow_element:
                        for embedded_variable in flow_element['EmbeddedData']:
                            # if the embedded variable value matches the keyword
                            if embedded_variable.get('Value') == to_replace:
                                # replace with the new value
                                embedded_variable['Value'] = replace_with


def get_modified_qsf(question, template_version=None):
    '''
    given a django question object, modify the template qsf file to match the information
    '''
    answers = question.answer_set.order_by('order')

    qsf = QSF()
    qsf.insert_question_id(question.id)
    # TODO other operations on QSF 

    return json.dumps(qsf.content)


def upload_qsf_to_qualtrics(qsf_url, survey_name ):
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
