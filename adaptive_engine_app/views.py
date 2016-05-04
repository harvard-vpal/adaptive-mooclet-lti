# sample views for adaptive_engine_app

from .algorithms import computeVersionOfComponent_Thompson 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Component, Version, Result

def get_version_of_component (request):
	if 'name' not in request.GET:
		return HttpResponse('name not found in GET parameters')
	if 'student' not in request.GET:
		return HttpResponse('student not found in GET parameters')
	component_name = request.GET['name']
	student = request.GET['student']

	component = get_object_or_404(Component, name=component_name)
	allVersions = []
	allVersionResults = []
	for version in Version.objects.filter(component_id=component.component_id).iterator():
		versionResults = []
		for result in Result.objects.filter(id=version.id).iterator():
			versionResults.append(result.value)
		allVersionResults.append(versionResults)
		allVersions.append(version)
	selectedVersion, exp_value = computeVersionOfComponent_Thompson(student, allVersions, allVersionResults)
	return JsonResponse({ "text": selectedVersion.text, "version_id": selectedVersion.id, "exp_value": exp_value })

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

	# Make sure there's not already an entry in the database for this (student,version) combination
	if Result.objects.filter(student=student, version_id=version_id).count() == 0:
		result = Result(student=student, version_id=version_id, value=value)
		result.save()
		return HttpResponse('Ok')
	else:
		return HttpResponse('Error: attempt to submit duplicate entry!')
