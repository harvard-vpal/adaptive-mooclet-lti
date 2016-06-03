import requests
from django.conf import settings
from os import path
import json
from .models import Template

class QSF:
    '''
    Loads a QSF file from either a URL or from our QSF database
    '''
    def __init__(self, template=None, url=None):
        if template and url:
            raise Exception('Too many arguments')

        # Option 1: Initialize QSF from a given URL
        elif url:
            try:
                self.content = requests.get(url).json()
            except:
                raise Exception('Error retrieving QSF from URL')

        # Option 2: Initialize QSF from one of our templates
        else:
            if template:
                # QSF template location, assumes it is in static/qualtrics
                template_path = path.join(settings.STATIC_ROOT, 'qualtrics/'+template.filename)
            # Default case: use the first template
            else:
                template = Template.objects.get(pk=1)

            # load template into QSF object content
            with open(template_path,'rb') as f:
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


def get_modified_qsf(question, template=None):
    '''
    given a django question object, modify the template qsf file to match the information
    '''
    template = Template.objects.get(pk=1)
    qsf = QSF(template)
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

    response = requests.post(api_url, headers=headers, files=data)
    print response.text
    print response.request.url
    print response.request.body
    if not response.status_code == 200:
        raise Exception('Something went wrong with qualtrics survey creation: {}'.format(response.text))

    else:
        qualtrics_id = response.json()['result']['id']
        qualtrics_url = "{}/SE/?SID={}".format(settings.QUALTRICS_BASE_URL,qualtrics_id)
        
        if not qualtrics_url:
            raise Exception('Something went wrong with qualtrics survey creation')

        return qualtrics_url
