# sample views for example_app

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# basic HTTP response
# http://localhost:8000/example_app/
def index(request):
	return HttpResponse('Hello World')

# accepts a GET parameter named PARAM and prints its value
# http://localhost:8000/example_app/handle_get_param?PARAM=3
def handle_get_param(request):
	if 'PARAM' not in request.GET:
		return HttpResponse('PARAM not found in GET parameters')
	param_value = request.GET['PARAM']
	return HttpResponse('The value of PARAM is {}'.format(param_value))

# view that returns json
# http://localhost:8000/example_app/return_json
def return_json(request):
	output = {'quiz_version':1}
	return JsonResponse(output)

# http://localhost:8000/example_app/do_redirect
def do_redirect(request):
	return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

