import requests

BASEURL = 'https://harvard.az1.qualtrics.com/API/v3/'
TOKEN = 'O26ev6Ml1djly7gE07XpdPnJntQ7LSk3gDcclL6E'


'''
Qualtrics API call to create quiz from qsf hosted at URL
'''
requests.post(
    BASEURL+'surveys',
    headers={
        'X-API-TOKEN':TOKEN,
#         'Content-Type':'multipart/form-data'
    },
    data={
        'name':'my new survey',
        'contentType': 'application/vnd.qualtrics.survey.qsf',
        'fileUrl': 'https://dl.dropboxusercontent.com/u/8138074/LTI_quiz_1.qsf'
#         'file':'LTI_quiz_1.qsf',
#         'owner_id': 'UR_8x2TCd1b3H7eSfb'
    },
    files={
#         'name': 'imported survey name',
        'file': None
        (
#             'myname',
            open('LTI_quiz_1.qsf','rb'),
            'application/vnd.qualtrics.survey.qsf',
#             {'Expires':0}
        )
    }
).json()


'''
Qualtrics API call to create quiz from provided file
'''
requests.post(
    BASEURL+'surveys',
    headers={
        'X-API-TOKEN':TOKEN,
#         'Content-Type':'multipart/form-data'
    },
    data={
        'name':'my new survey',
    },
    files={
        'file': (            
        	open('LTI_quiz_1.qsf','rb'),
            'application/vnd.qualtrics.survey.qsf',
        )
    }
).json()