# sample views for adaptive_engine_app

from .algorithms import computeExplanationOfAnswer_Thompson 
from .models import Answer, Explanation, Result
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def get_explanation_for_answer (request):
	if 'answer_id' not in request.GET:
		return HttpResponse('answer_id not found in GET parameters')
	if 'student_id' not in request.GET:
		return HttpResponse('student_id not found in GET parameters')

	answer = get_object_or_404(Answer, answer_id=request.GET['answer_id'])
	allExplanations = []
	allResultsForExplanations = []
	for explanation in Explanation.objects.filter(answer_id=answer.id).iterator():
		someResults = []
		for result in Result.objects.filter(explanation_id=explanation.id).iterator():
			someResults.append(result.value)
		allResultsForExplanations.append(someResults)
		allExplanations.append(explanation)
	selectedExplanation, exp_value = computeExplanationOfAnswer_Thompson(request.GET['student_id'], allExplanations, allResultsForExplanations)
	return JsonResponse({ "text": selectedExplanation.text, "explanation_id": selectedExplanation.id, "exp_value": exp_value })

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
