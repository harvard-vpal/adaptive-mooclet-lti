from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse

from .models import *
from .forms import *
from .utils import *

from qualtrics.utils import upload_qsf_to_qualtrics
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
    context = {
        'quiz': quiz,
        'quiz_url':quiz_url,
    }
    
    return render(request, 'engine/manage_quiz.html',context)

def create_quiz_options(request):
    return render(request, 'engine/create_quiz_options.html')

def create_blank_quiz(request):

    quiz = Quiz.objects.create(
        user=request.user,
        context = request.session['LTI_LAUNCH']['context_id'],
    )
    quiz.save()
    return redirect('lti:return_launch_url', quiz_id=quiz.pk)

def create_quiz_from_url(request):
    if request.method == 'GET':
        quiz_url_form = QuizUrlForm()


# def select_or_create_quiz(request):
#     '''
#     Accessed via select resource mode when editing assignment
#     Select a quiz that has already been made, or create a new one
#     see https://www.edu-apps.org/extensions/content.html
#     '''
#     if request.method == 'GET':
#         select_quiz_form = SelectQuizForm()
#         context = {'select_quiz_form':select_quiz_form}
#         return render(request, 'engine/select_or_create_quiz.html', context)

#     elif request.method == 'POST':
#         select_quiz_form = SelectQuizForm(request.POST)
#         if select_quiz_form.is_valid():
#             quiz = select_quiz_form.cleaned_data['quiz']

#             # embed quiz
#             return redirect('lti:return_launch_url',quiz_id=quiz.pk)


def modify_quiz(request, quiz_id):
    '''
    displays some a form to collect question, answers and explanations
    '''
    quiz = Quiz.objects.get(pk=quiz_id)

    if quiz.question_set.all().exists():
        question = quiz.question_set.first()
        question_status = 'exists'
    else:
        question = Question(quiz=quiz)
        question_status = 'new'
    
    if request.method == 'GET':

        INITIAL_NUM_CHOICES = 4
        INITIAL_NUM_EXPLANATIONS = 2
        
        AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
        # ExplanationFormset = inlineformset_factory(Answer, Explanation, fields=('text',),can_delete=False, extra=2)
        
        #TODO fix this
        quiz_form = QuizForm(instance=quiz)

        # if quiz.question_set.all().exists():
        #     question = quiz.question_set.first()
        # else:
        #     question = Question(quiz=quiz)

        print question.quiz.id
        question_form = QuestionForm(instance=question)

        answer_formset = AnswerFormset(instance=question)
        # answers = answer_formsets.save(commit=False)

        # answer_formgroups = zip(
        #     answer_formsets,
        #     [ExplanationFormset(instance=answer) for answer in answers]
        # )

        context = {
            # 'quiz_form':CreateQuizForm(),
            # 'Question':ModelForm(Question),
            'quiz_form':quiz_form,
            'question_form':question_form,
            'answer_formset': answer_formset,
            # 'answer_formgroups':answer_formgroups,
        }

        return render(request, 'engine/modify_quiz.html', context)

    elif request.method == 'POST':

        # logic for handling create quiz form data
        quiz_form = QuizForm(request.POST, instance=quiz)

        quiz = quiz_form.save(commit=False)

        # quiz.course = 7566
        if 'LTI_LAUNCH' in request.session:
            quiz.context = request.session['LTI_LAUNCH']['context_id']
        quiz.user = request.user
        quiz.save()

        # if quiz.question_set.all().exists():
        #     question = quiz.question_set.first()
        # else:
        #     question = Question(quiz=quiz)

        question_form = QuestionForm(request.POST, instance=question)


        question = question_form.save(commit=False)

        question.save()
        # question.quiz = quiz
        # question_form.save()

        AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
        # ExplanationFormset = inlineformset_factory(Answer, Explanation, fields=('text',),can_delete=False, extra=2)

        answer_formset = AnswerFormset(request.POST, instance=question)
        answers = answer_formset.save()

        # for i in range(len(answers)):
        #     explanations = ExplanationFormset(request.POST, instance=answers[i])
        #     explanations.save()

        quiz_form.is_valid()
        if quiz_form.cleaned_data['use_qualtrics']:

            if question_status is 'new' or not quiz.url:
                print "starting quiz provisioning process"

                # this is the url that the modified QSF will be hosted at
                qsf_url = request.build_absolute_uri(reverse('qualtrics:qsf_for_question',kwargs={'question_id':question.id}))

                # name of the survey that will created on Qualtrics after QSF upload
                survey_name = 'adaptive-quiz {} {}'.format(request.get_host().partition(':')[0],quiz.id)
                
                # new_survey_url is the url of the survey that was just created on Qualtrics
                new_survey_url = upload_qsf_to_qualtrics(qsf_url, survey_name)
                if not new_survey_url:
                    raise Exception('quiz creation failed and did not return a qualtrics id')

                quiz.url = new_survey_url
                quiz.save()


        # pass back lti launch url to LMS
        # return redirect('lti:return_launch_url',quiz_id=quiz.pk)

        # alternatively, could redirect back to select_or_create_quiz and have user select the quiz they just created
        return redirect('engine:manage_quiz',quiz_id=quiz_id)

# def manage_quiz(request, quiz_id):
#     '''
#     Instructor analytics/preview view for a quiz
#     maybe put modification options directly on here
#     '''






