from django.shortcuts import (render, redirect)
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse, HttpResponseRedirect
import logging
from urllib import urlencode
from django.forms import formset_factory
import requests
import utils

# using dce_lti_py instad of ims_lti_py for grade passback
from dce_lti_py import OutcomeRequest
#from ims_lti_py import OutcomeRequest

from django.views.generic.edit import CreateView
from .models import Quiz, Question, Answer, Explanation, Result
from django.forms import inlineformset_factory, ModelForm
from .forms import *

from engine.algorithms import computeExplanation_Thompson 


logger = logging.getLogger(__name__)

TOOL_NAME = 'Qualtrics LTI Bridge'


#### QLB views ####

def index(request):
    '''
    Show some placeholder page
    '''
    return render(request, 'lti/index.html')


def tool_config(request):
    '''
    This produces a Canvas specific XML config that can be used to
    add this tool to the Canvas LMS
    '''
    if request.is_secure():
        host = 'https://' + request.get_host()
    else:
        host = 'http://' + request.get_host()

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
        'url': host + reverse('lti:select_or_create_quiz'),
    }

    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'domain', request.get_host().partition(':')[0])
    lti_tool_config.description = 'The Qualtrics LTI Bridge allows instructors to embed qualtrics quizzes in an LMS as an LTI tool.'
    # add resource selection params to the xml
    lti_tool_config.set_ext_param('canvas.instructure.com', 'resource_selection', resource_selection_params)

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp


@login_required()
def launch_quiz_list(request):
    '''
    Display all quizzes, with some management functions
    Accessible via left navigation bar in canvas
    '''
    pass


@login_required()
def select_or_create_quiz(request):
    '''
    Accessed via select resource mode when editing assignment
    Select a quiz that has already been made, or create a new one
    '''
    
    if 'form_submit' not in request.GET:
        more_lti_params = {
            'ext_content_return_types': request.POST.get('ext_content_return_types', None),
            'ext_content_intended_use': request.POST.get('ext_content_intended_use', None),
            'ext_content_return_url': request.POST.get('ext_content_return_url', None),
        }
        request.session['LTI_LAUNCH'].update(more_lti_params)

        select_quiz_form = SelectQuizForm()
        context = {'select_quiz_form':select_quiz_form}
        return render(request, 'lti/select_or_create_quiz.html',context)
        # return HttpResponseRedirect(url_createQuizSurvey)

    elif 'form_submit' in request.GET:
        select_quiz_form = SelectQuizForm(request.POST)
        if select_quiz_form.is_valid():
            quiz = select_quiz_form.cleaned_data['quiz']

            # embed quiz
            return HttpResponseRedirect(reverse('lti:embed_quiz',kwargs={'quiz_id':quiz.pk}))



def create_quiz(request):
    '''
    displays some html form to collect question, answers and explanations
    '''
    NUM_CHOICES = 4
    NUM_EXPLANATIONS = 2
    AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','order','correct'), can_delete=False, extra=4)
    ExplanationFormset = inlineformset_factory(Answer, Explanation, fields=('text',),can_delete=False, extra=2)
    
    answer_formsets = AnswerFormset(initial=[{'order':i} for i in range(1,NUM_CHOICES+1)])

    answer_formgroups = zip(
        answer_formsets,
        [ExplanationFormset() for i in range(4)]
    )
    if request.method == 'GET':
        context = {
            # 'quiz_form':CreateQuizForm(),
            # 'Question':ModelForm(Question),
            'quiz_form':QuizForm(),
            'question_form':QuestionForm(),
            'answer_formsets': answer_formsets,
            'answer_formgroups':answer_formgroups,
        }

        return render(request, 'lti/create_quiz.html', context)

    elif request.method == 'POST':
        # logic for handling create quiz form data
        quiz_form = QuizForm(request.POST)
        if not quiz_form.is_valid():
            # change this to a rendered warning
            return Exception('quiz not valid')

        quiz = quiz_form.save(commit=False)
        quiz.course = 123
        quiz.user = request.user
        quiz.url = ''
        quiz.save()

        question_form = QuestionForm(request.POST)
        question = question_form.save(commit=False)
        question.quiz = quiz
        question.save()

        answer_forms = AnswerFormset(request.POST, instance=question)
        answers = answer_forms.save()

        for i in range(4):
            explanations = ExplanationFormset(request.POST, instance=answers[i])
            explanations.save()

        if quiz_form.cleaned_data['use_qualtrics']:
            qsf_url = 'https://'+request.get_host()+reverse('lti:qsf_for_quiz')
            survey_name = 'Survey from modified qsf'
            qualtrics_url = upload_qsf_to_qualtrics(qsf_url, survey_name)
            if qualtrics_url:
                quiz.url = qualtrics_url
                HttpResponseRedirect(reverse('lti:embed_quiz',kwargs={'quiz_id':quiz.pk}))
            else:
                raise Exception('quiz creation failed and did not return a qualtrics id')

        # alternatively, could redirect back to select_or_create_quiz and have user select the quiz they just created
        return HttpResponseRedirect(reverse('lti:embed_quiz',kwargs={'quiz_id':quiz.pk}))



def embed_quiz(request, quiz_id):
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
            launch_url='https://'+request.get_host()+reverse('lti:launch_quiz',kwargs={'quiz_id':quiz_id})
        )
    )


@login_required()
# @require_http_methods(['POST'])
def launch_quiz(request,quiz_id):
    '''
    Student: Launches the qualtrics quiz specified by the passed qualtrics_url parameter
    Instructor: Redirect to the analytics view for the particular quiz
    '''

    # put more LTI params in the LTI launch session variable - needed when authenticating sent results back to canvas
    more_lti_params = {
        'lis_outcome_service_url': request.POST.get('lis_outcome_service_url', None),
        'lis_result_sourcedid': request.POST.get('lis_result_sourcedid', None),
        'oauth_consumer_key': request.POST.get('oauth_consumer_key', None),
    }
    request.session['LTI_LAUNCH'].update(more_lti_params)

    # TODO store canvas user id and lti user id so that we can have a mapping

    quiz = Quiz.objects.get(pk=quiz_id)

    # could move to settings or infer this somehow
    # base_qualtrics_url = 'https://harvard.az1.qualtrics.com/SE/?SID='

    # Using a static sample qualtrics quiz for now
    # TODO: create this by auto-generating a qualtrics survey with API after instructor quiz creation
    # quiz_url = 'https://harvard.az1.qualtrics.com/SE/?SID=SV_e3t9eS1YWxFelYp'


    # Check if the quiz has a qualtrics url. If not, then we can host the quiz ourself
    if quiz.url:
        quiz_url = quiz.url
    else:
        quiz_url = reverse('lti:display_quiz_question',kwargs={'quiz_id':quiz.id})


    # qualtrics_url = '{}{}'.format(base_qualtrics_url,qualtrics_id)

    # get non-sensitive user_id

    # If instructor, redirect to instructor "manage quiz" view
    if 'Instructor' in request.session['LTI_LAUNCH']['roles']:

        # pass in qualtrics url so iframe in template can display qualtrics quiz preview
        context = {'quiz_url':quiz_url}
        
        return render(request, 'lti/manage_quiz.html',context)

        # return HttpResponseRedirect(reverse('lti:manage_quiz',kwargs={'quiz_id':quiz_id}))

    # if student, serve the quiz
    else:
        
        # TODO: determine params to pass to quiz. probably at least the user_lti_id and quiz_id so the quiz can make web service calls with these
        quiz_params = {
            # 'quiz_id':quiz_id,
            # 'user_lti_id': request.get_host()
            # 'qlb_return_url': request.get_host()
        }

        # TODO append params to qualtrics url
        # qualtrics_full_url = '{qualtrics_url}?SID={qualtrics_id}&'

        # TODO we might determine some adaptivity parameters here (e.g. quiz version) based on user
        
        # TODO add extra parameters to be passed to the qualtrics survey (lti_user_id, resource_id, adaptivity parameters, etc.)


        # TODO instructor view for the qualtrics quiz
        # return HttpResponseRedirect(qualtrics_url)


        return HttpResponseRedirect(quiz_url)
        # return HttpResponse('Instructor view for qualtrics quiz {}'.format(qualtrics_url))


# def manage_quiz(request, quiz_id):
#     '''
#     Instructor analytics/preview view for a quiz
#     maybe put modification options directly on here
#     '''



def modify_quiz(request, quiz_id):
    '''
    Modify a quiz (question/answer text)
    Accessed from the display quiz
    '''

    # similar to add_or_create quiz except there should be a modify currently used quiz option
    
    pass


def end_of_quiz(request):
    '''
    Quiz should send data here after completion
    Then the relevant outcome data is returned to the LMS
    '''
    print 'redirected to end_of_quiz'

    # TODO replace this default value if we have an actual grade
    score = 1

    # consumer_key = request.session['LTI_LAUNCH'].get('oauth_consumer_key')
    # consumer_secret = settings.LTI_OAUTH_CREDENTIALS[request.session['LTI_LAUNCH'].get('oauth_consumer_key')]

    # send the outcome data
    outcome = OutcomeRequest(
        {
            # required for outcome reporting
            'lis_outcome_service_url':request.session['LTI_LAUNCH'].get('lis_outcome_service_url'),
            'lis_result_sourcedid':request.session['LTI_LAUNCH'].get('lis_result_sourcedid'),
            'consumer_key': request.session['LTI_LAUNCH'].get('oauth_consumer_key'),
            'consumer_secret': settings.LTI_OAUTH_CREDENTIALS[request.session['LTI_LAUNCH'].get('oauth_consumer_key')],
        }
    )
    print outcome.generate_request_xml()
    outcome_response = outcome.post_replace_result(
        score,
        # result_data={
        #     # 'url':'placeholder'
        #     # 'text':None,
        # }
    )
    return HttpResponse(outcome_response.code_major)
    # return render(request, 'lti/end_of_quiz.html')
    return HttpResponseRedirect(request.session['LTI_LAUNCH'].get('launch_presentation_return_url'))

