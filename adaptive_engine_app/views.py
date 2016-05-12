# sample views for adaptive_engine_app

import json
from .algorithms import computeExplanation_Thompson 
from .models import Question, Explanation, Result
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import HttpResponse, JsonResponse

# Retrieves a Question object with the specified question_id.
# INPUT: question_id
# OUTPUT: Question object
def get_question (request):
	if 'question_id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	question = get_object_or_404(Question, id=request.GET['question_id'])
	jsonDict = json.loads(serializers.serialize("json", [ question ]))[0]
	return JsonResponse(jsonDict)

# Check if all required parameters are contained in the request object
# for the add_question function.
def verify_params_for_add_question (request):
	if 'text' not in request.GET:
		return HttpResponse('text not found in GET parameters')
	if 'answer1' not in request.GET:
		return HttpResponse('answer1 not found in GET parameters')
	if 'answer2' not in request.GET:
		return HttpResponse('answer2 not found in GET parameters')
	if 'answer3' not in request.GET:
		return HttpResponse('answer3 not found in GET parameters')
	if 'answer4' not in request.GET:
		return HttpResponse('answer4 not found in GET parameters')
	return None

# Adds a new Question object with the specified question text and answers.
# INPUT: text, answer1, answer2, answer3, and answer4
# OUTPUT: Confirmation message
def add_question (request):
	errorResponse = verify_params_for_add_question(request)
	if errorResponse != None:
		return errorResponse
	
	question = Question(text=request.GET['text'], answer1=request.GET['answer1'], \
	                                              answer2=request.GET['answer2'], \
	                                              answer3=request.GET['answer3'], \
	                                              answer4=request.GET['answer4'])
	question.save()
	return JsonResponse({ "received": "yes" })

# Changes an existing Question object.
# INPUT: Question object ("id", "text", "answer1", "answer2", "answer3", and "answer4")
# OUTPUT: Confirmation message
def change_question (request):
	errorResponse = verify_params_for_add_question(request)
	if errorResponse != None:
		return errorResponse
	if 'id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')

	question = Question(id=request.GET['id'], text=request.GET['text'], \
	                    answer1=request.GET['answer1'], \
			    answer2=request.GET['answer2'], \
	                    answer3=request.GET['answer3'], \
	                    answer4=request.GET['answer4'])
	question.save()
	return JsonResponse({ "received": "yes" })

# Retrieves all explanations for a particular question.
# INPUT: question_id
# OUTPUT: Array of Explanation objects
def get_explanations_for_question (request):
	if 'question_id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	allExplanations = []
	for explanation in Explanation.objects.filter(question_id=request.GET['question_id']).iterator():
		allExplanations.append(explanation)
	return JsonResponse(allExplanations)

# Changes an existing Explanation object.
# INPUT: Explanation object ("id", "question_id", "answer_id", "text")
# OUTPUT: Confirmation message
def change_explanation (request):
	if 'explanation' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	for deserialized_object in serializers.deserialize("json", request.GET['explanation']):
		deserialized_object.save()
	return JsonResponse({ "received": "yes" })

# Adds an explanation for a particular answer (1-4) of a particular question.
# INPUT: question_id, answer_id (1-4), and text
# OUTPUT: Confirmation message
def add_explanation (request):
	if 'question_id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	if 'answer_id' not in request.GET:
		return HttpResponse('answer_id not found in GET parameters')
	if 'text' not in request.GET:
		return HttpResponse('text not found in GET parameters')
	explanation = Explanation(question_id=request.GET['question_id'], answer_id=int(request.GET['answer_id']), text=request.GET['text'])
	explanation.save()
	return JsonResponse({ "received": "yes" })

# Computes and returns the Explanation that a particular student should receive for
# a particular question.
# INPUT: question_id, student_id
# OUTPUT: JSON dictionary: { "explanation": theExplanation, "exp_value": expectedValueOfExplanation }
def get_explanation_for_student (request):
	if 'question_id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	if 'student_id' not in request.GET:
		return HttpResponse('student_id not found in GET parameters')

	allExplanations = []
	allResultsForExplanations = []
	for explanation in Explanation.objects.filter(question_id=request.GET['question_id']).iterator():
		someResults = []
		for result in Result.objects.filter(explanation_id=explanation.id).iterator():
			someResults.append(result.value)
		allResultsForExplanations.append(someResults)
		allExplanations.append(explanation)
	selectedExplanation, exp_value = computeExplanation_Thompson(request.GET['student_id'], allExplanations, allResultsForExplanations)
	return JsonResponse({ "explanation": selectedExplanation, "exp_value": exp_value })

# Submits a scalar score (1-7) associated with a particular student who received a
# particular explanation.
# INPUT: explanation_id, student_id, value (1-7)
# OUTPUT: Confirmation message
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
	return JsonResponse({ "received": "yes" })
