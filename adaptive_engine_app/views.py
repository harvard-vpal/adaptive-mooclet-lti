# sample views for adaptive_engine_app

from .algorithms import computeVersionOfComponent_Thompson 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Component, Version, Result

def get_version_of_component (request):
	if 'component_id' not in request.GET:
		return HttpResponse('component_id not found in GET parameters')
	if 'student' not in request.GET:
		return HttpResponse('student not found in GET parameters')
	component_id = request.GET['component_id']
	student = request.GET['student']

	component = get_object_or_404(Component, pk=component_id)
	allVersions = []
	allVersionResults = []
	for version in Version.objects.filter(component_id=component_id).iterator():
		versionResults = []
		for result in Result.objects.filter(version_id=version.version_id).iterator():
			versionResults.append(result.value)
		allVerionResults.append(versionResults)
		allVersions.append(version)
	selectedVersion = computeVersionOfComponent_Thompson(student, allVersions, allVersionResults)
	return JsonResponse({ "text": selectedVersion.text, "version_id": selectedVersion.version_id })

def submit_result_of_version (request):
	if 'version_id' not in request.GET:
		return HttpResponse('version_id not found in GET parameters')
	if 'student' not in request.GET:
		return HttpResponse('student not found in GET parameters')
	if 'value' not in request.GET:
		return HttpResponse('value not found in GET parameters')
	
	version_id = request.GET['version_id']
	student = request.GET['student']
	value = float(request.GET['value'])

	result = Result(student=student, version_id=version_id, value=value)
	result.save()
	return HttpResponse('Ok')
