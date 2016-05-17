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

# using dce_lti_py instad of ims_lti_py for grade passback
from dce_lti_py import OutcomeRequest
#from ims_lti_py import OutcomeRequest

from django.views.generic.edit import CreateView
from .models import Quiz, Question, Answer, Explanation
from django.forms import inlineformset_factory, ModelForm
from .forms import *

from adaptive_engine_app.algorithms import computeExplanation_Thompson 


logger = logging.getLogger(__name__)

TOOL_NAME = 'Qualtrics LTI Bridge'


#### QLB views ####


def index(request):
    '''
    Show some placeholder page
    '''
    return render(request, 'qlb/index.html')


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
    #     'url': host + reverse('qlb:manage_quizzes'),
    # }
    # lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', course_nav_params)

    # configuration for quiz selection mode
    resource_selection_params = {
        'enabled': 'true',
        'selection_width':"700",
        'selection_height':"500",
        'url': host + reverse('qlb:select_or_create_quiz'),
    }

    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'domain', request.get_host().partition(':')[0])
    lti_tool_config.description = 'The Qualtrics LTI Bridge allows instructors to embed qualtrics quizzes in an LMS as an LTI tool.'
    # add resource selection params to the xml
    lti_tool_config.set_ext_param('canvas.instructure.com', 'resource_selection', resource_selection_params)

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp


@login_required()
def quiz_list(request):
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

        # qualtrics survey for creating quizzes
        # url_createQuizSurvey = 'https://harvard.az1.qualtrics.com/SE/?SID=SV_8GSbHCQpHUcuNnf'
        select_quiz_form = SelectQuizForm()
        context = {'select_quiz_form':select_quiz_form}
        return render(request, 'qlb/select_or_create_quiz.html',context)
        # return HttpResponseRedirect(url_createQuizSurvey)

    elif 'form_submit' in request.GET:
        select_quiz_form = SelectQuizForm(request.POST)
        if select_quiz_form.is_valid():
            quiz = select_quiz_form.cleaned_data['quiz']

            # embed quiz
            return HttpResponseRedirect(reverse('qlb:embed_quiz',kwargs={'quiz_id':quiz.pk}))


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

        return render(request, 'qlb/create_quiz.html', context)

    elif request.method == 'POST':
        # logic for handling create quiz form data
        quiz_form = QuizForm(request.POST)
        quiz = quiz_form.save(commit=False)
        quiz.course = 123
        quiz.user = request.user
        quiz.url = 'abc123'
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

        return HttpResponseRedirect(reverse('qlb:embed_quiz',kwargs={'quiz_id':quiz.pk}))


def create_quiz_from_submission(request):
    '''
    Triggered on a submission to the create quiz survey
    Makes an API call to the quiz to get submission data
    Save questions/answers to database
    Use questions/answers to create new qualtrics quiz
    Embed the quiz in the location if in an assignments context
    Redirect to a confirmation page
    '''

    # expect some id parameter to be passed
    user_id = request.GET['course_id']

    # TODO use qualtrics api to get latest submission for course
    # data = request.get(qualtrics_api_endpoint).json()

    # TODO save questions/answers to database, either locally or to adaptive engine

    # TODO provision a new quiz on qualtrics using API

    # url of newly generated quiz
    url_newQuiz = 'https://harvard.az1.qualtrics.com/SE/?SID=newquiz'

    # save quiz in quiz bank database

    # check if the launch is from the assignment context
    if 'ext_content_return_types' in request.session['LTI_LAUNCH']:

        # embed the quiz by giving the qlb launch url to the LMS return location
        return_url = request.session['LTI_LAUNCH']['ext_content_return_url']
        return HttpResponseRedirect(
            '{return_url}?return_type=lti_launch_url&url={qlb_launch_url}'.format(
                return_url=return_url,
                qlb_launch_url='https://' + request.get_host() + reverse('qlb:launch_quiz',kwargs={'qualtrics_id':qualtrics_id})
            )
        )


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
            launch_url='https://'+request.get_host()+reverse('qlb:launch_quiz',kwargs={'quiz_id':quiz_id})
        )
    )


@login_required()
# @require_http_methods(['POST'])
def launch_quiz(request,quiz_id):
    '''
    Student: Launches the qualtrics quiz specified by the passed qualtrics_url parameter
    Instructor: Redirect to the analytics view for the particular quiz
    '''

    # TODO store canvas user id and lti user id so that we can have a mapping

    quiz = Quiz.objects.get(pk=quiz_id)


    # could move to settings or infer this somehow
    # base_qualtrics_url = 'https://harvard.az1.qualtrics.com/SE/?SID='

    # Using a static sample qualtrics quiz for now
    # TODO: create this by auto-generating a qualtrics survey with API after instructor quiz creation
    qualtrics_url = 'https://harvard.az1.qualtrics.com/SE/?SID=SV_e3t9eS1YWxFelYp'
    # qualtrics_url = '{}{}'.format(base_qualtrics_url,qualtrics_id)

    # get non-sensitive user_id

    

    # If instructor, redirect to instructor "manage quiz" view
    if 'Instructor' in request.session['LTI_LAUNCH']['roles']:

        # pass in qualtrics url so iframe in template can display qualtrics quiz preview
        context = {'qualtrics_url':qualtrics_url}
        
        return render(request, 'qlb/manage_quiz.html',context)

        # return HttpResponseRedirect(reverse('qlb:manage_quiz',kwargs={'quiz_id':quiz_id}))

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
        return HttpResponseRedirect(qualtrics_url)
        # return HttpResponse('Instructor view for qualtrics quiz {}'.format(qualtrics_url))


# def manage_quiz(request, quiz_id):
#     '''
#     Instructor analytics/preview view for a quiz
#     maybe put modification options directly on here
#     '''

def display_quiz_question(request, quiz_id):
    if not request.method=='POST':
        question = Question.objects.filter(quiz=quiz_id).first()
        answers = question.answer_set.all().order_by('order')

        # simulate web service request to get: questions, answers
        # question_data = requests.get(reverse('adaptive_engine:get_question'),params={'id':question.id})
        # question_text = question_data['text']

        # alternative:

        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
            'question':question,
            # 'answers': question.answer_set.all().order_by('order'),
            'choose_answer_form': choose_answer_form,
        }

        return render(request, 'qlb/display_quiz_question.html', context)


    else:
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']
            # save chosen answer to db

            # get explanation
            # make API call to adaptive engine
            
            url = 'https://'+request.get_host()+reverse('adaptive_engine:get_explanation_for_student')
            explanation_id = requests.get(
                url,
                params={
                    'student_id':student_id,
                    'answer_id':answer_id
                }
            ).json()['explanation']['fields']['text']


            student_id = 'placeholder'
            
            # explanation = Explanation.get(pk=explanation_id)

            # redirect to explanation view
            HttpResponseRedirect(reverse('qlb:display_quiz_explanation',kwargs={'explanation_id':explanation_id}))

def display_quiz_explanation(request, explanation_id):
    explanation = Explanation.objects.get(pk=explanation_id)

    if not request.method=='POST':
        rate_explanation_form = RateExplanationForm()

        context = {
            'explanation':explanation,
            'rate_explanation_form':rate_explanation_form
        }

        return render(request, 'qlb:display_quiz_explanation', context)

    else:
        # process student rating for explanation
        rate_explanation_form = RateExplanationForm(request.POST)
        if rate_explanation_form.is_valid():
            rating = rate_explanation_form.cleaned_data['rating']

            # save to db
            rating = Result(student=request.user, explanation=explanation, value=rating)



def modify_quiz(request, quiz_id):
    '''
    Modify a quiz (question/answer text)
    Accessed from the display quiz
    '''

    # similar to add_or_create quiz except there should be a modify currently used quiz option
    
    pass


def end_of_quiz(request):
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


