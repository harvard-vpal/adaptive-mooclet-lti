from django.shortcuts import (render, redirect)
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SelectQualtricsForm
import logging
from urllib import urlencode

# using dce_lti_py instad of ims_lti_py for grade passback
from dce_lti_py import OutcomeRequest
#from ims_lti_py import OutcomeRequest

logger = logging.getLogger(__name__)

TOOL_NAME = 'Qualtrics LTI Bridge'


#### QLB views ####

@require_http_methods(['GET'])
def index(request):
    """
    Show the index file
    """
    return render(request, 'qlb/index.html')


@require_http_methods(['GET'])
def tool_config(request):
    """
    This produces a Canvas specific XML config that can be used to
    add this tool to the Canvas LMS
    """
    if request.is_secure():
        host = 'https://' + request.get_host()
    else:
        host = 'http://' + request.get_host()



    lti_tool_config = ToolConfig(
        title=TOOL_NAME,
        launch_url = host,
        secure_launch_url = host,
    )

    # configuration specific for quiz selection mode
    resource_selection_params = {
        'enabled': 'true',
        'selection_width':"700",
        'selection_height':"500",
        'url': host + reverse('qlb:select_qualtrics'),
    }

    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'domain', request.get_host())
    # lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', account_nav_params)
    lti_tool_config.description = 'The Qualtrics LTI Bridge allows instructors to embed qualtrics quizzes in an LMS as an LTI tool.'
    # add resource selection params to the xml
    lti_tool_config.set_ext_param('canvas.instructure.com', 'resource_selection', resource_selection_params)

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp

@login_required()
@require_http_methods(['POST'])
def select_qualtrics(request):
    """
    Presents a form where an instructor can specify the qualtrics quiz to be displayed
    """

    if request.user.is_authenticated():
        

        # this places more LTI launch parameters into the LTI_LAUNCH session dictionary variable 
        # that django-auth-lti doesn't already handle
        more_lti_params = {
            'ext_content_return_types': request.POST.get('ext_content_return_types', None),
            'ext_content_intended_use': request.POST.get('ext_content_intended_use', None),
            'ext_content_return_url': request.POST.get('ext_content_return_url', None),
            'ext_content_file_extensions': request.POST.get('ext_content_file_extensions', None),
        }
        request.session['LTI_LAUNCH'].update(more_lti_params)

        # TODO may store context id and associate it with quiz url

        form = SelectQualtricsForm()

        return render(request, 'qlb/select_qualtrics.html', {'select_qualtrics_form':form})

    else:
        return render(request, 'qlb/error.html', {'message': 'Error: user is not authenticated!'})


# @require_http_methods(['POST'])
def embed_qualtrics(request):
    '''
    Recieves the qualtrics URL specified in the select_qualtrics form
    Returns back a custom launch URL for the LMS context
    '''
    print "called embed_qualtrics view"
    LTI = request.session['LTI_LAUNCH']
    # url to send the qualtrics launch link to
    return_url = LTI['ext_content_return_url']
    qualtrics_url = request.POST['qualtrics_url']

    form = SelectQualtricsForm(request.POST)

    # TODO could check that this is a valid qualtrics url in validation method
    if form.is_valid():
    
        qualtrics_url = form.cleaned_data['qualtrics_url']

        # get qualtrics survey id
        # qualtrics_id = qualtrics_url.partition('/?SID=')[-1]


        #TODO have a mapping between qualtrics id and generated qlb display code - requires db
        # for now, just use the qualtrics id

        qualtrics_id = qualtrics_url.rpartition('/?SID=')[-1]

        # embed the quiz by giving the qlb launch url to the LMS return location
        return HttpResponseRedirect(
            '{return_url}?return_type=lti_launch_url&url={qlb_launch_url}'.format(
                return_url=return_url,
                qlb_launch_url='https://' + request.get_host() + reverse('qlb:display_qualtrics',kwargs={'qualtrics_id':qualtrics_id})
            )
        )


@login_required()
# @require_http_methods(['POST'])
def display_qualtrics(request,qualtrics_id):
    '''
    Launches the qualtrics quiz specified by the passed qualtrics_url parameter
    '''
    LTI = request.session['LTI_LAUNCH']

    # TODO store canvas user id and lti user id so that we can have a mapping

    base_qualtrics_url = 'https://harvard.az1.qualtrics.com/SE/?SID='
    qualtrics_url = '{}{}'.format(base_qualtrics_url,qualtrics_id)


    params = {
        'SID':qualtrics_id,
        'qlb_return_url': request.get_host()
        # TODO define other params to pass to qualtrics survey
    }
    qualtrics_full_url = '{qualtrics_url}?SID={qualtrics_id}&'

    if 'Instructor' in LTI['roles']:

        # TODO instructor view for the qualtrics quiz
        return render(request, 'qlb/instructor_view.html', {'qualtrics_url':qualtrics_url})
        # return HttpResponse('Instructor view for qualtrics quiz {}'.format(qualtrics_url))
    
    else:
        # student view

        # TODO we might determine some adaptivity parameters here (e.g. quiz version) based on user

        # TODO add extra parameters to be passed to the qualtrics survey (lti_user_id, resource_id, adaptivity parameters, etc.)

        return HttpResponseRedirect(qualtrics_url)


    


def qualtrics_result(request):
    '''
    Qualtrics should send data here after survey completion
    Then the relevant outcome data is returned to the LMS
    '''
    # TODO maybe it would be a good idea to have some kind of inbound authentication here

    # TODO get qualtrics data
    # user_id = request.GET['user_id']
    # resource_id = request.GET['resource_id']
    # score = request.GET['grade']

    # TODO store some results in a database?

    # TODO delete this default value if qualtrics is passing back a grade
    score = 1

    # send the outcome data
    OutcomeRequest({
        # required for outcome reporting
        'lis_outcome_service_url':request['lis_outcome_service_url'],
        'consumer_key': request.LTI.get('oauth_consumer_key'),
        'consumer_secret': settings.LTI_OAUTH_CREDENTIALS[request.LTI.get('oauth_consumer_key')],
        # outcomes data
        'score':score,
        # 'result_data':{'text':'This is some outcomes text'}
        }
    ).post_outcome_request()



def manage_quizzes(request):
    '''
    Display available quizzes, with some management functions
    '''
    pass


def create_quiz(request):
    '''
    Redirects to a qualtrics survey for creating a quiz
    '''
    # create quiz object
    pass
    
def create_quiz_from_submission(request):
    '''
    Triggered on a submission to the create quiz survey
    Makes an API call to the quiz
    '''

# from django.contrib.sessions.models import Session
def testview(request):
    pass
    # return HttpResponse(request.session.session_key)

