from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm

from .models import *
from .forms import *
from .utils import *
# from qualtrics.utils import upload_qsf_to_qualtrics
import qualtrics.utils.upload_qsf_to_qualtrics

from engine.algorithms import computeExplanation_Thompson 


# from django.views.generic.edit import CreateView


#### QUIZ MANAGEMENT ####

def manage_quiz(request, quiz_id):
    '''
    Teacher view for a quiz
    '''
    quiz = Quiz.objects.get(pk=quiz_id)


    # Check if the quiz has a qualtrics url. If not, then we can host the quiz ourself
    if quiz.url:
        # qualtrics url
        quiz_url = quiz.url
    else:
        # django url
        quiz_url = reverse('quiz:display_quiz_question',kwargs={'quiz_id':quiz.id})


    # pass in qualtrics url so iframe in template can display qualtrics quiz preview
    context = {'quiz_url':quiz_url}
    
    return render(request, 'engine/manage_quiz.html',context)


def select_or_create_quiz(request):
    '''
    Accessed via select resource mode when editing assignment
    Select a quiz that has already been made, or create a new one
    see https://www.edu-apps.org/extensions/content.html
    '''
    if request.method == 'GET':
        select_quiz_form = SelectQuizForm()
        context = {'select_quiz_form':select_quiz_form}
        return render(request, 'engine/select_or_create_quiz.html', context)

    elif request.method == 'POST':
        select_quiz_form = SelectQuizForm(request.POST)
        if select_quiz_form.is_valid():
            quiz = select_quiz_form.cleaned_data['quiz']

            # embed quiz
            return redirect('lti:return_launch_url',quiz_id=quiz.pk)


def create_quiz(request):
    '''
    displays some a form to collect question, answers and explanations
    '''
    
    if request.method == 'GET':

        INITIAL_NUM_CHOICES = 4
        INITIAL_NUM_EXPLANATIONS = 2

        AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','order','correct'), can_delete=False, extra=4)
        ExplanationFormset = inlineformset_factory(Answer, Explanation, fields=('text',),can_delete=False, extra=2)
        
        answer_formsets = AnswerFormset(initial=[{'order':i} for i in range(1,INITIAL_NUM_CHOICES+1)])

        answer_formgroups = zip(
            answer_formsets,
            [ExplanationFormset() for i in range(4)]
        )

        context = {
            # 'quiz_form':CreateQuizForm(),
            # 'Question':ModelForm(Question),
            'quiz_form':QuizForm(),
            'question_form':QuestionForm(),
            'answer_formsets': answer_formsets,
            'answer_formgroups':answer_formgroups,
        }

        return render(request, 'engine/create_quiz.html', context)

    elif request.method == 'POST':

        # logic for handling create quiz form data
        quiz_form = QuizForm(request.POST)
        if not quiz_form.is_valid():
            # TODO change this so that we return to the form and display a warning
            raise Exception('quiz not valid')

        quiz = quiz_form.save(commit=False)
        # quiz.course = 7566
        if 'LTI_LAUNCH' is request.session:
            quiz.context = request.session['LTI_LAUNCH']['context_id']
        quiz.user = request.user
        quiz.url = ''
        quiz.save()

        question_form = QuestionForm(request.POST)
        question = question_form.save(commit=False)
        question.quiz = quiz
        question.save()

        AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','order','correct'), can_delete=False, extra=4)
        ExplanationFormset = inlineformset_factory(Answer, Explanation, fields=('text',),can_delete=False, extra=2)

        answer_forms = AnswerFormset(request.POST, instance=question)
        answers = answer_forms.save()

        for i in range(len(answers)):
            explanations = ExplanationFormset(request.POST, instance=answers[i])
            explanations.save()

        if quiz_form.cleaned_data['use_qualtrics']:
            # this is the url that the modified QSF will be available at
            qsf_url = 'https://'+request.get_host()+reverse('qualtrics:qsf_for_quiz')
            # name of the survey that will created on Qualtrics after QSF upload
            survey_name = 'Survey from modified qsf'
            # new_survey_url is the url of the survey that was just created on Qualtrics
            new_survey_url = qualtrics.utils.upload_qsf_to_qualtrics(qsf_url, survey_name)
            if qualtrics_url:
                quiz.url = qualtrics_url
                HttpResponseRedirect(reverse('lti:lti_return_launch_url',kwargs={'quiz_id':quiz.pk}))
            else:
                raise Exception('quiz creation failed and did not return a qualtrics id')

        # pass back lti launch url to LMS
        # return redirect('lti:return_launch_url',quiz_id=quiz.pk)

        # alternatively, could redirect back to select_or_create_quiz and have user select the quiz they just created
        return redirect('engine:select_or_create_quiz')

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




