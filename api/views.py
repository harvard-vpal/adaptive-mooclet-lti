from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from collections import OrderedDict
import json

from engine.algorithms import computeExplanation_Thompson 
from engine.models import *
from engine import utils

from rest_framework import viewsets
from api.serializers import *

##########################
##### rest-framework #####
##########################

class QuizViewSet(viewsets.ModelViewSet):
    """
    list quizzes
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    list questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


#####################################################################
#### custom endpoints, used by qualtrics to retrieve object text ####
#####################################################################

def get_question(request):
    '''
    INPUT (via GET params): question_id
    OUTPUT: quiz_id, question_text, correct_choice, [answer{n}_text]*n
    '''
    if 'id' not in request.GET:
        return HttpResponse('question_id not found in GET parameters')
    question = get_object_or_404(Question, pk=request.GET['id'])
    answers = question.answer_set.all()

    num_answers = len(answers)

    # identifies the correct answer choice
    # if there's more than one labelled correct only the first is identified
    correct_choice = 0
    for answer in answers:
        if answer.correct:
            # answer.order is zero-indexed
            correct_choice = answer.order+1
            break

    output = {
        'quiz_id': question.quiz.id,
        'text':question.text,
        'correct_choice':correct_choice,
    }

    # add answer text to output, e.g. answer1_text: "answer text"
    for i in range(num_answers):
        output['answer{}_text'.format(i+1)] = answers[i].text
    
    return JsonResponse(output, json_dumps_params={'sort_keys':True})

def is_correct(request):
    '''
    to be implemented
    check whether a
    '''
    pass

def get_explanation_for_student(request):
    '''
    Computes and returns the Explanation that a particular student should receive for
    a particular question.

    INPUT (via GET params): question_id, answer_choice, user_id
    OUTPUT: explanation_id, explanation_text
    '''
    if 'answer_choice' not in request.GET:
        return HttpResponse('answer_choice not found in GET parameters')
    if 'question_id' not in request.GET:
        return HttpResponse('question_id not found in GET parameters')
    # disabled for ease of testing
    # if 'user_id' not in request.GET:
    #     return HttpResponse('user_id not found in GET parameters')

    question = get_object_or_404(Question, id=request.GET['question_id'])
    answer = get_object_or_404(Answer, question=question, order=request.GET['answer_choice'])

    # placeholder student for now, still need to determine what kind of user_id to use (internal django, lti id, etc)
    user = User.objects.first()
    # student = get_object_or_404(User, id=request.GET['user_id'])

    explanation = utils.get_explanation_for_student(answer, user)

    return JsonResponse({
        'explanation_id':explanation.id,
        'explanation_text':explanation.text,
    })


def submit_result_of_explanation(request):
    '''
    # Submits a scalar score (1-7) associated with a particular student who received a
    # particular explanation.

    INPUT (via GET params): explanation_id, user_id, value (1-7)
    OUTPUT: result_id
    '''
    if 'explanation_id' not in request.GET:
        return HttpResponse('explanation_id not found in GET parameters')
    # if 'user_id' not in request.GET:
    #     return HttpResponse('user_id not found in GET parameters')
    if 'value' not in request.GET:
        return HttpResponse('value not found in GET parameters')
    
    value = (float(request.GET['value']) - 1.0) / 6.0

    result = Result(
        user_id=request.GET['user_id'],
        explanation_id=request.GET['explanation_id'],
        value=value
    )
    result.save()
    return JsonResponse({ "result_id": result.id })


def submit_quiz_grade(request):
    '''
    Submits a quiz grade and triggers grade passback to the LMS

    INPUT (via GET params): user_id, quiz_id, grade
    '''
    return JsonResponse({'message': 'not implemented'})





