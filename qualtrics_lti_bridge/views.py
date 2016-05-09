from django.core.exceptions import PermissionDenied


def lti_auth_error(request):
    raise PermissionDenied
