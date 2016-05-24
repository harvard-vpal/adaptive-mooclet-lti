from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def home(request):
	return HttpResponse('Adaptive Quiz LTI')


def lti_auth_error(request):
    raise PermissionDenied

