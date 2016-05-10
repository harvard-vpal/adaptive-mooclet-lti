# sample views for adaptive_engine_app

from .algorithms import computeExplanation_Thompson 
from .models import Question, Explanation, Result
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def add_question (request):
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
	question = Question(text=request.GET['text'], answer1=request.GET['answer1'], \
	                                              answer2=request.GET['answer2'], \
	                                              answer3=request.GET['answer3'], \
	                                              answer4=request.GET['answer4'])
	question.save()
	return JsonResponse({ "received": "yes" })

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

def get_explanation (request):
	if 'question_id' not in request.GET:
		return HttpResponse('question_id not found in GET parameters')
	if 'student_id' not in request.GET:
		return HttpResponse('student_id not found in GET parameters')

	question = get_object_or_404(Question, question_id=request.GET['question_id'])
	allExplanations = []
	allResultsForExplanations = []
	for explanation in Explanation.objects.filter(question_id=question.id).iterator():
		someResults = []
		for result in Result.objects.filter(explanation_id=explanation.id).iterator():
			someResults.append(result.value)
		allResultsForExplanations.append(someResults)
		allExplanations.append(explanation)
	selectedExplanation, exp_value = computeExplanation_Thompson(request.GET['student_id'], allExplanations, allResultsForExplanations)
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
