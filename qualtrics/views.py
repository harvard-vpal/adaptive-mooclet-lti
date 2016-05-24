from django.shortcuts import render
from django.http import HttpResponse
from engine import *
from engine.models import Quiz
from .utils import get_modified_qsf

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

        # placeholder values
        quiz.course = 7566 
        quiz.user = request.user

        quiz.save()

        # alternatively, could redirect back to select_or_create_quiz and have user select the quiz they just created
        return HttpResponseRedirect(reverse('lti:return_launch_url',kwargs={'quiz_id':quiz.pk}))


def qsf_for_question(request, quiz_id):
    '''
    Generates the qsf corresponding to the quiz_id provided as input
    Referenced by 'upload QSF by URL' Qualtrics API call
    '''
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz_qsf = get_modified_qsf(quiz)
    # upload multiple qsf for multiple questions in a quiz?

    return HttpResponse(quiz_qsf)
