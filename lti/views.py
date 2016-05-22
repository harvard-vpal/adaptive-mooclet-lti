from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse, HttpResponseRedirect
import logging
from engine.models import Quiz

# using dce_lti_py instad of ims_lti_py for grade passback
from dce_lti_py import OutcomeRequest
# from ims_lti_py import OutcomeRequest

logger = logging.getLogger(__name__)



#####################################
#### GENERATE TOOL CONFIGURATION ####
#####################################

def tool_config(request):
    '''
    Generates an XML config that can be used to add this tool to the Canvas LMS
    '''
    TOOL_NAME = 'Adaptive Quiz LTI'
    host = 'https://' + request.get_host()

    lti_tool_config = ToolConfig(
        title=TOOL_NAME,
        launch_url = host,
        secure_launch_url = host,
    )

    # # configuration for nav bar
    # course_nav_params = {
    #     'enabled': 'true',
    #     'selection_width':"700",
    #     'selection_height':"500",
    #     'url': host + reverse('lti:manage_quizzes'),
    # }
    # lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', course_nav_params)

    # configuration for quiz selection mode
    resource_selection_params = {
        'enabled': 'true',
        'selection_width':"700",
        'selection_height':"500",
        'url': request.build_absolute_uri(reverse('lti:launch_resource_selection')),
    }
    # add resource selection params to the xml
    lti_tool_config.set_ext_param('canvas.instructure.com', 'resource_selection', resource_selection_params)

    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'domain', request.get_host().partition(':')[0])
    lti_tool_config.description = 'The Qualtrics LTI Bridge allows instructors to embed qualtrics quizzes in an LMS as an LTI tool.'
    
    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)


##########################
#### LTI launch modes ####
##########################

@login_required()
@require_http_methods(['POST'])
def launch(request,quiz_id):
    '''
    Standard LTI launch
    Checks if the LTI user is a student or instructor
    If Student: display the quiz (specified by quiz_id)
    If Instructor: display the management view associated with the quiz
    '''

    # put more LTI params in the LTI launch session variable - needed when authenticating sent results back to canvas
    more_lti_params = {
        'lis_outcome_service_url': request.POST.get('lis_outcome_service_url', None),
        'lis_result_sourcedid': request.POST.get('lis_result_sourcedid', None),
        'oauth_consumer_key': request.POST.get('oauth_consumer_key', None),
    }
    request.session['LTI_LAUNCH'].update(more_lti_params)

    if 'Instructor' in request.session['LTI_LAUNCH']['roles']:
        return redirect('engine:manage_quiz',quiz_id=quiz_id)

    # TODO researcher role check

    else:
        # TODO store canvas user id and lti user id so that we can have a mapping

        quiz = Quiz.objects.get(pk=quiz_id)

        # Check if the quiz has a qualtrics url. If not, then we can host the quiz ourself
        if quiz.url:
            quiz_url = quiz.url
        else:
            quiz_url = reverse('quiz:display_quiz_question',kwargs={'quiz_id':quiz.id})

        return redirect(quiz_url)


@login_required()
@require_http_methods(['POST'])
def launch_resource_selection(request):
    '''
    LTI launch from nav bar
    Display all quizzes, with some management functions
    Accessible via left navigation bar in canvas
    '''
    if 'ext_content_return_types' in request.POST:
        more_lti_params = {
            'ext_content_return_types': request.POST.get('ext_content_return_types', None),
            'ext_content_intended_use': request.POST.get('ext_content_intended_use', None),
            'ext_content_return_url': request.POST.get('ext_content_return_url', None),
        }
        request.session['LTI_LAUNCH'].update(more_lti_params)

    return redirect('engine:select_or_create_quiz')


@login_required()
@require_http_methods(['POST'])
def launch_course_navigation(request):
    '''
    LTI launch from nav bar
    Display all quizzes, with some management functions
    Accessible via left navigation bar in canvas
    '''
    # TODO to be implemented 
    pass


########################################################
#### returning data back to the tool consumer / LMS ####
########################################################

def return_launch_url(request, quiz_id):
    '''
    Embeds a specific qualtrics quiz by passing the quiz launch URL to the resource selection return URL
    '''
    if 'ext_content_return_types' not in request.session['LTI_LAUNCH']:
        raise Exception('Return URL not found in LTI params')

    # embed the quiz by giving the qlb launch url to the LMS return location
    return_url = request.session['LTI_LAUNCH']['ext_content_return_url']

    return HttpResponseRedirect(
        "{return_url}?return_type=lti_launch_url&url={launch_url}".format(
            return_url=return_url,
            launch_url= request.build_absolute_uri(reverse('lti:launch',kwargs={'quiz_id':quiz_id}))
        )
    )


def return_outcome(request):
    '''
    Return grade / outcome data back to the LMS via LTI Outcome Service protocol
    '''
    # TODO replace this default value if we have an actual grade
    score = 1.0

    # send the outcome data
    outcome = OutcomeRequest(
        {
            # required for outcome reporting
            'lis_outcome_service_url':request.session['LTI_LAUNCH'].get('lis_outcome_service_url'),
            'lis_result_sourcedid':request.session['LTI_LAUNCH'].get('lis_result_sourcedid'),
            'consumer_key': request.session['LTI_LAUNCH'].get('oauth_consumer_key'),
            'consumer_secret': settings.LTI_OAUTH_CREDENTIALS[request.session['LTI_LAUNCH'].get('oauth_consumer_key')],
            'message_identifier': 'myMessage'
        }
    )
    
    # print 'outcome service url: {}'.format(outcome.lis_outcome_service_url)
    # print 'result source id: {}'.format(outcome.lis_result_sourcedid)
    # print 'operation: {}'.format(outcome.operation)
    outcome_response = outcome.post_replace_result(
        score,
        # result_data={
        # #     # 'url':'placeholder'
        #     'text':'complete'
        # }
    )

    # print 'OUTCOME REQUEST VARIABLES'
    # print 'consumer key: {}'.format(outcome.consumer_key)
    # print 'consumer secret: {}'.format(outcome.consumer_secret)
    # print 'result sourcedid: {}'.format(outcome.lis_result_sourcedid)

    # print 'outcome response successful? {}'.format(outcome_response.is_success())
    # print 'outcome response status code: {}'.format(outcome_response.response_code)
    
    # print 'outcome response content: {}'.format(outcome_response.post_response)

    # print 'outcome response code major: {}'.format(outcome_response.code_major)
    # print 'outcome response description: {}'.format(outcome_response.description)
    # print 'outcome response message ref {}'.format(outcome_response.message_ref_identifier)

    # print 'outcome response headers: {}'.format(outcome_response.post_response.headers)

    # print 'outcome response code major: {}'.format(outcome_response.code_major)
    # print 'outcome request body: {}'.format(outcome_response.post_response.request.body)
    # print 'outcome request url: {}'.format(outcome_response.post_response.request.url)
    # print 'outcome request headers: {}'.format(outcome_response.post_response.request.headers)
    # 
    # print 'outcome response content: {}'.format(outcome_response.post_response.text)

    # print 'outcome response description: {}'.format(outcome_response.post_response.imsx_description)
    # print 'outcome response message ref id: {}'.format(outcome_response.post_response.message_ref_identifier)

    # return HttpResponse(outcome_response.post_response.content)
    return redirect(request.session['LTI_LAUNCH'].get('launch_presentation_return_url'))


    




