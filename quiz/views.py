from django.shortcuts import render, redirect
from engine.models import *
from .forms import ChooseAnswerForm, RateExplanationForm
from engine.utils import get_explanation_for_student
from lti.utils import grade_passback

# Create your views here.

def question(request, question_id):
    '''
    self-hosted quiz: display initial question and prompt for answer choice
    '''
    if request.method=='GET':
        # quiz = Quiz.objects.get(pk=quiz_id)

        # just get first question in quiz for now
        question = Question.objects.get(pk=question_id)
        answers = question.answer_set.all().order_by('_order')

        # could simulate web service request to get: questions, answers
        # question_data = requests.get(reverse('adaptive_engine:get_question'),params={'id':question.id})
        # question_text = question_data['text']

        # alternative: get objects directly
        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
            'question':question,
            'choose_answer_form': choose_answer_form,
        }

        return render(request, 'quiz/question.html', context)

    elif request.method=='POST':
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']

            # TODO save selected answer and grade to database

            # redirect to explanation/rating view, for the selected explanation
            return redirect('quiz:answer',answer_id=answer.id)


def answer(request, answer_id):
    '''
    self-hosted quiz: show explanation for answer and let student rate the explanation
    '''
    answer = Answer.objects.get(pk=answer_id)
    mooclet = answer.mooclet

    if request.method =='GET':

        # get explanation mooclet version
        mooclet_context = {
            'user':request.user,
            'mooclet':mooclet,
        }
        version = mooclet.get_version(mooclet_context)
        explanation = version.explanation

        rate_explanation_form = RateExplanationForm(initial={'object_id':version.id})

        context = {
            'answer':answer,
            'explanation':explanation,
            'rate_explanation_form':rate_explanation_form
        }

        return render(request, 'quiz/answer.html', context)

    elif request.method == 'POST':

        user_roles = request.session['LTI_LAUNCH']['roles']
        if 'Instructor' in user_roles or 'ContentDeveloper' in user_roles:
            return redirect('quiz:question', question_id=answer.question.id)

        else:
            # process student rating for explanation
            rate_explanation_form = RateExplanationForm(request.POST)

            rating = rate_explanation_form.save(commit=False)
            rating.variable_id = Variable.objects.get(name='version_rating').id
            rating.user = request.user
            rating.save()

            #TODO determine grading policy
            score = 1

            # grade passback to LMS
            grade_passback(request,score)

            return redirect('lti:return_to_LMS')

        # else:
        #     return redirect('quiz:answer',answer_id=answer.id)

def placeholder(request):
    return render(request, 'quiz/placeholder.html')

def complete(request):
    return render(request, 'quiz/complete.html')
    

    