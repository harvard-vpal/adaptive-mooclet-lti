from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse, HttpResponseRedirect
import logging
from engine.models import Quiz
from lti.models import LtiParameters
from utils import display_preview
import json

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
    Additional storage of LTI parameters
    Checks if the LTI user is a student or instructor
        If Student: display the quiz (specified by quiz_id)
        If Instructor: display the management view associated with the quiz
    '''
    quiz = get_object_or_404(Quiz, pk=quiz_id)


    # save student LTI parameters to db
    lti_parameters, created = LtiParameters.objects.get_or_create(
        user=request.user,
        quiz=quiz,
    )
    for parameter_name in lti_parameters.parameter_names:
        setattr(lti_parameters, parameter_name, request.POST.get(parameter_name,''))

    # do this separately bc its named differently
    lti_parameters.lti_user_id = request.POST.get('user_id','')

    # save raw post params
    lti_parameters.data = json.dumps(dict(request.POST))

    lti_parameters.save()

    # determine whether to display in preview mode or quiz mode (does role check)
    if display_preview(request.user, quiz):
        # instructor-like role: launch the quiz management view
        #return redirect('engine:quiz_detail', quiz_id=quiz_id)
        # temporary: make the first question management view the landing page by going to question_detail rather than quiz_detail
        return redirect('engine:question_detail', quiz_id=quiz_id)

    else:
        # student role; launch the quiz
        return redirect('engine:launch', quiz_id=quiz.id)


@login_required()
@require_http_methods(['POST'])
def launch_resource_selection(request):
    '''
    LTI launch from assignment settings
    Used when first creating a new LTI quiz assignment
    '''

    # TODO Safari-proofing
    if 'ext_content_return_types' in request.POST:
        more_lti_params = {
            'ext_content_return_types': request.POST.get('ext_content_return_types', None),
            'ext_content_intended_use': request.POST.get('ext_content_intended_use', None),
            'ext_content_return_url': request.POST.get('ext_content_return_url', None),
        }
        request.session['LTI_LAUNCH'].update(more_lti_params)


    return redirect('engine:quiz_create_options')


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

#########################
#### LTI session end ####
#########################

def exit(request):
    '''
    Redirect back to LMS, using the launch_presentation_url LTI parameter
    '''
    # TODO delete LTI session variables if useful

    return redirect(request.session['LTI_LAUNCH'].get('launch_presentation_return_url'))




