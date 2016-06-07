from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse, JsonResponse

import json

from engine.algorithms import computeExplanation_Thompson 
from engine.models import *
from engine import utils

from rest_framework import viewsets
from api.serializers import *

##### rest-framework #####

class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


#### custom endpoints, used by qualtrics to retrieve object text ####

# Get question text and answer choices using a question id
# INPUT: question_id
# OUTPUT: question text, answer texts, correct answer choice
def get_question (request):
    if 'id' not in request.GET:
        return HttpResponse('question_id not found in GET parameters')
    question = get_object_or_404(Question, id=request.GET['id'])
    answers = question.answer_set.all()

    correctAnswerChoice = 0
    for i in range(len(answers)):
        if answers[i].correct:
            correctAnswerChoice = i+1
            break

    return JsonReponse({
        'questionText':question.text,
        'answer1':answers[0].text,
        'answer2':answers[1].text,
        'answer3':answers[2].text,
        'answer4':answers[3].text,
        'correctAnswerChoice':correctAnswerChoice,
    })
    return JsonResponse(data)

# Computes and returns the Explanation that a particular student should receive for
# a particular question.
def get_explanation_for_student (request):
    if 'answer_id' not in request.GET:
        return HttpResponse('answer_id not found in GET parameters')
    # if 'student_id' not in request.GET:
    #     return HttpResponse('student_id not found in GET parameters')

    answer = get_object_or_404(Answer, id=request.GET['answer_id'])

    # placeholder student for now
    student = User.objects.first()
    # student = get_object_or_404(User, id=request.GET['student_id'])

    explanation = utils.get_explanation_for_student(answer,student)

    return JsonResponse({
        'explanationid':explanation.id,
        'explanation':explanation.text,
    })


# Retrieves all explanations for a particular question.
# INPUT: question_id
# OUTPUT: Array of Explanation objects
def get_explanations_for_question (request):
    if 'question_id' not in request.GET:
        return HttpResponse('question_id not found in GET parameters')
    allExplanations = []
    for explanation in Explanation.objects.filter(question_id=request.GET['question_id']).iterator():
        allExplanations.append(explanation)
    return JsonResponse(json.loads(serializers.serialize("json", allExplanations)), safe=False)


# Submits a scalar score (1-7) associated with a particular student who received a
# particular explanation.
# INPUT: explanation_id, student_id, value (1-7)
# OUTPUT: id of new Result object
def submit_result_of_explanation (request):
    if 'explanation_id' not in request.GET:
        return HttpResponse('explanation_id not found in GET parameters')
    if 'student_id' not in request.GET:
        return HttpResponse('student_id not found in GET parameters')
    if 'value' not in request.GET:
        return HttpResponse('value not found in GET parameters')
    
    theValue = (float(request.GET['value']) - 1.0) / 6.0
    result = Result(student_id=request.GET['student_id'], explanation_id=request.GET['explanation_id'], value=theValue)
    result.save()
    return JsonResponse({ "id": result.id })
