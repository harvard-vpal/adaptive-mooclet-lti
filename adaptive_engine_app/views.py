# sample views for adaptive_engine_app

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .models import Component, Version

# basic HTTP response
# http://localhost:8000/adaptive_engine_app/
def index (request):
	return HttpResponse('Hello World')

def computeVersionOfComponent (student, versions):
	return { "version": versions[0].text }

def get_version_of_component (request):
	if 'component_id' not in request.GET:
		return HttpResponse('component_id not found in GET parameters')
	if 'student' not in request.GET:
		return HttpResponse('student not found in GET parameters')
	component_id = request.GET['component_id']
	student = request.GET['student']

	component = get_object_or_404(Component, pk=component_id)
	versions = []
	for version in Version.objects.filter(component_id=component_id).iterator():
		versions.append(version)
	return JsonResponse(computeVersionOfComponent(student, versions))

def submit_result_of_version (request):
	if 'version_id' not in request.GET:
		return HttpResponse('version_id not found in GET parameters')
	if 'student' not in request.GET:
		return HttpResponse('student not found in GET parameters')
	if 'result' not in request.GET:
		return HttpResponse('result not found in GET parameters')
	version_id = request.GET['version_id']
	student = request.GET['student']
	result = request.GET['result']
	return HttpResponse('The value of component_name is {}'.format(param_value))
