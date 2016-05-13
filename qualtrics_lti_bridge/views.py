from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def home(request):
	return HttpResponse('Qualtrics LTI Bridge')


def lti_auth_error(request):
    raise PermissionDenied

