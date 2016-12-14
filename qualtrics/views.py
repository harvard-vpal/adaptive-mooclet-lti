from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from quip.models import *
from .utils import get_modified_qsf
from lti.utils import grade_passback

# Create your views here.

def create_qualtrics_quiz_from_url(request):
    '''
    Used for embedding an arbitrary Qualtrics (or other) URL in the resource selection mode
    '''
    if request.method == 'GET':
        context = {
            'qualtrics_quiz_form':QualtricsUrlQuizForm(),
        }
        return render(request, 'qualtrics/create_qualtrics_quiz_from_url.html', context) 
    elif request.method == 'POST':
        qualtrics_quiz_form = QualtricsUrlQuizForm(request.POST)
        quiz = qualtrics_quiz_form.save(commit=False)
        quiz.user = request.user
        quiz.context = request.session['LTI_LAUNCH']['context_id']
        quiz.save()

        return HttpResponseRedirect(reverse('lti:return_launch_url',kwargs={'quiz_id':quiz.pk}))


def qsf_for_question(request, question_id):
    '''
    Generates the qsf corresponding to the question_id provided as input
    Referenced by 'upload QSF by URL' Qualtrics API call
    '''
    question = get_object_or_404(Question, pk=question_id)
    question_qsf = get_modified_qsf(question)

    # TODO LATER upload multiple qsf for multiple questions in a quiz?

    return HttpResponse(question_qsf)


def end_quiz(request, quiz, grade):
    '''
    Redirect here after survey (end of last survey in chain, if multiple questions) 
    to do grade passback and return to LMS
    '''
    grade_passback(grade, request.user, quiz)
    return redirect('lti:exit')
