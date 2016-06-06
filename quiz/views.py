from django.shortcuts import render, redirect
from engine.models import *
from .forms import ChooseAnswerForm, RateExplanationForm
from engine.utils import get_explanation_for_student


# Create your views here.

def display_quiz_question(request, question_id):
    '''
    self-hosted quiz: display initial question and prompt for answer choice
    '''
    if request.method=='GET':
        # quiz = Quiz.objects.get(pk=quiz_id)

        # just get first question in quiz for now
        question = Question.objects.get(pk=question_id)
        answers = question.answer_set.all().order_by('order')

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

        return render(request, 'quiz/display_quiz_question.html', context)

    elif request.method=='POST':
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']

            selected_explanation = get_explanation_for_student(answer, request.user, 'random')

            # redirect to explanation/rating view, for the selected explanation
            return redirect('quiz:display_quiz_explanation',explanation_id=selected_explanation.id)


def display_quiz_explanation(request, explanation_id):
    '''
    self-hosted quiz: show explanation and let student rate the explanation
    '''
    explanation = Explanation.objects.get(pk=explanation_id)

    if request.method =='GET':
        rate_explanation_form = RateExplanationForm()

        context = {
            'explanation':explanation,
            'rate_explanation_form':rate_explanation_form
        }

        return render(request, 'quiz/display_quiz_explanation.html', context)

    elif request.method == 'POST':
        print "posted to display_quiz_explanation"
        # process student rating for explanation
        rate_explanation_form = RateExplanationForm(request.POST)

        if rate_explanation_form.is_valid():
            rating = rate_explanation_form.cleaned_data['rating']

            # save to db
            rating = Result(user=request.user, explanation=explanation, value=rating)

            rating.save()
            
            return redirect('lti:return_outcome')


